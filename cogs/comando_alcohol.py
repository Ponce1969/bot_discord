import asyncio
from discord.ext import commands
from acciones.alcohol import tomar_acompañado, tomar_solo

class ComandoAlcohol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command(name="tomar")
    async def tomar(self, ctx, nombre: str = None):
        if nombre:
            mensaje = await ctx.send(tomar_acompañado(ctx.author.name, nombre))
        else:
            mensaje = await ctx.send(tomar_solo(ctx.author.name))
        
        # Esperar 30 segundos antes de borrar los mensajes
        await asyncio.sleep(30)
        await mensaje.delete()
        await ctx.message.delete()
        
async def setup(bot):
    await bot.add_cog(ComandoAlcohol(bot))