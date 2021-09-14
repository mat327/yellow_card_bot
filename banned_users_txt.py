#Zaimplementowane funkcje do odczytu i zapisu rol obecnie zbanowanego uzytkownika w pliku txt.
#Zapobiega utracie rol uzytkownika w przypadku wylaczenia serwera kiedy jest on zbanowany.

import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os

def write_banned_user(role_list, user_id): 
    banned_users_file = open("banned_users.txt", "a") #otwarcie pliku
    try:
        print("Writting user info to file ...")
        banned_users_file.write(str(user_id)+ "\n")
        print("Banned user id: " + str(user_id)) #zapisanie w pierwszej linii txt id uzytkownika
        print("User role list :")
        for role in role_list : #zapisanie rol uzytkownika w txt
            banned_users_file.write(str(role.name)+ "\n")
            print(role.name)
    finally:
        print("File closed, user info saved")
        banned_users_file.close()

async def read_banned_user(client1, guild_id): #odczyt pliku z info zbanowanych uzytkownikow
    print("Checking banned_users file ...")
    filesize = os.path.getsize("banned_users.txt") #rozmiar pliku txt
    if filesize == 0: #jezeli plik jest pusty funkcja nic nie robi
        print("The file is empty")
    else:
        print("Restoring roles to users ...")
        banned_users_file = open("banned_users.txt", "r") #otwarcie pliku
        try:
            guild = client1.get_guild(guild_id) #zapis obiektu gildii
            for line in banned_users_file.readlines():
                strip_line = line.rstrip('\n') #usuniecie \n ze stringa
                if strip_line.isdigit() : #jezeli linijka txt jest liczba
                    print("user id :" + strip_line)
                    member = await guild.fetch_member(int(strip_line)) #zapisanie obiektu uzytkownika
                    role = discord.utils.get(guild.roles, name="Muted") 
                    await member.remove_roles(role) #usuniecie roli muted
                    print("Role 'Muted' deleted")
                else:
                    if strip_line != "@everyone": 
                        role = discord.utils.get(guild.roles, name=strip_line) #zapisanie obiektu roli
                        await member.add_roles(role) #nadanie roli uzytkownikowi
                        print(strip_line + " ... done")
            print("Roles restored")
        finally:
            banned_users_file.close()
            open('banned_users.txt', 'w').close() #otwarcie i zamkniecie pliku w celu usuniecia jego zawartosci
            print("File closed and cleared")