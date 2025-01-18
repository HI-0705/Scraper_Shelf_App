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
            author = (
                book.find("p", class_="author").text
                if book.find("p", class_="author")
                else "Unknown"
            )
            book_info.append({"title": title, "author": author})

            time.sleep(2)

        return book_info
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
