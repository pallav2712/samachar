from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.pipeline import fetch_and_save_news

router = APIRouter(prefix="/news", tags=["News"])


@router.post("/fetch")
def fetch_news(
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str]:
    
    fetch_and_save_news(db)

    return {"message": "News fetched and saved successfully"}
