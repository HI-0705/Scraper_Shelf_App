import requests
from bs4 import BeautifulSoup
import time


def scrape_book_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")
        book_info = []

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating = book.p["class"][1]
            book_info.append({"title": title, "price": price, "rating": rating})

            time.sleep(2)

        return book_info
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
