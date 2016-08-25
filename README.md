# tinylibrary :books:
tinylibrary is a simple web app for managing small libraries.

# Features
* Add new books: **just enter the ISBN**, and it will auto-populate information from Google Books API including title, author, description, and cover image.
* Check out and return books to lenders

# Local development
From the root of this repo:
1. Make a virtual environment using `requirements.txt`
2. Activate the virtual environment: `source activate env/bin/activate`
3. Run the app: `python tinylibrary/app.py`

For playing on the REPL while debugging or adding new features, use `ipython -i console_helper.py` to conveniently have an app context.

The local development version uses a sqlite3 database created at `/tmp/tinylibrary.db`. The admin account is `admin@admin.com` and the password is `whyyoumakeusread`.

The default books added don't use the Google Books API so they're ugly entries. Toss a few real books in there, like `9781491912768` (Advanced Analytics with Spark :p )

# TODO:
* Admin control of students and rooms
* Do not allow books with no title
* Watch out for users quickly adding without letting Google Books info populate - you'd get no title, just ISBN. ("Do not allow books with no title" helps with this...)
* Test on mobile
* Let Admin DELETE book
* Control `cover image` size in `/books/` - it's rather chaotic
