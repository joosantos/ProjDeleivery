from typing import Optional
from pydantic import UUID4, BaseModel


class AddressBase(BaseModel):
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressInDBBase(AddressBase):
    id: UUID4

    class Config:
        from_attributes = True


class Address(AddressInDBBase):
    pass


class AddressInDB(AddressInDBBase):
    pass
