from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.llm import generate_topics_digest
from app.services.pipeline import fetch_and_save_news
from app.services.topics import get_topics

router = APIRouter(prefix="/news", tags=["News"])


@router.post("/fetch")
def fetch_news(
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str]:
    fetch_and_save_news(db)

    return {"message": "News fetched and saved successfully"}


@router.post("/digest")
def generate_digest(
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, str]:
    topics = get_topics(db)

    digest = generate_topics_digest(
        db,
        topics,
    )

    return {"digest": digest}