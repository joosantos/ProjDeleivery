import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class AthleteCompetition(Base):
    __tablename__ = "athlete_competitions"
    _deep_hidden_fields = ["athletes_group.athlete_competition", "competition"]
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    competition_id = Column(UUID(as_uuid=True), ForeignKey("competitions.id"))

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    competition = relationship("Competition", back_populates="athletes")
    athletes_group = relationship("AthleteGroup", back_populates="athlete_competition")
    matches = relationship(
        "Match",
        uselist=True,
        primaryjoin="and_(AthleteCompetition.id==Match.athlete_red_id, or_(AthleteCompetition.id==Match.athlete_blue_id))",
    )
