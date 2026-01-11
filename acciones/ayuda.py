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
            "**>llama [pregunta]**\n"
            "Habla con la IA Llama sobre Python.\n"
            "Ejemplo: `>llama ¿Cómo uso listas por comprensión?`\n\n"
            "**>llama_stats**\n"
            "Muestra tus estadísticas personales de uso de Llama.\n\n"
            "**>llama_stats True**\n"
            "Muestra las estadísticas globales del día para la IA Llama.\n\n"
            "**>llama_dashboard**\n"
            "Visualiza un resumen visual (tabla) de las métricas globales de la IA Llama.\n\n"
            "**>deepseek [--lang código] [pregunta]**\n"
            "Habla con la IA DeepSeek sobre cualquier tema o analiza imágenes.\n"
            "Con memoria persistente y soporte multilingüe. Respuestas en embeds coloridos.\n"
            "Ejemplos:\n"
            "• `>deepseek ¿Qué es la computación cuántica?`\n"
            "• `>deepseek --lang en Tell me about quantum computing`\n"
            "• `>deepseek --lang fr` (adjuntando una imagen)\n\n"
            "**>deepseek_reset**\n"
            "Reinicia tu historial de conversación con DeepSeek para empezar desde cero.\n\n"
            "**>deepseek_help**\n"
            "Muestra información detallada sobre el uso de DeepSeek y los idiomas soportados."
        )
    elif categoria == "juegos":
        return (
            "**>tateti**\n"
            "Juega tateti contra el bot o un amigo.\n\n"
            "**>adivina**\n"
            "Adivina la letra oculta.\n\n"
            "**>chiste**\n"
            "Te cuento un chiste.\n\n"
            "**>aventura**\n"
            "Inicia una aventura de texto."
        )
    elif categoria == "utilidades":
        return (
            "**>gracias @usuario**\n"
            "Agradece a alguien y suma puntos al ranking.\n\n"
            "**>ranking**\n"
            "Muestra el ranking de agradecimientos.\n\n"
            '**>encuesta "Pregunta" "Opción1" "Opción2"...**\n'
            "Crea una encuesta rápida.\n\n"
            "**>claves**\n"
            "Muestra palabras clave para activar respuestas sin prefijo.\n\n"
            "**oyente**\n"
            "Haz preguntas comunes, el bot responde automáticamente."
        )
    elif categoria == "moderacion":
        return "**>vigilante**\nMonitorea malas palabras y aplica advertencias."
    elif categoria == "otros":
        return (
            "**>ayuda**\n"
            "Muestra este mensaje de ayuda.\n\n"
            "**>info**\n"
            "Muestra información del servidor y temperatura del CPU.\n\n"
            "**>hola**\n"
            "Saluda al bot.\n\n"
            "**>cafe**\n"
            "Muestra las opciones de café.\n\n"
            "**>frases**\n"
            "Frases motivadoras.\n\n"
            "**>traducir [texto]**\n"
            "Traduce un texto al español.\n\n"
            "**>youtube [tipo de música]**\n"
            "Busca un video en YouTube.\n\n"
            "**>abrazo [@usuario]**\n"
            "Abraza a un usuario o a ti mismo con >me_abrazo."
        )
    elif categoria in ("novedades", "tips"):
        return (
            "**🆕 NOVEDADES IA**\n"
            "- **Persistencia en DeepSeek:** Ahora tu historial de chat se guarda incluso si el bot se reinicia.\n"
            "- **>deepseek_reset:** Comando para reiniciar tu historial de conversación.\n"
            "- Consulta tus estadísticas personales y globales con `>llama_stats` y `>llama_stats True`.\n"
            "- Visualiza un dashboard simple con `>llama_dashboard`.\n\n"
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
