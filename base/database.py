# Este script se encarga de crear las tablas de la base de datos y de insertar datos iniciales en la tabla FAQ.
# También valida los datos antes de insertarlos y muestra un mensaje de error si los datos son inválidos.
# Para ejecutar este script, debes tener la base de datos creada y configurada en el archivo .env.
import os
from datetime import datetime, timedelta

import pytz
from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    create_engine,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    thanks_count = Column(Integer, default=0)  # Nueva columna para contar "gracias"


class TatetiWinner(Base):
    __tablename__ = "tateti_winners"
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    win_date = Column(DateTime, default=lambda: datetime.now(pytz.utc))


class FAQ(Base):
    __tablename__ = "faq"
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    keyword = Column(String, nullable=False)  # Nueva columna para palabras clave

    # Crear un índice en la columna 'question' para mejorar la eficiencia de las búsquedas
    __table_args__ = (Index("ix_faq_question", "question"),)


# Modelo para métricas por día y usuario
class LlamaMetrics(Base):
    __tablename__ = "llama_metrics"
    date = Column(Date, primary_key=True)
    user_id = Column(String, primary_key=True)  # Discord user ID
    llama_uses = Column(Integer, default=0)
    tokens_used = Column(Integer, default=0)
    total_response_time = Column(Integer, default=0)  # en segundos
    responses_as_file = Column(Integer, default=0)
    api_failures = Column(Integer, default=0)


# Modelo para sesiones de chat de Gemini
class GeminiChatSession(Base):
    __tablename__ = "gemini_chat_sessions"
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    last_updated = Column(
        DateTime,
        default=lambda: datetime.now(pytz.utc),
        onupdate=lambda: datetime.now(pytz.utc),
    )
    is_active = Column(Boolean, default=True)

    # Relación con los mensajes de la sesión
    messages = relationship(
        "GeminiChatMessage", back_populates="session", cascade="all, delete-orphan"
    )


# Modelo para mensajes individuales en sesiones de chat
class GeminiChatMessage(Base):
    __tablename__ = "gemini_chat_messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("gemini_chat_sessions.id"), nullable=False)
    role = Column(String, nullable=False)  # 'user' o 'model'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(pytz.utc))

    # Relación con la sesión
    session = relationship("GeminiChatSession", back_populates="messages")


# Modelo para historial de chat de Gemini
class GeminiChatHistory(Base):
    __tablename__ = "gemini_chat_history"
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(String, nullable=False, index=True)
    chat_session_id = Column(
        Integer, ForeignKey("gemini_chat_sessions.id"), nullable=False
    )
    message_id = Column(Integer, ForeignKey("gemini_chat_messages.id"), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(pytz.utc))

    # Relación con la sesión de chat
    chat_session = relationship("GeminiChatSession", backref="chat_history")

    # Relación con el mensaje de chat
    chat_message = relationship("GeminiChatMessage", backref="chat_history")


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
    today = datetime.now(pytz.timezone("America/Montevideo")).date()
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
    today = datetime.now(pytz.timezone("America/Montevideo")).date()
    metrics = db.query(LlamaMetrics).filter_by(date=today, user_id=user_id).first()
    db.close()
    return metrics


def get_global_metrics():
    db = next(get_db())
    today = datetime.now(pytz.timezone("America/Montevideo")).date()
    result = (
        db.query(
            func.sum(LlamaMetrics.llama_uses),
            func.sum(LlamaMetrics.tokens_used),
            func.sum(LlamaMetrics.total_response_time),
            func.sum(LlamaMetrics.responses_as_file),
            func.sum(LlamaMetrics.api_failures),
        )
        .filter_by(date=today)
        .first()
    )
    db.close()
    return result


# Funciones para manejar sesiones de chat de Gemini
def get_or_create_gemini_session(discord_user_id):
    """
    Obtiene la sesión de chat activa de Gemini para un usuario o crea una nueva si no existe.

    Args:
        discord_user_id (str): ID del usuario de Discord

    Returns:
        GeminiChatSession: Sesión de chat de Gemini
    """
    db = next(get_db())

    try:
        # Buscar una sesión activa existente
        session = (
            db.query(GeminiChatSession)
            .filter_by(discord_user_id=str(discord_user_id), is_active=True)
            .first()
        )

        # Si no existe, crear una nueva
        if not session:
            session = GeminiChatSession(discord_user_id=str(discord_user_id))
            db.add(session)
            db.commit()
            db.refresh(session)

        return session
    finally:
        db.close()


def add_message_to_session(session_id, role, content):
    """
    Añade un mensaje a una sesión de chat de Gemini.

    Args:
        session_id (int): ID de la sesión de chat
        role (str): Rol del mensaje ('user' o 'model')
        content (str): Contenido del mensaje

    Returns:
        GeminiChatMessage: Mensaje añadido
    """
    db = next(get_db())

    try:
        # Actualizar timestamp de la sesión
        session = db.query(GeminiChatSession).filter_by(id=session_id).first()
        if not session:
            return None

        session.last_updated = datetime.now(pytz.utc)

        # Añadir el mensaje
        message = GeminiChatMessage(session_id=session_id, role=role, content=content)

        db.add(message)
        db.commit()
        db.refresh(message)

        return message
    finally:
        db.close()


def get_session_messages(session_id, limit=20):
    """
    Obtiene los últimos mensajes de una sesión de chat de Gemini.

    Args:
        session_id (int): ID de la sesión de chat
        limit (int): Número máximo de mensajes a obtener

    Returns:
        list: Lista de mensajes
    """
    db = next(get_db())

    try:
        messages = (
            db.query(GeminiChatMessage)
            .filter_by(session_id=session_id)
            .order_by(GeminiChatMessage.timestamp)
            .limit(limit)
            .all()
        )

        return messages
    finally:
        db.close()


def reset_gemini_session(discord_user_id):
    """
    Desactiva todas las sesiones anteriores y crea una nueva para el usuario.

    Args:
        discord_user_id (str): ID del usuario de Discord

    Returns:
        GeminiChatSession: Nueva sesión de chat
    """
    db = next(get_db())

    try:
        # Desactivar todas las sesiones existentes
        db.query(GeminiChatSession).filter_by(
            discord_user_id=str(discord_user_id)
        ).update({GeminiChatSession.is_active: False})

        # Crear nueva sesión
        new_session = GeminiChatSession(discord_user_id=str(discord_user_id))
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        return new_session
    finally:
        db.close()


def prune_old_sessions(days_inactive=30):
    """
    Marca como inactivas las sesiones que no han sido actualizadas en un tiempo determinado.

    Args:
        days_inactive (int): Número de días de inactividad para marcar como inactiva
    """
    db = next(get_db())

    try:
        cutoff_date = datetime.now(pytz.utc) - timedelta(days=days_inactive)

        db.query(GeminiChatSession).filter(
            GeminiChatSession.last_updated < cutoff_date, GeminiChatSession.is_active
        ).update({GeminiChatSession.is_active: False})

        db.commit()
    finally:
        db.close()


def init_db():
    # Crear todas las tablas si no existen
    Base.metadata.create_all(bind=engine)


# Inicializar la base de datos
init_db()

# Definir las preguntas, respuestas y palabras clave
faq_data = [
    {
        "question": "¿Qué puedes hacer?",
        "answer": ">ayuda y verás todo lo que puedo hacer en el chat por ti!!",
        "keyword": "hacer",
    },
    {
        "question": "¿Dónde puedo jugar?",
        "answer": "juega en el chat_juego_aventura !",
        "keyword": "jugar",
    },
    {
        "question": "¿Tenemos alguna IA ?",
        "answer": "Si en el chat tenemos a DeepSeek y LLama usa > y nombre de la IA!",
        "keyword": "IA",
    },
    {
        "question": "¿Que juegos hay?",
        "answer": "Tenemos tateti y aventura !",
        "keyword": "juegos",
    },
    {
        "question": "¿Que musica tenemos?",
        "answer": "Nos conectamos a la api de youtube y podemos ver videos en el chat!",
        "keyword": "musica",
    },
    {
        "question": "¿Que hacen en este chat general?",
        "answer": "Estudiamos Python y usamos sus librerias!",
        "keyword": "chat",
    },
    {
        "question": "¿Necesito ayuda?",
        "answer": "si quieres ayuda con algun codigo pegalo en el chat con carbon o CodeSnap!",
        "keyword": "ayuda",
    },
    # Agrega más preguntas, respuestas y palabras clave aquí
]


# Validar los datos antes de insertarlos
def validate_faq_data(faq):
    if not faq.get("question") or not faq.get("answer") or not faq.get("keyword"):
        return False
    return True


# Insertar las preguntas y respuestas en la base de datos usando yield
def insert_faq_data():
    from acciones.oyente import (
        normalize_text,  # Import local para evitar circular import
    )

    session = next(get_db())
    try:
        for faq in faq_data:
            if validate_faq_data(faq):
                # Normalizar la keyword antes de insertar
                keyword_norm = normalize_text(faq["keyword"])
                # Verificar si la pregunta ya existe en la base de datos
                existing_faq = (
                    session.query(FAQ)
                    .filter_by(
                        question=faq["question"],
                        answer=faq["answer"],
                        keyword=keyword_norm,
                    )
                    .first()
                )
                if not existing_faq:
                    faq_obj = FAQ(
                        question=faq["question"],
                        answer=faq["answer"],
                        keyword=keyword_norm,
                    )
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
