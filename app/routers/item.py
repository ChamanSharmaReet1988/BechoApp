from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas import schema_item
from app.models.items_model import Item
from app.database import jwt
from datetime import datetime
from fastapi.security import OAuth2

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


@router.delete("/delete_item/{user_id}")
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


@router.put("/update_item/{user_id}")
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
