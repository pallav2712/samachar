

from telegram.ext import Application, CommandHandler

from app.core.config import settings
from app.scheduler import start_scheduler
from app.telegram.handlers import (
    digest_command,
    help_command,
    start_command,
    subscribe_command,
    unsubscribe_command,
)


def create_bot():
    application = Application.builder().token(settings.telegram_bot_token).build()

    application.add_handler(CommandHandler("start", start_command))

    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CommandHandler("subscribe", subscribe_command))

    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))

    application.add_handler(CommandHandler("digest", digest_command))

    return application


if __name__ == "__main__":
    application = create_bot()

    
    start_scheduler(application)
    
    
    application.run_polling() #for continously message checking form telegram gui
