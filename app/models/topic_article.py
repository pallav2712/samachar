from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TopicArticle(Base):
    __tablename__ = "topic_articles"

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        primary_key=True,
    )

    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id"),
        primary_key=True,
    )