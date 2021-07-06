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



filename = 'etsy-chess.txt'

with open(filename) as f:
	hrefs = f.readlines()

for href in hrefs:

	href = href.strip()

	ws_product(href)

	# print('\n'*2)






	
