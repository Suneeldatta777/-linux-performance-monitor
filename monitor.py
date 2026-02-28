"""
Linux System Performance Monitor
=================================
Monitors CPU, Memory, and Disk I/O metrics on Linux/Windows systems.
Logs results to a file and triggers alerts when thresholds are exceeded.

Author : Bairaju Suneel Datta
GitHub : github.com/bairajusuneel-datta
"""

import os
import time
import logging
import argparse
from datetime import datetime

try:
    import psutil
except ImportError:
    print("Error: 'psutil' library not found. Run: pip install psutil")
    exit(1)


# ── CONFIGURATION ──────────────────────────────────────────────────────────────

DEFAULT_INTERVAL   = 5       # seconds between each check
DEFAULT_LOG_FILE   = "performance_log.txt"
CPU_THRESHOLD      = 80.0    # % — alert if CPU usage exceeds this
MEMORY_THRESHOLD   = 80.0    # % — alert if memory usage exceeds this
DISK_THRESHOLD     = 90.0    # % — alert if disk usage exceeds this


# ── LOGGING SETUP ───────────────────────────────────────────────────────────────

def setup_logger(log_file: str) -> logging.Logger:
    """Configure logger to write to both console and a log file."""
    logger = logging.getLogger("PerfMonitor")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# ── METRIC COLLECTORS ───────────────────────────────────────────────────────────

def get_cpu_metrics() -> dict:
    """Collect CPU usage percentage."""
    return {
        "usage_percent": psutil.cpu_percent(interval=1),
        "core_count"   : psutil.cpu_count(logical=True),
    }


def get_memory_metrics() -> dict:
    """Collect RAM usage statistics."""
    mem = psutil.virtual_memory()
    return {
        "total_gb"      : round(mem.total / (1024 ** 3), 2),
        "used_gb"       : round(mem.used  / (1024 ** 3), 2),
        "available_gb"  : round(mem.available / (1024 ** 3), 2),
        "usage_percent" : mem.percent,
    }


def get_disk_metrics(path: str = "/") -> dict:
    """Collect disk usage statistics for a given path."""
    disk = psutil.disk_usage(path)
    return {
        "path"          : path,
        "total_gb"      : round(disk.total / (1024 ** 3), 2),
        "used_gb"       : round(disk.used  / (1024 ** 3), 2),
        "free_gb"       : round(disk.free  / (1024 ** 3), 2),
        "usage_percent" : disk.percent,
    }


def get_disk_io_metrics() -> dict:
    """Collect disk I/O read/write counters."""
    io = psutil.disk_io_counters()
    if io is None:
        return {"read_mb": 0, "write_mb": 0}
    return {
        "read_mb" : round(io.read_bytes  / (1024 ** 2), 2),
        "write_mb": round(io.write_bytes / (1024 ** 2), 2),
    }


# ── ALERT ENGINE ────────────────────────────────────────────────────────────────

def check_alerts(cpu: dict, memory: dict, disk: dict, logger: logging.Logger):
    """Log WARNING alerts if any metric exceeds its defined threshold."""
    if cpu["usage_percent"] > CPU_THRESHOLD:
        logger.warning(
            f"HIGH CPU ALERT — Usage: {cpu['usage_percent']}% "
            f"(threshold: {CPU_THRESHOLD}%)"
        )

    if memory["usage_percent"] > MEMORY_THRESHOLD:
        logger.warning(
            f"HIGH MEMORY ALERT — Usage: {memory['usage_percent']}% "
            f"| Used: {memory['used_gb']} GB / {memory['total_gb']} GB "
            f"(threshold: {MEMORY_THRESHOLD}%)"
        )

    if disk["usage_percent"] > DISK_THRESHOLD:
        logger.warning(
            f"HIGH DISK ALERT — Usage: {disk['usage_percent']}% "
            f"| Used: {disk['used_gb']} GB / {disk['total_gb']} GB "
            f"(threshold: {DISK_THRESHOLD}%)"
        )


# ── REPORT PRINTER ──────────────────────────────────────────────────────────────

def print_report(cpu: dict, memory: dict, disk: dict, io: dict, logger: logging.Logger):
    """Log a formatted snapshot of all current metrics."""
    logger.info("─" * 55)
    logger.info(f"  CPU     | Usage: {cpu['usage_percent']}%  |  Cores: {cpu['core_count']}")
    logger.info(f"  MEMORY  | Usage: {memory['usage_percent']}%  |  Used: {memory['used_gb']} GB / {memory['total_gb']} GB  |  Free: {memory['available_gb']} GB")
    logger.info(f"  DISK    | Usage: {disk['usage_percent']}%  |  Used: {disk['used_gb']} GB / {disk['total_gb']} GB  |  Free: {disk['free_gb']} GB")
    logger.info(f"  DISK I/O| Read: {io['read_mb']} MB  |  Written: {io['write_mb']} MB")
    logger.info("─" * 55)


# ── MAIN MONITOR LOOP ───────────────────────────────────────────────────────────

def run_monitor(interval: int, log_file: str, cycles: int = 0):
    """
    Main monitoring loop.

    Args:
        interval : seconds between each metric collection cycle
        log_file : path to output log file
        cycles   : number of cycles to run (0 = run indefinitely)
    """
    logger = setup_logger(log_file)
    logger.info("=" * 55)
    logger.info("  Linux System Performance Monitor — Started")
    logger.info(f"  Interval : {interval}s  |  Log file: {log_file}")
    logger.info("=" * 55)

    # Detect OS
    platform = "Windows" if os.name == "nt" else "Linux/Mac"
    disk_path = "C:\\" if os.name == "nt" else "/"
    logger.info(f"  Platform : {platform}")

    count = 0
    try:
        while True:
            count += 1
            logger.info(f"\n  [ Cycle {count} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ]")

            # Collect all metrics
            cpu    = get_cpu_metrics()
            memory = get_memory_metrics()
            disk   = get_disk_metrics(disk_path)
            io     = get_disk_io_metrics()

            # Print snapshot
            print_report(cpu, memory, disk, io, logger)

            # Check and fire alerts
            check_alerts(cpu, memory, disk, logger)

            # Stop after N cycles if specified
            if cycles > 0 and count >= cycles:
                logger.info("Monitor completed all requested cycles. Exiting.")
                break

            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("\nMonitor stopped by user (Ctrl+C). Goodbye!")


# ── CLI ENTRY POINT ─────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Linux System Performance Monitor — Monitor CPU, Memory, and Disk metrics"
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=DEFAULT_INTERVAL,
        help=f"Seconds between each check (default: {DEFAULT_INTERVAL})"
    )
    parser.add_argument(
        "--log", "-l",
        type=str,
        default=DEFAULT_LOG_FILE,
        help=f"Log file path (default: {DEFAULT_LOG_FILE})"
    )
    parser.add_argument(
        "--cycles", "-c",
        type=int,
        default=0,
        help="Number of monitoring cycles to run (default: 0 = run forever)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_monitor(
        interval=args.interval,
        log_file=args.log,
        cycles=args.cycles
    )
