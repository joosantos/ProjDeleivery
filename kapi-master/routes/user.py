from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
import crud
from auth import get_active_user, verify_role
from constants.roles import Role
from schemas import (
    User,
    UserUpdate,
    UserAdmin,
    PageQueries,
    PagedResponse,
    AthleteToAssociate,
)
from pydantic import UUID4
from core.mail import (
    send_verified_coach,
    send_not_verified_coach,
    send_blocked_coach,
    send_unblocked_coach,
)

from sql_app import Session

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("/me", response_model=Union[User, None], name="Returns logged user")
async def read_self(current_user: User = Depends(get_active_user)):
    """
    Gets logged user
    """
    return current_user


@user_router.get(
    "/not-verified", response_model=List[User], name="Returns all users not verified"
)
async def not_verified(
    current_user: User = Depends(get_active_user), db: Session = Depends()
):
    """
    Gets all users not verified
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.user.get_all_not_verified(db=db)


@user_router.get(
    "",
    response_model=PagedResponse[UserAdmin],
    name="Returns all users paginated",
)
async def get_all(
    is_coach: bool | None = Query(
        None,
        description="User is a coach",
    ),
    name: str | None = Query(
        None,
        description="User name",
    ),
    athlete_associated: bool | None = Query(
        None,
        description="User has an athlete associated or not",
    ),
    pagination: PageQueries = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Gets all users
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    n_results, results = crud.user.get_all(
        db=db,
        is_coach=is_coach,
        name=name,
        athlete_associated=athlete_associated,
        skip=pagination.skip,
        limit=pagination.limit,
    )

    return PagedResponse(n_results=n_results, results=results)


@user_router.get(
    "/coaches", response_model=List[UserAdmin], name="Returns all active coaches"
)
async def active_coaches(
    current_user: User = Depends(get_active_user), db: Session = Depends()
):
    """
    Gets all active coaches
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.user.get_active_coaches(db=db)


@user_router.get("/{user_id}", response_model=UserAdmin, name="Returns logged " "user")
async def get_by_id(
    user_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Gets logged user
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.user.get(db=db, id=user_id)


@user_router.put(
    "/verify-coach/{coach_id}",
    response_model=Union[User, None],
    name="Verifies a coach account",
)
async def verify_coach(
    coach_id: str,
    coach_in: UserUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Verifies a coach account
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    coach_db: User = crud.user.get(db=db, id=coach_id)

    if coach_db is None:
        raise HTTPException(status_code=404, detail="Coach not Found")

    if coach_in.admin_verified is None:
        raise HTTPException(status_code=400, detail="Coach not Verified")

    if coach_db.admin_verified == coach_in.admin_verified:
        return coach_db

    coach: User = crud.user.update_data(
        db=db,
        obj_in=UserUpdate(admin_verified=coach_in.admin_verified is True),
        db_obj=coach_db,
    )

    if coach.admin_verified:
        background_tasks.add_task(send_verified_coach, coach.email)
    else:
        background_tasks.add_task(send_not_verified_coach, coach.email)

    return coach


@user_router.put(
    "/update-block/{coach_id}",
    response_model=Union[User, None],
    name="Blocks or unblocks a coach",
)
async def block_coach(
    coach_id: str,
    coach_in: UserUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Blocks or unblocks a coach
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    coach_db: User = crud.user.get(db=db, id=coach_id)

    if coach_db is None:
        raise HTTPException(status_code=404, detail="Coach not Found")

    if coach_in.is_active is None:
        raise HTTPException(status_code=400, detail="Coach not Blocked or Unblocked")

    if coach_db.is_active == coach_in.is_active:
        return coach_db

    coach: User = crud.user.update_data(
        db=db, obj_in=UserUpdate(is_active=coach_in.is_active is True), db_obj=coach_db
    )

    if not coach.is_active:
        background_tasks.add_task(send_blocked_coach, coach.email)
    else:
        background_tasks.add_task(send_unblocked_coach, coach.email)

        return coach


@user_router.put("/me", response_model=User, name="Updates authenticated user")
async def update_self(
    user_in: UserUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates authenticated User
    """

    return crud.user.update_data(db=db, obj_in=user_in, db_obj=current_user)


@user_router.put("/{user_id}", response_model=UserAdmin, name="Updates user")
async def update_by_id(
    user_id: str,
    user_in: UserUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates User
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    user_db = crud.user.get(db=db, id=user_id)

    if user_db is None:
        raise HTTPException(404, "User Not Found")

    user = crud.user.update_data(db=db, db_obj=user_db, obj_in=user_in)
    return user


@user_router.put(
    "/{user_id}/associate-athlete",
    response_model=UserAdmin,
    name="Associates athlete with user",
)
async def associate_athlete(
    user_id: UUID4,
    athlete_in: AthleteToAssociate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Associates Athlete With User
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    user_db = crud.user.get(db=db, id=user_id)
    athlete_db = crud.athlete.get(db=db, id=athlete_in.athlete_id)

    user = crud.user.associate_athlete(
        db=db, db_obj=user_db, athlete_id=athlete_in.athlete_id
    )
    crud.athlete.associate_user(db=db, db_obj=athlete_db, user_id=user_id)
    return user
