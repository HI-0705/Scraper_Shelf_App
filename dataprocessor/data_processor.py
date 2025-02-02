def filter_books(book_info, keyword):
    filtered_books = [
        book for book in book_info if keyword.lower() in book["title"].lower()
    ]
    return filtered_books


def sort_books(books, key):
    if key == "title":
        return sorted(books, key=lambda x: x.get("title", "").lower())
    elif key == "price":
        return sorted(
            books,
            key=lambda x: float(
                x.get("price", "").replace("£", "").replace("Â", "").strip()
            ),
        )
    elif key == "rating":
        rating = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }
        return sorted(books, key=lambda x: rating.get(x.get("rating", "Zero"), 0))
    elif key == "category":
        return sorted(books, key=lambda x: x.get("category", "").lower())
    else:
        return books
