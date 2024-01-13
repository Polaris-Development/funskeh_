from discord.ext import commands, tasks
from handlers.calculations import *
import os
from dotenv import load_dotenv
from datetime import datetime
from handlers.calculations import *
import asyncio
import traceback

load_dotenv()

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client

async def setup(client):
    await client.add_cog(Tasks(client))