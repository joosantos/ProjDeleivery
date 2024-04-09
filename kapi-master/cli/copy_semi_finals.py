from pydantic import UUID4

from sql_app import Session
from sqlalchemy import select
from models import Tournament, Match as MatchModel
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/copy_semi_finals.py
"""


def main(db: Session, competition_id: UUID4):
    query = select(Tournament).filter(
        Tournament.day == 2, Tournament.competition_id == competition_id
    )
    tournaments = db.scalars(query).all()
    total = len(tournaments)
    for count, tournament in enumerate(iterable=tournaments, start=1):
        print(f"Processing tournament {count} of {total}")
        query = select(Tournament).filter(
            Tournament.day == 3,
            Tournament.age_min == tournament.age_min,
            Tournament.age_max == tournament.age_max,
            Tournament.belt_max_id == tournament.belt_max_id,
            Tournament.belt_min_id == tournament.belt_min_id,
            Tournament.weight_max == tournament.weight_max,
            Tournament.weight_min == tournament.weight_min,
            Tournament.is_male == tournament.is_male,
            Tournament.category_id == tournament.category_id,
        )
        day3_tournament = db.execute(query).first()
        if day3_tournament is None:
            if tournament.category.name == "Kempo Gladiadores":
                continue
            print(
                f"""{tournament.category.name}
gender: {"Open" if tournament.is_male is None else "Masc." if tournament.is_male else "Fem." }
age: {tournament.age_min}/{tournament.age_max}
belt: {tournament.belt_min.name}-{tournament.belt_max.name}
weight: {tournament.weight_min}-{tournament.weight_max} Kg."""
            )
            print("=====================")
        else:
            day3_tournament = day3_tournament[0]

        total_matches = len(tournament.matches)
        semi_finals_numbers = []
        if tournament.category.name == "Kempo Contact":
            for match in tournament.matches:
                if match.number == len(tournament.matches) - 1:
                    day3_tournament.matches[0].athlete_red_id = match.athlete_red_id
                    day3_tournament.matches[0].athlete_blue_id = match.athlete_blue_id
            continue
        if tournament.category.category_type.name == "Tournament":
            if total_matches == 8:
                semi_finals_numbers = [5, 6]
            if total_matches == 16:
                semi_finals_numbers = [13, 14]
            if total_matches == 32:
                semi_finals_numbers = [29, 30]

        athletes = []
        if tournament.category.category_type.name == "Tournament":
            for match in tournament.matches:
                if match.number in semi_finals_numbers:
                    if match.number in [5, 13, 29]:
                        if (
                            match.athlete_red_id is not None
                            and match.athlete_red_id not in athletes
                        ):
                            athletes.append(match.athlete_red_id)
                        if (
                            match.athlete_blue_id is not None
                            and match.athlete_blue_id not in athletes
                        ):
                            athletes.append(match.athlete_blue_id)
                    if match.number in [6, 14, 30]:
                        if (
                            match.athlete_red_id is not None
                            and match.athlete_red_id not in athletes
                        ):
                            athletes.append(match.athlete_red_id)
                        if (
                            match.athlete_blue_id is not None
                            and match.athlete_blue_id not in athletes
                        ):
                            athletes.append(match.athlete_blue_id)
            if len(athletes) == 4:
                for match in tournament.matches:
                    if match.number in semi_finals_numbers:
                        if match.number in [5, 13, 29]:
                            for day3_match in day3_tournament.matches:
                                if day3_match.number == 1:
                                    day3_match.athlete_red_id = str(
                                        match.athlete_red_id
                                    )
                                    day3_match.athlete_blue_id = str(
                                        match.athlete_blue_id
                                    )
                                    db.add(day3_match)
                                    break
                        if match.number in [6, 14, 30]:
                            for day3_match in day3_tournament.matches:
                                if day3_match.number == 2:
                                    day3_match.athlete_red_id = str(
                                        match.athlete_red_id
                                    )
                                    day3_match.athlete_blue_id = str(
                                        match.athlete_blue_id
                                    )
                                    db.add(day3_match)
                                    break
            elif len(athletes) == 3:
                for day3_match in day3_tournament.matches:
                    if day3_match.number == 4:
                        db.delete(day3_match)
                for match in tournament.matches:
                    for day3_match in day3_tournament.matches:
                        if day3_match.number == 1:
                            day3_match.athlete_red_id = str(athletes[0])
                            day3_match.athlete_blue_id = str(athletes[1])
                            db.add(day3_match)
                        if day3_match.number == 2:
                            day3_match.athlete_red_id = str(athletes[0])
                            day3_match.athlete_blue_id = str(athletes[2])
                            db.add(day3_match)
                        if day3_match.number == 3:
                            day3_match.athlete_red_id = str(athletes[1])
                            day3_match.athlete_blue_id = str(athletes[2])
                            db.add(day3_match)
            elif len(athletes) <= 2 and len(athletes) > 0:
                for day3_match in day3_tournament.matches:
                    if day3_match.number in [2, 3, 4]:
                        db.delete(day3_match)
                    if day3_match.number == 1:
                        day3_match.athlete_red_id = str(athletes[0])
                        day3_match.athlete_blue_id = (
                            str(athletes[1]) if len(athletes) == 2 else None
                        )
                        db.add(day3_match)
            commit_to_bd(session_db=db)

        else:
            athletes = get_top_4(tournament=tournament)
            for idx, match in enumerate(iterable=day3_tournament.matches, start=0):
                if len(athletes) < idx + 1:
                    break
                match.athlete_red_id = str(athletes[idx])
                db.add(match)
            if len(athletes) > 4:
                for idx in range(5, len(athletes) - 3):
                    match = MatchModel(
                        tournament_id=tournament.id,
                        number=idx,
                        athlete_red_id=str(athletes[idx - 1]),
                    )
                    db.add(match)

    commit_to_bd(session_db=db)


def get_top_4(tournament: Tournament):
    first = []
    first_points = 0
    second = []
    second_points = 0
    third = []
    third_points = 0
    forth = []
    forth_points = 0
    for match in tournament.matches:
        if match.points_red_total is None:
            continue
        if match.points_red_total >= first_points:
            if match.points_red_total == first_points:
                first.append(match.athlete_red_id)
            else:
                forth = third
                forth_points = third_points
                third = second
                third_points = second_points
                second = first
                second_points = first_points
                first = [match.athlete_red_id]
                first_points = match.points_red_total
            continue
        if match.points_red_total >= second_points:
            if match.points_red_total == second_points:
                second.append(match.athlete_red_id)
            else:
                forth = third
                forth_points = third_points
                third = second
                third_points = second_points
                second = [match.athlete_red_id]
                second_points = match.points_red_total
            continue
        if match.points_red_total >= third_points:
            if match.points_red_total == third_points:
                third.append(match.athlete_red_id)
            else:
                forth = third
                forth_points = third_points
                third = [match.athlete_red_id]
                third_points = match.points_red_total
            continue
        if match.points_red_total >= forth_points:
            if match.points_red_total == forth_points:
                forth.append(match.athlete_red_id)
            else:
                forth = [match.athlete_red_id]
                forth_points = match.points_red_total
            continue

    top_four = []
    top_four += first
    if len(top_four) == 4:
        return top_four
    top_four += second
    if len(top_four) == 4:
        return top_four
    top_four += third
    if len(top_four) == 4:
        return top_four
    top_four += forth
    return top_four


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db, competition_id=UUID4("81078150-8440-4031-b7e7-013953efe7e8"))
    print("END")
