####################################################
#
#         Бизнес-логика для сущности User
#
####################################################

from typing import Annotated
from datetime import (
    datetime,
    timedelta,
    timezone,
)

import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import (
    select,
    insert,
    update,
)
from fastapi import (
    Depends,
    HTTPException,
    status,
)

from app.models.user import User
from app.schemas.user import CreateUser
from app.conf import (
    SECRET_KEY,
    ALGORITHM,
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def create_access_token(
        user_id: int,
        username: str,
        is_admin: bool,
        is_supplier: bool,
        is_customer: bool,
        expires_delta: timedelta,
    ):
    """
    Асинхронная функция для для создания токена
    """
    payload = {
        "id": user_id,
        "sub": username,
        "is_admin": is_admin,
        "is_supplier": is_supplier,
        "is_customer": is_customer,
        "exp": int((datetime.now(timezone.utc) + expires_delta).timestamp())
    }

    return jwt.encode(payload, SECRET_KEY, ALGORITHM)
    

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ):
    """
    Асинхронная функция для для получения токена (используется как зависимость)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get("id")
        username = payload.get("sub")
        is_admin = payload.get("is_admin")
        is_supplier = payload.get('is_supplier')
        is_customer = payload.get('is_customer')
        expire = payload.get('exp')

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not validate user'
            )
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        if not isinstance(expire, int):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token format"
            )

        if expire < datetime.now(timezone.utc).timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired!"
            )
        
        return {
            'id': user_id,
            'username': username,
            'is_admin': is_admin,
            'is_supplier': is_supplier,
            'is_customer': is_customer,
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.exceptions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not validate user'
        )


async def authenticate_user(
        session: AsyncSession,
        username: str,
        password: str,
    ):
    """
    Асинхронная функция проведения аутентификации пользователя
    """
    user_stmt = select(User).where(User.username == username)
    user = await session.scalar(user_stmt)
    
    if not user or not bcrypt_context.verify(password, user.hashed_password) or user.is_active == False:  # noqa: E712
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def app_get_user(
        session: AsyncSession,
        user_id: int,
    ):
    """
    Асинхронная функция для получения данных о пользователе
    """
    user_stmt = select(User).where(User.id == user_id)
    user = await session.scalar(user_stmt)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access permission denied"
        )
    
    return user


def app_create_user(
        create_user: CreateUser,
    ):
    """
    Функция для создания/регистрации нового пользователя
    """
    user = insert(User).values(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            username=create_user.username,
            email=create_user.email,
            hashed_password=bcrypt_context.hash(create_user.password)
        )

    return user


def app_check_admin(
        user: dict,
    ) -> None:
    """
    Функция для проверки прав доступа уровеня администратор
    """
    if user.get("is_admin") is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access permission denied"
        )
    

def app_check_supplier(
        user: dict,
    ) -> None:
    """
    Функция для проверки прав доступа уровеня продавец
    """
    if user.get("is_supplier") is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access permission denied"
        )


def app_check_customer(
        user: dict,
    ) -> None:
    """
    Функция для проверки прав доступа уровеня пользователь
    """
    if user.get("is_customer") is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access permission denied"
        )


def app_check_admin_or_supplier(
        user: dict,
    ) -> None:
    """
    Функция для проверки прав доступа уровеня администратор или продавец
    """
    if user.get("is_admin") is None or user.get("is_supplier") is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access permission denied"
        )
    

def app_update_user(
        user: User,
        user_id: int,
    ) -> tuple:
    """
    Функция для измения прав доступа пользователя
    """
    user_stmt = update(User).where(User.id == user_id)

    if user.is_supplier:
        user_stmt = user_stmt.values(is_supplier=False, is_customer=True)
        detail = "user is now customer"
    else:
        user_stmt = user_stmt.values(is_supplier=True, is_customer=False)
        detail = "user is now supplier"

    return user_stmt, detail


def app_update_active_user(
        user: User,
        user_id: int,
    ):
    """
    Функция для обновления признака активности пользователя
    """
    user_stms = update(User).where(User.id == user_id)

    if user.is_active:
        user_stms = user_stms.values(is_active=False)
    else:
        user_stms = user_stms.values(is_active=True)

    return user_stms
