from typing import Optional
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4

from crud.base import CRUDBase
from models.insured_entity import InsuredEntity
from schemas.insured_entity import InsuredEntityCreate, InsuredEntityUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDInsuredEntity(
    CRUDBase[InsuredEntity, InsuredEntityCreate, InsuredEntityUpdate]
):
    def get(self, db: Session, id: UUID4) -> Optional[InsuredEntity]:
        if not validate_uuid4(id):
            raise HTTPException(status_code=422, detail="Invalid ID")
        try:
            return db.query(InsuredEntity).filter(InsuredEntity.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def create(self, db: Session, obj_in: InsuredEntityCreate) -> InsuredEntity:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


insured_entity = CRUDInsuredEntity(InsuredEntity)
