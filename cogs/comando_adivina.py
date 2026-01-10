from discord.ext import commands
from discord.ext.commands import Bot, Context

from acciones.adivina import adivina


class Adivina(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600  # ID del canal donde se permitirá jugar

    @commands.command(name="adivina")
    async def adivina_cmd(self, ctx: Context) -> None:
        """
        Inicia el juego de adivinar la palabra secreta.
        """
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        await adivina(ctx, self.bot)  # Pasamos el bot como parámetro

async def setup(bot: Bot) -> None:
    await bot.add_cog(Adivina(bot))



