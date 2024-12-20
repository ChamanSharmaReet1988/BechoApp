from pydantic import BaseModel
from typing import Optional


class ItemResponse(BaseModel):
    id: int


class ItemCreate(BaseModel):
    userId: int
    title: str
    description: str
    price: str
    imageUrls: str
    otherDetails: str


class ItemUpdate(BaseModel):
    title: str
    description: str
    price: str
    imageUrls: str
    otherDetails: str
