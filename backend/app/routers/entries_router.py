import datetime
import mimetypes
import os

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, Response

from sqlmodel import Session, select

from fpdf import FPDF

from ..database.base import get_session
from ..database.crud import get_current_user, add_year
from ..database.model import UserBase, YearCreate, Years, EntriesCreate, Entries, Files, Categories
from ..database.seed_entries import UPLOADS_DIR

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

@router.post("/years/{year_id}/entries")
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
    total_revenue = sum(entry.revenue for entry in entries)
    total_cost = sum(entry.cost for entry in entries)
    profit = total_revenue - total_cost
    return {"profit": profit}

@router.get("/years/uploads/{file_id}")
def read_file(
    file_id: int,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    file = db.exec(select(Files).where(Files.id == file_id)).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file.file_path, media_type=file.file_type, filename=file.name)

# upload a file, only pdf or image files are allowed
@router.post("/years/uploads")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    if file.content_type not in ("image/png", "image/jpeg", "application/pdf"):
        raise HTTPException(status_code=400, detail="Only PDF or image files are allowed")

    file_path = os.path.join(UPLOADS_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    file_type, _ = mimetypes.guess_type(file_path)
    new_file = Files(name=file.filename, file_path=file_path, file_type=file_type, user_id=current_user.id)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return {"message": "File uploaded successfully", "data": new_file}

@router.get("/years/{year_id}/export/csv")
def export_csv(
    year_id: int,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    year = db.exec(select(Years).where(Years.id == year_id)).first()
    if not year:
        raise HTTPException(status_code=404, detail="Year not found")

    entries = db.exec(select(Entries).where(Entries.year_id == year_id)).all()
    csv_data = "revenue,cost,date,profit,category\n"
    for entry in entries:
        csv_data += f"{entry.revenue},{entry.cost},{entry.date},{entry.revenue - entry.cost},{entry.cat_id}\n"



    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={year.year}.csv"}
    )

@router.get("/years/{year_id}/export/pdf")
def export_pdf(
    year_id: int,
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    year = db.exec(select(Years).where(Years.id == year_id)).first()
    if not year:
        raise HTTPException(status_code=404, detail="Year not found")

    entries = db.exec(select(Entries).where(Entries.year_id == year_id)).all()
    total_revenue = sum(entry.revenue for entry in entries)
    total_cost = sum(entry.cost for entry in entries)
    profit = total_revenue - total_cost

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.cell(200, 10, txt=f"Year: {year.year}", ln=1)

    for entry in entries:
        pdf.cell(200, 10, txt=f"Revenue: {entry.revenue}, Cost: {entry.cost}, Date: {entry.date}", ln=1)

    pdf.cell(200, 10, txt="", ln=1)
    pdf.cell(200, 10, txt=f"Profit: {profit}", ln=1)

    # remove .encode("latin-1"), as pdf.output(dest="S") returns a bytes-like object
    pdf_out = pdf.output(dest="S")  # returns a bytearray in recent fpdf2 versions
    pdf_out = bytes(pdf_out)        # convert to regular bytes just in case

    return Response(
        content=pdf_out,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={year.year}.pdf"}
    )

# get all categories
@router.get("/categories")
def read_categories(
    db: Session = Depends(get_session),
    current_user: UserBase = Depends(get_current_user)
):
    categories = db.exec(select(Categories)).all()
    return {"data": categories}
