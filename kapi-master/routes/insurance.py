import os
from typing import Annotated, Optional, Dict
import uuid
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from starlette.responses import FileResponse
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY
from core.utils import commit_to_bd
from core.mail import send_new_payment_comprovative

from pydantic import UUID4, TypeAdapter, ValidationError
import crud
from auth import get_active_user, verify_role, get_role
from constants.roles import Role
from schemas import (
    Insurance,
    InsuranceUpdateDatetime,
    User,
    InsuranceCreateMulti,
    InsuranceCreateDatetime,
    InsuranceTeamSubGroup,
    InsuranceUpdateMulti,
    PagedResponse,
    PageQueries,
    InsuranceGroupped,
    InsuranceUpdate,
    InsuranceUpdateMultiStatus,
    InsuranceUpdateMultiGroups,
)
from models import InsuranceStatusEnum, InsuranceType, InsuredEntity
from sql_app import Session
from core.file_validator import FileUploadValidator, FileTypes, MAX_PDF_SIZE
from core.file_storage import FileStorageService, FileStorageDirectories
from datetime import datetime
from core.file_creation import (
    create_excel_with_athletes_insurances,
    create_excel_with_teams_insurances,
)

insurance_router = APIRouter(prefix="/insurances", tags=["Insurances"])
TA_LIST_IDS = TypeAdapter(list[str])
TA_INSURANCES_LIST = TypeAdapter(list[Insurance])
TEAM_INSURANCE_TYPE = "d8624297-f889-44e9-95cb-ba36a36d74f8"


@insurance_router.get(
    "/get-payment-guide",
    name="Returns payment guide of insurances",
)
async def get_payment_guide(
    team_id: str = Query(
        None,
        description="Team ID",
    ),
    sub_team_groups: list[str] = Query(
        None,
        description="Sub team groups",
    ),
    payment_comprovative: str = Query(
        None,
        description="Payment comprovative url",
    ),
    db: Session = Depends(),
):
    """
    Returns Insurance by ID
    """

    if payment_comprovative is not None:
        insurances_groups = crud.insurance.get_by_team_group(
            db=db,
            payment_comprovative_url=payment_comprovative,
        )
    else:
        insurances_groups = crud.insurance.get_by_team_group(
            db=db,
            sub_team_groups=sub_team_groups,
        )

    team = team = {"abbreviation": "NOTEAM"}
    if team_id is None and len(insurances_groups) != 0:
        insurances, n_insurances = crud.insurance.get_all(
            db=db, sub_team_group=insurances_groups[0][1], limit=1
        )
        team_id = (
            insurances[0].insured_entity.team_id
            if insurances[0].insured_entity.team_id is not None
            else insurances[0].insured_entity.athlete.team_id
        )

    team = crud.team.get(db=db, id=team_id)
    # Creating PDF
    fileName = "core/temp/payment_guide.pdf"
    pdf = canvas.Canvas(fileName, pagesize=A4)

    # Draw Image
    page_width, page_height = A4
    script_dir = os.path.dirname(__file__)
    pdf.drawImage(
        os.path.join(script_dir, f"../images/fplk_banner.webp"),
        0,
        page_height - 80,
        page_width,
        80,
        mask="auto",
    )

    # Write Title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 120,
        f"Guia de pagamento - {team.abbreviation}",
    )

    # Write IBAN
    pdf.setFont("Helvetica", 12)
    pdf.drawString(
        50,
        page_height - 150,
        "IBAN: 0033-0000-45424408682-05",
    )

    # Write Description
    style = getSampleStyleSheet()["Normal"]
    style.setFont = "Helvetica"
    style.textColor = colors.black
    style.fontSize = 16
    style.leading = 18
    style.alignment = TA_JUSTIFY
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    data = [["Quantidade", "Tipo de seguro", "Preço unitário", "Preço total"]]
    cache = {}
    for group in insurances_groups:
        if group[2] not in cache:  # type: ignore
            insurance_type: InsuranceType = crud.insurance_type.get(db=db, id=group[2])  # type: ignore
            cache[group[2]] = {  # type: ignore
                "number": 0,
                "fee": insurance_type.fee,  # type: ignore
                "name": insurance_type.name,  # type: ignore
            }
        cache[group[2]]["number"] = cache[group[2]]["number"] + group[0]  # type: ignore
    for c in cache:
        data.append(
            [
                str(cache[c]["number"]),
                str(cache[c]["name"]),
                str(cache[c]["fee"]) + "€",
                str(cache[c]["fee"] * cache[c]["number"]) + "€",
            ]
        )
    data.append(["", "", "", ""])
    data.append(
        [
            "",
            "",
            "Total:",
            str(sum(cache[c]["fee"] * cache[c]["number"] for c in cache)) + "€",
        ]
    )

    known_cols_width = max(
        [
            sum(
                (stringWidth(col + "vvv", "Helvetica-Bold", 16))
                for col in (row[:0] + row[2:])
            )
            for row in data
        ]
    )
    remaining_width = page_width - 100 - known_cols_width
    known_cols_height = (len(data) - 1) * 20
    remaining_height = page_height - 350 - known_cols_height
    table = Table(
        data,
        colWidths=[None, remaining_width, None, None],
        rowHeights=[None] * (len(data) - 2) + [remaining_height, None],
    )
    table.setStyle(table_style)

    table.wrapOn(pdf, page_width - 100, page_height - 350)
    print(known_cols_height)
    table.drawOn(pdf, 50, 190)

    # Save PDF
    pdf.save()
    return FileResponse(
        fileName, media_type="application/octet-stream", filename=fileName
    )


@insurance_router.get(
    "/get-excel",
    name="Returns excel of insurances of a group",
)
async def get_excel(
    year: int | None = Query(
        default=None,
        description="Year of the insurances",
    ),
    insurance_group_id: UUID4 = Query(
        default=None, description="Show excel of all athletes of insurance group"
    ),
    team_id: UUID4 | None = Query(
        default=None,
        description="ID of the team",
    ),
    name: str | None = Query(
        default=None,
        description="Name of the insured",
    ),
    insurance_type: list[str] | None = Query(
        default=None,
        description="Type of the insurance",
    ),
    team_abbreviation: str | None = Query(
        default=None,
        description="Abbreviation of a insured team of the insured",
    ),
    group: str | None = Query(
        default=None,
        description="Name of the insurance group",
    ),
    db: Session = Depends(),
    current_user: User = Depends(get_active_user),
):
    verify_role(current_user, [Role.ADMIN["name"]])

    insurances, n_results = crud.insurance.get_all(
        db=db,
        insurance_group_id=(
            str(group)
            if group is not None
            else str(insurance_group_id) if insurance_group_id is not None else None
        ),
        team_id=str(team_id) if team_id is not None else None,
        status=[InsuranceStatusEnum.accepted],
        year=year,
        only_athletes=True,
        order_by_name=True,
        name=name,
        team_abbreviation=team_abbreviation,
        insurance_type=insurance_type,
        limit=-1,
    )
    if insurance_group_id is not None:
        insurance_group = crud.insurance_group.get(db=db, id=insurance_group_id)
        return create_excel_with_athletes_insurances(
            insurance_group_name=insurance_group.name, insurances=insurances, n_results=n_results  # type: ignore
        )
    if team_id is not None:
        team = crud.team.get(db=db, id=team_id)  # type: ignore
        return create_excel_with_athletes_insurances(
            team_name=f"{team.name} ({team.abbreviation})", insurances=insurances, n_results=n_results  # type: ignore
        )
    return create_excel_with_athletes_insurances(insurances=insurances, n_results=n_results)  # type: ignore


@insurance_router.get(
    "/get-teams-excel",
    name="Returns excel of insurances of a group",
)
async def get_teams_excel(
    year: int | None = Query(
        default=None,
        description="Year of the insurances",
    ),
    db: Session = Depends(),
    current_user: User = Depends(get_active_user),
):
    verify_role(current_user, [Role.ADMIN["name"]])

    insurances, n_results = crud.insurance.get_all(
        db=db,
        status=[InsuranceStatusEnum.accepted],
        year=year,
        order_by_name=True,
        insurance_type=[TEAM_INSURANCE_TYPE],
        limit=-1,
    )
    return create_excel_with_teams_insurances(insurances=insurances, n_results=n_results)  # type: ignore


@insurance_router.get(
    "",
    response_model=PagedResponse[Insurance],
    name="Returns All Insurances filtered by a query",
)
async def get_all(
    is_federated: Optional[bool] = None,
    insurance_type: list[str] | None = Query(
        default=None,
        description="ID of the insurance type",
    ),
    year: int | None = Query(
        default=None,
        description="Year of the insurance",
    ),
    name: str | None = Query(
        default=None,
        description="Name of the insured",
    ),
    athlete_name: str | None = Query(
        default=None,
        description="Name of the athlete",
    ),
    status: list[InsuranceStatusEnum] | None = Query(
        default=None,
        description="Status of the insurance",
    ),
    team_abbreviation: str | None = Query(
        default=None,
        description="Abbreviation of a insured team of the insured",
    ),
    payment_comprovative_url: str | None = Query(
        default=None,
        description="Name of the payment comprovative file",
    ),
    group: str | None = Query(
        default=None,
        description="Name of the insurance group",
    ),
    sub_team_group: str | None = Query(
        default=None,
        description="Name of the sub team group",
    ),
    insurance_id: str | None = Query(
        default=None,
        description="ID of the insurance",
    ),
    pagination: PageQueries = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns Insurances List
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    if is_federated is not None:
        is_federated = is_federated is True
    if year is not None:
        year = year if year > 1900 else None
    if name is not None:
        name = name if name.strip() != "" else None
    if team_abbreviation is not None:
        team_abbreviation = (
            team_abbreviation if team_abbreviation.strip() != "" else None
        )
    if group is not None:
        group = group if group.strip() != "" else None
    if payment_comprovative_url is not None:
        payment_comprovative_url = (
            payment_comprovative_url if payment_comprovative_url.strip() != "" else None
        )

    insurances_db, n_insurances = crud.insurance.get_all(
        db=db,
        insurance_type=insurance_type,
        year=year,
        status=status,
        name=name,
        athlete_name=athlete_name,
        team_abbreviation=team_abbreviation,
        insurance_group_id=group,
        sub_team_group=sub_team_group,
        payment_comprovative_url=payment_comprovative_url,
        insurance_id=insurance_id,
        page=pagination.skip,
        limit=pagination.limit,
    )

    return PagedResponse(
        results=TA_INSURANCES_LIST.validate_python(insurances_db),
        n_results=n_insurances,
    )


@insurance_router.get(
    "/get-groupped",
    response_model=PagedResponse[InsuranceGroupped],
    name="Returns All Insurances groupped by payment comprovatives or by insurance groups",
)
async def get_groupped(
    insurance_type: list[str] | None = Query(
        default=None,
        description="ID of the insurance type",
    ),
    year: int | None = Query(
        default=None,
        description="Year of the insurance",
    ),
    status: list[InsuranceStatusEnum] | None = Query(
        default=None,
        description="Status of the insurance",
    ),
    name: str | None = Query(
        default=None,
        description="Name of the insured",
    ),
    team_abbreviation: str | None = Query(
        default=None,
        description="Abbreviation of a insured team of the insured",
    ),
    group: str | None = Query(
        default=None,
        description="Name of the insurance group",
    ),
    group_by: str = Query(
        default="payment_comprovatives",
        description="Group insurances by payment comprovatives or insurance groups",
    ),
    pagination: PageQueries = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.ADMIN["name"]])
    if year is not None:
        year = year if year > 1900 else None
    if name is not None:
        name = name if name.strip() != "" else None
    if team_abbreviation is not None:
        team_abbreviation = (
            team_abbreviation if team_abbreviation.strip() != "" else None
        )
    if group is not None:
        group = group if group.strip() != "" else None

    results, n_results = crud.insurance.get_groupped(
        db=db,
        insurance_type=insurance_type,
        year=year,
        name=name,
        team_abbreviation=team_abbreviation,
        group=group,
        status=[s.value for s in status] if status is not None else None,
        group_by=group_by,
        page=pagination.skip,
        limit=pagination.limit,
    )

    insurances = []
    teams_cache = {}
    for result in results:
        team_ids = list(
            set(
                str(r)
                for r in (result[8] or "").split(",") + (result[9] or "").split(",")
                if r is not None and r.strip() != ""
            )
        )

        for id in team_ids:
            if id not in teams_cache:
                try:
                    team = crud.team.get(db=db, id=id)
                except HTTPException:
                    team = None
                teams_cache[id] = team
        insurances.append(
            InsuranceGroupped(
                number_insured=result[0],
                payment_comprovative_url=(
                    result[1] if group_by == "payment_comprovatives" else None
                ),
                insurance_group_id=(
                    result[1] if group_by != "payment_comprovatives" else None
                ),
                number_medical_exams=result[2] if result[2] is not None else 0,
                number_payment_comprovatives=result[3] if result[3] is not None else 0,
                number_pending=result[4] if result[4] is not None else 0,
                number_accepted=result[5] if result[5] is not None else 0,
                number_other_status=result[6] if result[6] is not None else 0,
                profile_pictures=str(result[7]).split(","),
                team_ids=team_ids,
                teams=[teams_cache[id] for id in team_ids],
                insurance_group_name=result[10] if result[10] is not None else "",
            )
        )

    return PagedResponse(
        results=insurances,
        n_results=n_results,
    )


@insurance_router.get(
    "/teams/{team}",
    response_model=list[InsuranceTeamSubGroup],
    name="Returns All Insurances of the team grouped by the sub group",
)
async def get_by_sub_team(
    team: str,
    year: int | None = Query(
        default=None,
        description="Year covered by the insurance",
    ),
    sub_team_group: str | None = Query(
        default=None,
        description="Sub team id",
    ),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])
    results = crud.insurance.get_by_team_group(
        db=db, team_id=team, year=year, sub_team_group=sub_team_group  # type: ignore
    )

    insurance_groups: list[InsuranceTeamSubGroup] = []
    cache_insurance_types: Dict[str, InsuranceType] = {}
    for r in results:
        if r[2] not in cache_insurance_types:
            insurance_type = crud.insurance_type.get(db=db, id=r[2])
            cache_insurance_types[r[2]] = insurance_type
        insurance_groups.append(
            InsuranceTeamSubGroup(
                number_insured=r[0],
                sub_team_group=str(r[1]),
                insurance_type_id=r[2],
                insurance_type=cache_insurance_types[r[2]],
                number_medical_exams=r[3] if r[3] is not None else 0,
                number_payment_comprovatives=r[4] if r[4] is not None else 0,
                number_pending=r[5] if r[5] is not None else 0,
                number_accepted=r[6] if r[6] is not None else 0,
                number_other_status=r[7] if r[7] is not None else 0,
                profile_pictures=str(r[8]).split(","),
            )
        )

    return insurance_groups


@insurance_router.get(
    "/{insurance_id}", response_model=Insurance, name="Returns Insurance by ID"
)
async def get(
    insurance_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns Insurance by ID
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.insurance.get(db=db, id=insurance_id)  # type: ignore


@insurance_router.post(
    "/multi",
    name="Creates Multiple Insurances for Athletes",
    status_code=status.HTTP_201_CREATED,
)
async def create_multi(
    insurance_in: InsuranceCreateMulti,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates Multiple Insurances for Athletes
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    if crud.insurance_type.get(db=db, id=insurance_in.insurance_type_id) is None:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"insurance_type": "Insurance type Not Found"},
        )

    if (
        insurance_in.insurance_group_id
        and insurance_in.insurance_group_id != ""
        and crud.insurance_group.get(db=db, id=insurance_in.insurance_group_id) is None  # type: ignore
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"insurance_group": "Insurance Group Not Found"},
        )

    insurances_to_create = []
    insurance_end_date = datetime(
        insurance_in.start_date.year,
        12,
        31,
    )
    for insured_entity_id in insurance_in.insured_entities_ids:
        insured_entity_db = crud.insured_entity.get(db=db, id=insured_entity_id)  # type: ignore
        if insured_entity_db is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail={"insured_entity": "Insured entity not found"},
            )

        # Check permissions for coach user
        if get_role(current_user) == "COACH":
            check_permissions_for_coach(
                db=db, current_user=current_user, insured_entity_db=insured_entity_db
            )

        insurances_to_create.append(
            InsuranceCreateDatetime(
                start_date=insurance_in.start_date,  # type: ignore
                end_date=insurance_end_date,
                insured_entity_id=insured_entity_id,
                insurance_type_id=insurance_in.insurance_type_id,
                insurance_group_id=insurance_in.insurance_group_id,
                sub_team_group=insurance_in.sub_team_group,
                status=InsuranceStatusEnum.pending.value,
            )
        )
    crud.insurance.multi_create(db=db, objs_in=insurances_to_create)
    return


@insurance_router.put(
    "/{insurance_id}/medical-exam",
    response_model=Insurance,
    name="Saves medical exam",
    dependencies=[
        Depends(
            FileUploadValidator(max_size_mb=MAX_PDF_SIZE, allowed_types=[FileTypes.PDF])
        )
    ],
)
async def upload_medical_exam(
    insurance_id: str,
    file: Annotated[UploadFile, Body(..., description="Medical exam file")],
    background_tasks: BackgroundTasks,
    aux: str | None = Form(default=None),
    file_storage_service: FileStorageService = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Uploads medical exam
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    insurance: Insurance = crud.insurance.get(db=db, id=insurance_id)  # type: ignore
    if insurance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # Check permissions for coach user
    if get_role(current_user) == "COACH":
        check_permissions_for_coach(
            db=db, current_user=current_user, insured_entity_db=insurance.insured_entity
        )

    file_name = file_storage_service.get_file_name(
        directory=FileStorageDirectories.MEDICAL_EXAMS,
        obj_id=uuid.uuid4(),
        file=file,
    )
    if insurance.medical_exam_url is not None:
        background_tasks.add_task(
            file_storage_service.delete, insurance.medical_exam_url  # type: ignore
        )
    background_tasks.add_task(file_storage_service.upload, file_name, file)

    return crud.insurance.update(
        db=db,
        db_obj=insurance,
        obj_in=InsuranceUpdateDatetime(medical_exam_url=file_name),
    )


@insurance_router.put(
    "/{insurance_id}/coach-certificate",
    response_model=Insurance,
    name="Saves medical exam",
    dependencies=[
        Depends(
            FileUploadValidator(max_size_mb=MAX_PDF_SIZE, allowed_types=[FileTypes.PDF])
        )
    ],
)
async def upload_coach_certificate(
    insurance_id: str,
    file: Annotated[UploadFile, Body(..., description="Coach certificate")],
    background_tasks: BackgroundTasks,
    aux: str | None = Form(default=None),
    file_storage_service: FileStorageService = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Uploads coach certificate
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    insurance: Insurance = crud.insurance.get(db=db, id=insurance_id)  # type: ignore

    # Check permissions for coach user
    if get_role(current_user) == "COACH":
        check_permissions_for_coach(
            db=db, current_user=current_user, insured_entity_db=insurance.insured_entity
        )

    file_name = file_storage_service.get_file_name(
        directory=FileStorageDirectories.COACH_CERTIFICATES,
        obj_id=uuid.uuid4(),
        file=file,
    )
    if insurance.coach_certificate_url is not None:
        background_tasks.add_task(
            file_storage_service.delete, insurance.coach_certificate_url  # type: ignore
        )
    background_tasks.add_task(file_storage_service.upload, file_name, file)

    return crud.insurance.update(
        db=db,
        db_obj=insurance,
        obj_in=InsuranceUpdateDatetime(coach_certificate_url=file_name),
    )


@insurance_router.put(
    "/multi/payment-comprovative",
    name="Saves payment comprovative for multiple insurances",
    dependencies=[
        Depends(
            FileUploadValidator(max_size_mb=MAX_PDF_SIZE, allowed_types=[FileTypes.PDF])
        )
    ],
)
def upload_payment_comprovative_for_multiple_insurances(
    file: Annotated[UploadFile, Body(..., description="Payment comprovative file")],
    background_tasks: BackgroundTasks,
    sub_team_ids_in: str = Form(...),
    file_storage_service: FileStorageService = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Saves payment comprovative for multiple insurances
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])
    sub_team_ids = []
    try:
        sub_team_ids = TA_LIST_IDS.validate_json(sub_team_ids_in)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.json()
        )

    if len(sub_team_ids) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"sub_teams_ids": "No IDs found"},
        )

    file_name = file_storage_service.get_file_name(
        directory=FileStorageDirectories.PAYMENTS_COMPROVATIVES,
        obj_id=uuid.uuid4(),
        file=file,
    )
    background_tasks.add_task(file_storage_service.upload, file_name, file)
    crud.insurance.update_multiple_payment_comprovative_url_by_sub_team(
        db=db,
        sub_team_ids=sub_team_ids,
        file_name=file_name,
        background_tasks=background_tasks,
        file_storage_service=file_storage_service,
    )
    return


@insurance_router.put(
    "/multi/status-update",
    name="Updates Multiple Stauts of Insurances",
)
async def update_multi_status(
    insurances_in: InsuranceUpdateMultiStatus,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Multiple Status of Insurances
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    insurances_db, n_results = crud.insurance.get_all(
        db=db, ids=insurances_in.ids, limit=-1
    )

    for insurance in insurances_db:
        insurance.status = insurances_in.status.value
        if insurances_in.status != InsuranceStatusEnum.accepted:
            insurance.notes = insurances_in.notes
        else:
            add_federation_number(db=db, insurance=insurance)
        db.add(insurance)
    commit_to_bd(session_db=db)

    return


@insurance_router.put(
    "/multi/insurance-groups",
    name="Updates Multiple Groups of Insurances",
)
async def update_multi_groups(
    insurances_in: InsuranceUpdateMultiGroups,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Multiple Groups of Insurances
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    insurances_db, n_results = crud.insurance.get_all(
        db=db, ids=insurances_in.ids, limit=-1
    )

    if insurances_in.insurance_group_id is not None:
        insurance_group_db = crud.insurance_group.get(
            db=db, id=insurances_in.insurance_group_id
        )
        if insurance_group_db is None:
            raise HTTPException(404)

    for insurance in insurances_db:
        insurance.insurance_group_id = insurances_in.insurance_group_id  # type: ignore
        db.add(insurance)
    commit_to_bd(session_db=db)

    return


@insurance_router.put(
    "/multi/{sub_team_group}",
    name="Updates Multiple Insurances for Athletes",
)
async def update_multi(
    sub_team_group: str,
    insurance_in: InsuranceUpdateMulti,
    background_tasks: BackgroundTasks,
    file_storage_service: FileStorageService = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Multiple Insurances for Athletes
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    if crud.insurance_type.get(db=db, id=insurance_in.insurance_type_id) is None:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"insurance_type": "Insurance type Not Found"},
        )

    insurances_db, n_results = crud.insurance.get_all(
        db=db, sub_team_group=sub_team_group, limit=-1
    )
    ids_db = []

    insurance_end_date = datetime(
        insurance_in.start_date.year,
        12,
        31,
    )
    for insurance in insurances_db:
        # Check permissions for coach user
        if get_role(current_user) == "COACH":
            check_permissions_for_coach(
                db=db,
                current_user=current_user,
                insured_entity_db=insurance.insured_entity,
            )
        ids_db.append(str(insurance.insured_entity_id))

    insurances_to_create = []
    insurances_udpated = []
    for insured_entity_id in insurance_in.insured_entities_ids:
        insured_entity_db = crud.insured_entity.get(db=db, id=insured_entity_id)  # type: ignore
        if insured_entity_db is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail={"insured_entity": "Insured entity not found"},
            )
        # Update insurances maintained
        if insured_entity_id in ids_db:
            insurances_udpated.append(insured_entity_id)
            for insurance in insurances_db:
                if insured_entity_id == str(insurance.insured_entity_id):
                    crud.insurance.update(
                        db=db,
                        db_obj=insurance,
                        obj_in=InsuranceUpdateDatetime(
                            start_date=insurance_in.start_date,  # type: ignore
                            end_date=insurance_end_date,
                            insurance_type_id=insurance_in.insurance_type_id,
                            status=InsuranceStatusEnum.pending.value,
                            sub_team_group=sub_team_group,
                        ),
                    )
        # Get list of insurances to create
        else:
            insurances_to_create.append(
                InsuranceCreateDatetime(
                    start_date=insurance_in.start_date,  # type: ignore
                    end_date=insurance_end_date,
                    insured_entity_id=insured_entity_id,
                    insurance_type_id=insurance_in.insurance_type_id,
                    sub_team_group=sub_team_group,
                    status=InsuranceStatusEnum.pending.value,
                )
            )
    # Create insurances added
    crud.insurance.multi_create(db=db, objs_in=insurances_to_create)

    # Delete insurances removed
    for id in ids_db:
        if id not in insurance_in.insured_entities_ids:
            for insurance in insurances_db:
                if id == str(insurance.insured_entity_id):
                    if insurance.payment_comprovative_url is not None:
                        results, n_results = crud.insurance.get_all(db=db, payment_comprovative_url=insurance.payment_comprovative_url, limit=-1)  # type: ignore
                        if n_results == 1:
                            background_tasks.add_task(
                                file_storage_service.delete,
                                insurance.payment_comprovative_url,  # type: ignore
                            )
                    if insurance.medical_exam_url is not None:
                        background_tasks.add_task(
                            file_storage_service.delete, insurance.medical_exam_url  # type: ignore
                        )
                    crud.insurance.delete(db=db, id=insurance.id)  # type: ignore

    return


@insurance_router.put(
    "/{insurance_id}/payment-comprovative",
    response_model=Insurance,
    name="Saves payment comprovative",
    dependencies=[
        Depends(
            FileUploadValidator(max_size_mb=MAX_PDF_SIZE, allowed_types=[FileTypes.PDF])
        )
    ],
)
async def upload_payment_comprovative(
    insurance_id: str,
    file: Annotated[UploadFile, Body(..., description="Payment comprovative file")],
    background_tasks: BackgroundTasks,
    aux: str | None = Form(default=None),
    file_storage_service: FileStorageService = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Uploads payment comprovative
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    insurance: Insurance = crud.insurance.get(db=db, id=insurance_id)  # type: ignore
    if insurance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    file_name = file_storage_service.get_file_name(
        directory=FileStorageDirectories.PAYMENTS_COMPROVATIVES,
        obj_id=uuid.uuid4(),
        file=file,
    )
    if insurance.payment_comprovative_url is not None:
        background_tasks.add_task(
            file_storage_service.delete, insurance.payment_comprovative_url  # type: ignore
        )
    background_tasks.add_task(file_storage_service.upload, file_name, file)

    team = None
    if insurance.insured_entity.team_id is None:
        team = insurance.insured_entity.athlete.team
    else:
        team = insurance.insured_entity.team

    background_tasks.add_task(
        send_new_payment_comprovative, file_name=file_name, team=team
    )

    return crud.insurance.update(
        db=db,
        db_obj=insurance,
        obj_in=InsuranceUpdateDatetime(payment_comprovative_url=file_name),
    )


@insurance_router.put(
    "/{sub_team_group}/contract",
    name="Saves insurance's contract",
    dependencies=[
        Depends(
            FileUploadValidator(max_size_mb=MAX_PDF_SIZE, allowed_types=[FileTypes.PDF])
        )
    ],
)
async def upload_contract(
    sub_team_group: str,
    file: Annotated[UploadFile, Body(..., description="Payment comprovative file")],
    background_tasks: BackgroundTasks,
    aux: str | None = Form(default=None),
    file_storage_service: FileStorageService = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Uploads insurnace's contract
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    insurances, n_insurances = crud.insurance.get_all(
        db=db, sub_team_group=sub_team_group
    )

    file_name = file_storage_service.get_file_name(
        directory=FileStorageDirectories.CONTRACTS,
        obj_id=uuid.uuid4(),
        file=file,
    )
    cache_file_names = []
    background_tasks.add_task(file_storage_service.upload, file_name, file)
    for insurance in insurances:
        if insurance.contract_url is not None:
            if insurance.contract_url not in cache_file_names:
                cache_file_names.append(insurance.contract_url)
                background_tasks.add_task(
                    file_storage_service.delete, insurance.contract_url  # type: ignore
                )
        insurance.contract_url = file_name  # type: ignore
        db.add(insurance)

    commit_to_bd(session_db=db)

    return


@insurance_router.put(
    "/{insurance_id}", response_model=Insurance, name="Returns Insurance by ID"
)
async def update(
    insurance_id: UUID4,
    insurance_in: InsuranceUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Update a single Insurace
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    insurance_db = crud.insurance.get(db=db, id=insurance_id)

    if insurance_db is None:
        raise HTTPException(status_code=404, detail="Insurance Not Found")

    format = "%d-%m-%Y"
    insurance_start_date = None
    insurance_end_date = None
    if (
        insurance_in.insurance_date is not None
        and insurance_in.insurance_date.strip() != ""
    ):
        try:
            insurance_start_date = datetime.strptime(
                insurance_in.insurance_date, format
            )
            insurance_end_date = datetime(
                insurance_start_date.year,
                12,
                31,
            )
        except:
            raise HTTPException(
                status_code=400,
                detail={"insurance_date": "The insurance must have a valid date"},
            )

    insurance_to_update = InsuranceUpdateDatetime()
    if insurance_start_date:
        insurance_to_update.start_date = insurance_start_date
        insurance_to_update.end_date = insurance_end_date
    if insurance_in.status:
        insurance_to_update.status = insurance_in.status.value
    if insurance_in.insurance_type_id:
        insurance_to_update.insurance_type_id = insurance_in.insurance_type_id
    if insurance_in.insurance_group_id:
        insurance_to_update.insurance_group_id = insurance_in.insurance_group_id
    if insurance_in.notes is not None:
        insurance_to_update.notes = insurance_in.notes

    if insurance_in.status == InsuranceStatusEnum.accepted:
        add_federation_number(db=db, insurance=insurance_db)
        commit_to_bd(session_db=db)

    return crud.insurance.update(db=db, db_obj=insurance_db, obj_in=insurance_to_update)


# @insurance_router.delete("/{insurance_id}", name="Deletes Insurance by ID")
# async def delete(
#     insurance_id: str,
#     current_user: User = Depends(get_active_user),
#     db: Session = Depends(),
# ):
#     """
#     Deletes Insurance by ID
#     """
#     verify_role(current_user, [Role.ADMIN["name"]])

#     crud.insurance.delete(db=db, id=insurance_id)
#     return


def check_permissions_for_coach(
    db: Session, current_user: User, insured_entity_db: InsuredEntity
):
    authorized = True
    # if insurance.status != InsuranceStatusEnum.pending.value:
    #     authorized = False
    # insured_entity_db = insurance.insured_entity
    # if insured_entity_db is None:
    #     authorized = False
    if insured_entity_db.athlete_id is not None:  # type: ignore
        athlete = crud.athlete.get(db=db, id=insured_entity_db.athlete_id)  # type: ignore
        if athlete is None or athlete.team.coach_id != current_user.id:
            authorized = False
    if insured_entity_db.team_id is not None:  # type: ignore
        team = crud.team.get(db=db, id=insured_entity_db.team_id)  # type: ignore
        if team.coach_id != current_user.id:  # type: ignore
            authorized = False
    if insured_entity_db.user_id is not None:  # type: ignore
        user = crud.user.get(db=db, id=insured_entity_db.user_id)  # type: ignore
        if user.id != current_user.id:  # type: ignore
            authorized = False
    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient Permissions.",
        )


def add_federation_number(db: Session, insurance: Insurance):
    if insurance.insured_entity.athlete_id is not None:
        athlete = crud.athlete.get(db=db, id=insurance.insured_entity.athlete_id)
        private_info = crud.private_info.get(db=db, id=athlete.private_info_id)
        if private_info.federation_number is None:
            private_info.federation_number = (
                crud.private_info.get_highest_fed_number(db=db) + 1
            )
            db.add(private_info)
