import requests
import pprint
from bs4 import BeautifulSoup
from multipledispatch import dispatch

class ProductPage():

	def __init__(self, url, title=None, price=None, nSales=None, nStock=None, rating=None, shopTitle=None, shopURL=None):
		if type(self) is ProductPage:
			raise Exception('ProductPage is an abstract class and cannot be instantiated directly')
		self.url = url
		self.title = title
		self.price = price
		self.nSales = nSales
		self.nStock = nStock
		self.rating = rating
		self.shopTitle = shopTitle
		self.shopURL = shopURL

		# initialize all variables with data webscraped from Product page
		self.wscrape_all()


	def __repr__(self):
		"""returns a printable representation of the product"""
		return pprint.pformat(vars(self), indent=4)


	def foo(self):
		"""abstract function"""
		raise NotImplementedError('subclasses must override this function!')


	def wscrape_title(self, soup):
		raise NotImplementedError()

	def wscrape_price(self):
		raise NotImplementedError()

	def wscrape_nSales(self):
		raise NotImplementedError()

	def wscrape_nStock(self):
		raise NotImplementedError()

	def wscrape_rating(self):
		raise NotImplementedError()

	def wscrape_shopTitle(self):
		raise NotImplementedError()

	def wscrape_shopURL(self):
		raise NotImplementedError()



	def wscrape_all(self):
		""" web scrapes various data from the Product page"""
		
		headers = {
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'GET',
			'Access-Control-Allow-Headers': 'Content-Type',
			'Access-Control-Max-Age': '3600',
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
		}

		req = requests.get(self.url, headers)
		soup = BeautifulSoup(req.content, 'html.parser')

		self.title = self.wscrape_title(soup)
		self.price = self.wscrape_price(soup)
		self.nSales = self.wscrape_nSales(soup)
		self.nStock = self.wscrape_nStock(soup)
		self.rating = self.wscrape_rating(soup)
		self.shopTitle = self.wscrape_shop_title(soup)
		self.shopURL = self.wscrape_shop_url(soup)
		
		print("Page has successfully been webscraped.")

		return



class AmazonProductPage(ProductPage):
	
	def __init__(self, *args, **kwargs):
		super(AmazonProductPage, self).__init__(*args, **kwargs)

	def wscrape_title(self, soup):
		return "lorem"

	def wscrape_price(self, soup):
		return "lorem"

	def wscrape_nSales(self, soup):
		return "lorem"

	def wscrape_rating(self, soup):
		return "lorem"

	def wscrape_nStock(self, soup):
		return "lorem"

	def wscrape_shop_title(self, soup):
		return "lorem"

	def wscrape_shop_url(self, soup):
		return "lorem"


class EbayProductPage(ProductPage):
	pass


class EtsyProductPage(ProductPage):

	def __init__(self, *args, **kwargs):
		super(EtsyProductPage, self).__init__(*args, **kwargs)


	def wscrape_title(self, soup):

		tag = soup.find_all('h1', {'class': 'wt-text-body-03 wt-line-height-tight wt-break-word wt-mb-xs-1'})[0]
		title = tag.text.strip()
		return title


	def wscrape_price(self, soup):

		tag = soup.find_all('p', {'class': 'wt-text-title-03 wt-mr-xs-2'})[0]

		# occassionally there is a span tag. This must be removed
		if(tag.find_all('span')):
			tag.span.decompose()

		price = tag.text.strip()

		return price


	def wscrape_nSales(self, soup):

		starsTag = soup.find_all('a', {'class': 'wt-text-link-no-underline ssh-review-stars-text-decoration-none wt-display-inline-flex-xs wt-align-items-center'})[0]
		nSalesTag = starsTag.parent.previous_sibling.previous_sibling.previous_sibling.previous_sibling
		nSales = nSalesTag.text.strip()

		return nSales


	def wscrape_rating(self, soup):

		starsTag = soup.find_all('a', {'class': 'wt-text-link-no-underline ssh-review-stars-text-decoration-none wt-display-inline-flex-xs wt-align-items-center'})[0]

		starTags = starsTag.find('span').find_all('span')[1].find_all('span', {'class': 'etsy-icon wt-nudge-b-1 wt-icon--smallest'})

		rating = 5 # starting from the fifth star icon
		# we will keep going down the stars until we find a filled in star
		while not starTags[rating-1].find('svg').find('path')['d'].startswith("M20.83,9.15l-6-.52L12.46"):
			rating -= 1

		return rating


	def wscrape_nStock(self, soup):

		return soup.find('div', {'data-buy-box-region': 'price'}).find_all('b')[0].text.strip()


	def wscrape_shop_title(self, soup):

		return soup.find('p', {'class': 'wt-text-body-01 wt-mr-xs-1'}).text.strip()


	def wscrape_shop_url(self, soup):
		
		return soup.find('p', {'class': 'wt-text-body-01 wt-mr-xs-1'}).find('a')['href'].split("?")[0]



def convert_file_to_list(filename):
	"""Reads in a file like links.example.txt and returns a list"""

	items = []

	with open(filename) as f:
		lines = f.readlines()

	for line in lines:

		items.append(line.strip())

	return items


def resolve_product_page(url):
	""" Returns the appropriate ProductPage subclass, fully instantiated.

		amazon.com url will return an AmazonProductPage object
		ebay.com url will return an EbayProductPage object

		:param url:

	"""
	if "www.amazon.com" in url:
		return AmazonProductPage(url)
	elif "www.ebay.com" in url:
		return EbayProductPage(url)
	elif "www.etsy.com" in url:
		return EtsyProductPage(url)
	else:
		raise Exception("Sorry. The domain name you provided is not supported in this moment.")



@dispatch(str)
def webscrape_many(filename):
	"""Webscrape all pages listed out line by line in a file.

		:param filename: The file which contains a list of all
		 the pages that are to be webscraped.
	"""

	products = []

	urls = convert_file_to_list(filename)

	for url in urls:
		# p = EtsyProductPage(url)
		p = resolve_product_page(url)
		products.append(p)

	return products


# @dispatch(list)
# def webscrape_many(urls):
# 	"""Webscrape all pages specified by urls.

# 		:param urls: An array of urls.
# 	"""

# 	products = []

# 	for url in urls:
# 		p = EtsyProductPage(url)
# 		products.append(p)

# 	return products

def foozoo(query, website):
	"""


		:param query: A string representing the search query.
	"""