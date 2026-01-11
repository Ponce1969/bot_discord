# 📊 Sistema de Métricas Avanzado - OrangePi 5 Plus

## 🎯 Objetivo

Crear un sistema de monitoreo completo para tu OrangePi 5 Plus que muestre métricas en tiempo real con colores dinámicos y alertas inteligentes.

## 🖥️ Hardware OrangePi 5 Plus - Especificaciones

### CPU: Rockchip RK3588S
- **8 núcleos**: 4x Cortex-A76 (2.4GHz) + 4x Cortex-A55 (1.8GHz)
- **Arquitectura**: ARM64
- **Thermal zones**: `/sys/class/thermal/thermal_zone0` (CPU)

### Memoria
- **RAM**: Hasta 32GB LPDDR5-4800
- **Storage**: eMMC 5.1 + NVMe M.2 2280

### GPU
- **Mali-G610 MP4** (OpenGL ES 3.2, Vulkan 1.2)

## 🎨 Sistema de Colores Dinámicos

### 🌡️ Temperatura CPU
```python
@property
def cpu_temp_color(self) -> str:
    """Colores basados en thermal throttling del RK3588S"""
    if self.cpu_temp < 50:
        return "🟦"  # Azul: Frío (< 50°C)
    elif self.cpu_temp < 65:
        return "🟢"  # Verde: Normal (50-65°C)
    elif self.cpu_temp < 75:
        return "🟡"  # Amarillo: Tibio (65-75°C)
    elif self.cpu_temp < 85:
        return "🟠"  # Naranja: Caliente (75-85°C)
    else:
        return "🔴"  # Rojo: Crítico (>85°C)

@property
def cpu_temp_status(self) -> str:
    if self.cpu_temp < 50:
        return "❄️ FRÍO"
    elif self.cpu_temp < 65:
        return "✅ NORMAL"
    elif self.cpu_temp < 75:
        return "⚠️ TIBIO"
    elif self.cpu_temp < 85:
        return "🔥 CALIENTE"
    else:
        return "🚨 CRÍTICO"
```

### 📊 CPU Usage (8 cores)
```python
@property
def cpu_usage_color(self) -> str:
    """Colores para uso de CPU considerando 8 núcleos"""
    if self.cpu_usage < 25:
        return "🟢"  # Verde: Bajo uso
    elif self.cpu_usage < 50:
        return "🟡"  # Amarillo: Uso moderado
    elif self.cpu_usage < 75:
        return "🟠"  # Naranja: Uso alto
    else:
        return "🔴"  # Rojo: Uso crítico

@property
def cpu_load_bar(self) -> str:
    """Barra visual de carga CPU"""
    filled = int(self.cpu_usage / 10)
    empty = 10 - filled
    return f"{'█' * filled}{'░' * empty}"
```

### 🧠 Memoria RAM (hasta 32GB)
```python
@property
def memory_color(self) -> str:
    """Colores para uso de memoria"""
    if self.memory_percentage < 60:
        return "🟢"  # Verde: Disponible
    elif self.memory_percentage < 80:
        return "🟡"  # Amarillo: Moderado
    elif self.memory_percentage < 95:
        return "🟠"  # Naranja: Alto
    else:
        return "🔴"  # Rojo: Crítico

@property
def memory_bar(self) -> str:
    """Barra visual de memoria"""
    filled = int(self.memory_percentage / 10)
    empty = 10 - filled
    return f"{'█' * filled}{'░' * empty}"

@property
def memory_status(self) -> str:
    used_gb = self.memory_used / (1024**3)
    total_gb = self.memory_total / (1024**3)
    return f"{used_gb:.1f}GB / {total_gb:.1f}GB ({self.memory_percentage:.1f}%)"
```

### 💾 Almacenamiento
```python
@property
def storage_color(self) -> str:
    """Colores para uso de disco"""
    if self.disk_percentage < 70:
        return "🟢"  # Verde: Espacio disponible
    elif self.disk_percentage < 85:
        return "🟡"  # Amarillo: Cuidado
    elif self.disk_percentage < 95:
        return "🟠"  # Naranja: Poco espacio
    else:
        return "🔴"  # Rojo: Espacio crítico

@property
def storage_bar(self) -> str:
    filled = int(self.disk_percentage / 10)
    empty = 10 - filled
    return f"{'█' * filled}{'░' * empty}"
```

### 🌐 Red y I/O
```python
@property
def network_status_color(self) -> str:
    """Color basado en velocidad de red"""
    if self.network_speed > 100:  # MB/s
        return "🟢"  # Verde: Alta velocidad
    elif self.network_speed > 10:
        return "🟡"  # Amarillo: Velocidad media
    else:
        return "🟠"  # Naranja: Velocidad baja
```

## 📋 Métricas a Implementar

### 🔥 Térmicas
- [x] **CPU Temperature** - `/sys/class/thermal/thermal_zone0/temp`
- [ ] **GPU Temperature** - `/sys/class/thermal/thermal_zone1/temp` (si disponible)
- [ ] **Board Temperature** - Sensores adicionales

### ⚡ CPU Performance
- [ ] **CPU Usage Total** - `/proc/stat`
- [ ] **CPU Usage per Core** - 8 núcleos individuales
- [ ] **CPU Frequency** - `/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq`
- [ ] **Load Average** - `/proc/loadavg` (1m, 5m, 15m)
- [ ] **Context Switches** - `/proc/stat`

### 🧠 Memoria
- [ ] **RAM Usage** - `/proc/meminfo`
- [ ] **Swap Usage** - `/proc/meminfo`
- [ ] **Memory Buffers/Cache** - Detalles avanzados
- [ ] **Available Memory** - Memoria realmente disponible

### 💾 Almacenamiento
- [ ] **Disk Usage** - `df -h`
- [ ] **Disk I/O** - `/proc/diskstats`
- [ ] **Read/Write Speed** - Velocidades actuales
- [ ] **IOPS** - Operaciones por segundo

### 🌐 Red
- [ ] **Network I/O** - `/proc/net/dev`
- [ ] **Bandwidth Usage** - Upload/Download actual
- [ ] **Network Connections** - Conexiones activas
- [ ] **Ping Latency** - A gateway/DNS

### 🎮 GPU (Mali-G610)
- [ ] **GPU Usage** - Si es accesible via sysfs
- [ ] **GPU Memory** - VRAM usage
- [ ] **GPU Frequency** - Clock actual

### 🔋 Sistema
- [ ] **Uptime** - `/proc/uptime`
- [ ] **Boot Time** - Tiempo desde último reinicio
- [ ] **Process Count** - Procesos activos
- [ ] **Users Logged** - Usuarios conectados

## 🎨 Diseño del Embed

```python
async def create_advanced_system_embed(metrics: SystemMetrics) -> discord.Embed:
    """Crear embed rico con todas las métricas"""
    
    embed = discord.Embed(
        title="🖥️ OrangePi 5 Plus - Estado del Sistema",
        description="Métricas en tiempo real del servidor",
        color=discord.Color.blue(),
        timestamp=datetime.now(timezone('America/Montevideo'))
    )
    
    # CPU Section
    embed.add_field(
        name=f"🔥 CPU {metrics.cpu_temp_color} {metrics.cpu_temp_status}",
        value=f"""
        **Temperatura:** {metrics.cpu_temp}°C
        **Uso Total:** {metrics.cpu_usage_color} {metrics.cpu_usage}%
        **Load Avg:** {metrics.load_1m} {metrics.load_5m} {metrics.load_15m}
        **Frecuencia:** {metrics.cpu_freq_avg} MHz
        
        {metrics.cpu_load_bar}
        """,
        inline=True
    )
    
    # Memory Section
    embed.add_field(
        name=f"🧠 Memoria {metrics.memory_color}",
        value=f"""
        **RAM:** {metrics.memory_status}
        **Swap:** {metrics.swap_used}MB / {metrics.swap_total}MB
        **Disponible:** {metrics.memory_available}GB
        
        {metrics.memory_bar}
        """,
        inline=True
    )
    
    # Storage Section
    embed.add_field(
        name=f"💾 Almacenamiento {metrics.storage_color}",
        value=f"""
        **Usado:** {metrics.disk_used}GB / {metrics.disk_total}GB
        **Libre:** {metrics.disk_free}GB ({metrics.disk_percentage}%)
        **I/O:** ↗️{metrics.disk_read_speed} ↙️{metrics.disk_write_speed}
        
        {metrics.storage_bar}
        """,
        inline=False
    )
    
    # Network Section
    embed.add_field(
        name=f"🌐 Red {metrics.network_status_color}",
        value=f"""
        **Subida:** ↗️ {metrics.network_upload_speed} MB/s
        **Bajada:** ↙️ {metrics.network_download_speed} MB/s
        **Ping:** {metrics.ping_latency}ms
        **Conexiones:** {metrics.active_connections}
        """,
        inline=True
    )
    
    # System Info
    embed.add_field(
        name="⚙️ Sistema",
        value=f"""
        **Uptime:** {metrics.uptime_formatted}
        **Procesos:** {metrics.process_count}
        **Usuarios:** {metrics.logged_users}
        **Kernel:** {metrics.kernel_version}
        """,
        inline=True
    )
    
    # Alerts (si hay)
    if metrics.has_alerts:
        embed.add_field(
            name="🚨 Alertas",
            value=metrics.alerts_text,
            inline=False
        )
    
    # Footer con timestamp
    embed.set_footer(
        text=f"🤖 Actualizado cada 30s • Próxima actualización: {metrics.next_update}",
        icon_url="https://cdn.discordapp.com/emojis/orangepi_icon.png"
    )
    
    return embed
```

## 🦀 Estructura Rust Component

```rust
// system_monitor/src/main.rs
use serde::{Deserialize, Serialize};
use std::fs;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Serialize, Deserialize)]
pub struct SystemMetrics {
    // CPU
    pub cpu_temp: f32,
    pub cpu_usage: f32,
    pub cpu_usage_per_core: Vec<f32>,
    pub cpu_freq_avg: u32,
    pub load_avg: (f32, f32, f32),
    
    // Memory
    pub memory_total: u64,
    pub memory_used: u64,
    pub memory_available: u64,
    pub memory_percentage: f32,
    pub swap_total: u64,
    pub swap_used: u64,
    
    // Storage
    pub disk_total: u64,
    pub disk_used: u64,
    pub disk_free: u64,
    pub disk_percentage: f32,
    pub disk_read_speed: f32,
    pub disk_write_speed: f32,
    
    // Network
    pub network_upload_speed: f32,
    pub network_download_speed: f32,
    pub ping_latency: u32,
    pub active_connections: u32,
    
    // System
    pub uptime: u64,
    pub process_count: u32,
    pub logged_users: u32,
    pub kernel_version: String,
    
    // Metadata
    pub timestamp: u64,
    pub alerts: Vec<String>,
}

impl SystemMetrics {
    pub fn collect() -> Result<Self, Box<dyn std::error::Error>> {
        Ok(SystemMetrics {
            cpu_temp: Self::get_cpu_temperature()?,
            cpu_usage: Self::get_cpu_usage()?,
            cpu_usage_per_core: Self::get_cpu_usage_per_core()?,
            cpu_freq_avg: Self::get_cpu_frequency_avg()?,
            load_avg: Self::get_load_average()?,
            
            memory_total: Self::get_memory_total()?,
            memory_used: Self::get_memory_used()?,
            memory_available: Self::get_memory_available()?,
            memory_percentage: Self::calculate_memory_percentage()?,
            swap_total: Self::get_swap_total()?,
            swap_used: Self::get_swap_used()?,
            
            disk_total: Self::get_disk_total()?,
            disk_used: Self::get_disk_used()?,
            disk_free: Self::get_disk_free()?,
            disk_percentage: Self::calculate_disk_percentage()?,
            disk_read_speed: Self::get_disk_read_speed()?,
            disk_write_speed: Self::get_disk_write_speed()?,
            
            network_upload_speed: Self::get_network_upload_speed()?,
            network_download_speed: Self::get_network_download_speed()?,
            ping_latency: Self::get_ping_latency()?,
            active_connections: Self::get_active_connections()?,
            
            uptime: Self::get_uptime()?,
            process_count: Self::get_process_count()?,
            logged_users: Self::get_logged_users()?,
            kernel_version: Self::get_kernel_version()?,
            
            timestamp: SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs(),
            alerts: Self::generate_alerts()?,
        })
    }
}

fn main() {
    match SystemMetrics::collect() {
        Ok(metrics) => {
            println!("{}", serde_json::to_string_pretty(&metrics).unwrap());
        }
        Err(e) => {
            eprintln!("Error collecting metrics: {}", e);
            std::process::exit(1);
        }
    }
}
```

## 🚀 Próximos Pasos

1. **Implementar Rust binary** con métricas básicas
2. **Integrar con comando `>info`** actual
3. **Añadir colores dinámicos** según thresholds
4. **Testing en OrangePi 5 Plus** real
5. **Optimizar performance** y caching
6. **Documentar API** del sistema

¿Te gusta este diseño? ¿Quieres que empecemos implementando el componente Rust o prefieres primero migrar a uv?