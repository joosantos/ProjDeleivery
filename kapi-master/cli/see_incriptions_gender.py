from models import Competition, Tournament, Inscription
import crud
from sql_app import Session
from sqlalchemy import select
import pandas as pd
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/see_incriptions_gender.py
"""

OUTPUT_FILE = "cli/output_links.txt"

COMPETITION_ID = "eccb9b9b-4387-4789-ba7e-677af3e40b1e"

output = {}


def main(db: Session):
    competition: Competition = crud.competition.get(db=db, id=COMPETITION_ID)
    total_tournaments = len(competition.tournaments)
    i = 0
    for tournament in competition.tournaments:
        i = i + 1
        print(f"Processing tournament {i} of {total_tournaments}")
        if tournament.is_male is None:
            continue

        for match in tournament.matches:
            if match.athlete_red_id is not None:
                for group in match.athlete_red.athletes_group:
                    if group.athlete.is_male != tournament.is_male:
                        print(
                            f"Wrong atlhete {group.athlete.name} in category {tournament.category.name}"
                        )
            if match.athlete_blue_id is not None:
                for group in match.athlete_blue.athletes_group:
                    if group.athlete.is_male != tournament.is_male:
                        print(
                            f"Wrong atlhete {group.athlete.name} in category {tournament.category.name}"
                        )


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
