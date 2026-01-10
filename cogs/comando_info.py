import asyncio
import json

from discord.ext import commands
from discord.ext.commands import Bot, Context

from acciones.system_metrics_rust import create_advanced_info_embed


class Info(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600  # ID del canal donde se permitirá usar el comando

    @commands.command(name="info")
    async def info(self, ctx: Context) -> None:
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return
        """
        Comando de Discord para mostrar información avanzada del sistema.
        Usa el componente Rust para métricas completas del OrangePi 5 Plus.
        """
        try:
            # Mensaje de "cargando" mientras se obtienen métricas
            loading_msg = await ctx.send("🔄 Obteniendo métricas del sistema...")

            # Crear embed avanzado con Rust
            embed = await create_advanced_info_embed(ctx.guild.name if ctx.guild else "OrangePi 5 Plus")

            # Actualizar mensaje con las métricas
            await loading_msg.edit(content=None, embed=embed)

            # Auto-eliminar después de 60 segundos (más tiempo por la riqueza de info)
            await asyncio.sleep(60)
            await loading_msg.delete()

        except Exception as e:
            error_msg = f"Error al obtener métricas del sistema: {str(e)}"
            await ctx.send(error_msg)
            print(f"Error en comando info: {e}")

    @commands.command(name="info_json")
    async def info_json(self, ctx: Context) -> None:
        """
        Comando para desarrolladores: obtener métricas en formato JSON
        """
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        try:
            from io import StringIO

            from discord import File

            from acciones.system_metrics_rust import get_system_metrics_json

            metrics = await get_system_metrics_json()
            if metrics:
                # Enviar como archivo JSON
                json_str = json.dumps(metrics, indent=2, ensure_ascii=False)
                buffer = StringIO(json_str)
                buffer.seek(0)

                await ctx.send(
                    "📊 Métricas del sistema en formato JSON:",
                    file=File(fp=buffer, filename="system_metrics.json")
                )
            else:
                await ctx.send("❌ Error obteniendo métricas del sistema")

        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

async def setup(bot: Bot) -> None:
    await bot.add_cog(Info(bot))
