"""
Integración Python ↔ Rust para métricas del sistema
Reemplaza el sistema básico de info.py con métricas avanzadas
"""

import asyncio
import json
from datetime import datetime
from typing import Any

import discord
from pytz import timezone


class SystemMetricsRust:
    """Interfaz Python para el monitor Rust"""

    def __init__(self, rust_binary_path: str = "./system_monitor/target/release/system_monitor"):
        self.rust_binary_path = rust_binary_path
        self.cache_duration = 30  # segundos
        self._last_metrics = None
        self._last_update = None

    async def get_metrics(self, detailed: bool = True, processes: bool = False) -> dict[str, Any] | None:
        """Obtener métricas del sistema usando el binary Rust"""

        # Cache simple para evitar llamadas muy frecuentes
        now = datetime.now()
        if (self._last_metrics and self._last_update and
            (now - self._last_update).seconds < self.cache_duration):
            return self._last_metrics

        try:
            # Construir comando
            cmd = [self.rust_binary_path, "--format", "json"]
            if detailed:
                cmd.append("--detailed-cpu")
            if processes:
                cmd.extend(["--processes", "--top-processes", "5"])

            # Ejecutar binary Rust
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                metrics = json.loads(stdout.decode())
                self._last_metrics = metrics
                self._last_update = now
                return metrics
            else:
                print(f"Error ejecutando Rust binary: {stderr.decode()}")
                return None

        except Exception as e:
            print(f"Error en get_metrics: {e}")
            return None

    def get_color_for_percentage(self, percentage: float) -> str:
        """Obtener emoji de color según porcentaje"""
        if percentage < 50:
            return "🟢"  # Verde
        elif percentage < 75:
            return "🟡"  # Amarillo
        elif percentage < 90:
            return "🟠"  # Naranja
        else:
            return "🔴"  # Rojo

    def get_temperature_color(self, temp: float) -> str:
        """Color específico para temperatura"""
        if temp < 50:
            return "🟦"  # Azul frío
        elif temp < 65:
            return "🟢"  # Verde normal
        elif temp < 75:
            return "🟡"  # Amarillo tibio
        elif temp < 85:
            return "🟠"  # Naranja caliente
        else:
            return "🔴"  # Rojo crítico

    def format_bytes(self, bytes_value: int) -> str:
        """Formatear bytes a unidades legibles"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"

    def format_uptime(self, uptime_seconds: int) -> str:
        """Formatear uptime a formato legible"""
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60

        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    def create_progress_bar(self, percentage: float, length: int = 10) -> str:
        """Crear barra de progreso ASCII"""
        filled = int(percentage / 100 * length)
        empty = length - filled
        return f"{'█' * filled}{'░' * empty}"

    async def create_advanced_embed(self, guild_name: str = "OrangePi 5 Plus") -> discord.Embed | None:
        """Crear embed avanzado con métricas completas"""

        metrics = await self.get_metrics(detailed=True, processes=True)
        if not metrics:
            return await self.create_fallback_embed()

        # Timestamp
        uruguay_time = datetime.now(timezone('America/Montevideo'))

        # Color del embed basado en alertas
        embed_color = discord.Color.green()
        if metrics.get('alerts'):
            critical_alerts = [a for a in metrics['alerts'] if a['level'] == 'Critical']
            warning_alerts = [a for a in metrics['alerts'] if a['level'] == 'Warning']

            if critical_alerts:
                embed_color = discord.Color.red()
            elif warning_alerts:
                embed_color = discord.Color.orange()

        embed = discord.Embed(
            title=f"🖥️ {guild_name} - Sistema Avanzado",
            description="Métricas en tiempo real del servidor",
            color=embed_color,
            timestamp=uruguay_time
        )

        # CPU Section
        cpu = metrics['cpu']
        cpu_color = self.get_color_for_percentage(cpu['usage_percent'])
        temp_color = self.get_temperature_color(cpu.get('temperature', 0))

        cpu_info = f"""
        **Uso:** {cpu_color} {cpu['usage_percent']:.1f}%
        **Temperatura:** {temp_color} {cpu.get('temperature', 'N/A')}°C
        **Frecuencia:** {cpu.get('frequency', 'N/A')} MHz
        **Load Avg:** {cpu['load_average'][0]:.2f} {cpu['load_average'][1]:.2f} {cpu['load_average'][2]:.2f}

        {self.create_progress_bar(cpu['usage_percent'])}
        """

        embed.add_field(
            name=f"🔥 CPU RK3588S ({metrics['system']['cpu_count']} cores)",
            value=cpu_info.strip(),
            inline=True
        )

        # Memory Section
        memory = metrics['memory']
        mem_color = self.get_color_for_percentage(memory['percentage'])

        memory_info = f"""
        **RAM:** {mem_color} {self.format_bytes(memory['used'])} / {self.format_bytes(memory['total'])}
        **Disponible:** {self.format_bytes(memory['available'])}
        **Swap:** {self.format_bytes(memory['swap_used'])} / {self.format_bytes(memory['swap_total'])}
        **Cache:** {self.format_bytes(memory.get('cached', 0))}

        {self.create_progress_bar(memory['percentage'])}
        """

        embed.add_field(
            name=f"🧠 Memoria ({memory['percentage']:.1f}%)",
            value=memory_info.strip(),
            inline=True
        )

        # Storage Section
        storage_info = ""
        for disk in metrics['storage'][:2]:  # Mostrar solo los primeros 2 discos
            disk_color = self.get_color_for_percentage(disk['percentage'])
            storage_info += f"""
            **{disk['mount_point']}** {disk_color} {disk['percentage']:.1f}%
            {self.format_bytes(disk['used'])} / {self.format_bytes(disk['total'])}
            {self.create_progress_bar(disk['percentage'], 8)}
            """

        embed.add_field(
            name="💾 Almacenamiento",
            value=storage_info.strip(),
            inline=False
        )

        # Network Section
        network = metrics['network']
        network_info = f"""
        **Total Subida:** ↗️ {self.format_bytes(network['total_bytes_sent'])}
        **Total Bajada:** ↙️ {self.format_bytes(network['total_bytes_received'])}
        **Interfaces:** {len(network['interfaces'])}
        """

        embed.add_field(
            name="🌐 Red",
            value=network_info.strip(),
            inline=True
        )

        # System Info
        system_info = f"""
        **Uptime:** {self.format_uptime(metrics['uptime'])}
        **OS:** {metrics['system']['os_name']} {metrics['system']['os_version']}
        **Kernel:** {metrics['system']['kernel_version']}
        **Arch:** {metrics['system']['architecture']}
        """

        embed.add_field(
            name="⚙️ Sistema",
            value=system_info.strip(),
            inline=True
        )

        # Top Processes (si están disponibles)
        if metrics.get('processes'):
            process_info = ""
            for proc in metrics['processes'][:3]:  # Top 3
                process_info += f"**{proc['name']}** CPU: {proc['cpu_usage']:.1f}% RAM: {proc['memory_percentage']:.1f}%\n"

            embed.add_field(
                name="🔝 Procesos Top",
                value=process_info.strip(),
                inline=False
            )

        # Alerts Section
        if metrics.get('alerts'):
            alerts_text = ""
            for alert in metrics['alerts'][:3]:  # Mostrar solo las primeras 3
                emoji = "🚨" if alert['level'] == 'Critical' else "⚠️"
                alerts_text += f"{emoji} {alert['message']}\n"

            embed.add_field(
                name="🚨 Alertas",
                value=alerts_text.strip(),
                inline=False
            )

        # Footer
        embed.set_footer(
            text=f"🦀 Rust Monitor • Actualizado cada {self.cache_duration}s • Próxima: {(uruguay_time.replace(second=0, microsecond=0) + timezone('America/Montevideo').localize(datetime.now()).utcoffset()).strftime('%H:%M:%S')}",
        )

        return embed

    async def create_fallback_embed(self) -> discord.Embed:
        """Embed de fallback si Rust falla"""
        uruguay_time = datetime.now(timezone('America/Montevideo'))

        embed = discord.Embed(
            title="🖥️ Sistema - Modo Fallback",
            description="Error accediendo al monitor Rust, usando métricas básicas",
            color=discord.Color.yellow(),
            timestamp=uruguay_time
        )

        # Intentar leer temperatura básica
        try:
            with open('/sys/class/thermal/thermal_zone0/temp') as temp_file:
                cpu_temp = int(temp_file.read()) / 1000
            embed.add_field(
                name="🌡️ Temperatura CPU",
                value=f"{cpu_temp}°C",
                inline=True
            )
        except Exception:
            embed.add_field(
                name="❌ Error",
                value="No se pueden leer métricas del sistema",
                inline=True
            )

        embed.set_footer(text="💡 Instala el componente Rust para métricas avanzadas")

        return embed

# Instancia global
system_metrics = SystemMetricsRust()

async def create_advanced_info_embed(guild_name: str = "OrangePi 5 Plus") -> discord.Embed:
    """Función principal para crear embed avanzado"""
    return await system_metrics.create_advanced_embed(guild_name)

async def get_system_metrics_json() -> dict[str, Any] | None:
    """Obtener métricas en formato JSON para otros usos"""
    return await system_metrics.get_metrics()
