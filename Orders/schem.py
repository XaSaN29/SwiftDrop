from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field


class OrderSchema(BaseModel):
    deliverer_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: datetime = Field(default=None)

    class Config:
        orm_mode = True


class OrderItemSchema(BaseModel):
    order_id: int
    place_id: int
    product_id: int

    class Config:
        orm_mode = True
