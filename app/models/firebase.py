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




def firebase_push(item_action, child_name):
    def get_counter(child_name):
        db_firebase = db.child(child_name).get().val()
        return db_firebase.popitem()[1]['id']
    timestamp_without_ms = str(datetime.now())[:19]
    counter = get_counter(child_name) + 1
    data = dict(
        id=counter,
        timestamp=timestamp_without_ms,
        action=f'{item_action} Flask++'
    )
    return db.child(child_name).push(data)
