from flask import Flask
from models import db, Book, Room, Checkout
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tinylibrary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #XXX:???

db.init_app(app)

def init_db(add_stuff=False):
    with app.app_context():
        db.create_all()
        if add_stuff:
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

@app.route('/')
def test_output():
    print Book.query.all()
    return ' '.join([b.isbn13 for b in Book.query.all()])

if __name__ == '__main__':
    app.run(debug=True)
