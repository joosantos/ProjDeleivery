from typing import List
from fastapi import APIRouter, Depends
import crud
from schemas import CategoryType

from sql_app import Session

category_type_router = APIRouter(prefix="/categories-type", tags=["Category Type"])


@category_type_router.get(
    "", response_model=List[CategoryType], name="Gets all categories types"
)
async def get_all(db: Session = Depends()):
    """
    Gets all categories types
    """
    return crud.category_type.get_all(db=db)
