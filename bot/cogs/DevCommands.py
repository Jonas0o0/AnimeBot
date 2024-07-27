# Anime Bot
# Copyright (c) Jonas0o0 2024
# 
# This software is licensed under the Anime Bot License.
# You may use, modify, and distribute this software under the terms of the Anime Bot License.
# See the LICENSE file for more details.

import discord
from discord import app_commands
from discord.ext import commands
import config
import sys
import os
import traceback
from logging_config import get_logger

# Utilisez le logger configuré
logger = get_logger()

class DevCommands(commands.GroupCog, name="dev"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context.
        self.interaction = None

    async def extension_can_be_load_autocomplete(self, interaction: discord.Interaction, current: str):
        liste = []
        for cog in os.listdir("./cogs"):
            if cog.endswith('.py'):
                if f"cogs.{cog[:-3]}" not in self.bot.extensions.keys():
                    liste.append(cog[:-3])
        return [
            app_commands.Choice(name=extension_load, value=extension_load)
            for extension_load in liste if current.lower() in extension_load.lower()
        ]

    async def extension_can_be_unload_autocomplete(self, interaction: discord.Interaction, current: str):
        liste = []
        for cog in os.listdir("./cogs"):
            if cog.endswith('.py'):
                if f"cogs.{cog[:-3]}" in self.bot.extensions.keys():
                    liste.append(cog[:-3])
        return [
            app_commands.Choice(name=extension_unload, value=extension_unload)
            for extension_unload in liste if current.lower() in extension_unload.lower()
        ]

    async def extension_can_be_reload_autocomplete(self, interaction: discord.Interaction, current: str):
        liste = []
        for cog in os.listdir("./cogs"):
            if cog.endswith('.py'):
                if f"cogs.{cog[:-3]}" in self.bot.extensions.keys():
                    liste.append(cog[:-3])
        return [
            app_commands.Choice(name=extension_reload, value=extension_reload)
            for extension_reload in liste if current.lower() in extension_reload.lower()
        ]

    async def load_ex(self, extension):
        try:
            await self.bot.load_extension(f"cogs.{extension}")
            await self.interaction.edit_original_response(content=f"Cog : {extension} Loaded")
        except discord.ext.commands.ExtensionNotFound:
            await self.interaction.edit_original_response(f"Cog : {extension} not Found.")
        except discord.ext.commands.ExtensionAlreadyLoaded:
            await self.interaction.edit_original_response(f"Cog : {extension} already Loaded.")
        await self.bot.sync()

    async def unload_ex(self, extension):
        try:
            await self.bot.unload_extension(f"cogs.{extension}")
            await self.interaction.edit_original_response(content=f"Cog : {extension} Unloaded")
        except discord.ext.commands.ExtensionNotFound:
            await self.interaction.edit_original_response(f"Cog : {extension} not Found.")
        except discord.ext.commands.ExtensionNotLoaded:
            await self.interaction.edit_original_response(f"Cog : {extension} not Loaded.")
        await self.bot.sync()

    async def reload_ex(self, extension) -> None:
        try:
            await self.bot.reload_extension(f"cogs.{extension}")
            await self.interaction.edit_original_response(content=f"Cog : {extension} Reloaded")
        except discord.ext.commands.ExtensionNotFound:
            await self.interaction.edit_original_response(f"Cog : {extension} not Found.")
        except discord.ext.commands.ExtensionNotLoaded:
            await self.load_ex(extension)
        await self.bot.sync()

    async def reload_all(self) -> None:
        for cog in os.listdir('./cogs'):
            print("ok")
            if cog.endswith('.py'):
                print(cog[:-3])
                await self.reload_ex(f"{cog[:-3]}")
        await self.bot.sync()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Dev Loaded")

    @app_commands.command()
    @commands.is_owner()
    async def restart(self, interaction: discord.Interaction):
        """Restart the bot"""
        if self.bot.owner_id == interaction.user.id:
            await interaction.response.defer(thinking=True)
            await interaction.edit_original_response(content="Restarted!")
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            await interaction.response.send_message("Only my creator can use this command")

    @app_commands.command()
    @commands.is_owner()
    @app_commands.autocomplete(extension_load=extension_can_be_load_autocomplete)
    async def load(self, interaction: discord.Interaction, extension_load: str):
        """Load one Bot Extension"""
        if self.bot.owner_id == interaction.user.id:
            await interaction.response.defer(thinking=True)
            self.interaction = interaction
            await self.load_ex(extension_load)
        else:
            await interaction.response.send_message("Only my creator can use this command")

    @app_commands.command()
    @commands.is_owner()
    @app_commands.autocomplete(extension_unload=extension_can_be_unload_autocomplete)
    async def unload(self, interaction: discord.Interaction, extension_unload: str):
        """Unload one Bot Extension"""
        if self.bot.owner_id == interaction.user.id:
            await interaction.response.defer(thinking=True)
            self.interaction = interaction
            await self.unload_ex(extension_unload)
        else:
            await interaction.response.send_message("Only my creator can use this command")

    @app_commands.command()
    @commands.is_owner()
    @app_commands.autocomplete(extension_reload=extension_can_be_reload_autocomplete)
    async def reload(self, interaction: discord.Interaction, extension_reload: str):
        """Reload one Bot Extension"""
        if self.bot.owner_id == interaction.user.id:
            await interaction.response.defer(thinking=True)
            self.interaction = interaction
            await self.reload_ex(extension_reload)
        else:
            await interaction.response.send_message("Only my creator can use this command")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DevCommands(bot))
