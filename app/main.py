from fastapi import FastAPI

import app.models
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Samachar API is running"}