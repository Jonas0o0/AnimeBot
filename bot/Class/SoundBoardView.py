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

class SoundBoardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def update_button(self, interaction, payload=None):
        if payload:
            player = payload.player
        else:
            player = cast(wavelink.Player, interaction.guild.voice_client)
        button = self.pause_button
        if player.paused:
            button.label = "Resume"
            button.emoji = "▶️"
            button.style = discord.ButtonStyle.green
        else:
            button.label = "Pause"
            button.emoji = "⏸"
            button.style = discord.ButtonStyle.primary

        volum1 = player.volume + 5
        volum2 = player.volume - 5
        if volum1 > 1000:
            self.volume_up_button.disabled = True
        else:
            self.volume_up_button.disabled = False
        if volum2 < 0:
            self.volume_down_button.disabled = True
        else:
            self.volume_down_button.disabled = False

        self.skip_button.style = discord.ButtonStyle.primary
        self.shuffle_button.style = discord.ButtonStyle.primary

        if player.queue.mode == wavelink.QueueMode.loop :
            self.track_loop_button.label = "Normal"
            self.track_loop_button.style = discord.ButtonStyle.green
            self.track_loop_button.emoji = "➡️"
            self.queue_loop_button.label = "Queue Loop"
            self.queue_loop_button.style = discord.ButtonStyle.primary
            self.queue_loop_button.emoji = "🔁"
            
        elif player.queue.mode == wavelink.QueueMode.loop_all:
            self.track_loop_button.label = "Track Loop"
            self.track_loop_button.style = discord.ButtonStyle.primary
            self.track_loop_button.emoji = "🔂"
            self.queue_loop_button.label = "Normal"
            self.queue_loop_button.style = discord.ButtonStyle.green
            self.queue_loop_button.emoji = "➡️"

        elif player.queue.mode == wavelink.QueueMode.normal:
            self.track_loop_button.label = "Track Loop"
            self.track_loop_button.style = discord.ButtonStyle.primary
            self.track_loop_button.emoji = "🔂"
            self.queue_loop_button.label = "Queue Loop"
            self.queue_loop_button.style = discord.ButtonStyle.primary
            self.queue_loop_button.emoji = "🔁"

        await player.soundboard.edit(view = self)
    
    async def loop_manger(self, interaction, value):
        if value == 'Track Loop':
            return await self.music.fonction_loop(interaction, "track_loop")
        elif value == 'Queue Loop':
            return await self.music.fonction_loop(interaction, "queue_loop")
        else:
            return await self.music.fonction_loop(interaction, "normal")
        

    @discord.ui.button(label='Pause', emoji="⏸", style=discord.ButtonStyle.blurple, row=1)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = await self.music.fonction_resume_pause(interaction)
        await self.update_button(interaction)
        await self.music.delete_message(message)

    @discord.ui.button(label='Skip', emoji="⏩", style=discord.ButtonStyle.primary, row=1)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        self.skip_button.style = discord.ButtonStyle.green
        await player.soundboard.edit(view = self)
        message = await self.music.fonction_skip(interaction)
        await self.music.delete_message(message)
    
    @discord.ui.button(label='Shuffle Queue', emoji="🔀", style=discord.ButtonStyle.primary, row=1)
    async def shuffle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        self.shuffle_button.style = discord.ButtonStyle.green
        await player.soundboard.edit(view = self)
        message = await self.music.fonction_shuffle(interaction)
        await self.update_button(interaction)
        await self.music.delete_message(message)

    @discord.ui.button(label='Track Loop', emoji="🔂", style=discord.ButtonStyle.primary, row=2)
    async def track_loop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = await self.loop_manger(interaction, self.track_loop_button.label)
        await self.update_button(interaction)
        await self.music.delete_message(message)

    @discord.ui.button(label='Queue Loop', emoji="🔁", style=discord.ButtonStyle.primary, row=2)
    async def queue_loop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = await self.loop_manger(interaction, self.queue_loop_button.label)
        await self.update_button(interaction)
        await self.music.delete_message(message)

    @discord.ui.button(label='Queue Info', emoji="ℹ️", style=discord.ButtonStyle.gray, row=3)
    async def queue_info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = await self.music.fonction_queue_info(interaction)
        await self.update_button(interaction)
        await self.music.delete_message(message, 5)

    @discord.ui.button(label='Volum Down', emoji="🔉", style=discord.ButtonStyle.gray, row=3)
    async def volume_down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = await self.music.fonction_set_volume(interaction, -5)
        await self.update_button(interaction)
        await self.music.delete_message(message)
    
    @discord.ui.button(label='Volum Up', emoji="🔊", style=discord.ButtonStyle.gray, row=3)
    async def volume_up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = await self.music.fonction_set_volume(interaction, 5)
        await self.update_button(interaction)
        await self.music.delete_message(message)
        
    @discord.ui.button(label='Stop', emoji="⏹", style=discord.ButtonStyle.red, row=4)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.music.fonction_stop(interaction)