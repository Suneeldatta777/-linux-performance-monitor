[README.md](https://github.com/user-attachments/files/25621507/README.md)
# 🖥️ Linux System Performance Monitor

A Python-based CLI tool to monitor and log **CPU, Memory, and Disk I/O** metrics in real time on Linux and Windows systems. Automatically generates alerts when resource usage exceeds defined thresholds.

---

## 📌 Features

- **Real-time monitoring** of CPU usage, RAM, Disk usage, and Disk I/O
- **Automatic alerts** when metrics exceed configurable thresholds
- **Structured logging** — outputs to both console and a log file
- **Modular architecture** — each metric collector is an independent, reusable function
- **Cross-platform** — works on Linux (Ubuntu, CentOS) and Windows
- **CLI support** — fully configurable via command-line arguments

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/linux-performance-monitor.git
cd linux-performance-monitor
```

### 2. Install dependencies
```bash
pip install psutil
```

### 3. Run the monitor
```bash
# Default: checks every 5 seconds, runs indefinitely
python monitor.py

# Custom interval (every 10 seconds)
python monitor.py --interval 10

# Run for 5 cycles only
python monitor.py --cycles 5

# Save logs to a custom file
python monitor.py --log my_logs.txt

# Combine options
python monitor.py --interval 3 --cycles 10 --log output.txt
```

---

## 📊 Sample Output

```
[2025-06-01 14:32:10] INFO     [ Cycle 1 — 2025-06-01 14:32:10 ]
[2025-06-01 14:32:11] INFO     ───────────────────────────────────────────────────────
[2025-06-01 14:32:11] INFO       CPU     | Usage: 23.4%  |  Cores: 8
[2025-06-01 14:32:11] INFO       MEMORY  | Usage: 61.2%  |  Used: 9.8 GB / 16.0 GB  |  Free: 6.2 GB
[2025-06-01 14:32:11] INFO       DISK    | Usage: 54.3%  |  Used: 108.6 GB / 200.0 GB  |  Free: 91.4 GB
[2025-06-01 14:32:11] INFO       DISK I/O| Read: 2045.3 MB  |  Written: 1893.7 MB
[2025-06-01 14:32:11] INFO     ───────────────────────────────────────────────────────
[2025-06-01 14:32:11] WARNING  HIGH MEMORY ALERT — Usage: 85.1% (threshold: 80.0%)
```

---

## ⚙️ Configuration

You can change default thresholds directly in `monitor.py`:

| Constant | Default | Description |
|---|---|---|
| `CPU_THRESHOLD` | `80.0` | Alert if CPU usage exceeds this % |
| `MEMORY_THRESHOLD` | `80.0` | Alert if Memory usage exceeds this % |
| `DISK_THRESHOLD` | `90.0` | Alert if Disk usage exceeds this % |
| `DEFAULT_INTERVAL` | `5` | Seconds between each check |

---

## 🗂️ Project Structure

```
linux-performance-monitor/
│
├── monitor.py          # Main script — metric collection, alerting, CLI
├── performance_log.txt # Auto-generated log file (after first run)
└── README.md           # Project documentation
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Library:** [psutil](https://pypi.org/project/psutil/) — cross-platform system metrics
- **Modules:** `os`, `time`, `logging`, `argparse`, `datetime`
- **Tested on:** Ubuntu 20.04, Windows 10

---

## 📖 How It Works

1. **Metric Collectors** — Separate functions (`get_cpu_metrics`, `get_memory_metrics`, `get_disk_metrics`, `get_disk_io_metrics`) collect system data using `psutil`
2. **Alert Engine** — `check_alerts()` compares each metric against its threshold and logs a WARNING if exceeded
3. **Logger** — Dual-output logging writes timestamped entries to both the console and a log file
4. **Monitor Loop** — `run_monitor()` orchestrates collection, reporting, and alerting at a configurable interval
5. **CLI** — `argparse` exposes `--interval`, `--log`, and `--cycles` flags for flexible usage

---

## 👤 Author

**Bairaju Suneel Datta**  
B.Tech — Artificial Intelligence  
Sri Venkateswara College of Engineering, Tirupati  
📧 suneeldatta6@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/bairajusuneel-datta-081aa4264)
