import time
from tkinter import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def make_backup_firebase(msg_id, user_id, ban_duration, terminal):
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)
    db=firestore.client()

    #dodanie nowej wiadomosci do backupu
    data = {'msg_id': int(msg_id)}
    db.collection('banned_messages').add(data)

    # Update data with unknown key: second way
    doc = db.collection('banned_users_stats').where("user_id", "==", int(user_id)).get() # Get all documents with age >=40
    if doc.exists:
        key = doc.id
        db.collection('banned_users_stats').document(key).update({"number_of_bans": firestore.Increment(1), "bans_time": firestore.Increment(ban_duration)}) # increment a field
    else :
        data = {'user_id': int(user_id), 'number_of_bans': 1, 'bans_time': ban_duration}
        db.collection('banned_users_stats').add(data)

    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Firebase Backup updated.")