#########################################################
#
#        Бизнес-логика для сущности Product
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

from app.models.product import Product
from app.models.category import Category
from app.schemas.product import CreateProduct


async def app_get_all_products(
        session: AsyncSession,
    ):
    """
    Асинхронная функция для получения всех продуктов
    """
    products_stmt = select(Product).join(Category).where(Product.is_active == True, Category.is_active == True, Product.stock > 0)  # noqa: E712
    products = (await session.scalars(products_stmt)).all()
    
    return products


async def app_get_product(
        session: AsyncSession,
        product_id: int | None = None,
        product_slug: str | None = None,
        user: dict | None = None,
    ):
    """
    Асинхронная функция для получения продукта по признаку id или slug
    """
    product_stmt = select(Product).where(Product.stock > 0)

    if user is None:
        product_stmt = product_stmt.where(Product.is_active == True)  # noqa: E712
    elif user.get("is_supplier"):
        product_stmt = product_stmt.where(Product.supplier_id == user.get("is_supplier", ""))

    if product_id:
        product_stmt = product_stmt.where(Product.id == product_id)
    elif product_slug:
        product_stmt = product_stmt.where(Product.slug == product_slug)

    product = await session.scalar(product_stmt)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not founc"
        )
    
    return product


async def app_get_product_by_category(
        session: AsyncSession,
        category_slug: str,
    ):
    """
    Асинхронная функция для получения всех продуктов по определенной категории
    """
    category_index_list = []

    category_stmt = select(Category.id).where(Category.is_active == True, Category.slug == category_slug)  # noqa: E712
    categoty_id = await session.scalar(category_stmt)
    if categoty_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    category_index_list.append(categoty_id)
    
    category_stmt = select(Category.id).where(Category.is_active == True, Category.parent_id == categoty_id)  # noqa: E712
    categories_id = await session.scalars(category_stmt).all()
    category_index_list.extend(categories_id)
    
    product_stmt = select(Product).where(Product.category_id.in_(category_index_list), Product.is_active == True, Product.stock > 0)  # noqa: E712
    products = await session.scalars(product_stmt).all()
    if products is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return products


def app_create_product(
        create_product: CreateProduct,
        user: dict,
    ):
    """
    Функция для создания нового продукта
    """
    product = insert(Product).values(
        name=create_product.name,
        description=create_product.description,
        price=create_product.price,
        image_url=create_product.image_url,
        stock=create_product.stock,
        rating=0.0,
        slug=slugify(create_product.name),
        category_id=create_product.category_id,
        supplier_id=user.get("id", ""),
    )

    return product


def app_update_product(
        update_product: CreateProduct,
        product_id: int | None = None,
        product_slug: str | None = None,
    ):
    """
    Функция для обновления свойств продукта по признаку id или slug
    """
    product_stmt = update(Product).where(Product.is_active == True)  # noqa: E712
    
    if product_id:
        product_stmt = product_stmt.where(Product.id == product_id)
    elif product_slug:
        product_stmt = product_stmt.where(Product.slug == product_slug)

    update_product = product_stmt.values(
        name=update_product.name,
        description=update_product.description,
        price=update_product.price,
        image_url=update_product.image_url,
        stock=update_product.stock,
        category_id=update_product.category_id,
        slug=slugify(update_product.name)
        )
    
    return update_product


def app_update_rating_product(
        product_id: int,
        rating: float
    ):
    """
    Функция для обновления значения рейтинга у продукта
    """
    product_stmt = update(Product).where(Product.id == product_id).values(rating=rating)

    return product_stmt


def app_update_active_product(
        product,
        product_slug: str,
    ):
    """
    Функция для обновления признака активности продукта
    """
    product_stmt = update(Product).where(Product.slug == product_slug)

    if product.is_active:
        update_product = product_stmt._values(is_active=False)
    else:
        update_product = product_stmt._values(is_active=True)

    return update_product
