from typing import List, Optional
from fastapi import HTTPException
from pydantic import UUID4
from crud.base import CRUDBase
from models import Team
from schemas import TeamCreate, TeamUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    def get(self, db: Session, id: UUID4 | str) -> Team:
        team_db = None
        if not validate_uuid4(id):
            raise HTTPException(404)
        try:
            team_db = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)
        if team_db is None:
            raise HTTPException(404)
        return team_db

    def get_by_name(self, db: Session, name: str) -> Optional[Team]:
        try:
            return db.query(self.model).filter(self.model.name == name).first()
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def get_by_abbreviation(self, db: Session, abbreviation: str) -> Optional[Team]:
        try:
            return (
                db.query(self.model)
                .filter(self.model.abbreviation == abbreviation)
                .first()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def get_all(self, db: Session) -> list[Team]:
        try:
            return db.query(self.model).all()
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def get_all_by_coach(self, db: Session, coach_id: str) -> List[Team]:
        if not validate_uuid4(coach_id):
            return []
        try:
            return db.query(self.model).filter(self.model.coach_id == coach_id).all()
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def create(self, db: Session, obj_in: TeamCreate) -> Optional[Team]:
        db_obj = Team(
            name=obj_in.name,
            abbreviation=obj_in.abbreviation,
            coach_id=obj_in.coach_id,
            association=obj_in.association,
        )
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_insured_entity(
        self, db: Session, db_obj: Team, insured_entity_id: UUID4
    ) -> Team:
        if not validate_uuid4(insured_entity_id):
            raise HTTPException(404)
        db_obj.insured_entity_id = insured_entity_id
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


team = CRUDTeam(Team)
