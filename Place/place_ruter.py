from typing import List

from fastapi import APIRouter, HTTPException, Depends
from Place.schem import PlaceSchema, PlaceGetSchema, ProductCreate
from Place.models import Place, PlaceType, PlaceRating, Product
from database import session

place_router = APIRouter(
    prefix="/place"
)

db = session()


@place_router.post('/create')
async def create_place(place: PlaceSchema):
    new_place = Place(
        name=place.name,
        type=place.type,
        about=place.about
    )

    db.add(new_place)
    db.commit()

    data = {
        "id": new_place.id,
        "name": new_place.name,
        "type": new_place.type,
        "about": new_place.about
    }

    return data


@place_router.get('/get')
async def get_places() -> list[PlaceGetSchema]:
    places = db.query(Place).all()

    data = []
    for place in places:
        data.append({
            "id": place.id,
            "name": place.name,
            "type": place.type,
            "rating": place.rating,
            "about": place.about
        })

    return data


@place_router.get('/rating_get')
async def get_places_rating(rating: int):
    try:
        rating_enum = PlaceRating(str(rating))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid rating value. Must be between 1 and 5.")

    places = db.query(Place).filter(Place.rating == rating_enum).all()

    if not places:
        raise HTTPException(status_code=404, detail="No places found with the given rating")

    data = [
        {
            "id": place.id,
            "name": place.name,
            "type": place.type,
            "rating": place.rating.value,
            "about": place.about
        }
        for place in places
    ]

    return data


@place_router.post('/product/create')
async def product_create(product: ProductCreate):
    new_product = Product(
        joy_id=product.joy_id,
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        is_active=product.is_active
    )
    db.add(new_product)
    db.commit()

    return f'Product created with ID: {new_product.id}'

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def place_products_get_id(place_id: int, db: session):
    products = db.query(Product).filter(Product.joy_id == place_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found for the given place ID")
    return products


@place_router.get('/place/products', response_model=List[dict])
async def place_products(place_id: int, db: session = Depends(get_db)):
    products = place_products_get_id(place_id, db)
    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "is_active": product.is_active,
        }
        for product in products
    ]


@place_router.put('/place/product-update')
async def place_product_update(product: ProductCreate, db: session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product.id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    product_db.name = product.name
    product_db.description = product.description
    product_db.price = product.price
    product_db.quantity = product.quantity
    product_db.is_active = product.is_active

    db.commit()
    return {"message": "Product updated successfully"}


@place_router.delete('/place/product-delete')
async def place_product_delete(product_id: int, db: session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product_db)
    db.commit()
    return {"message": "Product deleted successfully"}


@place_router.put('/place-update')
async def place_update(place: PlaceSchema, db: session = Depends(get_db)):
    place_db = db.query(Place).filter(Place.id == place.id).first()
    if not place_db:
        raise HTTPException(status_code=404, detail="Place not found")
    place_db.name = place.name
    place_db.type = place.type
    place_db.about = place.about

    db.commit()
    return {"message": "Place updated successfully"}


@place_router.delete('/place-delete')
async def place_delete(place_id: int, db: session = Depends(get_db)):
    place_db = db.query(Place).filter(Place.id == place_id).first()
    if not place_db:
        raise HTTPException(status_code=404, detail="Place not found")
    places = db.query(Place).all()
    for place in places:
        for product in place.products:
            db.delete(product)

    db.delete(place_db)
    db.commit()
    return {"message": "Place deleted successfully"}
