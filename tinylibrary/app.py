from database import db, login_manager, bcrypt
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from views import add_books, books, checkout
from views import tinylibrary_app
from models import Book, Room, Checkout, Person, Admin

import urlparse
import os
from datetime import datetime

import logging

def create_app(TINYLIBRARY_SQLITE3_PATH='/tmp/tinylibrary.db'):
    """Create a SQLite-backed app and populates it for local development"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TINYLIBRARY_SQLITE3_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #XXX:???
    app.config.from_pyfile('secrets.py')

    db.init_app(app)

    login_manager.login_view = 'tinylibrary_app.login'
    login_manager.init_app(app)

    bcrypt.init_app(app)

    app.register_blueprint(tinylibrary_app)

    # setup logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

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

    alice = Person(first_name='Alice', middle_name='X', last_name='Aaronson')
    bob = Person(first_name='Bob', last_name='Bobberson')
    inactive_student = Person(first_name='Inactive', last_name='Student', active=False)

    co1 = Checkout(book=book1, room=room1, person=alice, return_date=datetime.now())
    co2 = Checkout(book=book2, room=room2, person=bob)

    admin = Admin(username='admin@admin.com', password='whyyoumakeusread')

    with app.app_context():
        for rec in (book1, book2, room1, room2, alice, bob, inactive_student, co1, co2, admin):
            db.session.add(rec)
            print repr(rec), 'added'

        db.session.commit()
    print 'added some data'

if __name__ == '__main__':
    TINYLIBRARY_SQLITE3_PATH='/tmp/tinylibrary.db'
    app = create_app(TINYLIBRARY_SQLITE3_PATH)
    #Because this is just a demonstration we set up the database like this.
    if not os.path.isfile(TINYLIBRARY_SQLITE3_PATH):
        print "no database found. making one..."
        init_db(app)
        populate_db(app)
    app.run(debug=True)
