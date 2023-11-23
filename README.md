# Book Data Scraper

This project is a Python script for scraping book information and images from a website and saving the data into a CSV file.

## Installation

To run this script, you'll need Python installed on your system. This script was developed with Python 3.12.

First, clone this repository to your local machine:

git clone https://github.com/Ryu-134/Market-Analysis.git

Then, navigate to the project directory and install the required packages:

cd Market-Analysis

pip install -r requirements.txt

## Running the Script

To run the script, use the following command:

python main.py

The script will start scraping data from the website and save book information into a CSV file named `books_data.csv`. Images of the books will be downloaded to a folder named `book_images`.

## Output

- `books_data.csv`: Contains the scraped book data, including URLs, titles, prices, availability, descriptions, categories, ratings, and image URLs.
- `book_images/`: Directory containing downloaded images of the books.

## Note

Ensure you have permission to scrape the website and adhere to its `robots.txt` file and terms of service.