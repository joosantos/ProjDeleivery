from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import String, Column


class CategoryType(Base):
    __tablename__ = "category_types"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255), index=True)
    description = Column(String(1023), index=True)
