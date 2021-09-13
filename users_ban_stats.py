import discord
from discord.ext import commands
from discord.utils import get
import asyncio

async def stats(ctx, client1, banned_messages):
    stats = {}
    messages = await ctx.channel.history().flatten()
    for message_id in banned_messages: #utworzenie dict z listy zbanowanych wiadomosci
        try :
            for x in messages:
                if x.id == message_id:
                    message = x
            member = message.author
            if member.id in stats:
                stats[member.id] += stats[member.id]
            else :
                stats[member.id] = 1
        except :
            print("Cannot find banned message.")

    await ctx.send("Users Ban Statistic:")
    for user_id, cards in stats.items():
        user = client1.get_user(user_id)
        time =  cards * 15
        await ctx.send(user.display_name + " - " + str(cards) + "   |   " + str(time) + " minutes")