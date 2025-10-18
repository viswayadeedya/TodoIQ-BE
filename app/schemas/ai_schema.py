from pydantic import BaseModel
from typing import List
from datetime import  datetime


class TaskForSuggestions(BaseModel):
    title: str


class SubtaskItem(BaseModel):
    title: str
    description: str


class SubtaskSuggestionsResponse(BaseModel):
    subtasks: list[SubtaskItem]


class TaskItem(BaseModel):
    title: str
    description: str
    priority: int
    created_at: datetime
    completed: bool


class TasksWrapper(BaseModel):
    tasks: List[TaskItem]
