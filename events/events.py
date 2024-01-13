import discord
from discord import app_commands
from discord.ext import commands
import traceback
from discord.app_commands import AppCommandError
from discord import Interaction
import os
from dotenv import load_dotenv

load_dotenv()

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot = client

    def cog_load(self):
        tree = self.client.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

    async def on_app_command_error(self, interaction: Interaction, error: AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message(content="You do not have permission to use this command")
        
        elif isinstance(error, discord.Forbidden):
            embedVar = discord.Embed(description=":x: **Missing Permissions**: Make sure I have the required permissions!")
            await interaction.response.send_message(embed=embedVar)

        elif isinstance(error, commands.CommandOnCooldown):
            time_until_cooldown_reset = error.retry_after
            await interaction.response.send_message(content=f"Slow down! You can try again after {round(time_until_cooldown_reset)} seconds!")

        elif isinstance(error, app_commands.CommandOnCooldown):
            time_until_cooldown_reset = error.retry_after
            await interaction.response.send_message(content=f"Slow down! You can try again after {round(time_until_cooldown_reset)} seconds!")
        else:
            embedVar = discord.Embed(title="An Error Occurred <:warning:919782406649700352>", description = "The error has been reported to staff.\nSorry for the inconvenience!", color=0xfbff00)
            embedVar.set_footer(text=f"RPG")
            try:
                await interaction.response.send_message(embed=embedVar)
            except Exception:
                await interaction.followup.send(embed=embedVar)
        
            tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            pages = TextPageSource(tb, max_size=1000).pages # paginates so it fits in a message
            msg = f"Command: `{interaction.command}`\nInvoker: `{interaction.user.name} ({interaction.user.id})`\nArguments: ctx.args\n{pages[0]}"
            error_channel = os.getenv('ERROR_CHANNEL')

            await self.client.get_channel(int(error_channel)).send(msg)
            for page in pages[1:]:
                await self.client.get_channel(int(error_channel)).send(page)

class TextPageSource:
    """ Get pages for text paginator """

    def __init__(self, text, *, prefix='```', suffix='```', max_size=2000):
        pages = commands.Paginator(prefix=prefix, suffix=suffix, max_size=max_size - 200)
        for line in text.split('\n'):
            pages.add_line(line)
        self._pages = pages

    @property
    def pages(self):
        return self._pages.pages

async def setup(client):
    await client.add_cog(Events(client))