# aqui va la logica de tu bot
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
import os
import asyncio
import logging



# Configurar el registro (logging), para que muestre los mensajes de nivel INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = Bot(command_prefix='>', description="Bot de ayuda", intents=intents, case_insensitive=True)

# Cargar todos los cogs en la carpeta cogs
async def load_cogs(bot):
    for filename in os.listdir('/app/cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: cogs.{filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load extension cogs.{filename[:-3]}: {e}')
            

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')            


async def main():
    await load_cogs(bot)
    await bot.start(token)


asyncio.run(main())

