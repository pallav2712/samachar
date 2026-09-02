from telegram.ext import Application, CommandHandler

from app.core.config import settings
from app.telegram.handlers import help_command, start_command


def create_bot():
    application = Application.builder().token(settings.telegram_bot_token).build()

    application.add_handler(CommandHandler("start", start_command))

    application.add_handler(CommandHandler("help", help_command))

    return application


if __name__ == "__main__":
    application = create_bot()
    application.run_polling()
