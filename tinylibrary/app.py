from flask import Flask, render_template, request
from models import db, Book, Room, Checkout
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tinylibrary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #XXX:???

db.init_app(app)

def init_db(add_stuff=False):
    with app.app_context():
        db.create_all()
        if add_stuff:
            book1 = Book('3232323232154','A')
            book2 = Book('3213216546548')

            room1 = Room('1', 'Ms Foo')
            room2 = Room('2', 'Mr Spam')

            co1 = Checkout(book1, room1)
            co2 = Checkout(book2, room2)

            for rec in (book1, book2, room1, room2, co1, co2):
                db.session.add(rec)

            db.session.commit()
            print 'added some data'

##########
# Routes #
##########

@app.route('/books/', methods=['GET','POST','DELETE'])
def show_books():
    return render_template('show_books.html', books=Book.query.all())

# innercover_id is optional
@app.route('/books/<isbn>', methods=['GET','POST','DELETE'])
@app.route('/books/<isbn>/<inside_cover_id>', methods=['GET','POST','DELETE'])
def single_book(isbn=None, inside_cover_id=None):
    print 'DEBUG: got single book ', isbn, inside_cover_id
    if request.method == 'GET':
        return 'GET not implemented!'
    if request.method == 'POST':
        return 'Post not implemented!'
    if request.method == 'DELETE':
        return 'Delete not implemented!'


if __name__ == '__main__':
    app.run(debug=True)
