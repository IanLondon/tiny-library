from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tinylibrary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #XXX:???

db = SQLAlchemy(app)
