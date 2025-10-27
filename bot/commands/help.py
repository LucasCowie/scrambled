"""Help command for the bot."""

import discord
from discord import app_commands
from discord.ext import commands


class HelpCommand(commands.Cog):
    """Help command cog."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="print information on how to use this bot")
    async def help_command(self, interaction: discord.Interaction):
        """Display help information."""
        embed = discord.Embed(
            title="help",
            description="print information on how to use this bot",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(HelpCommand(bot))
