from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "User"

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    name: str
    description: str = None

class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
