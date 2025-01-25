import datetime
from Place.models import Product
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLAlchemyEnum, DateTime, Float
from sqlalchemy.orm import relationship, Session


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), index=True)
    deliverer_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    delivered_at = Column(DateTime, nullable=False)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="orders")
    deliverer = relationship("User", foreign_keys=[deliverer_id], back_populates="delivered_orders")
    order_items = relationship("OrderItem", back_populates="order")

    def calculate_total_items(self, db: Session):
        return db.query(OrderItem).filter(OrderItem.order_id == self.id).count()

    def calculate_total_amount(self, db: Session):
        total = 0
        order_items = db.query(OrderItem).filter(OrderItem.order_id == self.id).all()
        for item in order_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                total += product.price
        return total


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    product_id = Column(Integer, ForeignKey("products.id"), index=True)

    order = relationship("Order", back_populates="order_items")
    user = relationship("User", back_populates="order_items")
    place = relationship("Place", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

