#Zaimplementowane funkcje do odczytu i zapisu listy zbanowanych wiadomosci uzytkownikow w pliku txt.
#Zapobiega utracie danych po restarcie serwera 

import discord
from discord.ext import commands
from discord.utils import get

def read_banned_messages(banned_messages): #odczyt wczesniej zapisanych id wiadomosci
    banned_messages_file = open("banned_messages_list.txt", "r")
    print("Copying ids message from file to list ...")
    try:
        for line in banned_messages_file.readlines():
            banned_messages.append(int(line))
    finally:
        print("File closed, records were copied to list")
        banned_messages_file.close()

def write_banned_messages(message_id): #zapis id nowej zbanowanej wiadomosci
    banned_messages_file = open("banned_messages_list.txt", "a")
    print("Writting new id message to file ...")
    try:
        banned_messages_file.write(str(message_id)+ "\n")
        print("New banned message id : " + str(message_id))
    finally:
        print("File closed, list rewritted")
        banned_messages_file.close()
