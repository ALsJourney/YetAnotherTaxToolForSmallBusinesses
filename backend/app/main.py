import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from .database.seed_entries import init_db_and_seed
from sqlmodel import SQLModel
from .database.base import engine
from dotenv import load_dotenv

from .database.seed_users import init_users

from .routers import auth_router as auth, entries_router as entries

load_dotenv()
origin = os.getenv("FRONTEND_URL")
secret_key = os.getenv("SECRET_KEY")

SECRET_KEY = secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    try:
        await init_users()
        await init_db_and_seed()
    except Exception as e:
        print(e)
        print("Error initializing database or it was already initialized.")
    print("Database initialized and seeded.")
    # Hand control over to the app
    yield
    print("Shutting the app down.")

app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

origins = [
    origin,
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(entries.router, tags=["entries"])
