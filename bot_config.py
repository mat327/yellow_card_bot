#Zaimplementowana funkcja do wprowadzania danych serwera
#Dane zapisywane sa w formie slownika

import json
import os
import time

from tkinter import *

def load_config_from_file(main_gui_terminal):
    sec = time.localtime() # get struct_time
    main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Checking bot config file ...")
    filesize = os.path.getsize("bot_config.json") #rozmiar pliku
    if filesize == 0: #jezeli plik jest pusty funkcja nic nie robi
        main_gui_terminal.insert(END, "The file is empty.")
        bot_config_dict = dict()
        return bot_config_dict
    else:
        main_gui_terminal.insert(END, "Opening bot_config.json ...")
        try:
            config_file = open("bot_config.json", "r")
            bot_config_dict_str = config_file.read() #odczyt z pliku jako str
            bot_config_dict = json.loads(bot_config_dict_str) #zmiana typu z str na dict
            config_file.close()
            main_gui_terminal.insert(END, "Data loaded to server memory, file closed.")
            return bot_config_dict
        except:
            main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  [Error] Cannot open config file.")
            main_gui_terminal.itemconfig(END, fg = "red")
            bot_config_dict = dict()
            return bot_config_dict

def write_config_to_file(bot_config_dict, main_gui_terminal):
    try:
        config_file = open("bot_config.json", "w")
        json.dump(bot_config_dict, config_file)
        config_file.close()
        sec = time.localtime() # get struct_time
        main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Config file updated, file closed.")
    except:
        sec = time.localtime() # get struct_time
        main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  [Error] Cannot rewritte config file.")
        main_gui_terminal.itemconfig(END, fg = "red")

def save_config_to_file_window(bot_config_dict, main_gui_terminal):
    save_config_windows = Tk()
    save_config_windows.title("Yellow Card Bot - Save config to file")
    save_config_windows.grid_rowconfigure(1, weight=1)
    save_config_windows.grid_columnconfigure(1, weight=1)
    save_config_windows.grid_columnconfigure(0, weight=1)
    ask = Label(save_config_windows, text="Do you want save configuration to file ?")

    def onclick_yes_button():
        write_config_to_file(bot_config_dict, main_gui_terminal)
        save_config_windows.destroy()
    
    def onclick_no_button():
        save_config_windows.destroy()

    yes_button = Button(save_config_windows, text="    YES   ", command=onclick_yes_button)
    no_button = Button(save_config_windows, text="    NO   ", command=onclick_no_button)
    ask.grid(row = 0, column=0, columnspan=2, pady=5, padx=5)
    yes_button.grid(row = 1, column=0, pady=5, padx=15, sticky="en")
    no_button.grid(row = 1, column=1, pady=5, padx=15, sticky="wn")

    save_config_windows.mainloop()

def enter_config(bot_config_dict, main_gui_terminal):
    config_gui = Tk()
    config_gui.title("Elo Server Bot - Configuration")
    config_gui.grid_rowconfigure(2, weight=1)
    config_gui.grid_columnconfigure(1, weight=1)
    config_gui.grid_columnconfigure(0, weight=1)

    oauth_token_label = Label(config_gui, text="Enter oAuth Token : ")#zadeklarowanie widgetow
    guild_id_label = Label(config_gui, text="Enter Guild ID : ")
    oauth_token_entry = Entry(config_gui)
    guild_id_entry = Entry(config_gui)

    correct_variable = [False, False] #zmienne potwierdzajace poprawne wpisanie wartosci do pol

    def onclick_enter_button():
        bot_config_dict["oauth_token"] = oauth_token_entry.get()
        if bot_config_dict["oauth_token"] == "":
            oauth_token_entry.insert(0, "Entered wrong value.")
        else:
            correct_variable[0] = True
        
        try:
            bot_config_dict["guild_id"] = int(guild_id_entry.get()) #pobranie tekstu z pola i zapisanie do slownika
            correct_variable[1] = True
        except ValueError:
            guild_id_entry.delete(0, 'end') #wyczyszczenie pola
            guild_id_entry.insert(0, "Entered wrong value.") #wpisanie tekstu do pola

        if correct_variable[0] and correct_variable[1]:
            sec = time.localtime() # get struct_time
            main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Configuration variables saved to memory.")
            config_gui.destroy() #zamkniecie okna/ przerwanie mainloop
            save_config_to_file_window(bot_config_dict, main_gui_terminal)      

    enter_button = Button(config_gui, text="    ENTER   ", command=onclick_enter_button)

    oauth_token_label.grid(row=0, column=0, pady=5, padx=10, sticky="e") #ustawienie widgetow w siatce
    guild_id_label.grid(row=1, column=0, pady=5, padx=10, sticky="e")
    oauth_token_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w") 
    guild_id_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")
    enter_button.grid(row=4, column=0, columnspan=2, padx=30, pady=30, sticky= "n")

    config_gui.mainloop()