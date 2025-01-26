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

def create_initial_context() -> dict:
    """Crea el contexto inicial para el modelo."""
    CONTEXT_INICIAL = (
        "Eres un experto en Python y desarrollo de software en Python y debes entrenar a los junior developers. "
        "Estás trabajando en un proyecto. "
        "Esto te ayuda a contestar de la manera correcta con todo conocimiento aprendido como si tu fueras un experto en Python. "
        "Puedes responder preguntas sobre sintaxis, bibliotecas, frameworks, buenas prácticas y más. "
        "Recuerda que solo debes responder sobre temas relacionados con Python."
    )

    return {
        "messages": [
            {
                "role": "system",
                "content": CONTEXT_INICIAL,
            },
        ]
    }

def initialize_groq_client(api_key: str) -> Groq:
    """Inicializa el cliente de Groq."""
    return Groq(api_key=api_key)

def set_model_and_context(client: Groq, model: Optional[str], context: dict):
    """Configura el modelo y el contexto del cliente."""
    if model:
        client.model = model
    client.context = context

def initialize_groq_client_and_model(api_key: str, model: Optional[str] = "llama-3.3-70b-versatile") -> Groq:
    """Inicializa el cliente de Groq y el modelo especificado."""
    client = initialize_groq_client(api_key)
    initial_context = create_initial_context()
    set_model_and_context(client, model, initial_context)
    return client

def get_chat_completion(client: Groq, user_message: str) -> str:
    """Obtiene una respuesta del modelo Groq."""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model=client.model,
    )
    return chat_completion.choices[0].message.content