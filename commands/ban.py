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


class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="Ban Command!")
    async def ban(self, interaction, user: discord.Member, reason: str):
        await interaction.response.defer()
        
        admin_role = interaction.guild.get_role(ADMIN_ROLE)
        if admin_role not in interaction.user.roles:
            embed = discord.Embed(description=":x: This is an admin only command!", color=discord.colour.Colour.red())
            return await interaction.followup.send(embed=embed)
        
        
        try:
            await self.client.pool.execute("INSERT INTO banlist VALUES ($1, $2, $3, $4)", user.id, interaction.user.id, reason, time.time())
            try:
                embed = discord.Embed(description=f"You have been banned from {interaction.guild.name} for {reason}!", color=discord.colour.Colour.red())
                await user.send(embed=embed)
            except Exception:
                pass

            await user.ban(reason=reason)
            embed = discord.Embed(description=f":white_check_mark: {user.mention} has been banned!", color=discord.colour.Colour.green())
            await interaction.followup.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(description=":x: I don't have permission to ban members!", color=discord.colour.Colour.red())
            await interaction.followup.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(description=":x: An error occurred while trying to ban the member!", color=discord.colour.Colour.red())
            await interaction.followup.send(embed=embed)

    @app_commands.command(description="Banlist Command!")
    async def banlist(self, interaction):
        await interaction.response.defer()

        admin_role = interaction.guild.get_role(ADMIN_ROLE)
        if admin_role not in interaction.user.roles:
            embed = discord.Embed(description=":x: This is an admin only command!", color=discord.colour.Colour.red())
            return await interaction.followup.send(embed=embed)
        
        # Get Banlist
        banlist = await self.client.pool.fetch("SELECT * FROM banlist")
        embed = discord.Embed(description=f"**Banlist**", color=discord.colour.Colour.green())
        for ban in banlist:
            embed.add_field(name=f"Ban #{banlist.index(ban) + 1}", value=f"**User**: <@{ban['userid']}>\n**Reason:** {ban['reason']}\n**Banned By:** <@{ban['staffid']}>\n**Time:** {time.ctime(ban['time'])}")
        await interaction.followup.send(embed=embed)

async def setup(client):
    await client.add_cog(Ban(client))