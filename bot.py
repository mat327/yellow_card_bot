import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os
import banned_messages_txt
import banned_user_info_txt

banned_messages = []

intents = discord.Intents.default()
intents.members = True
client1 = commands.Bot(command_prefix='$', intents=intents)


@client1.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client1))
  await banned_user_info_txt.read_banned_user_info(client1) #po zalogowaniu wykonuje funkcję


@client1.event
async def on_message(message): #zdarzenie wysłania wiadomosci
  if message.author == client1.user:
    return
  await client1.process_commands(message) #obsluga wiadomosci usuwa komendy, potrzebna ta linia

@client1.event
async def on_raw_reaction_add(payload): #licznik emoji
  if payload.emoji.name == '\U0001F7E8': #porównanie emoji
    channel = client1.get_channel(payload.channel_id) #zapisanie obiektu channel
    message = await channel.fetch_message(payload.message_id) #zapisanie obiektu message
    reaction = get(message.reactions, emoji=payload.emoji.name) #zapisanie obiektu reakcji wiadomości z danym emoji
    if reaction and reaction.count > 3: #porówanie ilości reakcji
      if payload.message_id in banned_messages:
        await message.channel.send(message.author.name + " otrzymał już karę.")
      else:
        await message.channel.send(message.author.name + " otrzymał trzy żółte kartki.")
        guild = message.guild
        Muted = discord.utils.get(guild.roles, name="Muted")
        if not Muted: #tworzenie roli muted
          Muted = await guild.create_role(name="Muted")
          for channel in guild.channels:
            await channel.set_permissions(Muted, speak=True, send_messages=False, read_message_history=True, read_messages=False)
        member = await guild.fetch_member(message.author.id) #zapisanie obiektu użytkownika
        roles_list = member.roles #lista roli zmutowanego użytkownika
        for role in roles_list: #usuwanie dotychczasowych roli
          if role.name != "@everyone":
            role1 = discord.utils.get(guild.roles, name=role.name)
            await member.remove_roles(role1)
        await member.add_roles(Muted) #nadanie roli muted
        await message.channel.send(message.author.name + " został zmutowany na 15 minut.")
        banned_messages.append(payload.message_id) #dodanie wiadomości do listy zbanowanych
        banned_messages_txt.write_banned_messages(payload.message_id) #dodanie wiadomości do pliku
        banned_user_info_txt.write_banned_user_info(roles_list, message.author.id) #dodatnie informacji o zbanowanym uzytkowniku do txt
        await asyncio.sleep(900)
        await member.remove_roles(Muted) #usunięcie roli muted
        for role in roles_list: #przywracanie roli
          if role.name != "@everyone":
            role1 = discord.utils.get(guild.roles, name=role.name)
            await member.add_roles(role1)
        await message.channel.send(message.author.name + " został odmutowany.")
        open('banned_user_info.txt', 'w').close() #otwarcie i zamknięcie pliku w celu usunięcia jego zawartości
        print("User info file cleared")

@client1.event
async def on_member_join(member):
  guild = client1.get_guild(470919364951146507)
  Gosc = discord.utils.get(guild.roles, name="Zwykły")
  await member.add_roles(Gosc)
      
banned_messages_txt.read_banned_messages(banned_messages)
client1.run("ODY3NDg1MTY0NDAwODAzODkw.YPhyhA.Wmey0A7HWGerDNLB7mzgEBOnivE")
