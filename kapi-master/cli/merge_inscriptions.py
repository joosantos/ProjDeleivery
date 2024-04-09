from datetime import datetime
from typing import List, Optional
from sqlalchemy import and_, select, func, text, or_, Integer
from core.utils import commit_to_bd

import crud
from schemas import TournamentUpdate, InscriptionUpdate
from models import Tournament, Inscription

from sql_app import Session

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/merge_inscriptions.py
"""


COMPETITION_ID = "eccb9b9b-4387-4789-ba7e-677af3e40b1e"

CATEGORIES = [
    "Rumble Kids",
    "Semi Kempo",
]

RUMBLE_INIT = "d87506db-33c2-442f-ab4b-2ea4d2a06513"
SEMI_INIT = "595cac52-cc82-43a2-a4bc-041d3c6e6857"
cache = {}


def main(db: Session):
    competition = crud.competition.get(db=db, id=COMPETITION_ID)
    white_belt = crud.belt.get_by_name(db=db, name="white")
    orange_belt = crud.belt.get_by_name(db=db, name="orange")
    purple_belt = crud.belt.get_by_name(db=db, name="orange-purple")
    black_belt = crud.belt.get_by_name(db=db, name="black")
    if (
        white_belt is None
        or orange_belt is None
        or purple_belt is None
        or black_belt is None
    ):
        print("Belt not found")
        return

    number_tournaments = len(competition.tournaments)

    for index, tournament in enumerate(iterable=competition.tournaments, start=1):
        print(f"Processing Tournament number {index} of {number_tournaments}")
        if tournament.category.name not in CATEGORIES:
            continue

        if tournament.belt_min_id == purple_belt.id:
            continue

        if tournament.belt_min_id == white_belt.id:
            tourn = Tournament(
                competition_id=COMPETITION_ID,
                category_id=SEMI_INIT
                if tournament.category.name == "Semi Kempo"
                else RUMBLE_INIT,
                is_male=tournament.is_male,
                age_min=tournament.age_min,
                age_max=tournament.age_max,
                weight_min=tournament.weight_min,
                weight_max=tournament.weight_max,
                belt_min_id=tournament.belt_min_id,
                belt_max_id=tournament.belt_max_id,
            )
            db.add(tourn)
            tourn = commit_to_bd(session_db=db, db_obj=tourn)

        elif tournament.belt_min_id is None:
            tournament.belt_min_id = purple_belt.id
            tournament.belt_max_id = black_belt.id
            db.add(tournament)
            tourn = Tournament(
                competition_id=COMPETITION_ID,
                category_id=SEMI_INIT
                if tournament.category.name == "Semi Kempo"
                else RUMBLE_INIT,
                is_male=tournament.is_male,
                age_min=tournament.age_min,
                age_max=tournament.age_max,
                weight_min=tournament.weight_min,
                weight_max=tournament.weight_max,
                belt_min_id=white_belt.id,
                belt_max_id=orange_belt.id,
            )
            db.add(tourn)
            tourn = commit_to_bd(session_db=db, db_obj=tourn)
        for inscription in tournament.inscriptions:
            if inscription.athlete_competition.athletes_group[0].athlete.belt.order < 6:
                inscription.tournament_id = tourn.id
                db.add(inscription)

    commit_to_bd(session_db=db)


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
