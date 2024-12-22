import datetime

from sqlmodel import Field, SQLModel
from pydantic import conint

current_year = datetime.date.today().year

class Users(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str

class Entries(SQLModel, table=True):
    id: int = Field(primary_key=True)
    revenue: float
    cost: float
    date: str
    file_id: int = Field(foreign_key="files.id")
    year_id: int = Field(foreign_key="years.id")

class Years(SQLModel, table=True):
    id: int = Field(primary_key=True)
    year: conint(ge=2010, le=current_year)

class Files(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    file_path: str
    file_type: str

class YearCreate(SQLModel, table=False):
    year: conint(ge=2010, le=current_year)

class UserBase(SQLModel, table=False):
    username: str

    class Config:
        orm_mode = True

class UserCreate(UserBase, SQLModel, table=False):
    password: str

class UserInDb(UserBase, SQLModel, table=False):
    hashed_password: str

class Token(SQLModel, table=False):
    access_token: str
    token_type: str