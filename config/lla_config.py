import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

if not GROQ_API_KEY or not GROQ_MODEL:
    raise ValueError(
        "Las variables de entorno GROQ_API_KEY y GROQ_MODEL deben estar definidas."
    )
