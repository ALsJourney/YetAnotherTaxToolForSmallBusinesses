import datetime
import mimetypes
import os.path
from os.path import exists

from .model import Entries, Files, Years, Categories
from sqlmodel import Session
from .base import engine

# Uploads directory relative to the project root
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")


async def init_db_and_seed():
    with Session(engine) as session:

        os.makedirs(UPLOADS_DIR, exist_ok=True)

        # Create and commit `Files` and `Years` first
        year_1 = Years(year=2023)
        year_2 = Years(year=2024)
        year_3 = Years(year=2025)
        file_1_path = os.path.relpath(os.path.join(UPLOADS_DIR, "black.png"))
        file_type_1, _ = mimetypes.guess_type(file_1_path)
        file_1 = Files(name="File 1", file_path=file_1_path, file_type=file_type_1, user_id=1)
        file_2_path = os.path.relpath(os.path.join(UPLOADS_DIR, "white.png"))
        file_type_2, _ = mimetypes.guess_type(file_2_path)
        file_2 = Files(name="File 2", file_path=file_2_path, file_type=file_type_2, user_id=1)
        category_1 = Categories(name="Category 1", short_description="Category 1 description")
        category_2 = Categories(name="Category 2", short_description="Category 2 description")
        category_3 = Categories(name="Category 3")

        session.add(year_1)
        session.add(year_2)
        session.add(year_3)
        session.add(file_1)
        session.add(file_2)
        session.add(category_1)
        session.add(category_2)
        session.add(category_3)
        session.commit()

        # Now create `Entries` that depend on `Files` and `Years`
        entry_1 = Entries(
            revenue=1000,
            cost=500,
            date=int(datetime.datetime(2021, 1, 1).timestamp()),
            file_id=file_1.id,
            year_id=year_1.id,
            cat_id=category_1.id
        )
        entry_2 = Entries(
            revenue=2000,
            cost=1000,
            date=int(datetime.datetime(2021, 1, 2).timestamp()),
            file_id=file_1.id,
            year_id=year_1.id,
            cat_id=category_2.id
        )
        entry_3 = Entries(
            revenue=3000,
            cost=1500,
            date=int(datetime.datetime(2021, 1, 3).timestamp()),
            file_id=file_1.id,
            year_id=year_1.id,
            cat_id=category_3.id
        )

        session.add(entry_1)
        session.add(entry_2)
        session.add(entry_3)
        session.commit()
