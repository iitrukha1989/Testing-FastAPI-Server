#########################################################
#
#           Бизнес-логиа для сущности Review
#
#########################################################

from datetime import datetime

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    insert,
    update,
    func,
)
from fastapi import (
    HTTPException,
    status,
)

from app.models.review import Review
from app.models.rating import Rating
from app.models.product import Product
from app.schemas.review import CreateReview


async def app_get_all_reviews(
        session: AsyncSession,
    ):
    """
    Асинхронная функция для получения всех отзывов и рейтингов
    """
    review_stmt = select(Review).where(Review.is_active == True).options(joinedload(Review.rating))  # noqa: E712
    reviews = (await session.scalars(review_stmt)).all()
    
    return reviews


async def app_get_review(
        session: AsyncSession,
        review_id: int,
        user: dict | None = None,
    ):
    """
    Асинхронная функция для получения определенного отзыва
    """
    review_stmt = select(Review).where(Review.id == review_id)
    if user.get("is_admin") is None:
        review_stmt = review_stmt.where(Review.is_active == True)  # noqa: E712
        
    review = await session.scalar(review_stmt)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    return review


async def app_get_rating(
        session: AsyncSession,
        rating_id: int,
        user: dict | None = None,
    ):
    """
    Асинхронная функция для получения определенного рейтинга
    """
    rating_stmt = select(Rating).where(Rating.id == rating_id)

    if user.get("is_admin") is None:
        rating_stmt = rating_stmt.where(Review.is_active == True)  # noqa: E712

    rating = await session.scalar(rating_stmt)
    if rating is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    return rating


async def app_get_products_reviews(
        session: AsyncSession,
        product: Product,
    ):
    """
    Асинхронная функция для получения определенного отзыва и рейтинга по продукту
    """
    review_stmt = select(Review).where(
        Review.is_active == True,  # noqa: E712
        Review.product_id == product.id).options(
        joinedload(Review.rating),
        joinedload(Review.product)
    )
    review = (await session.scalars(review_stmt)).all()
    
    return review


async def app_get_products_ratings(
        session: AsyncSession,
        product: Product,
    ) -> int:
    """
    Асинхронная функция для получения кол-ва активных рейтингов и суммы по свойству grade (оценка)
    """
    review_stmt = select(Rating.id).where(Rating.is_active == True, Rating.product_id == product.id)  # noqa: E712
    rating_stmt = select(func.sum(Rating.grade)).where(Rating.is_active == True, Rating.product_id == product.id)  # noqa: E712
    reviews_count = await session.scalar(select(func.count()).select_from(review_stmt.subquery()))
    ratings_sum = await session.scalar(rating_stmt)
    
    return reviews_count, ratings_sum


def app_create_review(
        create_review: CreateReview,
        rating: Rating,
        user: dict,
    ):
    """
    Функция для создания нового отзыва
    """
    review_stmt = insert(Review).values(
            comment=create_review.comment,
            comment_data=datetime.now(),
            product_id=create_review.product_id,
            rating_id=rating.id,
            user_id=user.get("id"),
        )
    
    return review_stmt


def app_update_active_review(
        review: Review,
    ):
    """
    Функция для обновления признака активности отзыва
    """
    update_review_stmt = update(Review).where(Review.id == review.id)

    if review.is_active:
        update_review_stmt = update_review_stmt.values(is_active=False)
    else:
        update_review_stmt = update_review_stmt.values(is_active=True)

    return update_review_stmt


def app_update_acitve_rating(
        review: Review,
        rating: Rating,
    ):
    """
    Функция для обновления признака активности рейтинга
    """
    update_rating_stmt = update(Rating).where(Rating.id == review.rating_id)

    if rating.is_active:
        update_rating_stmt = update_rating_stmt.values(is_active=False)
    else:
        update_rating_stmt = update_rating_stmt.values(is_active=True)

    return update_rating_stmt
    