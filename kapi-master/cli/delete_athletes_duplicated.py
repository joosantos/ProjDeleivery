from models import Athlete, PrivateInfo, IdentificationDocument, Address, Responsible
from sql_app import Session

from sqlalchemy import text


def main(db: Session):
    query = """
select p.federation_number, count(p.federation_number)
from private_info p
join athletes a on a.private_info_id = p.id
group by p.federation_number 
having count(p.federation_number) > 1;"""

    results = db.execute(text(query))
    for result in results:
        athletes = (
            db.query(Athlete)
            .join(PrivateInfo)
            .filter(PrivateInfo.federation_number == result[0])
            .all()
        )
        if len(athletes) == 2:
            try:
                delete_athlete(athletes[0].id)
            except:
                print(f"Athelte {athletes[0].name} couldn't delete first")
                try:
                    delete_athlete(athletes[1].id)
                except:
                    print("WARNING")
                    print(f"Athelte {athletes[0].name} couldn't delete second")
                    continue
    return


def delete_athlete(id, db: Session):
    athlete = db.query(Athlete).filter(Athlete.id == id).first()
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
    db.delete(athlete)
    db.delete(private_info)
    db.delete(responsible)
    db.delete(address)
    db.delete(identification_document)
    db.delete(responsible_identification_document)
    try:
        db.commit()
    except:
        db.rollback()
        raise Exception("Error writing to DB")
    print(f"Deleted {athlete.name}")


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db)
    print("END")
