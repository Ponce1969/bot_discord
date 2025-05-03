# Aqui va la funcion de ayuda, que muestra todo lo que puede hacer el bot

# Sistema de ayuda por categorías para Discord

def ayuda(categoria: str = None) -> str:
    """
    Devuelve el mensaje de ayuda general o por categoría.
    Categorías válidas: ia, juegos, utilidades, moderacion, otros, novedades
    """
    if not categoria:
        return (
            "**🤖 Bienvenido al bot de la comunidad Python**\n\n"
            "Puedes interactuar con el bot escribiendo los comandos en el chat.\n"
            "Ejemplo: `>hola`\n\n"
            "__Categorías de ayuda disponibles:__\n"
            "- **ia**: Comandos de inteligencia artificial\n"
            "- **juegos**: Juegos y diversión\n"
            "- **utilidades**: Utilidades y comunidad\n"
            "- **moderacion**: Moderación y seguridad\n"
            "- **otros**: Otros comandos\n"
            "- **novedades**: Últimas novedades y tips\n\n"
            "Escribe `>ayuda [categoría]` para ver los comandos de esa sección.\n"
            "Ejemplo: `>ayuda ia`\n"
        )
    categoria = categoria.lower()
    if categoria == "ia":
        return (
            "__*IA y Asistentes*__\n"
            "> **>llama [pregunta]**\n> _Habla con la IA Llama sobre Python._\n> Ejemplo: `>llama ¿Cómo uso listas por comprensión?`\n\n"
            "> **>llama_stats**\n> _Muestra tus estadísticas personales de uso de Llama._\n\n"
            "> **>llama_stats True**\n> _Muestra las estadísticas globales del día para la IA Llama._\n\n"
            "> **>llama_dashboard**\n> _Visualiza un resumen visual (tabla) de las métricas globales de la IA Llama._\n\n"
            "> **>gemini [pregunta]**\n> _Habla con la IA Gemini sobre cualquier tema._\n"
        )
    elif categoria == "juegos":
        return (
            "__*Juegos y Diversión*__\n"
            "> **>tateti**\n> _Juega tateti contra el bot o un amigo._\n"
            "> **>adivina**\n> _Adivina la letra oculta._\n"
            "> **>chiste**\n> _Te cuento un chiste._\n"
            "> **>aventura**\n> _Inicia una aventura de texto._\n"
        )
    elif categoria == "utilidades":
        return (
            "__*Utilidades y Comunidad*__\n"
            "> **>gracias @usuario**\n> _Agradece a alguien y suma puntos al ranking._\n"
            "> **>ranking**\n> _Muestra el ranking de agradecimientos._\n"
            "> **>encuesta \"Pregunta\" \"Opción1\" \"Opción2\"...**\n> _Crea una encuesta rápida._\n"
            "> **>claves**\n> _Muestra palabras clave para activar respuestas sin prefijo._\n"
            "> **oyente**\n> _Haz preguntas comunes, el bot responde automáticamente._\n"
        )
    elif categoria == "moderacion":
        return (
            "__*Moderación*__\n"
            "> **>vigilante**\n> _Monitorea malas palabras y aplica advertencias._\n"
        )
    elif categoria == "otros":
        return (
            "__*Otros Comandos*__\n"
            "> **>ayuda**\n> _Muestra este mensaje de ayuda._\n"
            "> **>info**\n> _Muestra información del servidor y temperatura del CPU._\n"
            "> **>hola**\n> _Saluda al bot._\n"
            "> **>cafe**\n> _Muestra las opciones de café._\n"
            "> **>frases**\n> _Frases motivadoras._\n"
            "> **>traducir [texto]**\n> _Traduce un texto al español._\n"
            "> **>youtube [tipo de música]**\n> _Busca un video en YouTube._\n"
            "> **>abrazo [@usuario]**\n> _Abraza a un usuario o a ti mismo con >me_abrazo._\n"
        )
    elif categoria in ("novedades", "tips"):
        return (
            "**🆕 NOVEDADES IA Llama**\n"
            "- Consulta tus estadísticas personales y globales con `>llama_stats` y `>llama_stats True`.\n"
            "- Visualiza un dashboard simple con `>llama_dashboard`.\n"
            "- El bot ahora registra cuántas veces usas Llama, tokens consumidos, errores y más.\n\n"
            "**ℹ️ CONSEJOS ÚTILES**\n"
            "- ¡Puedes escribir los comandos en minúsculas o mayúsculas!\n"
            "- Usa `@usuario` para mencionar a alguien en comandos sociales.\n"
            "- Si tienes dudas, escribe `>ayuda` en cualquier momento.\n"
            "\n¡Diviértete y aprende con el bot! 😃\n"
        )
    else:
        return (
            "Categoría no reconocida. Categorías válidas: ia, juegos, utilidades, moderacion, otros, novedades.\n"
            "Ejemplo: `>ayuda juegos`"
        )

