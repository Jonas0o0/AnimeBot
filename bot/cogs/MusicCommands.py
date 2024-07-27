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
import wavelink
from typing import cast, Literal
import time 
import asyncio
from Class.SoundBoardView import SoundBoardView
from logging_config import get_logger

# Utilisez le logger configuré
logger = get_logger()

class MusicCommands(commands.GroupCog, name="music"):
    def __init__(self, bot: commands.Bot, color = 0xE9A6EA) -> None:
        self.bot = bot
        self.embed_error = discord.Embed(color=color,title="Nothing is Playing !", description=":pensive: Songs must be playing to use that command. The queue is currently empty! Add songs using: </music play:1260202505938407515> command.")
        self.embed_voice_error = discord.Embed(color=color,title="You aren't in voice channel !", description=":pensive: To do this you must join the voice channel.")
        self.view = SoundBoardView()
        self.view.music = self
        self.color = color
        super().__init__()  # this is now required in this context.

    def voice_check(self, interaction):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        channel = player.channel.id
        return channel == interaction.user.voice.channel.id

    async def delete_message(self, meassage, time=2):
        if meassage:
            await asyncio.sleep(time)
            await meassage.delete()

    async def fonction_queue_info(self, interaction):
        await interaction.response.defer()
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            await interaction.followup.send(embed=self.embed_error)
            return
        if not self.voice_check(interaction):
            await interaction.followup.send(embed=self.embed_voice_error)
            return

        track = player.current
        position = player.position

        count = player.queue.count
        history = player.queue.history

        queuetime = 0
        for track_item in player.queue:
            queuetime += track_item.length

        embed = discord.Embed(color=self.color)
        embed.set_author(name=f"Queue Information", icon_url = interaction.user.avatar.url)
        embed.description = f"**[{track}]({track.uri})** [`{time.strftime('%M:%S', time.gmtime(track.length/1000))}`] by `{track.author}`\n\n"
        if track.artwork:
            embed.set_thumbnail(url=track.artwork)
        embed.add_field(name="Information: ", value=f"[`{time.strftime('%M:%S', time.gmtime((track.length-position)/1000))}`] remaining \n **{history.count}**th track out of **{history.count + count}** tracks\n Queue Time : [`{time.strftime('%H:%M:%S', time.gmtime(queuetime/1000))}`]")
        message = await interaction.followup.send(embed=embed)
        return message

    async def fonction_skip(self, interaction):
        await interaction.response.defer()
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            await interaction.followup.send(embed=self.embed_error)
            return
        if not self.voice_check(interaction):
            await interaction.followup.send(embed=self.embed_voice_error)
            return
        
        if player.queue.count == 0:
            embed = discord.Embed(color=self.color, title=":pensive: There is nothing in the queue.")
            message = await interaction.followup.send(embed=embed)
            return message


        await player.skip(force=True)

        embed = discord.Embed(color=self.color, description=":ok_hand: Skipped the current song.")
        message = await interaction.followup.send(embed=embed)
        return message
    
    async def fonction_resume_pause(self, interaction):
        await interaction.response.defer()
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            await interaction.followup.send(embed=self.embed_error)
            return
        if not self.voice_check(interaction):
            await interaction.followup.send(embed=self.embed_voice_error)
            return

        info = not player.paused

        await player.pause(info)

        if info:
            val="Paused" 
        else:
            val="Resumed"
        
        embed = discord.Embed(color=self.color)
        embed.set_author(name=f"Music {val}", icon_url = interaction.user.avatar.url)
        message = await interaction.followup.send(embed=embed)
        return message

    async def fonction_stop(self, interaction):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            await interaction.response.send_message(embed=self.embed_error)
            return
        if not self.voice_check(interaction):
            await interaction.followup.send(embed=self.embed_voice_error)
            return

        await player.soundboard.delete()
        await player.disconnect()
        
        embed = discord.Embed(color=self.color)
        embed.set_author(name=f"{interaction.user.name} has just stop the playback !", icon_url = interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    
    async def fonction_set_volume(self, interaction, value:int, set=None):
        await interaction.response.defer()
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            await interaction.followup.send(embed=self.embed_error)
            return
        if not self.voice_check(interaction):
            await interaction.followup.send(embed=self.embed_voice_error)
            return

        if set:
            await player.set_volume(value)
        else:
            await player.set_volume(player.volume + value)

        
        embed = discord.Embed(color=self.color)
        embed.set_author(name=f"Volum set at {player.volume}", icon_url = interaction.user.avatar.url)
        message = await interaction.followup.send(embed=embed)
        
        return message

    async def fonction_shuffle(self, interaction):
        await interaction.response.defer()
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            await interaction.response.send_message(embed=self.embed_error)
            return
        if not self.voice_check(interaction):
            await interaction.followup.send(embed=self.embed_voice_error)
            return
        player.queue.shuffle()
        embed = discord.Embed(color=self.color)
        embed.set_author(name=f'Queue has been mixed', icon_url = interaction.user.avatar.url)
        message = await interaction.followup.send(embed=embed)
        
        return message

    async def fonction_loop(self, interaction, loop):
        await interaction.response.defer()
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            await interaction.response.send_message(embed=self.embed_error)
            return
        if not self.voice_check(interaction):
            await interaction.followup.send(embed=self.embed_voice_error)
            return

        if loop == "track_loop":
            player.queue.mode= wavelink.QueueMode.loop 
            val = "Track Loop"
        elif loop == "queue_loop":
            player.queue.mode = wavelink.QueueMode.loop_all
            val = "Queue Loop"
        else:
            player.queue.mode = wavelink.QueueMode.normal
            val = "Normal"

        
        embed = discord.Embed(color=self.color)
        embed.set_author(name=f'Queue Mode set at "{val}"', icon_url = interaction.user.avatar.url)
        message = await interaction.followup.send(embed=embed)
        
        return message

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Music Loaded")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logger.info("Wavelink Node connected: %r | Resumed: %s", payload.node, payload.resumed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        bot_member = member.guild.get_member(self.bot.user.id)
        if bot_member.voice and bot_member.voice.channel:
            member_in_channel = len(bot_member.voice.channel.members)
            if member_in_channel == 1:
                for channel in self.bot.voice_clients:
                    if channel.channel.id == before.channel.id:
                        player: wavelink.Player = cast(wavelink.Player, channel)
                        if not player:
                            await channel.disconnect()
                            return

                        await player.soundboard.delete()
                        await player.disconnect()
                                        

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        embed: discord.Embed = discord.Embed(title="Now Playing : ", color=self.color)
        embed.description = f"**[{track}]({track.uri})** [`{time.strftime('%M:%S', time.gmtime(track.length/1000))}`] by `{track.author}`\n\n"
        embed.set_footer(text="Use the buttons below to control the music")

        if track.artwork:
            embed.set_thumbnail(url=track.artwork)

        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"

        if track.album.name:
            embed.add_field(name="Album", value=track.album.name)

        if hasattr(player, "soundboard"):
            await player.soundboard.delete()

        player.soundboard = await player.home.send(embed=embed, view=self.view)
        await self.view.update_button(interaction=None, payload=payload)

    @app_commands.command()
    async def play(self, interaction, query: str) -> None:
        """Play a song with the given query."""
        if not interaction.guild:
            return

        player: wavelink.Player
        player = cast(wavelink.Player, interaction.guild.voice_client)  # type: ignore

        if not player:
            try:
                player = await interaction.user.voice.channel.connect(cls=wavelink.Player)  # type: ignore
            except AttributeError:
                await interaction.response.send_message("Please join a voice channel first before using this command.")
                return
            except discord.ClientException:
                await interaction.response.send_message("I was unable to join this voice channel. Please try again.")
                return

        # Turn on AutoPlay to enabled mode.
        # enabled = AutoPlay will play songs for us and fetch recommendations...
        # partial = AutoPlay will play songs for us, but WILL NOT fetch recommendations...
        # disabled = AutoPlay will do nothing...
        player.autoplay = wavelink.AutoPlayMode.partial

        # Lock the player to this channel...
        if not hasattr(player, "home"):
            player.home = interaction.channel
        elif player.home != interaction.channel:
            await interaction.response.send_message(f"You can only play songs in {player.home.mention}, as the player has already started there.")
            return

        # This will handle fetching Tracks and Playlists...
        # Seed the doc strings for more information on this method...
        # If spotify is enabled via LavaSrc, this will automatically fetch Spotify tracks if you pass a URL...
        # Defaults to YouTube for non URL based queries...
        tracks: wavelink.Search = await wavelink.Playable.search(query)
        if not tracks:
            await interaction.response.send_message(f"{interaction.user.mention} - Could not find any tracks with that query. Please try again.")
            return

        if isinstance(tracks, wavelink.Playlist):
            # tracks is a playlist...
            added: int = await player.queue.put_wait(tracks)

            embed = discord.Embed(color=self.color)
            embed.set_author(name=f"Added the Playlist to Queue ({added} songs)", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            track: wavelink.Playable = tracks[0]

            await player.queue.put_wait(track)
            embed = discord.Embed(color=self.color, description=f"**[{track}]({track.uri})** [`{time.strftime('%M:%S', time.gmtime(track.length/1000))}`]")
            embed.set_author(name=f"Added the Song to Queue #{player.queue.count}", icon_url = interaction.user.avatar.url)
            if track.artwork:
                embed.set_thumbnail(url=track.artwork)
            await interaction.response.send_message(embed=embed)

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(track=player.queue.get(), volume=30)
            #await player.play(player.queue.get(), volume=30)



    @app_commands.command()
    async def skip(self, interaction) -> None:
        """Skip the current song."""
        message = await self.fonction_skip(interaction)
        await self.delete_message(message)

    #@app_commands.command()
    #async def nightcore(self, ctx: commands.Context) -> None:
    #    """Set the filter to a nightcore style."""
     #   player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
     #   if not player:
    #        return
#
     #   filters: wavelink.Filters = player.filters
    #    filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
     #   await player.set_filters(filters)
#
     #   await ctx.message.add_reaction("\u2705")


    @app_commands.command()
    async def resume(self, interaction) -> None:
        """Resume the Player depending on its current state."""
        message = await self.fonction_resume_pause(interaction)
        await self.delete_message(message)

    @app_commands.command()
    async def pause(self, interaction) -> None:
        """Pause the Player depending on its current state."""
        message = await self.fonction_resume_pause(interaction)
        await self.delete_message(message)

    @app_commands.command()
    async def volume(self, interaction, value:int) -> None:
        """Change the volume of the player."""
        message = await self.fonction_set_volume(interaction, value, True)
        await self.delete_message(message)

    @app_commands.command()
    async def disconnect(self, interaction) -> None:
        """Disconnect the Player."""
        await self.fonction_stop(interaction)

    @app_commands.command()
    async def loop(self, interaction, choice: Literal["track_loop", "queue_loop", "normal"]) -> None:
        """Change the "Loop Mode" of the player."""
        message = await self.fonction_loop(interaction, choice)
        await self.delete_message(message)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MusicCommands(bot))
