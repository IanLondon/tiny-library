from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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
        # TODO: ISBN10 conversion, ISBN13 validation. Use core/isbn.py
        self.isbn13 = isbn13
        self.inside_cover_id = inside_cover_id
        self.date_added = datetime.utcnow()

    def __repr__(self):
        return '<Book ISBN:%r inside_cover_id:%r added:%r>' % (self.isbn13, self.inside_cover_id, self.date_added)

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
