#Glowna funkcja odpowiedzialna za banowanie. Wywolywana jest w momencie dodania reakcji do wiadomosci na kanale.

import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import banned_messages_txt
import banned_users_txt
import users_ban_stats
import time
from tkinter import *

async def ban_function(payload, client1, banned_messages, ban_duration, min_reaction_amount, terminal, func_on):
    if payload.emoji.name == '\U0001F7E8': #porównanie emoji
        channel = client1.get_channel(payload.channel_id) #zapisanie obiektu channel
        message = await channel.fetch_message(payload.message_id) #zapisanie obiektu message
        reaction = get(message.reactions, emoji=payload.emoji.name) #zapisanie obiektu reakcji wiadomości z danym emoji
        if reaction and reaction.count > (min_reaction_amount-1): #porówanie ilości reakcji
            if func_on == 1:
                if payload.message_id in banned_messages:
                    #await message.channel.send(message.author.name + " otrzymał już karę.")
                    await message.reply(message.author.name + " otrzymał już karę.")
                else:
                    banned_messages.append(payload.message_id) #dodanie wiadomości do listy zbanowanych
                    if min_reaction_amount < 5:
                        await message.channel.send(message.author.name + " otrzymał " + str(min_reaction_amount) + " żółte kartki.")
                    else:
                        await message.channel.send(message.author.name + " otrzymał " + str(min_reaction_amount) + " żółtych kartek.")
                    guild = message.guild
                    Muted = discord.utils.get(guild.roles, name="Muted")
                    if not Muted: #tworzenie roli muted
                        Muted = await guild.create_role(name="Muted")
                        for channel in guild.channels:
                            await channel.set_permissions(Muted, speak=True, send_messages=False, read_message_history=True, read_messages=True)

                    if banned_users_txt.check_is_user_banned(message.author.id, terminal): #sprawdzenie czy użytkownik jest już zbanowany
                        await message.channel.send(message.author.name + " otrzyma karę po zakończeniu obecnej.")

                    while banned_users_txt.check_is_user_banned(message.author.id, terminal): #sprawdzenie czy użytkownik jest już zbanowany
                        await asyncio.sleep(10)

                    member = await guild.fetch_member(message.author.id) #zapisanie obiektu użytkownika
                    roles_list = member.roles #lista roli zmutowanego użytkownika
                    for role in roles_list: #usuwanie dotychczasowych roli
                        if role.name != "@everyone" and role.name != "Server Booster":
                            role1 = discord.utils.get(guild.roles, name=role.name)
                            await member.remove_roles(role1)
                    await member.add_roles(Muted) #nadanie roli muted
                    if ban_duration < 300:
                        await message.channel.send(message.author.name + " został zmutowany na " + str(ban_duration)+ " sekund.")
                    else:
                        await message.channel.send(message.author.name + " został zmutowany na " + str(ban_duration//60)+ " minut.")

                    banned_messages_txt.write_banned_messages(payload.message_id, terminal) #dodanie wiadomości do pliku
                    banned_users_txt.write_banned_user(roles_list, message.author.id, terminal) #dodatnie informacji o zbanowanym uzytkowniku do txt
                    users_ban_stats.update_stats(message.author.id, terminal, ban_duration) #zaktualizowanie statystyk banow

                    await asyncio.sleep(ban_duration)

                    await member.remove_roles(Muted) #usunięcie roli muted
                    for role in roles_list: #przywracanie roli
                        if role.name != "@everyone" and role.name != "Server Booster":
                            role1 = discord.utils.get(guild.roles, name=role.name)
                            await member.add_roles(role1)
                    await message.channel.send(message.author.name + " został odmutowany.")
                    try:
                        banned_users_txt.delete_banned_user(message.author.id, terminal) #usuniecie użytkownika z pliku zbanowanych uzytkownikow
                        sec = time.localtime() # get struct_time
                        terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   User banned file updated.")
                    except:
                        sec = time.localtime() # get struct_time
                        terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   [Error] Cannot clear banned_users file.")
            else:
                await message.channel.send("Ban function is off :(")