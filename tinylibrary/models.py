from urlparse import urlparse
from os.path import splitext, basename
from datetime import datetime

from sqlalchemy import event
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from core.isbn import toI13
from core.fetch_book_info import google_books_info
from app import db

def normalize_url(url):
    """prepend 'http://' to url. Ensure there's no non-http(s) scheme."""
    disassembled_url = urlparse(url)
    if disassembled_url.scheme == '':
        url = 'http://' + url
    elif disassembled_url.scheme not in ['http', 'https']:
        raise ValueError('Bad URL scheme')
    return url

# def normalize_img_url(raw_url):
#     url = normalize_url(raw_url)
#     disassembled_url = urlparse(url)
#     filename, file_ext = splitext(basename(disassembled_url.path))
#     imgtypes = '.jpg .jpeg .gif .png .apng .bmp .ico'.split()
#     assert file_ext in imgtypes
#     return url

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn13 = db.Column(db.String(13), info = {'label': 'ISBN'})
    inside_cover_id = db.Column(db.String(30), info = {'label': 'Custom ID'})

    title = db.Column(db.String, info = {'label': 'Title'})
    description = db.Column(db.String, info = {'label': 'Description'})
    thumbnail_url = db.Column(db.String, info = {'label': 'Thumbnail image URL'})

    date_added = db.Column(db.DateTime, default=func.now())

    #TODO: status

    __table_args__ = (
        db.UniqueConstraint('isbn13', 'inside_cover_id', name='_isbn_coverid_uc'),
    )

    def __repr__(self):
        return '<Book isbn13=%r, inside_cover_id=%r, date_added=%r, title=%r>' % (
            self.isbn13, self.inside_cover_id, self.date_added, self.title)

    def append_google_book_data(self):
        if not self.isbn13:
            raise ValueError('No isbn13')
        google_data = google_books_info(self.isbn13)
        self.title = google_data['title']
        self.description = google_data['description']
        self.thumbnail_url = google_data['imageLinks']['smallThumbnail']

        # allow chaining
        return self

    @validates('isbn13')
    def validate_isbn(self, key, isbn_raw):
        """Convert to stripped ISBN13, validating in the process"""
        # raises InvalidIsbn if bad
        return toI13(isbn_raw)

    @validates('thumbnail_url')
    def validate_optional_img_url(self, key, url):
        if url is None:
            return None
        return normalize_url(url)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

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

    def __repr__(self):
        return '<Checkout %r to %r from %r to %r>' % (self.book, self.room, self.checkout_date, self.return_date)
