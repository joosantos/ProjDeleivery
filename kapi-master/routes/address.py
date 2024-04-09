from fastapi import APIRouter, Depends
import crud
from auth import get_active_user, verify_role
from constants.roles import Role
from schemas import User, AddressUpdate

from sql_app import Session

address_router = APIRouter(prefix="/addresses", tags=["Athlete's Address"])


@address_router.put("/{address_id}", name="Updates an Address")
async def update(
    address_id,
    address_in: AddressUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    address_db = crud.address.get(db=db, id=address_id)

    crud.address.update(db=db, db_obj=address_db, obj_in=address_in)
    return
