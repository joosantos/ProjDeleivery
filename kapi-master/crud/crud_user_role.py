from typing import Optional
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4

from crud.base import CRUDBase
from models.user_role import UserRole
from schemas.user_role import UserRoleCreate, UserRoleUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleUpdate]):
    def get_by_user_id(self, db: Session, user_id: UUID4) -> Optional[UserRole]:
        if not validate_uuid4(user_id):
            raise HTTPException(status_code=422, detail="Invalid ID")
        try:
            return db.query(UserRole).filter(UserRole.user_id == user_id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="Error accessing the DB")

    def multi_create(self, db: Session, obj_in) -> None:
        db.bulk_insert_mappings(
            UserRole, [dict(user_id=obj.user_id, role_id=obj.role_id) for obj in obj_in]
        )

        commit_to_bd(session_db=db)

    def create(self, db: Session, obj_in: UserRoleCreate) -> UserRole:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


user_role = CRUDUserRole(UserRole)
