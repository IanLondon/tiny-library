# Run with `python -m pytest -v tests` from parent directory
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

from tinylibrary.models import Book, Room, Checkout
from tinylibrary.core.isbn import InvalidIsbn, randIsbn10, randIsbn13
from tinylibrary.app import create_app
from tinylibrary.database import db

class DumbTest(TestCase):

    SQLALCHEMY_DATABASE_URI = 'sqlite://' #this is the same as :memory:
    TESTING = True

    def create_app(self):
        app = create_app()
        # db = SQLAlchemy(app)
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

    def test_book_isbn10(self):
        b = Book(isbn13=randIsbn10())
        db.session.add(b)
        db.session.commit()

    def test_book_isbn_validation(self):
        self.assertRaises(InvalidIsbn, Book, isbn13='123')

if __name__ == '__main__':
    unittest.main()
