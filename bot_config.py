#Zaimplementowana funkcja do wprowadzania danych serwera i wartosci dotyczacych banow
#Dane zapisywane sa w formie slownika

from tkinter import *

def enter_config(server_ban_config):
    root = Tk()
    root.title("Yellow Card Bot")

    oauth_token_label = Label(root, text="Enter oAuth Token : ")#zadeklarowanie widgetow
    guild_id_label = Label(root, text="Enter Guild ID : ")
    ban_duration_label = Label(root, text="Enter ban duration in seconds : ")
    min_reaction_amount_label = Label(root, text="Enter minimum amount of reaction to ban : ")
    oauth_token_entry = Entry(root)
    guild_id_entry = Entry(root)
    ban_duration_entry = Entry(root)
    min_reaction_amount_entry = Entry(root)

    correct_variable = [False, False, False, False] #zmienne potwierdzajace poprawne wpisanie wartosci do pol

    def onclick_connect_button():
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
            root.destroy() #zamkniecie okna/ przerwanie mainloop

    connect_button = Button(root, text="Connect", command=onclick_connect_button)

    oauth_token_label.grid(row=0, column=0, pady=5, padx=10) #ustawienie widgetow w sietce
    guild_id_label.grid(row=1, column=0, pady=5, padx=10)
    ban_duration_label.grid(row=2, column=0, pady=5, padx=10)
    min_reaction_amount_label.grid(row=3, column=0, pady=5, padx=10)
    oauth_token_entry.grid(row=0, column=1, pady=5, padx=10) 
    guild_id_entry.grid(row=1, column=1, pady=5, padx=10)
    ban_duration_entry.grid(row=2, column=1, pady=5, padx=10)
    min_reaction_amount_entry.grid(row=3, column=1, pady=5, padx=10)
    connect_button.grid(row=4, column=0, columnspan=2, padx=30, pady=30)

    root.mainloop()