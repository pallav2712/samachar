from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.topic import Topic

VALID_TOPICS = [
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


def subscribe_to_topic(
    db: Session,
    topic_name: str,
) -> str:
    topic_name = topic_name.lower()

    if topic_name not in VALID_TOPICS:
        return "Invalid topic."

    existing_topic = (
        db.query(Topic)
        .filter(Topic.name == topic_name)
        .first()
    )

    if existing_topic:
        return f"You are already subscribed to {topic_name}."

    topic = Topic(name=topic_name)

    db.add(topic)
    db.commit()

    return f"You are subscribed to {topic_name}."


def unsubscribe_from_topic(
        db: Session,
        topic_name: str,
) -> str:
    
    topic_name = topic_name.lower()
    
    if topic_name not in VALID_TOPICS:
        return "Invalid topic."

    existing_topic = (
            db.query(Topic)
            .filter(Topic.name == topic_name)
            .first()
        )

    if not existing_topic:
            return f"You are not subscribed to {topic_name}."

    
    
    db.delete(existing_topic)
    db.commit()

    return f"You have unsubscribed from {topic_name}."