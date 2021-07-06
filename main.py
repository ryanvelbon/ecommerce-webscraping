# coding: utf-8

from ecompy import EtsyProductPage


filename = 'links.example.txt'

with open(filename) as f:
	hrefs = f.readlines()

for href in hrefs:

	href = href.strip()

	p = EtsyProductPage(href)

	print(p)

	print('\n'*2)






	
