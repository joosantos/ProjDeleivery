from typing import List, Union, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import UUID4

import crud
from auth import get_active_user, verify_role
from constants.roles import Role
from schemas import (
    Category,
    User,
    CategoryCreate,
    CategoryUpdate,
    PageQueries,
    PagedResponse,
)

from sql_app import Session

category_router = APIRouter(prefix="/categories", tags=["Category"])


@category_router.get(
    "", response_model=PagedResponse[Category], name="Gets all categories"
)
async def get_all(
    defaults: bool | None = Query(
        default=False,
        description="Returns only defaults if true or only non defaults if false",
    ),
    competition_id: UUID4 | None = Query(
        default=None,
        description="All categories of one competition",
    ),
    pagination: PageQueries = Depends(),
    db: Session = Depends(),
):
    """
    Gets all categories
    """
    categories, n_results = crud.category.get_all(
        db=db,
        defaults=defaults,
        competition_id=competition_id,
        limit=pagination.limit,
        skip=pagination.skip,
    )
    return PagedResponse(results=categories, n_results=n_results)


@category_router.get(
    "/{defaults}", response_model=List[Category], name="Gets all categories"
)
async def get_all_defaults(defaults: bool, db: Session = Depends()):
    """
    Gets all categories
    """
    categories, n_results = crud.category.get_all(
        db=db, defaults=defaults, competition_id=None, limit=-1, skip=0
    )
    return categories


@category_router.get(
    "/{name}", response_model=Union[Category, None], name="Gets category by name"
)
async def get_by_name(name, db: Session = Depends()):
    """
    Gets category by name
    """
    return crud.category.get_by_name(db=db, name=name)


@category_router.post(
    "", response_model=Union[Category, None], name="Creates a new Category"
)
async def create(
    category_in: CategoryCreate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Creates a new Category
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    error_exists = False
    error_message: Dict[str, str] = {}

    if category_in.name is None or category_in.name.strip() == "":
        error_message["name"] = "The category must have a name"
        error_exists = True

    if crud.category.get_by_name(db=db, name=category_in.name) is not None:
        error_message["name"] = "Already exists a category with this name"
        error_exists = True

    if category_in.third_place is None:
        error_message["third_place"] = (
            "The category must have an indication of third place"
        )
        error_exists = True

    if category_in.three_points is None:
        error_message["three_points"] = (
            "The category must have an indication of three points"
        )
        error_exists = True

    if category_in.rounds is None:
        error_message["rounds"] = "The category must have an indication of rounds"
        error_exists = True

    if category_in.penalties is None:
        error_message["penalties"] = "The category must have an indication of penalties"
        error_exists = True

    if category_in.number_all_at_once is None:
        error_message["number_all_at_once"] = (
            "The category must have an indication of number all at once"
        )
        error_exists = True

    if category_in.category_type_id is None:
        error_message["type"] = "The category must have a type"
        error_exists = True

    if category_in.team_category is None:
        error_message["team_category"] = (
            "The category must have an indication if it has a team"
        )
        error_exists = True

    if (
        category_in.team_category is not None
        and category_in.team_category
        and (category_in.team_number is None or category_in.team_number <= 1)
    ):
        error_message["team_number"] = (
            "The team category must have a team bigger than 1 element"
        )
        error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    return crud.category.create(db=db, obj_in=category_in)


@category_router.put(
    "/{category_id}", response_model=Union[Category, None], name="Updates a Category"
)
async def update(
    category_id: str,
    category_in: CategoryUpdate,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(),
):
    """
    Updates a Competition
    """
    verify_role(current_user, [Role.ADMIN["name"]])

    category_db = crud.category.get(db=db, id=category_id)

    if category_db is None:
        raise HTTPException(status_code=404, detail="Category Not Found")

    error_exists = False
    error_message: Dict[str, str] = {}

    if category_in.name is not None and category_in.name.strip() == "":
        error_message["name"] = "The category must have a name"
        error_exists = True

    category_name = crud.category.get_by_name(db=db, name=category_in.name)
    if category_name is not None and str(category_name.id) != category_id:
        error_message["name"] = "Already exists a category with this name"
        error_exists = True

    if (
        category_in.team_category is not None
        and category_in.team_category
        and (category_in.team_number is None or category_in.team_number <= 1)
    ):
        error_message["team_number"] = (
            "The category of team must have a team bigger than 1 element"
        )
        error_exists = True

    if error_exists:
        raise HTTPException(status_code=400, detail=error_message)

    return crud.category.update(db=db, db_obj=category_db, obj_in=category_in)
