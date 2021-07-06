import urllib.request
from bs4 import BeautifulSoup

class ProductPage():

	def __init__(self, href, title=None, price=None, nSales=None, nStock=None, rating=None, shopTitle=None, shopHref=None):
		if type(self) is ProductPage:
			raise Exception('ProductPage is an abstract class and cannot be instantiated directly')
		self.href = href
		self.title = title
		self.price = price
		self.nSales = nSales
		self.nStock = nStock
		self.rating = rating
		self.shopTitle = shopTitle
		self.shopHref = shopHref


	def details(self):
		"""not an abstract function"""
		print(self.title)


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

	def wscrape_shopHref(self):
		raise NotImplementedError()



	def wscrape_all(self):
		""" web scrapes various data from the Product page"""

		try:
			webURL = urllib.request.urlopen(self.href)
		except urllib.error.HTTPError:
			print("Error {}. Skipped".format(webURL.getcode()))
			# raise Error
		except:
			print("Something went wrong...not sure what tho...")
			# raise Error

		html = webURL.read()

		soup = BeautifulSoup(html, 'html.parser')

		self.title = self.wscrape_title(soup)
		self.price = self.wscrape_price(soup)
		self.nSales = self.wscrape_nSales(soup)
		self.nStock = self.wscrape_nStock(soup)
		self.rating = self.wscrape_rating(soup)
		self.shopTitle = self.wscrape_shop_title(soup)
		self.shopHref = self.wscrape_shop_href(soup)
		
		print("Scraped 1 product")

		return



class AmazonProductPage(ProductPage):
	pass


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
		# we will keep going down the starts until we find a filled in star
		while not starTags[rating-1].find('svg').find('path')['d'].startswith("M20.83,9.15l-6-.52L12.46"):
			rating -= 1

		return rating


	def wscrape_nStock(self, soup):

		return soup.find('div', {'data-buy-box-region': 'price'}).find_all('b')[0].text.strip()


	def wscrape_shop_title(self, soup):

		return soup.find('p', {'class': 'wt-text-body-01 wt-mr-xs-1'}).text.strip()


	def wscrape_shop_href(self, soup):
		
		return soup.find('p', {'class': 'wt-text-body-01 wt-mr-xs-1'}).find('a')['href'].split("?")[0]