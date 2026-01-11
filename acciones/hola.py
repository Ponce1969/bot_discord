# Aqui realizamos la funcion hola que da la bienvenida al usuario y le cuenta de que trata el servidor.
# Esta funcion es llamada por el servidor cuando el usuario se conecta.
# La funcion recibe como parametro el socket del usuario y el nombre del usuario.

import asyncio


async def hola(usuario, nombre):
    mensajes = []
    mensajes.append(await usuario.send(f"Bienvenido a nuestro servidor, {nombre}.\n"))
    await asyncio.sleep(2)
    mensajes.append(
        await usuario.send("Este servidor es para compartir y divertirse.\n")
    )
    await asyncio.sleep(5)
    mensajes.append(
        await usuario.send(
            "Para enviar un mensaje a un usuario en particular, escribe @nombre mensaje y presiona enter.\n"
        )
    )
    await asyncio.sleep(5)
    mensajes.append(
        await usuario.send(
            "Para ver las funciones que tiene pythonbot, escribe ```>ayuda``` y presiona enter.\n"
        )
    )
    await asyncio.sleep(6)
    mensajes.append(
        await usuario.send("Disfruta de tu estancia en nuestro servidor.\n")
    )
    return mensajes
