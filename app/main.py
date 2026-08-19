from fastapi import FastAPI

import app.models
from app.database import Base, engine
from app.routes.news import router as news_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(news_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Samachar API is running"}
