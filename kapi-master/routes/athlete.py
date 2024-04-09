import datetime
from math import ceil
from typing import Annotated, Dict, List, Union

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
from pydantic import TypeAdapter, UUID4

import crud
from auth import (
    can_edit_athlete,
    get_active_user,
    get_active_user_or_none,
    get_role,
    verify_role,
)
from constants.roles import Role
from core.utils import validate_uuid4
from core.file_validator import IMAGES_TYPES, FileUploadValidator, MAX_IMAGE_SIZE
from core.file_storage import FileStorageDirectories, FileStorageService
from schemas import (
    Athlete,
    AthleteAdmin,
    AthleteAdminUpdate,
    AthleteCompleteCreate,
    AthletePrivate,
    AthletePrivatePage,
    AthleteTournaments,
    AthleteUpdate,
    Belt,
    InsuredEntityCreate,
    User,
    PageQueries,
    PagedResponse,
)
from schemas.athlete import Tournament as TournamentAthlete
from sql_app import Session

athlete_router = APIRouter(prefix="/athletes", tags=["Athlete"])


TA_ATHLETE_ADMIN = TypeAdapter(AthleteAdmin)
TA_ATHLETE = TypeAdapter(Athlete)
TA_ATHLETE_PRIVATE = TypeAdapter(AthletePrivate)
TA_ATHLETE_ADMIN_LIST = TypeAdapter(list[AthleteAdmin])
TA_ATHLETE_LIST = TypeAdapter(list[Athlete])
TA_ATHLETE_PRIVATE_LIST = TypeAdapter(list[AthletePrivate])
TA_ATHLETE_TOURNAMENTS = TypeAdapter(AthleteTournaments)
TA_TOURNAMENT = TypeAdapter(TournamentAthlete)


@athlete_router.get(
    "/name/{name}",
    response_model=List[AthletePrivate],
    name="Returns all athletes based on the name",
)
async def get_all(
    name: str,
    federation_requests_year: int | None = None,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns all Athletes based on the name
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.athlete.get_by_name(
        db=db,
        soft_deleted=False,
        name=name,
        federation_requests_year=federation_requests_year,
    )


@athlete_router.get(
    "",
    response_model=PagedResponse[AthleteAdmin],
    name="Returns all athletes based on the query",
)
async def get_query_new(
    teams: list[str] = Query(
        default=[],
        description='ID of team of the athletes, string "noteam" for athletes without team',
    ),
    team_abbreviation: str | None = Query(
        default=None,
        description="Abbreviation of the team",
    ),
    name: str | None = Query(default=None, description="Name of the Atlhete"),
    age: int | None = Query(default=None, description="Age of the Atlhete"),
    age_min: int | None = Query(
        default=None, description="Athletes' age must be equal or superior than this"
    ),
    age_max: int | None = Query(
        default=None, description="Athletes' age must be equal or inferior than this"
    ),
    on_team: bool | None = Query(default=None, description="Athlete is on a team"),
    is_male: bool | None = Query(default=None, description="Athlete is masculine"),
    regions: list[str] = Query(default=[], description="Athletes' team's region"),
    districts: list[str] = Query(default=[], description="Athletes' team's district"),
    adapted: bool | None = Query(default=None, description="Athletes is adapted"),
    belts: list[str] = Query(default=[], description="Graduation level of the athlete"),
    federated: bool | None = Query(
        default=None, description="Athlete is federated or not"
    ),
    federation_number: int | None = Query(
        default=None, description="Federation number of the athlete"
    ),
    only_coaches: bool = Query(
        default=False, description="Athlete must also be a coach"
    ),
    soft_deleted: bool | None = Query(
        default=False, description="Show soft deleted athletes"
    ),
    order_by: str = Query(default="name", description="How to order the athletes"),
    pagination: PageQueries = Depends(),
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Returns all Athletes based on the query
    """

    athletes, n_results = crud.athlete.get_query_new(
        db=db,
        teams=teams,
        team_abbreviation=team_abbreviation,
        name=name,
        age=age,
        age_min=age_min,
        age_max=age_max,
        on_team=on_team,
        regions=regions,
        districts=districts,
        adapted=adapted,
        federated=federated,
        is_male=is_male,
        federation_number=federation_number,
        only_coaches=only_coaches,
        soft_deleted=soft_deleted,
        belts=belts,
        order_by=order_by,
        limit=pagination.limit,
        skip=pagination.skip,
    )

    return PagedResponse(
        n_results=n_results,
        results=get_athletes_by_role(current_user=current_user, athletes=athletes),
    )


@athlete_router.get(
    "/query",
    response_model=AthletePrivatePage,
    name="Returns all athletes based on the query",
)
async def get_all_query(
    team: str,
    name: str,
    federated: bool,
    page: int,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns all Athletes based on the query
    """

    verify_role(current_user, [Role.ADMIN["name"]])

    if team == "1":
        team = None

    if team is not None and not validate_uuid4(team):
        raise HTTPException(404, "ID Not Found")

    limit = 30
    athletes = crud.athlete.get_by_name_and_team_query(
        db=db, name=name, team_id=team, federated=federated, page=page - 1, limit=limit
    )

    count = crud.athlete.get_by_name_and_team_query_count(
        db=db, name=name, team_id=team, federated=federated
    )

    athlete_page = AthletePrivatePage(
        athletes=athletes,
        skip=0,
        limit=limit,
        total_elements=count,
        total_pages=ceil(count / limit),
        current_page=page,
    )
    return athlete_page


@athlete_router.get(
    "/team/{team_id}",
    response_model=List[AthletePrivate],
    name="Returns all athletes of the team",
)
async def get_by_team(
    team_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns all Athletes of the team
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    id_to_search = team_id
    if team_id == "null":
        id_to_search = None
    return crud.athlete.get_by_team(db=db, team_id=id_to_search)


@athlete_router.get(
    "/team/abbreviation/{abbreviation}",
    response_model=List[AthletePrivate],
    name="Returns all athletes of the team",
)
async def get_by_team_abbreviation(
    abbreviation: str,
    federation_requests_year: int | None = None,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns all Athletes of the team
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.athlete.get_by_abbreviation(
        db=db,
        abbreviation=abbreviation,
        federation_requests_year=federation_requests_year,
    )


@athlete_router.get(
    "/team/coach/{team_id}/{federated}",
    response_model=List[AthletePrivate],
    name="Returns all athletes of the team",
)
async def get_by_team_for_coach(
    team_id: str,
    federated: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns all Athletes of the team
    """

    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])
    id_to_search = team_id
    if team_id == "null":
        id_to_search = None
    failed = False
    if current_user.user_role.role.name == "COACH":
        try:
            team_db = crud.team.get(db=db, id=team_id)
            if team_db is not None and team_db.coach_id == current_user.id:
                if federated == "null":
                    return crud.athlete.get_by_team(db=db, team_id=id_to_search)
                if federated == "true":
                    return crud.athlete.get_by_team_federated(
                        db=db, team_id=id_to_search, federated=True
                    )
                if federated == "false":
                    return crud.athlete.get_by_team_federated(
                        db=db, team_id=id_to_search, federated=False
                    )
                failed = True
        except Exception as e:
            print(e)
    else:
        try:
            if federated == "null":
                return crud.athlete.get_by_team(db=db, team_id=id_to_search)
            if federated == "true":
                return crud.athlete.get_by_team_federated(
                    db=db, team_id=id_to_search, federated=True
                )
            if federated == "false":
                return crud.athlete.get_by_team_federated(
                    db=db, team_id=id_to_search, federated=False
                )
            failed = True
        except Exception as e:
            print(e)
    if failed:
        raise HTTPException(400)
    raise HTTPException(401)


@athlete_router.get(
    "/number/{athlete_number}",
    response_model=Union[Athlete, None],
    name="Returns athlete by ID",
)
async def get_by_number(athlete_number: int, db: Session = Depends()):
    """
    Returns Athlete by ID
    """
    return crud.athlete.get_by_number(db=db, number=athlete_number)


@athlete_router.get(
    "/{athlete_id}", response_model=AthleteAdmin, name="Returns athlete by ID"
)
async def get(
    athlete_id,
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Returns Athlete by ID
    """
    return get_athlete_by_role(
        athlete=crud.athlete.get(db=db, id=athlete_id),
        current_user=current_user,
    )


@athlete_router.get(
    "/{athlete_id}/public",
    response_model=AthleteTournaments,
    name="Returns athlete by ID for public",
)
async def get_public(
    athlete_id: UUID4,
    year: int | None = Query(
        default=None,
        description="Year of the tournament",
    ),
    db: Session = Depends(),
):
    """
    Returns Athlete by ID
    """
    athlete_db: Athlete = crud.athlete.get(db=db, id=athlete_id)
    athlete = TA_ATHLETE_TOURNAMENTS.validate_python(athlete_db)
    tournaments = crud.athlete.get_tournaments(db=db, athlete_id=athlete_id, year=year)

    for tournament in tournaments:
        tournament_schema = TA_TOURNAMENT.validate_python(tournament)
        tournament_schema.competition_name = tournament.competition.name
        athlete_place = get_athlete_place(tournament=tournament, athlete_id=athlete_id)
        if athlete_place == 1:
            athlete.first.append(tournament_schema)
            continue
        if athlete_place == 2:
            athlete.second.append(tournament_schema)
            continue
        if athlete_place == 3:
            athlete.third.append(tournament_schema)
            continue
        athlete.other.append(tournament_schema)

    return athlete


@athlete_router.post("", response_model=AthletePrivate, name="Creates a new Athlete")
async def create(
    data_in: AthleteCompleteCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a new Athlete
    """

    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    is_coach = False
    format = "%d-%m-%Y"
    if get_role(current_user) == "COACH":
        data_in.public_data.notes = ""
        is_coach = True

    error_exists = False
    error_message: Dict[str, str] = {}
    team_db = None

    if data_in.public_data.team_id != "" and data_in.public_data.team_id is not None:
        team_db = crud.team.get(db=db, id=data_in.public_data.team_id)
    else:
        data_in.public_data.team_id = None

    if is_coach:
        if team_db is None:
            raise HTTPException(404, "Team not found.")
        if team_db.coach_id != current_user.id:
            raise HTTPException(401, "Insufficient Permissions")

        if data_in.public_data.weight is None or data_in.public_data.weight <= 0:
            error_message["weight"] = "The athlete must have a valid weight"
            error_exists = True

    if data_in.public_data.belt_id is None and is_coach:
        error_message["belt"] = "The athlete must have a belt"
        error_exists = True
    if data_in.public_data.belt_id is not None:
        belt: Belt = crud.belt.get(db=db, id=data_in.public_data.belt_id)
        if belt is None:
            error_message["belt"] = "The athlete must have a valid belt"
            error_exists = True

    if data_in.public_data.birthday is None and is_coach:
        error_message["birthday"] = "The athlete must have a birthday"
        error_exists = True
    if data_in.public_data.birthday is not None:
        try:
            data_in.public_data.birthday = datetime.datetime.strptime(
                data_in.public_data.birthday, format
            )
        except:
            error_message["birthday"] = "The athlete must have a valid birthday"
            error_exists = True

    if data_in.public_data.name is None or data_in.public_data.name.strip() == "":
        error_message["name"] = "The athlete must have a name"
        error_exists = True

    if data_in.public_data.is_male is None:
        error_message["competition_gender"] = "The athlete must have a gender"
        error_exists = True

    try:
        if (
            data_in.identification.expiration_date != ""
            and data_in.identification.expiration_date is not None
        ):
            data_in.identification.expiration_date = datetime.datetime.strptime(
                data_in.identification.expiration_date, format
            )
        else:
            data_in.identification.expiration_date = None
    except:
        error_message["identification_expiration_date"] = (
            "The athlete's identification document must have a valid expiration date"
        )
        error_exists = True

    try:
        if (
            data_in.identification_responsible.expiration_date != ""
            and data_in.identification_responsible.expiration_date is not None
        ):
            data_in.identification_responsible.expiration_date = (
                datetime.datetime.strptime(
                    data_in.identification_responsible.expiration_date, format
                )
            )
        else:
            data_in.identification_responsible.expiration_date = None
    except:
        error_message["responsible_identification_expiration_date"] = (
            "The responsible's identification document must have a valid expiration date"
        )
        error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    responsible_identification = crud.identification_document.create(
        db=db, obj_in=data_in.identification_responsible
    )
    data_in.responsible.identification_document_id = responsible_identification.id
    responsible = crud.responsible.create(db=db, obj_in=data_in.responsible)

    address = crud.address.create(db=db, obj_in=data_in.address)

    identification = crud.identification_document.create(
        db=db, obj_in=data_in.identification
    )

    data_in.private_data.identification_document_id = identification.id

    private_info = crud.private_info.create(db=db, obj_in=data_in.private_data)

    data_in.public_data.responsible_id = responsible.id
    data_in.public_data.address_id = address.id
    data_in.public_data.private_info_id = private_info.id

    athlete_db = crud.athlete.create(
        db=db, obj_in=data_in.public_data, team_id=data_in.public_data.team_id
    )

    insured_entity_db = crud.insured_entity.create(
        db=db, obj_in=InsuredEntityCreate(athlete_id=athlete_db.id)
    )

    return get_athlete_by_role(
        athlete=crud.athlete.update(
            db=db,
            db_obj=athlete_db,
            obj_in=AthleteUpdate(insured_entity_id=str(insured_entity_db.id)),
        ),
        current_user=current_user,
    )


@athlete_router.put("/{athlete_id}", name="Updates an Athlete")
async def update(
    athlete_id,
    athlete_in: AthleteUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates an Athlete
    """
    athlete_db = crud.athlete.get(db=db, id=athlete_id)
    team_db = None
    try:
        team_db = crud.team.get(db=db, id=athlete_db.team_id)
    except HTTPException as e:
        if e.status_code != 404:
            raise e

    await can_edit_athlete(athlete=athlete_db, team=team_db, current_user=current_user)

    if get_role(current_user) == "COACH":
        athlete_in.notes = athlete_db.notes
        athlete_in.team_id = athlete_db.team_id

    error_exists = False
    error_message: Dict[str, str] = {}

    if athlete_in.belt_id == "":
        athlete_in.belt_id = None

    if athlete_in.belt_id is not None:
        belt: Belt = crud.belt.get(db=db, id=athlete_in.belt_id)
        if belt is None:
            error_message["belt"] = "The athlete must have a valid belt"
            error_exists = True

    if athlete_in.birthday == "":
        athlete_in.birthday = None

    if athlete_in.birthday is not None:
        format = "%d-%m-%Y"
        birthday = ""
        try:
            birthday = datetime.datetime.strptime(athlete_in.birthday, format)
        except:
            error_message["birthday"] = "The athlete must have a valid birthday"
            error_exists = True

        athlete_in.birthday = birthday

    if athlete_in.team_id == "":
        athlete_in.team_id = None

    if athlete_in.team_id is not None and str(athlete_in.team_id) != str(
        athlete_db.team_id
    ):
        team_in = crud.team.get(db=db, id=athlete_in.team_id)
        if team_in is None:
            error_message["team"] = "The team doesn't exist"
            error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    crud.athlete.update(db=db, obj_in=athlete_in, db_obj=athlete_db)

    return


@athlete_router.put(
    "/{athlete_id}/profile-picture",
    response_model=AthleteAdmin | AthletePrivate,
    name="Updates profile picture of athlete",
    dependencies=[
        Depends(
            FileUploadValidator(max_size_mb=MAX_IMAGE_SIZE, allowed_types=IMAGES_TYPES)
        )
    ],
)
async def upload_profile_picture(
    athlete_id: str,
    file: Annotated[UploadFile, Body(..., description="Profile picture")],
    background_tasks: BackgroundTasks,
    aux: str | None = Form(default=None),
    file_storage_service: FileStorageService = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Uploads profile picture
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    athlete_db: Athlete = crud.athlete.get(db=db, id=athlete_id)
    if athlete_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # Check permissions for coach user
    if get_role(current_user) == "COACH" and (
        athlete_db.team_id is None or athlete_db.team.coach_id != current_user.id
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    file_name = file_storage_service.get_file_name(
        directory=FileStorageDirectories.PROFILE_PICTURES,
        obj_id=athlete_db.id,  # type: ignore
        file=file,
    )
    if athlete_db.profile_picture_url is not None:
        background_tasks.add_task(
            file_storage_service.delete, athlete_db.profile_picture_url  # type: ignore
        )
    background_tasks.add_task(file_storage_service.upload, file_name, file)

    return get_athlete_by_role(
        athlete=crud.athlete.update(
            db=db,
            db_obj=athlete_db,
            obj_in=AthleteUpdate(profile_picture_url=file_name),
        ),
        current_user=current_user,
    )


@athlete_router.put(
    "/remove-from-team/{athlete_id}/{team_id}",
    response_model=Union[Athlete, None],
    name="Removes an Athlete from the team",
)
async def remove_from_team(
    athlete_id,
    team_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    athlete_db = crud.athlete.get(db=db, id=athlete_id)
    if athlete_db is None:
        raise HTTPException(status_code=404, detail="Athlete Not Found")

    team_db = crud.team.get(db=db, id=team_id)
    if team_db is None:
        raise HTTPException(status_code=404, detail="Team Not Found")

    if (
        current_user.user_role.role.name == "COACH"
        and team_db.coach_id != current_user.id
    ):
        raise HTTPException(401, "Insufficient Permissions")

    return crud.athlete.update(
        db=db, obj_in=AthleteUpdate(team_id=None), db_obj=athlete_db
    )


@athlete_router.patch("/{athlete_id}/notes", name="Updates an Athlete's Notes")
async def update_notes(
    athlete_id,
    athlete_in: AthleteAdminUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates an Athlete's Notes
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    athlete_db = crud.athlete.get(db=db, id=athlete_id)

    if athlete_db is None:
        raise HTTPException(404, "Athlete Not Found")

    crud.athlete.update_notes(db=db, db_obj=athlete_db, notes=athlete_in.notes)
    return


def get_athlete_place(tournament, athlete_id) -> int:
    if tournament.first_place_id is not None and [
        atlhete_group
        for atlhete_group in tournament.first_place.athletes_group
        if atlhete_group.athlete_id == athlete_id
    ]:
        return 1
    if tournament.second_place_id is not None and [
        atlhete_group
        for atlhete_group in tournament.second_place.athletes_group
        if atlhete_group.athlete_id == athlete_id
    ]:
        return 2
    if tournament.third_place_id is not None and [
        atlhete_group
        for atlhete_group in tournament.third_place.athletes_group
        if atlhete_group.athlete_id == athlete_id
    ]:
        return 3
    return 4


def get_athlete_by_role(
    athlete, current_user
) -> Athlete | AthletePrivate | AthleteAdmin:
    if current_user is None:
        return TA_ATHLETE.validate_python(athlete)

    role = get_role(current_user)
    if role == "ADMIN":
        return TA_ATHLETE_ADMIN.validate_python(athlete)

    if (
        role == "COACH"
        and athlete.team is not None
        and athlete.team.coach is not None
        and current_user.id == athlete.team.coach.id
    ):
        return TA_ATHLETE_PRIVATE.validate_python(athlete)

    return TA_ATHLETE.validate_python(athlete)


def get_athletes_by_role(
    athletes, current_user
) -> list[Athlete] | list[AthletePrivate] | list[AthleteAdmin]:
    if len(athletes) == 0:
        return []
    if current_user is None:
        return TA_ATHLETE_LIST.validate_python(athletes)

    role = get_role(current_user)
    if role == "ADMIN":
        return TA_ATHLETE_ADMIN_LIST.validate_python(athletes)

    if (
        role == "COACH"
        and athletes[0].team is not None
        and athletes[0].team.coach is not None
        and current_user.id == athletes[0].team.coach.id
    ):
        team_id = athletes[0].team_id
        for atlhete in athletes:
            if team_id != atlhete.team_id:
                return TA_ATHLETE_LIST.validate_python(athletes)
        return TA_ATHLETE_PRIVATE_LIST.validate_python(athletes)

    return TA_ATHLETE_LIST.validate_python(athletes)
