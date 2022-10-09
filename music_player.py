import youtube_dl
import discord
from discord.utils import get
import os

async def download_song(ctx, url, author, title):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'songs/'+author+' - '+title+'.mp3',
        'noplaylist': True,
        'continue_dl': True,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #await ctx.send("Downloading song ...")
            async with ctx.typing():
                ydl.cache.remove()
                info_dict = ydl.extract_info(url, download=False)
                ydl.prepare_filename(info_dict)
                ydl.download([url])
            await ctx.send("Song downloaded complete")
            return True
    except Exception:
        await ctx.send("Download failed, try again.")
        return False

async def play_song(ctx, author, title, client1):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        vc = get(client1.voice_clients, guild=ctx.guild)
        try:
            await ctx.send('songs/'+author+' - '+title+'.mp3')
            vc.play(discord.FFmpegPCMAudio(executable='C:/Users/Bialy/Dropbox/Komputer/Desktop/ffmpeg/bin/ffmpeg.exe', source='D:/Boty_discord_python/yellow_card_bot/songs/'+author+' - '+title+'.mp3'))
        except:
            await ctx.send("Cannot find song.")
    else:
        await ctx.send("Please connect to a voice channel first.")