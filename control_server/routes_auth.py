from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserCreate, UserResponse
from auth import register_user, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


# ------------------------
# Register
# ------------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = register_user(db, user.username, user.password)
    return new_user


# ------------------------
# Login
# ------------------------
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": str(db_user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
