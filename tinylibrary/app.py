from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tinylibrary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #XXX:???
# db.app = app
from models import db, Book, Room, Checkout
db.init_app(app)


# def init_db():
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
