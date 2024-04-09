from typing import Optional, List
from sqlalchemy import and_
from pydantic import UUID4
from crud.base import CRUDBase
from models import AthleteCompetition, Athlete, AthleteGroup
from schemas import AthleteCompetitionCreate, AthleteCompetitionUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDAthleteCompetition(
    CRUDBase[AthleteCompetition, AthleteCompetitionCreate, AthleteCompetitionUpdate]
):
    def get_bye(
        self, db: Session, competition_id: UUID4
    ) -> Optional[AthleteCompetition]:
        if not validate_uuid4(competition_id):
            return None
        try:
            return (
                db.query(AthleteCompetition)
                .join(AthleteGroup)
                .join(Athlete)
                .filter(
                    and_(
                        Athlete.name == "BYE",
                        AthleteCompetition.competition_id == competition_id,
                    )
                )
                .first()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def get_all(self, db: Session, competition_id: UUID4) -> List[AthleteCompetition]:
        try:
            return (
                db.query(self.model)
                .filter(self.model.competition_id == competition_id)
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def create(self, db: Session, competition_id: UUID4) -> AthleteCompetition:
        db_obj = AthleteCompetition(competition_id=competition_id)
        db.add(db_obj)
        return commit_to_bd(session_db=db, db_obj=db_obj)


athlete_competition = CRUDAthleteCompetition(AthleteCompetition)
