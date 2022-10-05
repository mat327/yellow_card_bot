import os
import time
from tkinter import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import users_ban_stats

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

def update_backup_firebase(msg_id, user_id, ban_duration, terminal):
    #dodanie nowej wiadomosci do backupu
    data = {'msg_id': str(msg_id)}
    db.collection('banned_messages').add(data)

    #aktualizacja statystyk banow
    docs = db.collection(u'banned_users_stats').where('user_id', '==', str(user_id)).get()

    if not docs:
        data = {'user_id': str(user_id), 'number_of_bans': 1, 'bans_time': ban_duration}
        db.collection('banned_users_stats').add(data)
    else :
        for doc in docs:
            key = doc.id
            db.collection('banned_users_stats').document(key).update({'number_of_bans': firestore.Increment(1), 'bans_time': firestore.Increment(ban_duration)}) # increment a fields

    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Firebase Backup updated.")

def create_backup_firebase(banned_messages):
    for msg in banned_messages:
        data = {'msg_id': str(msg)}
        db.collection('banned_messages').add(data)

    for x,y in users_ban_stats.stats.items():
        data = {'user_id': str(x), 'number_of_bans': y[0], 'bans_time': y[1]}
        db.collection('banned_users_stats').add(data)