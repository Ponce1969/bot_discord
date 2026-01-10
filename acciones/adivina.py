import asyncio
import random

# Juego de adivinar palabra secreta para Discord.

def generar_mensaje(palabra_descubierta, vidas, letras_usadas):
    return (f"**Palabra secreta:** {' '.join(palabra_descubierta)}\n"
            f"**Vidas restantes:** {vidas}\n"
            f"**Letras usadas:** {''.join(sorted(letras_usadas))}\n")

async def adivina(ctx, bot):
    palabras = ["hola", "adios", "python", "discord", "bot", "programacion", "computadora", "teclado",
                "mouse", "monitor", "ventana", "linux", "windows", "mac", "manzana", "naranja", "limon",
                "pera", "platano", "fresa", "uva", "sandia","aguacate", "coco", "cacao", "cafe",
                "melon", "papaya", "mango", "piña", "cereza", "ciruela", "durazno", "manzana", "kiwi" ]
    palabra_secreta = random.choice(palabras)
    vidas = 6
    palabra_descubierta = ["_"] * len(palabra_secreta)
    letras_usadas = set()

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and len(m.content) == 1

    await ctx.send("**Bienvenido al juego de adivinar la palabra secreta!**\n\n" + generar_mensaje(palabra_descubierta, vidas, letras_usadas) + "\n**Ingresa una letra para adivinar la palabra.**")

    while vidas > 0 and "_" in palabra_descubierta:
        try:
            mensaje = await bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send("Se acabó el tiempo! Juego terminado.")
            return

        letra = mensaje.content.lower()

        if not letra.isalpha():
            await ctx.send("Debes ingresar una letra para seguir con el juego.")
            continue

        if letra in letras_usadas:
            await ctx.send(f"Ya has usado la letra '{letra}'. Intenta con otra letra.")
            continue

        letras_usadas.add(letra)

        if letra in palabra_secreta:
            for i, char in enumerate(palabra_secreta):
                if char == letra:
                    palabra_descubierta[i] = letra
            await ctx.send("¡Bien hecho! " + generar_mensaje(palabra_descubierta, vidas, letras_usadas))
        else:
            vidas -= 1
            await ctx.send(f"Incorrecto. La letra '{letra}' no está en la palabra. " + generar_mensaje(palabra_descubierta, vidas, letras_usadas))

    if "_" not in palabra_descubierta:
        await ctx.send(f"¡Felicidades! Has adivinado la palabra secreta: **{palabra_secreta}**")
    else:
        await ctx.send(f"Has perdido. La palabra secreta era: **{palabra_secreta}**")






