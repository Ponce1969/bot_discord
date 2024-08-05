import discord
import datetime
from pytz import timezone
import asyncio

async def create_info_embed():
    """
    Crea un embed con la información deseada, incluyendo la temperatura del procesador.
    """
    uruguay_time = datetime.datetime.now(timezone('America/Montevideo'))
    embed = discord.Embed(
        title="Mensaje Directo",
        description="Aprendiendo Python y sus librerías",
        timestamp=uruguay_time,
        color=discord.Color.blue()
    )

    # Leer temperatura del procesador
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
            cpu_temp = int(temp_file.read()) / 1000  # Convertir de miligrados a grados
        embed.add_field(name="Temperatura del Procesador", value=f"{cpu_temp}°C")
    except Exception as e:
        embed.add_field(name="Temperatura del Procesador", value=f"Error al leer la temperatura: {e}")

    return embed

async def handle_info_error(ctx, error):
    """
    Maneja los errores en la función info.
    """
    response = await ctx.send(f"Error en la función info: {error}")
    await asyncio.sleep(10)
    await response.delete() 