from typing import List

from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from models import User as UserModel
from schemas import User
from fastapi_jwt_auth.exceptions import InvalidHeaderError
from constants.roles import Role

from sqlalchemy import select
from sql_app import Session
from core.utils import validate_uuid4


async def get_active_user(
    authorize: AuthJWT = Depends(), db: Session = Depends()
) -> User:
    authorize.jwt_optional()
    uid = authorize.get_jwt_subject()
    if uid is None or not validate_uuid4(uid):
        raise HTTPException(401)
    user_query = select(UserModel).filter(UserModel.id == uid)
    user = db.scalars(user_query).first()
    if user is None:
        raise HTTPException(401)
    return user


async def get_active_user_or_none(
    authorize: AuthJWT = Depends(), db: Session = Depends()
) -> User | None:
    try:
        authorize.jwt_optional()
        uid = authorize.get_jwt_subject()
        if uid is None:
            return None
        user = db.query(UserModel).get(uid)
        return user
    except InvalidHeaderError as e:
        raise e
    else:
        return None


def verify_role(user: User, authorized_roles: List[str]):
    if user is None or user.user_role is None or user.user_role.role is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    user_role = user.user_role.role.name

    if not user.email_verified:
        raise HTTPException(status_code=403, detail="Email Not Verified")

    if user.admin_verified is None:
        raise HTTPException(status_code=403, detail="Admin Not Verified")

    if not user.admin_verified:
        raise HTTPException(status_code=403, detail="Admin Refuse")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User Blocked")

    if user_role is None:
        raise HTTPException(status_code=403, detail="Insufficient Permissions.")

    if user_role in authorized_roles or user_role == "ADMIN":
        return

    raise HTTPException(status_code=403, detail="Insufficient Permissions.")


def get_role(user: User):
    if user is None or user.user_role is None or user.user_role.role is None:
        return None
    return user.user_role.role.name


async def can_edit_athlete(athlete, team, current_user):
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    if get_role(current_user) == "ADMIN":
        return

    if athlete is None:
        raise HTTPException(status_code=404, detail="Athlete Not Found")

    if team is None:
        raise HTTPException(status_code=404, detail="Team Not Found")

    if athlete.team_id is None:
        raise HTTPException(401, "Insufficient Permissions")

    if team.coach_id == current_user.id:
        return
    raise HTTPException(401, "Insufficient Permissions")
