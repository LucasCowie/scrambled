"""Song command for the bot."""

import os
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp


class SongCommand(commands.Cog):
    """Song command cog."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="song",
        description="see the currently playing song if any to be displayed on stream, if stream."
    )
    async def song_command(self, interaction: discord.Interaction):
        """Display currently playing song."""
        try:
            payload = {
                'token': os.getenv('SCRAMBLED'),
                'force': True
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'http://[::]:3000/api/v1/spotify/now',
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    data = await response.json()
                    print('!!', data)
            
            embed = discord.Embed(
                title="song",
                description="see the currently playing song if any to be displayed on stream, if stream.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as ex:
            print(f'[discord] Error in song command: {ex}')
            await interaction.response.send_message(
                'An error occurred while fetching the song.',
                ephemeral=True
            )


async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(SongCommand(bot))
