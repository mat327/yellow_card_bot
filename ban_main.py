#Glowna funkcja odpowiedzialna za banowanie. Wywolywana jest w momencie dodania reakcji do wiadomosci na kanale.
#Wykorzystuje users_ban_stats.py, banned_users.py i banned_messages_txt.py

import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import banned_messages_txt
import banned_users_txt
import users_ban_stats
import time
from tkinter import *

async def ban_function(payload, client1, banned_messages, ban_duration, min_reaction_amount, terminal):
    if payload.emoji.name == '\U0001F7E8': #porównanie emoji
        channel = client1.get_channel(payload.channel_id) #zapisanie obiektu channel
        message = await channel.fetch_message(payload.message_id) #zapisanie obiektu message
        reaction = get(message.reactions, emoji=payload.emoji.name) #zapisanie obiektu reakcji wiadomości z danym emoji
        if reaction and reaction.count > (min_reaction_amount-1): #porówanie ilości reakcji
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
                banned_messages_txt.write_banned_messages(payload.message_id, terminal) #dodanie wiadomości do pliku
                banned_users_txt.write_banned_user(roles_list, message.author.id, terminal) #dodatnie informacji o zbanowanym uzytkowniku do txt
                users_ban_stats.update_stats(message.author.id, terminal) #zaktualizowanie statystyk banow
                await asyncio.sleep(ban_duration)
                await member.remove_roles(Muted) #usunięcie roli muted
                for role in roles_list: #przywracanie roli
                    if role.name != "@everyone":
                        role1 = discord.utils.get(guild.roles, name=role.name)
                        await member.add_roles(role1)
                await message.channel.send(message.author.name + " został odmutowany.")
                try:
                    open('banned_users.txt', 'w').close() #otwarcie i zamknięcie pliku w celu usunięcia jego zawartości
                    sec = time.localtime() # get struct_time
                    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   User banned file cleared.")
                except:
                    sec = time.localtime() # get struct_time
                    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   [Error] Cannot clear banned_users file.")