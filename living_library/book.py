from datetime import datetime
import random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from living_library.auth import login_required
from living_library.data.database import db_session
from living_library.data.models import Book, User
from living_library.data.static.genre import Genre
from living_library.data.static.book_state import BookState
from living_library.utility.utils import build_uri, convert_book, convert_genre

PER_PAGE = 10
PER_ROW = 4

bp = Blueprint('book', __name__)

@bp.route('/')
def index():
    
    page = request.args.get('page', 1, type=int)
    query = build_query(request.args, filter=True, additions=True)
    books = query.paginate(page=page, per_page=PER_PAGE, error_out=False)
    users = (User.query.with_entities(User.username).all())
    
    for book in books.items: convert_book(book[0])

    books.items = build_row(books.items)
    
    return render_template('book/index.html', rows=books.items, pagination=books, users=users, genres=list(Genre))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        image_url = request.form['image_url']
        genre = request.form['genre']
        error = None

        if not title: error = 'Title is required'
        elif not author: error = 'Author is required'
        elif not genre: error = 'Genre is required'

        if error is not None: flash(error)
        else:
            book = Book(title=title, author=author, image_url=image_url, genre=genre, user_id=g.user.id, uri = build_uri(g.user.id, title), created=datetime.now())
            db_session.add(book)
            db_session.commit()
            return redirect(url_for('book.index'))
    
    return render_template('book/create.html', genres=list(Genre))

def get_book(idOrUri, check_author=True):
    book = Book.query.filter((Book.id == idOrUri) | (Book.uri == idOrUri)).join(User, User.id == Book.user_id).first()

    if book is None:
        abort(404, f"Post id {idOrUri} doesn't exist")

    if check_author and book.user_id != g.user.id:
        abort(403)

    return book

@bp.route('/<uri>/update', methods=('GET', 'POST'))
@login_required
def update(uri):
    book = get_book(uri)

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        image_url = request.form['image_url']
        genre = request.form['genre']
        error = None

        if not title: error = 'Title is required'
        elif not author: error = 'Author is required'
        elif not genre: error = 'Genre is required'

        if error is not None: flash(error)
        else:
            book.title = title
            book.author = author
            book.image_url = image_url
            book.genre = genre
            book.uri = build_uri(book.user_id, book.title)
            db_session.add(book)
            db_session.commit()
            return redirect(url_for('book.index'))
    
    return render_template('book/update.html', book=book, genres=list(Genre))

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    book = get_book(id)
    db_session.delete(book)
    db_session.commit()
    return redirect(url_for('book.index'))

@bp.route('/randomize', methods=('GET','POST'))
@login_required
def randomize():
    if request.method == 'POST':
        id = request.form['id']

        book = get_book(id, check_author=False)
        book.state = BookState.READING.id
        db_session.add(book)
        db_session.commit()
        return redirect(url_for('book.index'))
    return render_template('book/random_book.html')

@bp.route('/card-display', methods=('GET',))
def card_display():
    query = build_query(request.args, additions=True, filter=True)

    books = query.all()

    random.shuffle(limit_books(2,books))

    selected_book = random.choice(books)
    selected_book[0].genre = convert_genre(selected_book[0].genre)
    
    return render_template('book/card-display.html', book=selected_book)

def build_row(books):
    new_list = []
    temp = []
    for index, book in enumerate(books):
        if index > 0 and index % PER_ROW == 0:
            new_list.append(temp.copy())
            temp.clear()
        temp.append(book)

    if len(temp) > 0: new_list.append(temp.copy())
    return new_list

def build_query(args, filter=False, additions=False):
    query = (Book.query.join(User, User.id == Book.user_id)
             .order_by(Book.created.desc()))
    
    if filter: query = build_filter(query, args)
    if additions: query = build_additions(query)

    return query

def build_additions(query):
    return query.add_columns(User.username)

def build_filter(query, args):
    user = args.get('user', type=str)
    genre = args.get('genre', type=int)
    state = args.get('state', type=int)

    criteria = build_criteria(user=(User.username, user),genre=(Book.genre, genre),state=(Book.state, state))
    
    return query.filter(*criteria)
    
def build_criteria(**kwargs):
    criteria = []
    for k, val in kwargs.items():
        if val[1] is not None:
            criteria.append(val[0] == val[1])
    return criteria

def limit_books(limit, books):
    matches = {}
    limited_books = []
    for book in books:
        value = matches.get(book[1])
        if value is not None and value < limit:
            limited_books.append(book)
            matches[book[1]] = value + 1
        elif value is None:
            limited_books.append(book)
            matches[book[1]] = 1

    return limited_books