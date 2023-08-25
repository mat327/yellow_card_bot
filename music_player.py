import asyncio
from fileinput import filename
import random
import discord
from discord.utils import get
from pytube import YouTube
from pytube import Playlist
import os

playlist = list()

async def join_channel(ctx, client1):
    if (ctx.author.voice): # jesli osoba jest na kanale
        if not (ctx.voice_client and ctx.voice_client.is_connected()):
            channel = ctx.author.voice.channel #kanal gdzie jest osoba
            await channel.connect() #wejdz na kanal
            await ctx.send("Hello everyone")
        else :
            await ctx.send("I'm on a voice channel")
    else: #jesli osoby nie ma na kanale
        await ctx.send("You are not connected to a voice channel")

async def leave_channel(ctx, client1):
    if not (ctx.voice_client and ctx.voice_client.is_connected()): # jesli bot jest na kanale
        vc = get(client1.voice_clients, guild=ctx.guild)
        if vc.is_paused() or vc.is_playing() : vc.stop()
        playlist.clear()
        await vc.disconnect()
        await ctx.send("See you next time")
    else: # jesli bot nie jest na kanale
        await ctx.send("I'm not on a voice channel")

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

def delete_files_in_dir():
    dir = 'songs'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

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
        #if not vc.is_playing() and not vc.is_paused():
            delete_files_in_dir() #usuwa poprzedni plik
            await download_song(ctx) #pobiera piosenke   
            playlist.pop(0) #usuwa pozycje z listy        
            try:
                music_src = discord.FFmpegPCMAudio(executable='ffmpeg', source=filename) #for linux just ffmpeg
                vc.play(music_src)
                while vc.is_playing() or vc.is_paused():
                    await asyncio.sleep(1)
            except:
                await ctx.send("Cannot find song.")

async def next_song(ctx, client1, amount):
    if ctx.voice_client: # jesli bot jest na kanale
        vc = get(client1.voice_clients, guild=ctx.guild)
        if playlist and len(playlist) >= amount:
            for i in range(amount-1):
                playlist.pop(0)
            vc.stop()
            await ctx.send("Song/s skipped")
        else :
            await ctx.send("Too many songs to skip")
    else: # jesli bot nie jest na kanale
        await ctx.send("I'm not in a voice channel")

async def show_playlist(ctx, client1):
    if playlist:
        async with ctx.typing():
            playlist_str = str(len(playlist)) + " songs in Playlist \n"
            if len(playlist) > 10 :
                for i in range(10):
                    playlist_str = playlist_str + str(i+1) + ". "+ playlist[i].title + "\n"
            else :
                for i in range(len(playlist)):
                    playlist_str = playlist_str + str(i+1) + ". "+ playlist[i].title + "\n"                
        await ctx.send(playlist_str)
    else:
        await ctx.send("Currently there are no songs in playlist.")

async def pause(ctx, client1):
    if ctx.voice_client: # jesli bot jest na kanale
        vc = get(client1.voice_clients, guild=ctx.guild)
        if vc.is_playing():
            vc.pause()
            await ctx.send("Song paused.")
        else :
            await ctx.send("No song is playing.")
    else: # jesli bot nie jest na kanale
        await ctx.send("I'm not in a voice channel")

async def resume(ctx, client1):
    if ctx.voice_client: # jesli bot jest na kanale
        vc = get(client1.voice_clients, guild=ctx.guild)
        if vc.is_paused():
            vc.resume()
            await ctx.send("Resumed.")
        else :
            await ctx.send("No song is paused.")
    else: # jesli bot nie jest na kanale
        await ctx.send("I'm not in a voice channel")

async def clear_playlist(ctx, client1):
 try:
    playlist.clear()
    await ctx.send("Playlist cleared.")
 except:
    await ctx.send("Cannot clear playlist, try again.")

async def change_order_in_playlist(ctx, client1):
 try:
    random.shuffle(playlist)
    await ctx.send("Playlist order changed.")
 except:
    await ctx.send("Cannot change playlist order, try again.")