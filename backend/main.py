from fastapi import FastAPI
from db.database import Base, engine
from controllers import TaskController

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(TaskController.router)