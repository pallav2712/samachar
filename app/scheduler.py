from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.database import SessionLocal
from app.services.digest import generate_digest

scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Kolkata"))


def start_scheduler(application):
    scheduler.add_job(
        scheduled_digest,
        "interval",
        seconds = 30,
        args=[application],
    )

    scheduler.start()


async def scheduled_digest(application):
    db = SessionLocal()

    try:
        digest = generate_digest(db)

        if digest is None:
            return

    finally:
        db.close()

    await application.bot.send_message(
        chat_id=settings.telegram_chat_id,
        text=digest,
    )
