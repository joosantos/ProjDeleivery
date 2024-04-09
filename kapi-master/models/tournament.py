import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


class Tournament(Base):
    __tablename__ = "tournaments"
    _deep_hidden_fields = [
        "tournaments.competition",
        "tournaments.category",
        "tournaments.inscriptions.tournament",
        "tournaments.inscriptions.athlete_competition",
        "tournaments.matches.tournament",
        "tournaments.matches.tournament",
        "matches.tournament",
    ]
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    day = Column(Integer)
    order = Column(Integer)
    morning = Column(Boolean)
    is_male = Column(Boolean)
    age_min = Column(Integer)
    age_max = Column(Integer)
    weight_min = Column(Integer)
    weight_max = Column(Integer)
    belt = Column(String(255))
    central_referee = Column(String(255), index=True)
    judge1 = Column(String(255), index=True)
    judge2 = Column(String(255), index=True)
    area = Column(String(255), index=True)
    price = Column(Float)
    competition_id = Column(UUID(as_uuid=True), ForeignKey("competitions.id"))
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    first_place_id = Column(UUID(as_uuid=True), ForeignKey("athlete_competitions.id"))
    second_place_id = Column(UUID(as_uuid=True), ForeignKey("athlete_competitions.id"))
    third_place_id = Column(UUID(as_uuid=True), ForeignKey("athlete_competitions.id"))
    belt_min_id = Column(UUID(as_uuid=True), ForeignKey("belts.id"))
    belt_max_id = Column(UUID(as_uuid=True), ForeignKey("belts.id"))

    printed = Column(Boolean, default=False)
    podium_notes = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    competition = relationship("Competition", back_populates="tournaments")
    category = relationship("Category", back_populates="tournaments")
    first_place = relationship(
        "AthleteCompetition", foreign_keys="Tournament.first_place_id"
    )
    second_place = relationship(
        "AthleteCompetition", foreign_keys="Tournament.second_place_id"
    )
    third_place = relationship(
        "AthleteCompetition", foreign_keys="Tournament.third_place_id"
    )
    belt_min = relationship("Belt", foreign_keys="Tournament.belt_min_id")
    belt_max = relationship("Belt", foreign_keys="Tournament.belt_max_id")
    matches = relationship("Match", back_populates="tournament", uselist=True)
    inscriptions = relationship(
        "Inscription", back_populates="tournament", uselist=True
    )
