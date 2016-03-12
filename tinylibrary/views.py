from flask import render_template, request, redirect, url_for, flash
from flask_wtf import Form
from wtforms.fields.html5 import URLField
from wtforms import StringField, HiddenField, validators

# from wtforms_alchemy import model_form_factory

from app import app, db
from models import Book, Room, Checkout
from validators import ValidateIsbn

#########
# Forms #
#########

class AddBookForm(Form):
    isbn13 = StringField(label='ISBN', validators=[validators.DataRequired(), ValidateIsbn()])
    inside_cover_id = StringField(label='Custom ID')
    title = StringField()
    description = StringField()
    thumbnail_url = URLField(validators=[validators.url])


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

@app.route('/add_books/', methods=['GET','POST'])
def add_books():
    add_book_form = AddBookForm()
    if add_book_form.validate_on_submit():
        print 'got add book form %s' % add_book_form

        new_book = Book(isbn13=add_book_form.isbn13.data, inside_cover_id=add_book_form.inside_cover_id.data, title=add_book_form.title.data, description=add_book_form.description.data, thumbnail_url=add_book_form.thumbnail_url.data)

        db.session.add(new_book)
        db.session.commit()

        flash('Added ISBN#%s "%s"' % (add_book_form.isbn13.data, add_book_form.title.data), category='success')
        return redirect((url_for('add_books')))
    if add_book_form.is_submitted():
        flash('There was an error with your submission', category='error')
    return render_template('add_books.html', form=add_book_form)

@app.route('/books/')
def show_books():
    return render_template('show_books.html', books=Book.query.all())


# inside_cover_id is optional
@app.route('/books/<isbn>')
@app.route('/books/<isbn>/<inside_cover_id>')
def single_book(isbn=None, inside_cover_id=None):
    return 'GET not implemented!'
