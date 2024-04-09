from typing import Optional
from pydantic import UUID4
from sqlalchemy import and_

from crud.base import CRUDBase
from models import AthleteGroup
from schemas import AthleteGroupCreate, AthleteGroupUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDAthleteGroup(CRUDBase[AthleteGroup, AthleteGroupCreate, AthleteGroupUpdate]):
    def get(self, db: Session, id: UUID4) -> Optional[AthleteGroup]:
        if not validate_uuid4(id):
            return None
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def create(self, db: Session, obj_in: AthleteGroupCreate) -> Optional[AthleteGroup]:
        db_obj = AthleteGroup(
            athlete_id=obj_in.athlete_id,
            athlete_competition_id=obj_in.athlete_competition_id,
        )
        db.add(db_obj)
        return commit_to_bd(session_db=db, db_obj=db_obj)

    def delete_group(
        self, db: Session, athlete_competition_id: UUID4, athlete_id: UUID4
    ):
        if not validate_uuid4(athlete_competition_id) or not validate_uuid4(athlete_id):
            return None
        obj = (
            db.query(self.model)
            .filter(
                and_(
                    self.model.athlete_competition_id == athlete_competition_id,
                    self.model.athlete_id == athlete_id,
                )
            )
            .first()
        )
        db.delete(obj)
        commit_to_bd(session_db=db)


athlete_group = CRUDAthleteGroup(AthleteGroup)
