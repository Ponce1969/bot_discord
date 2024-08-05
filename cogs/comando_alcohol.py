# Aca iria los comandos de alcohol 
from discord.ext import commands
from acciones.alcohol import tomar_acompañado, tomar_solo

class ComandoAlcohol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command(name="tomar")
    async def tomar(self, ctx, nombre: str = None):
        if nombre:
            await ctx.send(tomar_acompañado(ctx.author.name, nombre))
        else:
            await ctx.send(tomar_solo(ctx.author.name))
            
            
async def setup(bot):
    await bot.add_cog(ComandoAlcohol(bot))