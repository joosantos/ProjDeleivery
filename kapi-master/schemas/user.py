from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

from .insured_entity import InsuredEntity
from .user_role import UserRole


class PasswordIn(BaseModel):
    password: str


class PasswordChangeIn(PasswordIn):
    old_password: str


class Email(BaseModel):
    email: str


class AthleteToAssociate(BaseModel):
    athlete_id: UUID4


class UserRegister(BaseModel):
    email: str
    name: str
    password: str


class UserBase(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    email_verified: Optional[bool] = False
    admin_verified: Optional[bool] = False
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    insured_entity_id: Optional[str] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    notes: Optional[str] = None


class UserInDBBase(UserBase):
    id: UUID4
    user_role: UserRole
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UserAdminBase(UserInDBBase):
    notes: Optional[str] = None
    insured_entity_id: Optional[UUID4] = None
    athlete_id: Optional[UUID4] = None
    insured_entity: Optional[InsuredEntity] = None


# Additional properties stored in DB
class UserInDB(UserAdminBase):
    hashed_password: str
