from app import app, db

from models import Book, Room, Checkout
from views import *

def init_db():
    db.create_all()
    print 'created tables'

def populate_db():
    book1 = Book('3232323232154','A')
    book2 = Book('3213216546548')

    room1 = Room('1', 'Ms Foo')
    room2 = Room('2', 'Mr Spam')

    co1 = Checkout(book1, room1)
    co2 = Checkout(book2, room2)

    for rec in (book1, book2, room1, room2, co1, co2):
        db.session.add(rec)

    db.session.commit()
    print 'added some data'

if __name__ == '__main__':
    app.run(debug=True)
