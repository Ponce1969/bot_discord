import asyncio
from discord.ext import commands
from acciones.frases import frases_motivadoras 

class Frases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="frases")
    async def frases(self, ctx):
        mensaje = await ctx.send(frases_motivadoras(nombre=ctx.author.name))
        
        # Esperar 30 segundos antes de borrar los mensajes
        await asyncio.sleep(30)
        await mensaje.delete()
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(Frases(bot))