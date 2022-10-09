import requests


url = "https://discord.com/api/v10/applications/867485164400803890/commands"

# This is an example CHAT_INPUT or Slash Command, with a type of 1
json = {
    "name": "play",
    "type": 1,
    "description": "Play song on voice channel.",
    "options": [
        {"name": "author",
            "description": "Author of the song.",
            "type": 3,
            "required": True,
        },
        {"name": "title",
            "description": "Song title.",
            "type": 3,
            "required": True,
        }
    ]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot ODY3NDg1MTY0NDAwODAzODkw.GU_OGb.e9zmgivgPjIKMjptgXe6Ft48djRfMU19UHUM2o"
}

# or a client credentials token for your app with the applications.commands.update scope
#headers = {
#    "Authorization": "Bearer <my_credentials_token>"
#}

r = requests.post(url, headers=headers, json=json)

print(r)