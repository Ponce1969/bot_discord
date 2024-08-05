# Desarrollamos el comando de ayuda en el archivo cogs/comando_ayuda.py:


from discord.ext import commands
from acciones.ayuda import ayuda
import asyncio

class Ayuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ayuda')
    async def ayuda(self, ctx):
        """
        Muestra los comandos disponibles.
        """
        # Enviar las opciones de ayuda
        mensaje = await ctx.send(ayuda())
        await asyncio.sleep(50)
        await mensaje.delete()
        await ctx.message.delete()
        
        

async def setup(bot):
    await bot.add_cog(Ayuda(bot))
           
        