import httpx

from app.core.config import settings


def handle_api_error(exc: httpx.HTTPStatusError):
    status_code = exc.response.status_code

    if status_code == 401:
        raise RuntimeError("Currents API authentication failed")

    if status_code == 404:
        raise RuntimeError("Currents API endpoint not found")

    if status_code >= 500:
        raise RuntimeError("Currents API server error")

    raise RuntimeError("Currents API request failed")


def make_currents_request(url: str, params: dict):
    try:
        response = httpx.get(
            url,
            headers={"Authorization": settings.currents_api_key},
            params=params,
        )
        response.raise_for_status()
        return response

    except httpx.HTTPStatusError as exc:
        handle_api_error(exc)

    except httpx.RequestError as exc:
        raise RuntimeError("Failed to fetch news") from exc


def fetch_news_by_topics(topics: list[str]) -> dict[str, list[dict]]:
    url = "https://api.currentsapi.services/v1/latest-news"

    response = make_currents_request(
        url,
        {
            "language": "en",
            "category": topics,
        },
    )

    data = response.json()

    if not data["news"]:
        return {topic: [] for topic in topics}

    articles_by_topic = {topic: [] for topic in topics}

    for article in data["news"]:
        for category in article.get("category", []):
            if category in articles_by_topic:
                articles_by_topic[category].append(article)

    return articles_by_topic