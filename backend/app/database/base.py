import os

from sqlmodel import create_engine
from dotenv import load_dotenv

load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("POSTGRES_DB")
postgres_host = os.getenv("POSTGRES_HOST")
DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"

engine = create_engine(DATABASE_URL)

