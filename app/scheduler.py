from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.database import SessionLocal
from app.services.digest import generate_digest

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(
        scheduled_digest,
        "cron",
        hour=8,
        minute=0,
    )

    scheduler.start()


def scheduled_digest(application):
    db = SessionLocal()

    try:
        digest = generate_digest(db)

        if digest is None:
            return

    finally:
        db.close()

    application.bot.send_message(
        chat_id=settings.telegram_chat_id,
        text=digest,
    )