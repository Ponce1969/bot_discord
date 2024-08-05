# aca van los comandos de frases motivadoras
from discord.ext import commands
from acciones.frases import frases_motivadoras 


class Frases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="frases")
    async def frases(self, ctx):
        await ctx.send(frases_motivadoras(nombre=ctx.author.name))
        
async def setup(bot):
    await bot.add_cog(Frases(bot))