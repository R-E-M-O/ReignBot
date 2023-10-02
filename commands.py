import json
import discord
from discord.ext import commands
from ReignBot import ReignBot
import youtube_dl

f = open('config.json')
data = json.load(f)

bot = ReignBot(command_prefix="/", intents=discord.Intents.all())

@bot.command(name='join')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not connected to a voice channel.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I am not connected to a voice channel.")

#useful commands for a music bot
@bot.command()
async def play(ctx, url):
    
    if url is None:
        await ctx.send("You must include a url.")
        return
    
    #if bot is not connected to a voice channel but url is valid, call join
    if not ctx.voice_client:
        await join(ctx)
    
    #play the song
    pass




bot.run(data['token'])