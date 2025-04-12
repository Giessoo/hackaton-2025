from fastapi import FastAPI
from db.database import Base, engine
from controllers import TaskController, UserController, TeamsController, UserTeamController, AuthController, FileController

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(TaskController.router)
app.include_router(UserController.router)
app.include_router(TeamsController.router)
app.include_router(UserTeamController.router)
app.include_router(AuthController.router)
app.include_router(FileController.router)