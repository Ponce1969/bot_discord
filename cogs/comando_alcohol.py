import asyncio

from discord.ext import commands
from discord.ext.commands import Bot, Context

from acciones.alcohol import tomar_acompañado, tomar_solo


class ComandoAlcohol(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600  # ID del canal donde se permitirá jugar

    @commands.command(name="tomar")
    async def tomar(self, ctx: Context, nombre: str = None) -> None:
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        if nombre:
            mensaje = await ctx.send(tomar_acompañado(ctx.author.name, nombre))
        else:
            mensaje = await ctx.send(tomar_solo(ctx.author.name))

        # Esperar 30 segundos antes de borrar los mensajes
        await asyncio.sleep(30)
        await mensaje.delete()
        await ctx.message.delete()

async def setup(bot: Bot) -> None:
    await bot.add_cog(ComandoAlcohol(bot))
