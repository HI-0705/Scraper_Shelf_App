import matplotlib.pyplot as plt


def plot_book_data(book_info):
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    sorted_books = sorted(
        book_info, key=lambda x: rating_map.get(x["rating"], 0), reverse=True
    )

    titles = [book["title"] for book in sorted_books]
    prices = [
        float(book["price"].replace("£", "").replace("Â", "").strip())
        for book in sorted_books
    ]
    ratings = [rating_map[book["rating"]] for book in sorted_books]

    fig, ax1 = plt.subplots()

    color = "tab:blue"
    ax1.set_xlabel("Books")
    ax1.set_ylabel("Price(£)", color=color)
    ax1.bar(titles, prices, color=color)
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.set_xticks(range(len(titles)))
    ax1.set_xticklabels(titles, rotation=90, ha="right")

    ax2 = ax1.twinx()
    color = "tab:red"
    ax2.set_ylabel("Rating", color=color)
    ax2.plot(range(len(titles)), ratings, color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    fig.tight_layout()
    plt.show()
