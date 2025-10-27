"""Interaction event handler for the bot."""

import discord
from discord.ext import commands


class InteractionEvent(commands.Cog):
    """Interaction event cog."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """Handle all interactions with the bot."""
        if interaction.type == discord.InteractionType.application_command:
            print(
                f'[discord] "{interaction.command.name}" from '
                f'{interaction.user}/{interaction.guild.id if interaction.guild else "DM"}'
            )


async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(InteractionEvent(bot))
