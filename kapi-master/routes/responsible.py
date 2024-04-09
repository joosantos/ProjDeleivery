from fastapi import APIRouter, Depends
import crud
from auth import get_active_user, verify_role
from constants.roles import Role
from schemas import User, ResponsibleUpdate

from sql_app import Session

responsible_router = APIRouter(prefix="/responsible", tags=["Athlete's Responsible"])


@responsible_router.put("/{responsible_id}", name="Updates a Responsible")
async def update(
    responsible_id,
    responsible_in: ResponsibleUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    responsible_db = crud.responsible.get(db=db, id=responsible_id)

    crud.responsible.update(db=db, db_obj=responsible_db, obj_in=responsible_in)
    return
