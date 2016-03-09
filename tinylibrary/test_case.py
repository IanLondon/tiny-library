# Run with `python -m unittest -v test_case` for verbose output
from flask import Flask, url_for
import unittest
from flask.ext.testing import TestCase
from sqlalchemy.exc import IntegrityError

from app import db
from models import *
import views

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

        b1 = Book('4848484848484','999')
        b2 = Book('4848484848484','999')
        db.session.add(b1)
        db.session.add(b2)
        self.assertRaises(IntegrityError, db.session.commit)

if __name__ == '__main__':
    unittest.main()
