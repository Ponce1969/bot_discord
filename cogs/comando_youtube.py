import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from acciones.youtube import youtube_search

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Youtube(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.api_key: str = os.getenv("YOUTUBE_API_KEY")
        self.canal_permitido_id: int = 1172339507899670600

    @commands.command(name="youtube")
    async def youtube(self, ctx: commands.Context, *, search: str = None) -> None:
        """
        Comando de Discord para buscar videos en YouTube.

        :param ctx: Contexto del comando.
        :param search: Término de búsqueda.
        """
        # Verificar que el comando se ejecuta en el canal permitido
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        if not search:
            await ctx.send("Por favor, ingrese un término de búsqueda. Ejemplo: >youtube tango")
            return

        response = await youtube_search(self.api_key, search)
        if response is None or 'items' not in response or not response['items']:
            await ctx.send("No se encontraron videos para tu búsqueda.")
            return

        options = [f"{i+1}. {item['snippet']['title']}" for i, item in enumerate(response['items']) if item['id']['kind'] == "youtube#video"]

        if not options:
            await ctx.send("No se encontraron videos para tu búsqueda.")
            return

        await ctx.send("Elije un video:\n" + "\n".join(options))

        def check(m: discord.Message) -> bool:
            return m.author == ctx.author and m.content.isdigit() and 0 < int(m.content) <= len(options)

        try:
            choice: discord.Message = await self.bot.wait_for("message", check=check, timeout=30.0)
            selected: int = int(choice.content) - 1
            video_id: str = response['items'][selected]['id']['videoId']
            await ctx.send(f"https://www.youtube.com/watch?v={video_id}")
        except asyncio.TimeoutError:
            await ctx.send("Se acabó el tiempo para seleccionar un video.")
        except Exception as e:
            await ctx.send(f"Ocurrió un error al procesar tu selección: {e}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Youtube(bot))
