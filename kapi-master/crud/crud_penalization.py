from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from crud.base import CRUDBase
from pydantic import UUID4
from models import Penalization
from schemas import PenalizationCreate, PenalizationUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDPenalization(CRUDBase[Penalization, PenalizationCreate, PenalizationUpdate]):
    def get(self, db: Session, id: UUID4 | str) -> Penalization:
        penalization_db = None
        if not validate_uuid4(id):
            raise HTTPException(404)
        try:
            penalization_db = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)
        if penalization_db is None:
            raise HTTPException(404)
        return penalization_db

    def get_all(
        self, db: Session, limit: int, skip: int, competition_id: UUID4 | None = None
    ) -> tuple[list[Penalization], int]:
        sql_string = select(Penalization)
        if competition_id:
            sql_string = sql_string.filter(
                Penalization.competition_id == competition_id
            )

        try:
            n_results = len(db.scalars(sql_string).all())

            if limit != -1:
                sql_string = sql_string.limit(limit).offset(skip)
            sql_string = sql_string.order_by(Penalization.id)

            return db.scalars(sql_string).all(), n_results
        except Exception as e:
            print(e)
            raise HTTPException(503, "Server error")

    def create(self, db: Session, obj_in: PenalizationCreate) -> Penalization:
        if not validate_uuid4(obj_in.team_id) or not validate_uuid4(
            obj_in.competition_id
        ):
            raise HTTPException(404)
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def delete(self, db: Session, id: UUID4 | str) -> Penalization:
        penalization_db = self.get(db=db, id=id)

        db.delete(penalization_db)

        commit_to_bd(session_db=db)
        return penalization_db


penalization = CRUDPenalization(Penalization)
