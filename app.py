import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telebot.credentials import API_TOKEN

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet the user."""

    user = update.effective_user

    await update.message.reply_html(
        rf"Hello {user.mention_html()}."
    )

async def show_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show weather."""

    await update.message.reply_text('weather now')


async def show_stocks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show stocks."""

    await update.message.reply_text('Stocks here')


async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show news."""
    await update.message.reply_text('News are here')


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to the user."""

    await update.message.reply_text(update.message.text)


def main() -> None:
    """Launch the bot."""

    # create the application and pass an api key
    application = Application.builder().token(API_TOKEN).build()

    # handle different commands
    application.add_handler(CommandHandler('start', start))
    # show news
    application.add_handler(CommandHandler('news', show_news))
    # show stocks
    application.add_handler(CommandHandler('stocks', show_stocks))
    # show weather
    application.add_handler(CommandHandler('weather', show_weather))

    # non-commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # run the bot
    application.run_polling()


if __name__ == '__main__':
    main()