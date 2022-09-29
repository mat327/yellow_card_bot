#Zaimplementowane funkcje do odczytu i zapisu rol obecnie zbanowanego uzytkownika w pliku txt.
#Zapobiega utracie rol uzytkownika w przypadku wylaczenia serwera kiedy jest on zbanowany.

import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os
import time
from tkinter import *

def write_banned_user(role_list, user_id, terminal): 
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Writting user info to file ...")
    try:
        banned_users_file = open("banned_users.txt", "a") #otwarcie pliku
        banned_users_file.write(str(user_id)+ "\n")
        terminal.insert(END, "Banned user id: " + str(user_id)) #zapisanie w pierwszej linii txt id uzytkownika
        terminal.insert(END, "User role list :")
        for role in role_list : #zapisanie rol uzytkownika w txt
            banned_users_file.write(str(role.name)+ "\n")
            terminal.insert(END, role.name)
        banned_users_file.close()
        terminal.insert(END, "File closed, user info saved")
    except:
        terminal.insert(END, "[Error] Cannot open user info file.")
        terminal.itemconfig(END, fg = "red")
               

async def read_banned_user(client1, guild_id, terminal): #odczyt pliku z info zbanowanych uzytkownikow
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Checking banned_users file ...")
    filesize = os.path.getsize("banned_users.txt") #rozmiar pliku txt
    if filesize == 0: #jezeli plik jest pusty funkcja nic nie robi
        terminal.insert(END, "The file is empty.")
    else:
        terminal.insert(END, "Restoring roles to users ...")     
        try:
            banned_users_file = open("banned_users.txt", "r") #otwarcie pliku
            guild = client1.get_guild(guild_id) #zapis obiektu gildii
            for line in banned_users_file.readlines():
                strip_line = line.rstrip('\n') #usuniecie \n ze stringa
                if strip_line.isdigit() : #jezeli linijka txt jest liczba
                    terminal.insert(END, "user id :" + strip_line)
                    member = await guild.fetch_member(int(strip_line)) #zapisanie obiektu uzytkownika
                    role = discord.utils.get(guild.roles, name="Muted") 
                    await member.remove_roles(role) #usuniecie roli muted
                    terminal.insert(END, "Role 'Muted' deleted")
                else:
                    if strip_line != "@everyone" and strip_line != "Server Booster": 
                        role = discord.utils.get(guild.roles, name=strip_line) #zapisanie obiektu roli
                        await member.add_roles(role) #nadanie roli uzytkownikowi
                        terminal.insert(END, strip_line + " ... done")
            terminal.insert(END, "Roles restored")
        except:
            terminal.insert(END, "[Error] Cannot restore roles.")
            terminal.itemconfig(END, fg = "red")
        finally:
            banned_users_file.close()
            open('banned_users.txt', 'w').close() #otwarcie i zamkniecie pliku w celu usuniecia jego zawartosci
            terminal.insert(END, "File closed and cleared.")

def check_is_user_banned(user_id, terminal): #sprawdzenie czy użytkownik jest obecnie zbanowany
    is_banned = False
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Checking banned_users file ...")
    filesize = os.path.getsize("banned_users.txt") #rozmiar pliku txt
    if filesize == 0: #jezeli plik jest pusty funkcja nic nie robi
        terminal.insert(END, "The file is empty.")
        return is_banned
    else:
        terminal.insert(END, "Searching user id ...")     
        try:
            banned_users_file = open("banned_users.txt", "r") #otwarcie pliku
            for line in banned_users_file.readlines():
                strip_line = line.rstrip('\n') #usuniecie \n ze stringa
                if strip_line.isdigit() : #jezeli linijka txt jest liczba
                    if int(strip_line) == user_id:
                        is_banned = True
        except:
            terminal.insert(END, "[Error] Cannot check if the user is banned.")
            terminal.itemconfig(END, fg = "red")
        finally:
            banned_users_file.close()
            terminal.insert(END, "File closed.")
            return is_banned
            
def delete_banned_user(user_id, terminal): #usuwanie info o zbanowanym użytkowniku
    sec = time.localtime() # get struct_time
    terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "   Deleting user from banned_users file ...")
    try:
        banned_users_file = open("banned_users.txt", "r") #otwarcie pliku
        lines = banned_users_file.readlines()
    except:
        terminal.insert(END, "[Error] Cannot open banned_users file.")
        terminal.itemconfig(END, fg = "red")
    finally:
        banned_users_file.close()
        terminal.insert(END, "File closed.")

    try:
        banned_users_file = open("banned_users.txt", "w") #otwarcie pliku
        delete = False
        for line in lines:
            strip_line = line.rstrip('\n') #usuniecie \n ze stringa

            if strip_line == str(user_id):
                delete = True

            if strip_line.isdigit() and strip_line != str(user_id):
                delete = False

            if delete == False:
                banned_users_file.write(line)
    except:
        terminal.insert(END, "[Error] Cannot open banned_users file.")
        terminal.itemconfig(END, fg = "red")
    finally:
        banned_users_file.close()
        terminal.insert(END, "File closed.")