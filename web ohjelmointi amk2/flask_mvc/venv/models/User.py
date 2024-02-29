from flask_login import UserMixin
from models.Database import db

class User(UserMixin, db.Document):
    #id = db.IntField()
    email = db.StringField(max_length=100, unique=True)
    password = db.StringField(max_length=100)
    name = db.StringField(max_length=100)