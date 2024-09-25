# aqui desarollamos el codigo de listener y fuzzywuzzy para obtener la respuesta mas adecuadafrom fuzzywuzzy import process
from fuzzywuzzy import process
from sqlalchemy.orm import Session
from base.database import get_db, FAQ

def get_questions_and_answers(session: Session):
    faqs = session.query(FAQ).all()
    return [(faq.question, faq.answer) for faq in faqs]

def fuzzy_match(user_input: str, session: Session):
    questions_and_answers = get_questions_and_answers(session)
    questions = [q[0] for q in questions_and_answers]
    best_match = process.extractOne(user_input, questions)
    if best_match and best_match[1] >= 70:  # 70% similarity threshold
        return best_match[0], questions_and_answers[questions.index(best_match[0])][1]
    return None, None 