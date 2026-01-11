import logging

from discord.ext import commands

from acciones.palabras_clave import palabras_clave

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClaveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="claves")
    async def mostrar_claves(self, ctx):
        mensaje = "Aquí están las palabras clave que puedes usar:\n\n"
        for clave, descripcion in palabras_clave.items():
            mensaje += f"**{clave}**: {descripcion}\n"

        # Enviar el mensaje y eliminarlo después de 30 segundos
        await ctx.send(mensaje, delete_after=30)

        # Eliminar el mensaje del usuario después de 30 segundos
        await ctx.message.delete(delay=30)


# Función para registrar el cog en el bot
async def setup(bot):
    await bot.add_cog(ClaveCog(bot))
