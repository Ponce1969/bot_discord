import asyncio

from discord import Message
from discord.ext.commands import Context


async def manejar_montania(ctx: Context, nombre_ficticio: str) -> None:
    """
    Maneja la aventura en la montaña.
    Este método maneja la aventura del jugador en la montaña. El jugador tiene la opción de subir la montaña o rodearla. Dependiendo de la elección, se presentarán diferentes escenarios y decisiones que el jugador debe tomar. Al final de la aventura, se mostrará un mensaje de finalización dependiendo de las elecciones del jugador.
    Parámetros:
    - ctx (Context): El contexto de la ejecución del comando.
    - nombre_ficticio (str): El nombre ficticio del jugador.
    Retorno:
    None
    """
    await ctx.send(
        f"{nombre_ficticio}, te encuentras en la base de una montaña. ¿Qué decides hacer? ¿Subir la montaña o rodearla? (subir o rodear) 🏔️"
    )

    try:
        decision_camino = await obtener_decision(ctx, ["subir", "rodear"])
        if decision_camino == "subir":
            await manejar_subida(ctx)
        elif decision_camino == "rodear":
            await manejar_rodeo(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! La montaña se ha vuelto peligrosa y debes regresar a la base. ⚠️"
        )


async def obtener_decision(ctx: Context, opciones: list) -> str:
    def check(msg: Message) -> bool:
        return msg.author == ctx.author and msg.content.lower() in opciones

    mensaje: Message = await ctx.bot.wait_for("message", check=check, timeout=60)
    return mensaje.content.lower()


async def manejar_subida(ctx: Context) -> None:
    await ctx.send(
        "Decides subir la montaña. Mientras subes, encuentras una cueva en tu camino. ¿Decides entrar en la cueva o continuar subiendo la montaña? (entrar o continuar) 🧗‍♂️"
    )
    try:
        decision_cueva = await obtener_decision(ctx, ["entrar", "continuar"])
        if decision_cueva == "entrar":
            await manejar_cueva(ctx)
        elif decision_cueva == "continuar":
            await manejar_continuacion(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! La montaña se ha vuelto peligrosa y debes regresar a la base. ⚠️"
        )


async def manejar_cueva(ctx: Context) -> None:
    await ctx.send(
        "Al entrar en la cueva, te das cuenta de que es muy grande y hay un olor raro a humedad. Algo extraño está pasando aquí... 😨"
    )
    await ctx.send(
        "Caminando por la cueva, encuentras huesos humanos y una especie de altar en un rincón oscuro. ¡Qué miedo! 💀"
    )
    await ctx.send(
        "Entre los huesos, encuentras un escudo antiguo y oxidado y una ballesta con muchas flechas. ¿Quieres tomar el escudo y la ballesta o dejarlos? (tomar o dejar) 🏹🛡️"
    )
    try:
        decision_tesoros = await obtener_decision(ctx, ["tomar", "dejar"])
        if decision_tesoros == "tomar":
            await manejar_tesoros(ctx)
        elif decision_tesoros == "dejar":
            await manejar_lago(ctx)
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! La cueva se ha vuelto peligrosa y debes regresar a la base de la montaña. ⚠️"
        )


async def manejar_tesoros(ctx: Context) -> None:
    await ctx.send(
        "¡Tomaste el escudo y la ballesta! De repente, la cueva comienza a temblar y una roca bloquea la salida. Debes encontrar una manera de salir. 🚪"
    )
    await ctx.send(
        "Encuentras una serie de túneles en la cueva. ¿Qué haces? ¿Exploras los túneles o buscas otra salida? (explorar o buscar) 🔦"
    )
    try:
        decision_tuneles = await obtener_decision(ctx, ["explorar", "buscar"])
        if decision_tuneles == "explorar":
            await ctx.send(
                "Exploras los túneles y encuentras una salida secreta. Regresas a la base de la montaña y encuentras una pequeña aldea donde la gente te agradece por liberar la cueva de los antiguos peligros. 🏡"
            )
            await ctx.send(
                "¡La aldea te recompensa con oro y una casa! ¡Has tenido un final feliz y te conviertes en un héroe local! 🎉"
            )
        elif decision_tuneles == "buscar":
            await ctx.send(
                "Buscas otra salida y, después de mucho esfuerzo, encuentras una ruta oculta. Regresas a la base de la montaña y encuentras que el oro y los tesoros antiguos se han perdido en la confusión. 💔"
            )
            await ctx.send(
                "¡Aunque no encuentras tesoros, tienes una experiencia valiosa y una nueva perspectiva sobre la vida! 🌟"
            )
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! La cueva se ha vuelto peligrosa y debes regresar a la base de la montaña. ⚠️"
        )


async def manejar_lago(ctx: Context) -> None:
    await ctx.send(
        "Decides dejar el escudo y la ballesta. Salgas de la cueva y continúas tu camino. 🚶‍♂️"
    )
    await ctx.send(
        "Más arriba en la montaña, encuentras un misterioso lago con una vista impresionante. ¡Parece que este lugar tiene un secreto! 🌅"
    )
    await ctx.send(
        "¿Quieres investigar el lago o continuar subiendo? (investigar o continuar) 🕵️‍♂️"
    )
    try:
        decision_lago = await obtener_decision(ctx, ["investigar", "continuar"])
        if decision_lago == "investigar":
            await ctx.send(
                "Investigas el lago y encuentras una antigua cabaña con un tesoro escondido. ¡Te llevas el tesoro y regresas a la base de la montaña como un héroe! 💰"
            )
            await ctx.send(
                "¡El tesoro te proporciona riquezas y reconocimiento en todo el reino! 👑"
            )
        elif decision_lago == "continuar":
            await ctx.send(
                "Decides continuar subiendo y finalmente llegas a la cima. ¡La vista es impresionante y te sientes en paz con el mundo! 🏞️"
            )
            await ctx.send(
                "¡Tu aventura en la montaña ha terminado, pero tu vida está llena de nuevas posibilidades! ✨"
            )
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! La montaña se ha vuelto peligrosa y debes regresar a la base. ⚠️"
        )


async def manejar_continuacion(ctx: Context) -> None:
    await ctx.send(
        "Decides continuar subiendo la montaña. Mientras subes, ves muchas cabras montesas y un par de águilas volando. No encuentras nada más en tu camino. 🦅"
    )
    await ctx.send(
        "¡En ese momento, ves una inscripción en una roca que parece ser un mapa de un tesoro escondido en la montaña! 📜"
    )
    await ctx.send(
        "¿Quieres tomar el mapa o continuar subiendo la montaña? (tomar o dejar) 🗺️"
    )
    try:
        decision_mapa = await obtener_decision(ctx, ["tomar", "dejar"])
        if decision_mapa == "tomar":
            await ctx.send(
                "¡Tomaste el mapa! Empiezas a buscar el tesoro siguiendo las indicaciones del mapa. 🗺️"
            )
            await ctx.send(
                "Encuentras una cueva secreta con un cofre lleno de oro y gemas. ¡Eres rico! 💎"
            )
            await ctx.send(
                "Decides regresar al pueblo y compartir tu hallazgo con los demás. Eres celebrado como un héroe y todos están agradecidos. 🏆"
            )
        elif decision_mapa == "dejar":
            await ctx.send(
                "Decides continuar subiendo la montaña. No encuentras nada más en tu camino. 🌧️"
            )
            await ctx.send(
                "¡Empieza a llover y un rayo cae en un árbol, rompiéndolo en mil pedazos. Sale fuego, y te acercas a calentarte! 🔥"
            )
            await ctx.send(
                "Después de la tormenta, encuentras una piedra preciosa en los escombros. 💎"
            )
            await ctx.send(
                "¿Quieres llevar la piedra al pueblo o esconderla allí mismo? (llevar o esconder) 🏠"
            )
            try:
                decision_piedra = await obtener_decision(ctx, ["llevar", "esconder"])
                if decision_piedra == "llevar":
                    await ctx.send(
                        "Llevas la piedra al pueblo y se convierte en un objeto de gran valor. Eres admirado por tu valentía y astucia. 🏅"
                    )
                    await ctx.send(
                        "¡Tu nombre se convierte en leyenda y tu vida está llena de éxito y respeto! 🌟"
                    )
                elif decision_piedra == "esconder":
                    await ctx.send(
                        "Escondes la piedra en la montaña. Aunque es una piedra preciosa, prefieres mantenerla en secreto. 🤐"
                    )
                    await ctx.send(
                        "Continúas tu vida con la satisfacción de haber hecho una gran aventura, pero sin el reconocimiento. 🌄"
                    )
            except asyncio.TimeoutError:
                await ctx.send(
                    "¡Te has tardado mucho en decidir! La piedra se ha perdido en el caos de la tormenta. 🌩️"
                )
    except asyncio.TimeoutError:
        await ctx.send(
            "¡Te has tardado mucho en decidir! La montaña se ha vuelto peligrosa y debes regresar a la base. ⚠️"
        )


async def manejar_rodeo(ctx: Context) -> None:
    await ctx.send(
        "Decides rodear la montaña. El camino es largo y sinuoso, pero logras evitar los peligros de la montaña. 🏞️"
    )
    await ctx.send(
        "Encuentras un pequeño pueblo al final del camino. La gente del pueblo te invita a quedarte con ellos y compartir historias de tus aventuras. 🏡"
    )
    await ctx.send(
        "Decides quedarte en el pueblo y contarles tus historias. Ellos te agradecen y te ofrecen un lugar para vivir en paz. 🌟"
    )
    await ctx.send(
        "¡Tu vida en el pueblo es tranquila y feliz, y disfrutas de tus días rodeado de amigos y nuevos compañeros! 😊"
    )
