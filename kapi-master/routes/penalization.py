from pydantic import UUID4
from fastapi import APIRouter, Depends, Query

from constants.roles import Role
from auth import get_active_user, verify_role
import crud
from schemas import (
    Penalization,
    PenalizationCreate,
    User,
    PageQueries,
    PagedResponse,
)
from sql_app import Session

penalization_router = APIRouter(prefix="/penalizations", tags=["Penalization"])


@penalization_router.get(
    "", response_model=PagedResponse[Penalization], name="Gets all penalizations"
)
async def get_all(
    competition_id: UUID4 = Query(default=..., description="ID of the competition"),
    pagination: PageQueries = Depends(),
    db: Session = Depends(),
):
    """
    Gets all penalizations
    """

    results, n_results = crud.penalization.get_all(
        db=db,
        competition_id=competition_id,
        limit=pagination.limit,
        skip=pagination.skip,
    )
    return PagedResponse(n_results=n_results, results=results)


@penalization_router.post("", response_model=Penalization, name="Add a penalization")
async def create(
    penalization_in: PenalizationCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a penalization
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.penalization.create(db=db, obj_in=penalization_in)


@penalization_router.delete(
    "/{penalization_id}", response_model=Penalization, name="Deletes a penalization"
)
async def delete(
    penalization_id: UUID4,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Deletes a penalization
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.penalization.delete(db=db, id=penalization_id)
