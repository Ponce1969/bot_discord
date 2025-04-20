# Aqui va la funcion de ayuda, que muestra todo lo que puede hacer el bot

def ayuda() -> str:
    ayuda_msg = """
\`\`\`
Comandos disponibles para el bot:
- **>cafe**: Muestra las opciones de café disponibles.
- **>hola**: Saluda al bot.
- **>ayuda**: Muestra este mensaje de ayuda.
- **>tomar**: Toma un trago solo o acompañado.
- **>frases**: Te muestra frases motivadoras.
- **>traducir**: Traduce un texto al español.
- **>youtube**: Busca un video en YouTube, debes ingresar el tipo de musica (tango).
- **>info**: Muestra información del servidor mas temperatura del cpu.
- **>gemini**: Inicia una conversación con la IA de Gemini.
- **>gemini_imagen**: Muestra una foto a la IA y te dira su contenido, en varios formatos.
- **>gemini_reset**: Reinicia la conversación con la IA de Gemini.
- **>abrazo**: Abraza a un usuario, debes ingresar el nombre del @usuario.
- **>abrazo**: Al no ingresar un nombre, el bot abraza a nadie.
- **>me_abrazo**: se abraza a si mismo.
- **>llama**: Inicia una conversación con la IA de Llama, sobre codigo Python.
- **>adivina**: Juego de adivinanzas, debes ingresar una letra .
- **>chiste**: Muestra un chiste , como tiene alias, puedes usar >chistes.
- **>aventura**: Inicia una aventura de texto, debes ingresar al chat_juego_aventura.
- **>gracias**: con el comando >gracias @usuario, agradece a un usuario, sumnando puntos para un ranking.
- **>ranking**: Muestra el ranking de los usuarios que han sido agradecidos.
- **>vigilante**: cuida las malas palabras, si las detecta, te avisa y te da una advertencia, al llegar a 3 advertencias, te banea por 24 horas.
- **>tateti**: Inicia un nuevo juego de tateti, debes ingresar una opcion de jugar contra el bot o contra otro usuario.
- **>tateti_ganadores**: Muestra la lista de ganadores del juego de tateti.
- **>encuesta**: Crea una encuesta con varias opciones, debes ingresar la pregunta y las opciones, entre comillas para el embed.
- **>claves**: Muestra las palabras clave que puedes usar, para el comando  oyente y el bot responde, sin necesidad de usar el prefijo >.
- **oyente**: preguntas y respuestas, comunes y el bot responde usamos fuzzywuzzy, python-Levenshtein.
\`\`\`
"""
    return ayuda_msg

