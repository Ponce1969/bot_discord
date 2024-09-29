# Asocia las palabras clave con las preguntas y respuestas en la base de datos
# y responde a las preguntas del usuario si se encuentra una coincidencia.
# Este archivo es un ejemplo de cómo se puede implementar un oyente en un bot de Discord
from base.database import get_db
from acciones.oyente import fuzzy_match
from discord.ext import commands
import logging
import unicodedata
import re

# Configurar el logger
logging.basicConfig(level=logging.DEBUG)  # Cambiar a DEBUG para más detalles
logger = logging.getLogger(__name__)

def normalize_text(text):
    # Eliminar acentos
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

class OyenteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keywords = {
            "hacer": ["¿Qué puedes hacer?", "¿Qué hace el bot?", "Que hace este bot?"],
            "jugar": ["¿Dónde puedo jugar?", "¿Cómo puedo jugar?", "¿Qué podemos jugar?"],
            "ayuda": ["¿Puedes ayudarme?", "¿Necesito ayuda"],
            "juegos": ["¿Qué juegos hay?", "¿Puedo jugar algún juego?"],
            "IA": ["¿Tenemos alguna IA?", "¿Hay una IA en el canal?", "¿Qué IA tenemos?", "¿Qué IA tenemos en el canal?", "¿Tenemos alguna IA en el canal?"],
            "musica": ["¿Qué música tenemos?", "¿Puedo escuchar música?"],
            "chat": ["¿Qué hacen en este chat general?", "¿Cuál es el propósito de este chat?"],
            # Agrega más palabras clave y preguntas aquí
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignorar mensajes de otros bots

        user_input = normalize_text(message.content)
        logger.debug(f"Normalized user input: {user_input}")

        # Filtrar las keywords de manera eficiente
        matched_keywords = [keyword for keyword in self.keywords.keys() if normalize_text(keyword) in user_input]
        logger.debug(f"Matched keywords: {matched_keywords}")

        if not matched_keywords:
            logger.debug("No keywords matched.")
            return  # Si no encuentra ninguna palabra clave, no hace nada

        # Obtener sesión de la base de datos usando el contexto de administrador
        with next(get_db()) as session:
            try:
                # Buscar la mejor coincidencia usando fuzzy_match
                question, answer = fuzzy_match(user_input, session, matched_keywords)
                logger.debug(f"Matched question: {question}")
                logger.debug(f"Matched answer: {answer}")
                if question and answer:
                    # Enviar la respuesta al canal y eliminarla después de 40 segundos
                    bot_message = await message.channel.send(answer, delete_after=40)
                    # Eliminar el mensaje del usuario después de 40 segundos
                    await message.delete(delay=40)
                else:
                    # Enviar mensaje de error y eliminarlo después de 40 segundos
                    bot_message = await message.channel.send("Lo siento, no entiendo la pregunta. ¿Podrías reformularla?", delete_after=40)
                    # Eliminar el mensaje del usuario después de 40 segundos
                    await message.delete(delay=40)
                    logger.debug("No matching question and answer found.")
            except Exception as e:
                logger.error(f"Error al procesar el mensaje: {e}")
                bot_message = await message.channel.send("Ocurrió un error al procesar tu pregunta. Por favor, intenta nuevamente más tarde.", delete_after=40)
                await message.delete(delay=40)
            finally:
                session.close()  # Cerrar la sesión de la base de datos

# Función para registrar el cog en el bot
async def setup(bot):
    await bot.add_cog(OyenteCog(bot))
