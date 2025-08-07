#!/usr/bin/env python3
"""
Example System - Demonstrates Queue System Best Practices

This is a simple example system that shows how to:
1. Inherit from QueueProcessor
2. Handle different data types
3. Implement request-response patterns
4. Use proper error handling
5. Monitor system health

Use this as a template when creating new systems.
"""

import time
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add framework directory to path for imports
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

from queue_manager import QueueProcessor

logger = logging.getLogger(__name__)


class ExampleSystem(QueueProcessor):
    """
    Example system demonstrating queue system best practices

    This system processes different types of data and demonstrates
    common patterns like request-response and data transformation.
    """

    def __init__(self):
        # Always call super().__init__ with your system name
        super().__init__("example_system")

        # Initialize your system's data
        self.processed_items = 0
        self.error_count = 0
        self.last_activity = time.time()

        # System-specific configuration
        self.config = {
            "max_processing_time": 5.0,  # seconds
            "enable_logging": True,
            "auto_cleanup": True,
        }

        logger.info(f"ExampleSystem initialized with config: {self.config}")

    def _process_item(self, item):
        """
        Override this method to handle your specific data types

        This is the main processing method that gets called for each
        item in your input queue.
        """
        try:
            # Update activity timestamp
            self.last_activity = time.time()

            # Get the data type to determine processing strategy
            data_type = item.data.get("type", "unknown")

            if data_type == "text_processing":
                self._process_text(item)
            elif data_type == "data_transformation":
                self._process_transformation(item)
            elif data_type == "request":
                self._handle_request(item)
            elif data_type == "status_check":
                self._handle_status_check(item)
            else:
                # Pass unknown types to base class
                logger.warning(
                    f"Unknown data type '{data_type}', passing to base class"
                )
                super()._process_item(item)

        except Exception as e:
            self.error_count += 1
            logger.error(f"Error processing item {item.id}: {e}")
            # Re-raise to let base class handle error queue
            raise

    def _process_text(self, item):
        """Process text data - demonstrates simple data processing"""
        try:
            text = item.data.get("text", "")
            operation = item.data.get("operation", "uppercase")

            # Perform the requested operation
            if operation == "uppercase":
                result = text.upper()
            elif operation == "lowercase":
                result = text.lower()
            elif operation == "reverse":
                result = text[::-1]
            else:
                result = f"Unknown operation: {operation}"

            # Send result back to requesting system
            self.send_to_system(
                "framework_cli",
                {
                    "type": "text_result",
                    "original_text": text,
                    "operation": operation,
                    "result": result,
                    "request_id": item.data.get("request_id"),
                },
            )

            self.processed_items += 1
            logger.info(f"Processed text item: {operation} -> {len(result)} chars")

        except Exception as e:
            logger.error(f"Error in text processing: {e}")
            raise

    def _process_transformation(self, item):
        """Process data transformation - demonstrates complex processing"""
        try:
            data = item.data.get("data", {})
            transform_type = item.data.get("transform_type", "none")

            # Perform transformation based on type
            if transform_type == "add_timestamp":
                transformed_data = {
                    **data,
                    "timestamp": time.time(),
                    "processed_by": "example_system",
                }
            elif transform_type == "calculate_stats":
                if isinstance(data, list):
                    transformed_data = {
                        "count": len(data),
                        "sum": (
                            sum(data)
                            if all(isinstance(x, (int, float)) for x in data)
                            else None
                        ),
                        "average": (
                            sum(data) / len(data)
                            if all(isinstance(x, (int, float)) for x in data)
                            else None
                        ),
                    }
                else:
                    transformed_data = {
                        "error": "Data must be a list for stats calculation"
                    }
            else:
                transformed_data = {
                    "error": f"Unknown transform type: {transform_type}"
                }

            # Send result
            self.send_to_system(
                "framework_cli",
                {
                    "type": "transformation_result",
                    "original_data": data,
                    "transform_type": transform_type,
                    "result": transformed_data,
                    "request_id": item.data.get("request_id"),
                },
            )

            self.processed_items += 1
            logger.info(f"Processed transformation: {transform_type}")

        except Exception as e:
            logger.error(f"Error in transformation processing: {e}")
            raise

    def _handle_request(self, item):
        """Handle requests - demonstrates request-response pattern"""
        try:
            request_type = item.data.get("request_type", "unknown")
            request_data = item.data.get("request_data", {})

            # Process different request types
            if request_type == "get_stats":
                response_data = self._get_system_stats()
            elif request_type == "get_config":
                response_data = self.config
            elif request_type == "update_config":
                new_config = request_data.get("config", {})
                self.config.update(new_config)
                response_data = {"status": "updated", "new_config": self.config}
            else:
                response_data = {"error": f"Unknown request type: {request_type}"}

            # Send response back to requesting system
            self.send_to_system(
                "framework_cli",
                {
                    "type": "response",
                    "request_id": item.data.get("request_id"),
                    "request_type": request_type,
                    "response_data": response_data,
                },
            )

            self.processed_items += 1
            logger.info(f"Handled request: {request_type}")

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            raise

    def _handle_status_check(self, item):
        """Handle status checks - demonstrates health monitoring"""
        try:
            current_time = time.time()
            idle_time = current_time - self.last_activity

            status_data = {
                "system_name": "example_system",
                "status": "healthy" if idle_time < 60 else "idle",
                "processed_items": self.processed_items,
                "error_count": self.error_count,
                "last_activity": self.last_activity,
                "idle_time": idle_time,
                "config": self.config,
            }

            # Send status back
            self.send_to_system(
                "framework_cli",
                {
                    "type": "status_response",
                    "status_data": status_data,
                    "request_id": item.data.get("request_id"),
                },
            )

            logger.info(f"Status check: {status_data['status']}")

        except Exception as e:
            logger.error(f"Error in status check: {e}")
            raise

    def _get_system_stats(self) -> Dict[str, Any]:
        """Get internal system statistics"""
        current_time = time.time()
        return {
            "processed_items": self.processed_items,
            "error_count": self.error_count,
            "last_activity": self.last_activity,
            "idle_time": current_time - self.last_activity,
            "uptime": current_time - self.last_activity,
            "config": self.config,
        }

    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status for monitoring"""
        stats = self._get_system_stats()

        # Determine health based on various factors
        health_status = "healthy"
        issues = []

        if stats["error_count"] > 10:
            health_status = "warning"
            issues.append("High error count")

        if stats["idle_time"] > 300:  # 5 minutes
            health_status = "idle"
            issues.append("System idle")

        return {"status": health_status, "issues": issues, "stats": stats}


# Example usage and testing
def test_example_system():
    """Test the example system functionality"""
    print("🧪 Testing Example System...")

    # Create the system
    system = ExampleSystem()

    # Test text processing
    system.send_to_system(
        "example_system",
        {
            "type": "text_processing",
            "text": "Hello World",
            "operation": "uppercase",
            "request_id": "test_1",
        },
    )

    # Test data transformation
    system.send_to_system(
        "example_system",
        {
            "type": "data_transformation",
            "data": [1, 2, 3, 4, 5],
            "transform_type": "calculate_stats",
            "request_id": "test_2",
        },
    )

    # Test request handling
    system.send_to_system(
        "example_system",
        {"type": "request", "request_type": "get_stats", "request_id": "test_3"},
    )

    # Test status check
    system.send_to_system(
        "example_system", {"type": "status_check", "request_id": "test_4"}
    )

    print("✅ Example system tests sent")

    # Wait a moment for processing
    time.sleep(2)

    # Check system health
    health = system.get_health_status()
    print(f"System Health: {health['status']}")
    print(f"Processed Items: {health['stats']['processed_items']}")

    return system


if __name__ == "__main__":
    # Run the test
    test_system = test_example_system()
    print("✅ Example system test completed")
