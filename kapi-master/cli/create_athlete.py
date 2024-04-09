from models import (
    Athlete,
    PrivateInfo,
    Address,
    IdentificationDocument,
    Responsible,
    Team,
)
from sql_app import Session
from sqlalchemy import select
import pandas as pd
from core.utils import commit_to_bd
import sys

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/create_athlete.py
"""

FIELDS = {
    "num_fed": "Nº Fed",
    "team": "Abreviatura",
    "name": "Nome",
}


def main(db: Session):
    team_abr = input("Team abbreviation: ").upper()
    query_team = select(Team).filter(Team.abbreviation == team_abr)
    team = db.scalars(query_team).first()
    if team is not None:
        team = team.id

    name = input("Athlete's name: ")
    fed_num = int(input("Athlete's federation number: "))

    responsible_identification_document = IdentificationDocument()
    responsible_identification_document = commit_to_bd(
        session_db=db, db_obj=responsible_identification_document
    )
    responsible = Responsible(
        identification_document_id=responsible_identification_document.id
    )
    responsible = commit_to_bd(session_db=db, db_obj=responsible)
    address = Address()
    address = commit_to_bd(session_db=db, db_obj=address)
    identification_document = IdentificationDocument()
    identification_document = commit_to_bd(
        session_db=db, db_obj=identification_document
    )
    private_info = PrivateInfo(
        identification_document_id=identification_document.id, federation_number=fed_num
    )
    private_info = commit_to_bd(session_db=db, db_obj=private_info)
    athlete = Athlete(
        name=name,
        responsible_id=responsible.id,
        private_info_id=private_info.id,
        address_id=address.id,
        team_id=team,
    )
    athlete = commit_to_bd(session_db=db, db_obj=athlete)
    return


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
