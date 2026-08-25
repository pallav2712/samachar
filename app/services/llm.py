from google import genai
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.article import Article
from app.models.topic import Topic
from app.services.articles import get_articles_by_topic

client = genai.Client(api_key=settings.gemini_api_key)


def build_prompt(articles_by_topic: dict[str, list[Article]]) -> str:
    prompt = """
You are a news summarizer for a daily morning news digest.

Summarize the following news articles into concise bullet points.

Rules:

- Use one bullet point per important story.
- Keep each bullet short and informative.
- Organize stories under their respective topics.
- Do not use nested bullet points.
- Use only information provided in the articles.
- Do not invent or assume facts.
- If multiple articles describe the same story, combine them into one bullet.
- Focus on the most important information from each story.

Articles:

"""

    for topic, articles in articles_by_topic.items():
        prompt += f"\n## {topic.title()}\n"

        for article in articles:
            prompt += f"""
Headline: {article.headline}

Content: {article.content}
"""

    return prompt


def generate_summary(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    return response.text


def generate_topics_digest(
    db: Session,
    topics: list[Topic],
) -> str:
    articles_by_topic = {}

    for topic in topics:
        articles_by_topic[topic.name] = get_articles_by_topic(
            db,
            topic,
        )

    prompt = build_prompt(articles_by_topic)

    return generate_summary(prompt)
