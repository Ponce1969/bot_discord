# iria aca los comandos de abrazo
from discord.ext import commands
from acciones.abrazo import abrazo_con_nombre, me_abrazo, abrazo_nadie  

class Abrazo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="abrazo")
    async def abrazo(self, ctx, nombre: str = None):
        if nombre:
            await ctx.send(abrazo_con_nombre(ctx.author.name, nombre))
        else:
            await ctx.send(abrazo_nadie(ctx.author.name))
    
    @commands.command(name="me_abrazo")
    async def me_abrazo(self, ctx):
        await ctx.send(me_abrazo(ctx.author.name))
    
    
async def setup(bot):
    await bot.add_cog(Abrazo(bot))


