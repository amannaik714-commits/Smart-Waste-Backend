import os
import json
import firebase_admin
from firebase_admin import credentials, db

firebase_credentials = os.getenv("FIREBASE_CREDENTIALS_JSON")

if firebase_credentials:
    cred = credentials.Certificate(json.loads(firebase_credentials))
else:
    cred = credentials.Certificate(
        "smart-waste-management-49d88-firebase-adminsdk-fbsvc-88b8b6d8ee.json"
    )

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://smart-waste-management-49d88-default-rtdb.asia-southeast1.firebasedatabase.app"
})