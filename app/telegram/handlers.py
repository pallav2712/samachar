from telegram import Update
from telegram.ext import ContextTypes

from app.database import SessionLocal
from app.services.llm import generate_topics_digest
from app.services.topics import (
    get_topics,
    subscribe_to_topic,
    unsubscribe_from_topic,
)


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text("Welcome to Samachar!")


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "Available commands:\n/start - Start Samachar\n/help - Show available commands"
    )


async def subscribe_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not context.args:
        await update.message.reply_text(
            "Please provide a topic. Example: /subscribe technology"
        )
        return

    topic_name = context.args[0]

    db = SessionLocal()

    try:
        result = subscribe_to_topic(db, topic_name)
    finally:
        db.close()

    await update.message.reply_text(result)


async def unsubscribe_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not context.args:
        await update.message.reply_text(
            "Please provide a topic. Example: /unsubscribe technology"
        )
        return

    topic_name = context.args[0]

    db = SessionLocal()

    try:
        result = unsubscribe_from_topic(db, topic_name)
    finally:
        db.close()

    await update.message.reply_text(result)


async def digest_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    db = SessionLocal()

    try:
        topics = get_topics(db)

        if not topics:
            await update.message.reply_text(
                "Please subscribe to at least one topic first."
            )
            return

        digest = generate_topics_digest(db, topics)

    finally:
        db.close()

    await update.message.reply_text(digest)