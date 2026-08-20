from datetime import datetime, time
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.topic import Topic
from app.models.topic_article import TopicArticle


def save_articles(db: Session, articles: list[dict], topic: Topic) -> int:

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


def get_todays_articles(db: Session) -> list[Article]:
    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()

    start_of_day = datetime.combine(
        today,
        time.min,
        tzinfo=ZoneInfo("Asia/Kolkata"),
    )

    end_of_day = datetime.combine(
        today,
        time.max,
        tzinfo=ZoneInfo("Asia/Kolkata"),
    )

    return (
        db.query(Article)
        .filter(
            Article.fetched_at >= start_of_day,
            Article.fetched_at <= end_of_day,
        )
        .all()
    )


def get_articles_by_topic(db: Session, topic: Topic) -> list[Article]:
    return (
        db.query(Article)
        .join(TopicArticle)
        .filter(TopicArticle.topic_id == topic.id)
        .order_by(Article.fetched_at.desc())
        .limit(5)
        .all()
    )