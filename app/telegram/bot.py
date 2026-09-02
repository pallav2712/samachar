from telegram.ext import Application

from app.core.config import settings


def create_bot():
    application = Application.builder().token(
        settings.telegram_bot_token
    ).build()

    return application