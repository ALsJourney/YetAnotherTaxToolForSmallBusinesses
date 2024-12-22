
from sqlmodel import Session, select

from .base import get_session
from .model import Years
from ..database.model import Users, UserBase, UserCreate
from fastapi import Depends, status, HTTPException

from ..utils.utils import verify_access_token, pwd_context


def add_year(year: int, db: Session = Depends(get_session)) -> Years:
    db_year = Years(year=year)
    db.add(db_year)
    db.commit()
    db.refresh(db_year)
    return db_year


def get_user_by_username(username: str, db: Session = Depends(get_session)) -> UserBase:
    result = db.exec(select(Users).where(Users.username == (username)))
    return result.first()


def create_user(user, db: Session = Depends(get_session)) -> UserCreate:
    hashed_password = pwd_context.hash(user.password)
    db_user = Users(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_current_user(token: str = Depends(verify_access_token), db: Session = Depends(get_session)) -> UserBase:
    username = token.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = get_user_by_username(username, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
