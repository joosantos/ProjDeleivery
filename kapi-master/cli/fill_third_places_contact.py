from pydantic import UUID4

from sql_app import Session
from sqlalchemy import select
from models import Tournament
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/fill_third_places_contact.py
"""


def main(db: Session):
    fill_third_palce(
        tournament_id=UUID4("4b3884c8-f998-40db-b5e9-04304f3cc0e5"),
        athlete_id=UUID4("3009c191-0260-4c6f-91bb-ca256750497f"),
    )
    fill_third_palce(
        tournament_id=UUID4("a755e069-1b73-40e2-91df-606847229f3e"),
        athlete_id=UUID4("c94052fd-1d3a-439f-b0c2-abd0f034418a"),
    )
    fill_third_palce(
        tournament_id=UUID4("c737db81-05ac-4c7c-9aa0-a9854c864a26"),
        athlete_id=UUID4("32fe46bb-59ef-4683-9a53-eeee14f396a4"),
    )
    fill_third_palce(
        tournament_id=UUID4("aee9fd2e-bc6e-4527-afab-6d850b9273bb"),
        athlete_id=UUID4("b7add24b-448b-4141-9a37-6113ba13da6e"),
    )
    fill_third_palce(
        tournament_id=UUID4("dfd46457-43ad-4947-a4f7-d53bb614cf3e"),
        athlete_id=UUID4("c226f15a-d7c7-4ae2-9883-03498bb11216"),
    )

    commit_to_bd(session_db=db)


def fill_third_palce(tournament_id: UUID4, athlete_id: UUID4):
    query = select(Tournament).filter(Tournament.id == tournament_id)
    tournament = db.execute(query).first()
    if tournament is None:
        raise Exception("Tournament not found")
    tournament = tournament[0]
    tournament.third_place_id = athlete_id
    db.add(tournament)


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db)
    print("END")
