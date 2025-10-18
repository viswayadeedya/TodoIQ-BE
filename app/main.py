from fastapi import FastAPI
from .api import users, todos, ai
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(todos.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {"Hello": "World"}
