from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import authenticate_user, create_access_token, register_user
from database import get_db
from schemas import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = register_user(db, user.username, user.password)
    return new_user


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(db_user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(db_user.id),
        "username": db_user.username,
    }
