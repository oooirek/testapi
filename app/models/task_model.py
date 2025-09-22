from sqlalchemy import Column, Integer, String, Text

from app.db.database import Base




class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    
# потом добавь функционал