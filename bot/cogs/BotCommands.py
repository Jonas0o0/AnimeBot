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
from logging_config import get_logger

# Utilisez le logger configuré
logger = get_logger()

        # embed = discord.Embed(title="Anime bot",
        #                       description="AnimeBot is your ultimate companion for exploring the world of anime. Whether you're a seasoned anime enthusiast or a newcomer to this captivating universe, AnimeBot is here to assist you in discovering, searching, and exploring a multitude of exciting anime.",
        #                       color=0xF0335E)
        # commandes = "`/help`"
        # embed.add_field(name="**Key Features : **", value=commandes, inline=False)
        # embed.add_field(name="**Invite AnimeBot**",
        #                 value="**[Click Here ! For invite AnimeBot.](https://discord.com/api/oauth2/authorize?client_id=1155549143570333826&permissions=8&scope=bot%20applications.commands)**",
        #                 inline=False)
        # embed.add_field(name="**Support and Contact:**",
        #                 value=f"**[Support server]({config.SUPPORT_SERVER})**\n\nCreator : **jonas0o0**",
        #                 inline=False)
        # embed.set_image(url="https://i.pinimg.com/originals/ed/64/e9/ed64e99481d843870d1e6b7d900f5e97.gif")
        # embed.set_thumbnail(url=self.bot.user.avatar.url)

class BotCommands(commands.GroupCog, name="bot"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Bot Loaded")
    
    def users_count(self):
            count = 0
            for guild in self.bot.guilds:
                count += guild.member_count
            return count

    @app_commands.command()
    async def info(self, interaction: discord.Interaction) -> None:
        """All the AnimeBot information you need to know"""
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
                "- **Anime Recommendations**: Personalized anime suggestions just for you.\n"
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
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BotCommands(bot))