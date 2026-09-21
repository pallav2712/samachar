from sqlalchemy.orm import Session

from app.services.llm import generate_topics_digest
from app.services.pipeline import fetch_and_save_news
from app.services.topics import get_topics


def generate_digest(db: Session) -> str | None:
    topics = get_topics(db)

    if not topics:
        return None

    fetch_and_save_news(db)

    return generate_topics_digest(db, topics)