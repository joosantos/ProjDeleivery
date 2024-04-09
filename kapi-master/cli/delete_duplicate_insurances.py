from models import (
    Athlete,
    PrivateInfo,
    Team,
    IdentificationDocument,
    Responsible,
    Address,
    InsuredEntity,
    Insurance,
    InsuranceStatusEnum,
)
from sql_app import Session
from sqlalchemy import select, text, or_, func
import csv
from datetime import datetime
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/delete_duplicate_insurances.py
"""


def main(db: Session):
    insurnaces_query = text(
        """select insurances.insured_entity_id
from insurances
group by insurances.insured_entity_id
having count(insurances.insured_entity_id) > 1;"""
    )
    insurnaces_ids = db.scalars(insurnaces_query).all()
    insurnaces_query_2 = (
        select(Insurance)
        .filter(
            or_(
                func.extract("year", Insurance.start_date) == 2024,
                func.extract("year", Insurance.end_date) == 2024,
            )
        )
        .filter(Insurance.insured_entity_id.in_(insurnaces_ids))
    )
    insurnaces: list[Insurance] = db.scalars(insurnaces_query_2).all()

    cache_insurnaces = {}
    for insurance in insurnaces:
        if str(insurance.insured_entity_id) not in cache_insurnaces:
            cache_insurnaces[str(insurance.insured_entity_id)] = {}

        cache_insurnaces[str(insurance.insured_entity_id)][insurance.id] = {
            "obj": insurance,
            "status": insurance.status,
        }

    for insured_entity_id in cache_insurnaces:
        accepted = 0
        for insurnace_id in cache_insurnaces[insured_entity_id]:
            if (
                cache_insurnaces[insured_entity_id][insurnace_id]["status"]
                == InsuranceStatusEnum.accepted.value
            ):
                accepted = accepted + 1
        if accepted == 1:
            for insurnace_id in cache_insurnaces[insured_entity_id]:
                if (
                    cache_insurnaces[insured_entity_id][insurnace_id]["status"]
                    != InsuranceStatusEnum.accepted.value
                ):
                    db.delete(cache_insurnaces[insured_entity_id][insurnace_id]["obj"])
    commit_to_bd(session_db=db)


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
