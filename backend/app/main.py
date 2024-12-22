from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database.seed import init_db_and_seed
from sqlmodel import SQLModel
from .database.base import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    await init_db_and_seed()
    print("Database initialized and seeded.")
    # Hand control over to the app
    yield
    print("Shutting the app down.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}
