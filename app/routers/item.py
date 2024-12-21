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

router = APIRouter(prefix="/items", tags=["Items"])
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
def get_items(user_id: int, db: Session = Depends(get_db), radius_km: float = 2.0, token: OAuth2 = Depends(oauth2_scheme)):
    # Check if email already exists
    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    # Verify the JWT token
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    # Fetch user latitude and longitude
    user_location = db.query(User.lat, User.lng).filter(
        User.id == user_id).first()
    if not user_location:
        raise ValueError("User not found")

    user_lat, user_lng = user_location

    # Query items within the radius
    items_with_distance = db.query(
        Item,
        (
            6371 * func.acos(
                func.sin(func.radians(user_lat)) * func.sin(func.radians(User.lat)) +
                func.cos(func.radians(user_lat)) * func.cos(func.radians(User.lat)) *
                func.cos(func.radians(User.lng) - func.radians(user_lng))
            )
        ).label("distance")
    ).join(User, Item.userId == User.id).filter(
        (6371 * func.acos(
            func.sin(func.radians(user_lat)) * func.sin(func.radians(User.lat)) +
            func.cos(func.radians(user_lat)) * func.cos(func.radians(User.lat)) *
            func.cos(func.radians(User.lng) - func.radians(user_lng))
        )) <= radius_km,  # Radius filter
        Item.isActive == True,  # Only active items
        Item.isDeleted == False,
        Item.userId != user_id
    ).all()

    if not items_with_distance:
        raise HTTPException(
            status_code=404, detail="No items found for this user")

# Serialize results
    results = [
        {
            **item.__dict__,
            "distance": distance
        }
        for item, distance in items_with_distance
    ]

    # Clean up SQLAlchemy metadata
    for result in results:
        result.pop("_sa_instance_state", None)

    return results


@router.get("/my_items/")
def get_my_items(user_id: int, db: Session = Depends(get_db), token: OAuth2 = Depends(oauth2_scheme)):
    # Check if email already exists
    if not token:
        raise HTTPException(status_code=401, detail="Not authotrized")
    # Verify the JWT token
    decoded_payload = jwt.verify_access_token(token)
    print(decoded_payload)

    # Query items for the given user_id
    items = db.query(Item).filter(Item.userId == user_id,
                                  Item.isDeleted == False, Item.isActive == True).all()

    if not items:
        raise HTTPException(
            status_code=404, detail="No items found for this user")

    return items
