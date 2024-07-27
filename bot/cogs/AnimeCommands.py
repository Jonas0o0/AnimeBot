# Anime Bot
# Copyright (c) Jonas0o0 2024
# 
# This software is licensed under the Anime Bot License.
# You may use, modify, and distribute this software under the terms of the Anime Bot License.
# See the LICENSE file for more details.

import discord
from discord import app_commands
from discord.ext import commands
from all_requests.jikanR import jikanRequests
import random
import config
from typing import Optional, Literal
from logging_config import get_logger

# Utilisez le logger configuré
logger = get_logger()

class AnimeCommands(commands.GroupCog, name="anime"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context.

    def RAMDOM_COLOR(self):
        return random.choice(config.COLOR)

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Anime Loaded")

    @app_commands.command()
    @app_commands.describe(day='The release date')
    async def schedules(self, interaction: discord.Interaction, day: config.DAYS):
        """List of anime that comes out every week"""
        all_anime = await jikanRequests().get_scheduls(day)
        channel = self.bot.get_channel(interaction.channel_id)
        color = self.RAMDOM_COLOR()
        await interaction.response.send_message("**[More info](https://myanimelist.net/anime/season/schedule)**", ephemeral=True)
        for anime in all_anime:
            url = anime['url']
            img = anime['img']

            tittle = anime['title']
            episode = anime['episodes']
            genre = anime['genres']
            status = anime['status']
            rank = anime['rank']
            embed = discord.Embed(title=f"N°{rank} : {tittle}", url=url, color=color)
            embed.set_image(url=img)
            embed.add_field(name=f"**Genre**", value=f"{genre}", inline=True)
            embed.add_field(name=f"**Status**", value=f"{status}", inline=True)
            embed.add_field(name=f"**Episode**", value=f"{episode}", inline=True)
            embed.set_footer(text="Explore, enjoy, and dive into the world of Anime and Musics with AnimeBot! 🌟")

            await channel.send(embed=embed)

    @app_commands.command()
    async def popular(self,interaction: discord.Interaction) -> None:
        """List of the most popular anime"""
        all_anime = await jikanRequests().get_anime_populaire()
        channel = self.bot.get_channel(interaction.channel_id)
        color = self.RAMDOM_COLOR()
        await interaction.response.send_message("**[More anime](https://myanimelist.net/topanime.php)**", ephemeral=True)
        for o in range(3):
            i = all_anime[o]
            url = i['url']
            img = i['img']

            tittle = i['title']
            episode = i['episodes']
            genre = i['genres']
            status = i['status']
            rank = i['rank']
            embed = discord.Embed(title=f"N°{rank} : {tittle}", url=url, color=color)
            embed.set_thumbnail(url=img)
            embed.add_field(name=f"**Genre**", value=f"{genre}", inline=True)
            embed.add_field(name=f"**Status**", value=f"{status}", inline=True)
            embed.add_field(name=f"**Episode**", value=f"{episode}", inline=True)
            embed.set_footer(text="Explore, enjoy, and dive into the world of Anime and Musics with AnimeBot! 🌟")

            await channel.send(embed=embed)

    @app_commands.command()
    async def recommendation(self,interaction: discord.Interaction) -> None:
        """An anime recommendation"""
        dico = await jikanRequests().get_anime_advice()
        dico = dico[0]
        embed = discord.Embed(title=f"{dico['title']}", url=dico['url'], color=self.RAMDOM_COLOR())
        embed.add_field(name="**Episodes**", value=dico['episodes'], inline=True)
        embed.add_field(name="**Status**", value=dico['status'], inline=True)
        embed.add_field(name="**Diffusion**", value=dico['diffuse'], inline=True)
        embed.add_field(name="**Genre**", value=dico['genres'], inline=False)
        embed.add_field(name="**Synopsis**", value=dico['synopsis'][:1023], inline=False)
        embed.add_field(name="**Producteur**",
                        value=f"{dico['producers']}", inline=True)
        embed.add_field(name="**Licence**",
                        value=f"{dico['licensors']}", inline=True)
        embed.add_field(name="**Studios**", value=f"{dico['studios']}",
                        inline=True)
        embed.set_thumbnail(url=dico['img'])
        embed.set_footer(text="Explore, enjoy, and dive into the world of Anime and Musics with AnimeBot! 🌟")

        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def random(self, interaction: discord.Interaction) -> None:
        """A random anime"""
        dico = await jikanRequests().get_anime_random()
        embed = discord.Embed(title=f"{dico['title']}", url=dico['url'], color=self.RAMDOM_COLOR())
        embed.add_field(name="**Episodes**", value=dico['episodes'], inline=True)
        embed.add_field(name="**Status**", value=dico['status'], inline=True)
        embed.add_field(name="**Diffusion**", value=dico['diffuse'], inline=True)
        embed.add_field(name="**Genre**", value=dico['genres'], inline=False)
        embed.add_field(name="**Synopsis**", value=dico['synopsis'][:1023], inline=False)
        embed.add_field(name="**Producteur**",
                        value=f"{dico['producers']}", inline=True)
        embed.add_field(name="**Licence**",
                        value=f"{dico['licensors']}", inline=True)
        embed.add_field(name="**Studios**", value=f"{dico['studios']}",
                        inline=True)
        embed.set_thumbnail(url=dico['img'])
        embed.set_footer(text="Explore, enjoy, and dive into the world of Anime and Musics with AnimeBot! 🌟")

        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.describe(name='Anime name')
    async def info(self,interaction: discord.Interaction, name: str) -> None:
        """Detailed information about an anime"""
        dico = await jikanRequests().get_anime_by_name(name)
        if type(dico) == str:
            await interaction.response.send_message(dico, ephemeral=True)
        else:
            embed = discord.Embed(title=f"{dico['title']}", url=dico['url'], color=self.RAMDOM_COLOR())
            embed.add_field(name="**Episodes**", value=dico['episodes'], inline=True)
            embed.add_field(name="**Status**", value=dico['status'], inline=True)
            embed.add_field(name="**Diffusion**", value=dico['diffuse'], inline=True)
            embed.add_field(name="**Genre**", value=dico['genres'], inline=False)
            embed.add_field(name="**Synopsis**", value=dico['synopsis'][:1023], inline=False)
            embed.add_field(name="**Producteur**",
                            value=f"{dico['producers']}", inline=True)
            embed.add_field(name="**Licence**",
                            value=f"{dico['licensors']}", inline=True)
            embed.add_field(name="**Studios**", value=f"{dico['studios']}",
                            inline=True)
            embed.set_thumbnail(url=dico['img'])
            embed.set_footer(text="Explore, enjoy, and dive into the world of Anime and Musics with AnimeBot! 🌟")

            await interaction.response.send_message(embed=embed)

    search = app_commands.Group(name="search", description="search an anime")

    @search.command()
    @app_commands.describe(genre='The first genre of anime', genre2='The second genre of anime', genre3='The third genre of anime', order_by='Anime order')
    async def by_genres(self, interaction: discord.Interaction, genre : config.GENRES, genre2 : Optional[config.GENRES], genre3 : Optional[config.GENRES], order_by : Literal["title", "start_date", "end_date", "episodes", "score", "scored_by", "rank", "popularity", "members", "favorites"]) -> None:
        """information about an anime by genres"""
        dico = await jikanRequests().get_anime_by_genre(genre,genre2, genre3, order_by)
        embed = discord.Embed(title=f"{dico['title']}", url=dico['url'], color=self.RAMDOM_COLOR())
        embed.add_field(name="**Episodes**", value=dico['episodes'], inline=True)
        embed.add_field(name="**Status**", value=dico['status'], inline=True)
        embed.add_field(name="**Diffusion**", value=dico['diffuse'], inline=True)
        embed.add_field(name="**Genre**", value=dico['genres'], inline=False)
        embed.add_field(name="**Synopsis**", value=dico['synopsis'][:1023], inline=False)
        embed.add_field(name="**Producteur**",
                        value=f"{dico['producers']}", inline=True)
        embed.add_field(name="**Licence**",
                        value=f"{dico['licensors']}", inline=True)
        embed.add_field(name="**Studios**", value=f"{dico['studios']}",
                        inline=True)
        embed.set_thumbnail(url=dico['img'])
        embed.set_footer(text="Explore, enjoy, and dive into the world of Anime and Musics with AnimeBot! 🌟")

        await interaction.response.send_message(embed=embed)

    @search.command()
    async def by_name(self, interaction: discord.Interaction, name: str) -> None:
        """information about an anime by name"""
        dico = await jikanRequests().get_anime_by_name(name)
        if type(dico) == str:
            await interaction.response.send_message(dico, ephemeral=True)
        else:
            embed = discord.Embed(title=f"{dico['title']}", url=dico['url'], color=self.RAMDOM_COLOR())
            embed.add_field(name="**Episodes**", value=dico['episodes'], inline=True)
            embed.add_field(name="**Status**", value=dico['status'], inline=True)
            embed.add_field(name="**Diffusion**", value=dico['diffuse'], inline=True)
            embed.add_field(name="**Genre**", value=dico['genres'], inline=False)
            embed.add_field(name="**Synopsis**", value=dico['synopsis'][:1023], inline=False)
            embed.add_field(name="**Producteur**",
                            value=f"{dico['producers']}", inline=True)
            embed.add_field(name="**Licence**",
                            value=f"{dico['licensors']}", inline=True)
            embed.add_field(name="**Studios**", value=f"{dico['studios']}",
                            inline=True)
            embed.set_thumbnail(url=dico['img'])
            embed.set_footer(text="Explore, enjoy, and dive into the world of Anime and Musics with AnimeBot! 🌟")
            
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AnimeCommands(bot))