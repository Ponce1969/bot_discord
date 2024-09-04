import os
from sqlalchemy import Column, Integer, String, create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    thanks_count = Column(Integer, default=0)  # Nueva columna para contar "gracias"

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
    
    # Verificar si la columna 'thanks_count' existe y añadirla si no existe
    with engine.connect() as connection:
        inspector = inspect(engine)
        columns = [column['name'] for column in inspector.get_columns('users')]
        if 'thanks_count' not in columns:
            try:
                connection.execute(text('ALTER TABLE users ADD COLUMN thanks_count INTEGER DEFAULT 0'))
                print("Columna 'thanks_count' añadida a la tabla 'users'.")
            except ProgrammingError as e:
                print(f"Error al añadir la columna 'thanks_count': {e}")

# Inicializar la base de datos
init_db()
