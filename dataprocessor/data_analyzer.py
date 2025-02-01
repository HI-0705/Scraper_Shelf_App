def analyze_book_data(book_info):
    num_books = len(book_info)
    total_price = sum(float(book["price"][1:].replace("£", "")) for book in book_info)
    average_price = total_price / num_books if num_books > 0 else 0
    return f"Number of books: {num_books}, Average price: {average_price:.2f}"
