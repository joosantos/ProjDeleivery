from fastapi import HTTPException
from pydantic import UUID4
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from crud.base import CRUDBase
from models import PrivateInfo
from schemas import PrivateInfoCreate, PrivateInfoUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDPrivateInfo(CRUDBase[PrivateInfo, PrivateInfoCreate, PrivateInfoUpdate]):
    def get(self, db: Session, id: UUID4) -> PrivateInfo:
        if not validate_uuid4(id):
            raise HTTPException(400, "Invalid ID")
        try:
            aux = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")
        if aux is None:
            raise HTTPException(404, "Not Found")
        return aux

    def get_highest_fed_number(self, db: Session) -> int:
        try:
            return db.query(func.max(PrivateInfo.federation_number)).first()[0]
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(404)

    def create(self, db: Session, obj_in: PrivateInfoCreate) -> PrivateInfo:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = PrivateInfo(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


private_info = CRUDPrivateInfo(PrivateInfo)
