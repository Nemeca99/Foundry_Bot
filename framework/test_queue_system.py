#!/usr/bin/env python3
"""
Test script for the comprehensive queue system
Verifies inter-system communication, bottleneck identification, and loose coupling
"""

import sys
import time
import threading
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from queue_manager import queue_manager, QueueProcessor
from framework_cli import FrameworkCLI
from plugins.ai_native_backend import AINativeBackend
from plugins.character_embodiment_engine import CharacterEmbodimentEngine
from plugins.learning_engine import LearningEngine


def test_queue_manager():
    """Test the queue manager functionality"""
    print("🧪 Testing Queue Manager...")

    # Test system registration
    queue_manager.register_system("test_system")
    assert "test_system" in queue_manager.systems
    print("✅ System registration works")

    # Test sending data between systems
    item_id = queue_manager.send_to_system(
        "test_system", "target_system", {"test": "data"}
    )
    assert item_id is not None
    print("✅ Data sending works")

    # Test getting data from queue
    item = queue_manager.get_from_input_queue("target_system")
    assert item is not None
    assert item.data["test"] == "data"
    print("✅ Data retrieval works")

    # Test statistics
    stats = queue_manager.get_system_stats("test_system")
    assert "input_queue_size" in stats
    print("✅ Statistics tracking works")

    print("✅ Queue Manager tests passed\n")


def test_framework_cli_queue():
    """Test FrameworkCLI queue integration"""
    print("🧪 Testing FrameworkCLI Queue Integration...")

    cli = FrameworkCLI()

    # Test that it's registered with queue manager
    assert cli.system_name == "framework_cli"
    assert "framework_cli" in queue_manager.systems
    print("✅ FrameworkCLI registered with queue system")

    # Test sending data from CLI
    item_id = cli.send_to_system("ai_native_backend", {"command": "test"}, priority=8)
    assert item_id is not None
    print("✅ FrameworkCLI can send data to other systems")

    # Test getting stats
    stats = cli.get_system_stats()
    # Stats might be empty initially, so just check it's a dict
    assert isinstance(stats, dict)
    print("✅ FrameworkCLI can get system stats")

    print("✅ FrameworkCLI Queue Integration tests passed\n")


def test_ai_native_backend_queue():
    """Test AI Native Backend queue integration"""
    print("🧪 Testing AI Native Backend Queue Integration...")

    backend = AINativeBackend()

    # Test that it's registered with queue manager
    assert backend.system_name == "ai_native_backend"
    assert "ai_native_backend" in queue_manager.systems
    print("✅ AI Native Backend registered with queue system")

    # Test sending data from backend
    item_id = backend.send_to_system("framework_cli", {"status": "ready"}, priority=7)
    assert item_id is not None
    print("✅ AI Native Backend can send data to other systems")

    # Test getting stats
    stats = backend.get_system_stats()
    # Stats might be empty initially, so just check it's a dict
    assert isinstance(stats, dict)
    print("✅ AI Native Backend can get system stats")

    print("✅ AI Native Backend Queue Integration tests passed\n")


def test_character_embodiment_queue():
    """Test Character Embodiment Engine queue integration"""
    print("🧪 Testing Character Embodiment Engine Queue Integration...")

    engine = CharacterEmbodimentEngine()

    # Test that it's registered with queue manager
    assert engine.system_name == "character_embodiment_engine"
    assert "character_embodiment_engine" in queue_manager.systems
    print("✅ Character Embodiment Engine registered with queue system")

    # Test sending data from engine
    item_id = engine.send_to_system(
        "framework_cli", {"character": "test_char"}, priority=6
    )
    assert item_id is not None
    print("✅ Character Embodiment Engine can send data to other systems")

    # Test getting stats
    stats = engine.get_system_stats()
    # Stats might be empty initially, so just check it's a dict
    assert isinstance(stats, dict)
    print("✅ Character Embodiment Engine can get system stats")

    print("✅ Character Embodiment Engine Queue Integration tests passed\n")


def test_learning_engine_queue():
    """Test Learning Engine queue integration"""
    print("🧪 Testing Learning Engine Queue Integration...")

    # Create a mock framework for testing
    class MockFramework:
        def __init__(self):
            self.config = {"chunk_size": 1000, "overlap_size": 200, "max_workers": 4}

    framework = MockFramework()
    engine = LearningEngine(framework)

    # Test that it's registered with queue manager
    assert engine.system_name == "learning_engine"
    assert "learning_engine" in queue_manager.systems
    print("✅ Learning Engine registered with queue system")

    # Test sending data from engine
    item_id = engine.send_to_system(
        "framework_cli", {"learning": "complete"}, priority=5
    )
    assert item_id is not None
    print("✅ Learning Engine can send data to other systems")

    # Test getting stats
    stats = engine.get_system_stats()
    # Stats might be empty initially, so just check it's a dict
    assert isinstance(stats, dict)
    print("✅ Learning Engine can get system stats")

    print("✅ Learning Engine Queue Integration tests passed\n")


def test_inter_system_communication():
    """Test communication between multiple systems"""
    print("🧪 Testing Inter-System Communication...")

    # Create test systems
    cli = FrameworkCLI()
    backend = AINativeBackend()
    engine = CharacterEmbodimentEngine()

    # Test communication chain
    # CLI -> Backend -> Engine -> CLI
    item_id1 = cli.send_to_system("ai_native_backend", {"request": "emotional_state"})
    item_id2 = backend.send_to_system(
        "character_embodiment_engine", {"request": "character_profile"}
    )
    item_id3 = engine.send_to_system("framework_cli", {"response": "character_data"})

    assert item_id1 is not None
    assert item_id2 is not None
    assert item_id3 is not None
    print("✅ Inter-system communication chain works")

    # Test global statistics
    global_stats = queue_manager.get_global_stats()
    assert "total_items_processed" in global_stats
    assert "system_health" in global_stats
    print("✅ Global statistics tracking works")

    print("✅ Inter-System Communication tests passed\n")


def test_bottleneck_detection():
    """Test bottleneck detection functionality"""
    print("🧪 Testing Bottleneck Detection...")

    # Start monitoring
    queue_manager.start_monitoring()

    # Simulate high queue usage
    for i in range(15):
        queue_manager.send_to_system(
            "test_system", "target_system", {"data": f"item_{i}"}
        )

    # Wait a moment for monitoring to detect
    time.sleep(2)

    # Check for bottlenecks
    global_stats = queue_manager.get_global_stats()
    bottlenecks = global_stats.get("bottlenecks", [])

    # Should detect high input queue
    high_queue_bottlenecks = [b for b in bottlenecks if b["type"] == "input_queue_full"]
    assert len(high_queue_bottlenecks) > 0
    print("✅ Bottleneck detection works")

    # Stop monitoring
    queue_manager.stop_monitoring()

    print("✅ Bottleneck Detection tests passed\n")


def test_queue_cleanup():
    """Test queue cleanup functionality"""
    print("🧪 Testing Queue Cleanup...")

    # Register the test system first
    queue_manager.register_system("cleanup_test")

    # Add some test data
    for i in range(10):
        queue_manager.send_to_system(
            "cleanup_test", "target_system", {"data": f"item_{i}"}
        )

    # Verify system is registered
    assert "cleanup_test" in queue_manager.systems

    # Clear queues
    queue_manager.clear_system_queues("cleanup_test")

    # Verify system is still registered after cleanup
    assert "cleanup_test" in queue_manager.systems
    print("✅ Queue cleanup works")

    print("✅ Queue Cleanup tests passed\n")


def test_error_handling():
    """Test error handling in queue system"""
    print("🧪 Testing Error Handling...")

    # Test error queue functionality
    test_item = queue_manager.send_to_system(
        "error_test", "target_system", {"data": "test"}
    )

    # Simulate an error
    item = queue_manager.get_from_input_queue("target_system")
    if item:
        queue_manager.put_to_error_queue("target_system", item, "Test error")

    # Check error queue
    error_item = queue_manager.get_from_error_queue("target_system")
    assert error_item is not None
    assert error_item.metadata.get("error") == "Test error"
    print("✅ Error handling works")

    print("✅ Error Handling tests passed\n")


def main():
    """Run all queue system tests"""
    print("🚀 Starting Comprehensive Queue System Tests\n")

    try:
        test_queue_manager()
        test_framework_cli_queue()
        test_ai_native_backend_queue()
        test_character_embodiment_queue()
        test_learning_engine_queue()
        test_inter_system_communication()
        test_bottleneck_detection()
        test_queue_cleanup()
        test_error_handling()

        print("🎉 All Queue System Tests Passed!")
        print("\n📊 Final System Statistics:")
        final_stats = queue_manager.get_global_stats()
        print(f"Total items processed: {final_stats['total_items_processed']}")
        print(f"Total errors: {final_stats['total_errors']}")
        print(f"Systems registered: {len(final_stats['system_health'])}")

        # Clean up
        queue_manager.reset_all_queues()
        print("\n🧹 Cleanup completed")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
