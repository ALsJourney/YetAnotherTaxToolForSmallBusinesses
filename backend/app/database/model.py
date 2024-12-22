from sqlmodel import Field, SQLModel

class Entries(SQLModel, table=True):
    id: int = Field(primary_key=True)
    revenue: float
    cost: float
    date: str
    file_id: int = Field(foreign_key="files.id")
    year_id: int = Field(foreign_key="years.id")

class Years(SQLModel, table=True):
    id: int = Field(primary_key=True)
    year: int

class Files(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    file_path: str
    file_type: str