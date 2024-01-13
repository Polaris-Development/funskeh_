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
        await interaction.response.defer()
        ADMIN_ROLE = int(os.getenv("ADMIN_ROLE"))
        admin_role = interaction.guild.get_role(ADMIN_ROLE)
        if admin_role not in interaction.user.roles:
            embed = discord.Embed(description=":x: This is an admin only command!", color=discord.colour.Colour.red())
            return await interaction.followup.send(embed=embed)
        
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
        try:
            await user.add_roles(interaction.guild.get_role(VERIFIED_ROLE))
        except Exception:
            return await interaction.followup.send("Invalid verified role id!")
        if cross == "Yes":
            try:
                await user.add_roles(interaction.guild.get_role(CROSS_ROLE))
            except Exception:
                return await interaction.followup.send("Invalid cross role id!")
        if trans == "Yes":
            try:
                await user.add_roles(interaction.guild.get_role(TRANS_ROLE))
            except Exception:
                return await interaction.followup.send("Invalid trans role id!")
        if gf_nb == "Yes":
            try:
                await user.add_roles(interaction.guild.get_role(GF_NB_ROLE))
            except Exception:
                return await interaction.followup.send("Invalid gf_nb role id!")
        if male_or_female == "Male":
            try:
                await user.add_roles(interaction.guild.get_role(MALE_ROLE))
            except Exception:
                return await interaction.followup.send("Invalid male role id!")
        if male_or_female == "Female":
            try:
                await user.add_roles(interaction.guild.get_role(FEMALE_ROLE))
            except Exception:
                return await interaction.followup.send("Invalid female role id!")

        # Welcome Message
        welcome_channel = self.client.get_channel(WELCOME_CHANNEL)
        embed = discord.Embed(
            title=f"Welcome to {interaction.guild.name}", 
            description=(
                f"{user.mention} is now verified! Let's welcome them!\n\n"
                f"Feel free to explore the server and if you haven't select some roles in <#1135880320839856258> <#1135880338275577968> <#1135880400812646410>!\nEnjoy"
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

        # Success Message
        embed = discord.Embed(title="Verification Complete!", description=(f"{user.mention} is now verified!"), color=0xe681c7)
        await interaction.followup.send(embed=embed)  


    @app_commands.command(description="ID Verification Embed!")
    async def idverification(self, interaction):
        embed = discord.Embed(
            title="How to ID verify!", 
            description=(
                "Open a ticket <#1065352947359305738>.\n"
                ""
                "1 | Send a selfie of you and your Identification.."
                "2 | Write down the server name + todays date on a piece of paper together with your id."
                "3 | Then a selfie of you holding the id or the paper. After confirmed from staff you can delete your pictures!"
                ""
                "Make sure all the sensitive information is blurred over except date of birth and your picture."
                "No filters, emotes etc. We need clear pictures!"
                "We will not force verify you. Verifying is optional but to stay in our server you gotta prove you are above the age of 18. The server is 18+ and you know it while joining."
                "If we suspect you are under the age of 18 we have the right to kick or ban you. Note that staff can ask for more pictures if we are suspicious of you being under age."
                ""
                "MAKE SURE YOU HAVE SELECTED <#1135880320839856258>.\n"
                "Other options of verification is <#1065352876664307773>.\n"
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