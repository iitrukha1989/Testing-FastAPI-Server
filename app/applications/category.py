#########################################################
#
#        Бизнес-логика для сущности Category
#
#########################################################

from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    insert,
    update
)
from fastapi import (
    status,
    HTTPException,
)

from app.models.category import Category
from app.schemas.category import CreateCategory


async def app_get_all_categories(
        session: AsyncSession,
    ):
    """
    Асинхронная функция для получения всех категорий
    """
    categories_stmt = select(Category).where(Category.is_active == True)  # noqa: E712
    categories = (await session.scalars(categories_stmt)).all()
    
    return categories


async def app_get_category(
        session: AsyncSession,
        category_id: int | None = None,
        category_slug: str | None = None,
        user_id: int | None = None,
    ):
    """
    Асинхронная функция для определенной категории по признаку id или slug
    """
    category_stmt = select(Category)

    if user_id is None:
        category_stmt = category_stmt.where(Category.is_active == True) # noqa: E712
    
    if category_id:
        category_stmt = category_stmt.where(Category.id == category_id)
    elif category_slug:
        category_stmt = category_stmt.where(Category.slug == category_slug)

    category = await session.scalar(category_stmt)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category


def app_create_category(
        create_category: CreateCategory,
    ):
    """
    Функция для создания новой категории
    """
    category = insert(Category).values(
        name=create_category.name,
        parent_id=create_category.parent_id,
        slug=slugify(create_category.name)
        )
    
    return category


def app_update_category(
        update_category: CreateCategory,
        category_id: int | None = None,
        category_slug: str | None = None,
    ):
    """
    Функция для обновления свойств категории по признаку id или slug
    """
    category_stmt = update(Category).where(Category.is_active == True)  # noqa: E712

    if category_id:
        category_stmt = category_stmt.where(Category.id == category_id)
    elif category_slug:
        category_stmt = category_stmt.where(Category.slug == category_slug)
    
    update_category = category_stmt.values(
            name=update_category.name,
            slug=slugify(update_category.name),
            parent_id=update_category.parent_id
        )

    return update_category


def app_update_active_category(
        categoty,
        category_slug: str,
    ):
    """
    Функция для обновления признака активности категории
    """
    update_stmt = update(Category).where(Category.slug == category_slug)
    
    if categoty.is_active:
        update_category = update_stmt.values(is_active=False)
    else:
        update_category = update_stmt.values(is_active=True)
    
    return update_category
