from typing import List, Optional
from core.utils import commit_to_bd, validate_uuid4
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from models import (
    Athlete,
    AthleteCompetition,
    AthleteGroup,
    PrivateInfo,
    Team,
    Tournament,
    InsuranceStatusEnum,
    Insurance,
    Match,
    Competition,
)
from pydantic import UUID4
from schemas import AthleteCreate, AthleteUpdate
from sql_app import Session
from sqlalchemy import and_, or_, select, func
import datetime

from crud.base import CRUDBase


class CRUDAthlete(CRUDBase[Athlete, AthleteCreate, AthleteUpdate]):
    def get_query_new(
        self,
        db: Session,
        limit: int,
        skip: int,
        teams: list[str] = [],
        name: str | None = None,
        age: int | None = None,
        age_min: int | None = None,
        age_max: int | None = None,
        on_team: bool | None = None,
        is_male: bool | None = None,
        regions: list[str] = [],
        districts: list[str] = [],
        belts: list[str] = [],
        adapted: bool | None = None,
        federated: bool | None = None,
        federation_number: int | None = None,
        soft_deleted: bool | None = None,
        team_abbreviation: str | None = None,
        order_by: str = "name",
        only_coaches: bool = False,
    ) -> tuple[list[Athlete], int]:
        sql_string = select(Athlete)
        if team_abbreviation or regions or districts:
            sql_string = sql_string.join(Team)
        if federation_number or order_by == "federation_number":
            sql_string = sql_string.join(PrivateInfo)

        if team_abbreviation:
            sql_string = sql_string.filter(
                Team.abbreviation == team_abbreviation.upper()
            )
        if teams:
            sql_string = sql_string.filter(
                or_(
                    *[
                        (
                            Athlete.team_id == None
                            if team == "noteam"
                            else Athlete.team_id == team
                        )
                        for team in teams
                    ]
                )
            )
        if name and name.strip():
            name_arr = name.strip().split(" ")
            final_name = "%"
            for n in name_arr:
                final_name = f"{final_name}{n}%"
            if final_name == "%":
                raise HTTPException(422, "Name can't be null or empty string")
            sql_string = sql_string.filter(Athlete.name.ilike(final_name))
        if age:
            sql_string = sql_string.filter(
                func.extract("year", func.age(Athlete.birthday)) == age
            )
        if age_min:
            sql_string = sql_string.filter(
                func.extract("year", func.age(Athlete.birthday)) >= age
            )
        if age_max:
            sql_string = sql_string.filter(
                func.extract("year", func.age(Athlete.birthday)) <= age
            )
        if on_team is not None:
            sql_string = sql_string.filter(
                Athlete.team_id != None if on_team else Athlete.team_id == None
            )
        if regions:
            sql_string = sql_string.filter(
                or_(*[(Team.region == region) for region in regions])
            )
        if districts:
            sql_string = sql_string.filter(
                or_(*[(Team.district == district) for district in districts])
            )
        if is_male is not None:
            sql_string = sql_string.filter(Athlete.is_male == is_male)
        if adapted is not None:
            sql_string = sql_string.filter(Athlete.is_adapted == adapted)
        if federated is not None:
            current_year = datetime.datetime.now().year
            sub_query = (
                select(
                    func.count(Insurance.id.distinct()) != 0
                    if federated
                    else func.count(Insurance.id.distinct()) == 0
                )
                .filter(
                    or_(
                        func.extract("year", Insurance.start_date) == current_year,
                        func.extract("year", Insurance.end_date) == current_year,
                    ),
                    Insurance.insured_entity_id == Athlete.insured_entity_id,
                    Insurance.status == InsuranceStatusEnum.accepted.value,
                )
                .subquery()
            )
            sql_string = sql_string.filter(sub_query)
        if federation_number:
            sql_string = sql_string.filter(
                PrivateInfo.federation_number == federation_number
            )
        if belts:
            sql_string = sql_string.filter(
                or_(
                    *[
                        (
                            Athlete.belt_id == None
                            if belt == "nobelt"
                            else Athlete.belt_id == belt
                        )
                        for belt in belts
                    ]
                )
            )
        if soft_deleted is not None:
            if soft_deleted:
                sql_string = sql_string.filter(Athlete.deleted_at != None)
            else:
                sql_string = sql_string.filter(Athlete.deleted_at == None)
        if only_coaches:
            sql_string = sql_string.filter(Athlete.user_id != None)

        try:
            n_results = len(db.scalars(sql_string).all())
            if order_by == "federation_number":
                sql_string = sql_string.order_by(PrivateInfo.federation_number.asc())
            else:
                sql_string = sql_string.order_by(Athlete.name.asc())

            if limit != -1:
                sql_string = sql_string.limit(limit).offset(skip)

            return db.scalars(sql_string).all(), n_results

        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    def get_all(self, db: Session, soft_deleted: bool) -> List[Athlete]:
        try:
            sql_string = db.query(self.model)
            if not soft_deleted:
                sql_string = sql_string.filter(self.model.deleted_at is None)
            return sql_string.all()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    def get(self, db: Session, id: str | UUID4) -> Athlete:
        if not validate_uuid4(id):
            raise HTTPException(404, "Not Found")
        try:
            query = select(Athlete).filter(Athlete.id == id)
            return db.scalars(query).one()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    def get_by_team(self, db: Session, team_id: str) -> List[Athlete]:
        if not validate_uuid4(team_id) and team_id is not None:
            raise HTTPException(404, "ID Not Found")
        try:
            return db.query(self.model).filter(self.model.team_id == team_id).all()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    def get_by_team_federated(
        self, db: Session, team_id: str, federated: bool
    ) -> List[Athlete]:
        if not validate_uuid4(team_id) and team_id is not None:
            raise HTTPException(404, "ID Not Found")
        try:
            return (
                db.query(self.model)
                .join(PrivateInfo)
                .filter(
                    and_(
                        self.model.team_id == team_id,
                        PrivateInfo.federation_active == federated,
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    def get_by_abbreviation(
        self,
        db: Session,
        abbreviation: str,
        federation_requests_year: int | None = None,
    ) -> List[Athlete]:
        try:
            sql_string = db.query(Athlete)
            if federation_requests_year:
                sql_string = sql_string.join(FederationRequest).filter(
                    FederationRequest.year == federation_requests_year,
                )
            return sql_string.join(Team).filter(Team.abbreviation == abbreviation).all()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    def get_by_number(self, db: Session, number: int) -> Athlete:
        try:
            return (
                db.query(self.model)
                .join(PrivateInfo)
                .filter(PrivateInfo.federation_number == number)
                .first()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)

    def get_by_name(
        self,
        db: Session,
        name: str,
        soft_deleted: bool,
        federation_requests_year: int | None = None,
    ) -> List[Athlete]:
        sql_string = db.query(Athlete)
        if federation_requests_year:
            sql_string = sql_string.join(FederationRequest).filter(
                FederationRequest.year == federation_requests_year,
            )
        if not soft_deleted:
            sql_string = sql_string.filter(self.model.deleted_at is None)
        name_arr = name.strip().split(" ")
        final_name = "%"
        for n in name_arr:
            final_name = f"{final_name}{n}%"
        if final_name == "" or final_name == "%%":
            raise HTTPException(422, "Name can't be null or empty string")
        try:
            sql_string = sql_string.filter(self.model.name.ilike(final_name)).order_by(
                self.model.name.asc()
            )
            return sql_string.all()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)

    def get_by_name_and_team(self, db: Session, name: str, team_id: UUID4) -> Athlete:
        if not validate_uuid4(team_id):
            raise HTTPException(404, "ID Not Found")
        try:
            return (
                db.query(Athlete)
                .join(Team)
                .filter(and_(Athlete.name == name, Team.id == team_id))
                .first()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)

    def get_by_name_and_team_query(
        self,
        db: Session,
        name: str,
        team_id: UUID4,
        federated: bool,
        page: int,
        limit: int,
    ) -> List[Athlete]:
        if team_id is not None and not validate_uuid4(team_id):
            raise HTTPException(404, "ID Not Found")
        try:
            sql_string = get_query_sql_string(
                db=db, name=name, team_id=team_id, federated=federated
            )
            return (
                sql_string.order_by(Athlete.name.asc(), Athlete.id.asc())
                .offset(page * limit)
                .limit(limit)
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)

    def get_by_name_and_team_query_count(
        self, db: Session, name: str, team_id: UUID4, federated: bool
    ) -> List[Athlete]:
        if team_id is not None and not validate_uuid4(team_id):
            raise HTTPException(404, "ID Not Found")
        try:
            sql_string = get_query_sql_string(
                db=db, name=name, team_id=team_id, federated=federated
            )
            return sql_string.count()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)

    def get_pending(self, db: Session, year: int):
        try:
            return (
                db.query(Athlete)
                .join(FederationRequest)
                .filter(
                    and_(
                        FederationRequest.year == year,
                        or_(
                            FederationRequest.status == "pending",
                            FederationRequest.status == "requested",
                        ),
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503)

    def get_tournaments(self, db: Session, athlete_id: UUID4, year: int | None):
        try:
            query = (
                select(Tournament)
                .distinct(Tournament.id)
                .join(Match, Match.tournament_id == Tournament.id)
                .join(
                    AthleteCompetition,
                    or_(
                        Match.athlete_red_id == AthleteCompetition.id,
                        Match.athlete_blue_id == AthleteCompetition.id,
                    ),
                )
                .join(
                    AthleteGroup,
                    AthleteGroup.athlete_competition_id == AthleteCompetition.id,
                )
                .join(Athlete, Athlete.id == AthleteGroup.athlete_id)
            )
            if year:
                query = query.join(
                    Competition, Competition.id == Tournament.competition_id
                ).filter(
                    or_(
                        func.extract("year", Competition.competition_start) == year,
                        func.extract("year", Competition.competition_end) == year,
                    )
                )
            query = query.filter(Athlete.id == athlete_id).order_by(Tournament.id)
            return db.scalars(query).all()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503)

    def create(
        self, db: Session, obj_in: AthleteCreate, team_id: UUID4
    ) -> Optional[Athlete]:
        if team_id is not None and not validate_uuid4(team_id):
            raise HTTPException(400, "Invalid Team ID")
        if obj_in.belt_id is not None and not validate_uuid4(obj_in.belt_id):
            raise HTTPException(400, "Invalid Belt ID")
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Athlete(**obj_in_data)
        db_obj.team_id = team_id
        db.add(db_obj)
        return commit_to_bd(session_db=db, db_obj=db_obj)

    def create_multiple(self, db: Session, obj_in: List[AthleteCreate]):
        db.bulk_insert_mappings(
            Athlete,
            [
                dict(
                    name=obj.name,
                    age=obj.age,
                    belt=obj.belt,
                    weight=obj.weight,
                    is_male=obj.is_male,
                    team_id=obj.team_id,
                )
                for obj in obj_in
            ],
        )
        commit_to_bd(session_db=db)

    def update_insured_entity(
        self, db: Session, db_obj: Athlete, insured_entity_id: UUID4
    ) -> Athlete:
        if not validate_uuid4(insured_entity_id):
            raise HTTPException(404)
        db_obj.insured_entity_id = insured_entity_id
        db.add(db_obj)
        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_notes(self, db: Session, db_obj: Athlete, notes: str) -> Athlete:
        db_obj.notes = notes
        db.add(db_obj)
        return commit_to_bd(session_db=db, db_obj=db_obj)

    def associate_user(self, db: Session, db_obj: Athlete, user_id: UUID4) -> Athlete:
        db_obj.user_id = user_id
        db.add(db_obj)
        return commit_to_bd(session_db=db, db_obj=db_obj)


def get_query_sql_string(db: Session, name: str, team_id: UUID4, federated: bool):
    final_name = "%"
    if name is not None:
        name_arr = name.strip().split(" ")
        for n in name_arr:
            final_name = f"{final_name}{n}%"
        if final_name == "":
            raise HTTPException(422, "Name can't be null or empty string")
    sql_string = ""
    if federated is False:
        sql_string = db.query(Athlete).filter(
            and_(Athlete.name.ilike(final_name), Athlete.team_id == team_id)
        )
    else:
        sql_string = (
            db.query(Athlete)
            .join(PrivateInfo)
            .filter(
                and_(
                    and_(Athlete.name.ilike(final_name), Athlete.team_id == team_id),
                    PrivateInfo.federation_active is True,
                )
            )
        )
    return sql_string


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


athlete = CRUDAthlete(Athlete)
