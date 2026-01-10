#!/usr/bin/env python3
"""
Script de migración de Poetry a uv
Automatiza la transición completa al workflow moderno
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """Ejecutar comando y mostrar output"""
    print(f"🔄 Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(f"✅ Output: {result.stdout}")
    
    if result.stderr and check:
        print(f"❌ Error: {result.stderr}")
        if check:
            sys.exit(1)
    
    return result

def backup_current_setup():
    """Hacer backup de la configuración actual"""
    print("📦 Haciendo backup de configuración actual...")
    
    backup_files = [
        "pyproject.toml",
        "poetry.lock",
        "Dockerfile",
        "docker-compose.yml"
    ]
    
    backup_dir = Path("backup_poetry")
    backup_dir.mkdir(exist_ok=True)
    
    for file in backup_files:
        if Path(file).exists():
            shutil.copy2(file, backup_dir / file)
            print(f"✅ Backup: {file} -> {backup_dir}/{file}")

def install_uv():
    """Instalar uv si no está disponible"""
    print("🚀 Verificando instalación de uv...")
    
    result = run_command("uv --version", check=False)
    if result.returncode != 0:
        print("📥 Instalando uv...")
        if os.name == 'nt':  # Windows
            run_command("powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
        else:  # Linux/Mac
            run_command("curl -LsSf https://astral.sh/uv/install.sh | sh")
    else:
        print("✅ uv ya está instalado")

def migrate_dependencies():
    """Migrar de Poetry a uv"""
    print("🔄 Migrando configuración a uv...")
    
    # Reemplazar pyproject.toml
    if Path("pyproject.toml.new").exists():
        shutil.move("pyproject.toml.new", "pyproject.toml")
        print("✅ pyproject.toml actualizado para uv")
    
    # Inicializar proyecto uv
    print("🔧 Inicializando proyecto uv...")
    run_command("uv sync")
    
    print("✅ Dependencias sincronizadas con uv")

def update_docker_setup():
    """Actualizar configuración de Docker"""
    print("🐳 Actualizando configuración Docker...")
    
    # Reemplazar Dockerfile
    if Path("Dockerfile.uv").exists():
        shutil.move("Dockerfile.uv", "Dockerfile")
        print("✅ Dockerfile actualizado para uv")
    
    # Reemplazar docker-compose
    if Path("docker-compose.uv.yml").exists():
        shutil.move("docker-compose.uv.yml", "docker-compose.yml")
        print("✅ docker-compose.yml actualizado para uv")

def test_migration():
    """Probar que la migración funciona"""
    print("🧪 Probando migración...")
    
    # Probar que uv puede resolver dependencias
    result = run_command("uv sync --dry-run", check=False)
    if result.returncode == 0:
        print("✅ Resolución de dependencias OK")
    else:
        print("❌ Error en resolución de dependencias")
        return False
    
    # Probar formateo con uv (reemplaza black)
    result = run_command("uv fmt --check", check=False)
    if result.returncode == 0:
        print("✅ Formateo de código OK")
    else:
        print("⚠️ Código necesita formateo (normal en migración)")
    
    # Probar análisis con uv (reemplaza ruff + mypy)
    result = run_command("uv check --select F", check=False)  # Solo errores críticos
    if result.returncode == 0:
        print("✅ Análisis de código OK")
    else:
        print("⚠️ Hay issues de código (revisar después)")
    
    # Probar que el bot puede importarse
    result = run_command("uv run python -c 'import pythonbot; print(\"Bot importado correctamente\")'", check=False)
    if result.returncode == 0:
        print("✅ Bot se puede importar correctamente")
    else:
        print("❌ Error al importar el bot")
        return False
    
    return True

def cleanup_old_files():
    """Limpiar archivos de Poetry"""
    print("🧹 Limpiando archivos de Poetry...")
    
    files_to_remove = [
        "poetry.lock",
        ".venv"  # Si existe un venv de Poetry
    ]
    
    for file in files_to_remove:
        path = Path(file)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"🗑️ Eliminado: {file}")

def main():
    """Función principal de migración"""
    print("🚀 MIGRACIÓN DE POETRY A UV - WORKFLOW MODERNO")
    print("=" * 50)
    
    try:
        # Paso 1: Backup
        backup_current_setup()
        
        # Paso 2: Instalar uv
        install_uv()
        
        # Paso 3: Migrar dependencias
        migrate_dependencies()
        
        # Paso 4: Actualizar Docker
        update_docker_setup()
        
        # Paso 5: Probar migración
        if test_migration():
            print("\n🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
            print("📋 Próximos pasos con uv moderno:")
            print("   1. uv sync                    # Sincronizar dependencias")
            print("   2. uv fmt                     # Formatear código (reemplaza black)")
            print("   3. uv check                   # Analizar código (reemplaza ruff+mypy)")
            print("   4. uv run python pythonbot.py # Ejecutar bot")
            print("   5. docker-compose up --build  # Levantar con Docker + uv")
            print("\n💡 Comandos útiles:")
            print("   - uv add package-name        # Agregar dependencia")
            print("   - uv tree                    # Ver árbol de dependencias")
            print("   - uv fmt --check             # Ver si necesita formateo")
            print("   - uv check --fix             # Arreglar issues automáticamente")
            
            # Paso 6: Limpiar archivos antiguos (opcional)
            response = input("\n¿Quieres limpiar archivos de Poetry? (y/N): ")
            if response.lower() == 'y':
                cleanup_old_files()
        else:
            print("\n❌ Error en la migración. Revisa los logs arriba.")
            print("💡 Puedes restaurar desde backup_poetry/ si es necesario")
    
    except Exception as e:
        print(f"\n💥 Error durante la migración: {e}")
        print("💡 Puedes restaurar desde backup_poetry/ si es necesario")
        sys.exit(1)

if __name__ == "__main__":
    main()