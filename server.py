import discord
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio, PCMVolumeTransformer


client = commands.Bot(command_prefix='.')  # prefix our commands with '.'

players = {}


guild_id = 
channel_id = 

@client.event
async def on_ready():
    print('Bot online')
    await join()


# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
async def join():
    channel = client.get_channel(id=channel_id)
    voice = get(client.voice_clients, guild=client.get_guild(id=guild_id))
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# command to play sound from a youtube URL
async def play(url, volume):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    voice = get(client.voice_clients, guild=client.get_guild(id=guild_id))

    if not voice.is_playing():
        voice.play(PCMVolumeTransformer(FFmpegPCMAudio("sounds/" + url), volume/100))

        voice.is_playing()
    else:
        return


# command to resume voice if it is paused
@client.command()
async def resume():
    voice = get(client.voice_clients, guild=client.get_guild(id=guild_id))

    if not voice.is_playing():
        voice.resume()


# command to pause voice if it is playing
async def pause():
    voice = get(client.voice_clients, guild=client.get_guild(id=guild_id))

    if voice.is_playing():
        voice.pause()


# command to stop voice
async def stop():
    voice = get(client.voice_clients, guild=client.get_guild(id=guild_id))

    if voice.is_playing():
        voice.stop()

import socket
import asyncio
import threading

def main():
    s = socket.socket()
    host = '0.0.0.0'
    port = 12345
    s.bind((host, port))
    s.listen(5)
    print('Server started')
    while True:
        c, addr = s.accept()
        threading.Thread(target=handle_client, args=(c,)).start()

def handle_client(client_socket):
    vol = 100
    while True:
        cmd = client_socket.recv(1024**2).decode().splitlines()
        if not cmd:
            break
        for c in cmd:
            if c == '\n' or c == '':
                continue
            if c.startswith('play'):
                asyncio.run(play(c[5:], vol))
            elif c.startswith('pause'):
                asyncio.run(pause())
            elif c.startswith('resume'):
                asyncio.run(resume())
            elif c.startswith('stop'):
                asyncio.run(stop())
            elif c.startswith('ls'):
                client_socket.sendall("\n".join(os.listdir("sounds")).encode())
            elif c.startswith('vol'):
                vol = int(c[4:])

threading.Thread(target=main).start()

client.run("OTQxNzc3NDA0Nzk0MzkyNjI3.Yga4jg.QABd1IuXwfVhgmt_-aEi4fUkck8")