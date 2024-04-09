from typing import List
from fastapi import APIRouter, Depends
import crud
from schemas import Belt

from sql_app import Session

belt_router = APIRouter(prefix="/belts", tags=["Belt"])


@belt_router.get("", response_model=List[Belt], name="Returns all Belts")
async def get_all(db: Session = Depends()):
    """
    Returns all Belts
    """

    return crud.belt.get_all(db=db)
