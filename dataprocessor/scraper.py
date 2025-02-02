import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com"


def scrape_book_info():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")
        book_info = []

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating = book.p["class"][1]
            detail_page_url = urljoin(BASE_URL, book.h3.a["href"])

            detail_response = requests.get(detail_page_url)
            detail_response.raise_for_status()
            detail_soup = BeautifulSoup(detail_response.text, "html.parser")
            category_tag = (
                detail_soup.find("ul", class_="breadcrumb").find_all("li")[2].a
            )
            category = category_tag.text if category_tag else "Unknown"

            book_info.append(
                {"title": title, "price": price, "rating": rating, "category": category}
            )

            time.sleep(1)

        return book_info
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def scrape_categories():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        categories = []
        category_elements = soup.find("ul", class_="nav-list").find("ul").find_all("a")
        for category_element in category_elements:
            category_name = category_element.text.strip()
            categories.append(category_name)

        return categories
    except requests.RequestException as e:
        print(f"Error fetching categories: {e}")
        return []
