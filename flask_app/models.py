from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
import base64


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    points = db.IntField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    boba_name = db.StringField(required=True, min_length=1, max_length=100)
    boba_id = db.IntField(required=True)

class BobaList(db.Document):
    name = db.StringField(required=True, min_length=1, max_length=100)
    address = db.StringField(required=False, min_length=1, max_length=300)
    boba_id = db.IntField(required=True)

def add_store(bname, addy):
    store = BobaList(
        name = bname,
        address = addy,
        boba_id = hash(bname),
    )
    store.save()