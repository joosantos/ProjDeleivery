from datetime import timedelta
from typing import Optional
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT, AuthJWTRefresh
from pydantic import BaseModel
from typing import Union
import crud
from auth import get_active_user
from core.jwt_tokens import decode_password_token, encode_password_token
from core.mail import send_mail, send_register_confirmation, send_verify_admin
from models import User
from schemas import (
    UserRegister,
    UserUpdate,
    User as UserSchema,
    Email,
    PasswordChangeIn,
    PasswordIn,
    UserRoleCreate,
)
from core.environment import config
from core.utils import verify_password
from constants.roles import Role

from sql_app import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

SECRET = config.get("jwt.secret") or "123"
URL_BASE_FRONTEND = config.get("app.url")


@auth_router.post(
    "/register", response_model=Union[UserSchema, None], name="Registers a new user"
)
def register(
    user_in: UserRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(),
):
    """
    Registers a new user.
    """

    role_aux = crud.role.get_by_name(db=db, name=Role.COACH["name"])

    user_db: Optional[UserSchema] = crud.user.get_by_email(db=db, email=user_in.email)

    if user_db is not None:
        raise HTTPException(
            status_code=409, detail={"email": "This email is already registered"}
        )

    user: UserSchema = crud.user.register(db=db, obj_in=user_in)
    crud.user_role.create(
        db=db,
        obj_in=UserRoleCreate(
            user_id=user.id,
            role_id=role_aux.id,
        ),
    )

    background_tasks.add_task(
        send_register_confirmation, recipient=user.email, id=user.id
    )
    background_tasks.add_task(send_verify_admin)

    return crud.user.get(db=db, id=user.id)


@auth_router.get(
    "/confirms/resend/{email}",
    response_model=bool,
    name="Resends email verification email",
)
async def resend_confirm_email(
    email: EmailStr,
    background_tasks: BackgroundTasks,
    db: Session = Depends(),
):
    user_db: UserSchema = crud.user.get_by_email(db=db, email=email)

    if user_db is None:
        raise HTTPException(
            status_code=404,
            detail="User Not Found",
        )

    if user_db.email_verified:
        raise HTTPException(
            status_code=409,
            detail="User Email already verified",
        )

    background_tasks.add_task(
        send_register_confirmation, recipient=user_db.email, id=user_db.id
    )
    return True


@auth_router.put(
    "/confirms/{user_id}",
    response_model=Union[UserSchema, None],
    name="Confirms user email",
)
async def confirm_email(
    user_id: str,
    db: Session = Depends(),
):
    """
    Confirms User Email
    """

    user_db: Optional[UserSchema] = crud.user.get(db=db, id=user_id)

    if user_db is None:
        raise HTTPException(
            status_code=404,
            detail="User Not Found",
        )

    if user_db.email_verified:
        raise HTTPException(
            status_code=409,
            detail="User Email already verified",
        )

    return crud.user.update_data(
        db=db, obj_in=UserUpdate(email_verified=True), db_obj=user_db
    )


@auth_router.post("/password", name="Change password")
def change_password(
    passwords: PasswordChangeIn,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Changes the password of the current user
    """

    if passwords.old_password == "" or passwords.password == "":
        raise HTTPException(status_code=422, detail={"data": "Invalid Data Received"})

    error_message = {}

    error_exists = False
    if not verify_password(passwords.old_password, current_user.hashed_password):
        error_message["old_password"] = "Wrong password"
        error_exists = True

    if passwords.password == passwords.old_password:
        error_message["new_password"] = "Your password can't be the same as the old one"
        error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    # Updates user password
    aux: Optional[User] = crud.user.get(db=db, id=current_user.id)
    if aux is None:
        raise HTTPException(status_code=422, detail={"user": "Invalid User"})
    db_user: User = aux

    user: User = crud.user.update(
        db=db,
        obj_in=UserUpdate(password=passwords.password),
        db_obj=db_user,
    )
    return user


@auth_router.post("/password/{token}", name="Password Change on case user forgot")
async def update_password(
    token: str,
    password: PasswordIn,
    db: Session = Depends(),
):
    """
    Changes the password in the special case that the user forgot the password
    """
    token_obj = decode_password_token(token)

    user: Optional[User] = crud.user.get(db=db, id=token_obj["user"])

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid Token")

    user_db: User = crud.user.update(
        db=db,
        obj_in=UserUpdate(password=password.password),
        db_obj=user,
    )

    if user_db is None:
        raise HTTPException(status_code=400, detail="Invalid Token")

    return user_db


@auth_router.post("/forgot-password", name="Account Recovery")
async def recover(
    email_obj: Email,
    db: Session = Depends(),
):
    """
    Sends email with a link to change the password
    """
    email = email_obj.email
    user: Optional[User] = crud.user.get_by_email(db=db, email=email)

    if user is not None:
        token = encode_password_token(user.id)
        await send_mail(
            [user.email],
            "<p>Click here <a href='"
            + URL_BASE_FRONTEND
            + "recover/password?token="
            + token
            + "'>link</a> to change your password.",
            "Password Recovery",
        )

    return "ok"


@auth_router.post("/recover/{token}", name="Password Change on case user forgot")
async def recover_password(
    token: str,
    password: PasswordIn,
    db: Session = Depends(),
):
    """
    Changes the password in the special case that the user forgot the password
    """
    token_obj = decode_password_token(token)

    user: Optional[User] = crud.user.get(db=db, id=token_obj["user"])

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid Token")

    user_db: User = crud.user.update_password(
        db=db,
        pass_in=password.password,
        db_obj=user,
    )

    if user_db is None:
        raise HTTPException(status_code=400, detail="Invalid Token")

    return user_db


@auth_router.post("/login", name="Login endpoint")
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    authorize: AuthJWT = Depends(),
    db: Session = Depends(),
):
    """
    Login
    """
    user = crud.user.authenticate(
        db=db, email=credentials.username, password=credentials.password
    )

    if user is None:
        raise HTTPException(status_code=400, detail={"email": "Invalid Credentials"})

    if not user.email_verified:
        raise HTTPException(status_code=403, detail={"email": "Email Not Verified"})

    if user.admin_verified is None:
        raise HTTPException(status_code=403, detail={"email": "Admin Not Verified"})

    if not user.admin_verified:
        raise HTTPException(status_code=403, detail={"email": "Admin Refuse"})

    if not user.is_active:
        raise HTTPException(status_code=403, detail={"email": "User Blocked"})

    """
    create_access_token supports an optional 'fresh' argument,
    which marks the token as fresh or non-fresh accordingly.
    As we just verified their username and password, we are
    going to mark the token as fresh here.
    """
    access_token = authorize.create_access_token(
        subject=str(user.id),
        fresh=True,
    )
    refresh_token = authorize.create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token}


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET
    authjwt_refresh_token_expires: timedelta = timedelta(days=1)


@AuthJWT.load_config
def get_config():
    return Settings()


@auth_router.post(
    "/refresh",
    name="Provides an access token if valid refresh token is provided",
)
def refresh(authorize: AuthJWTRefresh = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    if current_user is None:
        raise HTTPException(401)
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
