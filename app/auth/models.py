from sqlalchemy import String, Integer
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from app.db.database import Base


"""SQLAlchemy модели для пользователей, токенов (если нужно хранить refresh)."""


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[list["Task"]] = relationship(back_populates="user")