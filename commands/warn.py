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


class Warn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="Warn a user!")
    async def warn(self, interaction, user: discord.Member, reason: str):
        await interaction.response.defer()

        admin_role = interaction.guild.get_role(ADMIN_ROLE)
        if admin_role not in interaction.user.roles:
            embed = discord.Embed(description=":x: This is an admin only command!", color=discord.colour.Colour.red())
            return await interaction.followup.send(embed=embed)
        
        # Warn User
        try:
            try:
                embed = discord.Embed(description=f"You have been warned in {interaction.guild.name} for {reason}!", color=discord.colour.Colour.red())
                await user.send(embed=embed)
            except Exception:
                pass

            await self.client.pool.execute("INSERT INTO warnings VALUES ($1, $2, $3, $4)", user.id, interaction.user.id, reason, time.time())
            embed = discord.Embed(description=f":white_check_mark: {user.mention} has been warned!", color=discord.colour.Colour.green())
            await interaction.followup.send(embed=embed)

            # Log Warn
            log_channel = self.client.get_channel(LOG_CHANNEL)
            embed = discord.Embed(description=f"{user.mention} has been warned!", color=discord.colour.Colour.green())
            embed.add_field(name="Reason:", value=reason)
            embed.add_field(name="Warned By:", value=interaction.user.mention)
            await log_channel.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(description=":x: I don't have permission to warn members!", color=discord.colour.Colour.red())
            await interaction.followup.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(description=":x: An error occurred while trying to warn the member!", color=discord.colour.Colour.red())
            await interaction.followup.send(embed=embed)

    @app_commands.command(description="View a user's warnings!")
    async def warnings(self, interaction, user: discord.Member = None):
        await interaction.response.defer()

        if user == None:
            user = interaction.user

        warnings = await self.client.pool.fetch("SELECT * FROM warnings WHERE userid = $1", user.id)
        embed = discord.Embed(description=f"**{user.name}'s Warnings**", color=discord.colour.Colour.green())
        for warning in warnings:
            embed.add_field(name=f"Warning #{warnings.index(warning) + 1}", value=f"**Reason:** {warning['reason']}\n**Warned By:** <@{warning['staffid']}>\n**Time:** {time.ctime(warning['time'])}")
        await interaction.followup.send(embed=embed)

async def setup(client):
    await client.add_cog(Warn(client))