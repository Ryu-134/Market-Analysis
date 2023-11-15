import requests
import csv
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
print(page.content)

soup = BeautifulSoup(page.content, "html.parser")
title_td = soup.find("h1")
upc_td = soup.find("th", string="UPC").find_next_sibling("td")
price_incl_tax_td = soup.find("th", string="Price (incl. tax)").find_next_sibling("td")
price_excl_tax_td = soup.find("th", string="Price (excl. tax)").find_next_sibling("td")
quantity_available_td = soup.find("th", string="Availability").find_next_sibling("td")
product_description_td = soup.find("div", id="product_description").find_next_sibling("p")
category_td = soup.find("th", string="Product Type").find_next_sibling("td")
rating_td = soup.find("th", string="Number of reviews").find_next_sibling("td")
image_url_td = soup.find("img").get("src")

title = title_td.text
upc = upc_td.text
price_incl_tax = price_incl_tax_td.text
price_excl_tax = price_excl_tax_td.text
quantity_available = quantity_available_td.text
product_description = product_description_td.text
category = category_td.text
rating = rating_td.text

print(f"The URL is: {url}")
print(f"The UPC is: {upc}")
print(f"The title is: {title}")
print(f"The price (incl. tax) is: {price_incl_tax}")
print(f"The price (excl. tax) is: {price_excl_tax}")
print(f"Product availability: {quantity_available}")
print(f"Description: {product_description}")
print(f"Category: {category}")
print(f"Number of Reviews: {rating}")
print(f"Image URL: {image_url_td}")

headers = ["url", "UPC", "title", "price_incl_tax", "price_excl_tax",
           "quantity_available", "product_description", "category", "rating", "image_url_td"]

with open("data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(headers)
    for i in range(len(url)):
        row = [url[i], upc[i], title[i], price_incl_tax[i], price_excl_tax[i],
           quantity_available[i], product_description[i], category[i], rating[i], image_url_td[i]]
        writer.writerow(row)