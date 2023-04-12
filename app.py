"""
This bot finds all the closest markets based on your
location where you can buy a priced off product you told the bot.
"""
import logging
from warnings import filterwarnings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.warnings import PTBUserWarning
from telegram.ext import (
	filters, 
	Application,
	ContextTypes, 
	CommandHandler,
	MessageHandler,
	CallbackQueryHandler,
	ConversationHandler
)

from telebot.credentials import (API_TOKEN, BOT_NAME, users)


# define a logger
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO
	)

logger = logging.getLogger(__name__)

filterwarnings(action='ignore', message=r'.*CallbackQueryHandler', category=PTBUserWarning)


PRODUCT, VENDOR, LOCATION = range(3)


vendors = {
	'coffee': [
	[InlineKeyboardButton(text='Nestle', callback_data='Nestle')],
	[InlineKeyboardButton(text='Jacobs', callback_data='Jacobs')],
	[InlineKeyboardButton(text='Jardin', callback_data='Jardin')]
	],
	'candies': [
	[InlineKeyboardButton(text='Red October', callback_data='Red October')],
	[InlineKeyboardButton(text='Little Baby', callback_data='Little Baby')],
	[InlineKeyboardButton(text='Nesquick', callback_data='Nesquick')]
	],
	'fuzzy drinks': [
	[InlineKeyboardButton(text='CocaCola', callback_data='Coca Cola')],
	[InlineKeyboardButton(text='Buratino', callback_data='Buratino')],
	[InlineKeyboardButton(text='Lemonade', callback_data='Lemonade')]
	]
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	"""
	Starting a conversation and asking what the user has to buy.
	"""

	await update.message.reply_text(
		'What\'s up, buddy.'
		'I have heard you were going to buy something\n'
		'Please, enter a name of the product you want to buy;\n'
		'I \'ll dy my best to find a better solution.\n'
		'You can /cancel our talk'
		)

	return PRODUCT


async def store_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	"""
	Storing a product and returning a list of all the Vendors produce the product.
	"""
	user = update.message.from_user
	# fetch a previous message about a product
	product = update.message.text
	logger.info(f'The \'{user.first_name}\'\'s product: {product}')

	keyboard = InlineKeyboardMarkup(vendors[product])

	await update.message.reply_text(
			f'Ok. You\'ve entered: {product}.\n'
			'Please, choose a preferred Vendor of this product',
			reply_markup=keyboard
		)

	return VENDOR

 
async def find_by_vendor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	"""
	Storing a Vendor name and asking the user for his location.
	"""
	# fetch a previous message about a vendor
	query = update.callback_query
	await query.answer()
	vendor_name = query.data
	logger.info(f'The user \'John\'\'s choice: {vendor_name}')

	await query.edit_message_text(
			f'Well, I always knew you liked \'{vendor_name}\')).\n'
			'Now, share me your location, and I\'ll try to find the closest markets'
		)

	return LOCATION


async def find_markets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	"""
	Storing a user's location and finding a closest market to buy the product in.
	"""
	user = update.message.from_user
	# fetch a previous message about a location
	user_location = update.message.location
	logger.info(f'The \'{user.first_name}\'\'s location:\nlatitude:{user_location} \nlongitute:{user_location}')

	await update.message.reply_text(
			f'Here are the nearest markets\n'
			f'based on the location {user_location.latitude}/{user_location.longitude}'
		)

	return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""
	Cancel the trial.
	"""
	return ConversationHandler.END


def main():
	application = Application.builder().token(API_TOKEN).build()

	conv_handler = ConversationHandler(
			entry_points=[CommandHandler('start', start)],
			states={
				PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, store_product)],
				VENDOR: [CallbackQueryHandler(find_by_vendor)],
				LOCATION: [MessageHandler(filters.LOCATION, find_markets)]
			},
			fallbacks=[CommandHandler('cancel', cancel)]

		)

	application.add_handler(conv_handler)

	application.run_polling()


if __name__ == '__main__':
	main()	