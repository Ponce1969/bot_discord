# Este script se encarga de crear las tablas de la base de datos y de insertar datos iniciales en la tabla FAQ.
# También valida los datos antes de insertarlos y muestra un mensaje de error si los datos son inválidos.
# Para ejecutar este script, debes tener la base de datos creada y configurada en el archivo .env.
import os
import pytz
from sqlalchemy import Column, Integer, String, DateTime, Date, create_engine, Index, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    thanks_count = Column(Integer, default=0)  # Nueva columna para contar "gracias"

class TatetiWinner(Base):
    __tablename__ = 'tateti_winners'
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    win_date = Column(DateTime, default=lambda: datetime.now(pytz.utc))

class FAQ(Base):
    __tablename__ = 'faq'
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    keyword = Column(String, nullable=False)  # Nueva columna para palabras clave

    # Crear un índice en la columna 'question' para mejorar la eficiencia de las búsquedas
    __table_args__ = (Index('ix_faq_question', 'question'),)

# Modelo para métricas por día y usuario
class LlamaMetrics(Base):
    __tablename__ = 'llama_metrics'
    date = Column(Date, primary_key=True)
    user_id = Column(String, primary_key=True)  # Discord user ID
    llama_uses = Column(Integer, default=0)
    tokens_used = Column(Integer, default=0)
    total_response_time = Column(Integer, default=0)  # en segundos
    responses_as_file = Column(Integer, default=0)
    api_failures = Column(Integer, default=0)

# Obtener la URL de la base de datos desde la variable de entorno
DATABASE_URL = os.getenv("DB_URI")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_today_metrics(db, user_id):
    today = datetime.now(pytz.timezone('America/Montevideo')).date()
    metrics = db.query(LlamaMetrics).filter_by(date=today, user_id=user_id).first()
    if not metrics:
        metrics = LlamaMetrics(date=today, user_id=user_id)
        db.add(metrics)
        db.commit()
        db.refresh(metrics)
    return metrics

def increment_llama_metric(user_id, field, amount=1):
    db = next(get_db())
    metrics = get_or_create_today_metrics(db, user_id)
    setattr(metrics, field, getattr(metrics, field) + amount)
    db.commit()
    db.close()

def add_response_time(user_id, seconds):
    db = next(get_db())
    metrics = get_or_create_today_metrics(db, user_id)
    metrics.total_response_time += int(seconds)
    db.commit()
    db.close()

def get_user_metrics(user_id):
    db = next(get_db())
    today = datetime.now(pytz.timezone('America/Montevideo')).date()
    metrics = db.query(LlamaMetrics).filter_by(date=today, user_id=user_id).first()
    db.close()
    return metrics

def get_global_metrics():
    db = next(get_db())
    today = datetime.now(pytz.timezone('America/Montevideo')).date()
    result = db.query(
        func.sum(LlamaMetrics.llama_uses),
        func.sum(LlamaMetrics.tokens_used),
        func.sum(LlamaMetrics.total_response_time),
        func.sum(LlamaMetrics.responses_as_file),
        func.sum(LlamaMetrics.api_failures)
    ).filter_by(date=today).first()
    db.close()
    return result

def init_db():
    # Crear todas las tablas si no existen
    Base.metadata.create_all(bind=engine)

# Inicializar la base de datos
init_db()

# Definir las preguntas, respuestas y palabras clave
faq_data = [
    {"question": "¿Qué puedes hacer?", "answer": ">ayuda y verás todo lo que puedo hacer en el chat por ti!!", "keyword": "hacer"},
    {"question": "¿Dónde puedo jugar?", "answer": "juega en el chat_juego_aventura !", "keyword": "jugar"},
    {"question": "¿Tenemos alguna IA ?", "answer": "Si en el chat tenemos a Gemini y LLama usa > y nombre de la IA!", "keyword": "IA"},
    {"question": "¿Que juegos hay?", "answer": "Tenemos tateti y aventura !", "keyword": "juegos"},
    {"question": "¿Que musica tenemos?", "answer": "Nos conectamos a la api de youtube y podemos ver videos en el chat!", "keyword": "musica"},
    {"question": "¿Que hacen en este chat general?", "answer": "Estudiamos Python y usamos sus librerias!", "keyword": "chat"},
    {"question": "¿Necesito ayuda?", "answer": "si quieres ayuda con algun codigo pegalo en el chat con carbon o CodeSnap!", "keyword": "ayuda"},
    # Agrega más preguntas, respuestas y palabras clave aquí
]

# Validar los datos antes de insertarlos
def validate_faq_data(faq):
    if not faq.get("question") or not faq.get("answer") or not faq.get("keyword"):
        return False
    return True

# Importar la función de normalización para máxima robustez
from acciones.oyente import normalize_text

# Insertar las preguntas y respuestas en la base de datos usando yield
def insert_faq_data():
    session = next(get_db())
    try:
        for faq in faq_data:
            if validate_faq_data(faq):
                # Normalizar la keyword antes de insertar
                keyword_norm = normalize_text(faq["keyword"])
                # Verificar si la pregunta ya existe en la base de datos
                existing_faq = session.query(FAQ).filter_by(question=faq["question"], answer=faq["answer"], keyword=keyword_norm).first()
                if not existing_faq:
                    faq_obj = FAQ(question=faq["question"], answer=faq["answer"], keyword=keyword_norm)
                    session.add(faq_obj)
        session.commit()
        print("Datos insertados correctamente en la tabla FAQ.")
    except Exception as e:
        session.rollback()
        print(f"Error al insertar datos en la tabla FAQ: {e}")
    finally:
        session.close()

# Ejecutar la función para insertar los datos
insert_faq_data()