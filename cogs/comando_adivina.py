from acciones.adivina import adivina
from discord.ext import commands

class Adivina(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="adivina")
    async def adivina_cmd(self, ctx):
        """
        Inicia el juego de adivinar la palabra secreta.
        """
        await adivina(ctx, self.bot)  # Pasamos el bot como parámetro

async def setup(bot):
    await bot.add_cog(Adivina(bot))
        


