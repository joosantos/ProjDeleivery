from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import String, Column, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255), index=True)
    third_place = Column(Boolean, index=True)
    three_points = Column(Boolean, index=True)
    rounds = Column(Boolean, index=True)
    penalties = Column(Boolean, index=True)
    order = Column(Integer)
    number_all_at_once = Column(Boolean, index=True)
    team_category = Column(Boolean, index=True)
    team_number = Column(Integer, default=1)
    category_type_id = Column(UUID(as_uuid=True), ForeignKey("category_types.id"))

    tournaments = relationship("Tournament", back_populates="category", uselist=True)
    category_type = relationship("CategoryType")
