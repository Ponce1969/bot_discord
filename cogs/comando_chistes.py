# aca desarrollamos la funcion de chistes random
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot, Context
from acciones.chistes import chistes

class ComandoChistes(commands.Cog):
    """Cog para el comando de chistes."""

    def __init__(self, bot: Bot) -> None:
        """Inicializa el Cog."""
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600  # ID del canal donde se permitirá usar el comando

    @commands.command(name='chiste', aliases=['chistes'])  # aliases es para poner más de un nombre al comando
    async def chiste(self, ctx: Context) -> None:
        """Envía un chiste al canal."""
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        try:
            mensaje = await ctx.send(chistes())
            
            # Esperar 30 segundos antes de borrar los mensajes
            await asyncio.sleep(30)
            await mensaje.delete()
            await ctx.message.delete()
        except Exception as e:
            if ctx.invoked_with == 'chistes':
                await ctx.send("El comando correcto es `>chiste`, no `>chistes`.")
            else:
                await ctx.send(f"Ocurrió un error: {e}")

async def setup(bot: Bot) -> None:
    """Configura el Cog."""
    await bot.add_cog(ComandoChistes(bot))