from fastapi import FastAPI
from db.database import Base, engine
from controllers import TaskController, UserController

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(TaskController.router)
app.include_router(UserController.router)