from enum import Enum
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLAlchemyEnum, DateTime, Float
from sqlalchemy.orm import relationship, Session


class PlaceType(str, Enum):
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    BAR = "bar"


class PlaceRating(str, Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    type = Column(SQLAlchemyEnum(PlaceType))
    rating = Column(SQLAlchemyEnum(PlaceRating), default=PlaceRating.ONE, server_default=PlaceRating.ONE.value)
    about = Column(String(255))
    products = relationship("Product", back_populates="place")

    order_items = relationship(
        "OrderItem",
        primaryjoin="Place.id == OrderItem.place_id"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    price = Column(Integer)
    quantity = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, server_default='TRUE')
    joy_id = Column(Integer, ForeignKey("places.id"))
    place = relationship("Place", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
