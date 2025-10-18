from pydantic import BaseModel
from datetime import datetime


class TodoCreate(BaseModel):
    title: str
    description: str
    priority: int
    created_at: datetime


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    created_at: datetime
    completed: bool
    owner_id: int

    class Config:
        from_attributes = True
