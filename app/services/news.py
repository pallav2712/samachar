import httpx

from app.core.config import settings


def fetch_latest_news():
    url = "https://api.currentsapi.services/v1/latest-news"

    try:
        response = httpx.get(
            url,
            headers={"Authorization": settings.currents_api_key},
            params={"language": "en"},
        )

        response.raise_for_status()

    except httpx.RequestError as exc:
        raise RuntimeError("Failed to fetch latest news") from exc

    data = response.json()

    if not data["news"]:
        return []

    return data["news"]


def fetch_news_by_topic(topic: str):
    url = "https://api.currentsapi.services/v1/latest-news"

    try:
        response = httpx.get(
            url,
            headers={"Authorization": settings.currents_api_key},
            params={
                "language": "en",
                "category": topic,
            }
        )

        response.raise_for_status()

    except httpx.RequestError as exc:
        raise RuntimeError("Failed to fetch news by topic") from exc

    data = response.json()

    if not data["news"]:
        return []

    return data["news"]