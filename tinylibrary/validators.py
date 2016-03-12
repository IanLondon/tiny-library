from wtforms import validators
from core.isbn import toI13, InvalidIsbn

# These are validators for WTForms.

class ValidateIsbn(object):
    def __init__(self, message=None):
        if not message:
            message = 'Invalid ISBN.'
        self.message = message
    def __call__(self, form, field):
        isbn = field.data
        try:
            toI13(isbn)
        except InvalidIsbn:
            raise validators.ValidationError(self.message)
