import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import banned_messages_txt
import banned_users_txt
import users_ban_stats
import ban_main

banned_messages = []

intents = discord.Intents.default()
intents.members = True
client1 = commands.Bot(command_prefix='$', intents=intents)

@client1.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client1))
  banned_messages_txt.read_banned_messages(banned_messages) #po zalogowaniu wczytuje liste zbanowanych wiadomosci z pliku do pamieci
  await banned_users_txt.read_banned_user(client1) #po zalogowaniu przywraca role zbanowanym użytkownikom 
  users_ban_stats.load_stats_from_file() #po zalogowaniu laduje statystyki banow z pliku

@client1.event
async def on_message(message): #zdarzenie wysłania wiadomosci
  if message.author == client1.user:
    return
  await client1.process_commands(message) #obsluga wiadomosci usuwa komendy, potrzebna ta linia

@client1.event
async def on_raw_reaction_add(payload): #w momencie dodania reakcji
  await ban_main.ban_function(payload, client1, banned_messages) #glowna funkcja odpowiedzialna za bany

@client1.event
async def on_member_join(member): #nadanie roli nowemu użytkownikowi
  guild = client1.get_guild(470919364951146507)
  Gosc = discord.utils.get(guild.roles, name="Zwykły")
  await member.add_roles(Gosc)

@client1.command()
async def cards(ctx): #statystyki banow
  await users_ban_stats.display_stats(ctx, client1)
      
client1.run("ODY3NDg1MTY0NDAwODAzODkw.YPhyhA.Wmey0A7HWGerDNLB7mzgEBOnivE")