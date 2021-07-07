# coding: utf-8

from ecompy import EtsyProductPage, convert_file_to_list, webscrape_many



# example 1

products = webscrape_many('links.example.txt')
print(products)
print("-"*200)



# example 2

urls = convert_file_to_list('links.example.txt')
products = webscrape_many(urls)
print(products)
print("-"*200)