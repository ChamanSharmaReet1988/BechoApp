from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas import schema_item
from app.models.items_model import Item
from app.models.user_model import User
from app.database import jwt
from datetime import datetime
from fastapi.security import OAuth2
from sqlalchemy import func

router = APIRouter(prefix="/item", tags=["Items"])
oauth2_scheme = jwt.OptionalHTTPBearer()


@router.post("/create_Item", response_model=schema_item.ItemResponse)
def create_item(item: schema_item.ItemCreate, db: Session = Depends(get_db), token: OAuth2 = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    # Verify the JWT token
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    new_user = Item(**item.dict())
    new_user.createdAt = datetime.utcnow()

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/delete_item")
def delete_item(item_id: int, db: Session = Depends(get_db), token: OAuth2 = Depends(oauth2_scheme)):
    # Check if email already exists
    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    # Verify the JWT token
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    user = db.query(Item).filter(Item.id == item_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(Item)
    db.commit()
    return {"message": "Item deleted successfully", "item_id": item_id}


@router.put("/update_item")
def update_item(item_id: int, item_data: schema_item.ItemUpdate, db: Session = Depends(get_db), token: OAuth2 = Depends(oauth2_scheme)):
    # Check if email already exists
    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    # Verify the JWT token
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    # Fetch the user by ID
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update user fields dynamically
    for field, value in item_data.dict(exclude_unset=True).items():
        setattr(item, field, value)

    # Save changes
    item.updated_at = datetime.utcnow()
    db.add(item)
    db.commit()


@router.get("/get_items")
def get_items_within_radius(user_id: int, db: Session = Depends(get_db), radius_km: float = 2.0, token: OAuth2 = Depends(oauth2_scheme)):
    # Check if email already exists
    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    # Verify the JWT token
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    # Fetch user latitude and longitude
    user_location = db.query(User.latitude, User.longitude).filter(
        User.id == user_id).first()
    if not user_location:
        raise ValueError("User not found")

    user_lat, user_lng = user_location

    # Query items within the radius
    items = db.query(
        Item,
        (
            6371 * func.acos(
                func.sin(func.radians(user_lat)) * func.sin(func.radians(User.latitude)) +
                func.cos(func.radians(user_lat)) * func.cos(func.radians(User.latitude)) *
                func.cos(func.radians(User.longitude) - func.radians(user_lng))
            )
        ).label("distance")
    ).filter(
        (6371 * func.acos(
            func.sin(func.radians(user_lat)) * func.sin(func.radians(User.latitude)) +
            func.cos(func.radians(user_lat)) * func.cos(func.radians(User.latitude)) *
            func.cos(func.radians(User.longitude) - func.radians(user_lng))
        )) <= radius_km,
        Item.isActive == True,  # Only active items
        Item.isDeleted == False  # Exclude deleted items
    ).all()

    return items
