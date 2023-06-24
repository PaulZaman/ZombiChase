
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred_obj = {

}

# Initialize Firebase Admin SDK
cred = credentials.Certificate(cred_obj)
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': "https://zombichase-e04ac-default-rtdb.europe-west1.firebasedatabase.app/",
})

# Get a database reference
ref = db.reference('/')