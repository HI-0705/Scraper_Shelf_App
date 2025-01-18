import requests
from bs4 import BeautifulSoup


def scrape_book_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("div", class_="book")
        book_info = []

        for book in books:
            title = book.find("h2").text
            author = book.find("p", class_="author").text
            book_info.append({"title": title, "author": author})

        return book_info
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
