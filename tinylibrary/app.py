from database import db
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from views import add_books, books, checkout
from views import tinylibrary_app
from models import Book, Room, Checkout

import urlparse
import os
from datetime import datetime

TINYLIBRARY_SQLITE3_PATH = '/tmp/tinylibrary.db'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TINYLIBRARY_SQLITE3_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #XXX:???
    app.config.from_pyfile('secrets.py')
    db.init_app(app)
    app.register_blueprint(tinylibrary_app)
    return app

def init_db(app):
    with app.app_context():
        db.create_all()
    print 'created tables'

def populate_db(app):
    book1 = Book(isbn13='7796594424423', title='foo', inside_cover_id='A')
    book2 = Book(isbn13='9781491946008', title='fluent python') # Fluent Python book
    # book2.append_google_book_data() # too slow sometimes...

    room1 = Room(id='1', name='Ms Foo')
    room2 = Room(id='2', name='Mr Spam')

    co1 = Checkout(book=book1, room=room1, return_date=datetime.now())
    co2 = Checkout(book=book2, room=room2)

    with app.app_context():
        for rec in (book1, book2, room1, room2, co1, co2):
            db.session.add(rec)
            print repr(rec), 'added'

        db.session.commit()
    print 'added some data'

if __name__ == '__main__':
    app = create_app()
    #Because this is just a demonstration we set up the database like this.
    if not os.path.isfile(TINYLIBRARY_SQLITE3_PATH):
        print "no database found. making one..."
        init_db(app)
        populate_db(app)
    app.run(debug=True)
