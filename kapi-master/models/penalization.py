from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Penalization(Base):
    __tablename__ = "penalizations"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    description = Column(String(255))
    points = Column(Float)

    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    competition_id = Column(UUID(as_uuid=True), ForeignKey("competitions.id"))

    team = relationship("Team")
    competition = relationship("Competition", back_populates="penalizations")
