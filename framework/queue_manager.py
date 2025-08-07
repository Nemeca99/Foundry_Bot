#!/usr/bin/env python3
"""
Comprehensive Queue Management System
Handles inter-system communication, bottleneck identification, and loose coupling

DEVELOPER GUIDE:
- To add queue processing to a new system, inherit from QueueProcessor
- Example: class MySystem(QueueProcessor):
- Call super().__init__("my_system_name") in __init__
- Override _process_item() to handle your specific data types
- Use send_to_system() to communicate with other systems
- Use get_system_stats() to monitor your system's health

MONITORING:
- Queue bottlenecks are automatically detected and logged
- High queue sizes (>10 items) trigger warnings
- System idle time (>5 minutes) triggers alerts
- Error queues are monitored for failed items
"""

import asyncio
import threading
import time
import logging
from queue import Queue, Empty
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QueueItem:
    """Standardized queue item with metadata"""

    id: str
    source_system: str
    target_system: str
    data: Any
    priority: int = 5  # 1-10, higher is more important
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemQueue:
    """Queue system for a specific component"""

    input_queue: Queue = field(default_factory=Queue)
    output_queue: Queue = field(default_factory=Queue)
    processing_queue: Queue = field(default_factory=Queue)
    error_queue: Queue = field(default_factory=Queue)
    stats: Dict[str, Any] = field(default_factory=dict)
    last_activity: float = field(default_factory=time.time)


class QueueManager:
    """Central queue management system for all components"""

    def __init__(self):
        self.systems: Dict[str, SystemQueue] = {}
        self.global_stats = {
            "total_items_processed": 0,
            "total_errors": 0,
            "average_processing_time": 0.0,
            "bottlenecks": [],
            "system_health": {},
        }
        self.monitoring_active = False
        self.monitor_thread = None

        # Monitoring configuration
        self.alert_thresholds = {
            "input_queue_warning": 10,
            "input_queue_critical": 20,
            "error_queue_warning": 5,
            "error_queue_critical": 10,
            "idle_time_warning": 300,  # 5 minutes
            "idle_time_critical": 600,  # 10 minutes
        }

        # Alert callbacks (can be set by external systems)
        self.alert_callbacks = {"warning": [], "critical": []}

    def register_system(self, system_name: str) -> SystemQueue:
        """Register a new system with its queues"""
        if system_name not in self.systems:
            self.systems[system_name] = SystemQueue()
            logger.info(f"Registered system: {system_name}")
        return self.systems[system_name]

    def get_system_queue(self, system_name: str) -> Optional[SystemQueue]:
        """Get queue system for a specific component"""
        return self.systems.get(system_name)

    def send_to_system(
        self,
        source_system: str,
        target_system: str,
        data: Any,
        priority: int = 5,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """Send data from one system to another"""
        if target_system not in self.systems:
            self.register_system(target_system)

        item = QueueItem(
            id=str(uuid.uuid4()),
            source_system=source_system,
            target_system=target_system,
            data=data,
            priority=priority,
            metadata=metadata or {},
        )

        target_queue = self.systems[target_system].input_queue
        target_queue.put(item)

        # Update stats
        self.global_stats["total_items_processed"] += 1
        self.systems[target_system].last_activity = time.time()

        logger.debug(f"Sent item {item.id} from {source_system} to {target_system}")
        return item.id

    def get_from_input_queue(
        self, system_name: str, timeout: float = 1.0
    ) -> Optional[QueueItem]:
        """Get next item from system's input queue"""
        if system_name not in self.systems:
            return None

        try:
            item = self.systems[system_name].input_queue.get(timeout=timeout)
            self.systems[system_name].last_activity = time.time()
            return item
        except Empty:
            return None

    def put_to_output_queue(self, system_name: str, item: QueueItem):
        """Put processed item to system's output queue"""
        if system_name not in self.systems:
            self.register_system(system_name)

        self.systems[system_name].output_queue.put(item)
        self.systems[system_name].last_activity = time.time()

    def get_from_output_queue(
        self, system_name: str, timeout: float = 1.0
    ) -> Optional[QueueItem]:
        """Get next item from system's output queue"""
        if system_name not in self.systems:
            return None

        try:
            item = self.systems[system_name].output_queue.get(timeout=timeout)
            return item
        except Empty:
            return None

    def put_to_error_queue(self, system_name: str, item: QueueItem, error: str):
        """Put failed item to system's error queue"""
        if system_name not in self.systems:
            self.register_system(system_name)

        item.metadata["error"] = error
        item.metadata["error_timestamp"] = time.time()
        self.systems[system_name].error_queue.put(item)
        self.global_stats["total_errors"] += 1

    def get_from_error_queue(
        self, system_name: str, timeout: float = 1.0
    ) -> Optional[QueueItem]:
        """Get next item from system's error queue"""
        if system_name not in self.systems:
            return None

        try:
            item = self.systems[system_name].error_queue.get(timeout=timeout)
            return item
        except Empty:
            return None

    def get_system_stats(self, system_name: str) -> Dict[str, Any]:
        """Get statistics for a specific system"""
        if system_name not in self.systems:
            return {}

        system = self.systems[system_name]
        return {
            "input_queue_size": system.input_queue.qsize(),
            "output_queue_size": system.output_queue.qsize(),
            "processing_queue_size": system.processing_queue.qsize(),
            "error_queue_size": system.error_queue.qsize(),
            "last_activity": system.last_activity,
            "idle_time": time.time() - system.last_activity,
        }

    def get_global_stats(self) -> Dict[str, Any]:
        """Get global system statistics"""
        system_stats = {}
        bottlenecks = []

        for system_name, system in self.systems.items():
            stats = self.get_system_stats(system_name)
            system_stats[system_name] = stats

            # Identify bottlenecks
            if stats["input_queue_size"] > 10:
                bottlenecks.append(
                    {
                        "system": system_name,
                        "type": "input_queue_full",
                        "size": stats["input_queue_size"],
                    }
                )

            if stats["error_queue_size"] > 5:
                bottlenecks.append(
                    {
                        "system": system_name,
                        "type": "error_queue_full",
                        "size": stats["error_queue_size"],
                    }
                )

            if stats["idle_time"] > 300:  # 5 minutes
                bottlenecks.append(
                    {
                        "system": system_name,
                        "type": "system_idle",
                        "idle_time": stats["idle_time"],
                    }
                )

        self.global_stats["bottlenecks"] = bottlenecks
        self.global_stats["system_health"] = system_stats

        return self.global_stats

    def start_monitoring(self):
        """Start the monitoring thread"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_systems, daemon=True
            )
            self.monitor_thread.start()
            logger.info("Queue monitoring started")

    def stop_monitoring(self):
        """Stop the monitoring thread"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        logger.info("Queue monitoring stopped")

    def _monitor_systems(self):
        """Monitor all systems for bottlenecks and issues"""
        while self.monitoring_active:
            try:
                stats = self.get_global_stats()

                # Check each system for issues
                for system_name, system_stats in stats["system_health"].items():
                    input_size = system_stats["input_queue_size"]
                    error_size = system_stats["error_queue_size"]
                    idle_time = system_stats["idle_time"]

                    # Check input queue thresholds
                    if input_size >= self.alert_thresholds["input_queue_critical"]:
                        self._trigger_alert(
                            "critical",
                            f"Critical input queue size for {system_name}: {input_size} items",
                            system_name,
                            {"queue_size": input_size},
                        )
                    elif input_size >= self.alert_thresholds["input_queue_warning"]:
                        self._trigger_alert(
                            "warning",
                            f"High input queue size for {system_name}: {input_size} items",
                            system_name,
                            {"queue_size": input_size},
                        )

                    # Check error queue thresholds
                    if error_size >= self.alert_thresholds["error_queue_critical"]:
                        self._trigger_alert(
                            "critical",
                            f"Critical error queue size for {system_name}: {error_size} items",
                            system_name,
                            {"error_count": error_size},
                        )
                    elif error_size >= self.alert_thresholds["error_queue_warning"]:
                        self._trigger_alert(
                            "warning",
                            f"High error queue size for {system_name}: {error_size} items",
                            system_name,
                            {"error_count": error_size},
                        )

                    # Check idle time thresholds
                    if idle_time >= self.alert_thresholds["idle_time_critical"]:
                        self._trigger_alert(
                            "critical",
                            f"System {system_name} has been idle for {idle_time:.1f} seconds",
                            system_name,
                            {"idle_time": idle_time},
                        )
                    elif idle_time >= self.alert_thresholds["idle_time_warning"]:
                        self._trigger_alert(
                            "warning",
                            f"System {system_name} has been idle for {idle_time:.1f} seconds",
                            system_name,
                            {"idle_time": idle_time},
                        )

                time.sleep(5)  # Check every 5 seconds

            except Exception as e:
                logger.error(f"Error in monitoring thread: {e}")
                time.sleep(1)

    def clear_system_queues(self, system_name: str):
        """Clear all queues for a specific system"""
        if system_name in self.systems:
            system = self.systems[system_name]

            # Clear all queues
            while not system.input_queue.empty():
                try:
                    system.input_queue.get_nowait()
                except Empty:
                    break

            while not system.output_queue.empty():
                try:
                    system.output_queue.get_nowait()
                except Empty:
                    break

            while not system.processing_queue.empty():
                try:
                    system.processing_queue.get_nowait()
                except Empty:
                    break

            while not system.error_queue.empty():
                try:
                    system.error_queue.get_nowait()
                except Empty:
                    break

            logger.info(f"Cleared all queues for system: {system_name}")

    def reset_all_queues(self):
        """Reset all queues in the system"""
        for system_name in list(self.systems.keys()):
            self.clear_system_queues(system_name)

        self.global_stats = {
            "total_items_processed": 0,
            "total_errors": 0,
            "average_processing_time": 0.0,
            "bottlenecks": [],
            "system_health": {},
        }

        logger.info("Reset all queues and statistics")

    def register_alert_callback(self, alert_type: str, callback: Callable):
        """Register a callback for alerts (warning/critical)"""
        if alert_type in self.alert_callbacks:
            self.alert_callbacks[alert_type].append(callback)
            logger.info(f"Registered {alert_type} alert callback")

    def _trigger_alert(
        self,
        alert_type: str,
        message: str,
        system_name: str = None,
        data: Dict[str, Any] = None,
    ):
        """Trigger an alert with optional callback execution"""
        alert_data = {
            "type": alert_type,
            "message": message,
            "system": system_name,
            "timestamp": time.time(),
            "data": data or {},
        }

        # Log the alert
        if alert_type == "warning":
            logger.warning(f"QUEUE ALERT: {message}")
        else:
            logger.error(f"QUEUE CRITICAL: {message}")

        # Execute callbacks
        for callback in self.alert_callbacks.get(alert_type, []):
            try:
                callback(alert_data)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")

    def set_alert_thresholds(self, thresholds: Dict[str, int]):
        """Update alert thresholds"""
        self.alert_thresholds.update(thresholds)
        logger.info(f"Updated alert thresholds: {thresholds}")


# Global queue manager instance
queue_manager = QueueManager()


class QueueProcessor:
    """Base class for systems that need queue processing capabilities"""

    def __init__(self, system_name: str):
        self.system_name = system_name
        self.queue_system = queue_manager.register_system(system_name)
        self.processing_active = False
        self.processing_thread = None

    def start_processing(self):
        """Start the processing thread"""
        if not self.processing_active:
            self.processing_active = True
            self.processing_thread = threading.Thread(
                target=self._process_loop, daemon=True
            )
            self.processing_thread.start()
            logger.info(f"Started processing for {self.system_name}")

    def stop_processing(self):
        """Stop the processing thread"""
        self.processing_active = False
        if self.processing_thread:
            self.processing_thread.join(timeout=1.0)
        logger.info(f"Stopped processing for {self.system_name}")

    def _process_loop(self):
        """Main processing loop - override in subclasses"""
        while self.processing_active:
            try:
                item = queue_manager.get_from_input_queue(self.system_name, timeout=1.0)
                if item:
                    self._process_item(item)
                time.sleep(0.1)  # Small delay to prevent busy waiting
            except Exception as e:
                logger.error(f"Error in processing loop for {self.system_name}: {e}")
                time.sleep(1)

    def _process_item(self, item: QueueItem):
        """Process a queue item - override in subclasses"""
        try:
            # Default processing - just pass through
            queue_manager.put_to_output_queue(self.system_name, item)
        except Exception as e:
            logger.error(f"Error processing item {item.id} in {self.system_name}: {e}")
            queue_manager.put_to_error_queue(self.system_name, item, str(e))

    def send_to_system(
        self,
        target_system: str,
        data: Any,
        priority: int = 5,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """Send data to another system"""
        return queue_manager.send_to_system(
            self.system_name, target_system, data, priority, metadata
        )

    def get_system_stats(self) -> Dict[str, Any]:
        """Get statistics for this system"""
        return queue_manager.get_system_stats(self.system_name)
