from typing import Union, List
from fastapi import APIRouter, Depends, HTTPException
import crud
from auth import get_active_user, verify_role
from schemas import (
    Match,
    MatchCreate,
    MatchUpdate,
    MatchesTournamentCreate,
    User,
    TournamentNoInscriptions,
    MatchCalls,
    MatchRequestUpdate,
    MatchRequestSpecial,
)
from constants.roles import Role

from sql_app import Session

match_router = APIRouter(prefix="", tags=["Match"])


@match_router.get(
    "/matches/competition/{competition_id}/next",
    response_model=TournamentNoInscriptions,
    name="Returns The Tournament of the next match",
)
async def get_next(
    competition_id: str,
    area: int,
    day: int,
    morning: bool,
    number: int,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns The Tournament of the next match of the given competition
    """
    verify_role(current_user, [Role.AREA["name"]])

    return crud.match.get_next(
        db=db,
        competition_id=competition_id,
        area=area,
        day=day,
        morning=morning,
        number=number,
    )


@match_router.get(
    "/matches/competitions/{competition_id}/call",
    response_model=MatchCalls,
    name="Returns The Match",
)
async def get_call(
    competition_id: str,
    area: int,
    day: int,
    morning: bool,
    number: int,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns The Match based on the area, day, time and number
    """
    verify_role(current_user, [Role.AREA["name"]])

    return crud.match.get_call(
        db=db,
        competition_id=competition_id,
        area=area,
        day=day,
        morning=morning,
        number=number,
    )


@match_router.get(
    "/matches/call-requests/competitions/{competition_id}",
    response_model=List[MatchCalls],
    name="Returns All Call Requests of the competition",
)
async def get_call_requests(
    competition_id: str,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Returns The Match based on the area, day, time and number
    """
    verify_role(current_user, [Role.MICRO["name"]])

    if crud.competition.get(db=db, id=competition_id) is None:
        raise HTTPException(404)

    return crud.match.get_call_requests(db=db, competition_id=competition_id)


@match_router.get(
    "/tournaments/{tournament_id}/matches/{match_id}",
    response_model=Union[Match, None],
    name="Returns match by ID",
)
async def get_by_id(tournament_id, match_id, db: Session = Depends()):
    """
    Returns Match by ID
    """
    return crud.match.get(db=db, id=match_id)


@match_router.post(
    "/tournaments/{tournament_id}/matches/single",
    name="Creates a single match for the tournament",
)
async def create(
    tournament_id,
    match_in: MatchCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a single match for the tournament
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    return crud.match.create(db=db, obj_in=match_in, tournament_id=tournament_id)


@match_router.post(
    "/tournaments/{tournament_id}/matches",
    name="Creates all the matches for the tournament",
)
async def create_multiple(
    tournament_id,
    users_ids: MatchesTournamentCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates all the matches for the tournament
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    ids = users_ids.ids
    ids_to_create = []
    extras = []
    if len(ids) == 1:
        ids.append(None)
        ids_to_create = ids
    elif len(ids) == 2:
        ids_to_create = ids
    elif len(ids) == 3:
        ids_to_create = [ids[0], ids[1], ids[1], ids[2], ids[2], ids[0]]
    elif len(ids) == 4:
        extras.append(None)
        extras.append(None)
        ids_to_create = ids
    elif (len(ids)) < 9:
        extras.append(None)
        for i in range(3):
            extras.append(None)
        i = 0
        for j in range(8):
            if j % 2 == 0:
                try:
                    ids_to_create.append(ids[i])
                except IndexError:
                    ids_to_create.append(None)
                i = i + 1
            else:
                ids_to_create.append(None)
        for j in range(8):
            if j % 4 == 1:
                try:
                    ids_to_create[j] = ids[i]
                except IndexError:
                    pass
                i = i + 1
        for j in range(8):
            if j % 4 == 3:
                try:
                    ids_to_create[j] = ids[i]
                except IndexError:
                    pass
                i = i + 1
    elif (len(ids)) < 17:
        extras.append(None)
        for i in range(7):
            extras.append(None)
        i = 0
        for j in range(16):
            if j % 2 == 0:
                try:
                    ids_to_create.append(ids[i])
                except IndexError:
                    ids_to_create.append(None)
                i = i + 1
            else:
                ids_to_create.append(None)
        for j in range(16):
            if j % 4 == 1:
                try:
                    ids_to_create[j] = ids[i]
                except IndexError:
                    pass
                i = i + 1
        for j in range(16):
            if j % 4 == 3:
                try:
                    ids_to_create[j] = ids[i]
                except IndexError:
                    pass
                i = i + 1
    elif (len(ids)) < 32:
        extras.append(None)
        for i in range(15):
            extras.append(None)
        i = 0
        for j in range(32):
            if j % 2 == 0:
                try:
                    ids_to_create.append(ids[i])
                except IndexError:
                    ids_to_create.append(None)
                i = i + 1
            else:
                ids_to_create.append(None)
        for j in range(32):
            if j % 4 == 1:
                try:
                    ids_to_create[j] = ids[i]
                except IndexError:
                    pass
                i = i + 1
        for j in range(32):
            if j % 4 == 3:
                try:
                    ids_to_create[j] = ids[i]
                except IndexError:
                    pass
                i = i + 1

    crud.match.create_multiple(
        db=db, obj_in=ids_to_create, tournament_id=tournament_id, extras=extras
    )
    return


@match_router.put(
    "/tournaments/{tournament_id}/matches/{match_id}",
    response_model=Union[Match, None],
    name="Updates match by ID",
)
async def update(
    tournament_id,
    match_id,
    match_in: MatchUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Match by ID
    """

    verify_role(current_user, [Role.ADMIN["name"], Role.AREA["name"]])

    match_db = crud.match.get(db=db, id=match_id)

    if match_db is None:
        raise HTTPException(404, "Match not Found")
    return crud.match.update(db=db, db_obj=match_db, obj_in=match_in)


@match_router.put(
    "/matches/call-request/{match_id}",
    response_model=Match,
    name="Updates Call Request for a match",
)
async def update_call_request(
    match_id,
    request_in: MatchRequestUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Call Request for a match
    """

    verify_role(current_user, [Role.AREA["name"]])

    match_db = crud.match.get(db=db, id=match_id)

    if match_db is None:
        raise HTTPException(404, "Match not Found")

    return crud.match.update_request(db=db, db_obj=match_db, obj_in=request_in)


@match_router.put(
    "/matches/call-made/{match_id}",
    response_model=Match,
    name="Updates Call for a match after it being made",
)
async def update_call_made(
    match_id,
    request_in: MatchRequestUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Call for a match after it being made
    """

    verify_role(current_user, [Role.MICRO["name"]])

    match_db = crud.match.get(db=db, id=match_id)

    if match_db is None:
        raise HTTPException(404, "Match not Found")

    return crud.match.update_call_made(db=db, db_obj=match_db, obj_in=request_in)


@match_router.put(
    "/matches/special-request", response_model=MatchCalls, name="Creates a Special Call"
)
async def special_request(
    competition_id: str,
    area: int,
    day: int,
    morning: bool,
    number: int,
    call_in: MatchRequestSpecial,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a Special Call
    """
    verify_role(current_user, [Role.AREA["name"]])

    match_db = crud.match.get_call(
        db=db,
        competition_id=competition_id,
        area=area,
        day=day,
        morning=morning,
        number=number,
    )
    if match_db is None:
        raise HTTPException(404)

    return crud.match.special_request(db=db, db_obj=match_db, obj_in=call_in)


@match_router.put(
    "/matches/call-made-special/{match_id}",
    response_model=Match,
    name="Updates Call Special for a match after it being made",
)
async def update_call_made_special(
    match_id,
    request_in: MatchRequestSpecial,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Call Special for a match after it being made
    """

    verify_role(current_user, [Role.MICRO["name"]])

    match_db = crud.match.get(db=db, id=match_id)

    if match_db is None:
        raise HTTPException(404, "Match not Found")

    return crud.match.update_call_made_special(
        db=db, db_obj=match_db, obj_in=request_in
    )


@match_router.put(
    "/matches/noreturn/{match_id}",
    response_model=Union[Match, None],
    name="Updates match by ID",
)
async def update_match_no_return(
    match_id,
    match_in: MatchUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Match by ID
    """

    verify_role(current_user, [Role.ADMIN["name"], Role.AREA["name"]])

    match_db = crud.match.get(db=db, id=match_id)

    if match_db is None:
        raise HTTPException(404, "Match not Found")
    crud.match.update(db=db, db_obj=match_db, obj_in=match_in, refresh_and_return=False)
    return


@match_router.put(
    "/matches/{match_id}", response_model=Union[Match, None], name="Updates match by ID"
)
async def update_match(
    match_id,
    match_in: MatchUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Match by ID
    """

    verify_role(current_user, [Role.ADMIN["name"], Role.AREA["name"]])

    match_db = crud.match.get(db=db, id=match_id)

    if match_db is None:
        raise HTTPException(404, "Match not Found")
    return crud.match.update(db=db, db_obj=match_db, obj_in=match_in)


@match_router.delete("/matches/{match_id}", name="Deletes match by ID")
async def delete(
    match_id,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates Match by ID
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    crud.match.delete(db=db, id=match_id)
    return
