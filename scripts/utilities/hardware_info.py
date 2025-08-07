#!/usr/bin/env python3
"""
Comprehensive Hardware Information Script
Gathers detailed system specs for AI development optimization
"""

import subprocess
import psutil
import platform
import os
import json
from datetime import datetime
import time


def get_system_info():
    """Get basic system information"""
    info = {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        },
    }
    return info


def get_cpu_info():
    """Get detailed CPU information"""
    cpu_info = {
        "cpu_count": psutil.cpu_count(),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        "cpu_stats": psutil.cpu_stats()._asdict(),
        "cpu_times": psutil.cpu_times()._asdict(),
        "cpu_times_percent": psutil.cpu_times_percent()._asdict(),
    }

    # Get detailed CPU info using wmic
    try:
        result = subprocess.run(
            [
                "wmic",
                "cpu",
                "get",
                "name,numberofcores,maxclockspeed,voltage",
                "/format:csv",
            ],
            capture_output=True,
            text=True,
        )
        cpu_info["wmic_details"] = result.stdout
    except:
        cpu_info["wmic_details"] = "Not available"

    return cpu_info


def get_memory_info():
    """Get detailed memory information"""
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    memory_info = {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "free": memory.free,
        "percent": memory.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_free": swap.free,
        "swap_percent": swap.percent,
    }
    return memory_info


def get_disk_info():
    """Get detailed disk information and performance"""
    disk_info = {
        "partitions": [],
        "disk_usage": [],
        "disk_io": (
            psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else None
        ),
    }

    # Get all partitions
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info["partitions"].append(
                {
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "opts": partition.opts,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                }
            )
        except:
            continue

    return disk_info


def get_gpu_info():
    """Get GPU information using nvidia-smi if available"""
    gpu_info = {"nvidia_gpus": [], "available": False}

    try:
        # Try to get NVIDIA GPU info
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu,utilization.gpu,utilization.memory",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            gpu_info["available"] = True
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if line.strip():
                    parts = line.split(", ")
                    if len(parts) >= 7:
                        gpu_info["nvidia_gpus"].append(
                            {
                                "name": parts[0],
                                "memory_total": int(parts[1]),
                                "memory_used": int(parts[2]),
                                "memory_free": int(parts[3]),
                                "temperature": int(parts[4]),
                                "gpu_utilization": int(parts[5]),
                                "memory_utilization": int(parts[6]),
                            }
                        )
    except:
        pass

    return gpu_info


def get_network_info():
    """Get network information"""
    network_info = {
        "interfaces": [],
        "connections": [],
        "io_counters": (
            psutil.net_io_counters()._asdict() if psutil.net_io_counters() else None
        ),
    }

    # Get network interfaces
    for interface, addresses in psutil.net_if_addrs().items():
        interface_info = {"interface": interface, "addresses": []}
        for addr in addresses:
            interface_info["addresses"].append(
                {
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast,
                }
            )
        network_info["interfaces"].append(interface_info)

    # Get network connections
    try:
        connections = psutil.net_connections()
        for conn in connections[:10]:  # Limit to first 10 connections
            network_info["connections"].append(
                {
                    "fd": conn.fd,
                    "family": str(conn.family),
                    "type": str(conn.type),
                    "laddr": (
                        f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None
                    ),
                    "raddr": (
                        f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None
                    ),
                    "status": conn.status,
                }
            )
    except:
        pass

    return network_info


def get_process_info():
    """Get information about current processes"""
    process_info = {"total_processes": len(psutil.pids()), "top_processes": []}

    # Get top 10 processes by memory usage
    processes = []
    for proc in psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent"]):
        try:
            processes.append(proc.info)
        except:
            continue

    # Sort by memory usage
    processes.sort(key=lambda x: x["memory_percent"] or 0, reverse=True)
    process_info["top_processes"] = processes[:10]

    return process_info


def benchmark_disk_performance():
    """Simple disk performance benchmark"""
    benchmark_results = {}

    # Test write performance
    test_file = "disk_benchmark_test.tmp"
    test_size = 100 * 1024 * 1024  # 100MB

    try:
        # Write test
        start_time = time.time()
        with open(test_file, "wb") as f:
            f.write(b"0" * test_size)
        write_time = time.time() - start_time
        write_speed = test_size / write_time / (1024 * 1024)  # MB/s

        # Read test
        start_time = time.time()
        with open(test_file, "rb") as f:
            f.read()
        read_time = time.time() - start_time
        read_speed = test_size / read_time / (1024 * 1024)  # MB/s

        # Cleanup
        os.remove(test_file)

        benchmark_results = {
            "write_speed_mbps": round(write_speed, 2),
            "read_speed_mbps": round(read_speed, 2),
            "write_time_seconds": round(write_time, 2),
            "read_time_seconds": round(read_time, 2),
        }
    except Exception as e:
        benchmark_results = {"error": str(e)}

    return benchmark_results


def get_detailed_hardware_info():
    """Get all hardware information"""
    print("🔍 Gathering comprehensive hardware information...")

    hardware_info = {
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "gpu": get_gpu_info(),
        "network": get_network_info(),
        "processes": get_process_info(),
    }

    print("⚡ Running disk performance benchmark...")
    hardware_info["disk_benchmark"] = benchmark_disk_performance()

    return hardware_info


def format_size(bytes):
    """Format bytes into human readable format"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"


def print_hardware_summary(hardware_info):
    """Print a summary of hardware information"""
    print("\n" + "=" * 60)
    print("🖥️  HARDWARE INFORMATION SUMMARY")
    print("=" * 60)

    # System
    print(f"\n📋 System: {hardware_info['system']['system']['platform']}")
    print(f"🐍 Python: {hardware_info['system']['system']['python_version']}")

    # CPU
    cpu = hardware_info["cpu"]
    print(f"\n🖥️  CPU: {cpu['cpu_count']} cores ({cpu['cpu_count_logical']} logical)")
    if cpu["cpu_freq"]:
        print(f"⚡ Frequency: {cpu['cpu_freq']['current']:.0f} MHz")
    print(f"📊 Usage: {cpu['cpu_percent']:.1f}%")

    # Memory
    mem = hardware_info["memory"]
    print(f"\n💾 Memory: {format_size(mem['total'])} total")
    print(f"� Usage: {mem['percent']:.1f}% ({format_size(mem['used'])} used)")
    print(f"🆓 Available: {format_size(mem['available'])}")

    # Disk
    disk = hardware_info["disk"]
    print(f"\n💿 Disk Partitions:")
    for partition in disk["partitions"]:
        if partition["total"] > 0:
            print(
                f"   {partition['device']}: {format_size(partition['total'])} "
                f"({partition['percent']:.1f}% used)"
            )

    # GPU
    gpu = hardware_info["gpu"]
    if gpu["available"]:
        print(f"\n🎮 GPU:")
        for i, gpu_info in enumerate(gpu["nvidia_gpus"]):
            print(f"   GPU {i}: {gpu_info['name']}")
            print(
                f"   Memory: {gpu_info['memory_used']}MB / {gpu_info['memory_total']}MB"
            )
            print(f"   Temperature: {gpu_info['temperature']}°C")
            print(f"   Utilization: {gpu_info['gpu_utilization']}%")
    else:
        print(f"\n🎮 GPU: No NVIDIA GPUs detected")

    # Disk Performance
    benchmark = hardware_info["disk_benchmark"]
    if "error" not in benchmark:
        print(f"\n⚡ Disk Performance:")
        print(f"   Write Speed: {benchmark['write_speed_mbps']} MB/s")
        print(f"   Read Speed: {benchmark['read_speed_mbps']} MB/s")

    # Network
    net = hardware_info["network"]
    if net["io_counters"]:
        print(f"\n🌐 Network I/O:")
        print(f"   Bytes Sent: {format_size(net['io_counters']['bytes_sent'])}")
        print(f"   Bytes Recv: {format_size(net['io_counters']['bytes_recv'])}")

    print("\n" + "=" * 60)


def save_hardware_info(hardware_info, filename="hardware_info.json"):
    """Save hardware information to JSON file"""
    with open(filename, "w") as f:
        json.dump(hardware_info, f, indent=2, default=str)
    print(f"\n💾 Hardware information saved to: {filename}")


if __name__ == "__main__":
    try:
        # Get comprehensive hardware information
        hardware_info = get_detailed_hardware_info()

        # Print summary
        print_hardware_summary(hardware_info)

        # Save to file
        save_hardware_info(hardware_info)

        print(f"\n✅ Hardware information gathering complete!")
        print(f"📄 Full details saved to: hardware_info.json")

    except Exception as e:
        print(f"❌ Error gathering hardware information: {e}")
        import traceback

        traceback.print_exc()
