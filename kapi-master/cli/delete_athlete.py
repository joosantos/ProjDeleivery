import sys

from models import (
    Address,
    Athlete,
    IdentificationDocument,
    PrivateInfo,
    Responsible,
)
from sql_app import Session


def main(db: Session):
    athlete_number = sys.argv[1:][0]

    # athlete = (
    #     db.query(Athlete)
    #     .join(PrivateInfo)
    #     .filter(PrivateInfo.federation_number == athlete_number)
    #     .first()
    # )
    athlete = db.query(Athlete).filter(Athlete.id == athlete_number).first()
    if athlete is None:
        print("Not Found")
        return
    private_info = (
        db.query(PrivateInfo).filter(PrivateInfo.id == athlete.private_info_id).first()
    )
    responsible = (
        db.query(Responsible).filter(Responsible.id == athlete.responsible_id).first()
    )
    address = db.query(Address).filter(Address.id == athlete.address_id).first()
    identification_document = (
        db.query(IdentificationDocument)
        .filter(IdentificationDocument.id == private_info.identification_document_id)
        .first()
    )
    responsible_identification_document = (
        db.query(IdentificationDocument)
        .filter(IdentificationDocument.id == responsible.identification_document_id)
        .first()
    )
    print(athlete.name)
    db.delete(athlete)
    db.delete(private_info)
    db.delete(responsible)
    db.delete(address)
    db.delete(identification_document)
    db.delete(responsible_identification_document)
    db.commit()
    print("DELETED")


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
