import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import json
import os

#zapisując do dict w pamięci zmnienne mają typ int ale w przypadku zapisu do pliku id ma typ str,
#dlatego została zastosowana zmiana typu na str dla user_id
stats = {}

async def display_stats(ctx, client1):
    await ctx.send("Users Ban Statistic:")
    for user_id, cards in stats.items():
        user = client1.get_user(int(user_id))
        time =  cards * 15
        await ctx.send(user.display_name + " - " + str(cards) + "   |   " + str(time) + " minutes")

def writte_stats_to_file():
    try:
        stats_file = open("ban_stats.json", "w")
        json.dump(stats, stats_file)
        stats_file.close()
        print("User ban stats file updated, file closed.")
    except:
        print("Cannot rewritte ban_stats.json file.")
    

def load_stats_from_file():
    print("Checking ban_stats file ...")
    filesize = os.path.getsize("ban_stats.json") #rozmiar pliku txt
    if filesize == 0: #je�eli plik jest pusty funkcja nic nie robi
        print("The file is empty")
    else:
        print("Opening ban_stats.json ...")
        stats_file = open("ban_stats.json", "r")
        global stats
        stats_str = stats_file.read() #odczyt z pliku jako str
        stats = json.loads(stats_str) #zmiana typu z str na dict
        print(stats)
        stats_file.close()
        print("Data loaded to server memory, file closed.")

def update_stats(user_id):
    print("Updating users ban stats ...")
    if str(user_id) in stats:
        print("User id already exist in database, updating stats ...")
        stats[str(user_id)] += stats[str(user_id)]
    else :
        print("User id is not exist in database, added new record ...")
        stats[str(user_id)] = 1
    print("Updating users ban stats file ...")
    writte_stats_to_file()