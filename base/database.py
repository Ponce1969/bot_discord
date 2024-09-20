import os
from sqlalchemy import Column, Integer, String, DateTime, create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
from datetime import datetime

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
    win_date = Column(DateTime, default=datetime.utcnow)

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

def init_db():
    # Crear todas las tablas si no existen
    Base.metadata.create_all(bind=engine)

# Inicializar la base de datos
init_db()
