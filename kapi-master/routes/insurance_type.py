from typing import List

from fastapi import APIRouter, Depends, HTTPException

import crud
from auth import get_active_user, verify_role
from constants.roles import Role
from schemas import InsuranceType, User, InsuranceTypeCreate, InsuranceTypeUpdate

from sql_app import Session

insurance_type_router = APIRouter(prefix="/insurance-types", tags=["Insurance Types"])


@insurance_type_router.get(
    "", response_model=List[InsuranceType], name="Returns all Insurance Types"
)
async def get_all(
    current_user: User = Depends(get_active_user), db: Session = Depends()
):
    """
    Returns all Insurance Types
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    return crud.insurance_type.get_all(db=db)


@insurance_type_router.get(
    "/{insurance_type_id}",
    response_model=InsuranceType,
    name="Returns Insurance Type by ID",
)
async def get(
    insurance_type_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns Insurance Type by ID
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.insurance_type.get(db=db, id=insurance_type_id)


@insurance_type_router.post(
    "", response_model=InsuranceType, name="Creates a new Insurance Type"
)
async def create(
    insurance_type_in: InsuranceTypeCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a new Insurance Type
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.insurance_type.create(db=db, obj_in=insurance_type_in)


@insurance_type_router.put(
    "/{insurance_type_id}",
    response_model=InsuranceType,
    name="Updates a Insurance Type",
)
async def update(
    insurance_type_id: str,
    insurance_type_in: InsuranceTypeUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates a Insurance Type
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    insurance_type_db = crud.insurance_type.get(db=db, id=insurance_type_id)
    if insurance_type_db is None:
        raise HTTPException(status_code=404, detail="Insurance Type Not Found")

    return crud.insurance_type.update(
        db=db, db_obj=insurance_type_db, obj_in=insurance_type_in
    )
