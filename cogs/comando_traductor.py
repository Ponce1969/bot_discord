import asyncio

from discord.ext import commands
from discord.ext.commands import Bot, Context

from acciones.traductor import translate


class ComandoTraductor(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600  # ID del canal donde se permitirá usar el comando

    @commands.command(name="traducir")
    async def traducir(self, ctx: Context, *, text: str) -> None:
        """
        Comando de Discord para traducir texto al español.

        :param ctx: Contexto del comando.
        :param text: Texto a traducir.
        """
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        translation = translate(text)
        mensaje = await ctx.send(translation)

        # Esperar 30 segundos antes de borrar los mensajes
        await asyncio.sleep(30)
        await mensaje.delete()
        await ctx.message.delete()

async def setup(bot: Bot) -> None:
    await bot.add_cog(ComandoTraductor(bot))
