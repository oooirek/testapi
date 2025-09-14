from typing import Optional
from pydantic import BaseModel




# S == Schema
class STaskAdd(BaseModel):
    name: str
    description: Optional[str] = None

class Task(STaskAdd):
    id: int

    model_config = {"from_attributes": True}


class STaskId(BaseModel):
    ok: bool = True
    task_id: int