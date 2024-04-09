import datetime
from fastapi import APIRouter, Depends, HTTPException

import crud
from auth import get_active_user, verify_role
from constants.roles import Role
from schemas import User, IdentificationDocumentUpdate

from sql_app import Session


identification_document_router = APIRouter(
    prefix="/identification-documents", tags=["Athlete's Private Info"]
)


@identification_document_router.put(
    "/{identification_document_id}", name="Updates a Identification Document"
)
async def update(
    identification_document_id,
    identification_document_in: IdentificationDocumentUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    identification_document_db = crud.identification_document.get(
        db=db, id=identification_document_id
    )
    if identification_document_in.expiration_date == "":
        identification_document_in.expiration_date = None

    if identification_document_in.expiration_date is not None:
        format = "%d-%m-%Y"
        try:
            identification_document_in.expiration_date = datetime.datetime.strptime(
                identification_document_in.expiration_date, format
            )
        except:
            raise HTTPException(422, "Invalid Expiration Date")

    crud.identification_document.update(
        db=db, db_obj=identification_document_db, obj_in=identification_document_in
    )
    return
