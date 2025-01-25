from enum import Enum
from Orders.models import Order
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLAlchemyEnum, DateTime, Float
from sqlalchemy.orm import relationship, Session


class UserRole(str, Enum):
    USER = "user"
    DELIVERY = "deliverer"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    age = Column(Integer)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, server_default=UserRole.USER.value)
    orders = relationship("Order", foreign_keys=[Order.customer_id], back_populates="customer")
    delivered_orders = relationship("Order", foreign_keys=[Order.deliverer_id], back_populates="deliverer")
    order_items = relationship("OrderItem", back_populates="user")
