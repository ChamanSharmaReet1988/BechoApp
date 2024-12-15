from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    phone: str


class UserCreate(BaseModel):
    phone: str


class UserResponse(UserBase):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    jwt_token: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):        
    name: Optional[str]
    email: Optional[str]
    profileImage: Optional[str]
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        
