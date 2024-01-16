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


class WhoIs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="View a user's info")
    async def whois(self, interaction, member: discord.Member):
        await interaction.response.defer()
        if not member:  # if member is not mentioned
            member = interaction.message.author  # set member as the author
        roles = [role for role in member.roles if role.name != "@everyone"]
        embed = discord.Embed(colour=discord.Colour.purple(), title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f"Requested by {interaction.user}")

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        if roles:
            embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
            embed.add_field(name="Highest Role:", value=roles[-1].mention)
        else:
            embed.add_field(name="Roles:", value="No roles")
            embed.add_field(name="Highest Role:", value="No roles")

        await interaction.followup.send(embed=embed)

async def setup(client):
    await client.add_cog(WhoIs(client))