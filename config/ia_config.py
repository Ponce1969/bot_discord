"""
Configuración para los modelos de IA Gemini.
Este módulo contiene todas las configuraciones necesarias para los modelos de texto e imagen.
"""
from typing import Dict, List

# Configuración para generación de texto
text_generation_config: Dict = {
    "temperature": 0.9,  # Controla la creatividad de las respuestas
    "top_p": 1,         # Núcleo de probabilidad acumulativa
    "top_k": 1,         # Número de tokens a considerar
    "max_output_tokens": 2000,  # Aumentado para respuestas más largas
}

# Configuración para generación de imágenes
image_generation_config: Dict = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 500,
}

# Configuración de seguridad para filtrar contenido inapropiado
safety_settings: List[Dict] = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

# Configuraciones de Discord
MAX_MESSAGE_LENGTH = 2000  # Límite de caracteres por mensaje de Discord
MAX_HISTORY_LENGTH = 10    # Máximo número de mensajes en el historial
EMBED_COLORS = {
    "default": 0x3498db,  # Azul para mensajes normales
    "success": 0x2ecc71,  # Verde para éxitos
    "error": 0xe74c3c,    # Rojo para errores
    "warning": 0xf1c40f   # Amarillo para advertencias
}
