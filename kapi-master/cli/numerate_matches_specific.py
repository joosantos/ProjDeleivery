from pydantic import UUID4
from typing import List, Dict
import crud

from sql_app import Session
from schemas import Tournament, Competition
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/numerate_matches_specific.py
"""

CATEGORIES = {
    "ring": {
        "categories": ["Kempo Contact"],
        "age_min": 19,
    },
    "combats": {
        "categories": [
            "Rumble Kids",
            "Light Kempo",
            "Semi Kempo Open",
            "Kempo Gladiadores",
            "Kempo Gladiadores - Duplas",
        ],
        "age_min": 14,
    },
}


def main(db: Session, competition_id: UUID4):
    competition_db: Competition = crud.competition.get(db=db, id=competition_id)
    tournaments: Dict[int, Dict[bool, Dict[int, list[Tournament]]]] = {}

    for tournament in competition_db.tournaments:
        if tournament.day is None or len(tournament.matches) == 0:
            continue

        is_specially_numbered = False
        for categories_group in CATEGORIES:
            if (
                tournament.category.name in CATEGORIES[categories_group]["categories"]
                and tournament.age_min >= CATEGORIES[categories_group]["age_min"]
            ) and tournament.day == 2:
                is_specially_numbered = True
                break

        if not is_specially_numbered:
            continue

        if tournament.day not in tournaments:
            tournaments[tournament.day] = {True: {}, False: {}}
        if tournament.morning:
            if tournament.area not in tournaments[tournament.day][True]:
                tournaments[tournament.day][True][tournament.area] = []

            tournaments[tournament.day][True][tournament.area].append(tournament)
        else:
            if tournament.area not in tournaments[tournament.day][False]:
                tournaments[tournament.day][False][tournament.area] = []

            tournaments[tournament.day][False][tournament.area].append(tournament)
    count = 1
    for day in tournaments:
        for morning in tournaments[day]:
            for area in tournaments[day][morning]:
                print(
                    f"Numering tournament {count} day {day} morning {morning} area {area}"
                )
                count += 1
                number_matches_area(
                    db=db,
                    tournaments_array=tournaments[day][morning][area],
                    athlete_bye_id=-1,
                )


def number_matches_area(
    db: Session,
    tournaments_array: List[Tournament],
    athlete_bye_id: UUID4 | None,
):
    def order_tournaments(k):
        if k.order is None:
            return -1
        return k.order

    def order_matches(k):
        if k.number is None:
            return -1
        return k.number

    if len(tournaments_array) == 0:
        return

    # Order tournaments
    tournaments_array.sort(key=order_tournaments)

    # Separate tournaments by category
    tournament_area_by_cat: Dict[str, List[Tournament]] = {}
    for t in tournaments_array:
        if t.category.name not in tournament_area_by_cat:
            tournament_area_by_cat[t.category.name] = []
        tournament_area_by_cat[t.category.name].append(t)

    area_number = 1
    quantity_missing = []
    for tournaments_by_cat in tournament_area_by_cat:
        # Remove all numbers from the matches
        for tournament in tournament_area_by_cat[tournaments_by_cat]:
            for match in tournament.matches:
                if match.number_by_area is not None:
                    match.number_by_area = None
                    db.add(match)

    commit_to_bd(session_db=db)
    for tournaments_by_cat in tournament_area_by_cat:
        # If matches need to be numbered in order
        if (
            tournament_area_by_cat[tournaments_by_cat][0].category.number_all_at_once
            or tournament_area_by_cat[tournaments_by_cat][0].category.category_type.name
            != "Tournament"
        ):
            if (
                tournament_area_by_cat[tournaments_by_cat][
                    0
                ].category.category_type.name
                == "Tournament"
            ):
                for tournament in tournament_area_by_cat[tournaments_by_cat]:
                    tournament.matches.sort(key=order_matches)
                    matches_len = len(tournament.matches)
                    counter = 0
                    if matches_len > 3:
                        for match in tournament.matches:
                            counter += 1
                            if match.winner_id is not None:
                                continue
                            if match.number <= matches_len / 2 and (
                                match.athlete_blue_id is None
                                or match.athlete_red_id is None
                                or match.athlete_blue_id == athlete_bye_id
                                or match.athlete_red_id == athlete_bye_id
                            ):
                                continue
                            if counter == matches_len - 1:
                                if len(quantity_missing) == 0:
                                    quantity_missing.append(area_number)
                                    area_number += 1
                                    match.number_by_area = area_number
                                    db.add(match)
                                    area_number += 1
                                    continue
                                if len(quantity_missing) == 1:
                                    match.number_by_area = area_number
                                    db.add(match)
                                    area_number += 1
                                    continue
                                if len(quantity_missing) > 1:
                                    match.number_by_area = quantity_missing[1]
                                    db.add(match)
                                    quantity_missing.pop(1)
                                    continue
                            if len(quantity_missing) != 0:
                                match.number_by_area = quantity_missing[0]
                                db.add(match)
                                quantity_missing.pop(0)
                            else:
                                match.number_by_area = area_number
                                db.add(match)
                                area_number += 1
                    else:
                        for match in tournament.matches:
                            if match.winner_id is not None:
                                continue
                            if len(quantity_missing) != 0:
                                match.number_by_area = quantity_missing[0]
                                db.add(match)
                                quantity_missing.pop(0)
                            else:
                                match.number_by_area = area_number
                                db.add(match)
                                area_number += 1
                continue
            else:
                for tournament in tournament_area_by_cat[tournaments_by_cat]:
                    tournament.matches.sort(key=order_matches)
                    for match in tournament.matches:
                        if match.winner_id is not None:
                            continue
                        if len(quantity_missing) != 0:
                            match.number_by_area = quantity_missing[0]
                            db.add(match)
                            quantity_missing.pop(0)
                        else:
                            match.number_by_area = area_number
                            db.add(match)
                            area_number += 1
            continue

        # If matches don't need to be numbered in order
        # Number round of 32 only
        for tournament in tournament_area_by_cat[tournaments_by_cat]:
            tournament.matches.sort(key=order_matches)
            matches_len = len(tournament.matches)
            if matches_len == 32:
                match_number = 1
                limit_number = 17
                while limit_number != match_number:
                    for match in tournament.matches:
                        if match.winner_id is not None:
                            continue
                        if match.number == match_number:
                            if (
                                match.athlete_blue_id is None
                                or match.athlete_red_id is None
                            ):
                                break
                            match.number_by_area = area_number
                            db.add(match)
                            area_number += 1
                            break
                    match_number += 1
        # Number round of 16 only
        for tournament in tournament_area_by_cat[tournaments_by_cat]:
            matches_len = len(tournament.matches)
            if matches_len >= 16:
                match_number = 1
                limit_number = 9
                if matches_len == 32:
                    match_number += 16
                    limit_number += 16
                while limit_number != match_number:
                    for match in tournament.matches:
                        if match.winner_id is not None:
                            continue
                        if match.number == match_number:
                            if (
                                match.athlete_blue_id is None
                                or match.athlete_red_id is None
                            ) and matches_len == 16:
                                break
                            match.number_by_area = area_number
                            db.add(match)
                            area_number += 1
                            break
                    match_number += 1
        # Number quarter-finals only
        for tournament in tournament_area_by_cat[tournaments_by_cat]:
            matches_len = len(tournament.matches)
            if matches_len >= 8:
                match_number = 1
                limit_number = 5
                if matches_len == 32:
                    match_number += 16
                    limit_number += 16
                if matches_len >= 16:
                    match_number += 8
                    limit_number += 8
                while limit_number != match_number:
                    for match in tournament.matches:
                        if match.winner_id is not None:
                            continue
                        if match.number == match_number:
                            if (
                                match.athlete_blue_id is None
                                or match.athlete_red_id is None
                            ) and matches_len == 8:
                                break
                            match.number_by_area = area_number
                            db.add(match)
                            area_number += 1
                            break
                    match_number += 1

        # We only want to number until the semi-final so skip the rest
        if tournaments_by_cat != "Kempo Contact":
            continue
        for tournament in tournament_area_by_cat[tournaments_by_cat]:
            matches_len = len(tournament.matches)
            if matches_len >= 4:
                match_number = 1
                limit_number = 3
                if matches_len == 32:
                    match_number += 16
                    limit_number += 16
                if matches_len >= 16:
                    match_number += 8
                    limit_number += 8
                if matches_len >= 8:
                    match_number += 4
                    limit_number += 4
                while limit_number != match_number:
                    for match in tournament.matches:
                        if match.winner_id is not None:
                            continue
                        if match.number == match_number:
                            if (
                                match.athlete_blue_id is None
                                or match.athlete_red_id is None
                                or match.athlete_blue_id == athlete_bye_id
                                or match.athlete_red_id == athlete_bye_id
                            ) and matches_len == 4:
                                break
                            match.number_by_area = area_number
                            db.add(match)
                            area_number += 1
                            break
                    match_number += 1

        # Tournaments with 3 matches will be counted as "final"

        # Number only third place qualification
        for tournament in tournament_area_by_cat[tournaments_by_cat]:
            matches_len = len(tournament.matches)
            if matches_len == 3 or matches_len == 1:
                continue
            if matches_len >= 2 and matches_len != 3:
                match_number = 2
                if matches_len == 32:
                    match_number += 16
                if matches_len >= 16:
                    match_number += 8
                if matches_len >= 8:
                    match_number += 4
                if matches_len >= 4:
                    match_number += 2
            else:
                continue
            # Check if bye is present in tournament
            bye_present = False
            if matches_len == 4:
                for match in tournament.matches:
                    if match.winner_id is not None:
                        continue
                    if (
                        athlete_bye_id == match.athlete_blue_id
                        or athlete_bye_id == match.athlete_red_id
                    ):
                        bye_present = True
                        break

            # Number the third place qualification
            if bye_present and match_number == 4:
                match_number -= 1
                continue
            for match in tournament.matches:
                if match.winner_id is not None:
                    continue
                if match.number == match_number:
                    if len(quantity_missing) != 0:
                        match.number_by_area = quantity_missing[0]
                        db.add(match)
                        quantity_missing.pop(0)
                        break
                    match.number_by_area = area_number
                    db.add(match)
                    area_number += 1

    commit_to_bd(session_db=db)


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db, competition_id=UUID4("81078150-8440-4031-b7e7-013953efe7e8"))
    print("END")
