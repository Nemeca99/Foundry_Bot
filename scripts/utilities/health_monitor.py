# flake8: noqa
# type: ignore
#!/usr/bin/env python3
"""
Consolidated Health Monitor and Data Manager
Provides monitoring endpoints, system health tracking, and reliable data operations
"""

import asyncio
import json
import logging
import psutil
import time
import tempfile
import shutil

# fcntl is not available on Windows, use alternative approach
try:
    import fcntl

    FCNTL_AVAILABLE = True
except ImportError:
    FCNTL_AVAILABLE = False
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import socket
import os
import aiohttp
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DataManager:
    """Reliable data operations with atomic writes and file locking"""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path("data")
        self.backup_dir = self.data_dir / ".backups"
        self.temp_dir = self.data_dir / ".temp"

        # Create directories
        self.data_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

        # Backup configuration
        self.max_backups = 5
        self.backup_on_write = True

    @contextmanager
    def file_lock(self, file_path: Path, mode: str = "r"):
        """Context manager for file locking"""
        if not FCNTL_AVAILABLE:
            # On Windows, just open the file without locking
            with open(file_path, mode) as f:
                yield f
            return

        lock_file = file_path.with_suffix(file_path.suffix + ".lock")

        try:
            # Create lock file
            lock_fd = os.open(str(lock_file), os.O_CREAT | os.O_WRONLY)

            # Acquire exclusive lock with timeout
            timeout = 10  # seconds
            start_time = time.time()

            while True:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError:
                    if time.time() - start_time > timeout:
                        raise TimeoutError(f"Could not acquire lock for {file_path}")
                    time.sleep(0.1)

            # Open the actual file
            with open(file_path, mode) as f:
                yield f

        finally:
            # Release lock and cleanup
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                os.close(lock_fd)
                lock_file.unlink(missing_ok=True)
            except Exception as e:
                logger.warning(f"Error releasing lock: {e}")

    def atomic_write_json(self, file_path: Path, data: Any) -> bool:
        """Atomically write JSON data to file"""
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Create backup if file exists and backup is enabled
            if self.backup_on_write and file_path.exists():
                self._create_backup(file_path)

            # Create temporary file in same directory for atomic move
            temp_file = self.temp_dir / f"{file_path.name}.{int(time.time())}.tmp"

            # Write to temporary file
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())  # Ensure data is written to disk

            # Atomically move to target location
            shutil.move(str(temp_file), str(file_path))
            return True

        except Exception as e:
            logger.error(f"Atomic write failed for {file_path}: {e}")
            # Clean up temp file if it exists
            temp_file.unlink(missing_ok=True)
            return False

    def safe_read_json(self, file_path: Path, default: Any = None) -> Any:
        """Safely read JSON data with error handling and backup restoration"""
        try:
            if not file_path.exists():
                return default

            # Try to read the file
            with self.file_lock(file_path, "r") as f:
                data = json.load(f)

            # Validate the data structure
            self._validate_json_structure(data)
            return data

        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.warning(f"JSON decode error for {file_path}: {e}")
            # Try to restore from backup
            return self._try_restore_backup(file_path, default)

        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return self._try_restore_backup(file_path, default)

    def safe_write_json(self, file_path: Path, data: Any) -> bool:
        """Safely write JSON data with validation and atomic operations"""
        try:
            # Validate data structure before writing
            self._validate_json_structure(data)

            # Perform atomic write
            success = self.atomic_write_json(file_path, data)

            if success:
                # Clean up old backups
                self._cleanup_old_backups(file_path.name)
                logger.info(f"Successfully wrote {file_path}")
                return True
            else:
                logger.error(f"Failed to write {file_path}")
                return False

        except Exception as e:
            logger.error(f"Safe write failed for {file_path}: {e}")
            return False

    def _validate_json_structure(self, data: Any) -> None:
        """Validate JSON data structure"""
        if not isinstance(data, (dict, list, str, int, float, bool, type(None))):
            raise ValueError(f"Invalid JSON data type: {type(data)}")

        if isinstance(data, dict):
            for key, value in data.items():
                if not isinstance(key, str):
                    raise ValueError(f"Invalid dictionary key type: {type(key)}")
                self._validate_json_structure(value)

        elif isinstance(data, list):
            for item in data:
                self._validate_json_structure(item)

    def _create_backup(self, file_path: Path) -> bool:
        """Create a backup of the file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_name

            shutil.copy2(file_path, backup_path)
            logger.info(f"Created backup: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return False

    def _cleanup_old_backups(self, base_filename: str) -> None:
        """Clean up old backups, keeping only the most recent ones"""
        try:
            # Find all backups for this file
            backup_pattern = f"{base_filename.split('.')[0]}_*"
            backups = list(self.backup_dir.glob(backup_pattern))

            # Sort by modification time (newest first)
            backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            # Remove old backups beyond the limit
            for backup in backups[self.max_backups :]:
                backup.unlink()
                logger.info(f"Removed old backup: {backup}")

        except Exception as e:
            logger.warning(f"Backup cleanup failed: {e}")

    def _try_restore_backup(self, file_path: Path, default: Any) -> Any:
        """Try to restore data from the most recent backup"""
        try:
            # Find the most recent backup
            base_name = file_path.stem
            backup_pattern = f"{base_name}_*"
            backups = list(self.backup_dir.glob(backup_pattern))

            if not backups:
                logger.warning(f"No backups found for {file_path}")
                return default

            # Get the most recent backup
            latest_backup = max(backups, key=lambda x: x.stat().st_mtime)

            # Read from backup
            with open(latest_backup, "r", encoding="utf-8") as f:
                data = json.load(f)

            logger.info(f"Restored data from backup: {latest_backup}")
            return data

        except Exception as e:
            logger.error(f"Backup restoration failed: {e}")
            return default

    def get_file_integrity_info(self, file_path: Path) -> Dict[str, Any]:
        """Get integrity information for a file"""
        try:
            if not file_path.exists():
                return {"exists": False, "error": "File does not exist"}

            stat = file_path.stat()
            file_hash = hashlib.md5()

            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    file_hash.update(chunk)

            return {
                "exists": True,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "md5_hash": file_hash.hexdigest(),
                "permissions": oct(stat.st_mode)[-3:],
            }

        except Exception as e:
            return {"exists": False, "error": str(e)}

    def verify_data_integrity(self) -> Dict[str, Any]:
        """Verify integrity of all data files"""
        integrity_report = {
            "timestamp": datetime.now().isoformat(),
            "files_checked": 0,
            "files_valid": 0,
            "files_corrupted": 0,
            "backups_available": 0,
            "details": {},
        }

        try:
            # Check all JSON files in data directory
            for json_file in self.data_dir.rglob("*.json"):
                integrity_report["files_checked"] += 1

                # Try to read the file
                try:
                    data = self.safe_read_json(json_file, None)
                    if data is not None:
                        integrity_report["files_valid"] += 1
                        integrity_report["details"][str(json_file)] = {
                            "status": "valid",
                            "size": json_file.stat().st_size,
                        }
                    else:
                        integrity_report["files_corrupted"] += 1
                        integrity_report["details"][str(json_file)] = {
                            "status": "corrupted",
                            "error": "Failed to read JSON",
                        }

                except Exception as e:
                    integrity_report["files_corrupted"] += 1
                    integrity_report["details"][str(json_file)] = {
                        "status": "corrupted",
                        "error": str(e),
                    }

            # Count available backups
            integrity_report["backups_available"] = len(list(self.backup_dir.glob("*")))

        except Exception as e:
            integrity_report["error"] = str(e)

        return integrity_report


class HealthStatus:
    """Track system health status"""

    def __init__(self):
        self.start_time = datetime.now()
        self.last_heartbeat = datetime.now()
        self.ai_service_status = {}
        self.error_count = 0
        self.response_times = []
        self.memory_usage = []
        self.is_healthy = True
        self.health_issues = []

    def update_heartbeat(self):
        """Update last heartbeat timestamp"""
        self.last_heartbeat = datetime.now()

    def record_ai_response(self, service: str, response_time: float, success: bool):
        """Record AI service response"""
        if service not in self.ai_service_status:
            self.ai_service_status[service] = {
                "total_calls": 0,
                "successful_calls": 0,
                "avg_response_time": 0,
                "last_success": None,
                "last_failure": None,
            }

        status = self.ai_service_status[service]
        status["total_calls"] += 1

        if success:
            status["successful_calls"] += 1
            status["last_success"] = datetime.now().isoformat()
        else:
            status["last_failure"] = datetime.now().isoformat()
            self.error_count += 1

        # Update average response time
        if len(self.response_times) >= 10:
            self.response_times.pop(0)
        self.response_times.append(response_time)
        status["avg_response_time"] = sum(self.response_times) / len(
            self.response_times
        )

    def record_memory_usage(self):
        """Record current memory usage"""
        try:
            memory_info = psutil.virtual_memory()
            memory_data = {
                "timestamp": datetime.now().isoformat(),
                "percent": memory_info.percent,
                "available_gb": memory_info.available / (1024**3),
                "used_gb": memory_info.used / (1024**3),
            }

            if len(self.memory_usage) >= 60:  # Keep last 60 readings
                self.memory_usage.pop(0)
            self.memory_usage.append(memory_data)

        except Exception as e:
            logger.warning(f"Could not record memory usage: {e}")

    def check_health(self) -> bool:
        """Check overall system health"""
        issues = []

        # Check heartbeat age
        heartbeat_age = (datetime.now() - self.last_heartbeat).total_seconds()
        if heartbeat_age > 300:  # 5 minutes
            issues.append(f"Heartbeat stale ({heartbeat_age:.1f}s)")

        # Check memory usage
        if self.memory_usage:
            latest_memory = self.memory_usage[-1]["percent"]
            if latest_memory > 90:
                issues.append(f"High memory usage ({latest_memory:.1f}%)")

        # Check AI service health
        for service, status in self.ai_service_status.items():
            if status["total_calls"] > 0:
                success_rate = (
                    status["successful_calls"] / status["total_calls"]
                ) * 100
                if success_rate < 50:
                    issues.append(f"{service} success rate low ({success_rate:.1f}%)")

        # Check error rate
        uptime_hours = (datetime.now() - self.start_time).total_seconds() / 3600
        if uptime_hours > 1:  # Only check after 1 hour of operation
            error_rate = self.error_count / uptime_hours
            if error_rate > 10:  # More than 10 errors per hour
                issues.append(f"High error rate ({error_rate:.1f}/hour)")

        self.health_issues = issues
        self.is_healthy = len(issues) == 0
        return self.is_healthy

    def get_status_dict(self) -> Dict[str, Any]:
        """Get complete status as dictionary"""
        uptime = datetime.now() - self.start_time

        return {
            "healthy": self.is_healthy,
            "issues": self.health_issues,
            "uptime_seconds": int(uptime.total_seconds()),
            "uptime_human": str(uptime).split(".")[0],  # Remove microseconds
            "start_time": self.start_time.isoformat(),
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "heartbeat_age_seconds": int(
                (datetime.now() - self.last_heartbeat).total_seconds()
            ),
            "error_count": self.error_count,
            "ai_services": self.ai_service_status,
            "memory_usage_current": (
                self.memory_usage[-1] if self.memory_usage else None
            ),
            "avg_response_time": (
                sum(self.response_times) / len(self.response_times)
                if self.response_times
                else 0
            ),
        }


class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP handler for health check endpoints"""

    def __init__(self, *args, health_status=None, **kwargs):
        self.health_status = health_status
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == "/health":
                self._handle_health_check()
            elif self.path == "/status":
                self._handle_status_check()
            elif self.path == "/metrics":
                self._handle_metrics()
            else:
                self._send_response(404, {"error": "Not found"})
        except Exception as e:
            logger.error(f"Health check error: {e}")
            self._send_response(500, {"error": "Internal server error"})

    def _handle_health_check(self):
        """Handle basic health check"""
        if self.health_status:
            is_healthy = self.health_status.check_health()
            status_code = 200 if is_healthy else 503
            response = {
                "status": "healthy" if is_healthy else "unhealthy",
                "timestamp": datetime.now().isoformat(),
            }
            if not is_healthy:
                response["issues"] = self.health_status.health_issues
        else:
            status_code = 200
            response = {"status": "healthy", "timestamp": datetime.now().isoformat()}

        self._send_response(status_code, response)

    def _handle_status_check(self):
        """Handle detailed status check"""
        if self.health_status:
            status = self.health_status.get_status_dict()
        else:
            status = {"status": "no health monitoring available"}

        self._send_response(200, status)

    def _handle_metrics(self):
        """Handle metrics endpoint"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            metrics = {
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_available_gb": memory.available / (1024**3),
                    "disk_percent": disk.percent,
                    "disk_free_gb": disk.free / (1024**3),
                },
                "timestamp": datetime.now().isoformat(),
            }

            if self.health_status:
                metrics.update(self.health_status.get_status_dict())

            self._send_response(200, metrics)

        except Exception as e:
            logger.error(f"Metrics error: {e}")
            self._send_response(500, {"error": "Could not gather metrics"})

    def _send_response(self, status_code: int, data: Dict[str, Any]):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # CORS
        self.end_headers()

        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode("utf-8"))

    def log_message(self, format, *args):
        """Override to reduce log noise"""
        pass  # Disable default logging


class HealthMonitor:
    """Main health monitoring system"""

    def __init__(self, port: int = 8080):
        """Main health monitoring system"""
        self.port = port
        self.status = HealthStatus()
        # Webhook for health alerts
        self.alert_webhook: Optional[str] = os.getenv("LYRA_HEALTH_WEBHOOK_URL")
        self.server = None
        self.server_thread = None
        self.is_running = False

    def start(self):
        """Start health monitoring server"""
        try:
            # Find available port
            port = self._find_available_port(self.port)

            # Create handler with health status
            def handler(*args, **kwargs):
                return HealthCheckHandler(*args, health_status=self.status, **kwargs)

            self.server = HTTPServer(("localhost", port), handler)
            self.server_thread = Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            self.is_running = True

            logger.info(f"Health monitor started on http://localhost:{port}")
            logger.info(f"Endpoints: /health /status /metrics")

            # Start periodic monitoring
            asyncio.create_task(self._periodic_monitoring())

            return port

        except Exception as e:
            logger.error(f"Failed to start health monitor: {e}")
            return None

    def stop(self):
        """Stop health monitoring server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.is_running = False
            logger.info("Health monitor stopped")

    def _find_available_port(self, start_port: int) -> int:
        """Find an available port starting from start_port"""
        for port in range(start_port, start_port + 10):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(("localhost", port))
                    return port
            except socket.error:
                continue
        raise Exception("No available ports found")

    async def _periodic_monitoring(self):
        """Periodic monitoring tasks"""
        while self.is_running:
            try:
                # Update heartbeat
                self.status.update_heartbeat()

                # Record memory usage
                self.status.record_memory_usage()

                # Check health
                self.status.check_health()

                # Log health issues if any
                if not self.status.is_healthy:
                    issues = self.status.health_issues
                    logger.warning(f"Health issues detected: {issues}")
                    # Send webhook alert if configured
                    if self.alert_webhook:
                        await self._send_webhook_alert(issues)

                # Wait 30 seconds
                await asyncio.sleep(30)

            except Exception as e:
                logger.error(f"Monitoring error: {e}", exc_info=True)
                await asyncio.sleep(30)

    async def _send_webhook_alert(self, issues: list):
        """Send health issues alert to configured Discord webhook"""
        try:
            async with aiohttp.ClientSession() as session:
                content = f"⚠️ Health Alert: {', '.join(issues)}"
                await session.post(self.alert_webhook, json={"content": content})
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}", exc_info=True)

    def record_ai_call(self, service: str, response_time: float, success: bool):
        """Record AI service call"""
        self.status.record_ai_response(service, response_time, success)

    def get_health_summary(self) -> str:
        """Get simple health summary for Discord"""
        status = self.status.get_status_dict()

        if status["healthy"]:
            return f"✅ System healthy - Uptime: {status['uptime_human']}"
        else:
            issues = ", ".join(status["issues"])
            return f"⚠️ System issues - {issues}"


# Global health monitor instance
health_monitor = HealthMonitor()
