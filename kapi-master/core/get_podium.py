import crud
from models import Tournament
from schemas import Podium
from pydantic import UUID4, BaseModel
from typing import Optional
from sql_app import Session


class AthleteHelper(BaseModel):
    id: Optional[UUID4] = None
    wins: Optional[int] = None
    points: Optional[int] = None
    second_points: Optional[int] = None


def get_podium_forms(tournament: Tournament):
    matches = []
    podium: Podium = Podium(first=None, second=None, third=None)
    if len(tournament.matches) == 0:
        return podium
    if len(tournament.matches) == 1:
        podium.first = tournament.matches[0].athlete_red_id
        return podium

    for match in tournament.matches:
        if (
            match.points_red_total is None
            or match.points_red_central_referee_round1 is None
        ):
            return podium

    second = tournament.matches.copy()
    for match in tournament.matches:
        pop_index = 0
        highest_match = second[0]
        for index, second_match in enumerate(iterable=second, start=0):
            if index == 0:
                continue
            if highest_match.points_red_total == second_match.points_red_total:
                if (
                    highest_match.points_red_central_referee_round1
                    < second_match.points_red_central_referee_round1
                ):
                    highest_match = second_match
                    pop_index = index
            elif highest_match.points_red_total < second_match.points_red_total:
                highest_match = second_match
                pop_index = index
        second.pop(pop_index)
        matches.append(highest_match)

        if len(matches) == 3:
            break
    podium.first = matches[0].athlete_red_id
    if len(matches) > 1:
        podium.second = matches[1].athlete_red_id
    if len(matches) > 2:
        podium.third = matches[2].athlete_red_id
    return podium


def get_podium_one(tournament: Tournament):
    match = tournament.matches[0]
    podium: Podium = Podium(first=None, second=None, third=None)
    if match.winner_id is None:
        return podium
    podium.first = match.winner_id

    if match.athlete_red_id is None or match.athlete_blue_id is None:
        return podium

    if match.athlete_red_id == podium.first:
        podium.second = match.athlete_blue_id
        return podium

    podium.second = match.athlete_red_id
    return podium


def get_podium_three(tournament: Tournament):
    podium: Podium = Podium(first=None, second=None, third=None)
    if (
        tournament.matches[0].winner_id is None
        or tournament.matches[1].winner_id is None
        or tournament.matches[2].winner_id is None
    ):
        return podium

    athlete1: AthleteHelper = AthleteHelper(wins=0, points=0, second_points=0)
    athlete2: AthleteHelper = AthleteHelper(wins=0, points=0, second_points=0)
    athlete3: AthleteHelper = AthleteHelper(wins=0, points=0, second_points=0)

    match1 = tournament.matches[0]
    match2 = tournament.matches[1]

    athlete1.id = match1.athlete_red_id
    athlete2.id = match1.athlete_blue_id
    if (
        match1.athlete_red_id == match2.athlete_red_id
        or match1.athlete_blue_id == match2.athlete_red_id
    ):
        athlete3.id = match2.athlete_blue_id
    else:
        athlete3.id = match2.athlete_red_id

    for match in tournament.matches:
        if match.winner_id == athlete1.id:
            athlete1.wins += 1
            continue
        if match.winner_id == athlete2.id:
            athlete2.wins += 1
            continue
        if match.winner_id == athlete3.id:
            athlete3.wins += 1

    if not athlete1.wins == athlete2.wins:
        for athlete in [athlete1, athlete2, athlete3]:
            if athlete.wins == 2:
                podium.first = athlete.id
                continue
            if athlete.wins == 1:
                podium.second = athlete.id
                continue
            if athlete.wins == 0:
                podium.third = athlete.id
        return podium

    for match in tournament.matches:
        sum = (
            match.points_red_judge1_round2
            if match.points_red_judge1_round2 is not None
            else 0 + match.points_red_central_referee_round2
            if match.points_red_central_referee_round2 is not None
            else 0 + match.points_red_judge2_round2
            if match.points_red_judge2_round2 is not None
            else 0
        )
        if match.athlete_red_id == athlete1.id:
            athlete1.points += (
                match.points_red_total if match.points_red_total is not None else 0
            )
            athlete1.second_points += sum
        if match.athlete_red_id == athlete2.id:
            athlete2.points += (
                match.points_red_total if match.points_red_total is not None else 0
            )
            athlete2.second_points += sum
        if match.athlete_red_id == athlete3.id:
            athlete3.points += (
                match.points_red_total if match.points_red_total is not None else 0
            )
            athlete3.second_points += sum

        sum = (
            match.points_blue_judge1_round2
            if match.points_blue_judge1_round2 is not None
            else 0 + match.points_blue_central_referee_round2
            if match.points_blue_central_referee_round2 is not None
            else 0 + match.points_blue_judge2_round2
            if match.points_blue_judge2_round2 is not None
            else 0
        )

        if match.athlete_blue_id == athlete1.id:
            athlete1.points += (
                match.points_blue_total if match.points_blue_total is not None else 0
            )
            athlete1.second_points += sum
        if match.athlete_blue_id == athlete2.id:
            athlete2.points += (
                match.points_blue_total if match.points_blue_total is not None else 0
            )
            athlete2.second_points += sum
        if match.athlete_blue_id == athlete3.id:
            athlete3.points += (
                match.points_blue_total if match.points_blue_total is not None else 0
            )
            athlete3.second_points += sum

    if athlete1.points == athlete2.points and athlete2.points == athlete3.points:
        second_points = {
            athlete1.id: athlete1.second_points,
            athlete2.id: athlete2.second_points,
            athlete3.id: athlete3.second_points,
        }
        highest = sorted(second_points, key=second_points.get, reverse=True)[:3]
        podium.first = highest[0]
        podium.second = highest[1]
        podium.third = highest[2]
        return podium

    points = {
        athlete1.id: athlete1.points,
        athlete2.id: athlete2.points,
        athlete3.id: athlete3.points,
    }
    highest = sorted(points, key=points.get, reverse=True)[:3]

    if points[highest[0]] == points[highest[1]]:
        second_points = {athlete1.id: athlete1.points, athlete2.id: athlete2.points}
        highest_second = sorted(second_points, key=second_points.get, reverse=True)[:2]
        podium.first = highest_second[0]
        podium.second = highest_second[1]
        podium.third = highest[2]
        return podium

    podium.first = highest[0]
    if points[highest[1]] == points[highest[2]]:
        second_points = {
            athlete2.id: athlete2.second_points,
            athlete3.id: athlete3.second_points,
        }
        highest_second = sorted(second_points, key=second_points.get, reverse=True)[:2]
        podium.second = highest_second[0]
        podium.third = highest[1]
        return podium

    podium.second = highest[1]
    podium.third = highest[2]
    return podium


def get_podium_four_or_more(db: Session, tournament):
    podium: Podium = Podium(first=None, second=None, third=None)
    length = len(tournament.matches)
    match_final = None
    match_third = None
    bye = crud.athlete_competition.get_bye(
        db=db, competition_id=tournament.competition_id
    )
    bye_id = None
    if bye is not None:
        bye_id = bye.id
    has_bye = False
    potencial_third = None
    for match in tournament.matches:
        if length == 4 and match.number == 2:
            if match.athlete_blue_id is not None:
                if match.athlete_blue_id == bye_id:
                    has_bye = True
        if match.number == length:
            match_third = match
            continue
        if match.number == length - 1:
            match_final = match
            continue

    if match_final is None or match_final.winner_id is None or match_third is None:
        return podium

    podium.first = match_final.winner_id
    if match_final.athlete_red_id == podium.first:
        podium.second = match_final.athlete_blue_id
    else:
        podium.second = match_final.athlete_red_id

    if not has_bye and match_third.winner_id is None:
        return podium
    if has_bye or match_third.winner_id is None:
        podium.third = match_third.athlete_red_id
        return podium

    podium.third = match_third.winner_id
    return podium
