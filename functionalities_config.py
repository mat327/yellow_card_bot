import json
import os
import time

import tkinter as tk

def enter_config(functionalities_config_dict, main_gui_terminal):
    functionalities_gui = tk.Tk()
    functionalities_gui.title("Elo Server Bot - On/Off Functionalities")
    functionalities_gui.grid_rowconfigure(7, weight=1)
    functionalities_gui.grid_columnconfigure(0, weight=1)

    ban_func_check_var = tk.IntVar(functionalities_gui, value=functionalities_config_dict["ban_func"])
    ban_cmd_check_var = tk.IntVar(functionalities_gui, value=functionalities_config_dict["ban_cmd"])
    drink_cmd_check_var = tk.IntVar(functionalities_gui, value=functionalities_config_dict["drink_cmd"])
    cat_cmd_check_var = tk.IntVar(functionalities_gui, value=functionalities_config_dict["cat_cmd"])
    dog_cmd_check_var = tk.IntVar(functionalities_gui, value=functionalities_config_dict["dog_cmd"])
    music_player_check_var = tk.IntVar(functionalities_gui, value=functionalities_config_dict["music_player"])

    def onclick_enter_button():
        functionalities_config_dict["ban_func"] = ban_func_check_var.get()
        functionalities_config_dict["ban_cmd"] = ban_cmd_check_var.get()
        functionalities_config_dict["drink_cmd"] = drink_cmd_check_var.get()
        functionalities_config_dict["cat_cmd"] = cat_cmd_check_var.get()
        functionalities_config_dict["dog_cmd"] = dog_cmd_check_var.get()
        functionalities_config_dict["music_player"] = music_player_check_var.get()

        sec = time.localtime() # get struct_time
        main_gui_terminal.insert(tk.END, time.strftime("%d/%m/%Y, %H:%M:%S", sec) + "  Functionalities status :")
        
        for x, y in functionalities_config_dict.items():
            if y == 1:
                main_gui_terminal.insert(tk.END, x + " : " + "On\n")
            else:
                main_gui_terminal.insert(tk.END, x + " : " + "Off\n")

        functionalities_gui.destroy() #zamkniecie okna/ przerwanie mainloop   

    ban_func_check_button = tk.Checkbutton(functionalities_gui, text="Ban for cards", variable=ban_func_check_var)
    ban_cmd_check_button = tk.Checkbutton(functionalities_gui, text="Command /bans", variable=ban_cmd_check_var)
    drink_cmd_check_button  = tk.Checkbutton(functionalities_gui, text="Command /drink", variable=drink_cmd_check_var)
    cat_cmd_check_button  = tk.Checkbutton(functionalities_gui, text="Command /cat", variable=cat_cmd_check_var)
    dog_cmd_check_button  = tk.Checkbutton(functionalities_gui, text="Command /dog", variable=dog_cmd_check_var)
    music_player_check_button  = tk.Checkbutton(functionalities_gui, text="Music Player", variable=music_player_check_var)

    enter_button = tk.Button(functionalities_gui, text="    ENTER   ", command=onclick_enter_button)

    ban_func_check_button.grid(row=0, column=0, pady=5, padx=70, sticky="w") #ustawienie widgetow w siatce
    ban_cmd_check_button.grid(row=1, column=0, pady=5, padx=70, sticky="w")
    drink_cmd_check_button.grid(row=2, column=0, pady=5, padx=70, sticky="w")
    cat_cmd_check_button.grid(row=3, column=0, pady=5, padx=70, sticky="w")
    dog_cmd_check_button.grid(row=4, column=0, pady=5, padx=70, sticky="w")
    music_player_check_button.grid(row=5, column=0, pady=5, padx=70, sticky="w")

    enter_button.grid(row=6, column=0, columnspan=2, padx=30, pady=30, sticky= "n")

    functionalities_gui.mainloop()