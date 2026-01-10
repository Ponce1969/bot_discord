import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from acciones.ayuda import ayuda as ayuda_func


class Ayuda(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600

    @commands.command(name='ayuda')
    async def ayuda(self, ctx: Context, categoria: str = None) -> None:
        """
        Muestra la ayuda general o por categoría usando embed.
        El mensaje se borra automáticamente después de 60 segundos.
        """
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        ayuda_texto = ayuda_func(categoria)
        # Emojis para títulos
        titulos = {
            None: "📚 Ayuda general",
            "ia": "🤖 Comandos de IA y asistentes",
            "juegos": "🎮 Juegos y diversión",
            "utilidades": "🛠️ Utilidades y comunidad",
            "moderacion": "🛡️ Moderación",
            "otros": "🔎 Otros comandos",
            "novedades": "✨ Novedades y tips",
            "tips": "✨ Novedades y tips"
        }
        cat = (categoria or "").lower() if categoria else None
        titulo = titulos.get(cat, "📖 Ayuda")
        color = discord.Color.green() if cat in (None, "ia", "juegos", "utilidades", "moderacion", "otros") else discord.Color.blue()
        # Si es ayuda general, solo mostrar el resumen de categorías y tip
        if cat is None:
            ayuda_texto = (
                "**¡Tip!** Puedes ver ayuda por categoría: `>ayuda ia`, `>ayuda juegos`, etc.\n\n"
                + ayuda_func(None)
            )
            embed = discord.Embed(title=titulo, description=ayuda_texto, color=color)
        else:
            embed = discord.Embed(title=titulo, description=ayuda_texto, color=color)
        embed.set_footer(text="Este mensaje se autodestruirá en 60 segundos. Usa >ayuda [categoría] para más detalles.")
        mensaje_embed = await ctx.send(embed=embed)
        await asyncio.sleep(60)
        try:
            await mensaje_embed.delete()
            await ctx.message.delete()
        except discord.NotFound:
            pass

async def setup(bot: Bot) -> None:
    await bot.add_cog(Ayuda(bot))
