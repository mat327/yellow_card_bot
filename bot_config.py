#Zaimplementowana funkcja do wprowadzania danych serwera i wartosci dotyczacych banow
#Dane zapisywane sa w formie slownika

import json
import os
import time

from tkinter import *

def load_config_from_file(main_gui_terminal):
    sec = time.localtime() # get struct_time
    main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Checking config file ...")
    filesize = os.path.getsize("server_ban_config.json") #rozmiar pliku
    if filesize == 0: #jezeli plik jest pusty funkcja nic nie robi
        main_gui_terminal.insert(END, "The file is empty.")
        server_ban_config = dict()
        return server_ban_config
    else:
        main_gui_terminal.insert(END, "Opening server_ban_config.json ...")
        try:
            config_file = open("server_ban_config.json", "r")
            server_ban_config_str = config_file.read() #odczyt z pliku jako str
            server_ban_config = json.loads(server_ban_config_str) #zmiana typu z str na dict
            config_file.close()
            main_gui_terminal.insert(END, "Data loaded to server memory, file closed.")
            return server_ban_config
        except:
            main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  [Error] Cannot open config file.")
            main_gui_terminal.itemconfig(END, fg = "red")
            server_ban_config = dict()
            return server_ban_config

def write_config_to_file(server_ban_config, main_gui_terminal):
    try:
        config_file = open("server_ban_config.json", "w")
        json.dump(server_ban_config, config_file)
        config_file.close()
        sec = time.localtime() # get struct_time
        main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Config file updated, file closed.")
    except:
        sec = time.localtime() # get struct_time
        main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  [Error] Cannot rewritte config file.")
        main_gui_terminal.itemconfig(END, fg = "red")

def save_config_to_file_window(server_ban_config, main_gui_terminal):
    save_config_windows = Tk()
    save_config_windows.title("Yellow Card Bot - Save config to file")
    ask = Label(save_config_windows, text="Do you want save configuration to file ?")

    def onclick_yes_button():
        write_config_to_file(server_ban_config, main_gui_terminal)
        save_config_windows.destroy()
    
    def onclick_no_button():
        save_config_windows.destroy()

    yes_button = Button(save_config_windows, text="    YES   ", command=onclick_yes_button)
    no_button = Button(save_config_windows, text="    NO   ", command=onclick_no_button)
    ask.grid(row = 0, column=0, columnspan=2, pady=5, padx=5)
    yes_button.grid(row = 1, column=0, pady=5, padx=5)
    no_button.grid(row = 1, column=1, pady=5, padx=5)

    save_config_windows.mainloop()

def enter_config(server_ban_config, main_gui_terminal):
    config_gui = Tk()
    config_gui.title("Yellow Card Bot - Configuration")

    oauth_token_label = Label(config_gui, text="Enter oAuth Token : ")#zadeklarowanie widgetow
    guild_id_label = Label(config_gui, text="Enter Guild ID : ")
    ban_duration_label = Label(config_gui, text="Enter ban duration in seconds : ")
    min_reaction_amount_label = Label(config_gui, text="Enter minimum amount of reaction to ban : ")
    oauth_token_entry = Entry(config_gui)
    guild_id_entry = Entry(config_gui)
    ban_duration_entry = Entry(config_gui)
    min_reaction_amount_entry = Entry(config_gui)

    correct_variable = [False, False, False, False] #zmienne potwierdzajace poprawne wpisanie wartosci do pol

    def onclick_enter_button():
        server_ban_config["oauth_token"] = oauth_token_entry.get()
        if server_ban_config["oauth_token"] == "":
            oauth_token_entry.insert(0, "Entered wrong value.")
        else:
            correct_variable[0] = True
        
        try:
            server_ban_config["guild_id"] = int(guild_id_entry.get()) #pobranie tekstu z pola i zapisanie do slownika
            correct_variable[1] = True
        except ValueError:
            guild_id_entry.delete(0, 'end') #wyczyszczenie pola
            guild_id_entry.insert(0, "Entered wrong value.") #wpisanie tekstu do pola

        try:
            server_ban_config["ban_duration"] = int(ban_duration_entry.get())
            correct_variable[2] = True
        except ValueError:
            ban_duration_entry.delete(0, 'end')
            ban_duration_entry.insert(0, "Entered wrong value.")

        try:
            server_ban_config["min_reaction_amount"] = int(min_reaction_amount_entry.get())
            correct_variable[3] = True
        except ValueError:
            min_reaction_amount_entry.delete(0, 'end')
            min_reaction_amount_entry.insert(0, "Entered wrong value.")

        if correct_variable[0] and correct_variable[1] and correct_variable[2] and correct_variable[3]:
            sec = time.localtime() # get struct_time
            main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Configuration variables saved to memory.")
            config_gui.destroy() #zamkniecie okna/ przerwanie mainloop
            save_config_to_file_window(server_ban_config, main_gui_terminal)      

    enter_button = Button(config_gui, text="    ENTER   ", command=onclick_enter_button)

    oauth_token_label.grid(row=0, column=0, pady=5, padx=10) #ustawienie widgetow w siatce
    guild_id_label.grid(row=1, column=0, pady=5, padx=10)
    ban_duration_label.grid(row=2, column=0, pady=5, padx=10)
    min_reaction_amount_label.grid(row=3, column=0, pady=5, padx=10)
    oauth_token_entry.grid(row=0, column=1, pady=5, padx=10) 
    guild_id_entry.grid(row=1, column=1, pady=5, padx=10)
    ban_duration_entry.grid(row=2, column=1, pady=5, padx=10)
    min_reaction_amount_entry.grid(row=3, column=1, pady=5, padx=10)
    enter_button.grid(row=4, column=0, columnspan=2, padx=30, pady=30)

    config_gui.mainloop()