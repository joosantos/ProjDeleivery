import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    ForeignKey,
    Float,
    String,
)
from sqlalchemy.orm import relationship


class Match(Base):
    __tablename__ = "matches"
    _deep_hidden_fields = [
        "matches.tournament.matches",
        "matches.tournament.competition",
        "matches.tournament.inscriptions",
        "matches.tournament.category.tournaments",
        "matches.athlete_red.competition",
        "matches.athlete_red.matches",
        "matches.athlete_blue.matches",
        "matches.athlete_winner.matches",
        "matches.athlete_blue.competition",
        "matches.winner.competition",
        "matches.winner.matches",
    ]
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    number = Column(Integer)
    number_by_area = Column(Integer)
    points_red_total = Column(Float)
    points_red_central_referee_round1 = Column(Float)
    points_red_judge1_round1 = Column(Float)
    points_red_judge2_round1 = Column(Float)
    points_red_central_referee_round2 = Column(Float)
    points_red_judge1_round2 = Column(Float)
    points_red_judge2_round2 = Column(Float)
    points_blue_total = Column(Float)
    points_blue_central_referee_round1 = Column(Float)
    points_blue_judge1_round1 = Column(Float)
    points_blue_judge2_round1 = Column(Float)
    points_blue_central_referee_round2 = Column(Float)
    points_blue_judge1_round2 = Column(Float)
    points_blue_judge2_round2 = Column(Float)
    normal_win = Column(Boolean)
    abdicate_win = Column(Boolean)
    no_show_win = Column(Boolean)
    disqualified_win = Column(Boolean)

    call_request = Column(Boolean, default=False)
    number_call_request = Column(Integer, default=0)
    calls_made = Column(Integer, default=0)
    area_to_call = Column(String)
    description_to_micro = Column(String)
    call_type = Column(String)
    call_request_fireman = Column(Boolean, default=False)
    call_request_clean = Column(Boolean, default=False)

    winner_id = Column(UUID(as_uuid=True), ForeignKey("athlete_competitions.id"))
    athlete_red_id = Column(UUID(as_uuid=True), ForeignKey("athlete_competitions.id"))
    athlete_blue_id = Column(UUID(as_uuid=True), ForeignKey("athlete_competitions.id"))
    tournament_id = Column(UUID(as_uuid=True), ForeignKey("tournaments.id"))

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    tournament = relationship("Tournament", back_populates="matches")
    athlete_red = relationship(
        "AthleteCompetition",
        back_populates="matches",
        foreign_keys="Match.athlete_red_id",
    )
    athlete_blue = relationship(
        "AthleteCompetition",
        back_populates="matches",
        foreign_keys="Match.athlete_blue_id",
    )
    winner = relationship("AthleteCompetition", foreign_keys="Match.winner_id")
