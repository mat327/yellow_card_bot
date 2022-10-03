#Zaimplementowane funkcje do odczytu i zapisu statystyk banow uzytkownikow w pliku json. 
#Zaimplementowana funkcja wypisania statystyk banow uzytkownikow na kanle tekstowym.

import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import json
import os
from tkinter import *
import time

#zapisując do dict w pamięci zmnienne mają typ int ale w przypadku zapisu do pliku id ma typ str,
#dlatego została zastosowana zmiana typu na str dla user_id
stats = {}

async def display_stats(ctx, client1, sort_by): 
    if sort_by == "time":
        sort_stats = sorted(stats.items(), key=lambda x: x[1][1], reverse=True)
    elif sort_by == "amount":
        sort_stats = sorted(stats.items(), key=lambda x: x[1][0], reverse=True)
    elif sort_by == "username":
        sort_stats = sorted(stats.items(), key=lambda x: x[0], reverse=False)
    
    async with ctx.typing():
        message = "Users Ban Statistic:\n"
        for x in sort_stats:
            try :
                user = client1.get_user(int(x[0]))
                time =  x[1][1] // 60
                message += user.display_name + " - " + str(x[1][0]) + "   |   " + str(time) + " minutes \n"
            except:
                pass
    await ctx.send(message)

def writte_stats_to_file(terminal):
    try:
        stats_file = open("ban_stats.json", "w")
        json.dump(stats, stats_file)
        stats_file.close()
        terminal.insert(END, "User ban stats file updated, file closed.")
    except:
        terminal.insert(END, "[Error] Cannot rewritte ban_stats.json file.")
        terminal.itemconfig(END, fg = "red")    

def load_stats_from_file(terminal):
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Checking ban_stats file ...")
    filesize = os.path.getsize("ban_stats.json") #rozmiar pliku txt
    if filesize == 0: #jezeli plik jest pusty funkcja nic nie robi
        terminal.insert(END, "The file is empty")
    else:
        terminal.insert(END, "Opening ban_stats.json ...")
        try : 
            stats_file = open("ban_stats.json", "r")
            global stats
            stats_str = stats_file.read() #odczyt z pliku jako str
            stats = json.loads(stats_str) #zmiana typu z str na dict
            terminal.insert(END, stats)
            stats_file.close()
            terminal.insert(END, "Data loaded to server memory, file closed.")
        except:
            terminal.insert(END, "[Error] Cannot read ban_stats.json file.")
            terminal.itemconfig(END, fg = "red")

def update_stats(user_id, terminal, ban_time):
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Updating users ban stats ...")
    if str(user_id) in stats:
        terminal.insert(END, "User id already exist in database, updating stats ...")
        stats_list = stats.get(str(user_id))
        stats_list[0] += 1
        stats_list[1] += ban_time
        stats[str(user_id)] = stats_list
        terminal.insert(END, "User ban stats updated.")
    else :
        terminal.insert(END, "User id is not exist in database, added new record ...")
        stats_list = [1, ban_time]
        stats[str(user_id)] = stats_list
        terminal.insert(END, "User ban stats added to database.")
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Updating users ban stats file ...")
    writte_stats_to_file(terminal)