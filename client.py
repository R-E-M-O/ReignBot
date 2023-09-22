import discord
import json
from discord.ext import commands

f = open('config.json')
data = json.load(f)

bot = commands.Bot(command_prefix= "/", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready")




bot.run(data['token'])