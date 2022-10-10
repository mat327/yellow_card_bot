import requests


url = "https://discord.com/api/v10/applications/867485164400803890/commands"

# This is an example CHAT_INPUT or Slash Command, with a type of 1
json = {
    "name": "play",
    "type": 1,
    "description": "Play Youtube song/s.",
    "options": [
        {"name": "url",
            "description": "Song/s URL.",
            "type": 3,
            "required": True
        }
    ]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot <key>"
}

# or a client credentials token for your app with the applications.commands.update scope
#headers = {
#    "Authorization": "Bearer <my_credentials_token>"
#}

r = requests.post(url, headers=headers, json=json)

print(r)