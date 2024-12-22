from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..database.base import get_session
from ..database.crud import get_user_by_username, create_user, get_current_user
from ..database.model import Users, Token, UserBase, UserCreate
from ..utils.utils import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)
):
    user = get_user_by_username(form_data.username, db=db)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=None, status_code=status.HTTP_201_CREATED)
def register(
        user: UserCreate, db: Session = Depends(get_session)
):
    existing_user = get_user_by_username(user.username, db=db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    create_user(user, db)
    return {"message": "User created successfully"}


@router.get("/users/me", response_model=UserBase)
def read_users_me(current_user: UserBase = Depends(get_current_user)):
    return current_user

@router.post("/logout", response_model=None)
def logout():
    return {"message": "Logout successful"}
