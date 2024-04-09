import os
from pydantic import UUID4
from typing import List, Dict
from random import shuffle
from sql_app import Session
from schemas import Tournament
from models import Tournament as TournamentModel, AthleteCompetition
import crud
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from core.utils import commit_to_bd


def get_diploma_description(competition_name: str, place: int, tournament: Tournament):
    description = f"Has participated in the {competition_name} and has attained the qualification of {'1st' if place == 1 else '2nd' if place == 2 else '3rd'} place in the competition of <b>{tournament.category.name.upper()}</b> in the category of <b>"
    has_age = True
    if tournament.age_min is not None:
        if tournament.age_max is not None:
            description += f"{tournament.age_min}/{tournament.age_max} years old"
        else:
            description += f"+{tournament.age_min} years old"
    else:
        if tournament.age_max is not None:
            description += f"-{tournament.age_max} years old"
        else:
            has_age = False

    has_weight = True
    if tournament.weight_min is not None:
        if tournament.weight_max is not None:
            description += f"{', ' if has_age else ''}{tournament.weight_min}/{tournament.weight_max}kg. "
        else:
            description += f"{', ' if has_age else ''}+{tournament.weight_min}kg. "
    else:
        if tournament.weight_max is not None:
            description += f"{', ' if has_age else ''}-{tournament.weight_max}kg. "
        else:
            has_weight = False

    has_belt = True
    if tournament.belt_min_id is not None:
        if tournament.belt_max_id is not None:
            description += f"{', ' if has_age and not has_weight else ''}{tournament.belt_min.name.replace('-', ' ')} and {tournament.belt_max.name.replace('-', ' ').title()}"
        else:
            description += f"{', ' if has_age and not has_weight else ''}+{tournament.belt_min.name.replace('-', ' ').title()}"
    else:
        if tournament.belt_max_id is not None:
            description += f"{', ' if has_age and not has_weight else ''}-{tournament.belt_max.name.replace('-', ' ').title()}"
        else:
            has_belt = False

    if has_age and not has_weight and not has_belt:
        description += ", "
    description += (
        "open"
        if tournament.is_male is None
        else "male"
        if tournament.is_male
        else "female"
    )
    description += "</b>"
    return description


def create_diploma_page(
    canvas: Canvas,
    athlete_name: str,
    description: str,
    image: str,
    nameX: int,
    nameY: int,
    descriptionX: int,
    descriptionY: int,
):
    # Draw Image
    page_width, page_height = landscape(A4)
    canvas.drawImage(image, 0, 0, page_width + 1, page_height, mask="auto")

    # Write Name
    canvas.setFont("Helvetica-Bold", 24)
    canvas.drawCentredString(nameX, nameY, athlete_name)

    # Write Description
    style = getSampleStyleSheet()["Normal"]
    style.setFont = "Helvetica"
    style.textColor = colors.black
    style.fontSize = 16
    style.leading = 18
    style.alignment = TA_JUSTIFY

    p_test = Paragraph(description, style)
    text_height = p_test.wrap(310, 500)[1] - style.spaceBefore - style.spaceAfter
    n_lines = int(text_height / 18)
    if n_lines < 6:
        description += "<br/>" + "".join(["<br/>" for i in range(0, 6 - n_lines)])

    width = 310
    height = 500
    p = Paragraph(description, style)

    # create a canvas and draw the Paragraph object on it
    p.wrapOn(canvas, width, height)
    p.drawOn(canvas, descriptionX, descriptionY)
    canvas.showPage()


def create_matches_for_tournament(db: Session, tournament: Tournament):
    for match in tournament.matches:
        crud.match.delete(db=db, id=match.id)

    crud.tournament.add_podium(
        db=db,
        db_obj=tournament,
        first=None,
        second=None,
        third=None,
        podium_notes=None,
    )

    if len(tournament.inscriptions) == 0:
        return

    is_tournament = tournament.category.category_type.name == "Tournament"
    shuffle(tournament.inscriptions)
    inscriptions_ids = []
    for inscription in tournament.inscriptions:
        if inscription.accepted and inscription.confirmed:
            inscriptions_ids.append(inscription.athlete_competition_id)
    if len(inscriptions_ids) == 0:
        return
    ids_to_create = []
    extras = []

    if not is_tournament:
        crud.match.create_multiple(
            db=db,
            obj_in=inscriptions_ids,
            tournament_id=tournament.id,
            extras=extras,
            is_tournament=is_tournament,
        )
        return

    if len(inscriptions_ids) == 1:
        inscriptions_ids.append(None)
        ids_to_create = inscriptions_ids
    elif len(inscriptions_ids) == 2:
        ids_to_create = inscriptions_ids
    elif len(inscriptions_ids) == 3:
        ids_to_create = [
            inscriptions_ids[0],
            inscriptions_ids[1],
            inscriptions_ids[0],
            inscriptions_ids[2],
            inscriptions_ids[1],
            inscriptions_ids[2],
        ]
    elif len(inscriptions_ids) == 4:
        extras.append(None)
        extras.append(None)
        ids_to_create = inscriptions_ids
    elif (len(inscriptions_ids)) < 9:
        extras.append(None)
        extras.append(None)
        extras.append(None)
        extras.append(None)
        i = 0
        for j in range(8):
            if j % 2 == 0:
                try:
                    ids_to_create.append(inscriptions_ids[i])
                except IndexError:
                    ids_to_create.append(None)
                i = i + 1
            else:
                ids_to_create.append(None)
        for j in range(8):
            if j % 4 == 1:
                try:
                    ids_to_create[j] = inscriptions_ids[i]
                except IndexError:
                    pass
                i = i + 1
        for j in range(8):
            if j % 4 == 3:
                try:
                    ids_to_create[j] = inscriptions_ids[i]
                except IndexError:
                    pass
                i = i + 1
    elif (len(inscriptions_ids)) < 17:
        extras.append(None)
        for i in range(7):
            extras.append(None)
        i = 0
        for j in range(16):
            if j % 2 == 0:
                try:
                    ids_to_create.append(inscriptions_ids[i])
                except IndexError:
                    ids_to_create.append(None)
                i = i + 1
            else:
                ids_to_create.append(None)
        for j in range(16):
            if j % 4 == 1:
                try:
                    ids_to_create[j] = inscriptions_ids[i]
                except IndexError:
                    pass
                i = i + 1
        for j in range(16):
            if j % 4 == 3:
                try:
                    ids_to_create[j] = inscriptions_ids[i]
                except IndexError:
                    pass
                i = i + 1
    elif (len(inscriptions_ids)) < 32:
        extras.append(None)
        for i in range(15):
            extras.append(None)
        i = 0
        for j in range(32):
            if j % 2 == 0:
                try:
                    ids_to_create.append(inscriptions_ids[i])
                except IndexError:
                    ids_to_create.append(None)
                i = i + 1
            else:
                ids_to_create.append(None)
        for j in range(32):
            if j % 4 == 1:
                try:
                    ids_to_create[j] = inscriptions_ids[i]
                except IndexError:
                    pass
                i = i + 1
        for j in range(32):
            if j % 4 == 3:
                try:
                    ids_to_create[j] = inscriptions_ids[i]
                except IndexError:
                    pass
                i = i + 1

    crud.match.create_multiple(
        db=db, obj_in=ids_to_create, tournament_id=tournament.id, extras=extras
    )


def resolve_matches_of_tournament(
    db: Session,
    tournament: Tournament,
    athlete_bye_id: UUID4 | None,
    delete_current_podium: bool = False,
):
    if delete_current_podium:
        crud.tournament.add_podium(
            db=db,
            db_obj=tournament,
            first=None,
            second=None,
            third=None,
            podium_notes=None,
        )

    matches_len = len(tournament.matches)
    if matches_len == 1:
        if tournament.category.category_type.name != "Tournament":
            crud.tournament.add_podium(
                db=db,
                db_obj=tournament,
                first=tournament.matches[0].athlete_red_id,
                second=None,
                third=None,
                podium_notes=None,
            )
        else:
            if tournament.matches[0].athlete_blue_id is None:
                crud.tournament.add_podium(
                    db=db,
                    db_obj=tournament,
                    first=tournament.matches[0].athlete_red_id,
                    second=None,
                    third=None,
                    podium_notes=None,
                )
        return
    if tournament.category.category_type.name != "Tournament":
        return
    if matches_len == 1:
        if (
            tournament.matches[0].athlete_blue_id is None
            or tournament.matches[0].athlete_red_id is None
        ):
            if tournament.matches[0].athlete_red_id is not None:
                crud.match.add_winner(
                    db=db,
                    db_obj=tournament.matches[0],
                    winner_id=tournament.matches[0].athlete_red_id,
                )
                crud.tournament.add_podium(
                    db=db,
                    db_obj=tournament,
                    first=tournament.matches[0].athlete_red_id,
                    second=None,
                    third=None,
                    podium_notes=None,
                )
            if tournament.matches[0].athlete_blue_id is not None:
                crud.match.add_winner(
                    db=db,
                    db_obj=tournament.matches[0],
                    winner_id=tournament.matches[0].athlete_blue_id,
                )
                crud.tournament.add_podium(
                    db=db,
                    db_obj=tournament,
                    first=tournament.matches[0].athlete_blue_id,
                    second=None,
                    third=None,
                    podium_notes=None,
                )

    if matches_len == 4:
        for match in tournament.matches:
            if match.number == 1 and (
                match.athlete_blue_id == athlete_bye_id
                or match.athlete_red_id == athlete_bye_id
            ):
                for second_match in tournament.matches:
                    if second_match.number == 3:
                        winner_id = (
                            match.athlete_red_id
                            if match.athlete_blue_id == athlete_bye_id
                            else match.athlete_blue_id
                        )
                        crud.match.add_winner(db=db, db_obj=match, winner_id=winner_id)
                        crud.tournament.add_podium(
                            db=db,
                            db_obj=tournament,
                            first=winner_id,
                            second=None,
                            third=None,
                            podium_notes=None,
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=winner_id,
                            is_red=True,
                        )

            if match.number == 2 and (
                match.athlete_blue_id == athlete_bye_id
                or match.athlete_red_id == athlete_bye_id
            ):
                for second_match in tournament.matches:
                    if second_match.number == 3:
                        winner_id = (
                            match.athlete_red_id
                            if match.athlete_blue_id == athlete_bye_id
                            else match.athlete_blue_id
                        )
                        crud.match.add_winner(db=db, db_obj=match, winner_id=winner_id)
                        crud.tournament.add_podium(
                            db=db,
                            db_obj=tournament,
                            first=winner_id,
                            second=None,
                            third=None,
                            podium_notes=None,
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=winner_id,
                            is_red=True,
                        )

    if matches_len == 8:
        for match in tournament.matches:
            if match.number > 4:
                continue
            for second_match in tournament.matches:
                if second_match.number == 5 and (
                    match.number == 1 or match.number == 2
                ):
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 1),
                        )
                        break
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 1),
                        )
                        break
                if second_match.number == 6 and (
                    match.number == 3 or match.number == 4
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 3),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 3),
                        )
                        break
    if matches_len == 16:
        for match in tournament.matches:
            if match.number > 8:
                continue
            for second_match in tournament.matches:
                if second_match.number == 9 and (
                    match.number == 1 or match.number == 2
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 1),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 1),
                        )
                        break
                if second_match.number == 10 and (
                    match.number == 3 or match.number == 4
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 3),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 3),
                        )
                        break
                if second_match.number == 11 and (
                    match.number == 5 or match.number == 6
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 5),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 5),
                        )
                        break
                if second_match.number == 12 and (
                    match.number == 7 or match.number == 8
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 7),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 7),
                        )
                        break
    if matches_len == 32:
        for match in tournament.matches:
            if match.number > 16:
                continue
            for second_match in tournament.matches:
                if second_match.number == 17 and (
                    match.number == 1 or match.number == 2
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 1),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 1),
                        )
                        break
                if second_match.number == 18 and (
                    match.number == 3 or match.number == 4
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 3),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 3),
                        )
                        break
                if second_match.number == 19 and (
                    match.number == 5 or match.number == 6
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 5),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 5),
                        )
                        break
                if second_match.number == 20 and (
                    match.number == 7 or match.number == 8
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 7),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 7),
                        )
                        break
                if second_match.number == 21 and (
                    match.number == 9 or match.number == 10
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 9),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 9),
                        )
                        break
                if second_match.number == 22 and (
                    match.number == 11 or match.number == 12
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 11),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 11),
                        )
                        break
                if second_match.number == 23 and (
                    match.number == 13 or match.number == 14
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 13),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 13),
                        )
                        break
                if second_match.number == 24 and (
                    match.number == 15 or match.number == 16
                ):
                    if match.athlete_red_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_blue_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_blue_id,
                            is_red=(match.number == 15),
                        )
                        break
                    if match.athlete_blue_id is None:
                        crud.match.add_winner(
                            db=db, db_obj=match, winner_id=match.athlete_red_id
                        )
                        crud.match.add_athlete(
                            db=db,
                            db_obj=second_match,
                            athlete_id=match.athlete_red_id,
                            is_red=(match.number == 15),
                        )
                        break


def number_matches_area(
    db: Session,
    tournaments_array: List[Tournament] | List[TournamentModel],
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
    # Remove all numbers from the matches
    for tournaments_by_cat in tournament_area_by_cat:
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
        # Number semi-finals only
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
                            # TODO Remove this if depois de numerar a Open Cup
                            if (
                                match.athlete_blue_id is not None
                                or match.athlete_red_id is not None
                            ):
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

        # Gets how many tournaments exists with 3 matches
        combats_with_three_matches = 0
        for tournament in tournament_area_by_cat[tournaments_by_cat]:
            if len(tournament.matches) == 3:
                combats_with_three_matches += 1

        # If only exists 1 tournament with 3 matches, number it and save
        # the not used numbers
        if combats_with_three_matches == 1:
            tournaments_len = len(tournament_area_by_cat[tournaments_by_cat])
            tournaments_matches = 0
            if tournaments_len <= 2:
                for tournament in tournament_area_by_cat[tournaments_by_cat]:
                    tournaments_matches += len(tournament.matches)
            for tournament in tournament_area_by_cat[tournaments_by_cat]:
                match_number = 1
                if len(tournament.matches) == 3:
                    while 4 != match_number:
                        for match in tournament.matches:
                            if match.winner_id is not None:
                                continue
                            if match.number == match_number:
                                match.number_by_area = area_number
                                db.add(match)
                                area_number += 1
                                if match_number == 2 and tournaments_matches == 4:
                                    continue
                                if match_number != 3 and tournaments_matches >= 5:
                                    quantity_missing.append(area_number)
                                    area_number += 1
                                break
                        match_number += 1
        # If exists more than 1 tournament with 3 matches number them all at
        # the same time
        elif combats_with_three_matches > 1:
            match_number = 1
            while 4 != match_number:
                for tournament in tournament_area_by_cat[tournaments_by_cat]:
                    if len(tournament.matches) == 3:
                        for match in tournament.matches:
                            if match.winner_id is not None:
                                continue
                            if match.number == match_number:
                                match.number_by_area = area_number
                                db.add(match)
                                area_number += 1
                                break
                match_number += 1

        # Number final and third place qualification only
        for tournament in tournament_area_by_cat[tournaments_by_cat]:
            matches_len = len(tournament.matches)
            if matches_len == 3 or matches_len == 1:
                continue
            if matches_len >= 2 and matches_len != 3:
                match_number = 2
                limit_number = 0
                if matches_len == 32:
                    match_number += 16
                    limit_number += 16
                if matches_len >= 16:
                    match_number += 8
                    limit_number += 8
                if matches_len >= 8:
                    match_number += 4
                    limit_number += 4
                if matches_len >= 4:
                    match_number += 2
                    limit_number += 2
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

            # Number matches, first number the third place qualification and then the final
            while limit_number != match_number:
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
                match_number -= 1
        # Number tournaments with only 1 match
        for tournament in tournament_area_by_cat[tournaments_by_cat]:
            if len(tournament.matches) == 1:
                match = tournament.matches[0]
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
    commit_to_bd(session_db=db)


def get_athlete_name_from_competition(athelte_competition: AthleteCompetition):
    if (
        athelte_competition is None
        or not athelte_competition.athletes_group
        or len(athelte_competition.athletes_group) == 0
    ):
        return None

    name = ""
    for group in athelte_competition.athletes_group:
        name_aux = group.athlete.name.strip().split(" ")
        if len(name_aux) == 1:
            name += f"{name_aux[0]}, "
        else:
            name += f"{name_aux[0]} {name_aux[-1]}, "

    return name[:-2]
