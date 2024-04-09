from typing import Optional, List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4
from sqlalchemy import select

from crud.base import CRUDBase
from models.insurance_group import InsuranceGroup
from schemas.insurance_group import InsuranceGroupCreate, InsuranceGroupUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDInsuranceGroup(
    CRUDBase[InsuranceGroup, InsuranceGroupCreate, InsuranceGroupUpdate]
):
    def get(self, db: Session, id: UUID4) -> Optional[InsuranceGroup]:
        db_obj = None
        if not validate_uuid4(id):
            raise HTTPException(status_code=422, detail="Invalid ID")
        try:
            db_obj = db.query(InsuranceGroup).filter(InsuranceGroup.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")
        if not db_obj:
            raise HTTPException(404)
        return db_obj

    def get_all(self, db: Session, name: str | None = None) -> List[InsuranceGroup]:
        try:
            sql_string = select(InsuranceGroup)
            if name is not None:
                sql_string = sql_string.filter(InsuranceGroup.name == name)
            return db.scalars(sql_string).all()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def create(self, db: Session, obj_in: InsuranceGroupCreate) -> InsuranceGroup:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


insurance_group = CRUDInsuranceGroup(InsuranceGroup)
