# 🚀 Workflow Moderno con uv - Sin pip, 100% uv

## 🎯 Filosofía: Solo uv, nada más

**No usamos:**
- ❌ pip
- ❌ black (separado)
- ❌ ruff (separado) 
- ❌ mypy (separado)
- ❌ poetry
- ❌ pipenv
- ❌ virtualenv

**Solo usamos:**
- ✅ **uv** para TODO

## 📦 Gestión de Dependencias

### Instalar uv (una sola vez)
```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac  
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Comandos básicos del proyecto
```bash
# Sincronizar dependencias (equivale a npm install)
uv sync

# Agregar nueva dependencia
uv add discord.py

# Agregar dependencia de desarrollo
uv add --dev pytest

# Remover dependencia
uv remove package-name

# Actualizar todas las dependencias
uv sync --upgrade

# Ver dependencias instaladas
uv tree
```

## 🏃‍♂️ Ejecutar el Bot

### Desarrollo local
```bash
# Ejecutar directamente
uv run python pythonbot.py

# Ejecutar con variables de entorno
uv run --env-file .env python pythonbot.py

# Ejecutar script específico
uv run --script bot  # Usa project.scripts del pyproject.toml
```

### Con Docker (moderno)
```bash
# Build y run con uv
docker-compose up --build

# Solo el bot
docker-compose up bot-uv

# Ver logs del bot
docker-compose logs -f bot-uv
```

## 🔧 Herramientas de Desarrollo (Integradas en uv)

### Formateo de código (reemplaza black)
```bash
# Formatear todo el proyecto
uv fmt

# Formatear archivo específico
uv fmt pythonbot.py

# Ver qué cambiaría sin aplicar
uv fmt --check

# Formatear solo archivos modificados
uv fmt --diff
```

### Linting y análisis (reemplaza ruff + mypy)
```bash
# Analizar todo el proyecto
uv check

# Analizar archivo específico  
uv check pythonbot.py

# Solo errores, sin warnings
uv check --select E,F

# Arreglar automáticamente lo que se pueda
uv check --fix

# Type checking
uv check --type-check
```

### Testing
```bash
# Ejecutar tests
uv run pytest

# Tests con coverage
uv run pytest --cov

# Tests específicos
uv run pytest tests/test_bot.py

# Tests en modo watch
uv run pytest --watch
```

## 🐳 Docker Workflow Moderno

### Dockerfile optimizado
```dockerfile
# Usa la imagen oficial de uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# No crear virtual env (el contenedor ES el env)
ENV UV_SYSTEM_PYTHON=1

# Sync súper rápido
RUN uv sync --frozen

# Ejecutar con uv
CMD ["uv", "run", "python", "pythonbot.py"]
```

### Comandos Docker
```bash
# Build optimizado con cache de uv
docker-compose up --build

# Rebuild solo el bot
docker-compose up --build bot-uv

# Ejecutar comando dentro del contenedor
docker-compose exec bot-uv uv run python -c "print('Hello')"

# Ver dependencias en el contenedor
docker-compose exec bot-uv uv tree
```

## 🚀 Comandos de Desarrollo Diario

### Workflow típico
```bash
# 1. Sincronizar dependencias
uv sync

# 2. Formatear código
uv fmt

# 3. Analizar código
uv check

# 4. Ejecutar tests
uv run pytest

# 5. Ejecutar bot
uv run python pythonbot.py
```

### Un solo comando para todo
```bash
# Formatear, analizar y ejecutar
uv fmt && uv check && uv run python pythonbot.py
```

## 📊 Ventajas de uv vs Herramientas Separadas

| Tarea | Antes (separado) | Ahora (uv) | Velocidad |
|-------|------------------|------------|-----------|
| Instalar deps | `pip install -r requirements.txt` | `uv sync` | **10-100x más rápido** |
| Formatear | `black .` | `uv fmt` | **5x más rápido** |
| Linting | `ruff check .` | `uv check` | **3x más rápido** |
| Type check | `mypy .` | `uv check --type-check` | **2x más rápido** |
| Ejecutar | `python pythonbot.py` | `uv run python pythonbot.py` | **Mismo** |

## 🔄 Migración desde Poetry

### Automática (recomendado)
```bash
# Usar nuestro script
uv run python migrate_to_uv.py
```

### Manual
```bash
# 1. Backup
cp pyproject.toml pyproject.toml.backup

# 2. Reemplazar configuración
cp pyproject.toml.new pyproject.toml

# 3. Sincronizar
uv sync

# 4. Probar
uv run python pythonbot.py
```

## 🎯 Comandos Específicos del Bot

### Desarrollo
```bash
# Ejecutar bot en modo desarrollo
uv run --env-file .env python pythonbot.py

# Ejecutar con debug
uv run python -m pdb pythonbot.py

# Probar comando específico
uv run python -c "from cogs.comando_info import Info; print('OK')"
```

### Producción
```bash
# Docker con uv (recomendado)
docker-compose -f docker-compose.yml up -d

# Directo con uv
uv run --env-file .env.prod python pythonbot.py
```

### Métricas y monitoreo
```bash
# Cuando implementemos el componente Rust
uv run python -c "import subprocess; print(subprocess.run(['./system_monitor'], capture_output=True, text=True).stdout)"
```

## 💡 Tips y Trucos

### Performance
```bash
# Cache global de uv (persiste entre proyectos)
export UV_CACHE_DIR=/path/to/global/cache

# Usar compilación paralela
export UV_CONCURRENT_DOWNLOADS=10
```

### Debugging
```bash
# Ver qué hace uv internamente
uv --verbose sync

# Ver resolución de dependencias
uv tree --depth 2

# Verificar configuración
uv config list
```

### CI/CD
```bash
# En GitHub Actions, usar uv oficial
- uses: astral-sh/setup-uv@v1
- run: uv sync
- run: uv check
- run: uv run pytest
```

---

**🎉 ¡Workflow 100% moderno con uv!** 
Sin pip, sin herramientas separadas, solo uv para todo.