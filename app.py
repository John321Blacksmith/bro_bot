import logging
import sys
sys.path.append('C://Users//belok//Desktop//John321Blacksmith//bro_bot')
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

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ForceReply, Update
from telegram.ext import (Application,
                          CommandHandler,
                          ContextTypes,
                          CallbackQueryHandler,
                          MessageHandler,
                          filters)
from telebot.credentials import API_TOKEN
from telebot import great_parser

news_confs = great_parser.decode_json_data('telebot//scraping_confs.json')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet the user."""

    user = update.effective_user

    await update.message.reply_text(
        f"""Hello, {user.username}, I am your bro bot :-).\nI can show you news, weather and current stock.\nHere are the commands:
           /news - show news,
           /weather - show weather,
           /stock - show stock
        """
    )


async def choose_news_cat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show news."""
    news_cats_keyboard = [[InlineKeyboardButton('culture', callback_data='culture')],
                          [InlineKeyboardButton('sport', callback_data='sport')],
                          [InlineKeyboardButton('politics', callback_data='politics')],
                          [InlineKeyboardButton('high-tech', callback_data='high-tech')],
                          [InlineKeyboardButton('main', callback_data='main')]
                          ]

    # get a JSON serializable object
    keyboard_markup = InlineKeyboardMarkup(news_cats_keyboard)

    await update.message.reply_text("Select the category you prefer:", reply_markup=keyboard_markup)


async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    # define the chosen category as a keyword for the parser
    category = query.data

    ## get news of this category
    # unstrucured content
    news_content = great_parser.fetch_content(news_confs[category]['source'], category, news_confs)
    news_objs = great_parser.structure_data(category, news_confs, news_content)

    await update.message.reply_text(text=news_objs)


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to the user."""

    # catch user's input
    query = update.callback_query


def main() -> None:
    """Launch the bot."""

    # create the application and pass an api key
    application = Application.builder().token(API_TOKEN).build()

    # handle different commands
    application.add_handler(CommandHandler('start', start))
    # show news
    application.add_handler(CommandHandler('news', choose_news_cat))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    application.add_handler(CallbackQueryHandler(get_news))

    # # non-commands
    # application.add_handler()

    # run the bot
    application.run_polling()


if __name__ == '__main__':
    main()