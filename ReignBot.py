import discord
import youtube_dl
from discord.ext import commands,tasks


class ReignBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        #subclass init of commands.Bot
        super().__init__(command_prefix=command_prefix, intents= intents)


