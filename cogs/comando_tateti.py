# Description: Comando para jugar al tateti
# Comando: >tateti [contra_bot]
import discord
from discord.ext import commands
from acciones.tateti import TatetiSetup
from base.database import get_db, TatetiWinner
from tabulate import tabulate

class TatetiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tateti')
    async def tateti(self, ctx):
        """Inicia un nuevo juego de tateti"""
        view = TatetiSetup(ctx)
        await ctx.send('¿Contra quién quieres jugar?', view=view)

    @commands.command(name='tateti_ganadores')
    async def tateti_ganadores(self, ctx):
        """Muestra la lista de ganadores del juego de tateti"""
        db = next(get_db())
        try:
            ganadores = db.query(TatetiWinner).all()
            if not ganadores:
                await ctx.send("No hay ganadores registrados.")
                return

            tabla = [[ganador.username, ganador.discord_id, ganador.win_date] for ganador in ganadores]
            mensaje = "Lista de ganadores del juego de tateti:\n"
            mensaje += "```" + tabulate(tabla, headers=["Usuario", "ID de Discord", "Fecha"], tablefmt="grid") + "```"
            await ctx.send(mensaje)
        except Exception as e:
            await ctx.send(f"Error al obtener la lista de ganadores: {e}")
        finally:
            db.close()

# Necesario para que el bot cargue este cog
async def setup(bot):
    await bot.add_cog(TatetiCog(bot))