from fileinput import filename
from tokenize import String
import discord
from discord.utils import get
from numpy import delete
from pytube import YouTube
from pytube import Playlist
import os
import time

playlist = list()

async def join_channel(ctx, client1):
    if (ctx.author.voice): # jesli osoba jest na kanale
        channel = ctx.author.voice.channel #kanal gdzie jest osoba
        await channel.connect() #wejdz na kanal
        await ctx.send("Hello everyone")
    else: #jesli osoby nie ma na kanale
        await ctx.send("You are not connected to a voice channel")

async def leave_channel(ctx, client1):
    if ctx.voice_client: # jesli bot jest na kanale
        vc = get(client1.voice_clients, guild=ctx.guild)
        if vc.is_paused() or vc.is_playing() : vc.stop()
        playlist.clear()
        await vc.disconnect()
        await ctx.send("See you next time")
    else: # jesli bot nie jest na kanale
        await ctx.send("I'm not in a voice channel")

async def download_song(ctx):
    try :
        destination = "songs/"
        out_file = playlist[0].streams.filter(only_audio=True).first().download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        global filename
        filename = new_file
    except:
        await ctx.send("Download failed, try again.")

async def init_play(ctx, url, client1):
    if ctx.author.voice: #czy uzytkownik jest na kanale glosowym
        if not ctx.voice_client: #czy bot jest na kanale glosowym
            await join_channel(ctx, client1)
        vc = get(client1.voice_clients, guild=ctx.guild)

        #dodawanie utwory do kolejki
        if 'playlist?' in url: 
            for vid in Playlist(str(url)).videos:
                playlist.append(vid)
        else :
            playlist.append(YouTube(str(url)))

        if vc.is_playing() or vc.is_paused():
            await ctx.send('Song/s added to queue') 
        else: 
            await ctx.send('Playing...') 
            await play_song(ctx, vc)
    else:
        await ctx.send("Please connect to a voice channel first.")

async def play_song(ctx, vc):
    while playlist: #dopoki sa pozycje na liscie
        await download_song(ctx) #pobiera piosenke           
        try:
            vc.play(discord.FFmpegPCMAudio(executable='C:/Users/Bialy/Dropbox/Komputer/Desktop/ffmpeg/bin/ffmpeg.exe', source=filename))
            while vc.is_playing() or vc.is_paused():
                time.sleep(1)
            delete_files_in_dir() #usuwa poprzedni plik
            playlist.pop(0) #usuwa pozycje z listy
        except:
            await ctx.send("Cannot find song.")

def delete_files_in_dir():
    dir = 'songs'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))