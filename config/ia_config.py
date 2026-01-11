"""
Configuración para los modelos de IA DeepSeek.
Este módulo contiene todas las configuraciones necesarias para los modelos de texto e imagen.
"""

# Configuración para generación de texto
text_generation_config: dict = {
    "temperature": 0.9,  # Controla la creatividad de las respuestas
    "top_p": 1,  # Núcleo de probabilidad acumulativa
    "top_k": 1,  # Número de tokens a considerar
    "max_output_tokens": 2000,  # Aumentado para respuestas más largas
}

# Configuración para generación de imágenes
image_generation_config: dict = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 500,
}

# Tipos MIME soportados por DeepSeek Vision
SUPPORTED_MIME_TYPES: set[str] = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/heic",
    "image/heif",
}

# Configuración de seguridad para filtrar contenido inapropiado
safety_settings: list[dict] = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Configuraciones de Discord
MAX_MESSAGE_LENGTH = 2000  # Límite de caracteres por mensaje de Discord
MAX_HISTORY_LENGTH = 10  # Máximo número de mensajes en el historial

# Colores base para rotación en embeds
BASE_EMBED_COLORS = [
    0x50C878,  # Esmeralda (verde)
    0x4287F5,  # Azul vibrante
    0x9400D3,  # Púrpura oscuro
    0xFF8C00,  # Naranja oscuro
    0xDC143C,  # Carmesí
]

# Mapeo de códigos de idioma para instrucciones a DeepSeek
LANGUAGE_MAP = {
    "es": "español",
    "en": "English",
    "fr": "français",
    "pt": "português",
    "it": "italiano",
    "de": "Deutsch",
    "ru": "русский",
    "zh": "中文",
    "ja": "日本語",
    "ko": "한국어",
}

# Tiempo máximo de espera para respuestas de DeepSeek (en segundos)
DEEPSEEK_TIMEOUT = 60.0

# Colores para embeds
EMBED_COLORS = {
    "default": 0x3498DB,  # Azul para mensajes normales
    "success": 0x2ECC71,  # Verde para éxitos
    "error": 0xE74C3C,  # Rojo para errores
    "warning": 0xF1C40F,  # Amarillo para advertencias
}
