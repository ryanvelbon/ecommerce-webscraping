# coding: utf-8


# Input file must be a list of URLs separated by new line
#
# Example of content inside etsy.txt:
#
# https://www.etsy.com/listing/689318491/some-product
# https://www.etsy.com/listing/996572607/another-product
# https://www.etsy.com/listing/689318491/this-is-also-a-product

import json, sys
import urllib.request
from bs4 import BeautifulSoup

def pretty(dict):
	pass

def ws_product_title(soup):

	tag = soup.find_all('h1', {'class': 'wt-text-body-03 wt-line-height-tight wt-break-word wt-mb-xs-1'})[0]
	title = tag.text.strip()

	return title


def ws_product_price(soup):
	""" webscrape the product price"""

	tag = soup.find_all('p', {'class': 'wt-text-title-03 wt-mr-xs-2'})[0]

	# occassionally there is a span tag. This must be removed
	if(tag.find_all('span')):
		tag.span.decompose()

	price = tag.text.strip()

	return price


def ws_product_nSales(soup):

	starsTag = soup.find_all('a', {'class': 'wt-text-link-no-underline ssh-review-stars-text-decoration-none wt-display-inline-flex-xs wt-align-items-center'})[0]
	nSalesTag = starsTag.parent.previous_sibling.previous_sibling.previous_sibling.previous_sibling
	nSales = nSalesTag.text.strip()

	return nSales


def ws_product_rating(soup):

	starsTag = soup.find_all('a', {'class': 'wt-text-link-no-underline ssh-review-stars-text-decoration-none wt-display-inline-flex-xs wt-align-items-center'})[0]

	starTags = starsTag.find('span').find_all('span')[1].find_all('span', {'class': 'etsy-icon wt-nudge-b-1 wt-icon--smallest'})

	rating = 5 # starting from the fifth star icon
	# we will keep going down the starts until we find a filled in star
	while not starTags[rating-1].find('svg').find('path')['d'].startswith("M20.83,9.15l-6-.52L12.46"):
		rating -= 1

	return rating


def ws_product_nStock(soup):

	return soup.find('div', {'data-buy-box-region': 'price'}).find_all('b')[0].text.strip()


def ws_product_shop_title(soup):

	return soup.find('p', {'class': 'wt-text-body-01 wt-mr-xs-1'}).text.strip()


def ws_product_shop_href(soup):
	
	return soup.find('p', {'class': 'wt-text-body-01 wt-mr-xs-1'}).find('a')['href'].split("?")[0]



def ws_product(href):

	try:
		webURL = urllib.request.urlopen(href)
	except urllib.error.HTTPError:
		print("Error {}. Skipped".format(webURL.getcode()))

		# continue
	except:
		print("Something went wrong...not sure what tho...")
		# continue

	html = webURL.read()

	soup = BeautifulSoup(html, 'html.parser')

	title = ws_product_title(soup)
	price = ws_product_price(soup)
	nSales = ws_product_nSales(soup)
	nStock = ws_product_nStock(soup)
	rating = ws_product_rating(soup)
	shopTitle = ws_product_shop_title(soup)
	shopHref = ws_product_shop_href(soup)

	print("Scraped 1 product")

	return


filename = 'etsy-chess.txt'

with open(filename) as f:
	hrefs = f.readlines()

for href in hrefs:

	href = href.strip()

	ws_product(href)

	# print('\n'*2)






	
