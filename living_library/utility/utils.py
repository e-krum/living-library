from flask import url_for

from living_library.data.static.genre import Genre
from living_library.data.static.book_state import BookState

def build_uri(id, value):
    return "{id}-{value}".format(id=id, value=value.replace(' ', '-').lower())

def convert_book(book):
     book.genre = convert_genre(book.genre)
     book.state = convert_book_state(book.state)
     book.url = url_for('book.book_page', uri=book.uri)

def convert_book_state(id):
    for state in list(BookState):
        if state.id == id: return state.title

def convert_genre(id):
        for genre in list(Genre):
            if genre.id == id: return genre.title

