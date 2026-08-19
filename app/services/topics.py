from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.topic import Topic


def get_topics(db: Session):
    result = db.execute(select(Topic))
    return result.scalars().all()