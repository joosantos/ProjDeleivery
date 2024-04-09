from fastapi import BackgroundTasks, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4
from sqlalchemy import func, or_, and_, extract, select, case, literal_column, Text

from crud.base import CRUDBase
from models import (
    Insurance,
    InsuranceType,
    InsuredEntity,
    InsuranceGroup,
    Athlete,
    Team,
    User,
    PrivateInfo,
    InsuranceStatusEnum,
)
from schemas import InsuranceCreate, InsuranceUpdateDatetime, InsuranceCreateDatetime
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session
from core.mail import send_new_payment_comprovative


class CRUDInsurance(CRUDBase[Insurance, InsuranceCreate, InsuranceUpdateDatetime]):
    def get(self, db: Session, id: UUID4) -> Insurance:
        if not validate_uuid4(id):
            raise HTTPException(status_code=422, detail="Invalid ID")
        obj = None
        try:
            obj = db.query(Insurance).filter(Insurance.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"insurance": "Insurnace not found"},
            )
        return obj

    def get_all(
        self,
        db: Session,
        is_federated: bool | None = None,
        insurance_type: list[str] | None = None,
        year: int | None = None,
        name: str | None = None,
        athlete_name: str | None = None,
        team_abbreviation: str | None = None,
        team_id: str | None = None,
        insurance_group_id: str | None = None,
        status: list[InsuranceStatusEnum] | None = None,
        sub_team_group: str | None = None,
        sub_team_groups: list[str] | None = None,
        payment_comprovative_url: str | None = None,
        ids: list[UUID4] | None = None,
        insurance_id: str | None = None,
        only_athletes: bool = False,
        order_by_name: bool = False,
        limit: int = 20,
        page: int = 0,
    ) -> tuple[list[Insurance], int]:
        sql_string = select(Insurance)
        if insurance_type is not None:
            sql_string = sql_string.join(
                InsuranceType, InsuranceType.id == Insurance.insurance_type_id
            )
        if insurance_group_id is not None:
            sql_string = sql_string.join(
                InsuranceGroup,
                InsuranceGroup.id == Insurance.insurance_group_id,
                isouter=True,
            )
        if (
            is_federated
            or name is not None
            or team_abbreviation is not None
            or team_id is not None
            or athlete_name is not None
            or only_athletes
            or order_by_name
        ):
            sql_string = sql_string.join(
                InsuredEntity, InsuredEntity.id == Insurance.insured_entity_id
            )
            if (
                name is not None
                or team_abbreviation is not None
                or athlete_name is not None
                or team_id is not None
                or order_by_name
            ):
                sql_string = sql_string.join(
                    Athlete, InsuredEntity.athlete_id == Athlete.id, isouter=True
                ).join(User, InsuredEntity.user_id == User.id, isouter=True)
                if team_abbreviation is not None or team_id is not None:
                    sql_string = sql_string.join(
                        Team,
                        or_(
                            InsuredEntity.team_id == Team.id, Team.id == Athlete.team_id
                        ),
                        isouter=True,
                    )
                else:
                    sql_string = sql_string.join(
                        Team, InsuredEntity.team_id == Team.id, isouter=True
                    )
                if is_federated is not None and is_federated:
                    sql_string = sql_string.join(
                        PrivateInfo,
                        Athlete.private_info_id == PrivateInfo.id,
                        isouter=True,
                    )
            elif is_federated is not None and is_federated:
                sql_string = sql_string.join(
                    Athlete, InsuredEntity.athlete_id == Athlete.id, isouter=True
                ).join(PrivateInfo, isouter=True)
        if year is not None:
            sql_string = sql_string.filter(
                or_(
                    func.extract("year", Insurance.start_date) == year,
                    func.extract("year", Insurance.end_date) == year,
                )
            )
        if insurance_type is not None:
            sql_string = sql_string.filter(
                or_(*[InsuranceType.id == i for i in insurance_type])
            )
        if insurance_group_id is not None:
            if insurance_group_id == "without":
                sql_string = sql_string.filter(InsuranceGroup.id == None)
            else:
                sql_string = sql_string.filter(InsuranceGroup.id == insurance_group_id)
        if status is not None:
            sql_string = sql_string.filter(
                or_(
                    *[
                        (
                            Insurance.status == s.value
                            if s.value != "other"
                            else and_(
                                Insurance.status != InsuranceStatusEnum.pending.value,
                                Insurance.status != InsuranceStatusEnum.denied.value,
                                Insurance.status != InsuranceStatusEnum.accepted.value,
                            )
                        )
                        for s in status
                    ]
                )
            )
        if name is not None:
            name_arr = name.strip().split(" ")
            final_name = "%"
            for n in name_arr:
                final_name = f"{final_name}{n}%"
            if final_name == "" or final_name == "%%":
                raise HTTPException(422, "Name can't be null or empty string")

            sql_string = sql_string.filter(
                or_(
                    or_(Athlete.name.ilike(final_name), Team.name.ilike(final_name)),
                    User.name.ilike(final_name),
                )
            )
        if team_abbreviation is not None:
            sql_string = sql_string.filter(Team.abbreviation == team_abbreviation)
        if team_id is not None:
            sql_string = sql_string.filter(Team.id == team_id)
        if athlete_name is not None:
            name_arr = athlete_name.strip().split(" ")
            final_name = "%"
            for n in name_arr:
                final_name = f"{final_name}{n}%"
            if final_name == "" or final_name == "%%":
                raise HTTPException(422, "Name can't be null or empty string")
            sql_string = sql_string.filter(Athlete.name.ilike(final_name))
        if is_federated is not None and is_federated:
            sql_string = sql_string.filter(PrivateInfo.federation_active == True)
        if sub_team_group is not None:
            sql_string = sql_string.filter(Insurance.sub_team_group == sub_team_group)
        if sub_team_groups is not None:
            sql_string = sql_string.filter(
                Insurance.sub_team_group.in_(sub_team_groups)
            )
        if payment_comprovative_url is not None:
            if payment_comprovative_url == "none":
                sql_string = sql_string.filter(
                    Insurance.payment_comprovative_url == None
                )
            else:
                sql_string = sql_string.filter(
                    Insurance.payment_comprovative_url == payment_comprovative_url
                )
        if ids is not None:
            sql_string = sql_string.filter(Insurance.id.in_(ids))
        if insurance_id is not None and validate_uuid4(insurance_id):
            sql_string = sql_string.filter(Insurance.id == insurance_id)
        if only_athletes:
            sql_string = sql_string.filter(InsuredEntity.athlete_id != None)
        try:
            n_results = len(db.scalars(sql_string).all())
            if order_by_name:
                sql_string = sql_string.order_by(Athlete.name.asc())
                sql_string = sql_string.order_by(Team.name.asc())
            else:
                sql_string = sql_string.order_by(Insurance.id)
            if limit != -1:
                sql_string = sql_string.offset(page * limit).limit(limit)

            return db.scalars(sql_string).all(), n_results
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Database Error")

    def get_groupped(
        self,
        db: Session,
        insurance_type: list[str] | None = None,
        year: int | None = None,
        name: str | None = None,
        status: list[str] | None = None,
        team_abbreviation: str | None = None,
        group: str | None = None,
        payment_comprovative_url: str | None = None,
        group_by: str = "payment_comprovatives",
        limit: int = 20,
        page: int = 0,
    ):
        sql_string = (
            select(
                func.count(Insurance.id),
                (
                    Insurance.payment_comprovative_url
                    if group_by == "payment_comprovatives"
                    else Insurance.insurance_group_id
                ),
                func.sum(case((Insurance.medical_exam_url != None, 1), else_=0)),
                func.sum(
                    case((Insurance.payment_comprovative_url != None, 1), else_=0)
                ),
                func.sum(
                    case(
                        (Insurance.status == InsuranceStatusEnum.pending.value, 1),
                        else_=0,
                    )
                ),
                func.sum(
                    case(
                        (Insurance.status == InsuranceStatusEnum.accepted.value, 1),
                        else_=0,
                    )
                ),
                func.sum(
                    case(
                        (
                            and_(
                                Insurance.status != InsuranceStatusEnum.accepted.value,
                                Insurance.status != InsuranceStatusEnum.pending.value,
                            ),
                            1,
                        ),
                        else_=0,
                    )
                ),
                func.string_agg(Athlete.profile_picture_url, literal_column("','")),
                func.string_agg(
                    func.cast(Athlete.team_id, Text),
                    literal_column("','"),
                ),
                func.string_agg(
                    func.cast(Team.id, Text),
                    literal_column("','"),
                ),
                func.string_agg(
                    func.cast(InsuranceGroup.name, Text).distinct(),
                    literal_column("','"),
                ),
            )
            .join(InsuredEntity, Insurance.insured_entity_id == InsuredEntity.id)
            .join(
                InsuranceGroup,
                Insurance.insurance_group_id == InsuranceGroup.id,
                isouter=True,
            )
            .join(Athlete, InsuredEntity.athlete_id == Athlete.id, isouter=True)
            .join(
                Team,
                or_(
                    InsuredEntity.team_id == Team.id,
                    Athlete.team_id == Team.id,
                ),
                isouter=True,
            )
        )

        if year is None:
            sql_string = sql_string.having(
                func.sum(
                    case(
                        (
                            or_(
                                func.extract("year", Insurance.start_date) == year,
                                func.extract("year", Insurance.end_date) == year,
                            ),
                            1,
                        ),
                        else_=0,
                    )
                )
                > 0,
            )
        if insurance_type is not None:
            sql_string = sql_string.having(
                func.sum(
                    case(
                        *[
                            (Insurance.insurance_type_id == i, 1)
                            for i in insurance_type
                        ],
                        else_=0,
                    )
                )
                > 0,
            )
        if group is not None:
            if group == "without":
                sql_string = sql_string.having(
                    func.sum(
                        case(
                            (
                                InsuranceGroup.id == None,
                                1,
                            ),
                            else_=0,
                        )
                    )
                    > 0,
                )
            else:
                sql_string = sql_string.having(
                    func.sum(
                        case(
                            (
                                InsuranceGroup.id == group,
                                1,
                            ),
                            else_=0,
                        )
                    )
                    > 0,
                )
        if status is not None:
            sql_string = sql_string.having(
                func.sum(
                    case(
                        *[
                            (
                                (
                                    Insurance.status == s,
                                    1,
                                )
                                if s != "other"
                                else (
                                    and_(
                                        Insurance.status
                                        != InsuranceStatusEnum.pending.value,
                                        Insurance.status
                                        != InsuranceStatusEnum.denied.value,
                                        Insurance.status
                                        != InsuranceStatusEnum.accepted.value,
                                    ),
                                    1,
                                )
                            )
                            for s in status
                        ],
                        else_=0,
                    )
                )
                > 0,
            )
        if name is not None:
            if name is not None:
                name_arr = name.strip().split(" ")
                final_name = "%"
                for n in name_arr:
                    final_name = f"{final_name}{n}%"
                if final_name == "" or final_name == "%%":
                    raise HTTPException(422, "Name can't be null or empty string")

                sql_string = sql_string.having(
                    func.sum(
                        case(
                            (
                                or_(
                                    Athlete.name.ilike(final_name),
                                    Team.name.ilike(final_name),
                                ),
                                1,
                            ),
                            else_=0,
                        )
                    )
                    > 0,
                )
        if team_abbreviation is not None:
            sql_string = sql_string.having(
                func.sum(
                    case(
                        (
                            (Team.abbreviation == team_abbreviation.strip().upper()),
                            1,
                        ),
                        else_=0,
                    )
                )
                > 0,
            )
        if payment_comprovative_url is not None:
            sql_string = sql_string.having(
                func.sum(
                    case(
                        (
                            Insurance.payment_comprovative_url
                            == payment_comprovative_url,
                            1,
                        ),
                        else_=0,
                    )
                )
                > 0,
            )

        sql_string = sql_string.group_by(
            (
                Insurance.payment_comprovative_url
                if group_by == "payment_comprovatives"
                else Insurance.insurance_group_id
            ),
        )
        n_results = len(db.execute(sql_string).all())
        if limit != -1:
            sql_string = sql_string.offset(page * limit).limit(limit)

        return db.execute(sql_string).all(), n_results

    def get_by_team_group(
        self,
        db: Session,
        team_id: UUID4 | None = None,
        year: int | None = None,
        sub_team_group: str | None = None,
        sub_team_groups: list[str] | None = None,
        payment_comprovative_url: str | None = None,
    ):
        sql_string = (
            select(
                func.count(Insurance.id),
                Insurance.sub_team_group,
                Insurance.insurance_type_id,
                func.sum(case((Insurance.medical_exam_url != None, 1)), else_=0),
                func.sum(
                    case((Insurance.payment_comprovative_url != None, 1)), else_=0
                ),
                func.sum(
                    case((Insurance.status == InsuranceStatusEnum.pending.value, 1)),
                    else_=0,
                ),
                func.sum(
                    case((Insurance.status == InsuranceStatusEnum.accepted.value, 1)),
                    else_=0,
                ),
                func.sum(
                    case(
                        (
                            and_(
                                Insurance.status != InsuranceStatusEnum.accepted.value,
                                Insurance.status != InsuranceStatusEnum.pending.value,
                            ),
                            1,
                        )
                    ),
                    else_=0,
                ),
                func.string_agg(Athlete.profile_picture_url, literal_column("','")),
            )
            .join(InsuredEntity, Insurance.insured_entity_id == InsuredEntity.id)
            .join(Athlete, InsuredEntity.athlete_id == Athlete.id, isouter=True)
            .join(Team, InsuredEntity.team_id == Team.id, isouter=True)
        )

        if team_id:
            sql_string = sql_string.filter(
                or_(Athlete.team_id == team_id, Team.id == team_id)
            )
        if year:
            sql_string = sql_string.filter(
                (
                    extract("year", Insurance.end_date)
                    - extract("year", Insurance.start_date)
                )
                >= (year - extract("year", Insurance.start_date)),
                (year - extract("year", Insurance.start_date) >= 0),
            )
        if sub_team_group:
            sql_string = sql_string.filter(Insurance.sub_team_group == sub_team_group)
        if sub_team_groups:
            sql_string = sql_string.filter(
                Insurance.sub_team_group.in_(sub_team_groups)
            )
        if payment_comprovative_url:
            sql_string = sql_string.filter(
                Insurance.payment_comprovative_url == payment_comprovative_url
            )
        sql_string = sql_string.group_by(
            Insurance.sub_team_group,
            Insurance.insurance_type_id,
        )
        return db.execute(sql_string).all()

    def create(self, db: Session, obj_in: InsuranceCreate) -> Insurance:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def multi_create(self, db: Session, objs_in: list[InsuranceCreateDatetime]) -> None:
        dbs_obj = []
        for obj_in in objs_in:
            obj_in_data = jsonable_encoder(obj_in)
            dbs_obj.append(self.model(**obj_in_data))

        db.bulk_save_objects(dbs_obj)
        commit_to_bd(session_db=db)
        return None

    def update_multiple_payment_comprovative_url_by_sub_team(
        self,
        db: Session,
        sub_team_ids: list[UUID4] | list[str],
        file_name: str,
        background_tasks: BackgroundTasks,
        file_storage_service,
    ) -> None:
        for id in sub_team_ids:
            if not validate_uuid4(id):
                raise HTTPException(status_code=422, detail="Invalid ID")

        sql_string = select(Insurance).filter(
            Insurance.sub_team_group.in_(sub_team_ids)
        )
        results: list[Insurance] = db.scalars(sql_string).all()

        for result in results:
            if result.payment_comprovative_url is not None:
                if (
                    self.get_all(
                        db=db,
                        payment_comprovative_url=result.payment_comprovative_url,  # type: ignore
                        limit=-1,
                    )
                    == 1
                ):
                    background_tasks.add_task(
                        file_storage_service.delete, result.payment_comprovative_url
                    )
            result.payment_comprovative_url = file_name  # type: ignore
            db.add(result)
        commit_to_bd(session_db=db)

        team = None
        if results[0].insured_entity.team_id is None:
            team = results[0].insured_entity.athlete.team
        else:
            team = results[0].insured_entity.team

        background_tasks.add_task(
            send_new_payment_comprovative, file_name=file_name, team=team
        )


insurance = CRUDInsurance(Insurance)
