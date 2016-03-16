# Run with `python -m pytest -v tests` or `py.test -v tests' from parent directory
from flask import Flask, url_for
import unittest
from flask.ext.testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# from app import db
# from models import *
# import views

# project root is in parent directory
# import os
# import sys
# topdir = os.path.join(os.path.dirname(__file__), "..")
# sys.path.append(topdir)

from tinylibrary.models import Book, Room, Checkout, Person, Admin
from tinylibrary.core.isbn import InvalidIsbn, randIsbn10, randIsbn13
from tinylibrary.app import create_app
from tinylibrary.views import tinylibrary_app
from tinylibrary.database import db

def make_checkout(commit=False):
    bk = Book(isbn13=randIsbn13())
    rm = Room(name='Foo')
    # If checkout_date is null in the constructor,
    # a default value will get added by SQL database
    chk = Checkout(book=bk, room=rm)
    if commit:
        for obj in (bk, rm, chk):
            db.session.add(obj)
        db.session.commit()
    return bk, rm, chk

class ConstraintsTest(TestCase):

    SQLALCHEMY_DATABASE_URI = 'sqlite://' #this is the same as :memory:
    TESTING = True

    def create_app(self):
        # app = create_app()
        app = Flask(__name__)
        db.init_app(app)
        app.register_blueprint(tinylibrary_app)

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        # Make sure old session is removed and a new session is started
        # with each test run
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        """Ensure the test database stays empty"""
        for obj in (Book, Room, Checkout):
            assert len(obj.query.all()) == 0

    def test_book_isbn_coverid_unique(self):
        """Do not permit 2 books with same isbn13 and same inside_cover_id"""

        same_isbn = randIsbn13()
        same_inner_cover = 'ABC'

        b1 = Book(isbn13=same_isbn, inside_cover_id=same_inner_cover)
        b2 = Book(isbn13=same_isbn, inside_cover_id=same_inner_cover)

        db.session.add(b1)
        db.session.add(b2)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_book_isbn_coverid_diff(self):
        """Permit 2 books with same isbn13 as long as inside_cover_ids are different"""

        same_isbn = randIsbn13()

        b1 = Book(isbn13=same_isbn, inside_cover_id='1')
        b2 = Book(isbn13=same_isbn, inside_cover_id='2')

        db.session.add(b1)
        db.session.add(b2)
        db.session.commit()

        assert( len(Book.query.all()) == 2)

    def test_book_isbn10(self):
        b = Book(isbn13=randIsbn10())
        db.session.add(b)
        db.session.commit()

    def test_book_isbn_validation(self):
        self.assertRaises(InvalidIsbn, Book, isbn13='123')

    def test_checkout_date_null(self):
        make_checkout(commit=True)

        # Now try to give the Checkout object a null checkout_date
        chk_sess = Checkout.query.get(1)
        chk_sess.checkout_date = None
        db.session.add(chk_sess)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_checkout_one_at_a_time(self):
        """Test the UniqueConstraint"""
        bk, rm, chk = make_checkout(commit=True)
        chk2 = Checkout(book=bk, room=rm)
        db.session.add(chk2)
        self.assertRaises(IntegrityError, db.session.commit)

if __name__ == '__main__':
    unittest.main()
