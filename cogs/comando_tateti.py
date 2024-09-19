# Description: Comando para jugar al tateti
# Comando: >tateti
import discord
from discord.ext import commands
from acciones.tateti import Tateti

class TatetiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tateti')
    async def tateti(self, ctx):
        """Inicia un nuevo juego de tateti"""
        view = Tateti(ctx)
        await ctx.send('¡Comienza el juego de tateti!', view=view)

# Necesario para que el bot cargue este cog
async def setup(bot):
    await bot.add_cog(TatetiCog(bot))