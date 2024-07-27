# Anime Bot
# Copyright (c) Jonas0o0 2024
# 
# This software is licensed under the Anime Bot License.
# You may use, modify, and distribute this software under the terms of the Anime Bot License.
# See the LICENSE file for more details.

import discord
from discord.ext import commands
import config

class SugestionModal(discord.ui.Modal, title="Send us your suggestion"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context.

    fbt_tile = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Title",
        required=True,
        placeholder="Give a title for your suggestion"
    )
    message = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Title",
        required=True,
        max_length=1000,
        placeholder="Give a description/explication for your suggestion"
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        channel = self.bot.get_channel(config.SUGESTION_CH)
        embed = discord.Embed(title=f"Title : {self.fbt_tile.value}", description=f"Description : {self.message.value}", color=0x5DADE2)
        embed.add_field(name="User", value=f"Name : {interaction.user.name}\nID : {interaction.user.id}")
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await channel.send(embed=embed)
        await interaction.response.send_message("Thanks for this suggestion", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error) -> None:
        print(error)