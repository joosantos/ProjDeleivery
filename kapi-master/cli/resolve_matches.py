from pydantic import UUID4
import crud

from sql_app import Session
from schemas import Competition
from core.tournaments_utils import resolve_matches_of_tournament
import asyncio

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/resolve_matches.py
"""


def main(db: Session, competition_id: UUID4):
    competition_db: Competition = crud.competition.get(db=db, id=competition_id)
    total = len(competition_db.tournaments)
    count = 1
    for tournament in competition_db.tournaments:
        print(f"Tournament {count} of {total}")
        count += 1
        resolve_matches_of_tournament(
            db=db,
            tournament=tournament,
            athlete_bye_id=None,
            delete_current_podium=True,
        )


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db, competition_id=UUID4("81078150-8440-4031-b7e7-013953efe7e8"))
    print("END")
