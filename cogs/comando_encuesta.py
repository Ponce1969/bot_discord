# Aca desarrollamos el comando de encuesta que permite a los usuarios crear una encuesta con una pregunta y varias opciones. 
# El comando se llama encuesta y se define en la clase EncuestaCog.
# El comando recibe la pregunta y las opciones como argumentos y llama a la función encuesta con estos argumentos.
# >encuesta "Pregunta" "Opción 1" "Opción 2" ... "Opción N"
from discord.ext import commands
from acciones.encuesta import encuesta

class EncuestaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='encuesta')
    async def encuesta_command(self, ctx, pregunta: str, *opciones: str):
        """
        Comando para crear una encuesta.
        Uso: !encuesta "Pregunta" "Opción 1" "Opción 2" ... "Opción N"
        """
        await encuesta(ctx, pregunta, *opciones)

# Función para registrar el cog en el bot
async def setup(bot):
    await bot.add_cog(EncuestaCog(bot))