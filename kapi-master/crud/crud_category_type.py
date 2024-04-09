from typing import List, Optional
from pydantic import UUID4
from crud.base import CRUDBase
from models import CategoryType
from schemas import CategoryTypeCreate, CategoryTypeUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDCategoryType(CRUDBase[CategoryType, CategoryTypeCreate, CategoryTypeUpdate]):
    def get(self, db: Session, id: UUID4) -> Optional[CategoryType]:
        if not validate_uuid4(id):
            return None
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def get_all(self, db: Session) -> List[CategoryType]:
        try:
            return db.query(self.model).order_by(self.model.name.asc()).all()
        except Exception as e:
            print(e)
            db.rollback()
            return []


category_type = CRUDCategoryType(CategoryType)
