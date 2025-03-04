#########################################################################
#
#  Модуль FastAPI определяющий маршруты для авторизации и аутентификации
#
#########################################################################

from typing import Annotated
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.schemas.user import CreateUser
from app.database import get_async_db
from app.applications.user import (
    app_create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/read_current_user", status_code=status.HTTP_200_OK)
async def read_current_user(
    user: dict = Depends(get_current_user)
    ):
    try:
        return user
    
    except Exception as err:
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    session: Annotated[AsyncSession, Depends(get_async_db)],
    create_user: CreateUser,
    ):
    try:
        user = app_create_user(create_user)
        await session.execute(user)
        await session.commit()
        
        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Create successful"
    
        }
    
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.post("/token", status_code=status.HTTP_200_OK)
async def login(
    session: Annotated[AsyncSession, Depends(get_async_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
    try:
        user = await authenticate_user(session, form_data.username, form_data.password)
        token = await create_access_token(
            user.id,
            user.username,
            user.is_admin,
            user.is_supplier,
            user.is_customer,
            timedelta(days=1)
        )
        
        return {
            'access_token': token,
            'token_type': 'bearer'
        }
    
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")
