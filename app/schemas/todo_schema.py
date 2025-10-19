from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoCreate(BaseModel):
    title: str
    description: str
    priority: int
    created_at: datetime


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None


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
