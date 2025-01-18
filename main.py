import kivy
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


class BookInfoApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Label(text="Book Analysis App"))

        self.filter_input = TextInput(hint_text="Enter filter keyword")
        layout.add_widget(self.filter_input)

        self.sort_input = TextInput(hint_text="Enter sort key")
        layout.add_widget(self.sort_input)

        layout.add_widget(
            Button(text="Scrapa Book Info", on_press=self.on_scrape_button_press)
        )

        scroll_view = ScrollView()
        self.result_layout = GridLayout(cols=1, size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter("height"))
        scroll_view.add_widget(self.result_layout)
        layout.add_widget(scroll_view)

        return layout

    def on_scrape_button_press(self, instance):
        url = "http://example.com/books"
        book_info = scrape_book_info(url)
        self.result_layout.clear_widgets()

        if not book_info:
            self.result_layout.add_widget(Label(text="Error fetching data"))
            return

        filter_keyword = self.filter_input.text()
        filtered_books = filter_books(book_info, filter_keyword)

        sort_key = self.sort_input.text
        sort_books = sort_books(filtered_books, sort_key)

        for book in sort_books:
            self.result_layout.add_widget(
                Label(text=f"Title: {book['title']}, Author: {book['author']}")
            )

        analysis_result = analyze_book_data(sort_books)
        self.result_layout.add_widget(Label(text=analysis_result))


if __name__ == "__main__":
    BookInfoApp().run()
