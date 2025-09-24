from sqlalchemy import Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column




class Base(DeclarativeBase):
    pass



class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]

    status: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
        nullable=False
    )

