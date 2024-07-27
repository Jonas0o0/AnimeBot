# Anime Bot
# Copyright (c) Jonas0o0 2024
# 
# This software is licensed under the Anime Bot License.
# You may use, modify, and distribute this software under the terms of the Anime Bot License.
# See the LICENSE file for more details.

import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
from config import *
import random
import wavelink
import os
from logging_config import setup_logging, get_logger

# Initialisez la configuration du logger au démarrage de l'application
setup_logging()

# Utilisez le logger configuré
logger = get_logger()

class AnimeBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=commands.when_mentioned_or('>'), intents=intents, owner_id=757618515451838546)

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))
        logger.info("Logged in: %s | %s", self.user, self.user.id)
        nbr = 0
        for guild in bot.guilds:
            nbr += guild.member_count
        logger.info("Use by %s members", nbr)
        logger.info("On %s servers", len(bot.guilds))

    async def load_all(self):
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{cog[:-3]}")
                except Exception as error_name:
                    print(f"Error Loding cog {cog} : {error_name}")

    def def_satatus(self):
        op = random.randint(0,3)
        if op == 0:
            return f'| v{VERSION} | /help'
        elif op == 1:
            nbr = len(bot.guilds)
            return f'| On {nbr} servers | /help'
        elif op == 2:
            return '| /music | /anime | /help'
        elif op == 3:
            nbr = 0
            for guild in bot.guilds:
                nbr += guild.member_count
            return f'| Use by {nbr} members | /help'

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.wait_until_ready()
        status = [f'| v{VERSION} | /help', f'| On {len(self.guilds)} servers | /help', '| /music | /anime | /help']
        nbr = 0
        for guild in bot.guilds:
            nbr += guild.member_count
        status.append(f'| Use by {nbr} members | /help')
        await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(status)))

    async def setup_hook(self) -> None:
        # Register the persistent view for listening here.
        # Note that this does not send the view to any message.
        # In order to do this you need to first send a message with the View, which is shown below.
        # If you have the message_id you can also pass it as a keyword argument, but for this example
        # we don't have one.
        nodes = [wavelink.Node(uri="http://127.0.0.1:2333", password=LAVALINK_PASSWORD)]

        # cache_capacity is EXPERIMENTAL. Turn it off by passing None
        await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100)
        self.change_status.start()
        await self.load_all()
        await self.sync()

    async def sync(self):
        await self.tree.sync()

intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True
bot = AnimeBot(intents=intents)


bot.run(TOKEN)
