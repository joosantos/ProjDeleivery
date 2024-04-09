from models import Athlete, InsuredEntity
from sql_app import Session
from sqlalchemy import select

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/create_insure_entity_to_athletes.py
"""


def main(db: Session):
    athlete_query = select(Athlete).distinct()
    print(athlete_query)
    athletes = db.scalars(athlete_query).all()

    insured_entities = []
    for athlete in athletes:
        insured_entities.append(InsuredEntity(athlete_id=athlete.id))
    db.bulk_save_objects(insured_entities)
    db.commit()
    print("Athletes done")

    insured_entities_query = select(InsuredEntity).filter(
        InsuredEntity.athlete_id != None
    )
    insured_entities_db = db.scalars(insured_entities_query).all()

    athletes_to_update = []
    i = 0
    for insured_entity in insured_entities_db:
        print(f"{i} of {len(insured_entities_db)}")
        i += 1
        for athlete in athletes:
            if athlete.id == insured_entity.athlete_id:
                athlete.insured_entity_id = insured_entity.id
                athletes_to_update.append(athlete)
    db.bulk_save_objects(athletes_to_update)
    db.commit()


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
