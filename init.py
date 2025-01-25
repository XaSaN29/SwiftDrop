from database import Base, engine
from models import User, Place, Product, Order, OrderItem, PlaceType, UserRole

Base.metadata.create_all(bind=engine)
