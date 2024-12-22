import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session, select

from ..database.base import get_session
from ..database.crud import get_current_user, add_year
from ..database.model import UserBase, YearCreate, Years, EntriesCreate, Entries
router = APIRouter()

@router.get("/years")
def read_years(
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    years = db.exec(select(Years)).all()
    return {"data": years}

@router.delete("/years/{year_id}")
def delete_year(
    year_id: int,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    year = db.exec(select(Years).where(Years.id == year_id)).first()
    if not year:
        raise HTTPException(status_code=404, detail="Year not found")

    db.delete(year)
    db.commit()
    return {"message": "Year deleted successfully"}

@router.post("/years")
def create_year(
    payload: YearCreate,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    # Check if the year already exists
    year = db.exec(select(Years).where(Years.year == payload.year)).first()
    if year:
        raise HTTPException(status_code=400, detail="Year already exists")
    try:
        new_year = add_year(payload.year, db=db)
        return {"message": "Year created successfully", "data": new_year}
    except Exception as e:
        # Add any additional error handling or custom exceptions here
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/years/{year_id}/entries")
def read_entries(
    year_id: int,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    year = db.exec(select(Years).where(Years.id == year_id)).first()
    if not year:
        raise HTTPException(status_code=404, detail="Year not found")

    entries = db.exec(select(Entries).where(Entries.year_id == year_id)).all()
    return {"data": entries}


@router.post("/years/:year_id/entries")
def create_revenue(
    payload: EntriesCreate,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    year = db.exec(select(Years).where(Years.id == payload.year_id)).first()
    if not year:
        raise HTTPException(status_code=404, detail="Year not found")

    try:
        new_entry = Entries(**payload.model_dump())

        if isinstance(new_entry.date, datetime.datetime):
            new_entry.date = int(new_entry.date.timestamp())
        if not new_entry.date or new_entry.date == 0:
            new_entry.date = int(datetime.datetime.now().timestamp())

        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return {"message": "Revenue entry created successfully", "data": new_entry}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/years/{year_id}/entries/{entry_id}")
def delete_entry(
    year_id: int,
    entry_id: int,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    entry = db.exec(select(Entries).where(Entries.id == entry_id)).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    db.delete(entry)
    db.commit()
    return {"message": "Entry deleted successfully"}


@router.put("/years/{year_id}/entries/{entry_id}")
def update_entry(
    year_id: int,
    entry_id: int,
    payload: EntriesCreate,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    entry = db.exec(select(Entries).where(Entries.id == entry_id)).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    for key, value in payload.model_dump().items():
        setattr(entry, key, value)

    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"message": "Entry updated successfully", "data": entry}

@router.get("/years/{year_id}/entries/{entry_id}")
def read_entry(
    year_id: int,
    entry_id: int,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    entry = db.exec(select(Entries).where(Entries.id == entry_id)).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    return {"data": entry}

@router.get("/years/{year_id}/profit")
def read_profit(
    year_id: int,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    year = db.exec(select(Years).where(Years.id == year_id)).first()
    if not year:
        raise HTTPException(status_code=404, detail="Year not found")

    entries = db.exec(select(Entries).where(Entries.year_id == year_id)).all()
    total_revenue = sum([entry.revenue for entry in entries])
    total_cost = sum([entry.cost for entry in entries])
    profit = total_revenue - total_cost
    return {"profit": profit}