import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import json
import os

stats = {}

async def display_stats(ctx, client1):
    await ctx.send("Users Ban Statistic:")
    for user_id, cards in stats.items():
        user = client1.get_user(user_id)
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
        stats = stats_file.read()
        print(stats)
        stats_file.close()
        print("Data loaded to server memory, file closed.")

def update_stats(user_id):
    print("Updating users ban stats ...")
    if user_id in stats:
        print("User id already exist in database, updating stats ...")
        stats[user_id] += stats[user_id]
    else :
        print("User id is not exist in database, added new record ...")
        stats[user_id] = 1
    print("Updating users ban stats file ...")
    writte_stats_to_file()