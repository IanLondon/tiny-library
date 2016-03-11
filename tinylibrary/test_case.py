# Run with `python -m unittest -v test_case` for verbose output
from flask import Flask, url_for
import unittest
from flask.ext.testing import TestCase
from sqlalchemy.exc import IntegrityError

from app import db
from models import *
import views
from core.isbn import InvalidIsbn, randIsbn10, randIsbn13

class DumbTest(TestCase):

    SQLALCHEMY_DATABASE_URI = 'sqlite://' #this is the same as :memory:
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
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

        b1 = Book(same_isbn, same_inner_cover)
        b2 = Book(same_isbn, same_inner_cover)

        db.session.add(b1)
        db.session.add(b2)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_book_isbn_coverid_diff(self):
        """Permit 2 books with same isbn13 as long as inside_cover_ids are different"""

        same_isbn = randIsbn13()

        b1 = Book(same_isbn, '1')
        b2 = Book(same_isbn, '2')

        db.session.add(b1)
        db.session.add(b2)
        db.session.commit()

    def test_book_isbn10(self):
        b = Book(randIsbn10())
        db.session.add(b)
        db.session.commit()

    def test_book_isbn_validation(self):
        self.assertRaises(InvalidIsbn, Book, '123')

    def test_books_info_scraping(self):
        hunger_games_isbn = '9780545586177'
        b = Book(hunger_games_isbn)
        db.session.add(b)
        db.session.commit()
        print "IsbnCache:", IsbnCache.query.all()

if __name__ == '__main__':
    unittest.main()
