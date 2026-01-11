# Dockerfile moderno con uv - Sin pip, 100% uv workflow
FROM python:3.10-slim-bookworm

# Instalar dependencias del sistema necesarias (incluyendo Rust)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Rust para compilar el system_monitor
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

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

# Compilar el componente Rust system_monitor
WORKDIR /app/system_monitor
RUN cargo build --release && \
    cp target/release/deps/system_monitor-* target/release/system_monitor 2>/dev/null || \
    find target/release/deps/ -maxdepth 1 -type f -executable -name "system_monitor-*" -exec cp {} target/release/system_monitor \;

# Volver al directorio principal
WORKDIR /app

# Exponer puerto (si es necesario)
EXPOSE 8000

# Comando para ejecutar el bot usando uv
CMD ["uv", "run", "python", "pythonbot.py"]