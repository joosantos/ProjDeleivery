import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class InsuredEntity(Base):
    __tablename__ = "insured_entities"
    _deep_hidden_fields = ["insured_entity.insurances.insured_entity"]
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athletes.id"))
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    insurances = relationship("Insurance")
    athlete = relationship(
        "Athlete",
        primaryjoin="InsuredEntity.athlete_id==Athlete.id",
        back_populates="insured_entity",
        uselist=False,
    )
    team = relationship(
        "Team",
        primaryjoin="Team.id==InsuredEntity.team_id",
        uselist=False,
    )
    user = relationship(
        "User",
        primaryjoin="User.id==InsuredEntity.user_id",
        uselist=False,
    )
