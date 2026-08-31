from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
from google import genai
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.article import Article
from app.models.digest import Digest
from app.models.topic import Topic
from app.services.articles import get_articles_by_topic

gemini_client = genai.Client(api_key=settings.gemini_api_key)


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


def generate_summary_with_gemini(prompt: str) -> str:
    response = gemini_client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    return response.text


def generate_summary_with_groq(prompt: str) -> str:
    from groq import Groq

    client = Groq(api_key=settings.groq_api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content


def generate_summary_with_openrouter(prompt: str) -> str:
    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        },
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def generate_summary(prompt: str) -> str:
    try:
        return generate_summary_with_groq(prompt)

    except Exception:
        try:
            return generate_summary_with_openrouter(prompt)

        except Exception:
            try:
                return generate_summary_with_gemini(prompt)

            except Exception as exc:
                raise RuntimeError("All LLM providers failed") from exc


# def generate_summary(prompt: str) -> str:
#     try:
#         raise RuntimeError("Testing Gemini fallback")

#     except Exception:
#         try:
#             raise RuntimeError("Testing Groq fallback")

#         except Exception:
#             try:
#                 return generate_summary_with_openrouter(prompt)

#             except Exception as exc:
#                 raise RuntimeError(
#                     "All LLM providers failed"
#                 ) from exc


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

    digest = generate_summary(prompt)
    
    digest_obj = Digest(
        content=digest,
        generated_at=datetime.now(ZoneInfo("Asia/Kolkata")),
    )

    db.add(digest_obj)
    db.commit()

    return digest
