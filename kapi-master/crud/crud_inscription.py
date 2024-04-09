from typing import List, Optional
from fastapi import BackgroundTasks, HTTPException, status
from pydantic import UUID4
from sqlalchemy import and_, select

from crud.base import CRUDBase
from models import (
    Inscription,
    Tournament,
    Athlete,
    AthleteGroup,
    AthleteCompetition,
    Team,
    Competition,
)
from schemas import InscriptionCreate, InscriptionUpdate, InscriptionPaymentIn
from core.utils import validate_uuid4, commit_to_bd
from sql_app import Session
from core.mail import send_new_payment_comprovative_for_inscriptions


class CRUDInscription(CRUDBase[Inscription, InscriptionCreate, InscriptionUpdate]):
    def get_new(
        self,
        db: Session,
        limit: int,
        competition_id: UUID4 | None = None,
        team_id: UUID4 | None = None,
        inscription_confirmed: bool | None = None,
        inscription_accepted: bool | None = None,
        skip: int = 0,
        payment_comprovative_url: str | None = None,
    ) -> tuple[list[Inscription], int]:
        sql_string = select(Inscription).distinct()
        if competition_id:
            sql_string = sql_string.join(
                Tournament, Tournament.id == Inscription.tournament_id
            )
        if team_id:
            sql_string = sql_string.join(
                AthleteGroup,
                AthleteGroup.athlete_competition_id
                == Inscription.athlete_competition_id,
            ).join(Athlete, Athlete.id == AthleteGroup.athlete_id)
        if competition_id:
            sql_string = sql_string.filter(Tournament.competition_id == competition_id)
        if team_id:
            sql_string = sql_string.filter(Athlete.team_id == team_id)
        if inscription_confirmed:
            sql_string = sql_string.filter(
                Inscription.confirmed == inscription_confirmed
            )
        if inscription_accepted:
            sql_string = sql_string.filter(Inscription.accepted == inscription_accepted)
        if payment_comprovative_url:
            sql_string = sql_string.filter(
                Inscription.payment_comprovative_url == payment_comprovative_url
            )
        try:
            n_results = len(db.scalars(sql_string).all())

            sql_string = sql_string.order_by(
                Inscription.tournament_id, Inscription.athlete_competition_id
            )
            if limit != -1:
                sql_string = sql_string.offset(skip).limit(limit)

            return db.scalars(sql_string).all(), n_results
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Database Error")

    def get(
        self, db: Session, tournament_id: UUID4, athlete_competition_id: UUID4
    ) -> Optional[Inscription]:
        obj = None
        try:
            obj = (
                db.query(self.model)
                .filter(
                    and_(
                        self.model.tournament_id == tournament_id,
                        self.model.athlete_competition_id == athlete_competition_id,
                    )
                )
                .first()
            )
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

    def get_by_tournament(self, db: Session, tournament_id: UUID4) -> List[Inscription]:
        if not validate_uuid4(tournament_id):
            return []
        try:
            return (
                db.query(self.model)
                .filter(self.model.tournament_id == tournament_id)
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def get_by_tournament_confirmed(
        self, db: Session, tournament_id: UUID4, confirmed: bool
    ) -> List[Inscription]:
        if not validate_uuid4(tournament_id):
            return []
        try:
            return (
                db.query(self.model)
                .join(Tournament)
                .filter(
                    and_(
                        self.model.tournament_id == tournament_id,
                        Inscription.confirmed == confirmed,
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def get_by_competition(
        self, db: Session, competition_id: UUID4
    ) -> List[Inscription]:
        if not validate_uuid4(competition_id):
            return []
        try:
            return (
                db.query(self.model)
                .join(Tournament)
                .filter(Tournament.competition_id == competition_id)
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def get_stats_by_competition(self, db: Session, competition_id: UUID4):
        if not validate_uuid4(competition_id):
            return []
        queryInscription = (
            db.query(self.model)
            .join(Tournament)
            .filter(Tournament.competition_id == competition_id)
        )
        queryAthlete = queryInscription.distinct(Inscription.athlete_competition_id)
        competition = (
            db.query(Competition).filter(Competition.id == competition_id).first()
        )
        if competition is None:
            raise HTTPException(404)
        try:
            return {
                "athletes": {
                    "confirmed": queryAthlete.filter(
                        Inscription.confirmed == True
                    ).count(),
                    "notConfirmed": queryAthlete.filter(
                        Inscription.confirmed == False
                    ).count(),
                    "accepted": queryAthlete.filter(
                        Inscription.accepted == True
                    ).count(),
                },
                "inscriptions": {
                    "confirmed": queryInscription.filter(
                        Inscription.confirmed == True
                    ).count(),
                    "notConfirmed": queryInscription.filter(
                        Inscription.confirmed == False
                    ).count(),
                    "accepted": queryInscription.filter(
                        Inscription.accepted == True
                    ).count(),
                },
                "competition": {"id": competition.id, "name": competition.name},
            }
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503)

    def get_by_competition_confirmed(
        self, db: Session, competition_id: UUID4, confirmed: bool
    ) -> List[Inscription]:
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        try:
            return (
                db.query(self.model)
                .join(Tournament)
                .filter(
                    and_(
                        Tournament.competition_id == competition_id,
                        Inscription.confirmed == confirmed,
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)

    def get_by_competition_confirmed_count(
        self, db: Session, competition_id: UUID4, confirmed: bool
    ) -> int:
        if not validate_uuid4(competition_id):
            return 0
        try:
            return (
                db.query(self.model)
                .join(Tournament)
                .filter(
                    and_(
                        Tournament.competition_id == competition_id,
                        Inscription.confirmed == confirmed,
                    )
                )
                .count()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return 0

    def get_by_competition_by_team_accepted(
        self, db: Session, competition_id: UUID4, team_id: str, accepted: bool
    ) -> List[Inscription]:
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        if not validate_uuid4(team_id):
            raise HTTPException(404)
        try:
            return (
                db.query(Inscription)
                .join(AthleteCompetition)
                .join(AthleteGroup)
                .join(Athlete)
                .join(Team)
                .filter(
                    Tournament.competition_id == competition_id,
                    Team.id == team_id,
                    Inscription.accepted == accepted,
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503)

    def get_by_competition_by_team(
        self,
        db: Session,
        competition_id: UUID4,
        confirmed: bool,
        team_id: Optional[UUID4] = None,
    ) -> List[Inscription]:
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        if team_id is not None and not validate_uuid4(team_id):
            raise HTTPException(404)
        try:
            query = (
                db.query(Inscription)
                .join(Tournament, Tournament.id == Inscription.tournament_id)
                .join(
                    AthleteCompetition,
                    Inscription.athlete_competition_id == AthleteCompetition.id,
                )
                .join(AthleteGroup)
                .join(Athlete)
            )

            query = query.filter(
                Tournament.competition_id == competition_id,
                Athlete.team_id == team_id,
                Inscription.confirmed == confirmed,
            )
            return query.all()

        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)

    def create(self, db: Session, obj_in: InscriptionCreate) -> Optional[Inscription]:
        db_obj = Inscription(
            tournament_id=obj_in.tournament_id,
            athlete_competition_id=obj_in.athlete_competition_id,
        )
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_confirmed(
        self, db: Session, db_obj: Inscription, confirmed: bool
    ) -> Optional[Inscription]:
        db_obj.confirmed = confirmed
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_accepted(
        self, db: Session, db_obj: Inscription, accepted: bool
    ) -> Optional[Inscription]:
        db_obj.accepted = accepted
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_all(
        self, db: Session, db_obj: Inscription, obj_in: InscriptionUpdate
    ) -> Optional[Inscription]:
        if obj_in.tournament_id is not None:
            db_obj.tournament_id = obj_in.tournament_id
        if obj_in.accepted is not None:
            db_obj.accepted = obj_in.accepted
        if obj_in.confirmed is not None:
            db_obj.confirmed = obj_in.confirmed
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def upload_payment_comprovative(
        self,
        db: Session,
        inscriptions: list[InscriptionPaymentIn],
        file_name: str,
        background_tasks: BackgroundTasks,
        file_storage_service,
    ) -> None:
        athlete_ids = []
        tournament_ids = []
        for inscription in inscriptions:
            if not validate_uuid4(
                inscription.athlete_competition_id
            ) or not validate_uuid4(inscription.tournament_id):
                raise HTTPException(status_code=422, detail="Invalid ID")
            athlete_ids.append(inscription.athlete_competition_id)
            tournament_ids.append(inscription.tournament_id)

        sql_string = select(Inscription).filter(
            Inscription.athlete_competition_id.in_(athlete_ids),
            Inscription.tournament_id.in_(tournament_ids),
        )
        results = db.scalars(sql_string).all()

        for result in results:
            if result.payment_comprovative_url is not None:
                list, n_results = self.get_new(
                    db=db,
                    payment_comprovative_url=result.payment_comprovative_url,  # type: ignore
                    limit=-1,
                )

                if n_results == 1:
                    background_tasks.add_task(
                        file_storage_service.delete, result.payment_comprovative_url
                    )
            result.payment_comprovative_url = file_name  # type: ignore
            db.add(result)
        commit_to_bd(session_db=db)

        background_tasks.add_task(
            send_new_payment_comprovative_for_inscriptions,
            file_name=file_name,
            team=results[0].athlete_competition.athletes_group[0].athlete.team,
            competition=results[0].tournament.competition,
        )
        return

    def delete_inscription(
        self, db: Session, tournament_id: UUID4, athlete_competition_id: UUID4
    ):
        if not validate_uuid4(tournament_id) or not validate_uuid4(
            athlete_competition_id
        ):
            return None
        obj = (
            db.query(self.model)
            .filter(
                and_(
                    self.model.tournament_id == tournament_id,
                    self.model.athlete_competition_id == athlete_competition_id,
                )
            )
            .first()
        )
        db.delete(obj)

        commit_to_bd(session_db=db)


inscription = CRUDInscription(Inscription)
