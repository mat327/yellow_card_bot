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
from tkinter import *
import threading
import time
import os

#zmienne wykorzystywane w kodzie
banned_messages = []
server_ban_config = dict()

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
  await banned_users_txt.read_banned_user(client1, server_ban_config["guild_id"], terminal) #po zalogowaniu przywraca role zbanowanym użytkownikom 
  users_ban_stats.load_stats_from_file(terminal) #po zalogowaniu laduje statystyki banow z pliku

@client1.event
async def on_message(message): #zdarzenie wysłania wiadomosci
  if message.author == client1.user:
    return
  await client1.process_commands(message) #obsluga wiadomosci usuwa komendy, potrzebna ta linia

@client1.event
async def on_raw_reaction_add(payload): #w momencie dodania reakcji
  await ban_main.ban_function(payload, client1, banned_messages, server_ban_config["ban_duration"], server_ban_config["min_reaction_amount"], terminal) #glowna funkcja odpowiedzialna za bany

@client1.event
async def on_member_join(member): #nadanie roli nowemu użytkownikowi
  guild = client1.get_guild(470919364951146507)
  Gosc = discord.utils.get(guild.roles, name="Zwykły")
  await member.add_roles(Gosc)

@client1.command()
async def cards(ctx): #statystyki banow
  await users_ban_stats.display_stats(ctx, client1)

def discord_client_thread():
  try:
    client1.run(server_ban_config["oauth_token"])
  except:
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + " [Error] Cannot connect to server. Check configuration variables.")
    terminal.itemconfig(END, fg = "red")
    connect_button.config(state=NORMAL)
    config_button.config(state=NORMAL)
    disconnect_button.config(state=DISABLED)

#Kod GUI
main_gui = Tk()
main_gui.title("Yellow Card Bot v0.4")
main_gui.geometry("500x300")
main_gui.grid_rowconfigure(1, weight=1)
main_gui.grid_columnconfigure(3, weight=1)

def onclick_connect_button():
  if server_ban_config:
    global discord_client_thread_obj
    discord_client_thread_obj = threading.Thread(target=discord_client_thread) #obiekt watku clienta discorda
    discord_client_thread_obj.daemon = True #daemon thread (w momencie zamkniecia main tez przestaje dzialac)
    discord_client_thread_obj.start() #uruchomienie watku clienta discorda
    if discord_client_thread_obj.is_alive() == True:
      connect_button.config(state=DISABLED)
      config_button.config(state=DISABLED)
      disconnect_button.config(state=NORMAL)
  else:
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + " [Error] No configuration variables were entered. Click config button.")
    terminal.itemconfig(END, fg = "red")

def onclick_config_button():
  bot_config.enter_config(server_ban_config, terminal)

def onclick_disconnect_button():
  main_gui.destroy()
  os.startfile("bot.pyw")

scrollbar = Scrollbar(main_gui, orient="vertical")
terminal = Listbox(main_gui, yscrollcommand=scrollbar.set, background="black", foreground="white")
feet_author = Label(main_gui, text= " Author : Mateusz Białek     ")
feet_version = Label(main_gui, text="     Version : 0.4 ")
scrollbar.config(command=terminal.yview)
connect_button = Button(main_gui, text="Connect", command=onclick_connect_button)
config_button = Button(main_gui, text="Config", command=onclick_config_button)
disconnect_button = Button(main_gui, text="Disconnect", command=onclick_disconnect_button, state=DISABLED)

terminal.grid(row=1, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")
scrollbar.grid(row=1, column=4, sticky="ns")
connect_button.grid(row=0, column=0, padx=10, pady=10, ipadx=10)
config_button.grid(row=0, column=1, padx=10, pady=10, ipadx=13)
disconnect_button.grid(row=0, column=2, padx=10, pady=10, ipadx=8)
feet_author.grid(row=2, column=3, columnspan=2, sticky="e")
feet_version.grid(row=2, column=0, columnspan=3, sticky="w")

server_ban_config = bot_config.load_config_from_file(terminal)
   
main_gui.mainloop()