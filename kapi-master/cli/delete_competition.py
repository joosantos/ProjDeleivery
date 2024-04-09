import pandas as pd
from pydantic import UUID4
from sql_app import Session
from sqlalchemy import select

from datetime import datetime

from models import Competition

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/delete_competition.py
"""

COMPETITION_ID = "1e6dbfdd-3bbf-43ab-b0da-b7fd9f14cbba"


def main(db: Session):
    competition_query = select(Competition).filter(Competition.id == COMPETITION_ID)
    competition = db.scalars(competition_query).first()
    if competition is None:
        raise Exception("Competition Not Found")

    len_tournament = len(competition.tournaments)
    for index, tournament in enumerate(iterable=competition.tournaments, start=1):
        print(f"Deleting Tournament {index} of {len_tournament}")
        for match in tournament.matches:
            db.delete(match)
        for inscription in tournament.inscriptions:
            db.delete(inscription)
        db.commit()
        db.delete(tournament)

    db.commit()
    len_athletes = len(competition.athletes)
    for index, athlete in enumerate(iterable=competition.athletes, start=1):
        print(f"Deleting Tournament {index} of {len_athletes}")
        for group in athlete.athletes_group:
            db.delete(group)
        db.commit()
        db.delete(athlete)
    db.commit()
    db.delete(competition)
    db.commit()


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db)
    print("END")
