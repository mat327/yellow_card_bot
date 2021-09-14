#Zaimplementowana funkcja do wprowadzania danych serwera i wartosci dotyczacych banow
#Dane zapisywane sa w formie slownika

def enter_config(server_ban_config):
    correct_variable= [False, False, False]
    server_ban_config["oauth_token"] = input("Enter oAuth Token : ")
    while correct_variable[0] == False:
        try:
            server_ban_config["guild_id"] = int(input("Enter Guild ID : "))
            correct_variable[0] = True
        except ValueError:
            print("Entered wrong value. Try again.")

    while correct_variable[1] == False:
        try:
            server_ban_config["ban_duration"] = int(input("Enter ban duration in seconds : "))
            correct_variable[1] = True
        except ValueError:
            print("Entered wrong value.")

    while correct_variable[2] == False:
        try:
            server_ban_config["min_reaction_amount"] = int(input("Enter minimum amount of reaction to ban : "))
            correct_variable[2] = True
        except ValueError:
            print("Entered wrong value.") 