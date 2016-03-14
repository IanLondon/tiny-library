from tinylibrary import app
# from tinylibrary import app, db
#
# from tinylibrary.models import Book, Room, Checkout
#
#
# def init_db():
#     db.create_all()
#     print 'created tables'
#
# def populate_db():
#     book1 = Book(isbn13='7796594424423', inside_cover_id='A')
#     book2 = Book(isbn13='9781491946008') # Fluent Python book
#     book2.append_google_book_data()
#
#     room1 = Room(id='1', name='Ms Foo')
#     room2 = Room(id='2', name='Mr Spam')
#
#     co1 = Checkout(book=book1, room=room1)
#     co2 = Checkout(book=book2, room=room2)
#
#     for rec in (book1, book2, room1, room2, co1, co2):
#         db.session.add(rec)
#
#     db.session.commit()
#     print 'added some data'
#
# def reset_db():
#     db.drop_all()
#     print 'deleted tables'
#     init_db()
#     populate_db()

if __name__ == '__main__':
    app.run(debug=True)
