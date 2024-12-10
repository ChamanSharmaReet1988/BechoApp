from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database.database import get_db
from app.schemas import schema_user
from app.models.user_model import User
from app.database import jwt

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create_user", response_model=schema_user.UserResponse)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(
        User.phone == user.phone).first()
    if existing_user:
        existing_user.jwt_token = jwt.create_access_token(
            {"phone": user.phone})
        return existing_user

    new_user = User(**user.dict())
    new_user.jwt_token = jwt.create_access_token(
        {"phone": user.phone})
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=schema_user.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
