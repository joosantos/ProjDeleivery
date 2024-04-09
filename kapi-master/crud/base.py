from datetime import datetime
from typing import Generic, Type, TypeVar
import traceback
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel
from core.utils import commit_to_bd
from sql_app import Session
from core.utils import validate_uuid4

from sql_app import Base

# Define custom types for SQLAlchemy model, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """Base class that can be extend by other action classes.
           Provides basic CRUD and listing operations.

        :param model: The SQLAlchemy model
        :type model: Type[ModelType]
        """
        self.model = model

    def get(self, db: Session, id: UUID4) -> ModelType:
        if not validate_uuid4(id):
            raise HTTPException(400, "Invalid ID")
        try:
            obj_db = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")
        if obj_db is None:
            raise HTTPException(404, "Not Found")
        return obj_db

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = ModelType(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        refresh_and_return: bool = True,
    ) -> ModelType:
        try:
            obj_data = db_obj.to_json()
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            if refresh_and_return:
                return commit_to_bd(session_db=db, db_obj=db_obj)
            return commit_to_bd(session_db=db)
        except Exception as e:
            print(e)
            print(repr(e))
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Server error updating to DB")

    def delete(self, db: Session, id: UUID4) -> ModelType:
        obj = db.query(self.model).get(id)
        if obj is None:
            raise HTTPException(404)
        db.delete(obj)
        commit_to_bd(session_db=db)
        return obj

    def soft_delete(self, db: Session, db_obj: ModelType) -> ModelType:
        setattr(db_obj, "deleted_at", datetime.now())
        db.add(db_obj)
        return commit_to_bd(session_db=db, db_obj=db_obj)
