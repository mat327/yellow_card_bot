#Zaimplementowana funkcja do wprowadzania wartosci dotyczacych banow
#Dane zapisywane sa w formie slownika

import json
import os
import time

from tkinter import *

def load_config_from_file(main_gui_terminal):
    sec = time.localtime() # get struct_time
    main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Checking config file ...")
    filesize = os.path.getsize("ban_func_config.json") #rozmiar pliku
    if filesize == 0: #jezeli plik jest pusty funkcja nic nie robi
        main_gui_terminal.insert(END, "The file is empty.")
        ban_func_config_dict = dict()
        return ban_func_config_dict
    else:
        main_gui_terminal.insert(END, "Opening ban_func_config.json ...")
        try:
            config_file = open("ban_func_config.json", "r")
            ban_func_config_dict_str = config_file.read() #odczyt z pliku jako str
            ban_func_config_dict = json.loads(ban_func_config_dict_str) #zmiana typu z str na dict
            config_file.close()
            main_gui_terminal.insert(END, "Data loaded to server memory, file closed.")
            return ban_func_config_dict
        except:
            main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  [Error] Cannot open config file.")
            main_gui_terminal.itemconfig(END, fg = "red")
            ban_func_config_dict = dict()
            return ban_func_config_dict

def write_config_to_file(ban_func_config_dict, main_gui_terminal):
    try:
        config_file = open("ban_func_config.json", "w")
        json.dump(ban_func_config_dict, config_file)
        config_file.close()
        sec = time.localtime() # get struct_time
        main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Config file updated, file closed.")
    except:
        sec = time.localtime() # get struct_time
        main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  [Error] Cannot rewritte config file.")
        main_gui_terminal.itemconfig(END, fg = "red")

def save_config_to_file_window(ban_func_config_dict, main_gui_terminal):
    save_config_windows = Tk()
    save_config_windows.title("Yellow Card Bot - Save config to file")
    save_config_windows.grid_rowconfigure(1, weight=1)
    save_config_windows.grid_columnconfigure(1, weight=1)
    save_config_windows.grid_columnconfigure(0, weight=1)
    ask = Label(save_config_windows, text="Do you want save configuration to file ?")

    def onclick_yes_button():
        write_config_to_file(ban_func_config_dict, main_gui_terminal)
        save_config_windows.destroy()
    
    def onclick_no_button():
        save_config_windows.destroy()

    yes_button = Button(save_config_windows, text="    YES   ", command=onclick_yes_button)
    no_button = Button(save_config_windows, text="    NO   ", command=onclick_no_button)
    ask.grid(row = 0, column=0, columnspan=2, pady=5, padx=5)
    yes_button.grid(row = 1, column=0, pady=5, padx=15, sticky="en")
    no_button.grid(row = 1, column=1, pady=5, padx=15, sticky="wn")

    save_config_windows.mainloop()

def enter_config(ban_func_config_dict, main_gui_terminal):
    config_gui = Tk()
    config_gui.title("Elo Server Bot - Configuration")
    config_gui.grid_rowconfigure(2, weight=1)
    config_gui.grid_columnconfigure(1, weight=1)
    config_gui.grid_columnconfigure(0, weight=1)

    ban_duration_label = Label(config_gui, text="Enter ban duration in seconds : ")
    min_reaction_amount_label = Label(config_gui, text="Enter minimum amount of reaction to ban : ")
    ban_duration_entry = Entry(config_gui)
    min_reaction_amount_entry = Entry(config_gui)

    correct_variable = [False, False] #zmienne potwierdzajace poprawne wpisanie wartosci do pol

    def onclick_enter_button():
        try:
            ban_func_config_dict["ban_duration"] = int(ban_duration_entry.get())
            correct_variable[0] = True
        except ValueError:
            ban_duration_entry.delete(0, 'end')
            ban_duration_entry.insert(0, "Entered wrong value.")

        try:
            ban_func_config_dict["min_reaction_amount"] = int(min_reaction_amount_entry.get())
            correct_variable[1] = True
        except ValueError:
            min_reaction_amount_entry.delete(0, 'end')
            min_reaction_amount_entry.insert(0, "Entered wrong value.")

        if correct_variable[0] and correct_variable[1]:
            sec = time.localtime() # get struct_time
            main_gui_terminal.insert(END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Configuration variables saved to memory.")
            config_gui.destroy() #zamkniecie okna/ przerwanie mainloop
            save_config_to_file_window(ban_func_config_dict, main_gui_terminal)      

    enter_button = Button(config_gui, text="    ENTER   ", command=onclick_enter_button)

    ban_duration_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")
    min_reaction_amount_label.grid(row=3, column=0, pady=5, padx=10, sticky="e")
    ban_duration_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")
    min_reaction_amount_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")
    enter_button.grid(row=4, column=0, columnspan=2, padx=30, pady=30, sticky= "n")

    config_gui.mainloop()