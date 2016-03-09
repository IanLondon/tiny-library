# To run, go to app/ root and do `python -m examp.isbn_convert`
from core import isbn
discover_the_stars10 = '0517565293'
print 'the isbn10 %s -> isbn13 %s' % (discover_the_stars10, isbn.toI13(discover_the_stars10))
