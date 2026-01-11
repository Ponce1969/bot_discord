import asyncio

from discord.ext import commands

from acciones.hola import hola


class ComandoHola(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hola")  # Decorador para crear comandos
    async def hola_comando(self, ctx):
        """
        Da la bienvenida al usuario y le cuenta de qué trata el servidor.
        """
        # Llamar a la función hola con el socket del usuario y su nombre
        # En este caso, ctx es el contexto del comando y ctx.author.name es el nombre del usuario
        mensajes = await hola(ctx.author, ctx.author.name)
        # Esperar 50 segundos antes de eliminar los mensajes
        await asyncio.sleep(50)
        # Eliminar todos los mensajes enviados por la función hola
        for mensaje in mensajes:
            await mensaje.delete()
        # Eliminar el mensaje del comando
        await ctx.message.delete()

    @commands.Cog.listener()  # Decorador para escuchar eventos
    async def on_member_join(self, member):
        """
        Enviar un mensaje de bienvenida cuando un usuario se une al servidor.
        """
        # Llamar a la función hola con el miembro y su nombre
        mensajes = await hola(member, member.name)
        # Esperar 50 segundos antes de eliminar los mensajes
        await asyncio.sleep(50)
        # Eliminar todos los mensajes enviados por la función hola
        for mensaje in mensajes:
            await mensaje.delete()


async def setup(bot):
    await bot.add_cog(ComandoHola(bot))
