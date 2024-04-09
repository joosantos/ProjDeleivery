from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from crud.base import CRUDBase
from models.role import Role
from schemas.role import RoleCreate, RoleUpdate
from core.utils import commit_to_bd
from sql_app import Session


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        try:
            return db.query(Role).filter(Role.name == name).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def create(self, db: Session, obj_in: RoleCreate) -> Role:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


role = CRUDRole(Role)
