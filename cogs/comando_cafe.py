# cogs/cafe.py
# Description: Comando de café
# Importar librerías
from discord.ext import commands
from discord.ext.commands import Context
from acciones.cafe import cafe, opciones_cafe
from asyncio import TimeoutError  # Importar solo TimeoutError

class Cafe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cafe")
    async def cafe_cmd(self, ctx: Context):
        """
        Inicia el proceso de selección de café.
        """
        # Enviar las opciones de café
        await ctx.send(opciones_cafe())

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while True:
            try:
                # Esperar la respuesta del usuario
                msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                if not msg.content.isdigit():
                    await ctx.send(f"{ctx.author.mention}, por favor ingresa un número entero válido.")
                    await ctx.send(opciones_cafe())
                    continue

                tipo = msg.content
                cafe_tipo = cafe(tipo)
                await ctx.send(f"Aquí tienes el {cafe_tipo} caliente que pediste, {ctx.author.mention}!")
                break
            except TimeoutError:  # Capturar el error de tiempo de espera
                await ctx.send(f"{ctx.author.mention}, tardaste demasiado en responder. Intenta nuevamente.")
                break

async def setup(bot):
    await bot.add_cog(Cafe(bot))

