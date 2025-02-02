import os
import japanize_kivy
from kivy.config import Config

Config.set("graphics", "width", "1000")
Config.set("graphics", "height", "800")
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.togglebutton import ToggleButtonBehavior
from kivy.uix.spinner import Spinner
from dataprocessor.scraper import scrape_book_info, scrape_categories
from dataprocessor.data_analyzer import analyze_book_data
from dataprocessor.data_processor import filter_books, sort_books
from dataprocessor.graph import plot_book_data
from dataprocessor.database import create_connection, create_table, insert_book


class BookInfoApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Label(text="Book Analysis App", size_hint_y=None, height=80))

        self.filter_input = TextInput(
            hint_text="Enter filter keyword", size_hint_y=None, height=80
        )
        layout.add_widget(self.filter_input)

        sort_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=80)
        self.sort_key = "title"

        def on_sort_key_select(instance):
            self.sort_key = instance.text.lower()

        title_radio = ToggleButton(text="Title", group="sort", state="down")
        title_radio.bind(on_release=on_sort_key_select)
        sort_layout.add_widget(title_radio)

        price_radio = ToggleButton(text="Price", group="sort")
        price_radio.bind(on_release=on_sort_key_select)
        sort_layout.add_widget(price_radio)

        rating_radio = ToggleButton(text="Rating", group="sort")
        rating_radio.bind(on_release=on_sort_key_select)
        sort_layout.add_widget(rating_radio)

        layout.add_widget(sort_layout)

        self.category_spinner = Spinner(
            text="Select Category",
            values=("All",),
            size_hint_y=None,
            height=80,
        )
        layout.add_widget(self.category_spinner)

        layout.add_widget(
            Button(
                text="Scrape Book Info",
                size_hint_y=None,
                height=80,
                on_press=self.on_scrape_button_press,
            )
        )

        layout.add_widget(
            Button(
                text="Show Graph",
                size_hint_y=None,
                height=80,
                on_press=self.on_show_graph_button_press,
            )
        )

        scroll_view = ScrollView()
        self.result_layout = GridLayout(cols=1, size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter("height"))
        scroll_view.add_widget(self.result_layout)
        layout.add_widget(scroll_view)

        self.load_categories()

        return layout

    def load_categories(self):
        categories = scrape_categories()
        if categories:
            self.category_spinner.values = ("All",) + tuple(categories)

    def on_scrape_button_press(self, instance):
        book_info = scrape_book_info()
        self.result_layout.clear_widgets()

        if not book_info:
            self.result_layout.add_widget(
                Label(text="Error fetching book information.")
            )
            return

        filter_keyword = self.filter_input.text.lower()
        filtered_books = filter_books(book_info, filter_keyword)

        selected_category = self.category_spinner.text
        if selected_category != "All":
            filtered_books = [book for book in filtered_books if book["category"] == selected_category]

        sorted_books = sort_books(filtered_books, self.sort_key)

        database_dir = "./data"
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)
        database = os.path.join(database_dir, "books.db")

        conn = create_connection(database)
        if conn is not None:
            create_table(conn)
            for book in sorted_books:
                insert_book(conn, (book["title"], book["price"], book["rating"], book["category"]))
            conn.close()

        for book in sorted_books:
            self.result_layout.add_widget(
                Label(
                    text=f"Title: {book['title']}, Price: {book['price']}, Rating: {book['rating']}, Category: {book['category']}",
                    size_hint_y=None,
                    height=40,
                    halign="left",
                    text_size=(self.result_layout.width, None),
                )
            )

        analysis_result = analyze_book_data(sorted_books)
        self.result_layout.add_widget(
            Label(text=analysis_result, size_hint_y=None, height=40)
        )

        self.book_info = sorted_books

    def on_show_graph_button_press(self, instance):
        if hasattr(self, "book_info"):
            plot_book_data(self.book_info)


if __name__ == "__main__":
    BookInfoApp().run()
