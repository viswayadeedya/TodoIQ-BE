from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..api import dependencies
from typing import List


router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


@router.post("/", response_model=schemas.TodoResponse)
def create_todo(
        todo: schemas.TodoCreate,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    db_todo = models.Todo(title=todo.title, description=todo.description,
                          priority=todo.priority, created_at=todo.created_at, owner_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/", response_model=List[schemas.TodoResponse])
def get_all_todos(
        current_user: models.User = Depends(dependencies.get_current_user)
):
    return current_user.todos or []


# In app/api/todos.py

@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
        todo_id: int,
        todo_update: schemas.TodoUpdate,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")

    update_data = todo_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)

    return db_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    db.delete(db_todo)
    db.commit()


