import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import String, Column, DateTime, Boolean
from sqlalchemy.orm import relationship


class Competition(Base):
    __tablename__ = "competitions"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255), index=True)
    inscriptions_start = Column(DateTime)
    inscriptions_end = Column(DateTime)
    competition_start = Column(DateTime)
    competition_end = Column(DateTime)
    show_public = Column(Boolean, default=False)
    calculate_age_start_year = Column(Boolean, default=False)
    notes = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    tournaments = relationship(
        "Tournament",
        back_populates="competition",
        uselist=True,
        order_by="desc(Tournament.category_id), desc(Tournament.is_male), desc(Tournament.age_min), desc(Tournament.weight_min), desc(Tournament.belt_min_id)",
    )
    athletes = relationship(
        "AthleteCompetition",
        back_populates="competition",
        uselist=True,
    )
    penalizations = relationship(
        "Penalization",
        back_populates="competition",
        uselist=True,
    )
