import matplotlib.pyplot as plt


def plot_book_data(book_info):
    titles = [book["title"] for book in book_info]
    prices = [
        float(book["price"].replace("£", "").replace("Â", "").strip())
        for book in book_info
    ]
    ratings = [book["rating"] for book in book_info]

    fig, ax1 = plt.subplots()

    color = "tab:blue"
    ax1.set_xlabel("Books")
    ax1.set_ylabel("Price(£)", color=color)
    ax1.bar(titles, prices, color=color)
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.set_xticklabels(titles, rotation=90, ha="right")

    ax2 = ax1.twinx()
    color = "tab:red"
    ax2.set_ylabel("Rating", color=color)
    ax2.plot(titles, ratings, color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    fig.tight_layout()
    plt.show()
