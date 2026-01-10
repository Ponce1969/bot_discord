import asyncio
import datetime

import pytz
from discord import Embed
from groq import Groq

from base.database import add_response_time, increment_llama_metric
from config.lla_config import GROQ_API_KEY, GROQ_MODEL

# Configurar la zona horaria de Uruguay
URUGUAY_TZ = pytz.timezone('America/Montevideo')

# TokenManager puede mantenerse si deseas un límite diario adicional, pero las métricas reales se guardan en la base de datos.
class TokenManager:
    def __init__(self, daily_limit=500, tokens_per_request=10):
        self.daily_limit = daily_limit
        self.tokens_per_request = tokens_per_request
        self.tokens_used = 0
        now_uy = datetime.datetime.now(URUGUAY_TZ)
        tomorrow_uy = now_uy.date() + datetime.timedelta(days=1)
        self.reset_time = URUGUAY_TZ.localize(datetime.datetime.combine(tomorrow_uy, datetime.datetime.min.time()))

    def reset_tokens(self):
        if datetime.datetime.now(URUGUAY_TZ) >= self.reset_time:
            self.tokens_used = 0
            now_uy = datetime.datetime.now(URUGUAY_TZ)
            tomorrow_uy = now_uy.date() + datetime.timedelta(days=1)
            self.reset_time = URUGUAY_TZ.localize(datetime.datetime.combine(tomorrow_uy, datetime.datetime.min.time()))

    def can_use_tokens(self) -> bool:
        self.reset_tokens()
        return self.tokens_used + self.tokens_per_request <= self.daily_limit

    def use_tokens(self) -> bool:
        if self.can_use_tokens():
            self.tokens_used += self.tokens_per_request
            return True
        return False

# Helper para registrar métricas desde comandos
async def registrar_metricas_llama(user_id, tokens_usados, response_time, fue_archivo=False, fallo_api=False):
    increment_llama_metric(user_id, "llama_uses")
    increment_llama_metric(user_id, "tokens_used", tokens_usados)
    add_response_time(user_id, response_time)
    if fue_archivo:
        increment_llama_metric(user_id, "responses_as_file")
    if fallo_api:
        increment_llama_metric(user_id, "api_failures")

class GroqHandler:

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile", temperature: float = 0.7):

        """Inicializa el manejador de Groq con la API key y el modelo especificados."""

        self.client = Groq(api_key=api_key)

        self.client.model = model

        self.temperature = temperature

        self.system_message = (

            "Eres un asistente experto en Python, especializado en el desarrollo de software. "

            "Tu objetivo es ayudar a desarrolladores junior a mejorar sus habilidades en Python. "

            "Puedes responder preguntas sobre sintaxis, bibliotecas, frameworks, buenas prácticas y otros temas relacionados con Python. "

            "Por favor, asegúrate de que tus respuestas sean claras, concisas y orientadas a la enseñanza."

        )


    def _get_response_sync(self, user_message: str) -> str:

        """Obtiene la respuesta del modelo Groq de manera síncrona."""

        chat_completion = self.client.chat.completions.create(

            messages=[

                {"role": "system", "content": self.system_message},

                {"role": "user", "content": user_message}

            ],

            model=self.client.model,

            temperature=self.temperature,

        )

        return chat_completion.choices[0].message.content


    async def get_response(self, user_message: str) -> str:

        """Obtiene la respuesta del modelo Groq de manera asincrónica usando un thread."""

        # Usar to_thread para ejecutar la función síncrona en un hilo separado

        return await asyncio.to_thread(self._get_response_sync, user_message)

    def create_response_embed(self, username: str, response: str) -> Embed:
        """Crea un embed para la respuesta del bot."""
        embed = Embed(
            title="Respuesta del Asistente de Python",
            description=response,
            color=0x00ff00  # Color verde
        )
        # Usar la zona horaria de Uruguay para el timestamp
        embed.set_footer(text=f"Pedido por {username} a las {datetime.datetime.now(URUGUAY_TZ).strftime('%H:%M:%S')}")
        return embed

# Inicializar instancias globales para usar en otros módulos
token_manager = TokenManager()
groq_handler = GroqHandler(api_key=GROQ_API_KEY, model=GROQ_MODEL)

class GroqSession:
    """Context manager asíncrono para manejar sesiones con tokens."""
    def __init__(self, token_manager):
        self.token_manager = token_manager
        self.allowed = False

    async def __aenter__(self):
        self.allowed = self.token_manager.use_tokens()
        return self.allowed

    async def __aexit__(self, exc_type, exc, tb):
        pass  # Aquí puedes loggear errores si lo deseas
