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
- **>abrazo**: Abraza a un usuario, debes ingresar el nombre del @usuario.
- **>abrazo**: Al no ingresar un nombre, el bot abraza a nadie.
- **>me_abrazo**: se abraza a si mismo.
- **>llama**: Inicia una conversación con la IA de Llama, sobre codigo Python.
- **>adivina**: Juego de adivinanzas, debes ingresar una letra .
- **>chiste**: Muestra un chiste , como tiene alias, puedes usar >chistes.
- **>aventura**: Inicia una aventura de texto, debes ingresar al chat_juego_aventura.
\`\`\`
"""
    return ayuda_msg

