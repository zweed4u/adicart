#!/usr/bin/python3.6
import os
import random
import requests
from bs4 import BeautifulSoup

class WebSession:
	def __init__(self):
		# add user agent array and randomly select for header
		self.session = requests.session()
		self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
		self.total_stock = 0

	def _request(self, method, url, params=None, data=None, headers=None):
		# add passed headers
		if headers is not None:
			for key in headers.keys():
				self.headers[key] = headers[key]
		# implement method params
		self.response = self.session.request(method, url, headers=self.headers)
	
	def parse(self):
		soup = BeautifulSoup(self.response.content, "html5lib")
		sizes = soup.findAll('select', {'name':'pid'})[0]
		for size_option in sizes.findAll('option'):
			try: # first option is bogus (Select Size)
				sizes_stock = size_option['data-maxavailable']
				qty_can_order = size_option['data-maxorderqty']
				style_size_code = size_option['value']
				size = size_option.text.strip()
				print(f'Size: {size} ({style_size_code}) :: Stock: {sizes_stock} :: Limit: {qty_can_order}')
				self.total_stock += int(float(sizes_stock))
			except:
				pass

	def get_total_stock(self):
		return self.total_stock

# example
style_code = 'BZ0223'
shoe = WebSession() # creates a session with headers
shoe._request('GET', f'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Product-Show?pid=%20{style_code}')
shoe.parse()
print(f'Total Stock: {shoe.get_total_stock()}')
