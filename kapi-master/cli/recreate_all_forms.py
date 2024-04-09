from pydantic import UUID4
import crud

from sql_app import Session
from schemas import Competition
from core.tournaments_utils import (
    create_matches_for_tournament,
    resolve_matches_of_tournament,
)

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/recreate_all_forms.py
"""

COMPETITION_ID = "eccb9b9b-4387-4789-ba7e-677af3e40b1e"


def main(db: Session):
    competition_db: Competition = crud.competition.get(db=db, id=COMPETITION_ID)
    total = len(competition_db.tournaments)

    for count, tournament in enumerate(iterable=competition_db.tournaments, start=1):
        print(f"Analising tournament {count} of {total}")
        if tournament.category.category_type.name == "Tournament":
            continue
        create_matches_for_tournament(db=db, tournament=tournament)
        resolve_matches_of_tournament(
            db=db, tournament=tournament, athlete_bye_id=-1, delete_current_podium=True
        )


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
