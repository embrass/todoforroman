#uvicorn src.main:app --reload
from fastapi import FastAPI
from src.routers import tasks

app = FastAPI()


app.include_router(tasks.router)
