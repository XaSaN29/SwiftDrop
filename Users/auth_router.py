from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from fastapi_jwt_auth.exceptions import AuthJWTException
from Users.schem import RegisterSchema, LoginSchem
from Users.models import User
from database import session
from werkzeug.security import check_password_hash, generate_password_hash


auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.post('/register')
async def signup(user: RegisterSchema, Authorize: AuthJWT = Depends()):
    db_username = session().query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return {
            'success': False,
            'message': "Username already exists"
        }
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        role=user.role,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    db = session()
    db.add(new_user)
    db.commit()

    access_token = Authorize.create_access_token(
        subject=user.username,
        expires_time=timedelta(minutes=15),
    )

    refresh_token = Authorize.create_refresh_token(
        subject=user.username,
        expires_time=timedelta(minutes=25),
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@auth_router.post('/login')
async def login(user: LoginSchem, Authorize: AuthJWT = Depends()):
    db_user = session().query(User).filter(User.username == user.username).first()
    if db_user is None or not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=401, detail="Noto'g'ri username yoki parol")

    else:
        access_token = Authorize.create_access_token(
            subject=user.username,
            expires_time=timedelta(minutes=15),
        )

        refresh_token = Authorize.create_refresh_token(
            subject=user.username,
            expires_time=timedelta(minutes=25),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


def get_user(user_id: int):
    db = session()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@auth_router.get("/users/{user_id}")
async def read_user(user_id: int):
    user = get_user(user_id)
    data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age,
        "username": user.username,
        "email": user.email,
        'role': user.role
    }
    return data


@auth_router.get("/me")
async def read_users_me(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
    except:
        return HTTPException(status_code=401, detail='not access toking')

    db = session()
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }



@auth_router.get("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        raise HTTPException(status_code=401, detail='Refresh token expired')

    current_user = Authorize.get_jwt_subject()
    db = session()
    user = db.query(User).filter(User.username == current_user).first()
    access_token = Authorize.create_access_token(
        subject=user.username,
        expires_time=timedelta(minutes=15),
    )

    return {"access_token": access_token}

