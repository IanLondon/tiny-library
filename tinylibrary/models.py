from database import db

from urlparse import urlparse
from os.path import splitext, basename
from datetime import datetime

from sqlalchemy import event
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from core.isbn import toI13
from core.fetch_book_info import google_books_info

def normalize_url(url):
    """prepend 'http://' to url. Ensure there's no non-http(s) scheme."""
    if not url:
        return None
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
    isbn13 = db.Column(db.String(13))
    inside_cover_id = db.Column(db.String(30))

    title = db.Column(db.String)
    description = db.Column(db.String)
    thumbnail_url = db.Column(db.String)

    date_added = db.Column(db.DateTime, default=func.now())

    #TODO: status

    __table_args__ = (
        db.UniqueConstraint('isbn13', 'inside_cover_id', name='_isbn_coverid_uc'),
    )

    def __repr__(self):
        return '<Book id=%s, isbn13=%r, inside_cover_id=%r, date_added=%s, title=%r>' % (
            self.id, self.isbn13, self.inside_cover_id, self.date_added, self.title)

    def append_google_book_data(self):
        if not self.isbn13:
            raise ValueError('No isbn13')
        google_data = google_books_info(self.isbn13)
        self.title = google_data['title']
        self.description = google_data['description']
        self.thumbnail_url = google_data['imageLinks']['thumbnail']

        # allow chaining
        return self

    def is_available(self):
        """True if available, ie true if not currently checked out. False otherwise."""
        return self.checkout.filter(Checkout.return_date == None).count() == 0

    def open_checkout(self):
        """Returns the open Checkout for this book, or None if there's no open checkouts."""
        return self.checkout.filter(Checkout.return_date == None).scalar()

    def last_checked_out(self):
        """Date last checked out, or None if never checked out.
        Doesn't tell you anything about whether it's available or not."""
        return db.session.query(func.max(Checkout.checkout_date)).filter_by(book_id=self.id).scalar()

    def teaser(self, chars=120):
        """Teaser text for description"""
        # TODO: this should probably be a macro or something, it's not specific to this text field only
        if self.description:
            return self.description[:chars]

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

    def __str__(self):
        return '%s - %s' % (self.id, self.name)

class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkout_date = db.Column(db.DateTime, nullable=False, default=func.now())
    return_date = db.Column(db.DateTime)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book',
        backref=db.backref('checkout', lazy='dynamic'))

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room',
        backref=db.backref('checkout', lazy='dynamic'))

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person',
        backref=db.backref('chekout', lazy='dynamic'))

    __table_args__ = (
        db.UniqueConstraint('book_id', 'checkout_date', name='_one_checkout_at_a_time'),
    )

    def __repr__(self):
        return '<Checkout Book ID=%r to room=%r from %s to %s>' % (self.book.id, self.room.id, self.checkout_date, self.return_date)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(60))
    middle_name = db.Column(db.String(60), nullable=True)
    last_name = db.Column(db.String(60))

    active = db.Column(db.Boolean(), default=True, nullable=False)

    date_added = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return '<Person ID=%s, %s %s %s>' % (self.id, self.first_name, self.middle_name, self.last_name)

    def __str__(self):
        return '%s, %s %s (%s)' % (self.last_name, self.first_name, self.middle_name, self.id)
