from typing import Optional

from pydantic import UUID4, BaseModel
from .category_type import CategoryType


class CategoryName(BaseModel):
    id: UUID4
    name: str


class CategoryBase(BaseModel):
    name: Optional[str] = None
    third_place: Optional[bool] = None
    three_points: Optional[bool] = None
    rounds: Optional[bool] = None
    penalties: Optional[bool] = None
    number_all_at_once: Optional[bool] = None
    team_category: Optional[bool] = None
    team_number: Optional[int] = None
    order: Optional[int] = None
    category_type_id: Optional[UUID4] = None


# Properties to receive via API on creation
class CategoryCreate(CategoryBase):
    pass


# Properties to receive via API on update
class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    id: UUID4
    category_type: Optional[CategoryType] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class Category(CategoryInDBBase):
    pass


# Additional properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
