##########################################
#
#     Описание модели для сущности User
#
#########################################

from sqlalchemy.orm import (
    Mapped,
    relationship,
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = Column(String(255))
    last_name: Mapped[str] = Column(String(255))
    
    username: Mapped[str] = Column(String(255), unique=True)
    email: Mapped[str] = Column(String(255), unique=True)
    hashed_password: Mapped[str] = Column(String)
    
    is_active: Mapped[bool] = Column(Boolean, default=True)
    is_admin: Mapped[bool] = Column(Boolean, default=False)
    is_supplier: Mapped[bool] = Column(Boolean, default=False)
    is_customer: Mapped[bool] = Column(Boolean, default=True)

    review = relationship("Review", back_populates="user")
    rating = relationship("Rating", back_populates="user")
