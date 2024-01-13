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
    
        self.looping_task.start()

    @tasks.loop(minutes=1)
    async def looping_task(self):
        try:
            await self.client.wait_until_ready()
            print("Looping Task Started")

        except Exception as e:
            print(e)

async def setup(client):
    await client.add_cog(Tasks(client))