#####################################
#
#   Маршруты для сущности Product
#
#####################################

from typing import Annotated
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
)

from app.schemas.product import CreateProduct
from app.applications.category import app_get_category
from app.database import (
    get_async_db,
    celery,  # noqa: F401
)
from app.applications.product import (
    app_get_all_products,
    app_get_product,
    app_create_product,
    app_update_product,
    app_get_product_by_category,
    app_update_active_product,
)
from app.applications.user import (
    get_current_user,
    app_check_admin_or_supplier,
)

router = APIRouter(prefix="/products", tags=["products"])
logger.add(f"logs/{datetime.now()}-info.log")

# ---------------------- GET METHODS -----------------------

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(
    session: Annotated[AsyncSession, Depends(get_async_db)],
    ):
    """
    Асинхронная функция-обработчик для получения всех продуктов
    """
    logger.info(f"start function: {get_all_products.__name__}")

    try:
        products = await app_get_all_products(session)
        
        return products
    
    except Exception as err:
        logger.warning(f"error function: {get_all_products.__name__}: message {err}")
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.get("/category/{category_slug}", status_code=status.HTTP_200_OK)
async def get_product_by_category(
    category_slug: str,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    ):
    """
    Асинхронная функция-обработчик для получения всех продуктов по определенной категории
    """
    logger.info(f"start function: {get_product_by_category.__name__}")

    try:
        products = await app_get_product_by_category(session, category_slug)
        
        return products
    
    except Exception as err:
        logger.warning(f"error function: {get_product_by_category.__name__}: message {err}")
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product_id: int,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    ):
    """
    Асинхронная функция-обработчик для получения определенного продукта по id
    """
    logger.info(f"start function: {get_product_by_id.__name__}")

    try:
        product = await app_get_product(session, product_id=product_id)
        
        return product
    
    except HTTPException as http_err:
        raise HTTPException(
            status_code=http_err.status_code,
            detail=http_err.detail
            )
    except Exception as err:
        logger.warning(f"error function: {get_product_by_id.__name__}: message {err}")
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.get("/slug/{product_slug}", status_code=status.HTTP_200_OK)
async def get_product_by_slug(
    product_slug: str,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    ):
    """
    Асинхронная функция-обработчик для получения определенного продукта по slug
    """
    logger.info(f"start function: {get_product_by_slug.__name__}")

    try:
        product = await app_get_product(session, product_slug=product_slug)
        
        return product
    
    except HTTPException as http_err:
        raise HTTPException(
            status_code=http_err.status_code,
            detail=http_err.detail
            )
    except Exception as err:
        logger.warning(f"error function: {get_product_by_slug.__name__}: message {err}")
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")

# ---------------------- POST METHODS -----------------------

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    create_product: CreateProduct,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)],
    ) -> dict:
    """
    Асинхронная функция-обработчик для создания нового продукта
    """
    logger.info(f"start function: {create_product.__name__}")

    try:
        app_check_admin_or_supplier(user)
        await app_get_category(session, category_id=create_product.category_id)
        product = app_create_product(create_product, user)

        await session.execute(product)
        await session.commit()
        
        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Create successful"
            }
    
    except Exception as err:
        logger.warning(f"error function: {create_product.__name__}: message {err}")
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")

# ---------------------- PUT METHODS -----------------------

@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product_by_id(
    product_id: int,
    update_product: CreateProduct,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)],
    ) -> dict:
    """
    Асинхронная функция-обработчик для обновления свойств продукта по id
    """
    logger.info(f"start function: {update_product_by_id.__name__}")

    try:
        app_check_admin_or_supplier(user)
        await app_get_product(session, product_id=product_id, user=user)
        await app_get_category(session, category_id=update_product.category_id)
        product = app_update_product(update_product, product_id=product_id)

        await session.execute(product)
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
        logger.warning(f"error function: {update_product_by_id.__name__}: message {err}")
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.put("/slug/{product_slug}", status_code=status.HTTP_200_OK)
async def update_product_by_slug(
    product_slug: str,
    update_product: CreateProduct,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)],
    ) -> dict:
    """
    Асинхронная функция-обработчик для обновления свойств продукта по slug
    """
    logger.info(f"start function: {update_product_by_slug.__name__}")

    try:
        app_check_admin_or_supplier(user)
        product = await app_get_product(session, product_slug=product_slug, user=user)
        update_product = app_update_product(update_product, product, product_slug=product_slug)

        await session.execute(update_product)
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
        logger.warning(f"error function: {update_product_by_slug.__name__}: message {err}")
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")

# ---------------------- DELETE METHODS -----------------------

@router.delete("/{product_id}")
async def delete_product_by_id(
    product_id: int,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)],
    ) -> dict:
    """
    Асинхронная функция-обработчик для удаления продукта по id
    """
    logger.info(f"start function: {delete_product_by_id.__name__}")

    try:
        app_check_admin_or_supplier(user)
        product = await app_get_product(session, product_id=product_id, user=user)
        
        await session.delete(product)
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
        logger.warning(f"error function: {delete_product_by_id.__name__}: message {err}")
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.delete("/slug/{product_slug}")
async def delete_product_by_slug(
    product_slug: str,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)],
    ) -> dict:
    """
    Асинхронная функция-обработчик для обновления признака активности продукта
    """
    logger.info(f"start function: {delete_product_by_slug.__name__}")

    try:
        app_check_admin_or_supplier(user)
        product = await app_get_product(session, product_slug=product_slug, user=user)
        update_product = app_update_active_product(product, product_slug)
        
        await session.execute(update_product)
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
        logger.warning(f"error function: {delete_product_by_slug.__name__}: message {err}")
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")
