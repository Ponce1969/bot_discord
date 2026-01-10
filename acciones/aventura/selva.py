import asyncio

from discord import Message
from discord.ext.commands import Context


async def manejar_selva(ctx: Context, nombre_ficticio: str) -> None:
    await ctx.send(f"¡{nombre_ficticio} se adentra en la selva! 🌴 Arriesgando su vida en busca de tesoros ocultos.")
    await asyncio.sleep(5)
    await ctx.send(f"¡{nombre_ficticio} has encontrado un arco y flechas! 🏹 ¿Deseas equiparlo? (agarrar o ignorar)")

    try:
        eleccion_arco = await obtener_decision(ctx, ["agarrar", "ignorar"])
        if eleccion_arco == "agarrar":
            await manejar_arco(ctx, nombre_ficticio)
        elif eleccion_arco == "ignorar":
            await manejar_sin_arco(ctx, nombre_ficticio)
    except asyncio.TimeoutError:
        await ctx.send("¡Se acabó el tiempo para decidir! El destino te lleva de vuelta a la entrada de la selva. 🌿 Inténtalo de nuevo.")
        await manejar_selva(ctx, nombre_ficticio)

async def manejar_arco(ctx: Context, nombre_ficticio: str) -> None:
    await ctx.send("¡Has agarrado el arco y las flechas! Sientes una extraña energía recorrer tu cuerpo. ¡Esto podría cambiar el curso de tu aventura!")
    await asyncio.sleep(3)
    await ctx.send("De repente, te das cuenta de que no estás solo. Un grupo de guerreros salvajes 🏹 te rodea, protegiendo su territorio. ¿Qué haces? ¿Luchas o huyes para intentar escapar? (luchar o huir)")

    try:
        eleccion_guerreros = await obtener_decision(ctx, ["luchar", "huir"])
        if eleccion_guerreros == "luchar":
            await ctx.send("¡Con el arco en la mano, derrotas a los guerreros en una batalla épica! ⚔️ Los guerreros huyen, dejando un antiguo artefacto mágico 🧙 escondido en un rincón oscuro.")
            await asyncio.sleep(3)
            await ctx.send("El artefacto emite una luz intensa y te concede habilidades extraordinarias. Has ganado poderosos conocimientos y habilidades para tu aventura futura. 🌟 ¡Fin de la aventura en la selva, pero tu viaje continúa!")
        elif eleccion_guerreros == "huir":
            await ctx.send("Intentas huir por la selva, pero los guerreros te alcanzan y... ¡Oh no! Has sido capturado por los salvajes y llevado a su campamento. 🏕️ Fin del juego para ti.")
    except asyncio.TimeoutError:
        await ctx.send("¡Se acabó el tiempo para decidir! Los guerreros te rodean, y debes enfrentar las consecuencias de la indecisión. 🌪️ Fin de la aventura en la selva.")

async def manejar_sin_arco(ctx: Context, nombre_ficticio: str) -> None:
    await ctx.send("¡Has decidido ignorar el arco y las flechas! Sigues tu camino por la selva, explorando la exuberante vegetación y el canto de criaturas exóticas. 🦜")
    await asyncio.sleep(3)
    await ctx.send("Pronto te das cuenta de que no estás solo. Un grupo de guerreros salvajes 🏹 te rodea, protegiendo su territorio. ¿Qué haces? ¿Luchas o huyes para intentar escapar? (luchar o huir)")

    try:
        eleccion_guerreros = await obtener_decision(ctx, ["luchar", "huir"])
        if eleccion_guerreros == "luchar":
            await ctx.send("Decides enfrentarte a los guerreros con valentía. A pesar de no tener el arco, demuestras gran habilidad en combate y logras vencerlos. 🎉 En el suelo, encuentras un cofre antiguo con tesoros invaluables. 🗝️ ¡Fin de la aventura en la selva, y te llevas un rico botín a casa!")
        elif eleccion_guerreros == "huir":
            await ctx.send("Intentas escapar, pero los guerreros te persiguen a través de la selva. Te escondes en una cueva cercana, pero estás atrapado en la oscuridad... ¡El juego ha terminado para ti!")
    except asyncio.TimeoutError:
        await ctx.send("¡Se acabó el tiempo para decidir! Los guerreros te rodean, y tu aventura en la selva termina abruptamente. 🌿 Fin del juego.")

async def obtener_decision(ctx: Context, opciones: list) -> str:
    def check(msg: Message) -> bool:
        return msg.author == ctx.author and msg.content.lower() in opciones
    mensaje: Message = await ctx.bot.wait_for("message", check=check, timeout=60)
    return mensaje.content.lower()


