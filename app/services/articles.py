from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.topic import Topic
from app.models.topic_article import TopicArticle


def save_articles(db: Session, articles: list[dict], topic: Topic):

    saved_count = 0

    for article in articles:
        existing = db.query(Article).filter(Article.url == article["url"]).first()

        if existing:
            article_obj = existing
        else:
            article_obj = Article(
                headline=article["title"],
                url=article["url"],
                content=article["description"],
                fetched_at=datetime.now(ZoneInfo("Asia/Kolkata")),
            )

            db.add(article_obj)
            db.flush()

            saved_count += 1

        existing_relation = (
            db.query(TopicArticle)
            .filter(
                TopicArticle.topic_id == topic.id,
                TopicArticle.article_id == article_obj.id,
            )
            .first()
        )

        if not existing_relation:
            db.add(
                TopicArticle(
                    topic_id=topic.id,
                    article_id=article_obj.id,
                )
            )

    db.commit()

    return saved_count
