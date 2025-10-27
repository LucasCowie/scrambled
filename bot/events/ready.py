"""Ready event handler for the bot."""

import os
import discord
from discord.ext import commands


class ReadyEvent(commands.Cog):
    """Ready event cog."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Handle bot ready event."""
        try:
            guild = self.bot.get_guild(int(os.getenv('WUMPUS_GUILD')))
            
            if guild:
                print(
                    f'[discord] logged into "{guild.name}" [{guild.id}] '
                    f'as "{self.bot.user.name}#{self.bot.user.discriminator}"'
                )
            else:
                print(f'[discord] logged in as "{self.bot.user.name}"')
            
            # Sync slash commands
            print('[discord] Syncing application commands...')
            await self.bot.tree.sync()
            print('[discord] Application commands synced')
            
            # TODO: Import calendar and check forum events
            # print('[discord] checking calendar data')
            # calendar_data = await calendar()
            # await check_existing_forum_events(...)
            
            # TODO: Start calendar monitoring daemon
            # await start_calendar_monitor(self.bot)
            
        except Exception as ex:
            print(f'[discord] bot unable to start: {ex}')


async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(ReadyEvent(bot))
