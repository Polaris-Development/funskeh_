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

class Verify(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="Verify Command!")
    async def verify(self, interaction, user: discord.Member, cross: Literal["Yes", "No"], trans: Literal["Yes", "No"], gf_nb: Literal["Yes", "No"], male_or_female: Literal["Male", "Female", "N/A"]):
        try:
            ADMIN_ROLE = int(os.getenv("ADMIN_ROLE"))
            admin_role = interaction.guild.get_role(ADMIN_ROLE)
            if admin_role not in interaction.user.roles:
                embed = discord.Embed(description=":x: This is an admin only command!", color=discord.colour.Colour.red())
                return await interaction.response.send_message(embed=embed)
            
            WELCOME_ROLE = int(os.getenv("WELCOME_ROLE"))
            WELCOME_CHANNEL = int(os.getenv("WELCOME_CHANNEL"))
            LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
            VERIFIED_ROLE = int(os.getenv("VERIFIED_ROLE"))
            CROSS_ROLE = int(os.getenv("CROSS_ROLE"))
            TRANS_ROLE = int(os.getenv("TRANS_ROLE"))
            GF_NB_ROLE = int(os.getenv("GF_NB_ROLE"))
            MALE_ROLE = int(os.getenv("MALE_ROLE"))
            FEMALE_ROLE = int(os.getenv("FEMALE_ROLE"))


            # Give user roles
            await user.add_roles(interaction.guild.get_role(VERIFIED_ROLE))
            if cross == "Yes":
                await user.add_roles(interaction.guild.get_role(CROSS_ROLE))
            if trans == "Yes":
                await user.add_roles(interaction.guild.get_role(TRANS_ROLE))
            if gf_nb == "Yes":
                await user.add_roles(interaction.guild.get_role(GF_NB_ROLE))
            if male_or_female == "Male":
                await user.add_roles(interaction.guild.get_role(MALE_ROLE))
            if male_or_female == "Female":
                await user.add_roles(interaction.guild.get_role(FEMALE_ROLE))

            # Welcome Message
            welcome_channel = self.client.get_channel(WELCOME_CHANNEL)
            embed = discord.Embed(
                title=f"Welcome to {interaction.guild.name}", 
                description=(
                    f"{user.mention} is now verified! Let's welcome them!\n\n"
                    f"Feel free to explore the server and if you haven't select some roles in <#881701916626587136>!\nEnjoy"
                ), 
                color=0xe681c7
            )
            embed.set_footer(text=f"Bot made for exclusive use in {interaction.guild.name}")
            embed.set_thumbnail(url=interaction.guild.icon)
            await welcome_channel.send(f"<@&{WELCOME_ROLE}>", embed=embed)

            # Log Message
            log_channel = self.client.get_channel(LOG_CHANNEL)
            embed = discord.Embed(
                title=f"New user verification!", 
                description=(
                    f"User Verified: {user.mention}\n"
                    f"Staff: {interaction.user.mention}\n\n"
                    f"Account creation date: {user.created_at.strftime('%d/%m/%Y')}"
                ), 
                color=0xe681c7
            )
            embed.set_footer(text=f"Bot made for exclusive use in {interaction.guild.name}")
            embed.set_thumbnail(url=interaction.guild.icon)
            await log_channel.send(embed=embed)
        except Exception as e:
            logger.exception("Exception Occured while code Execution: "+ str(e))

    @app_commands.command(description="ID Verification Embed!")
    async def idverification(self, interaction):
        embed = discord.Embed(
            title="ID Verification", 
            description=(
                "Please send a picture of your ID in <#881701916626587136>.\n"
                "If you are not comfortable with that, please DM a staff member."
            ), 
            color=0xe681c7
        )
        embed.set_footer(text=f"Bot made for exclusive use in {interaction.guild.name}")
        embed.set_thumbnail(url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Cross Verification Embed!")
    async def crossverification(self, interaction):
        embed = discord.Embed(
            title="Cross Verification", 
            description=(
                "Please send a picture of your ID in <#881701916626587136>.\n"
                "If you are not comfortable with that, please DM a staff member."
            ), 
            color=0xe681c7
        )
        embed.set_footer(text=f"Bot made for exclusive use in {interaction.guild.name}")
        embed.set_thumbnail(url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(Verify(client))