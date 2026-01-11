# 🤖 Discord Bot - Python + Rust

Bot de Discord moderno con Python, métricas avanzadas en Rust, y AI integrada (DeepSeek, Groq/Llama).

## 🚀 Características

- **Discord.py 2.4+** - Framework moderno de Discord
- **AI Integrada** - DeepSeek y Groq/Llama para asistencia inteligente
- **Métricas del Sistema** - Componente Rust para monitoreo avanzado (OrangePi 5 Plus)
- **Base de Datos** - PostgreSQL con SQLAlchemy
- **Docker Ready** - Containerización completa con docker-compose
- **Gestión Moderna** - uv para dependencias ultra-rápidas

## 📦 Instalación

### Requisitos

- Python 3.10+
- PostgreSQL 16
- Docker (opcional)
- uv (gestor de paquetes)

### Setup Rápido

```bash
# 1. Instalar uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Clonar repositorio
git clone https://github.com/Ponce1969/bot_discord.git
cd bot_discord

# 3. Sincronizar dependencias
uv sync

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# IMPORTANTE: Para Docker, asegúrate de usar DATABASE_URL con hostname 'postgres'
# DATABASE_URL=postgresql://usuario:password@postgres:5432/discord

# 5. Ejecutar el bot
uv run python pythonbot.py
```

## 🐳 Docker

**Nota:** Docker usa el **mismo archivo `.env`** que desarrollo local. Asegúrate de configurar `DATABASE_URL` con el hostname correcto:
- **Desarrollo local:** `localhost:5432`
- **Docker/Producción:** `postgres:5432`

```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs del bot
docker-compose logs -f bot

# Detener servicios
docker-compose down
```

## 🎮 Comandos Principales

- `>ayuda` - Muestra todos los comandos disponibles
- `>info` - Métricas del sistema
- `>deepseek <pregunta>` - Chat con AI DeepSeek
- `>llama <pregunta>` - Asistente Python con Groq/Llama
- `>hola` - Saludo del bot
- `>tateti` - Juego de Ta-Te-Ti
- `>aventura` - Juego de aventura interactivo

## 🛠️ Desarrollo

### Workflow con uv

```bash
# Formatear código
uv run ruff format .

# Linting
uv run ruff check .

# Arreglar errores automáticamente
uv run ruff check --fix .

# Tests
uv run pytest
```

### Agregar Dependencias

```bash
# Dependencia de producción
uv add nombre-paquete

# Dependencia de desarrollo
uv add --dev nombre-paquete
```

## 📚 Documentación

Toda la documentación técnica está en la carpeta [`docs/`](./docs/):

- **[UV_WORKFLOW.md](./docs/UV_WORKFLOW.md)** - Guía completa de desarrollo con uv
- **[MIGRATION_STATUS.md](./docs/MIGRATION_STATUS.md)** - Estado de la migración a uv
- **[MODERNIZATION_2025.md](./docs/MODERNIZATION_2025.md)** - Plan de modernización
- **[SYSTEM_METRICS_DESIGN.md](./docs/SYSTEM_METRICS_DESIGN.md)** - Diseño del sistema de métricas

## 🏗️ Arquitectura

```
├── acciones/          # Lógica de negocio
├── cogs/              # Comandos de Discord
├── base/              # Database y configuración base
├── config/            # Archivos de configuración
├── system_monitor/    # Componente Rust para métricas
├── docs/              # Documentación técnica
└── pythonbot.py       # Entry point del bot
```

## 🔧 Stack Tecnológico

- **Python 3.10+** - Lenguaje principal
- **discord.py 2.4+** - API de Discord
- **uv** - Gestor de dependencias ultra-rápido
- **Rust** - Monitoreo de sistema de alto rendimiento
- **PostgreSQL** - Base de datos
- **Docker** - Containerización
- **Ruff** - Linting y formateo

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto.

## 👤 Autor

**Ponce1969**
- Email: gompatri@gmail.com
- GitHub: [@Ponce1969](https://github.com/Ponce1969)

---

**¡Hecho con ❤️ y Python!**
