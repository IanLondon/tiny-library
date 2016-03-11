import requests
import json

def google_books_info(isbn):
    """Use Google Books public API to get JSON info for a volume by ISBN. No API key needed."""
    r = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:%s" % isbn)
    data = r.json()

    if not data['totalItems'] == 1:
        # print "Warning: google_books_info expected one item, got %s" % data['totalItems']
        return False

    datadict = data['items'][0]['volumeInfo']

    # The keys in datadict should be:
        # publisher <type 'unicode'>
        # description <type 'unicode'>
        # language <type 'unicode'>
        # publishedDate <type 'unicode'>
        # readingModes <type 'dict'> --> eg, {u'image': False, u'text': False}
        # previewLink <type 'unicode'>
        # title <type 'unicode'>
        # printType <type 'unicode'>
        # canonicalVolumeLink <type 'unicode'>
        # pageCount <type 'int'>
        # maturityRating <type 'unicode'>
        # contentVersion <type 'unicode'>
        # industryIdentifiers <type 'list'> --> Eg,
        #     [{u'identifier': u'0545586178', u'type': u'ISBN_10'},
        #         {u'identifier': u'9780545586177', u'type': u'ISBN_13'}]
        # imageLinks <type 'dict'> --> Eg,
        # {u'smallThumbnail': u'http://books.google.com/books/content?id=39AMkgEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api',
        # u'thumbnail': u'http://books.google.com/books/content?id=39AMkgEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'}
        # authors --> list of strings, eg [u'Suzanne Collins']
        # ratingsCount <type 'int'>
        # allowAnonLogging <type 'bool'>
        # infoLink <type 'unicode'>
        # categories  --> list of strings, eg [u'Juvenile Fiction']
        # averageRating <type 'float'>


    return datadict

if __name__ == "__main__":
    # get info for Hunger Games Catching Fire
    hunger_games_isbn = '9780545586177'
    print google_books_info(hunger_games_isbn)
