
Author:					Ryan Vella Bonello
Project Commenced:		6 July 2021

# Introduction

With EcomPy you can:

- get, compare and monitor competing product information, like price, reviews, or availability
- analyze the cost management for operations
- find great deals for reselling





# urls.txt 

Populate the urls.txt file with a list of product pages (as URLs) separated by new line.

The products must all be from the same website. Choose from the following marketplaces:
	amazon.com
	ebay.com
	etsy.com

See urls.example.txt as a reference.


# webscraping product details for a given URL

Suppose you want to get the details of a product on Amazon.com. Do the following:

	product = AmazonProductPage("https://www.amazon.com/Some-Cool-Product/dp/B096K5S44Z")


# webscraping product details for multiple URLs

	urls = convert_file_to_list('urls.txt')
	products = webscrape_many(urls)


# webscraping product details of multiple results for a given search

Suppose you want to get the details of all the listings returned from searching "Greek chess sets" on Ebay.com







# Marketplaces

## Amazon
As a top eCommerce site, Amazon is one of the biggest databases for products, reviews, retailers, and market trends. It’s a web scraping gold mine.

Amazon does not encourage scraping its website. This is why the structure of the pages differs if the products fall into different categories. The website includes some basic anti-scraping measures that could prevent you from getting your much-needed information. Besides this, Amazon can find out if you’re using a bot to scrape it and will definitely block your IP.

Read: https://limeproxies.netlify.app/blog/the-top-5-guidelines-for-scraping-amazon-safely


## Ebay

## Etsy