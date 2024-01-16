import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View
import logging
from handlers.calculations import *
import time
import asyncio
from typing import Literal
import os

from dotenv import load_dotenv
load_dotenv()

logger=logging.getLogger()

ADMIN_ROLE = int(os.getenv("ADMIN_ROLE"))
WELCOME_ROLE = int(os.getenv("WELCOME_ROLE"))
WELCOME_CHANNEL = int(os.getenv("WELCOME_CHANNEL"))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
VERIFIED_ROLE = int(os.getenv("VERIFIED_ROLE"))
CROSS_ROLE = int(os.getenv("CROSS_ROLE"))
TRANS_ROLE = int(os.getenv("TRANS_ROLE"))
GF_NB_ROLE = int(os.getenv("GF_NB_ROLE"))
MALE_ROLE = int(os.getenv("MALE_ROLE"))
FEMALE_ROLE = int(os.getenv("FEMALE_ROLE"))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))


class Steal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="Steal Emoji Command!")
    async def steal(self, interaction, emoji: str):
        await interaction.response.defer()

        try:
            print
            print(emoji)
            # Example: <:crown:1196840025145479231>
            emoji_id = int(emoji.split(":")[2][:-1])
            print(emoji_id)
            emoji = self.client.get_emoji(emoji_id)
            print(emoji.url)
            await interaction.followup.send(emoji.url)



        except Exception:
            embed = discord.Embed(description=":x: Invalid emoji!", color=discord.colour.Colour.red())
            return await interaction.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(Steal(client))