##########################################
#
#    Описание модели для сущности Review
#
##########################################

from datetime import datetime

from sqlalchemy.orm import (
    Mapped,
    relationship,
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
)

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comment: Mapped[str] = Column(String, nullable=False)
    comment_data: Mapped[datetime] = Column(DateTime, default=datetime.now())

    is_active: Mapped[bool] = Column(Boolean, default=True)

    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id"), index=True)
    rating_id: Mapped[int] = Column(Integer, ForeignKey("ratings.id"), index=True)

    user = relationship("User", back_populates="review")
    product = relationship("Product", back_populates="review")
    rating = relationship("Rating", back_populates="review")
