from models import (
    Athlete,
    PrivateInfo,
    Team,
    IdentificationDocument,
    Responsible,
    Insurance,
    Address,
    InsuredEntity,
    InsuranceStatusEnum,
)
from sql_app import Session
from sqlalchemy import select
import csv
from datetime import datetime
from core.utils import commit_to_bd
import crud

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/fix_federation_numbers.py
"""


def main(db: Session):
    sql_string = (
        select(PrivateInfo)
        .join(Athlete, Athlete.private_info_id == PrivateInfo.id)
        .join(InsuredEntity, Athlete.insured_entity_id == InsuredEntity.id)
        .join(Insurance, Insurance.insured_entity_id == InsuredEntity.id)
        .filter(Insurance.status == InsuranceStatusEnum.accepted.value)
        .filter(PrivateInfo.federation_number == None)
    )
    results = db.scalars(sql_string).all()
    print(len(results))
    i = 1
    for private_info in results:
        print(f"Processing {i} of {len(results)}")
        i = i + 1
        private_info.federation_number = (
            crud.private_info.get_highest_fed_number(db=db) + 1
        )
        db.add(private_info)
        db.commit()
    return


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
