from tinylibrary.database import db
from tinylibrary.app import create_app
from tinylibrary.models import Book, Room, Checkout, Person

from sqlalchemy.sql import func

app = create_app()
db.init_app(app)

# so you don't have to do `with app.app_context():` all the time:
ctx = app.test_request_context()
ctx.push()
