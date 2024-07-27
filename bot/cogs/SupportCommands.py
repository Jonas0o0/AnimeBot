# Anime Bot
# Copyright (c) Jonas0o0 2024
# 
# This software is licensed under the Anime Bot License.
# You may use, modify, and distribute this software under the terms of the Anime Bot License.
# See the LICENSE file for more details.

import discord
from discord import app_commands
from discord.ext import commands
import random
import Class.SugestionModal
import config
import Class
from logging_config import get_logger

# Utilisez le logger configuré
logger = get_logger()

class SupportCommands(commands.GroupCog, name="support"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context.

    def RAMDOM_COLOR(self):
        return random.choice(config.COLOR)

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Support Loaded")

    @app_commands.command()
    async def suggestion(self, interaction: discord.Interaction) -> None:
        """ Send us your sugestion """
        sugestion_modal = Class.SugestionModal.SugestionModal(self.bot)
        await interaction.response.send_modal(sugestion_modal)

    @app_commands.command()
    async def bug_report(self, interaction: discord.Interaction) -> None:
        """ Send us your bug """
        report_modal = Class.ReportModal.ReportModal(self.bot)
        await interaction.response.send_modal(report_modal)

    @app_commands.command()
    async def assistance(self, interaction: discord.Interaction) -> None:
        """Assistance"""
        embed = discord.Embed(title="Technical Assistance", description="To get assistance, please join our Discord server by following this link: https://discord.gg/WKksRrQ6cf\n\nOn our Discord server, you can ask questions, get help, engage with the community, and interact with our support team. We are here to assist you and address any concerns you may have. Join us now and become a part of our vibrant community!", url="https://discord.gg/WKksRrQ6cf", color=0x5DADE2)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SupportCommands(bot))