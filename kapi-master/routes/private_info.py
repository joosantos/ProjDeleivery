from fastapi import APIRouter, Depends
import crud
from auth import get_active_user, verify_role, get_role
from constants.roles import Role
from schemas import User, PrivateInfoUpdate

from sql_app import Session

private_info_router = APIRouter(prefix="/private-info", tags=["Athlete's Private Info"])


@private_info_router.put("/{private_info_id}", name="Updates a private info")
async def update(
    private_info_id,
    private_info_in: PrivateInfoUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    private_info_db = crud.private_info.get(db=db, id=private_info_id)

    if get_role(current_user) == "COACH":
        private_info_in.federation_active = private_info_db.federation_active
        private_info_in.federation_number = private_info_db.federation_number

    crud.private_info.update(db=db, db_obj=private_info_db, obj_in=private_info_in)
    return
