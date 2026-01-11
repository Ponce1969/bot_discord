# Comando de encuesta que permite crear encuestas con una pregunta y varias opciones.
# El comando se llama encuesta y se define en la clase EncuestaCog.
# Usa el separador | para dividir la pregunta de las opciones, sin necesidad de comillas.
# Uso: >encuesta Pregunta | Opción 1 | Opción 2 | ... | Opción N
# Ejemplo: >encuesta ¿Quién gana el partido? | Peñarol | Nacional
from discord.ext import commands

from acciones.encuesta import encuesta


class EncuestaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="encuesta")
    async def encuesta_command(self, ctx, *, texto: str):
        """
        Comando para crear una encuesta.
        Uso: >encuesta Pregunta | Opción 1 | Opción 2 | ... | Opción N
        Ejemplo: >encuesta ¿Quién gana el partido? | Peñarol | Nacional
        """
        # Separar pregunta y opciones usando el delimitador |
        partes = [parte.strip() for parte in texto.split('|')]

        if len(partes) < 3:
            await ctx.send(
                "❌ **Formato incorrecto**\n"
                "Uso: `>encuesta Pregunta | Opción 1 | Opción 2`\n"
                "Ejemplo: `>encuesta ¿Quién gana? | Peñarol | Nacional`"
            )
            return

        pregunta = partes[0]
        opciones = partes[1:]

        # Llamar a la función encuesta y obtener el mensaje del embed
        embed_message = await encuesta(ctx, pregunta, *opciones)

        # Eliminar el mensaje del usuario después de 1 hora (3600 segundos)
        await ctx.message.delete(delay=3600)

        # Eliminar el mensaje del embed después de 1 hora (3600 segundos)
        await embed_message.delete(delay=3600)


# Función para registrar el cog en el bot
async def setup(bot):
    await bot.add_cog(EncuestaCog(bot))
