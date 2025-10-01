from typing import Optional
from sqlalchemy import Boolean, ForeignKey, String, Integer
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from sqlalchemy import DateTime, func
from datetime import datetime

from app.db.database import Base



class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    status: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
        nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="tasks")

