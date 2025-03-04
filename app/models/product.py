##########################################
#
#   Описание модели для сущности Product
#
##########################################

from sqlalchemy.orm import (
    Mapped,
    relationship,
)
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey,
    Float,
)

from app.database import Base
from app.models.rating import Rating  # noqa: F401


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    slug: Mapped[str] = Column(String(255), unique=True, index=True)
    description: Mapped[str] = Column(String)
    image_url: Mapped[str] = Column(String)
    
    price: Mapped[int] = Column(Integer, nullable=False)
    stock: Mapped[int] = Column(Integer)
    rating: Mapped[float] = Column(Float)
    
    is_active: Mapped[bool] = Column(Boolean, default=True)
    
    category_id: Mapped[int] = Column(Integer, ForeignKey("categories.id"))
    supplier_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=True)

    category = relationship("Category", back_populates="products")
    review = relationship("Review", back_populates="product")
    ratings = relationship("Rating", back_populates="product")
