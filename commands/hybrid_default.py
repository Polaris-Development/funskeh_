import discord
from discord.ext import commands
from discord.ui import View
import logging
from handlers.calculations import *
import time
import asyncio

from dotenv import load_dotenv
load_dotenv()

logger=logging.getLogger()

class PrefixDefault(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command(description="View the help command!")
    async def help(self, ctx):
        try:
            embed = discord.Embed(
                title="Help Menu",
                description=f"/help - Shows the help menu", 
                color=0xfbff00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

async def setup(client):
    await client.add_cog(PrefixDefault(client))