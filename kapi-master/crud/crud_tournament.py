from typing import List, Optional
from fastapi import HTTPException
from pydantic import UUID4
from crud.base import CRUDBase
from sqlalchemy import delete
from sqlalchemy.orm import aliased
from models import (
    Tournament,
    Match,
    AthleteCompetition,
    AthleteGroup,
    Athlete,
    Team,
    Competition,
)
from datetime import datetime, timedelta
from schemas import TournamentCreate, TournamentUpdate
from .crud_category import category as crud_category
from core.utils import validate_uuid4
from sqlalchemy import and_, or_, select
from core.utils import commit_to_bd
from sql_app import Session


class CRUDTournament(CRUDBase[Tournament, TournamentCreate, TournamentUpdate]):
    def get(self, db: Session, id: UUID4) -> Tournament:
        obj = None
        if not validate_uuid4(id):
            raise HTTPException(404)
        try:
            obj = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()

        if obj:
            return obj
        raise HTTPException(404)

    def get_paginated(
        self,
        db: Session,
        is_admin: bool,
        competition_id: UUID4 | None,
        category_id: UUID4 | None,
        is_male: bool | None,
        age: int | None,
        area: int | None,
        day: int | None,
        time: str | None,
        athlete: str | None,
        team: str | None,
        team_id: UUID4 | None,
        show_zero: bool,
        limit: int,
        skip: int,
    ) -> tuple[list[Tournament], int]:
        # region initial query
        query = select(Tournament)

        # Show hidden competitions only to admins
        if not is_admin:
            query = query.join(
                Competition, Competition.id == Tournament.competition_id
            ).filter(Competition.show_public == True)

        # region name filters
        search_athlete_name = athlete is not None and athlete.strip() != ""
        search_team_abbr = (
            team is not None and team.strip() != ""
        ) or team_id is not None

        if search_athlete_name or search_team_abbr or not show_zero:
            query = query.join(
                Match, Match.tournament_id == Tournament.id, isouter=True
            )

        # Add Athletes table to query
        if search_athlete_name or search_team_abbr:
            query = (
                query.join(
                    AthleteCompetition,
                    or_(
                        AthleteCompetition.id == Match.athlete_red_id,
                        AthleteCompetition.id == Match.athlete_blue_id,
                    ),
                )
                .join(
                    AthleteGroup,
                    AthleteGroup.athlete_competition_id == AthleteCompetition.id,
                    full=True,
                )
                .join(Athlete, Athlete.id == AthleteGroup.athlete_id)
            )
        # Add teams table to query and search by team abbreviation
        if search_team_abbr:
            query = query.join(Team, Team.id == Athlete.team_id)
            if team is not None and team.strip() != "":
                query = query.filter(Team.abbreviation.ilike(f"%{team.strip()}%"))
            if team_id is not None:
                query = query.filter(Team.id == team_id)
        # Search by athlete name
        if search_athlete_name:
            athlete_name = f"%{athlete.strip().replace(' ', '%')}%"
            query = query.filter(Athlete.name.ilike(athlete_name))

        # endregion

        # region other filters
        if category_id:
            query = query.filter(Tournament.category_id == category_id)

        if not show_zero:
            query = query.filter(Match.tournament_id == Tournament.id)

        if competition_id:
            query = query.filter(Tournament.competition_id == competition_id)

        if is_male is not None:
            query = query.filter(Tournament.is_male == is_male)

        if age:
            query = query.filter(
                and_(Tournament.age_min <= age, Tournament.age_max >= age)
            )
        if area:
            if area == -1:
                query = query.filter(Tournament.area == None)
            else:
                query = query.filter(Tournament.area.like(str(area)))

        if day:
            query = query.filter(Tournament.day == day)

        if time:
            query = query.filter(Tournament.morning == (time == "M"))
        # endregion

        query = query.distinct(Tournament.id)
        # endregion

        # Get count
        count = len(db.scalars(query).all())

        # Set order and pagination
        query = query.subquery()
        tournaments_subquery = aliased(Tournament, query)

        outer_query = select(tournaments_subquery).order_by(
            tournaments_subquery.day.asc(),
            tournaments_subquery.morning.desc(),
            tournaments_subquery.area.asc(),
            tournaments_subquery.order.asc(),
            tournaments_subquery.category_id.asc(),
            tournaments_subquery.is_male.desc(),
            tournaments_subquery.age_min.asc(),
            tournaments_subquery.age_max.asc(),
            tournaments_subquery.weight_min.asc(),
            tournaments_subquery.weight_max.asc(),
            tournaments_subquery.belt_min_id.asc(),
            tournaments_subquery.id.asc(),
        )
        if limit != -1:
            outer_query = outer_query.limit(limit=limit).offset(offset=skip)

        return (db.scalars(outer_query).all(), count)

    def get_by_category(
        self, db: Session, competition_id: UUID4, category_id: str
    ) -> List[Tournament]:
        if not validate_uuid4(competition_id):
            return []
        if not validate_uuid4(category_id):
            return []
        try:
            return (
                db.query(self.model)
                .filter(
                    and_(
                        self.model.competition_id == competition_id,
                        self.model.category_id == category_id,
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()

    def get_by_area_day(
        self, db: Session, competition_id: UUID4, area: int, day: int, morning: bool
    ) -> List[Tournament]:
        if not validate_uuid4(competition_id):
            return []
        try:
            return (
                db.query(self.model)
                .filter(
                    self.model.competition_id == competition_id,
                    self.model.area == area,
                    self.model.day == day,
                    self.model.morning == morning,
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    def get_defaults_of_category(
        self, db: Session, category_id: str
    ) -> List[Tournament]:
        if not validate_uuid4(category_id):
            return []
        try:
            return (
                db.query(Tournament).filter(Tournament.category_id == category_id).all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def get_podiums(self, db: Session, competition_id: str) -> List[Tournament]:
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        try:
            return (
                db.query(Tournament)
                .filter(
                    Tournament.competition_id == competition_id,
                    Tournament.first_place_id != None,
                    Tournament.printed == False,
                    Tournament.updated_at + timedelta(minutes=5) < datetime.today(),
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    def get_podium(self, db: Session, tournament_id: str) -> List[Tournament]:
        if not validate_uuid4(tournament_id):
            raise HTTPException(404)
        try:
            return db.query(Tournament).filter(Tournament.id == tournament_id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    # def get_can_signup(self, db: Session, competition_id: UUID4, athlete_obj: UUID4):
    #     if not validate_uuid4(competition_id):
    #         raise HTTPException(400)
    #     if athlete_obj is None:
    #         raise HTTPException(400)
    #     if not validate_uuid4(athlete_obj.id):
    #         raise HTTPException(400)
    #
    #     sql_string = db.query(Tournament).filter(
    #         Tournament.competition_id == competition_id,
    #         or_(and_(Tournament.age_max == None, Tournament.age_min == None), and_(Tournament.age_max == None, Tournament.age_min <= athelte_age))
    #     )

    def add_podium(
        self,
        db: Session,
        db_obj: Tournament,
        first: UUID4,
        second: UUID4,
        third: UUID4,
        podium_notes: str,
    ):
        if first is not None and not validate_uuid4(first):
            raise HTTPException(422)
        if second is not None and not validate_uuid4(second):
            raise HTTPException(422)
        if third is not None and not validate_uuid4(third):
            raise HTTPException(422)
        db_obj.first_place_id = first
        db_obj.second_place_id = second
        db_obj.third_place_id = third
        db_obj.printed = False
        if podium_notes is not None:
            if db_obj.podium_notes is None:
                db_obj.podium_notes = f"AREA: {podium_notes}"
            else:
                db_obj.podium_notes += f"\nAREA: {podium_notes}"

        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def create(self, db: Session, obj_in: TournamentCreate) -> Tournament:
        db_obj = Tournament(
            age_min=obj_in.age_min,
            age_max=obj_in.age_max,
            weight_min=obj_in.weight_min,
            weight_max=obj_in.weight_max,
            belt_min_id=obj_in.belt_min_id,
            belt_max_id=obj_in.belt_max_id,
            is_male=obj_in.is_male,
            competition_id=obj_in.competition_id,
            category_id=obj_in.category_id,
        )
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def create_multi(
        self, db: Session, obj_in: TournamentCreate, competition_id, category_id
    ) -> Optional[Tournament]:
        if competition_id is not None and not validate_uuid4(competition_id):
            return []
        if category_id is not None and not validate_uuid4(category_id):
            return []
        db_obj = Tournament(
            age_min=obj_in.age_min,
            age_max=obj_in.age_max,
            weight_min=obj_in.weight_min,
            weight_max=obj_in.weight_max,
            belt_min_id=obj_in.belt_min_id,
            belt_max_id=obj_in.belt_max_id,
            is_male=obj_in.is_male,
            competition_id=competition_id,
            category_id=category_id,
            price=obj_in.price,
        )
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def create_multiple(
        self, db: Session, obj_in: List[TournamentCreate], competition_id: UUID4
    ):
        db.bulk_insert_mappings(
            Tournament,
            [
                dict(
                    age_min=obj.age_min,
                    age_max=obj.age_max,
                    weight_min=obj.weight_min,
                    weight_max=obj.weight_max,
                    belt_min_id=obj_in.belt_min_id,
                    belt_max_id=obj_in.belt_max_id,
                    is_male=obj.is_male,
                    area=obj.area,
                    competition_id=competition_id,
                    category_id=crud_category.get_by_name(name=obj.category).id,
                    price=obj.price,
                )
                for obj in obj_in
            ],
        )

        commit_to_bd(session_db=db)

    def update_printed(
        self, db: Session, db_obj: Tournament, podium_notes: Optional[str] = None
    ):
        db_obj.printed = True
        if podium_notes is not None:
            if db_obj.podium_notes is None:
                db_obj.podium_notes = f"PODIUM: {podium_notes}"
            else:
                db_obj.podium_notes += f"\nPODIUM: {podium_notes}"
        db.add(db_obj)

        commit_to_bd(session_db=db)

    def delete_category(self, db: Session, competition_id: str, category_id: str):
        if competition_id is not None and not validate_uuid4(competition_id):
            return []
        if category_id is not None and not validate_uuid4(category_id):
            return []
        delete_query = delete(Tournament).where(
            Tournament.category_id == category_id,
            Tournament.competition_id == competition_id,
        )
        try:
            db.execute(delete_query)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="Error deleting object")


def get_search_string(
    db: Session,
    competition_id: UUID4,
    is_male: Optional[bool] = None,
    category: Optional[str] = None,
    age: Optional[int] = None,
    area: Optional[int] = None,
    day: Optional[int] = None,
    time: Optional[str] = None,
    athlete: Optional[str] = None,
    team: Optional[str] = None,
    show_zero: bool = False,
):
    sql_string = db.query(Tournament)

    if (athlete is not None and athlete.strip() != "") or (
        team is not None and team.strip() != ""
    ):
        sql_string = (
            sql_string.join(Match, Match.tournament_id == Tournament.id, isouter=True)
            .join(
                AthleteCompetition,
                or_(
                    AthleteCompetition.id == Match.athlete_red_id,
                    AthleteCompetition.id == Match.athlete_blue_id,
                ),
            )
            .join(
                AthleteGroup,
                AthleteGroup.athlete_competition_id == AthleteCompetition.id,
                full=True,
            )
            .join(Athlete, Athlete.id == AthleteGroup.athlete_id)
        )
        if team is not None and team.strip() != "":
            team_name = "%" + team.strip() + "%"
            sql_string = sql_string.join(Team, Team.id == Athlete.team_id).filter(
                Team.abbreviation.like(team_name)
            )
        if athlete is not None and athlete.strip() != "":
            athlete_arr = athlete.split(" ")
            athlete_name = "%"
            for name in athlete_arr:
                athlete_name += f"{name}%"
            sql_string = sql_string.filter(Athlete.name.ilike(athlete_name))
    elif not show_zero:
        sql_string = sql_string.join(
            Match, Match.tournament_id == Tournament.id, isouter=True
        )
    if not show_zero:
        sql_string = sql_string.filter(Match.tournament_id == Tournament.id)
    sql_string = sql_string.filter(Tournament.competition_id == competition_id)
    if is_male is not None:
        sql_string = sql_string.filter(Tournament.is_male == is_male)
    if category != "null":
        sql_string = sql_string.filter(Tournament.category_id == category)
    if age is not None:
        sql_string = sql_string.filter(
            and_(Tournament.age_min <= age, Tournament.age_max >= age)
        )
    if area is not None:
        if area == -2:
            sql_string = sql_string.filter(Tournament.area == None)
        else:
            sql_string = sql_string.filter(Tournament.area.like(str(area)))
    if day is not None:
        sql_string = sql_string.filter(Tournament.day == day)
    if time is not None:
        is_morning = time == "M"
        sql_string = sql_string.filter(Tournament.morning == is_morning)
    sql_string = sql_string.distinct(Tournament.id)
    return sql_string


tournament = CRUDTournament(Tournament)
