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


class Temprole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="View a user's warnings!")
    async def temprole(self, interaction, user: discord.Member, role: discord.Role, times: str):
        await interaction.response.defer()

        admin_role = interaction.guild.get_role(ADMIN_ROLE)
        if admin_role not in interaction.user.roles:
            embed = discord.Embed(description=":x: This is an admin only command!", color=discord.colour.Colour.red())
            return await interaction.followup.send(embed=embed)
        
        # Give user a role and place in database
        times = convert_time(times) + time.time()
        try:
            await user.add_roles(role)
            await self.client.pool.execute("INSERT INTO temproles VALUES ($1, $2, $3, $4, $5)", user.id, interaction.user.id, role.id, times, interaction.guild.id)
            embed = discord.Embed(description=f":white_check_mark: {user.mention} has been given the {role.name} role!", color=discord.colour.Colour.green())
            await interaction.followup.send(embed=embed)

            # Log Warn
            log_channel = self.client.get_channel(LOG_CHANNEL)
            embed = discord.Embed(description=f"{user.mention} has been given the {role.name} role!", color=discord.colour.Colour.green())
            embed.add_field(name="Given By:", value=interaction.user.mention)
            await log_channel.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(description=":x: I don't have permission to give members roles!", color=discord.colour.Colour.red())
            await interaction.followup.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(description=":x: An error occurred while trying to give the member a role!", color=discord.colour.Colour.red())
            await interaction.followup.send(embed=embed)

async def setup(client):
    await client.add_cog(Temprole(client))