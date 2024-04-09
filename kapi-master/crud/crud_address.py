from fastapi.encoders import jsonable_encoder
from crud.base import CRUDBase
from models import Address
from schemas import AddressCreate, AddressUpdate
from core.utils import commit_to_bd
from sql_app import Session


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    def create(self, db: Session, obj_in: AddressCreate) -> Address:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj: Address = Address(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


address = CRUDAddress(Address)
