# Desarrollamos el comando de ayuda en el archivo cogs/comando_ayuda.py:


from discord.ext import commands
from discord.ext.commands import Bot, Context
from acciones.ayuda import ayuda
import asyncio

class Ayuda(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600  # ID del canal donde se permitirá usar el comando

    @commands.command(name='ayuda')
    async def ayuda(self, ctx: Context) -> None:
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        """
        Muestra los comandos disponibles.
        """
        # Enviar las opciones de ayuda
        mensaje = await ctx.send(ayuda())
        await asyncio.sleep(50)
        await mensaje.delete()
        await ctx.message.delete()

async def setup(bot: Bot) -> None:
    await bot.add_cog(Ayuda(bot))
           
        