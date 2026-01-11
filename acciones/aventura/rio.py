import asyncio

from discord import Message
from discord.ext.commands import Context

"""
Aquí se desarrollarán las funciones y condicionales para la función del río
"""


async def manejar_rio(ctx: Context, nombre_ficticio: str) -> None:
    await ctx.send(
        f"Estás en el río {nombre_ficticio}. Te encuentras en la orilla de un río caudaloso rodeado de árboles antiguos y una niebla misteriosa. ¿Qué decides hacer? ¿Cruzar el río o seguir la orilla? (cruzar o orilla) 🏞️"
    )

    try:
        decision_camino = await obtener_decision(ctx, ["cruzar", "orilla"])
        if decision_camino == "cruzar":
            await manejar_cruzar(ctx)
        elif decision_camino == "orilla":
            await manejar_orilla(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! El río se ha vuelto peligroso y debes regresar a la orilla. ⚠️"
        )


async def obtener_decision(ctx: Context, opciones: list) -> str:
    def check(msg: Message) -> bool:
        return msg.author == ctx.author and msg.content.lower() in opciones

    mensaje: Message = await ctx.bot.wait_for("message", check=check, timeout=60)
    return mensaje.content.lower()


async def manejar_cruzar(ctx: Context) -> None:
    await ctx.send(
        "Decides cruzar el río. Mientras cruzas, encuentras un bote antiguo con símbolos arcanos grabados en él. ¿Decides tomar el bote o seguir nadando? (bote o nadar) 🚣‍♂️"
    )
    try:
        decision_bote = await obtener_decision(ctx, ["bote", "nadar"])
        if decision_bote == "bote":
            await manejar_bote(ctx)
        elif decision_bote == "nadar":
            await manejar_nadar(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! El río se ha vuelto peligroso y debes regresar a la orilla. ⚠️"
        )


async def manejar_orilla(ctx: Context) -> None:
    await ctx.send(
        "Decides seguir la orilla del río. La vegetación se vuelve más densa y escuchas el canto de criaturas místicas. Encuentras un puente colgante cubierto de musgo. ¿Decides cruzar el puente o seguir la orilla? (puente o orilla) 🌉"
    )
    try:
        decision_puente = await obtener_decision(ctx, ["puente", "orilla"])
        if decision_puente == "puente":
            await manejar_puente(ctx)
        elif decision_puente == "orilla":
            await manejar_orilla2(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! El río se ha vuelto peligroso y debes regresar a la orilla. ⚠️"
        )


async def manejar_bote(ctx: Context) -> None:
    await ctx.send(
        "Decides tomar el bote y navegas por el río. De repente, una niebla mágica envuelve el bote y te encuentras en una isla misteriosa. Allí hay dos caminos: uno lleva a un templo antiguo y el otro a un bosque encantado. ¿Qué eliges? (templo o bosque) 🏝️"
    )
    try:
        decision_isla = await obtener_decision(ctx, ["templo", "bosque"])
        if decision_isla == "templo":
            await manejar_templo(ctx)
        elif decision_isla == "bosque":
            await manejar_bosque(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! El bote ha sido arrastrado por la corriente de vuelta a la orilla. ⚠️"
        )


async def manejar_nadar(ctx: Context) -> None:
    await ctx.send(
        "Decides seguir nadando. Mientras avanzas, encuentras un remolino mágico que te lleva a una cueva subterránea llena de tesoros y criaturas fantásticas. Dentro, ves dos cofres: uno dorado y uno plateado. ¿Cuál eliges? (dorado o plateado) 🗝️"
    )
    try:
        decision_cueva = await obtener_decision(ctx, ["dorado", "plateado"])
        if decision_cueva == "dorado":
            await manejar_cofre_dorado(ctx)
        elif decision_cueva == "plateado":
            await manejar_cofre_plateado(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! El remolino te ha llevado de vuelta a la orilla. ⚠️"
        )


async def manejar_puente(ctx: Context) -> None:
    await ctx.send(
        "Cruzas el puente colgante y te encuentras en una aldea de elfos. Los elfos te ofrecen una elección: recibir una bendición mágica o aprender un secreto antiguo. ¿Qué eliges? (bendición o secreto) 🧙"
    )
    try:
        decision_elfos = await obtener_decision(ctx, ["bendición", "secreto"])
        if decision_elfos == "bendición":
            await manejar_bendicion(ctx)
        elif decision_elfos == "secreto":
            await manejar_secreto(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! Los elfos te piden que regreses a la orilla. ⚠️"
        )


async def manejar_orilla2(ctx: Context) -> None:
    await ctx.send(
        "Sigues la orilla y encuentras una antigua cabaña cubierta de enredaderas. Dentro, ves un libro antiguo y una poción mágica. ¿Qué decides examinar? (libro o poción) 📚"
    )
    try:
        decision_cabana = await obtener_decision(ctx, ["libro", "poción"])
        if decision_cabana == "libro":
            await manejar_libro(ctx)
        elif decision_cabana == "poción":
            await manejar_pocion(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! La cabaña se desvanece y debes regresar a la orilla. ⚠️"
        )


async def manejar_templo(ctx: Context) -> None:
    await ctx.send(
        "Entras al templo y encuentras una sala con un antiguo altar. Hay dos reliquias: una espada mágica y un escudo encantado. ¿Cuál eliges? (espada o escudo) ⚔️"
    )
    try:
        decision_reliquia = await obtener_decision(ctx, ["espada", "escudo"])
        if decision_reliquia == "espada":
            await manejar_espada(ctx)
        elif decision_reliquia == "escudo":
            await manejar_escudo(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! El templo se cierra y debes regresar a la orilla. ⚠️"
        )


async def manejar_bosque(ctx: Context) -> None:
    await ctx.send(
        "Te adentras en el bosque encantado y encuentras una fuente mágica con agua cristalina. La fuente ofrece dos opciones: beber de ella para obtener una visión del futuro o usarla para curar cualquier herida. ¿Qué eliges? (visión o curar) 🌿"
    )
    try:
        decision_fuente = await obtener_decision(ctx, ["visión", "curar"])
        if decision_fuente == "visión":
            await manejar_vision(ctx)
        elif decision_fuente == "curar":
            await manejar_curacion(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! El bosque se vuelve impenetrable y debes regresar a la orilla. ⚠️"
        )


async def manejar_cofre_dorado(ctx: Context) -> None:
    await ctx.send(
        "Abres el cofre dorado y encuentras un amuleto antiguo. El amuleto te otorga un poder especial y te transporta a un reino mágico lleno de criaturas fantásticas. ¿Qué decides hacer en este nuevo reino? (explorar o regresar) ✨"
    )
    try:
        decision_reino = await obtener_decision(ctx, ["explorar", "regresar"])
        if decision_reino == "explorar":
            await manejar_explorar(ctx)
        elif decision_reino == "regresar":
            await manejar_regresar(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! El reino mágico se desvanece y debes regresar a la orilla. ⚠️"
        )


async def manejar_cofre_plateado(ctx: Context) -> None:
    await ctx.send(
        "Abres el cofre plateado y encuentras un pergamino antiguo. El pergamino revela un hechizo poderoso que puede cambiar el curso de tu aventura. ¿Decides usar el hechizo ahora o guardarlo para más tarde? (usar o guardar) 🧙‍♂️"
    )
    try:
        decision_hechizo = await obtener_decision(ctx, ["usar", "guardar"])
        if decision_hechizo == "usar":
            await manejar_usar_hechizo(ctx)
        elif decision_hechizo == "guardar":
            await manejar_guardar_hechizo(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! El pergamino se desintegra y debes regresar a la orilla. ⚠️"
        )


async def manejar_bendicion(ctx: Context) -> None:
    await ctx.send(
        "Recibes la bendición de los elfos, otorgándote habilidades mágicas que te serán útiles en futuras aventuras. Los elfos te envían de vuelta a la orilla con un nuevo poder. 🌟"
    )


async def manejar_secreto(ctx: Context) -> None:
    await ctx.send(
        "Aprendes un secreto antiguo que te da conocimiento sobre el mundo mágico. Te despides de los elfos y regresas a la orilla con nuevos conocimientos. 📜"
    )


async def manejar_libro(ctx: Context) -> None:
    await ctx.send(
        "Lees el libro antiguo y descubres hechizos olvidados. Con el conocimiento del libro, obtienes habilidades mágicas adicionales. Regresas a la orilla con nuevas habilidades. 📚"
    )


async def manejar_pocion(ctx: Context) -> None:
    await ctx.send(
        "Bebes la poción mágica y sientes un poder curativo recorrer tu cuerpo. Estás completamente renovado y listo para nuevas aventuras. Regresas a la orilla con una sensación de fortaleza. 🍹"
    )


async def manejar_espada(ctx: Context) -> None:
    await ctx.send(
        "Tomas la espada mágica y te vuelves un guerrero formidable. Regresas a la orilla con una nueva arma y habilidades de combate mejoradas. ⚔️"
    )


async def manejar_escudo(ctx: Context) -> None:
    await ctx.send(
        "Tomas el escudo encantado y obtienes una defensa impenetrable. Regresas a la orilla con una protección mejorada para futuras batallas. 🛡️"
    )


async def manejar_vision(ctx: Context) -> None:
    await ctx.send(
        "Bebes del agua mágica y recibes una visión del futuro que te ayuda a tomar decisiones sabias en tu aventura. Regresas a la orilla con una perspectiva reveladora. 🔮"
    )


async def manejar_curacion(ctx: Context) -> None:
    await ctx.send(
        "Bebes del agua curativa y sanas todas tus heridas. Estás completamente curado y listo para continuar tu aventura. Regresas a la orilla con plena salud. 💧"
    )


async def manejar_explorar(ctx: Context) -> None:
    await ctx.send(
        "Exploras el reino mágico y encuentras un mapa antiguo que revela ubicaciones secretas y tesoros escondidos. Regresas a la orilla con un mapa de tesoros. 🗺️"
    )


async def manejar_regresar(ctx: Context) -> None:
    await ctx.send(
        "Decides regresar a tu punto de partida y continúas con tu vida, sabiendo que el reino mágico estará allí para futuras visitas. Regresas a la orilla con historias fascinantes. 🌟"
    )


async def manejar_usar_hechizo(ctx: Context) -> None:
    await ctx.send(
        "Usas el hechizo del pergamino y obtienes un poder especial que te ayudará en tus aventuras. Regresas a la orilla con una habilidad mágica recién adquirida. ✨"
    )


async def manejar_guardar_hechizo(ctx: Context) -> None:
    await ctx.send(
        "Decides guardar el hechizo para más tarde. Regresas a la orilla, con la opción de usar el hechizo en otro momento. 🧙‍♂️"
    )
