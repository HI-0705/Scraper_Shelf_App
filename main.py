import os
import japanize_kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from dataprocessor.scraper import scrape_book_info
from dataprocessor.data_analyzer import analyze_book_data
from dataprocessor.data_processor import filter_books, sort_books
from data.database import create_connection, create_table, insert_book


class BookInfoApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Label(text="Book Analysis App", size_hint_y=None, height=80))

        self.filter_input = TextInput(
            hint_text="Enter filter keyword", size_hint_y=None, height=80
        )
        layout.add_widget(self.filter_input)

        self.sort_input = TextInput(
            hint_text="Enter sort key", size_hint_y=None, height=80
        )
        layout.add_widget(self.sort_input)

        layout.add_widget(
            Button(
                text="Scrape Book Info",
                size_hint_y=None,
                height=80,
                on_press=self.on_scrape_button_press,
            )
        )

        scroll_view = ScrollView()
        self.result_layout = GridLayout(cols=1, size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter("height"))
        scroll_view.add_widget(self.result_layout)
        layout.add_widget(scroll_view)

        return layout

    def on_scrape_button_press(self, instance):
        url = "http://books.toscrape.com"
        book_info = scrape_book_info(url)
        self.result_layout.clear_widgets()

        if not book_info:
            self.result_layout.add_widget(
                Label(text="Error fetching book information.")
            )
            return

        filter_keyword = self.filter_input.text.lower()
        filtered_books = filter_books(book_info, filter_keyword)

        sort_key = self.sort_input.text
        sorted_books = sort_books(filtered_books, sort_key)

        database_dir = "./data"
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)
        database = os.path.join(database_dir, "books.db")

        conn = create_connection(database)
        if conn is not None:
            create_table(conn)
            for book in sorted_books:
                insert_book(conn, (book["title"], book["price"], book["rating"]))
            conn.close()

        for book in sorted_books:
            self.result_layout.add_widget(
                Label(
                    text=f"Title: {book['title']}, Price: {book['price']}, Rating: {book['rating']}",
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


if __name__ == "__main__":
    BookInfoApp().run()
