#!/usr/bin/env python3
"""
Script para compilar el componente Rust del sistema de métricas
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Ejecutar comando y mostrar output"""
    print(f"🔄 Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

    if result.stdout:
        print(f"✅ Output: {result.stdout}")

    if result.stderr:
        print(f"⚠️ Stderr: {result.stderr}")

    return result.returncode == 0


def check_rust_installation():
    """Verificar que Rust esté instalado"""
    print("🦀 Verificando instalación de Rust...")

    if not run_command(["rustc", "--version"]):
        print("❌ Rust no está instalado")
        print("💡 Instala Rust desde: https://rustup.rs/")
        return False

    if not run_command(["cargo", "--version"]):
        print("❌ Cargo no está disponible")
        return False

    print("✅ Rust está instalado correctamente")
    return True


def build_rust_component():
    """Compilar el componente Rust"""
    print("🔨 Compilando componente Rust...")

    rust_dir = Path("system_monitor")
    if not rust_dir.exists():
        print("❌ Directorio system_monitor no encontrado")
        return False

    # Build en modo release para máximo rendimiento
    if not run_command(["cargo", "build", "--release"], cwd=rust_dir):
        print("❌ Error compilando el componente Rust")
        return False

    # Verificar que el binary se creó
    binary_path = rust_dir / "target" / "release" / "system_monitor"
    if os.name == "nt":  # Windows
        binary_path = binary_path.with_suffix(".exe")

    if not binary_path.exists():
        print(f"❌ Binary no encontrado en {binary_path}")
        return False

    print(f"✅ Binary compilado exitosamente: {binary_path}")
    return True


def test_rust_component():
    """Probar el componente Rust"""
    print("🧪 Probando componente Rust...")

    binary_path = Path("system_monitor/target/release/system_monitor")
    if os.name == "nt":  # Windows
        binary_path = binary_path.with_suffix(".exe")

    if not binary_path.exists():
        print("❌ Binary no encontrado para testing")
        return False

    # Probar ejecución básica
    if not run_command([str(binary_path), "--help"]):
        print("❌ Error ejecutando el binary")
        return False

    print("✅ Componente Rust funciona correctamente")
    return True


def setup_permissions():
    """Configurar permisos del binary (Linux/Mac)"""
    if os.name != "nt":  # No Windows
        binary_path = Path("system_monitor/target/release/system_monitor")
        if binary_path.exists():
            os.chmod(binary_path, 0o755)
            print("✅ Permisos configurados")


def main():
    """Función principal"""
    print("🚀 BUILD COMPONENTE RUST - SISTEMA DE MÉTRICAS")
    print("=" * 50)

    try:
        # Verificar Rust
        if not check_rust_installation():
            sys.exit(1)

        # Compilar
        if not build_rust_component():
            sys.exit(1)

        # Configurar permisos
        setup_permissions()

        # Probar
        if not test_rust_component():
            sys.exit(1)

        print("\n🎉 ¡COMPONENTE RUST COMPILADO EXITOSAMENTE!")
        print("📋 Próximos pasos:")
        print("   1. uv run python pythonbot.py  # Ejecutar bot con métricas Rust")
        print("   2. >info  # Probar comando con métricas avanzadas")
        print("   3. >info_json  # Ver métricas en formato JSON")

        # Mostrar ubicación del binary
        binary_path = Path("system_monitor/target/release/system_monitor")
        if os.name == "nt":
            binary_path = binary_path.with_suffix(".exe")

        print(f"\n📍 Binary ubicado en: {binary_path.absolute()}")

    except KeyboardInterrupt:
        print("\n⚠️ Build cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error durante el build: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
