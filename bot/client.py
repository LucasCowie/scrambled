"""Discord bot client for Scrambled."""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord.ext import commands
from helpers.get_commands import get_commands

load_dotenv()

# Setup bot with intents
intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    """Load all command cogs and event handlers."""
    # Load commands
    commands_path = Path(__file__).parent / 'commands'
    command_files = [f for f in commands_path.glob('*.py') if f.name != '__init__.py']
    
    for command_file in command_files:
        try:
            await bot.load_extension(f'commands.{command_file.stem}')
            print(f'[discord] Loaded command: {command_file.stem}')
        except Exception as e:
            print(f'[discord] Failed to load {command_file.stem}: {e}')
    
    # Load events
    events_path = Path(__file__).parent / 'events'
    event_files = [f for f in events_path.glob('*.py') if f.name != '__init__.py']
    
    for event_file in event_files:
        try:
            await bot.load_extension(f'events.{event_file.stem}')
            print(f'[discord] Loaded event: {event_file.stem}')
        except Exception as e:
            print(f'[discord] Failed to load {event_file.stem}: {e}')

async def main():
    """Main bot startup function."""
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('WUMPUS_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())
