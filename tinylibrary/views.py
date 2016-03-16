from database import db

from flask import render_template, request, redirect, url_for, flash
from flask.blueprints import Blueprint
from flask_wtf import Form
from wtforms.fields.html5 import URLField, DateTimeField
from wtforms import StringField, HiddenField, validators
from datetime import datetime
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from models import Book, Room, Checkout, Person
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
    room = QuerySelectField(query_factory=lambda:db.session.query(Room), allow_blank=False)
    person = QuerySelectField(query_factory=lambda:db.session.query(Person).filter(Person.active), allow_blank=False)
    # book is assigned in the view

class ReturnForm(Form):
    return_date = DateTimeField(format='%Y/%m/%d %H:%M',validators=[validators.DataRequired()], default=datetime.today())


#########
# Views #
#########

@tinylibrary_app.route('/add_books/', methods=['GET','POST'])
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

    # No args
    return render_template('show_books.html', books=Book.query.all())

@tinylibrary_app.route('/checkout/<int:book_id>', methods=['GET','POST'])
def checkout(book_id):
    selected_book = Book.query.get_or_404(book_id)
    if not selected_book.is_available():
        flash('"%s" (ID: %s) is already checked out. It must be returned before you can check it out.' % (selected_book.title, selected_book.inside_cover_id), category='error')
        return redirect(url_for('.books'))

    checkout_form = CheckoutForm()
    if checkout_form.validate_on_submit():
        new_checkout = Checkout(checkout_date=checkout_form.checkout_date.data, book=selected_book, person=checkout_form.person.data, room=checkout_form.room.data)

        db.session.add(new_checkout)
        db.session.commit()

        flash('Checked out %s to Room %s' % (selected_book.title, checkout_form.room.data.id), category='success')
        return redirect(url_for('.books'))
    # return render_template('checkout.html', book=bk, people=people, rooms=rooms)
    return render_template('checkout.html', book=selected_book, form=checkout_form)

@tinylibrary_app.route('/return/<int:book_id>', methods=['GET','POST'])
def return_book(book_id):
    selected_book = Book.query.get_or_404(book_id)
    if selected_book.is_available():
        flash('"%s" (ID: %s) is not checked out. It cannot be returned.' % (selected_book.title, selected_book.inside_cover_id), category='error')
        return redirect(url_for('.books'))
    return_form = ReturnForm()
    if return_form.validate_on_submit():
        open_checkout = selected_book.open_checkout()
        open_checkout.return_date = return_form.return_date.data
        db.session.add(open_checkout)
        db.session.commit()
        flash('Returned %s (ID: %s)' % (selected_book.title, selected_book.inside_cover_id), category='success')
        return redirect(url_for('.books'))
    return render_template('return_book.html', book=selected_book, form=return_form)
