# aca se encuentra la funcion encuesta que permite crear una encuesta con varias opciones
# la función recibe el contexto, la pregunta y las opciones de la encuesta
# la función crea un embed con la pregunta y las opciones y envía el mensaje al canal
# luego, la función agrega reacciones a la encuesta para que los usuarios puedan votar

import discord


async def encuesta(ctx, pregunta: str, *opciones: str):
    if len(opciones) < 2:
        await ctx.send("Necesitas proporcionar al menos dos opciones.")
        return
    if len(opciones) > 10:
        await ctx.send("No puedes proporcionar más de diez opciones.")
        return

    descripcion = ""
    for i, opcion in enumerate(opciones):
        descripcion += f"\n{i + 1}. {opcion}"

    embed = discord.Embed(
        title=pregunta, description=descripcion, color=0x00FF00
    )  # Color verde
    mensaje = await ctx.send(embed=embed)

    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i in range(len(opciones)):
        await mensaje.add_reaction(emojis[i])
