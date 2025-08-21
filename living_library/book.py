from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from living_library.auth import login_required
from living_library.data.database import db_session
from living_library.data.models import Book, User
from living_library.utility.utils import build_uri

bp = Blueprint('book', __name__)

@bp.route('/')
def index():
    books = (Book.query.join(User, User.id == Book.user_id)
             .order_by(Book.created.desc())
             .add_columns(User.username, Book.id, Book.title, Book.author, Book.genre, Book.image_url)
             .all())
    return render_template('book/index.html', books=books)

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
            book = Book(title=title, author=author, image_url=image_url, genre=genre, user_id=g.user.id, uri = build_uri(g.user.id, title))
            db_session.add(book)
            db_session.commit()
            return redirect(url_for('book.index.html'))
    
    return render_template('book/create.html')
        


def get_book(idOrUri, check_author=True):
    book = Book.query.filter((Book.id == idOrUri) | (Book.uri == idOrUri)).join(User, User.id == Book.user_id).first()

    if book is None:
        abort(404, f"Post id {idOrUri} doesn't exist")

    if check_author and book.user_id != g.user.id:
        abort(403)

    return book