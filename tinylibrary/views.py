from database import db

from flask import render_template, request, redirect, url_for, flash
from flask.blueprints import Blueprint
from flask_wtf import Form
from wtforms.fields.html5 import URLField, DateTimeField
from wtforms import StringField, HiddenField, validators
from datetime import datetime
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from models import Book, Room, Checkout
from validators import ValidateIsbn

tinylibrary_app = Blueprint('tinylibrary_app', __name__,
    template_folder='templates', static_folder='static')


#########
# Forms #
#########

class AddBookForm(Form):
    isbn13 = StringField(label='ISBN', validators=[validators.DataRequired(), ValidateIsbn()])
    inside_cover_id = StringField(label='Custom ID')
    title = StringField()
    description = StringField()
    thumbnail_url = URLField(validators=[validators.url])

class CheckoutForm(Form):
    checkout_date = DateTimeField(format='%Y/%m/%d %H:%M',validators=[validators.DataRequired()], default=datetime.today())
    # room = QuerySelectField(query_factory=Room.query.all, allow_blank=False)
    room = QuerySelectField(query_factory=lambda:db.session.query(Room), allow_blank=False)
    # book is assigned in the view
    # book = QuerySelectField(query_factory=Book.query.all, allow_blank=False)


# BaseModelForm and ModelForm stuff is boilerplate
# for using flask-wtf + wtforms_alchemy together

# BaseModelForm = model_form_factory(Form)
#
# class ModelForm(BaseModelForm):
#     @classmethod
#     def get_session(self):
#         return db.session
#
# class AddBookForm(ModelForm):
#     class Meta:
#         model = Book


#########
# Views #
#########

@tinylibrary_app.route('/add_books', methods=['GET','POST'])
def add_books():
    add_book_form = AddBookForm()
    if add_book_form.validate_on_submit():
        print 'got add book form %s' % add_book_form

        new_book = Book(isbn13=add_book_form.isbn13.data, inside_cover_id=add_book_form.inside_cover_id.data, title=add_book_form.title.data, description=add_book_form.description.data, thumbnail_url=add_book_form.thumbnail_url.data)

        db.session.add(new_book)
        db.session.commit()

        flash('Added ISBN#%s "%s"' % (add_book_form.isbn13.data, add_book_form.title.data), category='success')
        return redirect(url_for('.add_books'))
    if add_book_form.is_submitted():
        flash('There was an error with your submission', category='error')
    return render_template('add_books.html', form=add_book_form)

@tinylibrary_app.route('/books/')
def books():
    # id overrides all other args
    if 'id' in request.args:
        bk = Book.query.get_or_404(request.args.get('id'))
        return render_template('single_book.html', book=bk)
    elif request.args:
        # If there are args that don't include id, filter by all of them
        # TODO: make this more useful/robust, use fuzzy matching on title & description
        return render_template('show_books.html', books=Book.query.filter_by(**request.args.to_dict()).all())
    return render_template('show_books.html', books=Book.query.all())

@tinylibrary_app.route('/checkout/<int:book_id>', methods=['GET','POST'])
def checkout(book_id):
    selected_book = Book.query.get_or_404(book_id)
    checkout_form = CheckoutForm()
    if checkout_form.validate_on_submit():
        new_checkout = Checkout(checkout_date=checkout_form.checkout_date.data, book=selected_book, room=checkout_form.room.data)

        db.session.add(new_checkout)
        db.session.commit()

        flash('Checked out %s to Room %s' % (selected_book.title, checkout_form.room.data.id), category='success')
        return redirect(url_for('.books'))
    # return render_template('checkout.html', book=bk, people=people, rooms=rooms)
    return render_template('checkout.html', book=selected_book, form=checkout_form)
