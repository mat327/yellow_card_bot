import requests


url = "https://discord.com/api/v10/applications/867485164400803890/commands"

# This is an example CHAT_INPUT or Slash Command, with a type of 1
json = {
    "name": "bans",
    "type": 1,
    "description": "Displays the current user ban statistics",
    "options": [
        {
            "name": "sort_by",
            "description": "Sort user ban statistics by ...",
            "type": 3,
            "required": False,
            "choices": [
                {
                    "name": "Amount",
                    "value": "amount"
                },
                {
                    "name": "Time",
                    "value": "time"
                },
                {
                    "name": "Username",
                    "value": "username"
                }
            ]
        }
    ]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot ODY3NDg1MTY0NDAwODAzODkw.GCqr9F.Jq-c96ZQOsSPjkC3r51U-uRVP5H05rt2msHaD8"
}

# or a client credentials token for your app with the applications.commands.update scope
#headers = {
#    "Authorization": "Bearer <my_credentials_token>"
#}

r = requests.post(url, headers=headers, json=json)

print(r)