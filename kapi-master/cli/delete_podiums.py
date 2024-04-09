from pydantic import UUID4

from sql_app import Session
from sqlalchemy import select
from models import Tournament
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/delete_podiums.py
"""


def main(db: Session, competition_id: UUID4):
    query = select(Tournament).filter(
        Tournament.day == 2, Tournament.competition_id == competition_id
    )
    tournaments = db.scalars(query).all()
    total = len(tournaments)
    for count, tournament in enumerate(iterable=tournaments, start=1):
        print(f"Processing tournament {count} of {total}")

        tournament.first_place_id = None
        tournament.second_place_id = None
        tournament.third_place_id = None
        db.add(tournament)
    commit_to_bd(session_db=db)


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db, competition_id=UUID4("81078150-8440-4031-b7e7-013953efe7e8"))
    print("END")
