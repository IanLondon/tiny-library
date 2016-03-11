from app import app, db

from models import Book, Room, Checkout
from views import *

def clear_db():
    db.drop_all()
    print 'deleted tables'

def init_db():
    db.create_all()
    print 'created tables'

def populate_db():
    book1 = Book(isbn13='7796594424423', inside_cover_id='A')
    book2 = Book(isbn13='9702999994186')
    book_info = {'isbn13':'9781491946008',
    "thumbnail_url": "https://books.google.com/books/content?id=kgrXoAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api",
    'title':'fluent python'}
    book3 = Book(**book_info)


    room1 = Room(id='1', name='Ms Foo')
    room2 = Room(id='2', name='Mr Spam')

    co1 = Checkout(book=book1, room=room1)
    co2 = Checkout(book=book2, room=room2)

    for rec in (book1, book2, book3, room1, room2, co1, co2):
        db.session.add(rec)

    db.session.commit()
    print 'added some data'

if __name__ == '__main__':
    app.run(debug=True)
