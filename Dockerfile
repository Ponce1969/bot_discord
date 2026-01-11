FROM python:3.10-slim-bookworm

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv - La forma más rápida y moderna
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Configurar directorio de trabajo
WORKDIR /app

# Configurar uv para no crear virtual env (usamos el contenedor como env)
ENV UV_SYSTEM_PYTHON=1

# Copiar archivos de configuración del proyecto
COPY pyproject.toml uv.lock ./

# Sincronizar dependencias con uv (súper rápido)
RUN uv sync --frozen

# Copiar el código de la aplicación
COPY . .

# Exponer puerto (si es necesario)
EXPOSE 8000

# Comando para ejecutar el bot usando uv
CMD ["uv", "run", "python", "pythonbot.py"]
