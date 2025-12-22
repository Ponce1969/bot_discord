FROM python:3.10-slim-buster

WORKDIR /app

# Instalar Poetry
RUN pip install poetry

# Copiar pyproject.toml y poetry.lock para instalar dependencias
COPY pyproject.toml poetry.lock* ./

# Instalar dependencias con Poetry
RUN poetry config virtualenvs.create false && poetry lock && poetry install --no-root

# Copiar el resto del código de la aplicación
COPY . .

# Comando para ejecutar el bot
CMD ["python", "/app/pythonbot.py"]
