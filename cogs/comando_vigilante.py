import asyncio
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from acciones.vigilante import contiene_palabra_prohibida


class Vigilante(commands.Cog):
    def __init__(self, bot, max_advertencias=3):
        """
        Inicializa el cog Vigilante.

        :param bot: Instancia del bot de Discord.
        :param max_advertencias: Número máximo de advertencias antes de banear al usuario.
        """
        self.bot = bot
        self.advertencias = {}
        self.max_advertencias = max_advertencias

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listener que se activa cuando se envía un mensaje en el servidor.

        :param message: El mensaje enviado.
        """
        if message.author.bot:
            return

        palabra_prohibida = contiene_palabra_prohibida(message.content)
        if palabra_prohibida:
            # Enviar mensaje de advertencia sin repetir la palabra prohibida
            advertencia_msg = await message.channel.send(f"{message.author.mention} ¡No puedes decir esa palabra!")

            # Borrar el mensaje del usuario que contiene la palabra prohibida
            await message.delete()

            # Registrar la advertencia
            if message.author.id not in self.advertencias:
                self.advertencias[message.author.id] = {'count': 0, 'timestamp': datetime.now()}
            self.advertencias[message.author.id]['count'] += 1

            # Bannear al usuario si supera el límite de advertencias
            if self.advertencias[message.author.id]['count'] >= self.max_advertencias:
                # Intenta banear al usuario
                try:
                    await message.author.ban(reason="Uso repetido de palabras prohibidas.")
                    ban_msg = await message.channel.send(f"{message.author.mention} ha sido baneado por uso repetido de palabras prohibidas.")
                except discord.Forbidden:
                    ban_msg = await message.channel.send(f"No tengo permisos para banear a {message.author.mention}.")
                except discord.HTTPException as e:
                    ban_msg = await message.channel.send(f"Ocurrió un error al intentar banear a {message.author.mention}: {e}")

                # Opcional: Limpiar las advertencias después de banear al usuario
                del self.advertencias[message.author.id]

                # Borrar mensajes después de 40 segundos
                await asyncio.sleep(40)
                await advertencia_msg.delete()
                await ban_msg.delete()
            else:
                # Borrar mensaje de advertencia después de 40 segundos si no se banea al usuario
                await asyncio.sleep(40)
                await advertencia_msg.delete()

    async def reset_advertencias(self):
        """
        Resetea las advertencias de los usuarios cada 24 horas.
        """
        while True:
            await asyncio.sleep(86400)  # Esperar 24 horas
            now = datetime.now()
            for user_id in list(self.advertencias.keys()):
                if now - self.advertencias[user_id]['timestamp'] >= timedelta(days=1):
                    del self.advertencias[user_id]

async def setup(bot):
    """
    Función para añadir el cog al bot.

    :param bot: Instancia del bot de Discord.
    """
    vigilante = Vigilante(bot)
    await bot.add_cog(vigilante)
    # Inicia la tarea de reset de advertencias
    asyncio.create_task(vigilante.reset_advertencias())

