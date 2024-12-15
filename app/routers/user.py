from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database.database import get_db
from app.schemas import schema_user
from app.models.user_model import User
from app.database import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, OAuth2
from fastapi.openapi.utils import get_openapi
from typing import Optional

router = APIRouter(prefix="/users", tags=["Users"])

class OptionalHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        from fastapi import status
        try:
            r = await super().__call__(request)
            token = r.credentials
        except HTTPException as ex:
            assert ex.status_code == status.HTTP_403_FORBIDDEN, ex
            token = None
        return token

oauth2_scheme = OptionalHTTPBearer()


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


@router.get("/{user_id}", response_model=schema_user.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
