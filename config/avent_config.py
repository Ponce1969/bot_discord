import asyncio

from acciones.aventura import (
    manejar_cueva,
    manejar_montania,
    manejar_rio,
    manejar_selva,
)


async def iniciar_juego(ctx):
    await ctx.send(
        "Bienvenido al emotivo juego de aventuras. Escribe 'inicio' para comenzar."
    )

    try:
        await esperar_mensaje(
            ctx,
            "inicio",
            "¡Gracias por unirte! Por favor, escribe un nombre ficticio para tu personaje:",
        )
        nombre_ficticio = await obtener_nombre_ficticio(ctx)
        await ctx.send(
            f"¡Excelente, {nombre_ficticio}! Tu aventura comienza ahora. ¡Buena suerte!"
        )
        await manejar_direccion(ctx, nombre_ficticio)
    except asyncio.TimeoutError:
        await ctx.send("¡Te has tardado mucho! Vuelve a intentarlo más tarde.")


async def esperar_mensaje(ctx, contenido_esperado, mensaje_respuesta):
    def check(mensaje):
        return (
            mensaje.author == ctx.author
            and mensaje.content.lower() == contenido_esperado
        )

    await ctx.bot.wait_for("message", check=check, timeout=60)
    await ctx.send(mensaje_respuesta)


async def obtener_nombre_ficticio(ctx):
    def check_nombre(mensaje):
        return mensaje.author == ctx.author and len(mensaje.content.strip()) > 0

    nombre_msg = await ctx.bot.wait_for("message", check=check_nombre, timeout=60)
    return nombre_msg.content.strip()


async def manejar_direccion(ctx, nombre_ficticio):
    """
    Maneja la dirección elegida por el usuario en el contexto dado.

    Parameters:
    - ctx (discord.ext.commands.Context): El contexto de Discord.
    - nombre_ficticio (str): El nombre ficticio del usuario.

    Returns:
    None
    """
    await ctx.send(
        f"{nombre_ficticio}, ¡estás en el centro de la aventura! ¿Qué dirección quieres tomar? (norte, sur, este, oeste)"
    )

    try:
        direccion = await obtener_direccion(ctx)
        if direccion == "norte":
            await manejar_cueva(ctx, nombre_ficticio)
        elif direccion == "sur":
            await manejar_montania(ctx, nombre_ficticio)
        elif direccion == "este":
            await manejar_rio(ctx, nombre_ficticio)
        elif direccion == "oeste":
            await manejar_selva(ctx, nombre_ficticio)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Se acabó el tiempo para elegir una dirección! Por favor, inténtalo de nuevo."
        )
        await manejar_direccion(ctx, nombre_ficticio)


async def obtener_direccion(ctx):
    def check_direccion(mensaje):
        return mensaje.author == ctx.author and mensaje.content.lower() in [
            "norte",
            "sur",
            "este",
            "oeste",
        ]

    direccion_msg = await ctx.bot.wait_for("message", check=check_direccion, timeout=60)
    return direccion_msg.content.lower()
