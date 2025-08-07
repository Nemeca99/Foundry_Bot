#!/usr/bin/env python3
"""
Queue System Monitoring Dashboard

This dashboard demonstrates the monitoring and alerting capabilities
of the queue system. It shows how to:
1. Register alert callbacks
2. Monitor system health in real-time
3. Display system statistics
4. Handle different types of alerts

Run this to see the monitoring system in action.
"""

import time
import threading
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add framework directory to path
framework_dir = Path(__file__).parent
sys.path.insert(0, str(framework_dir))

from queue_manager import queue_manager
from plugins.example_system import ExampleSystem


class MonitoringDashboard:
    """Simple monitoring dashboard for the queue system"""

    def __init__(self):
        self.alerts_received = []
        self.monitoring_active = False
        self.monitor_thread = None

        # Register alert callbacks
        queue_manager.register_alert_callback("warning", self._warning_callback)
        queue_manager.register_alert_callback("critical", self._critical_callback)

        print("🔍 Monitoring Dashboard Initialized")
        print("📊 Alert callbacks registered")

    def _warning_callback(self, alert_data: Dict[str, Any]):
        """Handle warning alerts"""
        self.alerts_received.append(alert_data)
        print(f"⚠️  WARNING: {alert_data['message']}")
        print(f"   System: {alert_data.get('system', 'unknown')}")
        print(
            f"   Time: {time.strftime('%H:%M:%S', time.localtime(alert_data['timestamp']))}"
        )

    def _critical_callback(self, alert_data: Dict[str, Any]):
        """Handle critical alerts"""
        self.alerts_received.append(alert_data)
        print(f"🚨 CRITICAL: {alert_data['message']}")
        print(f"   System: {alert_data.get('system', 'unknown')}")
        print(
            f"   Time: {time.strftime('%H:%M:%S', time.localtime(alert_data['timestamp']))}"
        )

    def start_monitoring(self):
        """Start the monitoring dashboard"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        # Start queue manager monitoring
        queue_manager.start_monitoring()

        print("🚀 Monitoring started")
        print("📈 Real-time statistics will be displayed")

    def stop_monitoring(self):
        """Stop the monitoring dashboard"""
        self.monitoring_active = False
        queue_manager.stop_monitoring()
        print("🛑 Monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Get global statistics
                stats = queue_manager.get_global_stats()

                # Display system health
                self._display_system_health(stats)

                # Display recent alerts
                if self.alerts_received:
                    self._display_recent_alerts()

                time.sleep(10)  # Update every 10 seconds

            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                time.sleep(1)

    def _display_system_health(self, stats: Dict[str, Any]):
        """Display system health information"""
        print("\n" + "=" * 60)
        print(f"📊 SYSTEM HEALTH REPORT - {time.strftime('%H:%M:%S')}")
        print("=" * 60)

        # Display global stats
        print(f"Total Items Processed: {stats['total_items_processed']}")
        print(f"Total Errors: {stats['total_errors']}")
        print(f"Systems Registered: {len(stats['system_health'])}")

        # Display system-specific stats
        print("\n🔧 SYSTEM STATUS:")
        for system_name, system_stats in stats["system_health"].items():
            status = "🟢" if system_stats["input_queue_size"] == 0 else "🟡"
            if system_stats["error_queue_size"] > 0:
                status = "🔴"

            print(f"  {status} {system_name}:")
            print(f"    Input Queue: {system_stats['input_queue_size']}")
            print(f"    Output Queue: {system_stats['output_queue_size']}")
            print(f"    Error Queue: {system_stats['error_queue_size']}")
            print(f"    Idle Time: {system_stats['idle_time']:.1f}s")

        # Display bottlenecks
        bottlenecks = stats.get("bottlenecks", [])
        if bottlenecks:
            print(f"\n⚠️  BOTTLENECKS DETECTED ({len(bottlenecks)}):")
            for bottleneck in bottlenecks:
                print(
                    f"  - {bottleneck['system']}: {bottleneck['type']} (size: {bottleneck['size']})"
                )
        else:
            print("\n✅ No bottlenecks detected")

    def _display_recent_alerts(self):
        """Display recent alerts"""
        if not self.alerts_received:
            return

        print(f"\n🚨 RECENT ALERTS ({len(self.alerts_received)}):")
        for alert in self.alerts_received[-5:]:  # Show last 5 alerts
            alert_type = "⚠️" if alert["type"] == "warning" else "🚨"
            time_str = time.strftime("%H:%M:%S", time.localtime(alert["timestamp"]))
            print(f"  {alert_type} {time_str}: {alert['message']}")

    def simulate_load(self):
        """Simulate high load to trigger alerts"""
        print("\n🧪 Simulating high load to test alerts...")

        # Create example system
        example_system = ExampleSystem()

        # Send many items to trigger queue alerts
        for i in range(25):
            example_system.send_to_system(
                "example_system",
                {
                    "type": "text_processing",
                    "text": f"Test message {i}",
                    "operation": "uppercase",
                    "request_id": f"load_test_{i}",
                },
            )
            time.sleep(0.1)  # Small delay

        print("✅ Load simulation completed")

    def clear_alerts(self):
        """Clear stored alerts"""
        self.alerts_received.clear()
        print("🧹 Alerts cleared")


def main():
    """Main monitoring dashboard"""
    print("🔍 Queue System Monitoring Dashboard")
    print("=" * 50)

    # Create dashboard
    dashboard = MonitoringDashboard()

    try:
        # Start monitoring
        dashboard.start_monitoring()

        # Give it a moment to initialize
        time.sleep(2)

        # Simulate some load to see alerts
        print("\n" + "=" * 50)
        print("🧪 DEMO: Simulating system load...")
        dashboard.simulate_load()

        # Let it run for a bit to see the monitoring in action
        print("\n📊 Monitoring for 30 seconds...")
        print("Press Ctrl+C to stop")

        time.sleep(30)

    except KeyboardInterrupt:
        print("\n🛑 Stopping monitoring...")
    finally:
        dashboard.stop_monitoring()

        # Final statistics
        print("\n📈 FINAL STATISTICS:")
        final_stats = queue_manager.get_global_stats()
        print(f"Total Items Processed: {final_stats['total_items_processed']}")
        print(f"Total Errors: {final_stats['total_errors']}")
        print(f"Alerts Received: {len(dashboard.alerts_received)}")

        # Clean up
        queue_manager.reset_all_queues()
        print("🧹 Cleanup completed")


if __name__ == "__main__":
    main()
