import requests
from telebot.credentials import API_TOKEN


message = 'Hello , World'

url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id=1418255178&text={message}"

print(requests.get(url).json()['ok'])