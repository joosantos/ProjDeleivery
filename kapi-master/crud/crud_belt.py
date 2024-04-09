from typing import Optional, List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4

from crud.base import CRUDBase
from models.belt import Belt
from schemas.belt import BeltCreate, BeltUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDBelt(CRUDBase[Belt, BeltCreate, BeltUpdate]):
    def get(self, db: Session, id: UUID4) -> Optional[Belt]:
        if not validate_uuid4(id):
            raise HTTPException(status_code=422, detail="Invalid ID")
        try:
            return db.query(Belt).filter(Belt.id == id).first()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def get_by_name(self, db: Session, name: str) -> Optional[Belt]:
        try:
            return db.query(Belt).filter(Belt.name == name).first()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def get_by_order(self, db: Session, order: int) -> Optional[Belt]:
        try:
            return db.query(Belt).filter(Belt.order == order).first()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def get_all(self, db: Session) -> List[Belt]:
        try:
            return db.query(Belt).all()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def create(self, db: Session, obj_in: BeltCreate) -> Belt:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


belt = CRUDBelt(Belt)
