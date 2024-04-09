from typing import List, Union, Dict
from fastapi import APIRouter, Depends, HTTPException
import crud
from auth import get_active_user, verify_role
from schemas import AthleteCompetition, User
from constants.roles import Role

from sql_app import Session

athlete_competition_router = APIRouter(
    prefix="/competitions/{competition_id}/athlete-competition",
    tags=["Athlete Competition"],
)


@athlete_competition_router.get(
    "/{athlete_competition_id}",
    response_model=Union[AthleteCompetition, None],
    name="Returns an athlete of the competition by ID",
)
async def get_by_id(
    competition_id,
    athlete_competition_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns an athlete of the competition by ID
    """
    return crud.athlete_competition.get(db=db, id=athlete_competition_id)


@athlete_competition_router.get(
    "",
    response_model=List[AthleteCompetition],
    name="Returns all athletes of the competition",
)
async def get_by_competition(
    competition_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns all athletes of the competition
    """
    a = {"appel": "red", "grape": "purple", "orange": "orange", "lemon": "yellow"}
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.athlete_competition.get_all(db=db, competition_id=competition_id)


@athlete_competition_router.post(
    "",
    response_model=Union[AthleteCompetition, None],
    name="Adds an athlete to the competition",
)
async def create(
    competition_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Adds a new athlete to the competition
    """

    if (
        current_user.user_role.role.name != "COACH"
        and current_user.user_role.role.name != "ADMIN"
    ):
        raise HTTPException(401, "Insufficient Permissions")

    error_exists = False
    error_message: Dict[str, str] = {}

    competition = crud.competition.get(db=db, id=competition_id)
    if competition is None:
        error_message["competition"] = "The competition doesn't exist"
        error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    return crud.athlete_competition.create(db=db, competition_id=competition_id)


@athlete_competition_router.delete(
    "/{athlete_competition_id}",
    response_model=Union[AthleteCompetition, None],
    name="Deletes an athlete to the competition",
)
async def delete(
    competition_id,
    athlete_competition_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Deletes a new athlete to the competition
    """

    if (
        current_user.user_role.role.name != "COACH"
        and current_user.user_role.role.name != "ADMIN"
    ):
        raise HTTPException(401, "Insufficient Permissions")

    athlete_competition: AthleteCompetition = crud.athlete_competition.get(
        db=db, id=athlete_competition_id
    )

    if athlete_competition is None:
        raise HTTPException(status_code=404, detail="Athlete Competition Not Found")

    return crud.athlete_competition.delete(db=db, id=athlete_competition_id)
