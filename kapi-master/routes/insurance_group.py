from typing import List
from fastapi import APIRouter, Depends, HTTPException
import crud
from auth import get_active_user, verify_role
from constants.roles import Role
from schemas import InsuranceGroup, User, InsuranceGroupUpdate, InsuranceGroupCreate

from sql_app import Session

insurance_group_router = APIRouter(
    prefix="/insurance-groups", tags=["Insurance Groups"]
)


@insurance_group_router.get(
    "", response_model=List[InsuranceGroup], name="Returns all Insurance Groups"
)
async def get_all(
    current_user: User = Depends(get_active_user), db: Session = Depends()
):
    """
    Returns all Insured Types
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.insurance_group.get_all(db=db)


@insurance_group_router.get(
    "/{insurance_group_id}",
    response_model=InsuranceGroup,
    name="Returns Insurance Group by ID",
)
async def get(
    insurance_group_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns Insurance Group by ID
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.insurance_group.get(db=db, id=insurance_group_id)


@insurance_group_router.post(
    "", response_model=InsuranceGroup, name="Creates a new Insurance Group"
)
async def create(
    insurance_group_in: InsuranceGroupCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a new Insurance Group
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    insurance_group_in.name = insurance_group_in.name.strip()

    insurance_group_db = crud.insurance_group.get_all(
        db=db, name=insurance_group_in.name
    )

    return crud.insurance_group.create(db=db, obj_in=insurance_group_in)


@insurance_group_router.put(
    "/{insurance_group_id}",
    response_model=InsuranceGroup,
    name="Updates a Insurance Group",
)
async def update(
    insurance_group_id: str,
    insurance_group_in: InsuranceGroupUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates a Insurance Group
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    insurance_group_db = crud.insurance_group.get(db=db, id=insurance_group_id)
    if insurance_group_db is None:
        raise HTTPException(status_code=404, detail="Insurance Type Not Found")

    return crud.insurance_group.update(
        db=db, db_obj=insurance_group_db, obj_in=insurance_group_in
    )
