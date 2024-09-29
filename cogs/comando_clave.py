# cogs/comando_clave.py
#aqui se importa el diccionario de palabras clave
# tratando de yaudar a los usuarios a entender las palabras clave que pueden usar en el bot

from discord.ext import commands
from acciones.palabras_clave import palabras_clave
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='claves')
    async def mostrar_claves(self, ctx):
        mensaje = "Aquí están las palabras clave que puedes usar:\n\n"
        for clave, descripcion in palabras_clave.items():
            mensaje += f"**{clave}**: {descripcion}\n"
        await ctx.send(mensaje)

# Función para registrar el cog en el bot
async def setup(bot):
    await bot.add_cog(ClaveCog(bot))