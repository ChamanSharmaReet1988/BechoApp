from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas import schema_user
from app.models.user_model import User
from app.database import jwt
from datetime import datetime
from fastapi.security import OAuth2

router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = jwt.OptionalHTTPBearer()


@router.post("/create_user", response_model=schema_user.UserResponse)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(
        User.phone == user.phone).first()
    if existing_user:
        existing_user.jwtToken = jwt.create_access_token(
            {"phone": user.phone})
        return existing_user

    new_user = User(**user.dict())
    new_user.jwtToken = jwt.create_access_token(
        {"phone": user.phone})
    new_user.createdAt = datetime.utcnow()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/update/{user_id}")
def update_user(user_id: int, user_data: schema_user.UserUpdate, db: Session = Depends(get_db), token: OAuth2 = Depends(oauth2_scheme)):

    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    # Verify the JWT token
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    user_phone = decoded_payload.get("phone")
    print(user_phone)

    # Fetch the user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user fields dynamically
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    # Save changes
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()

    return {"message": "User updated successfully", "user_id": user_id}


@router.put("/update_location/{user_id}")
def update_location(user_id: int, user_data: schema_user.UserLocationUpdate, db: Session = Depends(get_db), token: OAuth2 = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user fields dynamically
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    # Save changes
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()

    return {"message": "User location updated successfully", "user_id": user_id}


@router.get("/{user_id}", response_model=schema_user.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), token: OAuth2 = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), token: OAuth2 = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "Item deleted successfully", "user_id": user_id}
