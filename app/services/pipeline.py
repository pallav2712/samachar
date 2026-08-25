from sqlalchemy.orm import Session

from app.services.articles import save_articles
from app.services.news import fetch_news_by_topic
from app.services.topics import get_topics


def fetch_and_save_news(db: Session):
    topics = get_topics(db)

    for topic in topics:
        articles = fetch_news_by_topic(topic.name)
        save_articles(db, articles, topic)