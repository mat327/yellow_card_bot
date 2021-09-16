#Zaimplementowane funkcje do odczytu i zapisu listy zbanowanych wiadomosci uzytkownikow w pliku txt.
#Zapobiega utracie danych po restarcie serwera 

import discord
from discord.ext import commands
from discord.utils import get
import time
from tkinter import *

def read_banned_messages(banned_messages, terminal): #odczyt wczesniej zapisanych id wiadomosci
    banned_messages_file = open("banned_messages_list.txt", "r")
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Copying messages ids from file to list ...")
    try:
        for line in banned_messages_file.readlines():
            banned_messages.append(int(line))
        terminal.insert(END, "Records were copied to list.")
    except:
        terminal.insert(END, "[Error] Cannot copy messages ids.")
        terminal.itemconfig(END, fg = "red")
    finally:
        terminal.insert(END, "File closed.")
        banned_messages_file.close()

def write_banned_messages(message_id, terminal): #zapis id nowej zbanowanej wiadomosci
    banned_messages_file = open("banned_messages_list.txt", "a")
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Writting new id message to file ...")
    try:
        banned_messages_file.write(str(message_id)+ "\n")
        terminal.insert(END, "New banned message id : " + str(message_id))
        terminal.insert(END, "List rewritted.")
    except:
        terminal.insert(END, "[Error] Cannot write message id.")
        terminal.itemconfig(END, fg = "red")
    finally:
        terminal.insert(END, "File closed.")
        banned_messages_file.close()