from fastapi import FastAPI
from Users.auth_router import auth_router
from Place.place_ruter import place_router
from Orders.order_ruter import order_router

app = FastAPI()

#Users
app.include_router(auth_router, tags=['Users'])
#Places
app.include_router(place_router, tags=['Places'])
#Orders
app.include_router(order_router, tags=['Orders'])

