import datetime
from typing import Optional

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
    date: int = Field(default=int(datetime.datetime.now().timestamp()))
    file_id: int = Field(foreign_key="files.id")
    year_id: int = Field(foreign_key="years.id")
    cat_id: int = Field(foreign_key="categories.id")

class Years(SQLModel, table=True):
    id: int = Field(primary_key=True)
    year: conint(ge=2010, le=current_year)

class Files(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    file_path: str
    file_type: str
    user_id: int = Field(foreign_key="users.id")

class Categories(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    short_description: Optional[str]

class YearCreate(SQLModel, table=False):
    year: conint(ge=2010, le=current_year)


class EntriesCreate(SQLModel, table=False):
    revenue: float
    cost: float
    date: int
    file_id: Optional[int] = None
    year_id: int
    cat_id: int

class UserBase(SQLModel, table=False):
    username: str

    class Config:
        from_attributes = True

class UserCreate(UserBase, SQLModel, table=False):
    password: str

class UserInDb(UserBase, SQLModel, table=False):
    hashed_password: str

class Token(SQLModel, table=False):
    access_token: str
    token_type: str