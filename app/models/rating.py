###########################################
#
#    Описание модели для сущности Rating
#
###########################################

from sqlalchemy.orm import (
    Mapped,
    relationship,
)
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey,
)

from app.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    grade: Mapped[int] = Column(Integer)

    is_active: Mapped[bool] = Column(Boolean, default=True)

    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id"), index=True)

    user = relationship("User", back_populates="rating")
    product = relationship("Product", back_populates="ratings")
    review = relationship("Review", back_populates="rating")
