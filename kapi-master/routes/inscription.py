from typing import Annotated, List, Union, Optional
import uuid
from fastapi import (
    APIRouter,
    Body,
    Depends,
    Form,
    HTTPException,
    BackgroundTasks,
    Query,
    UploadFile,
    status,
)
from pydantic import UUID4, TypeAdapter, ValidationError
import crud
from auth import get_active_user, verify_role
from constants.roles import Role
from core.utils import commit_to_bd
from core.file_creation import create_payment_guide
from core.file_validator import MAX_PDF_SIZE, FileTypes, FileUploadValidator
from core.file_storage import FileStorageDirectories, FileStorageService
from schemas import (
    Inscription,
    InscriptionUpdate,
    User,
    Tournament,
    AthleteCompetition,
    Team,
    InscriptionsTeams,
    InscriptionsTournament,
    PageQueries,
    PagedResponse,
    InscriptionPaymentIn,
)
from core.mail import send_inscriptions_information
from datetime import datetime
from sql_app import Session

TA_INSCRIPTION_PAYMENT_IN = TypeAdapter(list[InscriptionPaymentIn])

inscription_router = APIRouter(
    prefix="/inscriptions", tags=["Tournament's Inscriptions"]
)


@inscription_router.get(
    "/get-payment-guide",
    name="Returns payment guide of insurances",
)
async def get_payment_guide_by_payment_comprovative(
    team_id: UUID4 | None = Query(
        default=None,
        description="Team ID",
    ),
    payment_comprovative: str = Query(
        default=None,
        description="URL of the payment comprovative",
    ),
    db: Session = Depends(),
):
    """
    Returns Insurance by ID
    """

    team_abbreviation = "NOTEAM"
    if team_id is not None:
        team = crud.team.get(db=db, id=team_id)
        team_abbreviation = team.abbreviation

    table_data: list[list[int | str]] = [
        ["Quantidade", "Categoria", "Preço unitário", "Preço total"]
    ]
    inscriptions, n_results = crud.inscription.get_new(
        db=db, payment_comprovative_url=payment_comprovative, limit=-1
    )
    categories_price = {}
    for inscription in inscriptions:
        if inscription.tournament.category.id not in categories_price:
            categories_price[inscription.tournament.category.id] = {
                "name": inscription.tournament.category.name,
                "price": (
                    inscription.tournament.price
                    if inscription.tournament.price is not None
                    else 0
                ),
                "quantity": 0,
            }
        categories_price[inscription.tournament.category.id]["quantity"] = (
            categories_price[inscription.tournament.category.id]["quantity"] + 1
        )

    total_price = 0
    for category in categories_price:
        table_data.append(
            [
                categories_price[category]["quantity"],
                categories_price[category]["name"],
                str(categories_price[category]["price"]) + "€",
                str(
                    categories_price[category]["quantity"]
                    * categories_price[category]["price"]
                )
                + "€",
            ]
        )
        total_price = (
            total_price
            + categories_price[category]["quantity"]
            * categories_price[category]["price"]
        )

    table_data.append(["", "", "", ""])
    table_data.append(["", "", "Total", str(total_price) + "€"])

    return create_payment_guide(
        title=f"Guia de pagamento - {team_abbreviation}", table_data=table_data
    )


@inscription_router.get(
    "",
    response_model=PagedResponse[Inscription],
    name="Returns all inscriptions paginated",
)
async def get_new(
    competition_id: UUID4 | None = Query(
        default=None,
        description="ID of the competition",
    ),
    team_id: UUID4 | None = Query(
        default=None,
        description="ID of the athlete's team",
    ),
    inscription_confirmed: bool | None = Query(
        default=None,
        description="If the inscription was already confirmed",
    ),
    inscription_accepted: bool | None = Query(
        default=None,
        description="If the inscription was already accepted",
    ),
    pagination: PageQueries = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Inscriptions Paginated
    """
    if not team_id:
        verify_role(current_user, [Role.ADMIN["name"]])
    else:
        team: Team = crud.team.get(db=db, id=team_id)
        if str(team.coach_id) == str(current_user.id):
            verify_role(current_user, [Role.COACH["name"], Role.ADMIN["name"]])
        else:
            verify_role(current_user, [Role.ADMIN["name"]])

    results, n_results = crud.inscription.get_new(
        db=db,
        competition_id=competition_id,
        team_id=team_id,
        inscription_confirmed=inscription_confirmed,
        inscription_accepted=inscription_accepted,
        limit=pagination.limit,
        skip=pagination.skip,
    )
    return PagedResponse(n_results=n_results, results=results)


@inscription_router.get(
    "/{tournament_id}/{athlete_competition_id}",
    response_model=Inscription,
    name="Returns all inscriptions for a tournament",
)
async def get(
    tournament_id,
    athlete_competition_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Inscriptions for a tournament
    """
    verify_role(current_user, [Role.ADMIN["name"]])
    inscription = crud.inscription.get(
        db=db,
        tournament_id=tournament_id,
        athlete_competition_id=athlete_competition_id,
    )
    if inscription is None:
        raise HTTPException(404, "Inscription Not Found")
    return inscription


@inscription_router.get(
    "/tournaments/{tournament_id}",
    response_model=List[Inscription],
    name="Returns all inscriptions for a tournament",
)
async def get_by_tournament(
    tournament_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Inscriptions for a tournament
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.inscription.get_by_tournament(db=db, tournament_id=tournament_id)


@inscription_router.get(
    "/competitions/{competition_id}/stats",
    name="Returns number of athletes accepted, confirmed and not confirmed",
)
async def get_stats_inscriptions_by_competition(
    competition_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns number of athletes accepted, confirmed and not confirme
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.inscription.get_stats_by_competition(
        db=db, competition_id=competition_id
    )


@inscription_router.get(
    "/competitions/{competition_id}/teams/confirmed/{confirmed}",
    response_model=List[InscriptionsTeams],
    name="Returns all teams signed up in the competition",
)
async def get_inscriptions_by_competition_group_by_teams(
    competition_id,
    confirmed: bool,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Teams Signed Up in the Competition
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    inscriptions = crud.inscription.get_by_competition_confirmed(
        db=db, competition_id=competition_id, confirmed=confirmed
    )
    teams = []
    teams_added = {}

    for inscription in inscriptions:
        if len(inscription.athlete_competition.athletes_group) == 0:
            continue
        team = inscription.athlete_competition.athletes_group[0].athlete.team
        team_id = str(team.id) if team is not None else "No Team"
        coach = crud.user.get_by_email(db=db, email="miguelangeloleal@hotmail.com")
        if team is None:
            team = Team(
                id=None,
                name="No Team",
                abbreviation="NT",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                deleted_at=None,
                coach_id=coach.id,
                coach=coach,
            )

        if team_id not in teams_added:
            teams_added[team_id] = len(teams_added)
            teams.append(
                InscriptionsTeams(team=team, inscriptions_length=0, athletes=[])
            )
        teams[teams_added[team_id]].inscriptions_length += 1
        if (
            inscription.athlete_competition_id
            not in teams[teams_added[team_id]].athletes
        ):
            teams[teams_added[team_id]].athletes.append(
                inscription.athlete_competition_id
            )

    return teams


@inscription_router.get(
    "/competitions/{competition_id}/tournaments/confirmed/{confirmed}",
    response_model=List[InscriptionsTournament],
    name="Returns all inscriptions group by tournaments in the competition",
)
async def get_inscriptions_by_competition_group_by_tournaments(
    competition_id,
    confirmed: bool,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Inscriptions group by Tournaments in the Competition
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    inscriptions = crud.inscription.get_by_competition_confirmed(
        db=db, competition_id=competition_id, confirmed=confirmed
    )
    tournaments = []
    tournaments_added = {}

    for inscription in inscriptions:
        tournament = inscription.tournament
        if str(tournament.id) not in tournaments_added:
            tournaments_added[str(tournament.id)] = len(tournaments_added)
            tournaments.append(
                InscriptionsTournament(tournament=tournament, inscriptions_length=0)
            )
        tournaments[tournaments_added[str(tournament.id)]].inscriptions_length += 1

    return tournaments


@inscription_router.get(
    "/competitions/{competition_id}/teams/{team_id}/accepted/{accepted}",
    response_model=List[Inscription],
    name="Returns all inscriptions for a competition for a team",
)
async def get_by_competition_by_team_accepted(
    competition_id,
    team_id,
    accepted: bool,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Inscriptions for a competition for a team
    """
    verify_role(current_user, [Role.COACH["name"], Role.ADMIN["name"]])

    team: Team = crud.team.get(db=db, id=team_id)
    if current_user.user_role.role.name == "COACH" and (
        team is None or team.coach_id != current_user.id
    ):
        raise HTTPException(401, "Insufficient Permissions")

    return crud.inscription.get_by_competition_by_team_accepted(
        db=db, competition_id=competition_id, team_id=team_id, accepted=accepted
    )


@inscription_router.get(
    "/competitions/{competition_id}/teams/{team_id}/confirmed/{confirmed}",
    response_model=List[Inscription],
    name="Returns all inscriptions for a competition for a team",
)
async def get_by_competition_by_team_confirmed(
    competition_id,
    team_id,
    confirmed: bool,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Inscriptions for a competition for a team
    """
    verify_role(current_user, [Role.COACH["name"], Role.ADMIN["name"]])

    if team_id == "null":
        verify_role(current_user, [Role.ADMIN["name"]])
        return crud.inscription.get_by_competition_by_team(
            db=db, competition_id=competition_id, confirmed=confirmed, team_id=None
        )

    team: Team = crud.team.get(db=db, id=team_id)
    if current_user.user_role.role.name == "COACH" and (
        team is None or team.coach_id != current_user.id
    ):
        raise HTTPException(401, "Insufficient Permissions")

    return crud.inscription.get_by_competition_by_team(
        db=db, competition_id=competition_id, confirmed=confirmed, team_id=team_id
    )


@inscription_router.get(
    "/tournaments/{tournament_id}/confirmed/{confirmed}",
    response_model=List[Inscription],
    name="Returns all inscriptions for a competition for a tournament",
)
async def get_by_competition_by_tournament_confirmed(
    tournament_id,
    confirmed: bool,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Inscriptions for a competition for a tournament
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    tournament: Tournament = crud.tournament.get(db=db, id=tournament_id)
    if tournament is None:
        raise HTTPException(404, "Tournament Not Found")

    return crud.inscription.get_by_tournament_confirmed(
        db=db, tournament_id=tournament_id, confirmed=confirmed
    )


@inscription_router.get(
    "/competitions/{competition_id}",
    response_model=List[Inscription],
    name="Returns all inscriptions for a competition",
)
async def get_by_competition(
    competition_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Inscriptions for a competition
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.inscription.get_by_competition(db=db, competition_id=competition_id)


@inscription_router.get(
    "/competitions/{competition_id}/confirmed/{confirmed}/number",
    name="Returns the number of inscriptions for a competition that are or aren't confirmed",
)
async def get_by_competition_confirmed_number(
    competition_id,
    confirmed: bool,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns the Number of Inscriptions for a competition that are or aren't confirmed
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.inscription.get_by_competition_confirmed_count(
        db=db, competition_id=competition_id, confirmed=confirmed
    )


@inscription_router.get(
    "/competitions/{competition_id}/confirmed/{confirmed}",
    response_model=List[Inscription],
    name="Returns all inscriptions for a competition that are or aren't confirmed",
)
async def get_by_competition_confirmed(
    competition_id,
    confirmed: bool,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns All Inscriptions for a competition that are or aren't confirmed
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.inscription.get_by_competition_confirmed(
        db=db, competition_id=competition_id, confirmed=confirmed
    )


@inscription_router.post(
    "/tournaments/{tournament_id}/{athlete_competition_id}",
    response_model=Union[Inscription, None],
    name="Signs up an athlete or team for the tournament",
)
async def create(
    tournament_id,
    athlete_competition_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Signs up an athlete or team for the tournament
    """

    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    tournament: Optional[Tournament] = crud.tournament.get(db=db, id=tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament Not Found")

    athlete_competition: Optional[AthleteCompetition] = crud.athlete_competition.get(
        db=db, id=athlete_competition_id
    )
    if athlete_competition is None:
        raise HTTPException(status_code=404, detail="Athlete Not Found")

    if (
        current_user.user_role.role.name == "COACH"
        and athlete_competition.athletes_group[0].athlete.team.coach_id
        != current_user.id
    ):
        raise HTTPException(401, "Insufficient Permissions")

    return crud.inscription.create(
        db=db,
        obj_in=Inscription(
            tournament_id=tournament_id, athlete_competition_id=athlete_competition_id
        ),
    )


@inscription_router.post(
    "/get-payment-guide",
    name="Returns payment guide of insurances",
)
async def get_payment_guide(
    team_id: UUID4 | None,
    inscriptions: list[InscriptionPaymentIn],
    db: Session = Depends(),
):
    """
    Returns Insurance by ID
    """

    team_abbreviation = "NOTEAM"
    if team_id is not None:
        team = crud.team.get(db=db, id=team_id)
        team_abbreviation = team.abbreviation

    table_data: list[list[int | str]] = [
        ["Quantidade", "Categoria", "Preço unitário", "Preço total"]
    ]
    categories_price = {}
    tournaments_cache = {}
    for inscription in inscriptions:
        if inscription.tournament_id not in tournaments_cache:
            tournament = crud.tournament.get(db=db, id=inscription.tournament_id)
            tournaments_cache[inscription.tournament_id] = tournament.category.id

        if tournaments_cache[inscription.tournament_id] not in categories_price:
            categories_price[tournaments_cache[inscription.tournament_id]] = {
                "name": tournament.category.name,
                "price": tournament.price if tournament.price is not None else 0,
                "quantity": 0,
            }
        categories_price[tournaments_cache[inscription.tournament_id]]["quantity"] = (
            categories_price[tournaments_cache[inscription.tournament_id]]["quantity"]
            + 1
        )

    total_price = 0
    for category in categories_price:
        table_data.append(
            [
                categories_price[category]["quantity"],
                categories_price[category]["name"],
                str(categories_price[category]["price"]) + "€",
                str(
                    categories_price[category]["quantity"]
                    * categories_price[category]["price"]
                )
                + "€",
            ]
        )
        total_price = (
            total_price
            + categories_price[category]["quantity"]
            * categories_price[category]["price"]
        )

    table_data.append(["", "", "", ""])
    table_data.append(["", "", "Total", str(total_price) + "€"])

    return create_payment_guide(
        title=f"Guia de pagamento - {team_abbreviation}", table_data=table_data
    )


@inscription_router.put("/confirm/list", name="Confirms multiple inscriptions at once")
async def confirms_multiple(
    inscriptions_in: List[InscriptionUpdate],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Confirms multiple inscriptions at once
    """

    verify_role(current_user, Role.COACH["name"])
    team_id = None
    competition_name = ""
    inscriptions_obj = []
    for inscription_in in inscriptions_in:
        inscription_obj: Inscription = crud.inscription.get(
            db=db,
            tournament_id=inscription_in.tournament_id,
            athlete_competition_id=inscription_in.athlete_competition_id,
        )
        if team_id is None:
            team_id = inscription_obj.athlete_competition.athletes_group[
                0
            ].athlete.team_id
            competition_name = inscription_obj.tournament.competition.name
        elif (
            team_id
            != inscription_obj.athlete_competition.athletes_group[0].athlete.team_id
        ):
            raise HTTPException(
                status_code=400,
                detail=[
                    {"inscription": "All inscriptions need to be of the same team"}
                ],
            )
        inscriptions_obj.append(inscription_obj)
    team: Team = crud.team.get(db=db, id=team_id)
    if team is None:
        raise HTTPException(status_code=404, detail=[{"team": "Team Not Found"}])
    for inscription_obj in inscriptions_obj:
        for inscription_in in inscriptions_in:
            if (
                inscription_in.athlete_competition_id
                == inscription_obj.athlete_competition_id
                and inscription_in.tournament_id == inscription_obj.tournament_id
            ):
                crud.inscription.update_confirmed(
                    db=db, db_obj=inscription_obj, confirmed=True
                )
                break

    background_tasks.add_task(
        send_inscriptions_information,
        competition_name=competition_name,
        team_name=team.name,
        coach_name=current_user.name,
        number_inscriptions=len(inscriptions_obj),
    )


@inscription_router.put(
    "/accept/list", name="Accepts or rejects multiple inscriptions at once"
)
async def accepts_multiple(
    inscriptions_in: list[InscriptionUpdate],
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Accepts or Rejects multiple inscriptions at once
    """

    verify_role(current_user, [Role.ADMIN["name"]])
    for inscription_in in inscriptions_in:
        inscription_obj: Inscription = crud.inscription.get(
            db=db,
            tournament_id=inscription_in.tournament_id,
            athlete_competition_id=inscription_in.athlete_competition_id,
        )
        inscription_obj.accepted = inscription_in.accepted or False
        db.add(inscription_obj)

    commit_to_bd(session_db=db)


@inscription_router.put(
    "/payment-comprovative",
    name="Uploads the payment comprovative for multiples inscriptions",
    dependencies=[
        Depends(
            FileUploadValidator(max_size_mb=MAX_PDF_SIZE, allowed_types=[FileTypes.PDF])
        )
    ],
)
async def upload_payment_comprovative(
    file: Annotated[UploadFile, Body(..., description="Medical exam file")],
    background_tasks: BackgroundTasks,
    inscriptions: str | None = Form(default=None),
    file_storage_service: FileStorageService = Depends(),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Uploads the payment comprovative for multiples inscriptions
    """
    if inscriptions is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Inscriptions are empty",
        )
    try:
        inscriptions_list = TA_INSCRIPTION_PAYMENT_IN.validate_json(inscriptions)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.json()
        )

    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    file_name = file_storage_service.get_file_name(
        directory=FileStorageDirectories.INSCRIPTIONS_PAYMENTS_COMPROVATIVES,
        obj_id=uuid.uuid4(),
        file=file,
    )
    background_tasks.add_task(file_storage_service.upload, file_name, file)

    crud.inscription.upload_payment_comprovative(
        db=db,
        inscriptions=inscriptions_list,
        file_name=file_name,
        background_tasks=background_tasks,
        file_storage_service=file_storage_service,
    )
    return


@inscription_router.put(
    "/{tournament_id}/{athlete_competition_id}",
    name="Updates an Inscription",
    response_model=Inscription,
)
async def update(
    tournament_id,
    athlete_competition_id,
    inscription_in: InscriptionUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates an Inscription
    """

    verify_role(current_user, [Role.ADMIN["name"]])

    inscription_db = crud.inscription.get(
        db=db,
        tournament_id=tournament_id,
        athlete_competition_id=athlete_competition_id,
    )
    if inscription_db is None:
        raise HTTPException(404, "Inscription Not Found")

    tournament_db = crud.tournament.get(db=db, id=inscription_in.tournament_id)
    if tournament_db is None:
        raise HTTPException(404, "Tournament Not Found")

    inscription = crud.inscription.update_all(
        db=db, db_obj=inscription_db, obj_in=inscription_in
    )
    if inscription is None:
        raise HTTPException(400, {"inscription": "Inscription Not Updated"})
    return inscription


@inscription_router.delete(
    "/tournaments/{tournament_id}/{athlete_competition_id}",
    name="Deletes an athlete or team for the tournament",
)
async def delete(
    tournament_id,
    athlete_competition_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Deletes an athlete or team for the tournament
    """

    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    athlete_competition: Optional[AthleteCompetition] = crud.athlete_competition.get(
        db=db, id=athlete_competition_id
    )
    if athlete_competition is None:
        raise HTTPException(status_code=404, detail="Athlete Not Found")

    if (
        current_user.user_role.role.name == "COACH"
        and athlete_competition.athletes_group[0].athlete.team.coach_id
        != current_user.id
    ):
        raise HTTPException(401, "Insufficient Permissions")

    crud.inscription.delete_inscription(
        db=db,
        tournament_id=tournament_id,
        athlete_competition_id=athlete_competition_id,
    )
    return
