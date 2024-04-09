from typing import Optional
from pydantic import UUID4, BaseModel


class CategoryTypeBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


class CategoryTypeCreate(CategoryTypeBase):
    pass


class CategoryTypeUpdate(CategoryTypeBase):
    pass


class CategoryTypeInDBBase(CategoryTypeBase):
    id: UUID4

    class Config:
        from_attributes = True


class CategoryType(CategoryTypeInDBBase):
    pass


class CategoryTypeInDB(CategoryTypeInDBBase):
    pass
