from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import users, todos, ai
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# set this to your React dev origin(s)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # use "*" only if you DON'T send cookies/auth
    allow_credentials=True,         # False if you don't use cookies/Authorization
    allow_methods=["*"],            # or list: ["GET","POST","PUT","DELETE","OPTIONS"]
    allow_headers=["*"],            # include "Content-Type", "Authorization", etc.
)

app.include_router(users.router)
app.include_router(todos.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {"Hello": "World"}
