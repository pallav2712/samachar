from google import genai

from app.core.config import settings
from app.models.article import Article

client = genai.Client(api_key=settings.gemini_api_key)


def build_prompt(articles: list[Article]) -> str:
    prompt = """
You are a news summarizer.

Create a concise and readable morning news digest from the following articles.
Use short bullet points.
Use only the information provided.
Do not invent facts.

Articles:
"""

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
