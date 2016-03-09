from sqlalchemy.orm import validates
from datetime import datetime

from core import isbn
from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn13 = db.Column(db.String(13))
    inside_cover_id = db.Column(db.String(20))
    date_added = db.Column(db.DateTime)
    #TODO: status

    __table_args__ = (
        db.UniqueConstraint('isbn13', 'inside_cover_id', name='_isbn_coverid_uc'),
    )

    def __init__(self, isbn13, inside_cover_id=None):
        # XXX: is this a good way to do validation? Should I use @validates instead?
        # isbn13 = isbn.toI13(isbn13) # raises InvalidIsbn if bad
        self.isbn13 = isbn13
        self.inside_cover_id = inside_cover_id
        self.date_added = datetime.utcnow()
        # TODO: is this where a call to get Google Books data should go? NO.
        # No, no, no. That should only happen when a book is committed!
        # I don't want to fetch data when I do `b = Book(blah, blah)`!!

    def __repr__(self):
        return '<Book ISBN:%r inside_cover_id:%r added:%r>' % (self.isbn13, self.inside_cover_id, self.date_added)

    @validates('isbn13')
    def validate_isbn(self, key, isbn_raw):
        """Convert to stripped ISBN13, validating in the process"""
        # raises InvalidIsbn if bad
        return isbn.toI13(isbn_raw)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Room id:%r name:%r>' % (self.id, self.name)

class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkout_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book',
        backref=db.backref('checkouts', lazy='dynamic'))

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room',
        backref=db.backref('checkouts', lazy='dynamic'))

    def __init__(self, book, room, checkout_date=None):
        self.book = book
        self.room = room
        if checkout_date is None:
            checkout_date = datetime.utcnow()
        self.checkout_date = checkout_date

    def __repr__(self):
        return '<Checkout %r to %r from %r to %r>' % (self.book, self.room, self.checkout_date, self.return_date)

#TODO: IsbnCache table
