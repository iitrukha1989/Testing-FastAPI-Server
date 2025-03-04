##################################
#
#  Маршруты для сущности Review
#
##################################

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.review import CreateReview
from app.mapper.rating import data_to_model
from app.database import get_async_db
from app.applications.product import (
    app_get_product,
    app_update_rating_product,
)
from app.applications.user import (
    get_current_user,
    app_check_admin,
    app_check_customer,
)
from app.applications.review import (
    app_get_rating,
    app_get_review,
    app_get_all_reviews,
    app_get_products_reviews,
    app_create_review,
    app_update_active_review,
    app_update_acitve_rating,
    app_get_products_ratings,
)

router = APIRouter(prefix="/review", tags=["review"])

# ---------------------- GET METHODS -----------------------

@router.get("/")
async def all_reviews(
    session: Annotated[AsyncSession, Depends(get_async_db)]
    ):
    """
    Асинхронная функция-обработчик для получения всех обзоров и рейтингов
    """
    try:
        reviews = await app_get_all_reviews(session)

        return reviews
    
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")


@router.get("/products")
async def products_reviews(
    session: Annotated[AsyncSession, Depends(get_async_db)],
    product_slug: str,
    ):
    """
    Асинхронная функция-обработчик для получения всех обзоров и рейтингов по определенному продукту
    """
    try:
        product = await app_get_product(session, product_slug=product_slug)
        reviews = await app_get_products_reviews(session, product)

        return reviews
        
    except HTTPException as http_err:
        raise HTTPException(
            status_code=http_err.status_code,
            detail=http_err.detail
            )
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")

# ---------------------- POST METHODS -----------------------

@router.post("/")
async def add_review(
    session: Annotated[AsyncSession, Depends(get_async_db)],
    create_review: CreateReview,
    user: Annotated[dict, Depends(get_current_user)]
    ) -> dict:
    """
    Асинхронная функция-обработчик для создания отзыва и рейтинга
    """
    try:
        app_check_customer(user)
        product = await app_get_product(session, product_id=create_review.product_id)
        rating = data_to_model(create_review, user)
        session.add(rating)
        await session.flush()
        await session.refresh(rating)
        review = app_create_review(create_review, rating, user)

        reviews_count, ratings_sum = await app_get_products_ratings(session, product)
        rating_value  = (ratings_sum + create_review.grage) / (reviews_count + 1)
        update_product = app_update_rating_product(create_review.product_id, rating_value)

        await session.execute(update_product)
        await session.execute(review)
        await session.commit()

        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Create successful"
            }
    
    except Exception as err:
        await session.rollback()
        print(f"{err}, {status.HTTP_400_BAD_REQUEST}")

# ---------------------- DELETE METHODS -----------------------

@router.delete("/")
async def delete_review(
    review_id: int,
    session: Annotated[AsyncSession, Depends(get_async_db)],
    user: Annotated[dict, Depends(get_current_user)] 
    ) -> dict:
    """
    Асинхронная функция-обработчик для обновления признака активности отзыва и рейтинга
    """
    try:
        app_check_admin(user)
        review = await app_get_review(session, review_id, user)
        update_review = app_update_active_review(review)
        rating = await app_get_rating(session, review.rating_id, user)
        update_rating = app_update_acitve_rating(review, rating)

        await session.execute(update_review)
        await session.execute(update_rating)
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
