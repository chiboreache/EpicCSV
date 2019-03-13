import pyrebase
from datetime import datetime


config = {
    "apiKey": "AIzaSyAKncmaGznghzq5IXUJBoYGt1-fOxCHUgM",
    "authDomain": "epiccsv.firebaseapp.com",
    "databaseURL": "https://epiccsv.firebaseio.com",
    "storageBucket": "epiccsv.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_last_upload():
    db_firebase = db.child("uploads").get().val()
    return db_firebase.popitem()[1]['id']


def firebase_push(item_action, item_id):
    timestamp_without_ms = str(datetime.now())[:19]
    counter = item_id + 1
    data = dict(
        id=counter,
        timestamp=timestamp_without_ms,
        action=f'{item_action} Flask++'
    )
    return db.child("uploads").push(data)
