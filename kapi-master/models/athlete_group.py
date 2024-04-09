from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


class AthleteGroup(Base):
    __tablename__ = "athletes_groups"
    athlete_competition_id = Column(
        UUID(as_uuid=True),
        ForeignKey("athlete_competitions.id"),
        primary_key=True,
        nullable=False,
    )
    athlete_id = Column(
        UUID(as_uuid=True), ForeignKey("athletes.id"), primary_key=True, nullable=False
    )

    athlete_competition = relationship(
        "AthleteCompetition",
        back_populates="athletes_group",
        uselist=True,
    )
    athlete = relationship("Athlete")
