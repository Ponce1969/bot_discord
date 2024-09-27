# aqui desarollamos el codigo de listener y fuzzywuzzy para obtener la respuesta mas adecuadafrom fuzzywuzzy import process
from fuzzywuzzy import process
from sqlalchemy.orm import Session
from base.database import get_db, FAQ
import dask.dataframe as dd
import pandas as pd

def get_questions_and_answers(session: Session):
    # Usar yield_per para manejar grandes cantidades de datos
    faqs = session.query(FAQ).yield_per(1000)  
    # Convertir la lista de FAQ en un DataFrame de pandas
    df = pd.DataFrame([(faq.question, faq.answer) for faq in faqs], columns=['question', 'answer'])
    # Convertir el DataFrame de pandas en un DataFrame de dask
    ddf = dd.from_pandas(df, npartitions=1)
    return ddf

def fuzzy_match(user_input: str, session: Session):
    df = get_questions_and_answers(session)
    
    # Extraer las preguntas
    questions = df['question'].compute().tolist()
    
    # Encontrar la mejor coincidencia usando fuzzywuzzy
    best_match = process.extractOne(user_input, questions)

    if best_match and best_match[1] >= 70:  # Umbral de similitud del 70%
        answer = df[df['question'] == best_match[0]]['answer'].compute().values[0]
        return best_match[0], answer
    return None, None
