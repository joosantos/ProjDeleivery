from typing import Optional, List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4

from crud.base import CRUDBase
from models.insurance_type import InsuranceType
from schemas.insurance_type import InsuranceTypeCreate, InsuranceTypeUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDInsuranceType(
    CRUDBase[InsuranceType, InsuranceTypeCreate, InsuranceTypeUpdate]
):
    def get(self, db: Session, id: UUID4) -> Optional[InsuranceType]:
        if not validate_uuid4(id):
            raise HTTPException(status_code=422, detail="Invalid ID")
        try:
            return db.query(InsuranceType).filter(InsuranceType.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def get_all(self, db: Session) -> List[InsuranceType]:
        try:
            return db.query(InsuranceType).all()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def create(self, db: Session, obj_in: InsuranceTypeCreate) -> InsuranceType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


insurance_type = CRUDInsuranceType(InsuranceType)
