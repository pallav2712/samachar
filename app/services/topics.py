from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.topic import Topic

DEFAULT_TOPICS = [
    "regional",
    "technology",
    "lifestyle",
    "business",
    "general",
    "programming",
    "science",
    "entertainment",
    "world",
    "sports",
    "finance",
    "academia",
    "politics",
    "health",
    "opinion",
    "food",
    "game",
]


def get_topics(db: Session):
    result = db.execute(select(Topic))
    return result.scalars().all()


def get_or_create_default_topics(db: Session):
    topics = get_topics(db)

    if topics:
        return topics

    topics = [Topic(name=name) for name in DEFAULT_TOPICS]

    db.add_all(topics)
    db.commit()

    return topics
