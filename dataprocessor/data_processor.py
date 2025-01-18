def filter_books(book_info, keyword):
    filtered_books = [
        book for book in book_info if keyword.lower() in book["title"].lower()
    ]
    return filtered_books


def sort_books(books, key):
    return sorted(books, key=lambda x: x.get(key, ""))
