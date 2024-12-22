from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session

from ..database.base import get_session
from ..database.crud import get_current_user, add_year
from ..database.model import UserBase, YearCreate

router = APIRouter()


@router.post("/years")
def create_year(
    payload: YearCreate,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    try:
        new_year = add_year(payload.year, db=db)  # <-- add_year expects an int
        return {"message": "Year created successfully", "data": new_year}
    except Exception as e:
        # Add any additional error handling or custom exceptions here
        raise HTTPException(status_code=400, detail=str(e))