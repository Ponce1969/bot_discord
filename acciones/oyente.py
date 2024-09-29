from fuzzywuzzy import process
from sqlalchemy.orm import Session
from base.database import FAQ
import dask.dataframe as dd
import pandas as pd
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

def get_questions_and_answers(session: Session):
    faqs = session.query(FAQ).yield_per(10)
    df = pd.DataFrame([(faq.question, faq.answer, faq.keyword) for faq in faqs], columns=['question', 'answer', 'keyword'])
    ddf = dd.from_pandas(df, npartitions=1)
    return ddf

def fuzzy_match(user_input: str, session: Session, keywords: list):
    df = get_questions_and_answers(session)
    
    # Filtrar las preguntas que contienen las palabras clave, manejando valores nulos
    filtered_df = df[df['keyword'].apply(lambda x: any(normalize_text(keyword) in normalize_text(x) for keyword in keywords) if pd.notna(x) else False, meta=('keyword', 'bool'))].compute()
    
    # Verificar el DataFrame filtrado
    logger.debug(f"Filtered DataFrame: {filtered_df}")
    
    # Extraer las preguntas filtradas
    questions = filtered_df['question'].tolist()
    
    # Verificar las preguntas extraídas
    logger.debug(f"Filtered questions: {questions}")
    
    # Encontrar la mejor coincidencia usando fuzzywuzzy
    best_match = process.extractOne(user_input, questions)
    logger.debug(f"Best match: {best_match}")
    
    if best_match and best_match[1] >= 60:  # Umbral de similitud del 60%
        answer = filtered_df[filtered_df['question'] == best_match[0]]['answer'].values[0]
        return best_match[0], answer
    return None, None