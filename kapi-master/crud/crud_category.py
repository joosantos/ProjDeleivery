from typing import List, Optional
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import not_, select
from crud.base import CRUDBase
from models import Category, Tournament
from schemas import CategoryCreate, CategoryUpdate
from core.utils import validate_uuid4, commit_to_bd
from sql_app import Session


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get(self, db: Session, id: UUID4) -> Optional[Category]:
        if not validate_uuid4(id):
            return None
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(
        self,
        db: Session,
        defaults: bool | None,
        competition_id: UUID4 | None,
        limit: int,
        skip: int,
    ) -> tuple[list[Category], int]:
        sql_string = select(Category).distinct()

        if competition_id:
            sql_string = sql_string.join(Tournament).filter(
                Tournament.competition_id == competition_id
            )
        if defaults is not None:
            if defaults:
                sql_string = sql_string.filter(Category.name.contains("DEFAULT"))
            else:
                sql_string = sql_string.filter(not_(Category.name.contains("DEFAULT")))

        try:
            n_results = len(db.scalars(sql_string).all())

            if limit != -1:
                sql_string = sql_string.offset(skip).limit(limit)

            sql_string = sql_string.order_by(Category.name)

            return db.scalars(sql_string).all(), n_results
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Database Error")

        try:
            if defaults:
                return (
                    db.query(self.model)
                    .filter(self.model.name.contains("DEFAULT"))
                    .order_by(self.model.name.asc())
                    .all()
                )
            else:
                return (
                    db.query(self.model)
                    .filter(not_(self.model.name.contains("DEFAULT")))
                    .order_by(self.model.name.asc())
                    .all()
                )
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        try:
            return db.query(self.model).filter(self.model.name == name).first()
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def create(self, db: Session, obj_in: CategoryCreate) -> Category:
        db_obj = Category(
            name=obj_in.name,
            third_place=obj_in.third_place,
            three_points=obj_in.three_points,
            rounds=obj_in.rounds,
            penalties=obj_in.penalties,
            number_all_at_once=obj_in.number_all_at_once,
            team_category=obj_in.team_category,
            team_number=obj_in.team_number,
            order=obj_in.order,
            category_type_id=obj_in.category_type_id,
        )
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


category = CRUDCategory(Category)
