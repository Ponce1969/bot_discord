import time
from groq import Groq
from typing import Optional
from config.lla_config import GROQ_API_KEY, GROQ_MODEL

class TokenManager:
    def __init__(self, daily_limit=500, tokens_per_request=10):
        self.daily_limit = daily_limit
        self.tokens_per_request = tokens_per_request
        self.tokens_used = 0
        self.reset_time = time.time() + 24 * 60 * 60  # 24 horas desde ahora

    def reset_tokens(self):
        if time.time() >= self.reset_time:
            self.tokens_used = 0
            self.reset_time = time.time() + 24 * 60 * 60

    def can_use_tokens(self):
        self.reset_tokens()
        return self.tokens_used + self.tokens_per_request <= self.daily_limit

    def use_tokens(self):
        if self.can_use_tokens():
            self.tokens_used += self.tokens_per_request
            return True
        return False

def initialize_groq_client_and_model(api_key: str, model: Optional[str] = "llama-3.1-70b-versatile") -> Groq:
    """Inicializa el cliente de Groq y el modelo especificado."""
    client = Groq(api_key=api_key)
    if model:
        client.model = model

    # Definimos el contexto inicial como una constante
    CONTEXT_INICIAL = (
        "Eres un experto en Python y un ingeniero de software con un gran conocimiento en este lenguaje. "
        "Estás trabajando en un proyecto de desarrollo de software en Python y debes entrenar a los junior developers. "
        "Esto te ayuda a contestar de la manera correcta con todo conocimiento aprendido como si tu fueras un experto en Python. "
        "Puedes responder preguntas sobre sintaxis, bibliotecas, frameworks, buenas prácticas y más. "
        "Recuerda que solo debes responder sobre temas relacionados con Python."
    )

    # Creamos el contexto de guía inicial
    guide_context = {
        "messages": [
            {
                "role": "assistant",
                "content": CONTEXT_INICIAL,
            },
        ]
    }

    # Agregamos el contexto de guía inicial al cliente
    client.context = guide_context

    return client