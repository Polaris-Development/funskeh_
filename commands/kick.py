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


class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="Kick Command!")
    async def kick(self, interaction, user: discord.Member, reason: str):
        await interaction.response.defer()

        admin_role = interaction.guild.get_role(ADMIN_ROLE)
        if admin_role not in interaction.user.roles:
            embed = discord.Embed(description=":x: This is an admin only command!", color=discord.colour.Colour.red())
            return await interaction.followup.send(embed=embed)
        
        try:
            try:
                embed = discord.Embed(description=f"You have been kicked from {interaction.guild.name} for {reason}!", color=discord.colour.Colour.red())
                await user.send(embed=embed)
            except Exception:
                pass

            await user.kick(reason=reason)
            embed = discord.Embed(description=f":white_check_mark: {user.mention} has been kicked!", color=discord.colour.Colour.green())
            await interaction.followup.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(description=":x: I don't have permission to kick members!", color=discord.colour.Colour.red())
            await interaction.followup.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(description=":x: An error occurred while trying to kick the member!", color=discord.colour.Colour.red())
            await interaction.followup.send(embed=embed)

async def setup(client):
    await client.add_cog(Kick(client))