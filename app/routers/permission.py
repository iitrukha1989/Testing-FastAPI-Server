#############################################
#
#       Маршруты для сущности User 
#
#############################################

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.database import get_async_db
from app.applications.user import (
    get_current_user,
    app_get_user,
    app_update_user,
    app_check_admin,
    app_update_active_user,
)

router = APIRouter(prefix="/permission", tags=["permission"])

# ---------------------- PATCH METHODS -----------------------

@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def supplier_permission(
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)],
    user_id: int,
    ) -> dict:
    """
    Асинхронная функция-обработчик для измения прав доступа пользователя
    """
    try:
        app_check_admin(user)
        user_data = await app_get_user(session, user_id)
        update_user, detail = app_update_user(user_data, user_id)
        
        await session.execute(update_user)
        await session.commit()

        return {
            "status_code": status.HTTP_200_OK,
            "detail": f"Update successful, {detail}",
            }
    
    except HTTPException as http_err:
        raise HTTPException(
            status_code=http_err.status_code,
            detail=http_err.detail
            )
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")

# ---------------------- DELETE METHODS -----------------------

@router.delete("/{user_id}")
async def delete_user(
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)],
    user_id: int
    ) -> dict:
    """
    Асинхронная функция-обработчик для удаления пользователя
    """
    try:
        app_check_admin(user)
        user_data = await app_get_user(session, user_id)

        await session.delete(user_data)
        await session.commit()

        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Delete successful"
            }

    except HTTPException as http_err:
        raise HTTPException(
            status_code=http_err.status_code,
            detail=http_err.detail
            )
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.delete("/activate/{user_id}")
async def activate_user(
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)],
    user_id: int,
    ) -> None:
    """
    Асинхронная функция-обработчик для обновления признака активности пользователя
    """
    try:
        app_check_admin(user)
        user_data = await app_get_user(session, user_id)
        update_user = app_update_active_user(user_data, user_id)

        await session.execute(update_user)
        await session.commit()

        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Update successful"
            }

    except HTTPException as http_err:
        raise HTTPException(
            status_code=http_err.status_code,
            detail=http_err.detail
            )
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")
