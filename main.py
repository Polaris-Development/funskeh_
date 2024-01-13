import asyncio
import os
import discord
from discord.ext import commands
import asyncpg
from dotenv import load_dotenv
load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
file_location = os.getenv('FILE_LOCATION')

intents = discord.Intents().all()
intents.message_content = True

async def load():
    for filename in os.listdir(f'{file_location}commands'):
        if filename.endswith('.py'):
            await client.load_extension(f'commands.{filename[:-3]}')
    for filename in os.listdir(f'{file_location}events'):
        if filename.endswith('.py'):
            await client.load_extension(f'events.{filename[:-3]}')


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        await load()

    async def on_ready(self):
        await client.change_presence(activity=discord.Game(name="👁️👁️"))
        print("Bot Online")
        await client.tree.sync()
        
client = DiscordBot()
client.pool = None

async def main():
    async with client:

        # user = os.getenv('DATABASE_USER')
        # database = os.getenv('DATABASE_DATABASE')
        # password = os.getenv('DATABASE_PASSWORD')
        
        # client.pool = await asyncpg.create_pool(
        #     host="localhost",
        #     database=database,
        #     user=user,
        #     password=password,
        #     min_size=10,
        #     max_size=2000,
        #     command_timeout=20)
        # print("Database opened!")

        # await client.pool.execute(
        #     '''CREATE TABLE IF NOT EXISTS players (
        #         id BIGINT
        # );''')

        try:
            await client.start(discord_token)
        except Exception as e:
            print(e.response.text)

asyncio.run(main())