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

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/name_matches_excel.py
"""

FIELDS = {
    "num_fed": "Nº Fed",
    "team": "Abreviatura",
    "name": "Nome",
}


def main(db: Session):
    df = pd.read_csv("cli/fplk_db.csv")
    for i in range(1000):
        num_fed = int(
            str(df[FIELDS["num_fed"]][i]).replace("*", "").replace("+", "").strip()
        )
        print(num_fed)
        team_abr = str(df[FIELDS["team"]][i].strip())
        athlete_name = str(df[FIELDS["name"]][i].strip())
        query = (
            select(Athlete)
            .join(PrivateInfo)
            .filter(PrivateInfo.federation_number == num_fed)
        )
        results = db.scalars(query).all()
        if len(results) == 0:
            query = select(Athlete).filter(Athlete.name == athlete_name)
            results = db.scalars(query).all()
            if len(results) == 0:
                print(f"Must create athlete num {num_fed}")
            if len(results) == 1:
                print("Must add federation number to this athlete")
            if len(results) >= 2:
                print("More than 2 athletes with same name")
        if len(results) == 1:
            if results[0].name == athlete_name:
                continue
            else:
                print(f"Wrong name for athlete {num_fed}")
    return


def create_athlete(fed_num: int, name: str, team_abr: str):
    query_team = select(Team).filter(Team.abbreviation == team_abr)
    team = db.scalars(query_team).first()
    if team is not None:
        team = team.id

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
    return athlete


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
