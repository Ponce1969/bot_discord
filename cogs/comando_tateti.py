import discord
from discord.ext import commands
from base.database import get_db, TatetiWinner
from tabulate import tabulate
from acciones.tateti import TatetiSetup  # Importar TatetiSetup

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
        """Muestra la lista de los últimos 10 ganadores del juego de tateti"""
        with next(get_db()) as db:
            try:
                ganadores = db.query(TatetiWinner).order_by(TatetiWinner.win_date.desc()).limit(10).all()
                if not ganadores:
                    await ctx.send("No hay ganadores registrados.")
                    return

                tabla = [[ganador.username, ganador.discord_id, ganador.win_date] for ganador in ganadores]
                mensaje = "Lista de los últimos 10 ganadores del juego de tateti:\n"
                mensaje += "```" + tabulate(tabla, headers=["Usuario", "ID de Discord", "Fecha"], tablefmt="grid") + "```"

                # Dividir el mensaje si es demasiado largo
                if len(mensaje) > 2000:
                    partes = [mensaje[i:i+2000] for i in range(0, len(mensaje), 2000)]
                    for parte in partes:
                        await ctx.send(parte)
                else:
                    await ctx.send(mensaje)
            except Exception as e:
                await ctx.send(f"Error al obtener la lista de ganadores: {e}")

# Necesario para que el bot cargue este cog
async def setup(bot):
    await bot.add_cog(TatetiCog(bot))