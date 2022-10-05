import pyrebase
from sympy import im
import users_ban_stats
import time
from tkinter import *

# Initialize Firebase
firebaseConfig = {"apiKey": "AIzaSyCvpC0Dh1FRohG_8lhDCWp_qxaCUfcjJ7s",
                  "authDomain": "elo-bot-backup.firebaseapp.com",
                  "databaseURL": "https://elo-bot-backup-default-rtdb.europe-west1.firebasedatabase.app",
                  "projectId": "elo-bot-backup",
                  "storageBucket": "elo-bot-backup.appspot.com",
                  "messagingSenderId": "241995792453",
                  "appId": "1:241995792453:web:cf0e8ec78317ce52d6a32c",
                  "measurementId": "G-4S5L7ZWCRX"}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()


def create_backup_firebase(banned_messages):
    for msg in banned_messages:
        data = {'msg_id': str(msg)}
        db.child('elo_bot_backup').child('banned_messages').push(data)

    for x, y in users_ban_stats.stats.items():
        data = {'user_id': str(x), 'number_of_bans': y[0], 'bans_time': y[1]}
        db.child('elo_bot_backup').child('banned_users_stats').push(data)


def update_backup_firebase(msg_id, user_id, ban_duration, terminal):
    # dodanie nowej wiadomosci do backupu
    data = {'msg_id': str(msg_id)}
    db.child('elo_bot_backup').child('banned_messages').push(data)

    # aktualizacja statystyk banow
    user_stats = db.child('elo_bot_backup').child(
        'banned_users_stats').order_by_child('user_id').equal_to(str(user_id)).get()

    if not user_stats.each(): #jezeli uzytkownika nie ma w bazie to dodaj
        data = {'user_id': str(user_id), 'number_of_bans': 1, 'bans_time': ban_duration}
        db.child('elo_bot_backup').child('banned_users_stats').push(data)
    else:
        for stat in user_stats.each():
            data = {'number_of_bans': stat.val()['number_of_bans'] + 1,
            'bans_time': stat.val()['bans_time'] + ban_duration}
            db.child('elo_bot_backup').child('banned_users_stats').child(stat.key()).update(data)

    sec = time.localtime()  # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Firebase Backup updated.")
