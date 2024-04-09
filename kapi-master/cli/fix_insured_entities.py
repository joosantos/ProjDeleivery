from models import (
    Athlete,
    PrivateInfo,
    Team,
    IdentificationDocument,
    Responsible,
    Address,
    InsuredEntity,
)
from sql_app import Session
from sqlalchemy import select
import csv
from datetime import datetime
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/fix_insured_entities.py
"""


def main(db: Session):
    athletes_query = select(Athlete).filter(Athlete.insured_entity_id == None)
    athletes = db.scalars(athletes_query).all()
    count = 1
    for athlete in athletes:
        print(f"Fixing athlete {count} of {len(athletes)}")
        count += 1
        insured_entity_query = select(InsuredEntity).filter(
            InsuredEntity.athlete_id == athlete.id
        )
        insured_entitiy = db.scalars(insured_entity_query).first()
        athlete.insured_entity_id = insured_entitiy.id
        db.add(athlete)

    try:
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception("Error commiting")


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
