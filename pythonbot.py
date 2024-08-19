import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
import os
import asyncio
import logging
import sys
from base.database import init_db  # Importar la función init_db

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar el registro (logging), para que muestre los mensajes de nivel INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = Bot(command_prefix='>', description="Bot de ayuda", intents=intents, case_insensitive=True)

# Inicializar la base de datos
init_db()

# Cargar todos los cogs en la carpeta cogs
async def load_cogs(bot):
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'cogs')):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: cogs.{filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load extension cogs.{filename[:-3]}: {e}')

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')

@bot.event
async def on_disconnect():
    logger.warning('Bot disconnected! Attempting to reconnect...')

@bot.event
async def on_resumed():
    logger.info('Bot resumed session successfully.')

async def main():
    while True:
        try:
            await load_cogs(bot)
            await bot.start(token)
        except Exception as e:
            logger.error(f'Error in main loop: {e}')
            await asyncio.sleep(5)  # Esperar 5 segundos antes de intentar reconectar

asyncio.run(main())

