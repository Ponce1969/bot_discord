import time
from io import StringIO

from discord import File
from discord.ext import commands

from acciones.llama import (
    GroqSession,
    groq_handler,
    registrar_metricas_llama,
    token_manager,
)
from base.database import get_global_metrics, get_user_metrics


class Llama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.groq_handler = groq_handler

    @commands.command(name='llama')
    async def llama(self, ctx, *, user_message: str = None):
        if not user_message:
            await ctx.send("Hola, debes hacerme una pregunta sobre código para que pueda responder.")
            return

        thinking_message = await ctx.send("Pythonbot está pensando...")
        start_time = time.monotonic()
        tokens_usados = token_manager.tokens_per_request  # Puedes adaptar esto si usas lógica diferente
        fue_archivo = False
        fallo_api = False
        try:
            async with GroqSession(token_manager) as allowed:
                if not allowed:
                    await thinking_message.edit(content="Se ha alcanzado el límite diario de tokens. Intenta mañana.")
                    return
                response = await self.groq_handler.get_response(user_message)
                if len(response) <= 1900:
                    embed = self.groq_handler.create_response_embed(ctx.author.name, response)
                    await thinking_message.delete()
                    await ctx.send(embed=embed)
                else:
                    fue_archivo = True
                    buffer = StringIO(response)
                    buffer.seek(0)
                    await thinking_message.edit(content="La respuesta es extensa, se enviará como archivo.")
                    await ctx.send(file=File(fp=buffer, filename="respuesta_llama.txt"))
        except Exception as e:
            fallo_api = True
            await thinking_message.edit(content=f"Error al obtener la respuesta: {str(e)}")
        finally:
            response_time = time.monotonic() - start_time
            await registrar_metricas_llama(str(ctx.author.id), tokens_usados, response_time, fue_archivo, fallo_api)

    @commands.command(name='llama_stats')
    async def llama_stats(self, ctx, global_stats: bool = False):
        """Muestra estadísticas del uso de llama (personales o globales). Usa >llama_stats True para global."""
        if global_stats:
            result = get_global_metrics()
            llama_uses, tokens_used, total_response_time, responses_as_file, api_failures = result
            avg_time = (total_response_time / llama_uses) if llama_uses else 0
            msg = (
                f"**Estadísticas globales de hoy:**\n"
                f"Consultas: {llama_uses or 0}\n"
                f"Tokens usados: {tokens_used or 0}\n"
                f"Tiempo de respuesta promedio: {avg_time:.2f} seg\n"
                f"Respuestas largas (archivo): {responses_as_file or 0}\n"
                f"Fallos de API: {api_failures or 0}"
            )
        else:
            metrics = get_user_metrics(str(ctx.author.id))
            if metrics:
                avg_time = (metrics.total_response_time / metrics.llama_uses) if metrics.llama_uses else 0
                msg = (
                    f"**Tus estadísticas de hoy:**\n"
                    f"Consultas: {metrics.llama_uses}\n"
                    f"Tokens usados: {metrics.tokens_used}\n"
                    f"Tiempo de respuesta promedio: {avg_time:.2f} seg\n"
                    f"Respuestas largas (archivo): {metrics.responses_as_file}\n"
                    f"Fallos de API: {metrics.api_failures}"
                )
            else:
                msg = "Aún no tienes estadísticas para hoy."
        await ctx.send(msg)

    @commands.command(name='llama_dashboard')
    async def llama_dashboard(self, ctx):
        """Muestra un resumen visual simple de las métricas globales usando table2ascii."""
        from table2ascii import PresetStyle
        from table2ascii import table2ascii as t2a
        result = get_global_metrics()
        llama_uses, tokens_used, total_response_time, responses_as_file, api_failures = result
        avg_time = (total_response_time / llama_uses) if llama_uses else 0
        headers = ["Consultas", "Tokens", "Resp. largas", "Errores API", "Resp. prom. (seg)"]
        row = [llama_uses or 0, tokens_used or 0, responses_as_file or 0, api_failures or 0, f"{avg_time:.2f}"]
        tabla = t2a(
            header=headers,
            body=[row],
            style=PresetStyle.thin_compact
        )
        await ctx.send(f"```\n{tabla}\n```\nMétricas globales de hoy para >llama")

async def setup(bot):
    await bot.add_cog(Llama(bot))
