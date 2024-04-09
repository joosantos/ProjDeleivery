import datetime
from datetime import datetime as DatetimeType
from typing import Dict, List, Optional, TypedDict, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import UUID4, BaseModel, TypeAdapter
from sqlalchemy import func, select

import crud
from auth import get_active_user, get_active_user_or_none, get_role, verify_role
from constants.roles import Role
from core.get_podium import (
    get_podium_forms,
    get_podium_four_or_more,
    get_podium_one,
    get_podium_three,
)
from core.tournaments_utils import (
    create_matches_for_tournament,
    number_matches_area,
    resolve_matches_of_tournament,
)
from core.utils import commit_to_bd
from models import (
    AthleteCompetition as AthleteCompetitionModel,
    AthleteGroup as AthleteGroupModel,
    Athlete as AthleteModel,
    Competition as CompetitionModel,
    Inscription as InscriptionModel,
    Tournament as TournamentModel,
    Category as CategoryModel,
    Match as MatchModel,
    Team as TeamModel,
)
from schemas import (
    Competition,
    CompetitionCreate,
    CompetitionDetails,
    CompetitionNoMatches,
    CompetitionUpdate,
    MatchCalls,
    PageQueries,
    Podium,
    Tournament,
    TournamentCreate,
    TournamentNoInscriptions,
    TournamentUpdate,
    User,
    CategoryName,
    TeamName,
    CompetitionInDBBase,
)
from sql_app import Session

competition_router = APIRouter(prefix="/competitions", tags=["Competition"])

TA_COMPETITION = TypeAdapter(Competition)
TA_COMPETITION_LIST = TypeAdapter(List[Competition])
TA_COMPETITION_DETAILS = TypeAdapter(CompetitionDetails)
TA_COMPETITION_DETAILS_LIST = TypeAdapter(List[CompetitionDetails])


class Ids(BaseModel):
    ids: List[UUID4] = []


@competition_router.get(
    "/inscriptions",
    name="Returns a list of all non deleted competitions that are in the period of inscriptions or all for admin",
)
async def get_inscriptions(
    db: Session = Depends(),
    current_user: User = Depends(get_active_user_or_none),
):
    """
    Returns a list of all non deleted competitions that are in the period of inscriptions
    """
    if current_user.user_role.role.name == "ADMIN":
        competitions: List[Competition] = crud.competition.get_all(db=db)
    else:
        competitions: List[Competition] = crud.competition.get_inscriptions(db=db)
    result = []
    if competitions is None:
        return []

    for competition in competitions:
        tournaments_length = 0
        matches_length = 0
        direct_winners_length = 0
        for tournament in competition.tournaments:
            tournaments_length += 1
            number_of_matches = len(tournament.matches)
            matches_length += number_of_matches
            if len(tournament.matches) > 0:
                match = tournament.matches[0]
                if number_of_matches == 1 and (
                    (match.athlete_blue_id is None and match.athlete_red_id is not None)
                    or (
                        match.athlete_blue_id is not None
                        and match.athlete_red_id is None
                    )
                ):
                    direct_winners_length += 1

        result.append(
            {
                "name": competition.name,
                "id": competition.id,
                "tournaments": tournaments_length,
                "matches": matches_length,
                "direct_winners": direct_winners_length,
                "athletes": len(competition.athletes),
                "inscriptions_end": competition.inscriptions_end,
                "competition_start": competition.competition_start,
                "competition_end": competition.competition_end,
                "calculate_age_start_year": competition.calculate_age_start_year,
            }
        )

    return result


@competition_router.get("/results", name="Returns all results of multiple competitions")
async def get_results_competitions(
    competition_ids: list[str] = Query(
        default=[], description="IDs of the competitions"
    ),
    db: Session = Depends(),
):
    """
    Returns all results of multiple competitions
    """
    if len(competition_ids) == 0:
        return None

    return crud.competition.get_results(db=db, competition_ids=competition_ids)


@competition_router.get(
    "",
    name="Returns a list of all competitions",
)
async def get_all_new(
    deleted: bool | None = Query(
        default=False, description="Return deleted competitions"
    ),
    show_public: bool | None = Query(
        default=None,
        description="Return competitions open or closed to public or all if null",
    ),
    arquived: bool | None = Query(
        default=False, description="Return arquived competitions"
    ),
    inscriptions_open: bool | None = Query(
        default=None, description="Return only competitions in period of inscriptions"
    ),
    year: int | None = Query(
        default=None, description="Return only competitions of the given year"
    ),
    competition_ended: bool | None = Query(
        default=None,
        description="Return only competitions that didn't happened or that already happened",
    ),
    pagination: PageQueries = Depends(),
    db: Session = Depends(),
    current_user: User = Depends(get_active_user_or_none),
):
    """
    Returns a list of all competitions
    """
    role = get_role(current_user)
    if role != "ADMIN":
        deleted = False
    if role is None:
        show_public = True

    return TA_COMPETITION_DETAILS_LIST.validate_python(
        crud.competition.get_all_new(
            db=db,
            deleted=deleted,
            show_public=show_public,
            arquived=arquived,
            inscriptions_open=inscriptions_open,
            competition_ended=competition_ended,
            year=year,
            limit=pagination.limit,
            skip=pagination.skip,
        )
    )


@competition_router.get(
    "/all",
    name="Returns a list of all non deleted competitions",
)
async def get_all(
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Returns a list of all non deleted competitions
    """
    is_admin = False
    is_anon = current_user is None
    if current_user is not None:
        try:
            verify_role(current_user, [Role.ADMIN["name"]])
            is_admin = True
        except:
            is_admin = False
        if not is_admin:
            try:
                verify_role(
                    current_user,
                    [Role.AREA["name"], Role.PODIUM["name"], Role.MICRO["name"]],
                )
                is_admin = True
            except:
                is_admin = False

    return crud.competition.get_all_filtered(db=db, is_admin=is_admin, is_anon=is_anon)


@competition_router.get(
    "/inscriptions/{competition_id}",
    response_model=CompetitionNoMatches,
    name="Returns competition by ID",
)
async def get_by_id_to_inscriptions(
    competition_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns Competition by ID
    """
    verify_role(current_user, [Role.COACH["name"], Role.ADMIN["name"]])
    competition: CompetitionNoMatches = crud.competition.get(db=db, id=competition_id)
    return competition


@competition_router.get(
    "/inscriptions/{competition_id}/athlete/{athlete_id}",
    response_model=Competition,
    name="Returns competition by ID",
)
async def get_by_athlete_to_inscriptions(
    competition_id: str,
    athlete_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns Competition by ID
    """
    verify_role(current_user, [Role.COACH["name"], Role.ADMIN["name"]])
    competition: Optional[Competition] = crud.competition.get(db=db, id=competition_id)
    if competition is None:
        raise HTTPException(404, "Competition Not Found")

    for tournament in competition.tournaments:
        for inscription in tournament.inscriptions:
            inscription.athlete_competition_id = None
            inscription.athlete_competition = None
    return competition


@competition_router.get("/name/{competition_id}", name="Returns competition name")
async def get_name(
    competition_id: UUID4,
    db: Session = Depends(),
):
    """
    Returns Competition name
    """
    return crud.competition.get_name(db=db, id=competition_id)


@competition_router.get(
    "/no-list/{competition_id}",
    response_model=Union[CompetitionInDBBase, None],
    name="Returns competition by ID without extra info",
)
async def get_by_id(
    competition_id: UUID4,
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Returns Competition by ID without extra info
    """
    competition: CompetitionInDBBase = crud.competition.get(db=db, id=competition_id)
    if competition.show_public:
        return competition

    if get_role(current_user) == "ADMIN":
        return competition

    raise HTTPException(404)


@competition_router.get(
    "/{competition_id}/show-by-area",
    response_model=List[MatchCalls],
    name="Returns Matches occurring in each area",
)
async def get_matches_by_area(competition_id: str, db: Session = Depends()):
    """
    Returns Matches occurring in each area
    """
    return crud.competition.get_matches_each_area(db=db, competition_id=competition_id)


@competition_router.get(
    "/{competition_id}/get-time-left/day/{day}",
    name="Returns Matches occurring in each area",
)
async def get_time_left(
    competition_id: str,
    day: int,
    db: Session = Depends(),
    current_user: User = Depends(get_active_user_or_none),
):
    """
    Returns time left for each area
    """

    verify_role(current_user, [Role.ADMIN["name"]])
    query = (
        select(
            func.min(MatchModel.number_by_area).label("min_number"),
            func.max(MatchModel.number_by_area).label("max_number"),
            TournamentModel.area.label("area"),
            TournamentModel.morning.label("morning"),
        )
        .join(TournamentModel)
        .filter(
            TournamentModel.competition_id == competition_id,
            TournamentModel.day == day,
            MatchModel.winner_id == None,
        )
        .group_by(TournamentModel.area, TournamentModel.morning)
    )

    results = db.execute(query).all()
    data = {}
    for result in results:
        if result[2] not in data:
            data[result[2]] = {}
        data[result[2]][result[3]] = {
            "min": result[0],
            "max": result[1],
        }

    return data


@competition_router.get(
    "/{competition_id}/athletes", name="Returns all athletes of competition"
)
async def get_competition_athletes(
    competition_id: str,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
    day: Optional[int] = None,
    time: Optional[bool] = None,
    gender: Optional[bool] = None,
    adapted: Optional[bool] = None,
    db: Session = Depends(),
):
    """
    Returns all athletes of competition
    """
    return crud.competition.get_athletes_competition(
        db=db,
        competition_id=competition_id,
        age_min=age_min,
        age_max=age_max,
        day=day,
        time=time,
        gender=gender,
        adapted=adapted,
    )


@competition_router.get(
    "/{competition_id}/calculate-age",
    name="Returns name and how to calculate age of the competition",
)
async def get_calculate_age(competition_id: str, db: Session = Depends()):
    """
    Returns name and how to calculate age of the competition
    """
    competition_db = crud.competition.get(db=db, id=competition_id)
    return {
        "name": competition_db.name,
        "calculate_age_start_year": competition_db.calculate_age_start_year,
    }


@competition_router.get(
    "/{competition_id}/inscriptions-started",
    name="Returns if inscriptions have started",
)
async def get_inscriptions_started(
    competition_id: str,
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Returns if inscriptions have started
    """
    today = datetime.datetime.now()
    competition: Optional[Competition] = crud.competition.get(db=db, id=competition_id)
    if competition is None:
        return None
    if competition.show_public:
        return competition.inscriptions_start < today
    if current_user == "":
        return None
    try:
        verify_role(current_user, [Role.ADMIN["name"]])
        return competition.inscriptions_start < today
    except:
        return None


@competition_router.get(
    "/{competition_id}/get-categories",
    response_model=List[CategoryName],
    name="Returns categories of the competition",
)
async def get_categories(competition_id: str, db: Session = Depends()):
    """
    Returns categories of the competition
    """
    query = (
        select(CategoryModel.id, CategoryModel.name)
        .join(TournamentModel, TournamentModel.category_id == CategoryModel.id)
        .distinct(CategoryModel.id)
        .filter(TournamentModel.competition_id == competition_id)
    )
    categories = db.execute(query).all()
    return categories


@competition_router.get(
    "/{competition_id}/get-teams",
    response_model=List[TeamName],
    name="Returns teams of the competition",
)
async def get_teams(
    competition_id: UUID4,
    db: Session = Depends(),
    current_user: User = Depends(get_active_user),
):
    """
    Returns teams of the competition
    """
    verify_role(current_user, [Role.ADMIN["name"], Role.COACH["name"]])

    query = (
        select(TeamModel.id, TeamModel.name, TeamModel.abbreviation)
        .join(AthleteModel, AthleteModel.team_id == TeamModel.id)
        .join(AthleteGroupModel, AthleteGroupModel.athlete_id == AthleteModel.id)
        .join(
            AthleteCompetitionModel,
            AthleteCompetitionModel.id == AthleteGroupModel.athlete_competition_id,
        )
        .filter(AthleteCompetitionModel.competition_id == competition_id)
        .distinct()
    )
    if get_role(current_user) == "COACH":
        query = query.filter(TeamModel.coach_id == current_user.id)

    teams = db.execute(query).all()
    return teams


@competition_router.get(
    "/{competition_id}",
    response_model=Competition,
    name="Returns competition by ID",
)
async def get_by_id_full(
    competition_id: UUID4,
    current_user: User = Depends(get_active_user_or_none),
    db: Session = Depends(),
):
    """
    Returns Competition by ID
    """
    competition: Competition = crud.competition.get(db=db, id=competition_id)
    if competition.show_public:
        return competition
    if current_user is None:
        raise HTTPException(404)
    try:
        verify_role(current_user, [Role.ADMIN["name"]])
        return competition
    except Exception as e:
        print(e)
        raise HTTPException(404)


@competition_router.get(
    "/{competition_id}/print",
    response_model=Competition,
    name="Returns competition by ID to print",
)
async def get_by_id_to_print(
    competition_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns Competition by ID To Print
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    competition: Optional[Competition] = crud.competition.get(db=db, id=competition_id)
    if competition is None:
        raise HTTPException(404, "Competition Not found")
    return competition


@competition_router.get(
    "/{competition_id}/athletes/{athlete_id}",
    response_model=List[TournamentNoInscriptions],
    name="Returns tournaments of athlete",
)
async def get_results_competition_athlete(
    competition_id: str, athlete_id: str, db: Session = Depends()
):
    """
    Returns tournaments of athlete
    """
    return crud.competition.get_tournaments_of_athlete(
        db=db, competition_id=competition_id, athlete_id=athlete_id
    )


@competition_router.get(
    "/{competition_id}/teams/{team_id}",
    response_model=List[TournamentNoInscriptions],
    name="Returns tournaments of team",
)
async def get_results_competition_team(
    competition_id: str, team_id: str, db: Session = Depends()
):
    """
    Returns tournaments of team
    """
    return crud.competition.get_tournaments_of_team(
        db=db, competition_id=competition_id, team_id=team_id
    )


@competition_router.post(
    "/{competition_id}/resolve-podium/{tournament_id}", name="Get podium for tournament"
)
async def resolve_podium_tournament(
    competition_id: str,
    tournament_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    tournament: Tournament = crud.tournament.get(db=db, id=tournament_id)
    verify_role(current_user, [Role.ADMIN["name"], Role.AREA["name"]])

    if tournament is None:
        raise HTTPException(
            status_code=404, detail=[{"competition": "Competition not found"}]
        )

    len_matches = len(tournament.matches)
    if tournament.category.category_type.name == "Tournament":
        for match in tournament.matches:
            if match.number == len_matches:
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


@competition_router.post(
    "/{competition_id}/matches/create",
    name="Creates matches for the competition by the inscriptions",
)
async def create_matches(
    competition_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a new Competition
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    competition = crud.competition.get(db=db, id=competition_id)

    if competition is None:
        raise HTTPException(404, "Competition Not Found")

    for tournament in competition.tournaments:
        create_matches_for_tournament(db=db, tournament=tournament)
        resolve_matches_of_tournament(db=db, tournament=tournament, athlete_bye_id="2")


@competition_router.post(
    "", response_model=Competition, name="Creates a new Competition"
)
async def create(
    competition_in: CompetitionCreate,
    # current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a new Competition
    """
    # verify_role(current_user, [Role.ADMIN["name"]])

    if competition_in.from_other:
        competition1_db: Competition = crud.competition.get(
            db=db, id=competition_in.competition1
        )
        competition2_db: Competition = crud.competition.get(
            db=db, id=competition_in.competition2
        )

        dates: List[DatetimeType] = verify_competition_in(
            db=db,
            competition_in=CompetitionUpdate(
                name=competition_in.name,
                competition_start=competition_in.competition_start,
                competition_end=competition_in.competition_end,
            ),
            is_update=False,
            verify_inscriptions=False,
            competition_id=None,
        )
        competition_db = crud.competition.create(
            db=db,
            db_obj=CompetitionModel(
                name=competition_in.name,
                inscriptions_start=None,
                inscriptions_end=None,
                competition_start=dates[2],
                competition_end=dates[3],
                show_public=False,
            ),
        )
        i = 0
        for tournament1 in competition1_db.tournaments:
            found = False
            i = i + 1
            for tournament2 in competition2_db.tournaments:
                if not tournaments_are_equal(
                    tournament1=tournament1, tournament2=tournament2
                ):
                    continue

                found = True

                if (
                    not competition_in.create_empty_tournaments
                    and len(tournament1.matches) == 0
                    and len(tournament2.matches == 0)
                ):
                    break

                tournament: Tournament = crud.tournament.create(
                    db=db,
                    obj_in=TournamentCreate(
                        age_min=tournament1.age_min,
                        age_max=tournament1.age_max,
                        weight_min=tournament1.weight_min,
                        weight_max=tournament1.weight_max,
                        belt_min_id=tournament1.belt_min_id,
                        belt_max_id=tournament1.belt_max_id,
                        is_male=tournament1.is_male,
                        competition_id=competition_db.id,
                        category_id=tournament1.category_id,
                    ),
                )

                best_four1: List[TopFour] = get_best_four(tournament=tournament1)
                best_four2: List[TopFour] = get_best_four(tournament=tournament2)
                inscriptions_added: List[UUID4] = []
                for at in [*best_four1, *best_four2]:
                    athlete_competition_id = get_athlete_competition(
                        db=db, ids=at["athletes"], competition_id=competition_db.id
                    )

                    # If athlete(s) not in competition, add it
                    if athlete_competition_id is None:
                        aux_at = AthleteCompetitionModel(
                            competition_id=competition_db.id
                        )
                        db.add(aux_at)
                        commit_to_bd(session_db=db, db_obj=aux_at)
                        athlete_competition_id = aux_at.id
                        for id in at["athletes"]:
                            db.add(
                                AthleteGroupModel(
                                    athlete_competition_id=athlete_competition_id,
                                    athlete_id=id,
                                )
                            )

                    at["competition"] = athlete_competition_id
                    if athlete_competition_id in inscriptions_added:
                        print(tournament.id)
                        continue
                    db.add(
                        InscriptionModel(
                            tournament_id=tournament.id,
                            athlete_competition_id=athlete_competition_id,
                            confirmed=True,
                            accepted=True,
                        )
                    )
                    # Commit Inscriptions
                    commit_to_bd(session_db=db)
                    inscriptions_added.append(athlete_competition_id)

                len1 = len(best_four1)
                len2 = len(best_four2)
                if len1 + len2 == 0:
                    continue

                if len1 + len2 < 3:
                    red = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=1
                    )
                    blue = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=2
                    )
                    db.add(
                        MatchModel(
                            number=1,
                            athlete_red_id=(
                                red["competition"] if red is not None else None
                            ),
                            athlete_blue_id=(
                                blue["competition"] if blue is not None else None
                            ),
                            tournament_id=tournament.id,
                        )
                    )
                    break
                if len1 + len2 == 3:
                    at1 = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=1
                    )
                    at1 = at1["competition"] if at1 is not None else None
                    at2 = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=2
                    )
                    at2 = at2["competition"] if at2 is not None else None
                    at3 = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=1
                    )
                    at3 = at3["competition"] if at3 is not None else None

                    db.add(
                        MatchModel(
                            number=1,
                            athlete_red_id=at1,
                            athlete_blue_id=at2,
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=2,
                            athlete_red_id=at1,
                            athlete_blue_id=at3,
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=3,
                            athlete_red_id=at2,
                            athlete_blue_id=at3,
                            tournament_id=tournament.id,
                        )
                    )
                    break
                if len1 + len2 == 4:
                    red = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=1
                    )
                    blue = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=2
                    )
                    db.add(
                        MatchModel(
                            number=1,
                            athlete_red_id=(
                                red["competition"] if red is not None else None
                            ),
                            athlete_blue_id=(
                                blue["competition"] if blue is not None else None
                            ),
                            tournament_id=tournament.id,
                        )
                    )
                    red = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=1
                    )
                    blue = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=2
                    )
                    db.add(
                        MatchModel(
                            number=2,
                            athlete_red_id=(
                                red["competition"] if red is not None else None
                            ),
                            athlete_blue_id=(
                                blue["competition"] if blue is not None else None
                            ),
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=3,
                            athlete_red_id=None,
                            athlete_blue_id=None,
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=4,
                            athlete_red_id=None,
                            athlete_blue_id=None,
                            tournament_id=tournament.id,
                        )
                    )
                    break

                for i in range(1, 5):
                    red = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=1
                    )
                    blue = get_next_athlete(
                        ids1=best_four1, ids2=best_four2, preference=2
                    )
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=(
                                red["competition"] if red is not None else None
                            ),
                            athlete_blue_id=(
                                blue["competition"] if blue is not None else None
                            ),
                            tournament_id=tournament.id,
                        )
                    )
                for i in range(5, 9):
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=None,
                            athlete_blue_id=None,
                            tournament_id=tournament.id,
                        )
                    )

                # Commit Matches
                commit_to_bd(session_db=db)
            if not found and competition_in.merge_unpair_tournaments:
                if (
                    not competition_in.create_empty_tournaments
                    and len(tournament1.matches) == 0
                ):
                    continue

                tournament: Tournament = crud.tournament.create(
                    db=db,
                    obj_in=TournamentCreate(
                        age_min=tournament1.age_min,
                        age_max=tournament1.age_max,
                        weight_min=tournament1.weight_min,
                        weight_max=tournament1.weight_max,
                        belt_min_id=tournament1.belt_min_id,
                        belt_max_id=tournament1.belt_max_id,
                        is_male=tournament1.is_male,
                        competition_id=competition_db.id,
                        category_id=tournament1.category_id,
                    ),
                )

                best_four1: List[TopFour] = get_best_four(tournament=tournament1)
                for at in best_four1:
                    athlete_competition_id = get_athlete_competition(
                        db=db, ids=at["athletes"], competition_id=competition_db.id
                    )

                    # If athlete(s) not in competition, add it
                    if athlete_competition_id is None:
                        aux_at = AthleteCompetitionModel(
                            competition_id=competition_db.id
                        )
                        db.add(aux_at)
                        commit_to_bd(session_db=db, db_obj=aux_at)
                        athlete_competition_id = aux_at.id
                        for id in at["athletes"]:
                            db.add(
                                AthleteGroupModel(
                                    athlete_competition_id=athlete_competition_id,
                                    athlete_id=id,
                                )
                            )

                    at["competition"] = athlete_competition_id

                    db.add(
                        InscriptionModel(
                            tournament_id=tournament.id,
                            athlete_competition_id=athlete_competition_id,
                            confirmed=True,
                            accepted=True,
                        )
                    )
                    # Commit Inscriptions
                    commit_to_bd(session_db=db)
                len1 = len(best_four1)
                if len1 == 0:
                    continue
                if len1 < 3:
                    db.add(
                        MatchModel(
                            number=1,
                            athlete_red_id=best_four1[0]["competition"],
                            athlete_blue_id=(
                                best_four1[1]["competition"] if len1 == 2 else None
                            ),
                            tournament_id=tournament.id,
                        )
                    )
                    continue
                if len1 == 3:
                    db.add(
                        MatchModel(
                            number=1,
                            athlete_red_id=best_four1[0]["competition"],
                            athlete_blue_id=best_four1[1]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=2,
                            athlete_red_id=best_four1[0]["competition"],
                            athlete_blue_id=best_four1[2]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=3,
                            athlete_red_id=best_four1[1]["competition"],
                            athlete_blue_id=best_four1[2]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    continue
                if len1 == 4:
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=best_four1[0]["competition"],
                            athlete_blue_id=best_four1[3]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=best_four1[1]["competition"],
                            athlete_blue_id=best_four1[2]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=None,
                            athlete_blue_id=None,
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=None,
                            athlete_blue_id=None,
                            tournament_id=tournament.id,
                        )
                    )
                    continue

                # Commit Matches
                commit_to_bd(session_db=db)
        for tournament2 in competition2_db.tournaments:
            found = False
            i = i + 1
            for tournament1 in competition1_db.tournaments:
                if not tournaments_are_equal(
                    tournament1=tournament1, tournament2=tournament2
                ):
                    continue

                found = True
                break
            if not found and competition_in.merge_unpair_tournaments:
                if (
                    not competition_in.create_empty_tournaments
                    and len(tournament2.matches) == 0
                ):
                    continue
                tournament: Tournament = crud.tournament.create(
                    db=db,
                    obj_in=TournamentCreate(
                        age_min=tournament2.age_min,
                        age_max=tournament2.age_max,
                        weight_min=tournament2.weight_min,
                        weight_max=tournament2.weight_max,
                        belt_min_id=tournament2.belt_min_id,
                        belt_max_id=tournament2.belt_max_id,
                        is_male=tournament2.is_male,
                        competition_id=competition_db.id,
                        category_id=tournament2.category_id,
                    ),
                )

                best_four2: List[TopFour] = get_best_four(tournament=tournament2)
                for at in best_four2:
                    athlete_competition_id = get_athlete_competition(
                        db=db, ids=at["athletes"], competition_id=competition_db.id
                    )

                    # If athlete(s) not in competition, add it
                    if athlete_competition_id is None:
                        aux_at = AthleteCompetitionModel(
                            competition_id=competition_db.id
                        )
                        db.add(aux_at)
                        commit_to_bd(session_db=db, db_obj=aux_at)
                        athlete_competition_id = aux_at.id
                        for id in at["athletes"]:
                            db.add(
                                AthleteGroupModel(
                                    athlete_competition_id=athlete_competition_id,
                                    athlete_id=id,
                                )
                            )

                    at["competition"] = athlete_competition_id

                    db.add(
                        InscriptionModel(
                            tournament_id=tournament.id,
                            athlete_competition_id=athlete_competition_id,
                            confirmed=True,
                            accepted=True,
                        )
                    )
                    # Commit Inscriptions
                    commit_to_bd(session_db=db)

                len1 = len(best_four2)
                if len1 == 0:
                    continue
                if len1 < 3:
                    db.add(
                        MatchModel(
                            number=1,
                            athlete_red_id=best_four2[0]["competition"],
                            athlete_blue_id=(
                                best_four2[1]["competition"] if len1 == 2 else None
                            ),
                            tournament_id=tournament.id,
                        )
                    )
                    continue
                if len1 == 3:
                    db.add(
                        MatchModel(
                            number=1,
                            athlete_red_id=best_four2[0]["competition"],
                            athlete_blue_id=best_four2[1]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=2,
                            athlete_red_id=best_four2[0]["competition"],
                            athlete_blue_id=best_four2[2]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=3,
                            athlete_red_id=best_four2[1]["competition"],
                            athlete_blue_id=best_four2[2]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    continue
                if len1 == 4:
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=best_four2[0]["competition"],
                            athlete_blue_id=best_four2[3]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=best_four2[1]["competition"],
                            athlete_blue_id=best_four2[2]["competition"],
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=None,
                            athlete_blue_id=None,
                            tournament_id=tournament.id,
                        )
                    )
                    db.add(
                        MatchModel(
                            number=i,
                            athlete_red_id=None,
                            athlete_blue_id=None,
                            tournament_id=tournament.id,
                        )
                    )
                    continue

                # Commit Matches
                commit_to_bd(session_db=db)
    dates: List[DatetimeType] = verify_competition_in(
        db=db,
        competition_in=CompetitionUpdate(
            name=competition_in.name,
            inscriptions_start=competition_in.inscriptions_start,
            inscriptions_end=competition_in.inscriptions_end,
            competition_start=competition_in.competition_start,
            competition_end=competition_in.competition_end,
        ),
        is_update=False,
        competition_id=None,
        verify_inscriptions=False,
    )

    return crud.competition.create(
        db=db,
        db_obj=CompetitionModel(
            name=competition_in.name,
            inscriptions_start=dates[0],
            inscriptions_end=dates[1],
            competition_start=dates[2],
            competition_end=dates[3],
            show_public=False,
        ),
    )


@competition_router.post(
    "/{competition_id}/tournaments/renumber",
    name="Renumbers matches of a specific time of the day of an area",
)
async def renumber(
    competition_id: str,
    day: int,
    morning: bool,
    area: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    :param competition_id: ID of the competition
    :param day: Day of the competition
    :param morning: If it's in the part of the morning
    :param area: Number of the area
    :param current_user: Logged User
    :return:
    """

    verify_role(current_user, [Role.ADMIN["name"]])

    tournaments: List[Tournament] = crud.tournament.get_by_area_day(
        db=db, competition_id=competition_id, day=day, morning=morning, area=area
    )
    athlete_bye = crud.athlete_competition.get_bye(db=db, competition_id=competition_id)
    athlete_bye_id = -1
    if athlete_bye is not None:
        athlete_bye_id = athlete_bye.id
    number_matches_area(
        db=db, tournaments_array=tournaments, athlete_bye_id=athlete_bye_id
    )


@competition_router.put(
    "/{competition_id}/tournaments/order/{day}/{morning}/{area}",
    response_model=List[Tournament],
    name="Orders tournaments of the array",
)
async def order_in_area(
    competition_id: str,
    day: int,
    morning: bool,
    area: str,
    ids: Ids,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Order tournaments of the array
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    tournaments_db: List[Tournament] = crud.tournament.get_by_area_day(
        db=db, competition_id=competition_id, area=area, day=day, morning=morning
    )

    if len(tournaments_db) == 0:
        return []

    order = 0
    tournaments: List[Tournament] = []
    for id in ids.ids:
        for tournament in tournaments_db:
            if tournament.id == id:
                order += 1
                tournaments.append(
                    crud.tournament.update(
                        db=db, db_obj=tournament, obj_in=TournamentUpdate(order=order)
                    )
                )

    return tournaments


@competition_router.put(
    "/make-public/{competition_id}",
    response_model=Competition,
    name="Changes competition visibility",
)
async def make_public(
    competition_id: str,
    competition_in: CompetitionUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a new Competition
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    competition_db = crud.competition.get(db=db, id=competition_id)

    if competition_db is None:
        raise HTTPException(status_code=404, detail="Competition Not Found")

    if competition_in.show_public is None:
        raise HTTPException(status_code=422, detail=[{"show_public": "Invalid Value"}])

    return crud.competition.update_show(
        db=db,
        db_obj=competition_db,
        obj_in=CompetitionModel(show_public=competition_in.show_public),
    )


@competition_router.put(
    "/year-calculation/{competition_id}",
    response_model=Competition,
    name="Changes competition way of calculate athlete's age",
)
async def year_calculation(
    competition_id: str,
    competition_in: CompetitionUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Changes competition way of calculate athlete's age
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    competition_db = crud.competition.get(db=db, id=competition_id)

    if competition_db is None:
        raise HTTPException(status_code=404, detail="Competition Not Found")

    if competition_in.calculate_age_start_year is None:
        raise HTTPException(
            status_code=422, detail=[{"calculate_age_start_year": "Invalid Value"}]
        )
    c = crud.competition.update(
        db=db,
        db_obj=competition_db,
        obj_in=CompetitionUpdate(
            calculate_age_start_year=competition_in.calculate_age_start_year
        ),
    )
    return c


@competition_router.put(
    "/{competition_id}/notes",
    response_model=Competition,
    name="Updates competition's notes",
)
async def update_notes(
    competition_id: str,
    competition_in: CompetitionUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates competition's notes
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    competition_db = crud.competition.get(db=db, id=competition_id)

    if competition_db is None:
        raise HTTPException(status_code=404, detail="Competition Not Found")

    c = crud.competition.update_notes(
        db=db,
        db_obj=competition_db,
        notes=competition_in.notes,
    )
    return c


@competition_router.put(
    "/{competition_id}",
    response_model=Union[Competition, None],
    name="Updates a Competition",
)
async def update(
    competition_id: str,
    competition_in: CompetitionUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a new Competition
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    competition_db = crud.competition.get(db=db, id=competition_id)

    if competition_db is None:
        raise HTTPException(status_code=404, detail="Competition Not Found")

    dates: List[DatetimeType] = verify_competition_in(
        db=db,
        competition_in=competition_in,
        is_update=True,
        competition_id=competition_id,
        verify_inscriptions=True,
    )

    return crud.competition.update(
        db=db,
        db_obj=competition_db,
        obj_in=CompetitionModel(
            name=competition_in.name,
            inscriptions_start=dates[0],
            inscriptions_end=dates[1],
            competition_start=dates[2],
            competition_end=dates[3],
            show_public=(
                competition_db.show_public
                if competition_in.show_public is None
                else competition_in.show_public
            ),
        ),
    )


def verify_competition_in(
    db: Session,
    competition_in: CompetitionUpdate,
    is_update: bool,
    competition_id: str,
    verify_inscriptions: bool = True,
):
    error_message: Dict[str, str] = {}

    if competition_in.name is None or competition_in.name.strip() == "":
        error_message["name"] = "The competition must have a name"

    competition_name = crud.competition.get_by_name(db=db, name=competition_in.name)
    if competition_name is not None:
        if not is_update or (
            competition_id is not None and str(competition_name.id) != competition_id
        ):
            error_message["name"] = "Already exists a competition with this name"
    inscriptions_start = None
    inscriptions_end = None
    competition_start = convert_str_to_datetime(
        date_in=competition_in.competition_start
    )
    competition_end = convert_str_to_datetime(date_in=competition_in.competition_end)

    if verify_inscriptions:
        inscriptions_start = convert_str_to_datetime(
            date_in=competition_in.inscriptions_start
        )
        inscriptions_end = convert_str_to_datetime(
            date_in=competition_in.inscriptions_end
        )
        if inscriptions_start == "":
            error_message["inscriptions_start"] = (
                "The competition must have a starting date for the inscriptions"
            )

        if inscriptions_end == "":
            error_message["inscriptions_end"] = (
                "The competition must have a end date for the inscriptions"
            )

    if competition_start == "":
        error_message["competition_start"] = (
            "The competition must have a starting date for the competition"
        )

    if competition_end == "":
        error_message["competition_end"] = (
            "The competition must have a end date for the competition"
        )

    if error_message:
        raise HTTPException(status_code=400, detail=error_message)

    if verify_inscriptions:
        if inscriptions_start > inscriptions_end:
            error_message["inscriptions_start"] = (
                "The start date of the inscriptions must be inferior to the end date of the inscriptions"
            )
            error_message["inscriptions_end"] = (
                "The end date of the inscriptions must be superior to the start date of the inscriptions"
            )

        if inscriptions_end > competition_start:
            error_message["inscriptions_end"] = (
                "The end date of the inscriptions must be inferior to the start date of the competition"
            )
            error_message["competition_start"] = (
                "The start date of the competition must be inferior to the end date of the inscriptions"
            )

    if competition_start > competition_end:
        error_message["competition_start"] = (
            "The start date of the competition must be inferior to the end date of the competition"
        )
        error_message["competition_end"] = (
            "The end date of the competition must be superior to the start date of the competition"
        )

    if competition_in.show_public is None:
        competition_in.show_public = False

    if error_message:
        raise HTTPException(status_code=400, detail=error_message)

    return [inscriptions_start, inscriptions_end, competition_start, competition_end]


def tournaments_are_equal(tournament1: Tournament, tournament2: Tournament):
    return (
        tournament1.category_id == tournament2.category_id
        and tournament1.is_male == tournament2.is_male
        and tournament1.age_min == tournament2.age_min
        and tournament1.age_max == tournament2.age_max
        and tournament1.weight_min == tournament2.weight_min
        and tournament1.weight_max == tournament2.weight_max
        and tournament1.belt_min == tournament2.belt_min
        and tournament1.belt_max == tournament2.belt_max
    )


def convert_str_to_datetime(date_in: str):
    format = "%d-%m-%Y"
    try:
        return datetime.datetime.strptime(date_in, format)
    except:
        return ""


class TopFour(TypedDict):
    athletes: List[UUID4]
    competition: UUID4 | None
    position: int


def get_best_four(tournament: Tournament) -> List[TopFour]:
    if len(tournament.matches) == 0:
        return []
    if len(tournament.matches) == 1:
        if tournament.matches[0].athlete_red_id is None:
            if tournament.matches[0].athlete_blue_id is None:
                return []
            return [
                TopFour(
                    competition=None,
                    athletes=[
                        group.athlete_id
                        for group in tournament.matches[0].athlete_blue.athletes_group
                    ],
                    position=1,
                )
            ]
        if tournament.matches[0].athlete_blue_id is None:
            return [
                TopFour(
                    competition=None,
                    athletes=[
                        group.athlete_id
                        for group in tournament.matches[0].athlete_red.athletes_group
                    ],
                    position=1,
                )
            ]

        red_winner = (
            tournament.matches[0].winner_id is None
            or tournament.matches[0].athlete_red_id == tournament.matches[0].winner_id
        )

        return [
            TopFour(
                competition=None,
                athletes=[
                    group.athlete_id
                    for group in tournament.matches[0].athlete_red.athletes_group
                ],
                position=1 if red_winner else 2,
            ),
            TopFour(
                competition=None,
                athletes=[
                    group.athlete_id
                    for group in tournament.matches[0].athlete_blue.athletes_group
                ],
                position=2 if red_winner else 1,
            ),
        ]

    if len(tournament.matches) == 3:
        if tournament.first_place_id is None:
            return []
        athlete1 = TopFour(
            competition=None,
            athletes=[
                group.athlete_id for group in tournament.first_place.athletes_group
            ],
            position=1,
        )
        if tournament.second_place_id is None:
            return [athlete1]
        athlete2 = TopFour(
            competition=None,
            athletes=[
                group.athlete_id for group in tournament.second_place.athletes_group
            ],
            position=2,
        )
        if tournament.third_place_id is None:
            return [athlete1, athlete2]
        return [
            athlete1,
            athlete2,
            TopFour(
                competition=None,
                athletes=[
                    group.athlete_id for group in tournament.third_place.athletes_group
                ],
                position=3,
            ),
        ]

    select3 = False
    for match in tournament.matches:
        if match.number is None or match.number <= len(tournament.matches) - 4:
            continue
        if match.normal_win is not None and match.normal_win is False:
            select3 = True

    if tournament.first_place_id is None:
        return []
    athlete1 = TopFour(
        competition=None,
        athletes=[group.athlete_id for group in tournament.first_place.athletes_group],
        position=1,
    )
    if tournament.second_place_id is None:
        return [athlete1]
    athlete2 = TopFour(
        competition=None,
        athletes=[group.athlete_id for group in tournament.second_place.athletes_group],
        position=2,
    )
    if tournament.third_place_id is None:
        return [athlete1, athlete2]

    if select3:
        return [
            athlete1,
            athlete2,
            TopFour(
                competition=None,
                athletes=[
                    group.athlete_id for group in tournament.third_place.athletes_group
                ],
                position=3,
            ),
        ]

    forth_athlete = None
    top_three = [
        tournament.first_place_id,
        tournament.second_place_id,
        tournament.third_place_id,
    ]
    for match in tournament.matches:
        if match.number is None or match.number <= len(tournament.matches) - 4:
            continue
        if match.athlete_red_id not in top_three:
            forth_athlete = match.athlete_red
            break
        if match.athlete_blue_id not in top_three:
            forth_athlete = match.athlete_blue
            break
    if forth_athlete is None:
        return [
            athlete1,
            athlete2,
            TopFour(
                competition=None,
                athletes=[
                    group.athlete_id for group in tournament.third_place.athletes_group
                ],
                position=3,
            ),
        ]

    return [
        athlete1,
        athlete2,
        TopFour(
            competition=None,
            athletes=[
                group.athlete_id for group in tournament.third_place.athletes_group
            ],
            position=3,
        ),
        TopFour(
            competition=None,
            athletes=[group.athlete_id for group in forth_athlete.athletes_group],
            position=4,
        ),
    ]

    return []


def get_athlete_competition(
    db: Session, ids: List[UUID4], competition_id: UUID4
) -> UUID4 | None:
    query = (
        select(AthleteCompetitionModel.id)
        .join(AthleteGroupModel)
        .filter(AthleteCompetitionModel.competition_id == competition_id)
        .filter(*[AthleteGroupModel.athlete_id == id for id in ids])
    )
    result = db.execute(query).first()
    return result[0] if result is not None else None


def get_next_athlete(ids1: List[UUID4], ids2: List[UUID4], preference: int):
    if len(ids1 if preference == 1 else ids2) == 0:
        return get_next_list(ids=ids2 if preference == 1 else ids1)
    return get_next_list(ids=ids1 if preference == 1 else ids2)


def get_next_list(ids: List[UUID4]):
    if len(ids) == 0:
        return None
    return ids.pop()
