from typing import Optional, List
from pydantic import UUID4, BaseModel
from schemas.athlete_competition import AthleteCompetition
from schemas.tournament import TournamentNoMatches
from schemas.team import Team


class InscriptionsTeams(BaseModel):
    team: Optional[Team] = None
    inscriptions_length: int
    athletes: List[UUID4]


class InscriptionsTournament(BaseModel):
    tournament: TournamentNoMatches
    inscriptions_length: int


class InscriptionBase(BaseModel):
    tournament_id: UUID4
    athlete_competition_id: UUID4
    confirmed: Optional[bool] = None
    accepted: Optional[bool] = None


class InscriptionCreate(BaseModel):
    tournament_id: Optional[UUID4] = None
    athlete_competition_id: Optional[UUID4] = None


class InscriptionUpdate(BaseModel):
    tournament_id: Optional[UUID4] = None
    athlete_competition_id: Optional[UUID4] = None
    confirmed: Optional[bool] = None
    accepted: Optional[bool] = None


class InscriptionInDBBase(InscriptionBase):
    athlete_competition: Optional[AthleteCompetition] = None
    tournament: Optional[TournamentNoMatches] = None
    payment_comprovative_url: str | None = None

    class Config:
        from_attributes = True


class Inscription(InscriptionInDBBase):
    pass


class InscriptionInDB(InscriptionInDBBase):
    pass
