import requests
import csv
import os
from bs4 import BeautifulSoup

# Initialize Arrays to load data into
(urls, upcs, titles, price_incl_taxs, price_excl_taxs, quantity_availables, product_descriptions,
 categories, ratings, image_urls) = ([], [], [], [], [], [], [], [], [], [])

# Function to download and save the image file for the book
def download_image(image_url, upc, folder='book_images'):
    # Create a folder for book images if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Use the UPC to create a valid filename
    filename = f"{upc}.jpg"
    # Combine the folder name and the filename for local path
    file_path = os.path.join(folder, filename)
    # Download and save the image
    response = requests.get(image_url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

# Function to get data from URL to scrape and append to lists
def scrape_book_data(book_url):
    response = requests.get(book_url)
    book_page_soup = BeautifulSoup(response.content, "html.parser")

    # Locate all necessary data and extract
    title_td = book_page_soup.find("h1").string
    upc_td = book_page_soup.find("th", string="UPC").find_next_sibling("td").string
    price_incl_tax_td = book_page_soup.find("th", string="Price (incl. tax)").find_next_sibling("td").string
    price_excl_tax_td = book_page_soup.find("th", string="Price (excl. tax)").find_next_sibling("td").string
    quantity_available_td = book_page_soup.find("th", string="Availability").find_next_sibling("td").string
    product_description_td = book_page_soup.find("div", id="product_description").find_next_sibling("p").string \
        if book_page_soup.find('div', id='product_description') else 'No description'
    category_elements = book_page_soup.find_all('a')
    category_td = [elem.get_text().strip() for elem in category_elements if 'category/books/' in elem.get('href')][-1]
    rating_td = book_page_soup.find("p", class_="star-rating").get("class")[-1]
    image_relative_url = book_page_soup.find("img")["src"]
    image_url_td = "https://books.toscrape.com" + image_relative_url.replace("../..", "")

    # Append data to lists
    urls.append(book_url)
    upcs.append(upc_td)
    titles.append(title_td)
    price_incl_taxs.append(price_incl_tax_td)
    price_excl_taxs.append(price_excl_tax_td)
    quantity_availables.append(quantity_available_td)
    product_descriptions.append(product_description_td)
    categories.append(category_td)
    ratings.append(rating_td)
    # Download and save the image
    image_urls.append(image_url_td)
    download_image(image_url_td, upc_td)

# Function to scrape books from a category page
def scrape_category(category_url):
    while True:
        response = requests.get(category_url)
        category_soup = BeautifulSoup(response.content, features="html.parser")
        books = category_soup.select("h3 > a")
        for book in books:
            book_url = book.get("href").replace("../../../", "https://books.toscrape.com/catalogue/")
            scrape_book_data(book_url)
        # Check for additional pages
        next_button = category_soup.select_one("li.next > a")
        if next_button:
            next_page = next_button.get("href")
            category_url = '/'.join(category_url.split('/')[:-1]) + '/' + next_page
        else:
          break

# Scrape categories from main page
main_url = "https://books.toscrape.com/index.html"
main_page = requests.get(main_url)
main_soup = BeautifulSoup(main_page.content, features="html.parser")
category_links = main_soup.select(".side_categories ul li ul li a")

# Scrape all categories
for link in category_links:
    category_url = f"https://books.toscrape.com/{link.get('href')}"
    scrape_category(category_url)

# CSV headers
headers = ["URL", "UPC", "Title", "Price_Incl_Tax", "Price_Excl_Tax",
           "Quantity_Available", "Product_Description", "Category", "Rating", "Image_URL"]

# Write to CSV
with open("books_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    for i in range(len(urls)):
        row = [urls[i], upcs[i], titles[i], price_incl_taxs[i], price_excl_taxs[i],
           quantity_availables[i], product_descriptions[i], categories[i], ratings[i], image_urls[i]]
        writer.writerow(row)