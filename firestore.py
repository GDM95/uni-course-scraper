import json
import firebase_admin
from firebase_admin import credentials, db, firestore


cred = credentials.Certificate('./class-chat-b0b05-firebase-adminsdk-dwokv-fff6abdd3c.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://class-chat-b0b05.firebaseio.com'
})


fstore = firestore.client()
with open('catalog.json') as json_file:
    data = json.load(json_file)
    for p in data:

        doc_ref = fstore.collection(u'subjects').document(p)
        doc_ref.set({
            u'courses': data[p]
        })
