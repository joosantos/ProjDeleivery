import datetime
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class Inscription(Base):
    __tablename__ = "inscriptions"
    tournament_id = Column(
        UUID(as_uuid=True), ForeignKey("tournaments.id"), primary_key=True, index=True
    )
    athlete_competition_id = Column(
        UUID(as_uuid=True),
        ForeignKey("athlete_competitions.id"),
        primary_key=True,
        index=True,
    )
    confirmed = Column(Boolean, default=False)
    accepted = Column(Boolean, default=False)
    payment_comprovative_url = Column(String(255))

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    tournament = relationship("Tournament", back_populates="inscriptions")
    athlete_competition = relationship("AthleteCompetition")
