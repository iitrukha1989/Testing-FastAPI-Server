####################################################
#
#       Описание модели для сущности Category
#
####################################################

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
)

from app.database import Base
from app.models.product import Product  # noqa: F401


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {'extend_existing': True} 

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    slug: Mapped[str] = Column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = Column(Boolean, default=True)

    # self-referential
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    products = relationship("Product", back_populates="category")
