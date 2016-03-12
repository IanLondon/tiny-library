from flask import render_template, request, redirect, url_for
from flask_wtf import Form
# from wtforms import StringField, HiddenField, validators

from wtforms_alchemy import model_form_factory

from app import app
from models import Book, Room, Checkout

#########
# Forms #
#########

# class AddBookForm(Form):
#     isbn = StringField(label='ISBN', validators=[validators.DataRequired()])
#     inside_cover_id = StringField(label=  'Custom ID')
#     title = StringField()
#     description = StringField()
#     thumbnail_url = StringField()


# BaseModelForm and ModelForm stuff is boilerplate
# for using flask-wtf + wtforms_alchemy together

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class AddBookForm(ModelForm):
    class Meta:
        model = Book


#########
# Views #
#########

@app.route('/add_books/', methods=['GET','POST'])
def add_books():
    add_book_form = AddBookForm()
    if add_book_form.validate_on_submit():
        print 'got add book form', add_book_form.isbn.data, add_book_form.inside_cover_id.data
        return redirect((url_for('show_books')))
    return render_template('add_books.html', form=add_book_form)

@app.route('/books/')
def show_books():
    return render_template('show_books.html', books=Book.query.all())


# inside_cover_id is optional
@app.route('/books/<isbn>')
@app.route('/books/<isbn>/<inside_cover_id>')
def single_book(isbn=None, inside_cover_id=None):
    return 'GET not implemented!'
