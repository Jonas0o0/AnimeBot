# Anime Bot
# Copyright (c) Jonas0o0 2024
# 
# This software is licensed under the Anime Bot License.
# You may use, modify, and distribute this software under the terms of the Anime Bot License.
# See the LICENSE file for more details.

import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal
import config
import aiohttp
import random
import json
from logging_config import get_logger

# Utilisez le logger configuré
logger = get_logger()

class BotCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def RAMDOM_COLOR(self):
        return random.choice(config.COLOR)

    def users_count(self):
            count = 0
            for guild in self.bot.guilds:
                count += guild.member_count
            return count

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Server Loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id == 1155541987039137792:
            channel = self.bot.get_channel(1160589524607451318)
            embed = discord.Embed(title='New member !', description=f"__**Welcome, {member.mention}, on {member.guild.name}!** We're thrilled to have you with us.__", color=self.RAMDOM_COLOR())
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.system_channel:
            embed = discord.Embed(
            title="🎉 Hello, everyone! I'm AnimeBot, your ultimate Anime and Music companion! 🎉",
            description=(
                "I'm here to help you Discover, Search, and Enjoy Your Tracks and Explore the exciting world of anime. Whether you're a newbie or a seasoned fan, "
                "I've got the tools you need to discover and enjoy anime to the fullest."
            ),
            color=0x00ff00  # A green color for the embed
            )
            
            embed.add_field(
                name="__Key Features__",
                value=(
                    "- **Anime Search**: Easily find anime by keywords or genres.\n"
                    "- **Popular Anime**: Stay updated with the highest-rated anime.\n"
                    "- **Random Anime**: Get surprised with a random anime.\n"
                    "- **Detailed Information**: Get comprehensive details about any anime.\n"
                    "- **Anime Recommendations**: Personalized anime suggestions just for you."
                    "- **Play a Song**\n"
                    "- **Skip the Song**\n"
                    "- **Resume Playback**\n"
                    "- **Pause Playback**\n"
                    "- **Adjust Volume**\n"
                    "- **Disconnect Player**\n"
                    "- **Change Loop Mode**\n"
                ),
                inline=False
            )

            embed.add_field(
                name="__Commands__",
                value=(
                    "</help:1169748403081728112>"
                ),
                inline=False
            )

            embed.add_field(
                name="__Technical Information__",
                value=(
                    f"- **Servers**: {len(self.bot.guilds)}\n"
                    f"- **Users**: {self.users_count()}\n"
                    "- **Language**: Python\n"
                    "- **Library**: discord.py, wavelink\n"
                    "- **API Used**: Jikan (MyAnimeList API), Lavalink\n"
                    f"- **Version**: {config.VERSION}\n"
                    "- **Developer**: jonas0o0"
                ),
                inline=False
            )

            embed.add_field(
                name="__Join Our Community__",
                value=(
                    f"Support Server: [Join Now]({config.SUPPORT_SERVER})\n"
                    "Creator: **jonas0o0**"
                ),
                inline=False
            )

            embed.set_thumbnail(url="https://i.pinimg.com/originals/ed/64/e9/ed64e99481d843870d1e6b7d900f5e97.gif")
            embed.set_footer(text="Explore, enjoy, and dive into the world of Anime and Musics with AnimeBot! 🌟")
            
            await guild.system_channel.send(embed=embed)

    @app_commands.command()
    @commands.is_owner()
    async def rules(self, interaction: discord.Interaction):
        if self.bot.owner_id == interaction.user.id:
            await interaction.response.send_message("Rules not define", ephemeral=True)
        else:
            await interaction.response.send_message("Only my creator can use this command")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BotCommands(bot))