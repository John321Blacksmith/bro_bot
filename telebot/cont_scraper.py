import requests
import json
from bs4 import BeautifulSoup as Bs


def decode_json_data(json_file):
	"""This function receives a json file and processes it so, a dict is returned."""
	data = None
	try:
		with open(json_file, mode='r', encoding='utf-8') as f:
			data = json.load(f)
	except (Exception, json.JSONDecodeEror) as error:
		print(error)

	return data


def get_soup(url):
	"""This function receives a source links and returns a soup of the page."""
	resp = requests.get(url).text
	soup = Bs(resp, 'html.parser')

	return soup


class GreatParser(Bs):
	def __init__(self, site_dict):
		super().__init__()
		self.site_dict = site_dict
		self.list_of_objects = []

	def get_weather(self, city):
		"""This method receives a parameter of the city to find the weather data there."""
		pass

	def get_news(self, category):
		"""This method receives a parameter of the category of the news to be listed in the chat."""

		url = self.site_dict['news'][category]['source']
		soup = get_soup(url)

		# fetch all the objects from the given soup and collect the data from each one to the list
		objs = soup.find_all(self.site_dict['news'][category]['object']['tag'], self.site_dict['news'][category]['object']['class'])
		
		# iterate through each object and save its data as a dict in otder to send it to the list
		for obj in objs:
			title = obj.find(self.site_dict['news'][category]['title']['tag'], self.site_dict['news'][category]['title']['class'])
			image = obj.find(self.site_dict['news'][category]['image']['tag'], self.site_dict['news'][category]['image']['class'])
			link = obj.find(self.site_dict['news'][category]['link']['tag'], self.site_dict['news'][category]['link']['class'])
			timestamp = obj.find(self.site_dict['news'][category]['timestamp']['tag'], self.site_dict['news'][category]['timestamp']['class'])

			# form a dictionary
			news_obj = {
				'title': title,
				'image': image,
				'link': link,
				'timestamp': timestamp
			}

			# dump it to the list
			self.list_of_objects.append(news_obj)

		return self.list_of_objects

	def get_stocks(self, currency):
		"""This method receives a parameter of a currency requested by the user."""
		pass
