import pyrebase
from typing_extensions import MutableMapping
from config import config

firebase = pyrebase.initialize_app(config)

db = firebase.database()

data = db.child("savedLoc/").child("1").get()
# data = ref.get()
print(data.val())
