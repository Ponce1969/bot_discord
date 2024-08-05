# Aca desarrollaremos el comando traductor que traducira el texto que le pasemos a español

from discord.ext import commands
from acciones.traductor import translate

class ComandoTraductor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="traducir")
    async def traducir(self, ctx, *, text: str):
        """
        Comando de Discord para traducir texto al español.

        :param ctx: Contexto del comando.
        :param text: Texto a traducir.
        """
        translation = translate(text)
        await ctx.send(translation)

async def setup(bot):
    await bot.add_cog(ComandoTraductor(bot))