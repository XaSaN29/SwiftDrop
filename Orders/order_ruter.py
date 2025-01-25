from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from Orders.schem import OrderSchema, OrderItemSchema
from Orders.models import Order, OrderItem
from Users.models import User
from database import session

order_router = APIRouter(
    prefix="/order"
)

db = session()


@order_router.post('/create')
async def create_order(order: OrderSchema, Authpayload: AuthJWT = Depends()):
    try:
        Authpayload.jwt_required()
        current_user = Authpayload.get_jwt_subject()
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = db.query(User).filter(User.username == current_user).first()

    new_order = Order(
        customer_id=user.id,
        deliverer_id=order.deliverer_id
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    data = {
        "id": new_order.id,
        "customer_id": new_order.customer_id,
        "deliverer_id": new_order.deliverer_id,
        "created_at": order.created_at,
        "delivered_at": order.delivered_at
    }

    return data


@order_router.get('/get')
async def get_orders():
    orders = db.query(Order).all()
    if orders is None:
        raise HTTPException(status_code=404, detail="Orders not found")

    data = []
    for order in orders:
        data.append({
            "id": order.id,
            "customer_id": order.customer_id,
            "deliverer_id": order.deliverer_id,
            "created_at": order.created_at,
            "delivered_at": order.delivered_at,
            "calculate_total_items": order.calculate_total_items(db),
            "calculate_total_amount": order.calculate_total_amount(db)
        })

    return data


@order_router.get('/order/{user_id}')
async def get_user_orders(Authpayload: AuthJWT = Depends()):
    try:
        Authpayload.jwt_required()
        current_user = Authpayload.get_jwt_subject()
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = db.query(User).filter(User.username == current_user).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    orders = db.query(Order).filter(Order.customer_id == user.id).all()

    if orders is None:
        raise HTTPException(status_code=404, detail="Orders not found")
    data = []
    for order in orders:
        data.append({
            "id": order.id,
            "customer_id": order.customer_id,
            "deliverer_id": order.deliverer_id,
            "created_at": order.created_at,
            "delivered_at": order.delivered_at,
            "calculate_total_items": order.calculate_total_items(db),
            "calculate_total_amount": order.calculate_total_amount(db)
        })

    return data


@order_router.post('/item/create')
async def create_order_item(order_item: OrderItemSchema, Authpayload: AuthJWT = Depends()):
    try:
        Authpayload.jwt_required()
        current_user = Authpayload.get_jwt_subject()
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(User).filter(User.username == current_user).first()

    new_order_item = OrderItem(
        order_id=order_item.order_id,
        user_id=user.id,
        place_id=order_item.place_id,
        product_id=order_item.product_id
    )

    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)

    data = {
        "id": new_order_item.id,
        "order_id": new_order_item.order_id,
        "user_id": new_order_item.user_id,
        "place_id": new_order_item.place_id,
        "product_id": new_order_item.product_id
    }

    return data


@order_router.get('/item/get')
async def get_order_items():
    order_items = db.query(OrderItem).all()

    if order_items is None:
        raise HTTPException(status_code=404, detail="Order items not found")

    data = []
    for order_item in order_items:
        data.append({
            "id": order_item.id,
            "order_id": order_item.order_id,
            "user_id": order_item.user_id,
            "place_id": order_item.place_id,
            "product_id": order_item.product_id
        })

    return data


@order_router.get('/item/order/{order_id}')
async def get_order_items_by_order_id(order_id: int):
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    if order_items is None:
        raise HTTPException(status_code=404, detail="Order items not found")
    data = []
    for order_item in order_items:
        data.append({
            "id": order_item.id,
            "order_id": order_item.order_id,
            "user_id": order_item.user_id,
            "place_id": order_item.place_id,
            "product_id": order_item.product_id
        })

    return data


@order_router.get('/item/user/{user_id}')
async def get_order_items_by_user_id(user_id: int):
    order_items = db.query(OrderItem).filter(OrderItem.user_id == user_id).all()

    if order_items is None:
        raise HTTPException(status_code=404, detail="Order items not found")
    data = []
    for order_item in order_items:
        data.append({
            "id": order_item.id,
            "order_id": order_item.order_id,
            "user_id": order_item.user_id,
            "place_id": order_item.place_id,
            "product_id": order_item.product_id
        })

    return data
