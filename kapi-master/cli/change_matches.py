from pydantic import UUID4
from typing import List
import crud

from sql_app import Session
from models import Tournament
from schemas import MatchCreate
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/change_matches_and_delete_tournament.py
"""


def main(db: Session, ids: List[UUID4]):
    for tournament_id in ids:
        old_tournament = crud.tournament.get(db=db, id=tournament_id)
        new_tournament = Tournament(
            is_male=old_tournament.is_male,
            age_min=old_tournament.age_min,
            age_max=old_tournament.age_max,
            day=3,
            order=old_tournament.order,
            morning=old_tournament.morning,
            weight_min=old_tournament.weight_min,
            weight_max=old_tournament.weight_max,
            belt_min_id=old_tournament.belt_min_id,
            belt_max_id=old_tournament.belt_max_id,
            area=old_tournament.area,
            category_id=old_tournament.category_id,
            competition_id=old_tournament.competition_id,
        )
        db.add(new_tournament)
        old_tournament.area = None
        old_tournament.day = None
        old_tournament.order = None
        old_tournament.morning = None
        db.add(old_tournament)
        new_tournament = commit_to_bd(session_db=db, db_obj=new_tournament)
        for i in range(1, 5):
            crud.match.create(
                db=db,
                obj_in=MatchCreate(athlete_red_id=None, athlete_blue_id=None, number=i),
                tournament_id=new_tournament.id,
            )


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(
        db=db,
        ids=[
            UUID4("f631b2ff-6d70-4abb-a95e-86c149183e1b"),
            UUID4("b0e8ce08-038e-4bb1-a52f-3c42f8586bac"),
        ],
    )
    print("END")
