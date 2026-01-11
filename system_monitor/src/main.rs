use anyhow::Result;
use clap::Parser;
use serde::{Deserialize, Serialize};
use std::fs;
use std::time::{SystemTime, UNIX_EPOCH};
use sysinfo::{System, Disks, Networks};

#[derive(Parser)]
#[command(name = "system_monitor")]
#[command(about = "Monitor avanzado para OrangePi 5 Plus")]
struct Cli {
    /// Formato de salida (json, pretty, compact)
    #[arg(short, long, default_value = "json")]
    format: String,
    
    /// Incluir métricas detalladas por core
    #[arg(long)]
    detailed_cpu: bool,
    
    /// Incluir información de procesos
    #[arg(long)]
    processes: bool,
    
    /// Número de procesos top a mostrar
    #[arg(long, default_value = "5")]
    top_processes: usize,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SystemMetrics {
    // Metadata
    pub timestamp: u64,
    pub hostname: String,
    pub uptime: u64,
    pub boot_time: u64,
    
    // CPU
    pub cpu: CpuMetrics,
    
    // Memory
    pub memory: MemoryMetrics,
    
    // Storage
    pub storage: Vec<StorageMetrics>,
    
    // Network
    pub network: NetworkMetrics,
    
    // System
    pub system: SystemInfo,
    
    // Processes (opcional)
    pub processes: Option<Vec<ProcessInfo>>,
    
    // Alerts
    pub alerts: Vec<Alert>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct CpuMetrics {
    pub usage_percent: f32,
    pub cores: Vec<CoreMetrics>,
    pub temperature: Option<f32>,
    pub frequency: Option<u64>,
    pub load_average: (f64, f64, f64),
}

#[derive(Serialize, Deserialize, Debug)]
pub struct CoreMetrics {
    pub id: usize,
    pub usage_percent: f32,
    pub frequency: Option<u64>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct MemoryMetrics {
    pub total: u64,
    pub used: u64,
    pub available: u64,
    pub percentage: f32,
    pub swap_total: u64,
    pub swap_used: u64,
    pub swap_percentage: f32,
    pub buffers: u64,
    pub cached: u64,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct StorageMetrics {
    pub name: String,
    pub mount_point: String,
    pub total: u64,
    pub used: u64,
    pub available: u64,
    pub percentage: f32,
    pub filesystem: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct NetworkMetrics {
    pub interfaces: Vec<NetworkInterface>,
    pub total_bytes_sent: u64,
    pub total_bytes_received: u64,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct NetworkInterface {
    pub name: String,
    pub bytes_sent: u64,
    pub bytes_received: u64,
    pub packets_sent: u64,
    pub packets_received: u64,
    pub errors_sent: u64,
    pub errors_received: u64,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SystemInfo {
    pub os_name: String,
    pub os_version: String,
    pub kernel_version: String,
    pub architecture: String,
    pub cpu_count: usize,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ProcessInfo {
    pub pid: u32,
    pub name: String,
    pub cpu_usage: f32,
    pub memory_usage: u64,
    pub memory_percentage: f32,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Alert {
    pub level: AlertLevel,
    pub message: String,
    pub metric: String,
    pub value: f32,
    pub threshold: f32,
}

#[derive(Serialize, Deserialize, Debug)]
pub enum AlertLevel {
    Info,
    Warning,
    Critical,
}

impl SystemMetrics {
    pub fn collect(detailed_cpu: bool, include_processes: bool, top_processes: usize) -> Result<Self> {
        let mut system = System::new_all();
        system.refresh_all();
        
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)?
            .as_secs();
        
        // CPU Metrics
        let cpu = Self::collect_cpu_metrics(&system, detailed_cpu)?;
        
        // Memory Metrics
        let memory = Self::collect_memory_metrics(&system)?;
        
        // Storage Metrics
        let storage = Self::collect_storage_metrics(&system)?;
        
        // Network Metrics
        let network = Self::collect_network_metrics(&system)?;
        
        // System Info
        let system_info = Self::collect_system_info(&system)?;
        
        // Processes (opcional)
        let processes = if include_processes {
            Some(Self::collect_process_metrics(&system, top_processes)?)
        } else {
            None
        };
        
        // Generate alerts
        let alerts = Self::generate_alerts(&cpu, &memory, &storage)?;
        
        Ok(SystemMetrics {
            timestamp,
            hostname: System::host_name().unwrap_or_else(|| "unknown".to_string()),
            uptime: System::uptime(),
            boot_time: System::boot_time(),
            cpu,
            memory,
            storage,
            network,
            system: system_info,
            processes,
            alerts,
        })
    }
    
    fn collect_cpu_metrics(system: &System, detailed: bool) -> Result<CpuMetrics> {
        let cpus = system.cpus();
        let global_cpu_usage = system.global_cpu_usage();
        
        // Temperatura CPU (específico para OrangePi/ARM)
        let temperature = Self::get_cpu_temperature().ok();
        
        // Frecuencia CPU
        let frequency = Self::get_cpu_frequency().ok();
        
        // Load average
        let load_avg = System::load_average();
        
        let cores = if detailed {
            cpus.iter()
                .enumerate()
                .map(|(id, cpu)| CoreMetrics {
                    id,
                    usage_percent: cpu.cpu_usage(),
                    frequency: None, // TODO: per-core frequency
                })
                .collect()
        } else {
            Vec::new()
        };
        
        Ok(CpuMetrics {
            usage_percent: global_cpu_usage,
            cores,
            temperature,
            frequency,
            load_average: (load_avg.one, load_avg.five, load_avg.fifteen),
        })
    }
    
    fn collect_memory_metrics(system: &System) -> Result<MemoryMetrics> {
        let total = system.total_memory();
        let used = system.used_memory();
        let available = system.available_memory();
        let percentage = (used as f32 / total as f32) * 100.0;
        
        let swap_total = system.total_swap();
        let swap_used = system.used_swap();
        let swap_percentage = if swap_total > 0 {
            (swap_used as f32 / swap_total as f32) * 100.0
        } else {
            0.0
        };
        
        // Buffers y cache desde /proc/meminfo
        let (buffers, cached) = Self::get_memory_details().unwrap_or((0, 0));
        
        Ok(MemoryMetrics {
            total,
            used,
            available,
            percentage,
            swap_total,
            swap_used,
            swap_percentage,
            buffers,
            cached,
        })
    }
    
    fn collect_storage_metrics(_system: &System) -> Result<Vec<StorageMetrics>> {
        let mut storage_metrics = Vec::new();
        let disks = Disks::new_with_refreshed_list();
        
        for disk in &disks {
            let total = disk.total_space();
            let available = disk.available_space();
            let used = total - available;
            let percentage = if total > 0 {
                (used as f32 / total as f32) * 100.0
            } else {
                0.0
            };
            
            storage_metrics.push(StorageMetrics {
                name: disk.name().to_string_lossy().to_string(),
                mount_point: disk.mount_point().to_string_lossy().to_string(),
                total,
                used,
                available,
                percentage,
                filesystem: format!("{:?}", disk.file_system()),
            });
        }
        
        Ok(storage_metrics)
    }
    
    fn collect_network_metrics(_system: &System) -> Result<NetworkMetrics> {
        let mut interfaces = Vec::new();
        let mut total_sent = 0;
        let mut total_received = 0;
        let networks = Networks::new_with_refreshed_list();
        
        for (interface_name, data) in &networks {
            let bytes_sent = data.total_transmitted();
            let bytes_received = data.total_received();
            
            total_sent += bytes_sent;
            total_received += bytes_received;
            
            interfaces.push(NetworkInterface {
                name: interface_name.clone(),
                bytes_sent,
                bytes_received,
                packets_sent: data.total_packets_transmitted(),
                packets_received: data.total_packets_received(),
                errors_sent: data.total_errors_on_transmitted(),
                errors_received: data.total_errors_on_received(),
            });
        }
        
        Ok(NetworkMetrics {
            interfaces,
            total_bytes_sent: total_sent,
            total_bytes_received: total_received,
        })
    }
    
    fn collect_system_info(system: &System) -> Result<SystemInfo> {
        Ok(SystemInfo {
            os_name: System::name().unwrap_or_else(|| "Unknown".to_string()),
            os_version: System::os_version().unwrap_or_else(|| "Unknown".to_string()),
            kernel_version: System::kernel_version().unwrap_or_else(|| "Unknown".to_string()),
            architecture: std::env::consts::ARCH.to_string(),
            cpu_count: system.cpus().len(),
        })
    }
    
    fn collect_process_metrics(system: &System, top_count: usize) -> Result<Vec<ProcessInfo>> {
        let mut processes: Vec<_> = system.processes()
            .values()
            .map(|process| ProcessInfo {
                pid: process.pid().as_u32(),
                name: process.name().to_string_lossy().to_string(),
                cpu_usage: process.cpu_usage(),
                memory_usage: process.memory(),
                memory_percentage: (process.memory() as f32 / system.total_memory() as f32) * 100.0,
            })
            .collect();
        
        // Ordenar por uso de CPU
        processes.sort_by(|a, b| b.cpu_usage.partial_cmp(&a.cpu_usage).unwrap());
        processes.truncate(top_count);
        
        Ok(processes)
    }
    
    fn generate_alerts(cpu: &CpuMetrics, memory: &MemoryMetrics, storage: &[StorageMetrics]) -> Result<Vec<Alert>> {
        let mut alerts = Vec::new();
        
        // CPU Alerts
        if cpu.usage_percent > 90.0 {
            alerts.push(Alert {
                level: AlertLevel::Critical,
                message: "CPU usage crítico".to_string(),
                metric: "cpu_usage".to_string(),
                value: cpu.usage_percent,
                threshold: 90.0,
            });
        } else if cpu.usage_percent > 75.0 {
            alerts.push(Alert {
                level: AlertLevel::Warning,
                message: "CPU usage alto".to_string(),
                metric: "cpu_usage".to_string(),
                value: cpu.usage_percent,
                threshold: 75.0,
            });
        }
        
        // Temperature Alerts
        if let Some(temp) = cpu.temperature {
            if temp > 85.0 {
                alerts.push(Alert {
                    level: AlertLevel::Critical,
                    message: "Temperatura CPU crítica".to_string(),
                    metric: "cpu_temperature".to_string(),
                    value: temp,
                    threshold: 85.0,
                });
            } else if temp > 75.0 {
                alerts.push(Alert {
                    level: AlertLevel::Warning,
                    message: "Temperatura CPU alta".to_string(),
                    metric: "cpu_temperature".to_string(),
                    value: temp,
                    threshold: 75.0,
                });
            }
        }
        
        // Memory Alerts
        if memory.percentage > 95.0 {
            alerts.push(Alert {
                level: AlertLevel::Critical,
                message: "Memoria RAM crítica".to_string(),
                metric: "memory_usage".to_string(),
                value: memory.percentage,
                threshold: 95.0,
            });
        } else if memory.percentage > 85.0 {
            alerts.push(Alert {
                level: AlertLevel::Warning,
                message: "Memoria RAM alta".to_string(),
                metric: "memory_usage".to_string(),
                value: memory.percentage,
                threshold: 85.0,
            });
        }
        
        // Storage Alerts
        for storage in storage {
            if storage.percentage > 95.0 {
                alerts.push(Alert {
                    level: AlertLevel::Critical,
                    message: format!("Disco {} crítico", storage.mount_point),
                    metric: "disk_usage".to_string(),
                    value: storage.percentage,
                    threshold: 95.0,
                });
            } else if storage.percentage > 85.0 {
                alerts.push(Alert {
                    level: AlertLevel::Warning,
                    message: format!("Disco {} alto", storage.mount_point),
                    metric: "disk_usage".to_string(),
                    value: storage.percentage,
                    threshold: 85.0,
                });
            }
        }
        
        Ok(alerts)
    }
    
    // Funciones específicas para OrangePi/ARM
    fn get_cpu_temperature() -> Result<f32> {
        // Intentar leer temperatura del thermal zone
        let temp_paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/class/thermal/thermal_zone1/temp",
        ];
        
        for path in &temp_paths {
            if let Ok(content) = fs::read_to_string(path) {
                if let Ok(temp_millidegrees) = content.trim().parse::<i32>() {
                    return Ok(temp_millidegrees as f32 / 1000.0);
                }
            }
        }
        
        Err(anyhow::anyhow!("No se pudo leer la temperatura"))
    }
    
    fn get_cpu_frequency() -> Result<u64> {
        // Intentar leer frecuencia actual
        let freq_path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq";
        
        if let Ok(content) = fs::read_to_string(freq_path) {
            if let Ok(freq_khz) = content.trim().parse::<u64>() {
                return Ok(freq_khz * 1000); // Convertir a Hz
            }
        }
        
        Err(anyhow::anyhow!("No se pudo leer la frecuencia"))
    }
    
    fn get_memory_details() -> Result<(u64, u64)> {
        // Leer /proc/meminfo para buffers y cache
        let meminfo = fs::read_to_string("/proc/meminfo")?;
        let mut buffers = 0;
        let mut cached = 0;
        
        for line in meminfo.lines() {
            if line.starts_with("Buffers:") {
                if let Some(value) = line.split_whitespace().nth(1) {
                    buffers = value.parse::<u64>().unwrap_or(0) * 1024; // kB to bytes
                }
            } else if line.starts_with("Cached:") {
                if let Some(value) = line.split_whitespace().nth(1) {
                    cached = value.parse::<u64>().unwrap_or(0) * 1024; // kB to bytes
                }
            }
        }
        
        Ok((buffers, cached))
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();
    
    let metrics = SystemMetrics::collect(
        cli.detailed_cpu,
        cli.processes,
        cli.top_processes,
    )?;
    
    match cli.format.as_str() {
        "pretty" => {
            println!("{}", serde_json::to_string_pretty(&metrics)?);
        }
        "compact" => {
            println!("{}", serde_json::to_string(&metrics)?);
        }
        _ => {
            println!("{}", serde_json::to_string_pretty(&metrics)?);
        }
    }
    
    Ok(())
}