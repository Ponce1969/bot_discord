import asyncio

from discord import Message
from discord.ext.commands import Context

"""
    Maneja la situación de un encuentro en una cueva durante una aventura.

    Parameters:
    - ctx (Context): El contexto de la ejecución del comando.
    - nombre_ficticio (str): El nombre ficticio del jugador.

    Returns:
    None
"""



async def manejar_cueva(ctx: Context, nombre_ficticio: str) -> None:
    await ctx.send(f"{nombre_ficticio}, has llegado a una cueva misteriosa. ¿Qué camino quieres tomar? (entrar o rodear)")

    try:
        camino = await obtener_decision(ctx, ["entrar", "rodear"])
        if camino == "entrar":
            await manejar_entrada(ctx, nombre_ficticio)
        elif camino == "rodear":
            await manejar_rodeo(ctx, nombre_ficticio)
    except asyncio.TimeoutError:
        await ctx.send("¡Se acabó el tiempo para elegir un camino! Por favor, inténtalo de nuevo.")
        await manejar_cueva(ctx, nombre_ficticio)

async def obtener_decision(ctx: Context, opciones: list) -> str:
    def check(mensaje: Message) -> bool:
        return mensaje.author == ctx.author and mensaje.content.lower() in opciones
    mensaje: Message = await ctx.bot.wait_for("message", check=check, timeout=60)
    return mensaje.content.lower()

async def manejar_entrada(ctx: Context, nombre_ficticio: str) -> None:
    await ctx.send("¡Has entrado a la cueva y encuentras una espada grande y poderosa 🗡️ con una inscripción en hebreo! ¿Quieres tomar la espada o dejarla? (tomar o dejar)")
    try:
        eleccion_espada = await obtener_decision(ctx, ["tomar", "dejar"])
        if eleccion_espada == "tomar":
            await manejar_espada(ctx, nombre_ficticio)
        elif eleccion_espada == "dejar":
            await manejar_sin_espada(ctx, nombre_ficticio)
    except asyncio.TimeoutError:
        await ctx.send("¡Se acabó el tiempo para decidir! Por favor, inténtalo de nuevo.")
        await manejar_entrada(ctx, nombre_ficticio)

async def manejar_espada(ctx: Context, nombre_ficticio: str) -> None:
    await ctx.send("¡Has tomado la espada! Sientes una extraña energía recorrer tu cuerpo. ¡Esto podría cambiar el curso de tu aventura!")
    await ctx.send("De repente, te das cuenta de que no estás solo. Un grupo de lobos furiosos 🐺 te rodea, protegiendo su territorio. ¿Qué haces? ¿Luchas o trepas para intentar escapar? (luchar o trepar)")
    try:
        eleccion_lobos = await obtener_decision(ctx, ["luchar", "trepar"])
        if eleccion_lobos == "luchar":
            await ctx.send("¡Con la espada en la mano, derrotas al lobo alfa y los otros lobos huyen! Mientras examinas la cueva, encuentras un antiguo artefacto mágico 🧙 escondido en un rincón oscuro.")
            await ctx.send("El artefacto emite una luz intensa y te concede habilidades extraordinarias. Has ganado poderosos conocimientos y habilidades para tu aventura futura. ¡Fin de la aventura en la cueva, pero tu viaje continúa!")
        elif eleccion_lobos == "trepar":
            await ctx.send("Intentas trepar por las paredes de la cueva, pero son demasiado resbaladizas. Los lobos te alcanzan y... Fin del juego para ti.")
    except asyncio.TimeoutError:
        await ctx.send("¡Se acabó el tiempo para decidir! Por favor, inténtalo de nuevo.")
        await manejar_espada(ctx, nombre_ficticio)

async def manejar_sin_espada(ctx: Context, nombre_ficticio: str) -> None:
    await ctx.send("Decides dejar la espada donde está. Quizás no era una buena idea tomar algo tan misterioso.")
    await ctx.send("Sin embargo, los lobos te han olido. ¿Luchas o trepas para intentar escapar? (luchar o trepar)")
    try:
        eleccion_lobos = await obtener_decision(ctx, ["luchar", "trepar"])
        if eleccion_lobos == "luchar":
            await ctx.send("Intentas luchar sin la espada, pero los lobos son demasiado fuertes. Fin del juego para ti.")
        elif eleccion_lobos == "trepar":
            await ctx.send("Intentas trepar por las paredes de la cueva, pero son demasiado resbaladizas. Los lobos te alcanzan y... Fin del juego para ti.")
    except asyncio.TimeoutError:
        await ctx.send("¡Se acabó el tiempo para decidir! Por favor, inténtalo de nuevo.")
        await manejar_sin_espada(ctx, nombre_ficticio)

async def manejar_rodeo(ctx: Context, nombre_ficticio: str) -> None:

    await ctx.send("¡Este camino que elegiste está infectado de ladrones! 🏴‍☠️ Debes esconderte y esperar a que se vayan.")
    await asyncio.sleep(5)
    await ctx.send("Los ladrones se han ido. Sigues tu camino en busca de nuevas aventuras.")
    await ctx.send("Mientras sigues tu camino, encuentras un cofre escondido en un rincón. ¡Es un tesoro perdido por los bandidos! 💰")
    await ctx.send("Decides tomar el tesoro y sigues tu camino. Sin embargo, parece que los bandidos se dieron cuenta de tu hallazgo y vienen tras de ti. ¿Qué haces? ¿Preparas una defensa o intentas escapar? (defender o escapar)")
    try:
        decision_encuentro = await obtener_decision(ctx, ["defender", "escapar"])
        if decision_encuentro == "defender":
            await ctx.send("Buscas un palo en el camino y lo usas para hacer un arma rudimentaria. Cuando los bandidos te alcanzan, logras defenderte con valentía.")
            await ctx.send("Después de una intensa batalla, los bandidos son derrotados. Encuentras un caballo 🐎 entre unos arboles y decides montarlo.")
            await ctx.send("¡Con tu nuevo caballo y el tesoro en tu poder, te marchas victorioso hacia nuevas aventuras!")
        elif decision_encuentro == "escapar":
            await ctx.send("Intentas escapar rápidamente, pero los bandidos son rápidos. Aunque logras evadirlos por un tiempo, te das cuenta de que necesitas hacer algo para defenderte.")
            await ctx.send("Encuentras un palo en el camino, lo usas para improvisar un arma y regresas para enfrentarte a los bandidos.")
            await ctx.send("Después de una intensa batalla, los bandidos son derrotados. Encuentras un caballo 🐎 de los bandidos y decides montarlo.")
            await ctx.send("¡Con tu nuevo caballo y el tesoro en tu poder, te marchas victorioso hacia nuevas aventuras!")
    except asyncio.TimeoutError:
        await ctx.send("¡Se acabó el tiempo para decidir! Por favor, inténtalo de nuevo.")
        await manejar_rodeo(ctx, nombre_ficticio)



