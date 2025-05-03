# Asocia las palabras clave con las preguntas y respuestas en la base de datos
# y responde a las preguntas del usuario si se encuentra una coincidencia.
# Este archivo es un ejemplo de cómo se puede implementar un oyente en un bot de Discord
from base.database import get_db
from acciones.oyente import fuzzy_match, direct_keyword_answer, fuzzy_suggestions
from discord.ext import commands
import discord
import logging
import unicodedata
import re

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Logger para preguntas no entendidas
noent_logger = logging.getLogger('preguntas_no_entendidas')
noent_handler = logging.FileHandler('preguntas_no_entendidas.log', encoding='utf-8')
noent_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
noent_logger.addHandler(noent_handler)
noent_logger.setLevel(logging.INFO)

def normalize_text(text):
    # Eliminar acentos, convertir a minúsculas y eliminar caracteres especiales
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

class OyenteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keywords = {
            "ia": {
                "aliases": ["inteligencia artificial", "asistente", "gemini", "llama"],
                "faq": ["¿Qué IA tenemos?", "¿Tenemos alguna IA en el canal?", "¿Hay una IA en el canal?"],
                "custom_response": "¡Sí! Tenemos asistentes IA como Gemini y Llama. Pregunta por '>ayuda ia' para más info."
            },
            "juegos": {
                "aliases": ["jugar", "diversión", "tateti"],
                "faq": ["¿Qué juegos hay?", "¿Dónde puedo jugar?", "¿Cómo puedo jugar?", "¿Qué podemos jugar?"],
                "custom_response": None
            },
            "hacer": {
                "aliases": ["funciones", "capacidades", "comandos"],
                "faq": ["¿Qué puedes hacer?", "¿Qué hace el bot?", "¿Para qué sirve el bot?"],
                "custom_response": "Puedo ayudarte con juegos, IA, música, encuestas y más. Escribe '>ayuda' para ver todo lo que puedo hacer."
            },
            "ayuda": {
                "aliases": ["soporte", "asistencia", "necesito ayuda"],
                "faq": ["¿Puedes ayudarme?", "¿Necesito ayuda?"],
                "custom_response": "¿Necesitas ayuda? Usa '>ayuda' o pregunta por una categoría como '>ayuda ia' o '>ayuda juegos'."
            },
            "musica": {
                "aliases": ["canciones", "escuchar música"],
                "faq": ["¿Qué música tenemos?", "¿Puedo escuchar música?"],
                "custom_response": None
            },
            "chat": {
                "aliases": ["charla", "general", "propósito del chat"],
                "faq": ["¿Qué hacen en este chat general?", "¿Cuál es el propósito de este chat?"],
                "custom_response": None
            },
            # Puedes agregar más keywords siguiendo este formato
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignorar mensajes de otros bots

        if message.content.startswith('>'):
            return  # Ignorar mensajes que comienzan con '>'

        user_input = normalize_text(message.content)
        logger.debug(f"Normalized user input: {user_input}")

        user_words = user_input.split()
        matched_keywords = [keyword for keyword in self.keywords.keys() if keyword in user_words]
        logger.debug(f"Matched keywords: {matched_keywords}")

        if not matched_keywords:
            logger.debug("No keywords matched.")
            return  # Si no encuentra ninguna palabra clave, no hace nada

        # Respuesta directa por palabra clave exacta usando función reutilizable
        direct_question = direct_keyword_answer(user_input, self.keywords)
        if direct_question:
            embed = discord.Embed(
                title="🔎 Respuesta rápida",
                description=f"{direct_question}\n\n¿Quieres saber más? Prueba con preguntas como: `¿Qué IA tenemos?`, `¿Cómo puedo jugar?`, etc.",
                color=discord.Color.teal()
            )
            embed.set_footer(text="¿La respuesta fue útil? Reacciona con 👍 o 👎")
            await message.channel.send(embed=embed, delete_after=40)
            await message.delete(delay=40)
            logger.info(f"Respuesta directa por keyword: {user_input}")
            return

        # Obtener sesión de la base de datos usando el contexto de administrador
        with next(get_db()) as session:
            try:
                # Buscar la mejor coincidencia usando fuzzy_match (umbral adaptativo)
                question, answer = fuzzy_match(user_input, session, matched_keywords)
                logger.debug(f"Matched question: {question}")
                logger.debug(f"Matched answer: {answer}")
                if question and answer:
                    if len(answer) > 80:
                        embed = discord.Embed(
                            title="💡 Respuesta a tu pregunta",
                            description=answer,
                            color=discord.Color.teal()
                        )
                        embed.set_footer(text="¿La respuesta fue útil? Reacciona con 👍 o 👎")
                        await message.channel.send(embed=embed, delete_after=40)
                    else:
                        await message.channel.send(f"💡 {answer}", delete_after=40)
                    await message.delete(delay=40)
                else:
                    # Sugerencias inteligentes
                    suggestions = fuzzy_suggestions(user_input, session, matched_keywords, topn=3)
                    if suggestions:
                        suggestion_text = '\n'.join([f'• {s}' for s in suggestions])
                        embed = discord.Embed(
                            title="🤔 ¿Quizás quisiste preguntar...?",
                            description=f"{suggestion_text}\n\nSi ninguna es lo que buscas, intenta ser más específico o usa `>ayuda`.",
                            color=discord.Color.blue()
                        )
                        embed.set_footer(text="¿La sugerencia fue útil? Reacciona con 👍 o 👎")
                        await message.channel.send(embed=embed, delete_after=40)
                        await message.delete(delay=40)
                        logger.info(f"Sugerencias ofrecidas: {suggestions}")
                        # Logging de pregunta no entendida
                        noent_logger.info(f"Usuario: {message.author} | Pregunta: '{message.content}' | Sugerencias: {suggestions}")
                    else:
                        msg = "😕 Ups, no logré entender tu pregunta. Intenta ser más específico o revisa las opciones con `>ayuda`."
                        await message.channel.send(msg, delete_after=40)
                        await message.delete(delay=40)
                        logger.debug("No matching question and answer found, ni sugerencias.")
                        # Logging de pregunta no entendida
                        noent_logger.info(f"Usuario: {message.author} | Pregunta: '{message.content}' | Sugerencias: []")
            except Exception as e:
                logger.error(f"Error al procesar el mensaje: {e}")
                await message.channel.send("Ocurrió un error al procesar tu pregunta. Por favor, intenta nuevamente más tarde.", delete_after=40)
                await message.delete(delay=40)
            finally:
                session.close()  # Cerrar la sesión de la base de datos

# Función para registrar el cog en el bot
async def setup(bot):
    await bot.add_cog(OyenteCog(bot))
