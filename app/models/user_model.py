from typing import List
from sqlalchemy.orm import  relationship, Mapped, mapped_column
from sqlalchemy import String, Integer

from app.db.database import Base






class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_verified: Mapped[bool] = mapped_column(default=False)

    tasks: Mapped[List["Task"]] = relationship(back_populates="user")