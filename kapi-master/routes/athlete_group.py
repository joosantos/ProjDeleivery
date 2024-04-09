from typing import Union, Optional
from fastapi import APIRouter, Depends, HTTPException
import crud
from auth import get_active_user
from schemas import AthleteGroup, AthleteGroupCreate, Athlete, AthleteCompetition, User

from sql_app import Session

athlete_group_router = APIRouter(prefix="/athletes-group", tags=["Athletes Group"])


@athlete_group_router.post(
    "", response_model=Union[AthleteGroup, None], name="Creates a Group of Athletes"
)
async def create(
    athlete_group_in: AthleteGroupCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a Group of Athletes
    """

    if (
        current_user.user_role.role.name != "COACH"
        and current_user.user_role.role.name != "ADMIN"
    ):
        raise HTTPException(401, "Insufficient Permissions")

    athlete: Optional[Athlete] = crud.athlete.get(db=db, id=athlete_group_in.athlete_id)
    if athlete is None:
        raise HTTPException(status_code=404, detail="Athlete Not Found")

    athlete_competition: Optional[AthleteCompetition] = crud.athlete_competition.get(
        db=db, id=athlete_group_in.athlete_competition_id
    )
    if athlete_competition is None:
        raise HTTPException(status_code=404, detail="Athlete Not in the competition")

    return crud.athlete_group.create(db=db, obj_in=athlete_group_in)


@athlete_group_router.delete(
    "/{athlete_competition_id}/{athlete_id}",
    response_model=Union[AthleteGroup, None],
    name="Deletes a Group of Athletes",
)
async def delete(
    athlete_competition_id,
    athlete_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Deletes a Group of Athletes
    """

    if (
        current_user.user_role.role.name != "COACH"
        and current_user.user_role.role.name != "ADMIN"
    ):
        raise HTTPException(401, "Insufficient Permissions")

    return crud.athlete_group.delete_group(
        db=db, athlete_competition_id=athlete_competition_id, athlete_id=athlete_id
    )
