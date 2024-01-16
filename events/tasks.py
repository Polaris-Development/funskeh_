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
        self.check_temp_roles.start()

    @tasks.loop(seconds=10)
    async def check_temp_roles(self):
        await self.client.wait_until_ready()
        try:
            temp_roles = await self.client.pool.fetch('''SELECT * FROM temproles''')
            for role in temp_roles:
                if time.time() > role['expire_time']:
                    guild = self.client.get_guild(role['guildid'])
                    member = guild.get_member(role['userid'])
                    role = guild.get_role(role['roleid'])
                    await member.remove_roles(role)
                    await self.client.pool.execute('''DELETE FROM temproles WHERE userid = $1 AND roleid = $2''', member.id, role.id)

        except Exception as e:
            print(e)
            traceback.print_exc()


async def setup(client):
    await client.add_cog(Tasks(client))