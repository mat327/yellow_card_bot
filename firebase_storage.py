import pyrebase
import time
import requests
import os
from tkinter import *

# Initialize Firebase
firebaseConfig = {"apiKey": "AIzaSyCvpC0Dh1FRohG_8lhDCWp_qxaCUfcjJ7s",
                  "authDomain": "elo-bot-backup.firebaseapp.com",
                  "databaseURL": "https://elo-bot-backup-default-rtdb.europe-west1.firebasedatabase.app",
                  "projectId": "elo-bot-backup",
                  "storageBucket": "elo-bot-backup.appspot.com",
                  "messagingSenderId": "241995792453",
                  "appId": "1:241995792453:web:cf0e8ec78317ce52d6a32c",
                  "measurementId": "G-4S5L7ZWCRX",
                  "serviceAccount": "firebase_key.json"}

firebase = pyrebase.initialize_app(firebaseConfig)

storage = firebase.storage()

def update_backup_files(terminal):
    try :
        storage.child("backup_files/banned_messages_list.txt").put("banned_messages_list.txt")
        storage.child("backup_files/ban_stats.json").put("ban_stats.json")
        sec = time.localtime()  # get struct_time
        terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Backup files updated in storage.")
    except :
        sec = time.localtime()  # get struct_time
        terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   [Error] Cannot update backup files in storage.")
        terminal.itemconfig(END, fg = "red")


def save_banned_pic_vid_in_storage(msg_id, urls, terminal):
    storage_urls = list()
    for i in range(len(urls)):
        r = requests.get(urls[i], allow_redirects=True)

        contentLength = r.headers.get('content-length', None)

        if contentLength and float(contentLength) < 10485760: # do pobrania oraz ponizej 10 mb
            if "video" in r.headers.get('content-type') or "image" in r.headers.get('content-type'):
                format = urls[i].rsplit('.', 1)[1]
                file_name = msg_id+'_'+str(i)+'.'+format
                open(file_name, 'wb').write(r.content)

                if "video" in r.headers.get('content-type'):
                    storage.child("banned_videos/"+file_name).put(file_name)
                    storage_urls.append(str(storage.child("banned_videos/"+file_name).get_url(None)))

                if "image" in r.headers.get('content-type'):
                    storage.child("banned_images/"+file_name).put(file_name)
                    storage_urls.append(str(storage.child("banned_images/"+file_name).get_url(None)))

                os.remove(file_name)
    sec = time.localtime()  # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Images/Videos saved in storage.")
    return storage_urls
                