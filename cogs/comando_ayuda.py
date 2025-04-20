import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
import asyncio

class Ayuda(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600

    @commands.command(name='ayuda')
    async def ayuda(self, ctx: Context) -> None:
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        embed = discord.Embed(
            title="Comandos Disponibles",
            description="Aquí tienes una lista de los comandos que puedes usar:",
            color=discord.Color.blue()
        )

        embed.add_field(name=">cafe", value="Muestra las opciones de café disponibles.", inline=False)
        embed.add_field(name=">hola", value="Saluda al bot.", inline=False)
        embed.add_field(name=">ayuda", value="Muestra este mensaje de ayuda.", inline=False)
        embed.add_field(name=">tomar", value="Toma un trago solo o acompañado.", inline=False)
        embed.add_field(name=">frases", value="Te muestra frases motivadoras.", inline=False)
        embed.add_field(name=">traducir", value="Traduce un texto al español.", inline=False)
        embed.add_field(name=">youtube", value="Busca un video en YouTube (ej: >youtube tango).", inline=False)
        embed.add_field(name=">info", value="Muestra información del servidor y temperatura del CPU.", inline=False)
        embed.add_field(name=">gemini", value="Inicia una conversación con la IA de Gemini.", inline=False)
        embed.add_field(name=">gemini_imagen", value="Envía una imagen a Gemini para describirla.", inline=False)
        embed.add_field(name=">gemini_reset", value="Reinicia la conversación con Gemini.", inline=False)
        embed.add_field(name=">abrazo [@usuario]", value="Abraza a un usuario mencionado. Sin mención, abraza al aire.", inline=False)
        embed.add_field(name=">me_abrazo", value="El bot se abraza a sí mismo.", inline=False)
        embed.add_field(name=">llama", value="Inicia una conversación con Llama sobre código Python.", inline=False)
        embed.add_field(name=">adivina [letra]", value="Juego de adivinanzas.", inline=False)
        embed.add_field(name=">chiste / >chistes", value="Muestra un chiste.", inline=False)
        embed.add_field(name=">aventura", value="Inicia una aventura de texto (usar en #chat_juego_aventura).", inline=False)
        embed.add_field(name=">gracias @usuario", value="Agradece a un usuario y suma puntos al ranking.", inline=False)
        embed.add_field(name=">ranking", value="Muestra el ranking de agradecimientos.", inline=False)
        embed.add_field(name=">vigilante", value="Modera el lenguaje y aplica advertencias/baneos.", inline=False)
        embed.add_field(name=">tateti [bot/usuario]", value="Inicia un juego de Ta-Te-Ti.", inline=False)
        embed.add_field(name=">tateti_ganadores", value="Muestra la lista de ganadores de Ta-Te-Ti.", inline=False)
        embed.add_field(name='>encuesta "pregunta" "opc1" "opc2" ...', value="Crea una encuesta.", inline=False)
        embed.add_field(name=">claves", value="Muestra palabras clave para activar al bot sin prefijo (>).", inline=False)
        embed.add_field(name="Oyente (sin prefijo >)", value="El bot responde a frases comunes usando palabras clave (ver >claves).", inline=False)

        mensaje_embed = await ctx.send(embed=embed)

        await asyncio.sleep(60)
        try:
            await mensaje_embed.delete()
            await ctx.message.delete()
        except discord.NotFound:
            pass

async def setup(bot: Bot) -> None:
    await bot.add_cog(Ayuda(bot))