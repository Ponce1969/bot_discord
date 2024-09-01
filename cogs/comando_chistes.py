# aca desarrollamos la funcion de chistes random
import asyncio
from discord.ext import commands
from acciones.chistes import chistes

class ComandoChistes(commands.Cog):
    """Cog para el comando de chistes."""

    def __init__(self, bot):
        """Inicializa el Cog."""
        self.bot = bot

    @commands.command(name='chiste', aliases=['chistes'])#aliases es para poner mas de un nombre al comando
    async def chiste(self, ctx):
        """Envía un chiste al canal."""
        try:
            mensaje = await ctx.send(chistes())
            
            # Esperar 30 segundos antes de borrar los mensajes
            await asyncio.sleep(30)
            await mensaje.delete()
            await ctx.message.delete()
        except Exception as e:
            if ctx.invoked_with == 'chistes':
                await ctx.send("El comando correcto es `>chiste`, no `>chistes`.")
            else:
                await ctx.send(f"Ocurrió un error: {e}")

async def setup(bot):
    """Configura el Cog."""
    await bot.add_cog(ComandoChistes(bot))