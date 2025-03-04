#########################################
#
#     Маршруты для сущности Category
#
#########################################

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
)

from app.database import get_async_db
from app.schemas.category import CreateCategory
from app.applications.user import (
    get_current_user,
    app_check_admin,
)
from app.applications.category import (
    app_get_all_categories,
    app_get_category,
    app_create_category,
    app_update_category,
    app_update_active_category,
)

router = APIRouter(prefix="/categories", tags=["category"])

# ---------------------- GET METHODS -----------------------

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_categories(
    session: Annotated[AsyncSession, Depends(get_async_db)]
    ):
    """
    Асинхронная функция-обработчик для получения всех категорий
    """
    try:
        categories = await app_get_all_categories(session)
        
        return categories
    
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.get("/{category_id}", status_code=status.HTTP_200_OK)
async def get_category_by_id(
    category_id: int,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    ):
    """
    Асинхронная функция-обработчик для определенной категории по id
    """
    try:
        category = await app_get_category(session, category_id=category_id)
        
        return category
    
    except HTTPException as http_err:
        raise HTTPException(
            status_code=http_err.status_code,
            detail=http_err.detail
            )
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.get("/slug/{category_slug}", status_code=status.HTTP_200_OK)
async def get_category_by_slug(
    category_slug: str,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    ):
    """
    Асинхронная функция-обработчик для определенной категории по slug
    """
    try:
        category = await app_get_category(session, category_slug=category_slug)
        
        return category
    
    except HTTPException as http_err:
        raise HTTPException(
            status_code=http_err.status_code,
            detail=http_err.detail
            )
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")

# ---------------------- POST METHODS -----------------------

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    create_category: CreateCategory,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)],
    ) -> dict:
    """
    Асинхронная функция-обработчик для создания новой категории
    """
    try:
        app_check_admin(user)
        category = app_create_category(create_category)

        await session.execute(category)
        await session.commit()
        
        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Create successful"
            }
    
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")

# ---------------------- PUT METHODS -----------------------

@router.put("/{category_id}", status_code=status.HTTP_200_OK)
async def update_category_by_id(
    category_id: int,
    update_category: CreateCategory,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)]
    ) -> dict:
    """
    Асинхронная функция-обработчик для обновления свойств категории по id
    """
    try:
        app_check_admin(user)
        await app_get_category(session, category_id=category_id)
        category = app_update_category(update_category, category_id=category_id)

        await session.execute(category)
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


@router.put("/slug/{category_slug}", status_code=status.HTTP_200_OK)
async def update_category_by_slug(
    category_slug: str,
    update_category: CreateCategory,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)]
    ) -> dict:
    """
    Асинхронная функция-обработчик для обновления свойств категории по slug
    """
    try:
        app_check_admin(user)
        await app_get_category(session, category_slug=category_slug)
        category = app_update_category(update_category, category_slug=category_slug)

        await session.execute(category)
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

# ---------------------- DELETE METHODS -----------------------

@router.delete("/{category_id}")
async def delete_category_by_id(
    category_id: int,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)]
    ) -> dict:
    """
    Асинхронная функция-обработчик для удаления категории по id
    """
    try:
        app_check_admin(user)
        category = await app_get_category(session, category_id=category_id)
        
        await session.delete(category)
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


@router.delete("/slug/{category_slug}")
async def delete_category_by_slug(
    category_slug: str,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)]
    ) -> dict:
    """
    Асинхронная функция-обработчик для обновления признака активности категории
    """
    try:
        app_check_admin(user)
        category = await app_get_category(session, category_slug=category_slug, user_id=user.get("id", ""))
        update_category = app_update_active_category(category, category_slug)
        
        await session.execute(update_category)
        await session.commit()
        
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Active status changed successful"
            }
    
    except HTTPException as http_err:
        raise HTTPException(
            status_code=http_err.status_code,
            detail=http_err.detail
            )
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")
