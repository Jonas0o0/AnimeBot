# Anime Bot
# Copyright (c) Jonas0o0 2024
# 
# This software is licensed under the Anime Bot License.
# You may use, modify, and distribute this software under the terms of the Anime Bot License.
# See the LICENSE file for more details.

import discord
from discord import app_commands
from discord.ext import commands
from Class import PaginationView
import json
from logging_config import get_logger

# Utilisez le logger configuré
logger = get_logger()

class HelpCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.data = json.load(open('HelpEmbeds.json'))

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Help Loaded")

    @app_commands.command()
    async def help(self, interaction: discord.Interaction) -> None:
        """Display help."""
        pagination_view = PaginationView.PaginationView()
        pagination_view.data = self.data["embeds"]
        await pagination_view.send(interaction=interaction)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HelpCommands(bot))
