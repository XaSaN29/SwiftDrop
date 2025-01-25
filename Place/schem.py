from typing import Optional
from pydantic import BaseModel, Field


class PlaceSchema(BaseModel):
    name: str
    type: str
    about: Optional[str] = None

    class Config:
        orm_mode = True


class PlaceGetSchema(BaseModel):
    id: int
    name: str
    type: str
    about: str
    rating: float

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    joy_id: int
    name: str
    description: Optional[str]
    price: int
    quantity: Optional[int]
    is_active: bool
