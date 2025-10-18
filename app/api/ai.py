# app/api/ai.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..services import ai_service
from . import dependencies
from datetime import datetime

# Create the router
router = APIRouter(
    prefix="/ai",
    tags=["AI Services"]
)


# Define the endpoint
@router.post("/suggest-subtasks", response_model=List[schemas.todo_schema.TodoResponse])
def get_subtask_suggestions(
        request_data: schemas.TaskForSuggestions,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    suggestions = ai_service.get_subtasks(task_title=request_data.title)
    if not suggestions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No subtasks generated")
    new_todos_to_save = []

    for subtask_dict in suggestions:
        new_todo_obj = models.Todo(
            title=subtask_dict.get("title", ""),  # .get() is safer
            description=subtask_dict.get("description", ""),
            priority=subtask_dict.get("priority", 0),
            created_at=datetime.utcnow(),
            owner_id=current_user.id
        )
        new_todos_to_save.append(new_todo_obj)
    db.add_all(new_todos_to_save)
    db.commit()
    for todo in new_todos_to_save:
        db.refresh(todo)

    return new_todos_to_save


@router.get("/re-prioritize-all", response_model=List[schemas.TodoResponse])
def re_prioritize_all_tasks(
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
):
    db_todos = current_user.todos

    if not db_todos:
        return []

    tasks_for_ai = [schemas.TodoResponse.model_validate(todo) for todo in db_todos]
    re_prioritized_tasks_data = ai_service.get_priority_tasks(task_list=tasks_for_ai)

    if not re_prioritized_tasks_data:
        raise HTTPException(status_code=400, detail="AI failed to re-prioritize tasks")

    db_todo_map = {db_todo.id: db_todo for db_todo in db_todos}

    for re_prioritized_task in re_prioritized_tasks_data:
        task_id = re_prioritized_task.get('id')
        new_priority = re_prioritized_task.get('priority')

        db_todo = db_todo_map.get(task_id)

        if db_todo and new_priority is not None:
            db_todo.priority = new_priority

    db.commit()

    return db_todos
