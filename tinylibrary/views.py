from flask import render_template, request

from app import app
from models import Book, Room, Checkout

@app.route('/books/')
def show_books():
    return render_template('show_books.html', books=Book.query.all())

# inside_cover_id is optional
@app.route('/books/<isbn>', methods=['GET','POST'])
@app.route('/books/<isbn>/<inside_cover_id>', methods=['GET','POST'])
def single_book(isbn=None, inside_cover_id=None):
    print 'DEBUG: got single book ', isbn, inside_cover_id
    if request.method == 'GET':
        return 'GET not implemented!'
    if request.method == 'POST':
        return 'Post not implemented!'
