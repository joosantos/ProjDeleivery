from typing import List, Union, Dict
import datetime
from fastapi import APIRouter, Depends, HTTPException
import crud
from auth import verify_role, get_role
from constants.roles import Role
from auth import get_active_user, get_active_user_or_none
from pydantic import TypeAdapter
from schemas import (
    Team,
    TeamCreate,
    TeamUpdate,
    User,
    AthleteUpdate,
    TeamAdmin,
    InsuranceCreate,
    InsuredEntityCreate,
    InsuranceCreateDatetime,
)

from sql_app import Session

team_router = APIRouter(prefix="/teams", tags=["Team"])

TA_TEAM_LIST = TypeAdapter(list[Team])
TA_TEAM_ADMIN_LIST = TypeAdapter(list[TeamAdmin])


@team_router.get(
    "/coach/{coach_id}",
    response_model=List[Team],
    name="Returns all teams of the coach",
)
async def get_by_coach(coach_id: str, db: Session = Depends()):
    """
    Returns all Teams of the coach
    """
    return crud.team.get_all_by_coach(db=db, coach_id=coach_id)


@team_router.get(
    "", response_model=list[Team] | list[TeamAdmin], name="Returns all teams"
)
async def get_all(
    db: Session = Depends(), current_user: User = Depends(get_active_user_or_none)
):
    """
    Returns all teams
    """
    teams = crud.team.get_all(db=db)
    if get_role(current_user) == "ADMIN":
        return TA_TEAM_ADMIN_LIST.validate_python(teams)
    return TA_TEAM_LIST.validate_python(teams)


@team_router.get(
    "/name/{team_name}", response_model=Union[Team, None], name="Returns team by name"
)
async def get_by_name(team_name, db: Session = Depends()):
    """
    Returns Team by name
    """
    return crud.team.get_by_name(db=db, name=team_name)


@team_router.get(
    "/{team_id}", response_model=TeamAdmin, name="Returns team by ID with insurances"
)
async def get_by_id(team_id, db: Session = Depends()):
    """
    Returns Team by ID
    """
    return crud.team.get(db=db, id=team_id)


@team_router.get(
    "/{team_id}/insurances", response_model=TeamAdmin, name="Returns team by ID"
)
async def get_insurances_by_id(team_id, db: Session = Depends()):
    """
    Returns Team by ID
    """
    return crud.team.get(db=db, id=team_id)


@team_router.post("", response_model=Union[Team, None], name="Creates a new Team")
async def create(
    team_in: TeamCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Create a new Team
    """
    verify_role(current_user, [Role.COACH["name"]])

    error_exists = False
    error_message: Dict[str, str] = {}

    if team_in.name is None or team_in.name.strip() == "":
        error_message["name"] = "The team must have a name"
        error_exists = True

    if crud.team.get_by_name(db=db, name=team_in.name) is not None:
        error_message["name"] = "The team name must be unique"
        error_exists = True

    if team_in.abbreviation is None or team_in.abbreviation.strip() == "":
        error_message["abbreviation"] = "The team must have an abbreviation"
        error_exists = True

    if (
        crud.team.get_by_abbreviation(db=db, abbreviation=team_in.abbreviation)
        is not None
    ):
        error_message["abbreviation"] = "The team abbreviation must be unique"
        error_exists = True

    if team_in.association is None or team_in.association.strip() == "":
        error_message["association"] = "The team must have an association"
        error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    team_in.coach_id = current_user.id

    team_db = crud.team.create(db=db, obj_in=team_in)

    insured_entity_db = crud.insured_entity.create(
        db=db, obj_in=InsuredEntityCreate(team_id=team_db.id)
    )

    return crud.team.update(
        db=db,
        db_obj=team_db,
        obj_in=TeamUpdate(insured_entity_id=str(insured_entity_db.id)),
    )


@team_router.put(
    "/{team_id}", response_model=Union[Team, None], name="Creates a new Team"
)
async def update(
    team_id,
    team_in: TeamUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Create a new Team
    """
    verify_role(current_user, [Role.COACH["name"], Role.ADMIN["name"]])

    if get_role(current_user) == "COACH":
        del team_in.notes
        del team_in.federation_number

    error_exists = False
    error_message: Dict[str, str] = {}

    team_db = crud.team.get(db=db, id=team_id)

    if team_db is None:
        raise HTTPException(404, "Team not found")

    if team_in.name is not None and team_in.name.strip() == "":
        error_message["name"] = "The team must have a name"
        error_exists = True

    if team_in.abbreviation is not None and team_in.abbreviation.strip() == "":
        error_message["abbreviation"] = "The team must have an abbreviation"
        error_exists = True

    if team_in.association is not None and team_in.association.strip() == "":
        error_message["association"] = "The team must have an association"
        error_exists = True

    same_name = crud.team.get_by_name(db=db, name=team_in.name)
    if same_name is not None and same_name.id != team_db.id:
        error_message["name"] = "The team name must be unique"
        error_exists = True

    same_abr = crud.team.get_by_abbreviation(db=db, abbreviation=team_in.abbreviation)
    if same_abr is not None and same_abr.id != team_db.id:
        error_message["abbreviation"] = "The team abbreviation must be unique"
        error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    return crud.team.update(db=db, db_obj=team_db, obj_in=team_in)


@team_router.delete("/{team_id}", name="Deletes a Team")
async def delete_team(
    team_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Deletes a Team
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    team = crud.team.get(db=db, id=team_id)

    if team is None:
        raise HTTPException(404, "Team Not Found")

    athletes_team = crud.athlete.get_by_team(db=db, team_id=team_id)

    if len(athletes_team) != 0:
        for athlete in athletes_team:
            crud.athlete.update(
                db=db, db_obj=athlete, obj_in=AthleteUpdate(team_id=None)
            )
    return crud.team.delete(db=db, id=team_id)
