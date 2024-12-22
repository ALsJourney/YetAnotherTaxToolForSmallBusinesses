from .model import Users
from sqlmodel import Session
from .base import engine
from ..utils.utils import pwd_context


async def init_users():
    with Session(engine) as session:
        user_1 = Users(username="user1", hashed_password=pwd_context.hash("password"))
        session.add(user_1)
        session.commit()
