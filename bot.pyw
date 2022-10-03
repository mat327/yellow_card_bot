from logging import disable
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import banned_messages_txt
import banned_users_txt
import users_ban_stats
import ban_main
import bot_config
import ban_func_config
import functionalities_config
from tkinter import *
import threading
import time
import os

import command_drink
import command_dog_cat

#zmienne wykorzystywane w kodzie
banned_messages = []
bot_config_dict = dict()
ban_func_config_dict = dict()
functionalities_config_dict = dict()
functionalities_config_dict = {"ban_func": 1, "ban_cmd": 1, "drink_cmd": 1, "cat_cmd": 1, "dog_cmd": 1}

#konfiguracja clienta discorda
intents = discord.Intents.default()
intents.members = True
client1 = commands.Bot(command_prefix='$', intents=intents)

#Funkcje clienta discorda
@client1.event
async def on_ready():
  sec = time.localtime() # get struct_time
  terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   We have logged in as {0.user}".format(client1))
  banned_messages_txt.read_banned_messages(banned_messages, terminal) #po zalogowaniu wczytuje liste zbanowanych wiadomosci z pliku do pamieci
  await banned_users_txt.read_banned_user(client1, bot_config_dict["guild_id"], terminal) #po zalogowaniu przywraca role zbanowanym użytkownikom 
  users_ban_stats.load_stats_from_file(terminal) #po zalogowaniu laduje statystyki banow z pliku

@client1.event
async def on_message(message): #zdarzenie wysłania wiadomosci
  if message.author == client1.user:
    return
  await client1.process_commands(message) #obsluga wiadomosci usuwa komendy, potrzebna ta linia

@client1.event
async def on_raw_reaction_add(payload): #w momencie dodania reakcji
  await ban_main.ban_function(payload, client1, banned_messages, ban_func_config_dict["ban_duration"], ban_func_config_dict["min_reaction_amount"], terminal, functionalities_config_dict["ban_func"]) #glowna funkcja odpowiedzialna za bany

@client1.event
async def on_member_join(member): #nadanie roli nowemu użytkownikowi
  guild = client1.get_guild(bot_config_dict["guild_id"])
  Gosc = discord.utils.get(guild.roles, name="Zwykły")
  await member.add_roles(Gosc)

@client1.hybrid_command()
async def bans(ctx, sort_by=""): #statystyki banow
  if functionalities_config_dict["ban_cmd"] == 1: #sprawdzenie czy komenda jest wlaczona w gui
    if sort_by == "time":
      await users_ban_stats.display_stats(ctx, client1, "time")
    elif sort_by == "amount":
      await users_ban_stats.display_stats(ctx, client1, "amount")
    elif sort_by == "username":
      await users_ban_stats.display_stats(ctx, client1, "username")
    else :
      await users_ban_stats.display_stats(ctx, client1, "time")
  else:
    await ctx.send("Command /bans is off :(")

@client1.hybrid_command() #komenda $drink
async def drink(ctx):
  if functionalities_config_dict["drink_cmd"] == 1: #sprawdzenie czy komenda jest wlaczona w gui 
    quote = command_drink.get_drink()
    await ctx.send(quote) 
  else:
    await ctx.send("Command /drink is off :(")

@client1.hybrid_command() #komenda $cat
async def cat(ctx):
  if functionalities_config_dict["cat_cmd"] == 1: #sprawdzenie czy komenda jest wlaczona w gui 
    quote = command_dog_cat.get_cat()
    await ctx.send(quote) 
  else:
    await ctx.send("Command /cat is off :(")

@client1.hybrid_command() #komenda $dog
async def dog(ctx):
  if functionalities_config_dict["dog_cmd"] == 1: #sprawdzenie czy komenda jest wlaczona w gui 
    quote = command_dog_cat.get_dog()
    await ctx.send(quote)
  else:
    await ctx.send("Command /dog is off :(") 

#Kod GUI
main_gui = Tk()
main_gui.title("Elo Server Bot")
main_gui.geometry("700x400")
main_gui.grid_rowconfigure(1, weight=1)
main_gui.grid_columnconfigure(6, weight=1)

def onclick_connect_button():
  if bot_config_dict:
    if ban_func_config_dict:
        loop = asyncio.get_event_loop()
        loop.create_task(client1.start(bot_config_dict.get("oauth_token")))
        global discord_client_thread_obj
        discord_client_thread_obj=threading.Thread(target=loop.run_forever) #obiekt watku clienta discorda
        discord_client_thread_obj.daemon = True #daemon thread (w momencie zamkniecia main tez przestaje dzialac)
        try:
          discord_client_thread_obj.start() #uruchomienie watku clienta discorda
        except:
          sec = time.localtime() # get struct_time
          terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + " [Error] Cannot connect to server. Check configuration variables.")
          terminal.itemconfig(END, fg = "red")
          connect_button.config(state=NORMAL)
          bot_config_button.config(state=NORMAL)
          disconnect_button.config(state=DISABLED)
        if discord_client_thread_obj.is_alive() == True:
          connect_button.config(state=DISABLED)
          bot_config_button.config(state=DISABLED)
          disconnect_button.config(state=NORMAL)
    else:
      sec = time.localtime() # get struct_time
      terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + " [Error] No configuration variables were entered. Click Ban func config button.")
      terminal.itemconfig(END, fg = "red")
  else:
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + " [Error] No configuration variables were entered. Click Server config button.")
    terminal.itemconfig(END, fg = "red")

def onclick_bot_config_button():
  bot_config.enter_config(bot_config_dict, terminal)

def onclick_ban_func_config_button():
  ban_func_config.enter_config(ban_func_config_dict, terminal)

def onclick_functionalities_config_button():
  functionalities_config.enter_config(functionalities_config_dict, terminal)

def onclick_disconnect_button():
  main_gui.destroy()
  os.startfile("bot.pyw")

scrollbar = Scrollbar(main_gui, orient="vertical")
terminal = Listbox(main_gui, yscrollcommand=scrollbar.set, background="black", foreground="white")
feet_author = Label(main_gui, text= " Author : Mateusz Białek     ")
feet_version = Label(main_gui, text="     Version : 0.5 ")
scrollbar.config(command=terminal.yview)
connect_button = Button(main_gui, text="Connect", command=onclick_connect_button)
bot_config_button = Button(main_gui, text="Bot Config", command=onclick_bot_config_button)
ban_func_config_button = Button(main_gui, text="Ban Func Config", command=onclick_ban_func_config_button)
functionalities_config_button = Button(main_gui, text="On/Off functionalities", command=onclick_functionalities_config_button)
disconnect_button = Button(main_gui, text="Disconnect", command=onclick_disconnect_button, state=DISABLED)


terminal.grid(row=1, column=0, columnspan=7, padx=0, pady=0, sticky="nsew")
scrollbar.grid(row=1, column=7, sticky="ns")
connect_button.grid(row=0, column=0, padx=5, pady=5, ipadx=10)
bot_config_button.grid(row=0, column=2, padx=5, pady=5, ipadx=13)
ban_func_config_button.grid(row=0, column=3, padx=5, pady=5, ipadx=13)
disconnect_button.grid(row=0, column=1, padx=5, pady=5, ipadx=8)
functionalities_config_button.grid(row=0, column=4, padx=5, pady=5, ipadx=10)
feet_author.grid(row=2, column=3, columnspan=4, sticky="e")
feet_version.grid(row=2, column=0, columnspan=3, sticky="w")

bot_config_dict = bot_config.load_config_from_file(terminal)
ban_func_config_dict = ban_func_config.load_config_from_file(terminal)
   
main_gui.mainloop()