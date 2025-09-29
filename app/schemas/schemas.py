from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# схема пайдентик



class TaskCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = ""


class TaskUpdate(BaseModel):
    status: bool


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True