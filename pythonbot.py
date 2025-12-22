import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
import os
import asyncio
import logging
import sys
from base.database import init_db  # Importar la función init_db
# DeepSeek se configura en el cog correspondiente

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar el registro (logging), para que muestre los mensajes de nivel INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar las variables de entorno
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
if deepseek_api_key:
    logger.info("DeepSeek API key found.")
else:
    logger.warning("DEEPSEEK_API_KEY not found in environment variables. DeepSeek commands may not work.")

# Configurar los intents del bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Crear una instancia del bot
bot = Bot(command_prefix='>', description="Bot de ayuda", intents=intents, case_insensitive=True)

# Inicializar la base de datos
init_db()

async def load_cogs(bot):
    """Carga todos los cogs en la carpeta cogs."""
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'cogs')):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: cogs.{filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load extension cogs.{filename[:-3]}: {e}')

@bot.event
async def on_ready():
    """Evento que se ejecuta cuando el bot está listo."""
    logger.info(f'Logged in as {bot.user}')
    # Configurar el estado del bot para que se vea en línea
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name=">ayuda para comandos")
    )

@bot.event
async def on_disconnect():
    """Evento que se ejecuta cuando el bot se desconecta."""
    logger.warning('Bot disconnected! Attempting to reconnect...')

@bot.event
async def on_resumed():
    """Evento que se ejecuta cuando el bot reanuda la sesión."""
    logger.info('Bot resumed session successfully.')

async def main():
    """Función principal que arranca el bot y maneja la reconexión."""
    while True:
        try:
            await load_cogs(bot)
            await bot.start(token)
        except discord.DiscordException as e:
            logger.error(f'Discord exception in main loop: {e}')
            await asyncio.sleep(5)  # Esperar 5 segundos antes de intentar reconectar
        except Exception as e:
            logger.error(f'Unexpected error in main loop: {e}')
            await asyncio.sleep(5)  # Esperar 5 segundos antes de intentar reconectar

if __name__ == '__main__':
    asyncio.run(main())

