# Anime Bot
# Copyright (c) Jonas0o0 2024
# 
# This software is licensed under the Anime Bot License.
# You may use, modify, and distribute this software under the terms of the Anime Bot License.
# See the LICENSE file for more details.

import discord

class PaginationView(discord.ui.View):
    current_page : int = 0

    async def send(self, interaction):
        await interaction.response.defer()
        self.message = await interaction.followup.send(view=self)
        await self.update_embed(self.data[0], interaction)

    def create_embed(self, data, interaction):
        embed = discord.Embed(title=data["title"], color=0xF4D03F)
        for field in data["fields"]:
            embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.set_footer(text=data["footer"]["text"])
        return embed

    async def update_embed(self, data, interaction):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data, interaction), view=self)

    def update_buttons(self):
        if self.current_page == 0:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == int(len(self.data)-1):
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    @discord.ui.button(label='|<', style=discord.ButtonStyle.primary)
    async def first_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 0
        await self.update_embed(self.data[self.current_page], interaction)

    @discord.ui.button(label='<', style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_embed(self.data[self.current_page], interaction)

    @discord.ui.button(label='>', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_embed(self.data[self.current_page], interaction)

    @discord.ui.button(label='>|', style=discord.ButtonStyle.primary)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = int(len(self.data)-1)
        await self.update_embed(self.data[self.current_page], interaction)
