# app/api/users.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserCreate, UserResponse
from ..models.user_model import User
from ..database import SessionLocal
from ..api import dependencies
from . import dependencies
from ..security import hash_password, verify_password, create_access_token

# from .dependencies import get_db # <-- We will create this file next to be even cleaner!

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/signup", response_model= UserResponse)
def create_user(user: UserCreate, db: Session = Depends(dependencies.get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User Already Exists")
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,  # 401 Unauthorized is the standard code for login failures
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},  # This is part of the OAuth2 standard
        )
    token_payload = {"sub": str(user.id)}
    access_token = create_access_token(token_payload)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup")
def signup(new_user: UserCreate, db: Session = Depends(dependencies.get_db)):
    user = db.query(User).filter(User.email == new_user.email).first()
    if user:
        raise HTTPException(
            status_code=400,  # 401 Unauthorized is the standard code for login failures
            detail="Email already exists. please login",  # This is part of the OAuth2 standard
        )
    hashed_password = hash_password(new_user.password)
    db_user = User(email=new_user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user
