from fuzzywuzzy import process
from sqlalchemy.orm import Session
from base.database import FAQ
import dask.dataframe as dd
import pandas as pd
import logging
import unicodedata
import re

# Configurar el logger
logging.basicConfig(level=logging.INFO)  # Cambiar a DEBUG para más detalles
logger = logging.getLogger(__name__)

def normalize_text(text):
    # Eliminar acentos
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def get_questions_and_answers(session: Session):
    faqs = session.query(FAQ).yield_per(10)
    df = pd.DataFrame([(faq.question, faq.answer, faq.keyword) for faq in faqs], columns=['question', 'answer', 'keyword'])
    ddf = dd.from_pandas(df, npartitions=1)
    return ddf

def direct_keyword_answer(user_input: str, keywords: dict):
    """
    Busca coincidencia exacta o por sinónimos (aliases) y responde con mensaje personalizado si existe, si no con la primera pregunta frecuente.
    La estructura de keywords debe ser:
    {
        'ia': {
            'aliases': ['inteligencia artificial', 'asistente', 'gemini', 'llama'],
            'faq': ["¿Qué IA tenemos?", ...],
            'custom_response': "¡Sí! Tenemos asistentes IA como Gemini y Llama. Pregunta por '>ayuda ia' para más info."
        },
        ...
    }
    """
    user_input = normalize_text(user_input)
    for key, data in keywords.items():
        # Coincidencia exacta con la keyword principal
        if user_input == normalize_text(key):
            if data.get('custom_response'):
                return data['custom_response']
            if data.get('faq') and len(data['faq']) > 0:
                return data['faq'][0]
        # Coincidencia con algún alias
        for alias in data.get('aliases', []):
            if user_input == normalize_text(alias):
                if data.get('custom_response'):
                    return data['custom_response']
                if data.get('faq') and len(data['faq']) > 0:
                    return data['faq'][0]
    return None

def fuzzy_match(user_input: str, session: Session, keywords: list, min_score: int = 70):
    df = get_questions_and_answers(session)
    # Filtrar las preguntas que contienen las palabras clave, manejando valores nulos
    filtered_df = df[df['keyword'].apply(lambda x: any(normalize_text(keyword) in normalize_text(x) for keyword in keywords) if pd.notna(x) else False, meta=('keyword', 'bool'))].compute()
    logger.debug(f"Filtered DataFrame: {filtered_df}")
    questions = filtered_df['question'].tolist()
    logger.debug(f"Filtered questions: {questions}")
    # Ajustar el umbral para preguntas muy cortas
    if len(user_input.split()) <= 2:
        min_score = 50
    # Encontrar la mejor coincidencia usando fuzzywuzzy
    best_match = process.extractOne(user_input, questions)
    logger.debug(f"Best match: {best_match}")
    if best_match and best_match[1] >= min_score:
        answer = filtered_df[filtered_df['question'] == best_match[0]]['answer'].values[0]
        return best_match[0], answer
    return None, None

def fuzzy_suggestions(user_input: str, session: Session, keywords: list, topn: int = 3):
    df = get_questions_and_answers(session)
    filtered_df = df[df['keyword'].apply(lambda x: any(normalize_text(keyword) in normalize_text(x) for keyword in keywords) if pd.notna(x) else False, meta=('keyword', 'bool'))].compute()
    questions = filtered_df['question'].tolist()
    if not questions:
        return []
    suggestions = process.extract(user_input, questions, limit=topn)
    logger.debug(f"Suggestions: {suggestions}")
    return [q for q, score in suggestions if score >= 40]