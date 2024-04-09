import os
from pydantic import UUID4
from typing import List, Union, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
import crud
from auth import get_active_user, get_active_user_or_none, verify_role
from constants.roles import Role
from core.tournaments_utils import (
    create_matches_for_tournament,
    resolve_matches_of_tournament,
    create_diploma_page,
    get_diploma_description,
)
from schemas import (
    Tournament,
    TournamentCreate,
    TournamentUpdate,
    User,
    Category,
    Competition,
    TournamentPage,
    TournamentName,
    TournamentNoInscriptions,
    Podium,
    RefereesUpdate,
    PageQueries,
    PagedResponse,
)
from core.get_podium import (
    get_podium_one,
    get_podium_three,
    get_podium_four_or_more,
    get_podium_forms,
)

from sql_app import Session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from starlette.responses import FileResponse
from core.tournaments_utils import get_athlete_name_from_competition
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY

tournament_router = APIRouter(prefix="", tags=["Tournament"])


@tournament_router.get(
    "/tournaments/{tournament_id}/get-diplomas",
    name="Gets Diploma of tournament",
)
async def get_diplomas_of_tournament(
    tournament_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.PODIUM["name"]])

    tournament_db = crud.tournament.get(db=db, id=tournament_id)
    # Creating PDF
    fileName = "diplomas.pdf"
    pdf = canvas.Canvas(fileName, pagesize=landscape(A4))
    names_first = []
    names_second = []
    names_third = []
    if tournament_db.category.team_category:
        names_first = get_athlete_name_from_competition(
            tournament_db.first_place
        ).split(", ")
        names_second = get_athlete_name_from_competition(
            tournament_db.second_place
        ).split(", ")
        names_third = get_athlete_name_from_competition(
            tournament_db.third_place
        ).split(", ")
    else:
        names_first = [get_athlete_name_from_competition(tournament_db.first_place)]
        names_second = [get_athlete_name_from_competition(tournament_db.second_place)]
        names_third = [get_athlete_name_from_competition(tournament_db.third_place)]
    for place in [1, 2, 3]:
        for name in (
            names_first if place == 1 else names_second if place == 2 else names_third
        ):
            if name is None or name == "":
                continue

            if tournament_db.competition_id == UUID4(
                "e6d55717-b2da-4e27-bbeb-e299bdb69a60"
            ):
                description = get_diploma_description(
                    competition_name="2nd World Adapted Kempo Championship 2023",
                    place=place,
                    tournament=tournament_db,
                )
                script_dir = os.path.dirname(__file__)
                image = os.path.join(script_dir, f"../diplomas/adaptado{place}.jpg")

                create_diploma_page(
                    canvas=pdf,
                    athlete_name=name,
                    description=description,
                    image=image,
                    nameX=230,
                    nameY=310,
                    descriptionX=75,
                    descriptionY=145,
                )
            else:
                description = get_diploma_description(
                    competition_name="1st International Kempo Open Cup 2023",
                    place=place,
                    tournament=tournament_db,
                )
                script_dir = os.path.dirname(__file__)
                image = os.path.join(script_dir, f"../diplomas/diploma{place}.jpg")

                create_diploma_page(
                    canvas=pdf,
                    athlete_name=name,
                    description=description,
                    image=image,
                    nameX=627,
                    nameY=305,
                    descriptionX=470,
                    descriptionY=145,
                )

    # Save PDF
    pdf.save()
    return FileResponse(
        fileName, media_type="application/octet-stream", filename="file_name"
    )


@tournament_router.get(
    "/tournaments/{tournament_id}/get-diploma/place/{place}/athlete/{athlete_id}",
    name="Gets Diploma of tournament",
)
async def get_diploma(
    tournament_id: str,
    place: int,
    athlete_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.PODIUM["name"]])

    tournament_db = crud.tournament.get(db=db, id=tournament_id)
    # Creating PDF
    fileName = "diploma.pdf"
    pdf = canvas.Canvas(fileName, pagesize=landscape(A4))
    names = []
    for match in tournament_db.matches:
        if match.athlete_red_id == UUID4(athlete_id):
            if tournament_db.category.team_category:
                names = get_athlete_name_from_competition(match.athlete_red).split(", ")
            else:
                names = [get_athlete_name_from_competition(match.athlete_red)]
            break
        if match.athlete_blue_id == UUID4(athlete_id):
            if tournament_db.category.team_category:
                names = get_athlete_name_from_competition(match.athlete_blue).split(
                    ", "
                )
            else:
                names = [get_athlete_name_from_competition(match.athlete_blue)]
            break

    if names is None or len(names) == 0 or place < 1 or place > 3:
        raise HTTPException(404)

    for name in names:
        if tournament_db.competition_id == UUID4(
            "e6d55717-b2da-4e27-bbeb-e299bdb69a60"
        ):
            description = get_diploma_description(
                competition_name="2nd World Adapted Kempo Championship 2023",
                place=place,
                tournament=tournament_db,
            )
            script_dir = os.path.dirname(__file__)
            image = os.path.join(script_dir, f"../diplomas/adaptado{place}.jpg")

            create_diploma_page(
                canvas=pdf,
                athlete_name=name,
                description=description,
                image=image,
                nameX=230,
                nameY=310,
                descriptionX=75,
                descriptionY=145,
            )
        else:
            description = get_diploma_description(
                competition_name="1st International Kempo Open Cup 2023",
                place=place,
                tournament=tournament_db,
            )
            script_dir = os.path.dirname(__file__)
            image = os.path.join(script_dir, f"../diplomas/diploma{place}.jpg")

            create_diploma_page(
                canvas=pdf,
                athlete_name=name,
                description=description,
                image=image,
                nameX=627,
                nameY=305,
                descriptionX=470,
                descriptionY=145,
            )

    # Save PDF
    pdf.save()
    return FileResponse(
        fileName, media_type="application/octet-stream", filename="file_name"
    )


@tournament_router.get(
    "/tournaments/defaults/categories/{category_id}",
    response_model=List[Tournament],
    name="Returns Defaults of category",
)
async def get_default_of_category(
    category_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns Competition by ID
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    tournaments = crud.tournament.get_defaults_of_category(
        db=db, category_id=category_id
    )

    return tournaments


@tournament_router.get(
    "/tournaments/competitions/{competition_id}/categories/{category_id}",
    response_model=List[TournamentName],
    name="Returns tournaments of competition by ID",
)
async def get_tournaments_by_category(
    competition_id: str,
    category_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns Tournaments of Competition by ID
    """
    verify_role(current_user, [Role.ADMIN["name"]])
    tournaments_db: List[Tournament] = crud.tournament.get_by_category(
        db=db, competition_id=competition_id, category_id=category_id
    )
    return tournaments_db


@tournament_router.get(
    "/tournaments",
    response_model=PagedResponse[Tournament],
    name="Returns competition by ID with filters and pagination",
)
async def get_by_paginated(
    competition_id: str | None = Query(
        default=None, description="Tournaments must be of the indicated competition"
    ),
    category_id: UUID4 | None = Query(
        default=None, description="Tournaments must be of the indicated category"
    ),
    is_male: bool | None = Query(
        default=None,
        description="Tournaments must be masculine only if true, feminine only if false",
    ),
    age: int | None = Query(
        default=None, description="A possible age of the atlhetes in the tournament"
    ),
    area: int | None = Query(
        default=None,
        description="Area of the tournament, -1 for tournaments without area",
    ),
    day: int | None = Query(
        default=None,
        description="Day of the competition that the tournament will take place",
    ),
    time: str | None = Query(
        default=None,
        description="Time of the day that the tournament will take place",
        pattern="^(M|A)$",
    ),
    athlete: str | None = Query(
        default=None, description="Name of an athlete that must be in the tournament"
    ),
    team: str | None = Query(
        default=None,
        description="Abbreviation of a team that must be in the tournament",
    ),
    team_id: UUID4 | None = Query(
        default=None,
        description="ID of a team that must be in the tournament",
    ),
    show_zero: bool = Query(
        default=False, description="Show tournaments with 0 matches"
    ),
    pagination: PageQueries = Depends(),
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Returns Competition by ID with Filters and Pagination
    """
    is_admin = False
    try:
        verify_role(current_user, [Role.ADMIN["name"]])
        is_admin = True
    except:
        is_admin = False
    results, n_results = crud.tournament.get_paginated(
        db=db,
        is_admin=is_admin,
        competition_id=competition_id,
        category_id=category_id,
        is_male=is_male,
        age=age,
        area=area,
        day=day,
        time=time,
        athlete=athlete,
        team=team,
        team_id=team_id,
        show_zero=show_zero,
        limit=pagination.limit,
        skip=pagination.skip,
    )

    return PagedResponse(n_results=n_results, results=results)


@tournament_router.get(
    "/tournaments/competitions/{competition_id}/print-podium",
    response_model=List[Tournament],
    name="Returns Tournaments To Print",
)
async def get_podiums_to_print(
    competition_id: str,
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Returns Tournaments To Print
    """
    verify_role(current_user, [Role.PODIUM["name"]])
    return crud.tournament.get_podiums(db=db, competition_id=competition_id)


@tournament_router.get(
    "/tournaments/{tournament_id}/print-podium",
    response_model=Tournament,
    name="Returns Tournaments To Print",
)
async def get_podium_to_print(
    tournament_id: str,
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Returns Tournaments To Print
    """
    verify_role(current_user, [Role.PODIUM["name"]])
    return crud.tournament.get_podium(db=db, tournament_id=tournament_id)


@tournament_router.get(
    "/competitions/{competition_id}/tournaments/{tournament_id}",
    response_model=Union[Tournament, None],
    name="Returns tournament by ID",
)
async def get_by_id_with_competition(
    competition_id, tournament_id, db: Session = Depends()
):
    """
    Returns Competition by ID
    """
    return crud.tournament.get(db=db, id=tournament_id)


@tournament_router.get(
    "/tournaments/table/{tournament_id}",
    response_model=TournamentNoInscriptions,
    name="Returns tournament by ID without Inscriptions",
)
async def get_by_id_with_inscriptions(tournament_id, db: Session = Depends()):
    """
    Returns Competition by ID without Inscriptions
    """
    return crud.tournament.get(db=db, id=tournament_id)


@tournament_router.get(
    "/tournaments/{tournament_id}",
    response_model=Tournament,
    name="Returns tournament by ID",
)
async def get_by_id(tournament_id, db: Session = Depends()):
    """
    Returns Tournament by ID
    """
    tourn = crud.tournament.get(db=db, id=tournament_id)
    if tourn is None:
        raise HTTPException(404)
    return tourn


@tournament_router.post(
    "/tournaments/{tournament_id}/recreate",
    name="Recreate and resolves matches for a single tournament",
)
async def recreate_matches(
    tournament_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.ADMIN["name"]])

    tournament: Tournament = crud.tournament.get(db=db, id=tournament_id)

    if tournament is None:
        raise HTTPException(404)

    create_matches_for_tournament(db=db, tournament=tournament)
    athlete_bye = crud.athlete_competition.get_bye(
        db=db, competition_id=tournament.competition_id
    )
    athlete_bye_id = -1
    if athlete_bye is not None:
        athlete_bye_id = athlete_bye.id
    tournament: Tournament = crud.tournament.get(db=db, id=tournament_id)
    resolve_matches_of_tournament(
        db=db, tournament=tournament, athlete_bye_id=athlete_bye_id
    )


@tournament_router.post(
    "/tournaments/resolve-podium/{tournament_id}",
    name="Calculate podium for tournament",
)
async def resolve_podium_tournament(
    tournament_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    verify_role(current_user, [Role.ADMIN["name"], Role.AREA["name"]])
    tournament: Tournament = crud.tournament.get(db=db, id=tournament_id)

    if tournament is None:
        raise HTTPException(404)

    len_matches = len(tournament.matches)
    if tournament.category.category_type.name == "Tournament":
        for match in tournament.matches:
            if len_matches == 1 or match.number == len_matches - 1:
                if match.winner_id is None:
                    return
                else:
                    break
    else:
        for match in tournament.matches:
            if match.winner_id is None:
                return

    podium: Podium = None
    if tournament.category.category_type.name != "Tournament":
        podium = get_podium_forms(tournament)
    else:
        length = len(tournament.matches)
        if length == 1:
            podium = get_podium_one(tournament)
        elif length == 3:
            podium = get_podium_three(tournament)
        else:
            podium = get_podium_four_or_more(db=db, tournament=tournament)

    crud.tournament.update(
        db=db,
        obj_in=TournamentUpdate(
            first_place_id=podium.first,
            second_place_id=podium.second,
            third_place_id=podium.third,
        ),
        db_obj=tournament,
    )


@tournament_router.post(
    "/competitions/{competition_id}/tournaments/multi",
    name="Creates multiple Tournaments",
)
async def create_multi(
    competition_id,
    tournaments: List[TournamentCreate],
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates multiple Tournaments
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    competition_db: Competition = crud.competition.get(db=db, id=competition_id)

    if competition_db is None:
        raise HTTPException(404, "Competition not found")

    category_db: Category = crud.category.get_by_name(
        db=db, name=tournaments[0].category
    )

    if category_db is None:
        raise HTTPException(404, "Category not found")

    for tournament in competition_db.tournaments:
        if tournament.category.name == tournaments[0].category:
            crud.tournament.delete_category(
                db=db, competition_id=competition_id, category_id=tournament.category.id
            )
            break

    for tournament in tournaments:
        crud.tournament.create_multi(
            db=db,
            obj_in=tournament,
            competition_id=competition_id,
            category_id=category_db.id,
        )

    return


@tournament_router.post(
    "/competitions/{competition_id}/tournaments/multiple",
    name="Creates multiple Tournaments",
)
async def create_multiple(
    competition_id,
    tournaments_list: List[TournamentCreate],
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates multiple Tournaments
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    to_create = []
    failed = []

    for tourn in tournaments_list:
        if tourn.category is None or tourn.category.strip() == "":
            failed.append(tourn)
            continue

        to_create.append(tourn)

    return crud.tournament.create_multiple(
        db=db, obj_in=to_create, competition_id=competition_id
    )


@tournament_router.post(
    "/tournaments",
    response_model=Union[Tournament, None],
    name="Creates a new Tournament",
)
async def create(
    tournament_in: TournamentCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a new Tournament
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    error_exists = False
    error_message: Dict[str, str] = {}

    if tournament_in.competition_id is None:
        error_message["competition_id"] = "The tournament has no competition ID"
        error_exists = True

    if tournament_in.category_id is None:
        error_message["category_id"] = "The tournament has no category ID"
        error_exists = True

    competition = crud.competition.get(db=db, id=tournament_in.competition_id)

    if competition is None:
        error_message["competition_id_exists"] = "The competition ID doesn't exist"
        error_exists = True

    category = crud.category.get(db=db, id=tournament_in.category_id)

    if category is None:
        error_message["category_id_exists"] = "The category ID doesn't exist"
        error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    return crud.tournament.create(db=db, obj_in=tournament_in)


@tournament_router.put(
    "/tournaments/podium/{tournament_id}",
    response_model=Tournament,
    name="Updates the Podium of a Tournament",
)
async def update_podium(
    tournament_id,
    podium_in: Podium,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates the Podium of a Tournament
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.AREA["name"]])

    tournament_db = crud.tournament.get(db=db, id=tournament_id)

    if tournament_db is None:
        raise HTTPException(404, "Tournament Not Found")

    return crud.tournament.add_podium(
        db=db,
        db_obj=tournament_db,
        first=podium_in.first,
        second=podium_in.second,
        third=podium_in.third,
        podium_notes=podium_in.podium_notes,
    )


@tournament_router.put(
    "/tournaments/{tournament_id}",
    response_model=Tournament,
    name="Updates a Tournament",
)
async def update(
    tournament_id,
    tournament_in: TournamentUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates a Tournament
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    tournament_db = crud.tournament.get(db=db, id=tournament_id)

    if tournament_db is None:
        raise HTTPException(404, "Tournament Not Found")

    return crud.tournament.update(db=db, obj_in=tournament_in, db_obj=tournament_db)


@tournament_router.put(
    "/tournaments/{tournament_id}/referees",
    response_model=Tournament,
    name="Updates a Tournament",
)
async def updates_referees(
    tournament_id,
    referees_in: RefereesUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates a Tournament
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.AREA["name"]])

    tournament_db = crud.tournament.get(db=db, id=tournament_id)

    if tournament_db is None:
        raise HTTPException(404, "Tournament Not Found")

    return crud.tournament.update(db=db, obj_in=referees_in, db_obj=tournament_db)


@tournament_router.put(
    "/tournaments/{tournament_id}/printed",
    name="Updates Printed Status to True",
)
async def update_printed(
    tournament_id: str,
    notes: Podium,
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Updates Printed Status to True
    """
    verify_role(current_user, [Role.PODIUM["name"]])
    tournament_db = crud.tournament.get(db=db, id=tournament_id)
    if tournament_db is None:
        raise HTTPException(404)
    return crud.tournament.update_printed(
        db=db, db_obj=tournament_db, podium_notes=notes.podium_notes
    )


@tournament_router.delete(
    "/tournaments/{tournament_id}",
    response_model=Union[Tournament, None],
    name="Deletes Tournament",
)
async def delete(
    tournament_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Deletes a Tournament
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.tournament.delete(db=db, id=tournament_id)
