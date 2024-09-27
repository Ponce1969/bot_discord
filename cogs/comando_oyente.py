# Asocia las palabras clave con las preguntas y respuestas en la base de datos
# y responde a las preguntas del usuario si se encuentra una coincidencia.
# Este archivo es un ejemplo de cómo se puede implementar un oyente en un bot de Discord
from base.database import get_db
from acciones.oyente import fuzzy_match
from discord.ext import commands

class OyenteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keywords = {
            "bot": ["¿Qué puedes hacer?", "¿Qué hace el bot?"],
            "jugar": ["¿Dónde puedo jugar?", "¿Cómo puedo jugar?"]
            # Agrega más palabras clave y preguntas aquí
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignorar mensajes de otros bots

        user_input = message.content.lower()

        # Filtrar las keywords de manera eficiente
        keyword_found = any(keyword in user_input for keyword in self.keywords.keys())

        if not keyword_found:
            return  # Si no encuentra ninguna palabra clave, no hace nada

        # Obtener sesión de la base de datos usando el contexto de administrador
        with next(get_db()) as session:
            try:
                # Buscar la mejor coincidencia usando fuzzy_match
                question, answer = fuzzy_match(user_input, session)
                if question and answer:
                    await message.channel.send(answer)  # Enviar la respuesta al canal
            except Exception as e:
                print(f"Error al procesar el mensaje: {e}")
            finally:
                session.close()  # Cerrar la sesión de la base de datos

# Función para registrar el cog en el bot
async def setup(bot):
    await bot.add_cog(OyenteCog(bot))

