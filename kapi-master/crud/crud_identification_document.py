from fastapi import HTTPException
from pydantic import UUID4
from fastapi.encoders import jsonable_encoder
from crud.base import CRUDBase
from models import IdentificationDocument
from schemas import IdentificationDocumentCreate, IdentificationDocumentUpdate
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDIdentificationDocument(
    CRUDBase[
        IdentificationDocument,
        IdentificationDocumentCreate,
        IdentificationDocumentUpdate,
    ]
):
    def get(self, db: Session, id: UUID4) -> IdentificationDocument:
        if not validate_uuid4(id):
            raise HTTPException(400, "Invalid ID")
        try:
            aux = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")
        if aux is None:
            raise HTTPException(404, "Not Found")
        return aux

    def create(
        self, db: Session, obj_in: IdentificationDocumentCreate
    ) -> IdentificationDocument:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = IdentificationDocument(**obj_in_data)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


identification_document = CRUDIdentificationDocument(IdentificationDocument)
