# cogs/comando_aventura.py
from discord.ext import commands

from config.avent_config import iniciar_juego


class AventuraCog(commands.Cog):
    """Cog para manejar el juego de aventuras."""

    def __init__(self, bot):
        self.bot = bot
        self.canal_juego_id = 1279149582936182816  # ID del canal permitido

    @commands.command(name="aventura")
    async def iniciar_aventura(self, ctx):
        """Comando para iniciar el juego de aventuras."""
        if ctx.channel.id != self.canal_juego_id:
            await ctx.send("Solo puedes jugar en el canal #chat_juego_aventura.")
            return
        await iniciar_juego(ctx)


async def setup(bot):
    """Configura el Cog."""
    await bot.add_cog(AventuraCog(bot))
