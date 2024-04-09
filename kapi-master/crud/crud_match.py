from typing import List, Optional
from fastapi import HTTPException
from pydantic import UUID4
from crud.base import CRUDBase
from models import Match, Tournament
from schemas import MatchCreate, MatchUpdate, MatchRequestUpdate, MatchRequestSpecial
from sqlalchemy import and_, or_
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDMatch(CRUDBase[Match, MatchCreate, MatchUpdate]):
    def get(self, db: Session, id: UUID4) -> Optional[Match]:
        if not validate_uuid4(id):
            return None
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def getAll(self, db: Session) -> List[Match]:
        try:
            return db.query(self.model).all()
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def get_next(
        self,
        db: Session,
        competition_id: str,
        area: int,
        day: int,
        morning: bool,
        number: int,
    ) -> Tournament:
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        try:
            print(area)
            tournament_db = (
                db.query(Tournament)
                .join(Match)
                .filter(
                    Tournament.area == str(area),
                    Tournament.day == day,
                    Tournament.morning == morning,
                    Match.number_by_area == number,
                    Tournament.competition_id == competition_id,
                )
                .first()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)
        if tournament_db is None:
            raise HTTPException(404)
        return tournament_db

    def get_call(
        self,
        db: Session,
        competition_id: str,
        area: int,
        day: int,
        morning: bool,
        number: int,
    ) -> Match:
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        try:
            match_db = (
                db.query(Match)
                .join(Tournament)
                .filter(
                    and_(
                        and_(
                            and_(Tournament.area == str(area), Tournament.day == day),
                            Tournament.competition_id == competition_id,
                        ),
                        and_(
                            Tournament.morning == morning,
                            Match.number_by_area == number,
                        ),
                    )
                )
                .first()
            )

        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)
        if match_db is None:
            raise HTTPException(404)
        return match_db

    def get_call_requests(self, db: Session, competition_id: UUID4) -> List[Match]:
        if not validate_uuid4(competition_id):
            return None
        try:
            return (
                db.query(Match)
                .join(Tournament)
                .filter(
                    and_(
                        Tournament.competition_id == competition_id,
                        or_(
                            or_(
                                Match.call_request == True,
                                Match.call_request_clean == True,
                            ),
                            Match.call_request_fireman == True,
                        ),
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)

    def create(
        self, db: Session, obj_in: MatchCreate, tournament_id: UUID4
    ) -> Optional[Match]:
        if not validate_uuid4(tournament_id):
            return None
        db_obj = Match(
            athlete_red_id=obj_in.athlete_red_id,
            athlete_blue_id=obj_in.athlete_blue_id,
            tournament_id=tournament_id,
            number=obj_in.number,
        )
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def add_winner(
        self, db: Session, db_obj: Match, winner_id: UUID4
    ) -> Optional[Match]:
        if not validate_uuid4(winner_id):
            return None
        if winner_id != db_obj.athlete_red_id and winner_id != db_obj.athlete_blue_id:
            raise HTTPException(status_code=400, detail="Invalid athlete")
        db_obj.winner_id = winner_id
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def add_athlete(
        self, db: Session, db_obj: Match, athlete_id: UUID4, is_red: bool
    ) -> Optional[Match]:
        if not validate_uuid4(athlete_id):
            return None
        if athlete_id is None:
            raise HTTPException(status_code=400, detail="Invalid athlete")
        if is_red:
            db_obj.athlete_red_id = athlete_id
        else:
            db_obj.athlete_blue_id = athlete_id
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def add_area_number(
        self, db: Session, db_obj: Match, number: int
    ) -> Optional[Match]:
        db_obj.number_by_area = number
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_request(
        self, db: Session, db_obj: Match, obj_in: MatchRequestUpdate
    ) -> Match:
        db_obj.number_call_request += 1
        db_obj.area_to_call = obj_in.area_to_call
        if (
            obj_in.description_to_micro != ""
            and obj_in.description_to_micro is not None
        ):
            if db_obj.description_to_micro is None:
                db_obj.description_to_micro = f"AREA: {obj_in.description_to_micro}"
            else:
                db_obj.description_to_micro += f"\nAREA: {obj_in.description_to_micro}"
        db_obj.call_type = obj_in.call_type
        db_obj.call_request = True

        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def special_request(
        self, db: Session, db_obj: Match, obj_in: MatchRequestSpecial
    ) -> Match:
        db_obj.call_request_fireman = (
            obj_in.call_request_fireman
            if obj_in.call_request_fireman is not None
            else db_obj.call_request_fireman
        )
        db_obj.call_request_clean = (
            obj_in.call_request_clean
            if obj_in.call_request_clean is not None
            else db_obj.call_request_clean
        )
        db_obj.area_to_call = obj_in.area_to_call

        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_call_made(
        self, db: Session, db_obj: Match, obj_in: MatchRequestUpdate
    ) -> Match:
        db_obj.calls_made += 1
        if (
            obj_in.description_to_micro != ""
            and obj_in.description_to_micro is not None
        ):
            if db_obj.description_to_micro is None:
                db_obj.description_to_micro = f"MICRO: {obj_in.description_to_micro}"
            else:
                db_obj.description_to_micro += f"\nMICRO: {obj_in.description_to_micro}"
        db_obj.call_request = False
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_call_made_special(
        self, db: Session, db_obj: Match, obj_in: MatchRequestSpecial
    ) -> Match:
        if obj_in.call_request_fireman is not None:
            db_obj.call_request_fireman = obj_in.call_request_fireman
        elif obj_in.call_request_clean is not None:
            db_obj.call_request_clean = obj_in.call_request_clean
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def create_multiple(
        self,
        db: Session,
        obj_in: List[UUID4],
        tournament_id: UUID4,
        extras: List[str],
        is_tournament: bool = True,
    ):
        number = 1
        if len(obj_in) == 0:
            return
        if is_tournament:
            aux = [
                dict(
                    athlete_red_id=obj_in[i],
                    athlete_blue_id=obj_in[i + 1],
                    tournament_id=tournament_id,
                    number=number + i / 2,
                )
                for i in range(0, len(obj_in), 2)
            ]
            number = len(obj_in) / 2
            for extra in extras:
                number += 1
                aux.append(
                    dict(
                        athlete_red_id=extra,
                        athlete_blue_id=extra,
                        tournament_id=tournament_id,
                        number=number,
                    )
                )
        else:
            aux = [
                dict(
                    athlete_red_id=obj_in[i],
                    athlete_blue_id=None,
                    tournament_id=tournament_id,
                    number=1 + i,
                )
                for i in range(0, len(obj_in))
            ]
        db.bulk_insert_mappings(Match, aux)

        commit_to_bd(session_db=db)


match = CRUDMatch(Match)
