from pydantic import UUID4
import crud

from sql_app import Session
from schemas import Competition, MatchCreate
from models import Tournament
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/copy_tournaments.py
"""

# CATEGORIES = {
#     "ring": {
#         "categories": ["Kempo Contact"],
#         "age_min": 0,
#     },
#     "fomrs": {
#         "categories": [
#             "Weapon Forms Open" "Empty Hands Forms Open",
#             "Empty Hands Forms Hard Open",
#             "Empty Hands Forms Soft Open",
#             "Weapon Forms Hard Open",
#             "Weapon Forms Soft Open",
#             "Team Empty Hands Forms Open",
#             "Self Defense Open",
#         ],
#         "age_min": 14,
#     },
#     "combats": {
#         "categories": ["Rumble Kids", "Light Kempo", "Semi Kempo Open"],
#         "age_min": 14,
#     },
# }

CATEGORIES = {
    "combats": {
        "categories": ["Kempo Gladiadores", "Kempo Gladiadores - Duplas"],
        "age_min": 14,
    }
}


def main(db: Session, competition_id: UUID4):
    competition_db: Competition = crud.competition.get(db=db, id=competition_id)
    total = len(competition_db.tournaments)

    for count, tournament in enumerate(iterable=competition_db.tournaments, start=1):
        print(f"Analising tournament {count} of {total}")
        for categories_group in CATEGORIES:
            if tournament.category.name in CATEGORIES[categories_group]["categories"]:
                if (
                    tournament.age_min >= CATEGORIES[categories_group]["age_min"]
                    and len(tournament.inscriptions) > 4
                    and accepted_inscriptions(tournament.inscriptions) > 4
                ):
                    new_tournament = Tournament(
                        is_male=tournament.is_male,
                        age_min=tournament.age_min,
                        age_max=tournament.age_max,
                        day=3,
                        order=tournament.order,
                        morning=tournament.morning,
                        weight_min=tournament.weight_min,
                        weight_max=tournament.weight_max,
                        belt_min_id=tournament.belt_min_id,
                        belt_max_id=tournament.belt_max_id,
                        area=tournament.area,
                        category_id=tournament.category_id,
                        competition_id=tournament.competition_id,
                    )
                    db.add(new_tournament)

                    new_tournament = commit_to_bd(session_db=db, db_obj=new_tournament)
                    for i in range(1, 5):
                        crud.match.create(
                            db=db,
                            obj_in=MatchCreate(
                                athlete_red_id=None, athlete_blue_id=None, number=i
                            ),
                            tournament_id=new_tournament.id,
                        )


def accepted_inscriptions(inscriptions):
    t = 0
    for i in inscriptions:
        if i.accepted and i.confirmed:
            t += 1
    return t


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db, competition_id=UUID4("81078150-8440-4031-b7e7-013953efe7e8"))
    print("END")
