import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = "teams"
    _deep_hidden_fields = [
        "team.coach.teams",
        "teams.coach.teams",
        "teams.athletes.team",
        "team.insured_entity.team",
    ]
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255))
    abbreviation = Column(String(255))
    association = Column(String(255))
    region = Column(String)
    district = Column(String)
    notes = Column(String)

    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    insured_entity_id = Column(UUID(as_uuid=True), ForeignKey("insured_entities.id"))
    federation_number = Column(Integer)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    athletes = relationship("Athlete", back_populates="team", uselist=True)
    coach = relationship("User", foreign_keys="Team.coach_id")
    insured_entity = relationship(
        "InsuredEntity",
        primaryjoin="Team.id==InsuredEntity.team_id",
        back_populates="team",
        uselist=False,
    )

    @property
    def federated_in_current_season(self) -> bool:
        current_year = datetime.datetime.now().year
        for insurance in self.insured_entity.insurances:
            if (
                insurance.start_date.year == current_year
                or insurance.end_date.year == current_year
            ):
                return True
        return False
