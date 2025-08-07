#!/usr/bin/env python3
"""
Comprehensive Queue System Integration Test
Tests queue system integration for Discord bots, emotional systems, and scripts
"""

import sys
import time
import uuid
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from framework.queue_manager import QueueManager, QueueItem


def test_discord_bots_queue_integration():
    """Test queue integration for Discord bots"""
    print("🧪 Testing Discord bots queue integration...")

    try:
        # Test AuthoringBot queue integration
        from discord.authoring_bot import AuthoringBot

        authoring_bot = AuthoringBot()

        # Test queue processing
        test_item = QueueItem(
            id=str(uuid.uuid4()),
            source_system="test_system",
            target_system="authoring_bot",
            data={
                "type": "discord_command",
                "command": "test_command",
                "args": {"test": "data"},
                "user_id": "test_user",
            },
            priority=1,
        )

        result = authoring_bot._process_item(test_item)
        assert isinstance(result, dict)
        assert "status" in result
        print("✅ AuthoringBot queue integration test passed")

        # Test CharacterSystemBot queue integration
        from discord.character_system_bot import CharacterSystemBot

        character_bot = CharacterSystemBot()

        # Test queue processing
        test_item = QueueItem(
            id=str(uuid.uuid4()),
            source_system="test_system",
            target_system="character_system_bot",
            data={
                "type": "character_embodiment",
                "operation": "embody",
                "character_name": "test_character",
                "content": "test content",
            },
            priority=1,
        )

        result = character_bot._process_item(test_item)
        assert isinstance(result, dict)
        assert "status" in result
        print("✅ CharacterSystemBot queue integration test passed")

        return True
    except Exception as e:
        print(f"❌ Discord bots queue integration test failed: {e}")
        return False


def test_emotional_systems_queue_integration():
    """Test queue integration for emotional systems"""
    print("🧪 Testing emotional systems queue integration...")

    try:
        # Test EnhancedEmotionalMeter queue integration
        from astra_emotional_fragments.enhanced_emotional_meter import (
            EnhancedEmotionalMeter,
        )

        emotional_meter = EnhancedEmotionalMeter()

        # Test queue processing
        test_item = QueueItem(
            id=str(uuid.uuid4()),
            source_system="test_system",
            target_system="enhanced_emotional_meter",
            data={
                "type": "emotion_update",
                "update_type": "interaction",
                "interaction_type": "romantic",
                "intensity": 0.3,
            },
            priority=1,
        )

        result = emotional_meter._process_item(test_item)
        assert isinstance(result, dict)
        assert "status" in result
        print("✅ EnhancedEmotionalMeter queue integration test passed")

        # Test EnhancedDynamicEmotionEngine queue integration
        from astra_emotional_fragments.dynamic_emotion_engine import (
            EnhancedDynamicEmotionEngine,
        )

        emotion_engine = EnhancedDynamicEmotionEngine()

        # Test queue processing
        test_item = QueueItem(
            id=str(uuid.uuid4()),
            source_system="test_system",
            target_system="enhanced_dynamic_emotion_engine",
            data={
                "type": "emotion_transition",
                "transition_type": "context_switch",
                "user_message": "test message",
                "previous_context": "previous",
            },
            priority=1,
        )

        result = emotion_engine._process_item(test_item)
        assert isinstance(result, dict)
        assert "status" in result
        print("✅ EnhancedDynamicEmotionEngine queue integration test passed")

        return True
    except Exception as e:
        print(f"❌ Emotional systems queue integration test failed: {e}")
        return False


def test_scripts_queue_integration():
    """Test queue integration for scripts"""
    print("🧪 Testing scripts queue integration...")

    try:
        # Test BotLauncher queue integration
        from scripts.start_bot import BotLauncher

        bot_launcher = BotLauncher()

        # Test queue processing
        test_item = QueueItem(
            id=str(uuid.uuid4()),
            source_system="test_system",
            target_system="bot_launcher",
            data={"type": "bot_status"},
            priority=1,
        )

        result = bot_launcher._process_item(test_item)
        assert isinstance(result, dict)
        assert "status" in result
        print("✅ BotLauncher queue integration test passed")

        return True
    except Exception as e:
        print(f"❌ Scripts queue integration test failed: {e}")
        return False


def test_inter_system_communication():
    """Test communication between different systems via queues"""
    print("🧪 Testing inter-system communication...")

    try:
        from framework.queue_manager import QueueManager

        queue_manager = QueueManager()

        # Register systems
        queue_manager.register_system("authoring_bot")
        queue_manager.register_system("character_system_bot")
        queue_manager.register_system("enhanced_emotional_meter")
        queue_manager.register_system("enhanced_dynamic_emotion_engine")
        queue_manager.register_system("bot_launcher")

        # Test sending items between systems
        test_item = QueueItem(
            id=str(uuid.uuid4()),
            source_system="test_system",
            target_system="enhanced_emotional_meter",
            data={
                "type": "interaction",
                "interaction_type": "romantic",
                "intensity": 0.3,
            },
            priority=1,
        )

        # Send to emotional meter
        queue_manager.send_to_system(
            "test_system", "enhanced_emotional_meter", test_item.data
        )

        # Get stats to verify
        stats = queue_manager.get_system_stats("enhanced_emotional_meter")
        assert isinstance(stats, dict)

        print("✅ Inter-system communication test passed")
        return True
    except Exception as e:
        print(f"❌ Inter-system communication test failed: {e}")
        return False


def test_queue_monitoring():
    """Test queue monitoring and alerting"""
    print("🧪 Testing queue monitoring...")

    try:
        from framework.queue_manager import QueueManager

        queue_manager = QueueManager()

        # Set alert thresholds
        queue_manager.set_alert_thresholds(
            {
                "input_queue_warning": 10,
                "input_queue_critical": 20,
                "error_queue_warning": 5,
                "error_queue_critical": 10,
                "idle_time_warning": 300,
                "idle_time_critical": 600,
            }
        )

        # Register alert callback
        def test_alert(alert_type, message, system_name=None, data=None):
            print(f"Alert: {system_name} - {alert_type}: {message}")

        queue_manager.register_alert_callback("warning", test_alert)

        # Register test system
        queue_manager.register_system("test_system")

        # Add items to trigger monitoring
        for i in range(15):
            test_item = QueueItem(
                id=str(uuid.uuid4()),
                source_system="test_system",
                target_system="test_system",
                data={"index": i},
                priority=1,
            )
            queue_manager.send_to_system("test_system", "test_system", test_item.data)

        # Wait for processing
        time.sleep(1)

        # Get monitoring stats
        stats = queue_manager.get_system_stats("test_system")
        assert isinstance(stats, dict)

        print("✅ Queue monitoring test passed")
        return True
    except Exception as e:
        print(f"❌ Queue monitoring test failed: {e}")
        return False


def test_error_handling():
    """Test error handling in queue systems"""
    print("🧪 Testing error handling...")

    try:
        from framework.queue_manager import QueueManager

        queue_manager = QueueManager()

        # Register test system
        queue_manager.register_system("error_test_system")

        # Send item with invalid data
        test_item = QueueItem(
            id=str(uuid.uuid4()),
            source_system="test_system",
            target_system="error_test_system",
            data={"invalid": "data"},
            priority=1,
        )

        queue_manager.send_to_system("test_system", "error_test_system", test_item.data)

        # Wait for processing
        time.sleep(1)

        # Check that system is still running
        stats = queue_manager.get_system_stats("error_test_system")
        assert isinstance(stats, dict)

        print("✅ Error handling test passed")
        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


def main():
    """Run all comprehensive queue integration tests"""
    print("🚀 Starting Comprehensive Queue System Integration Tests")
    print("=" * 60)

    tests = [
        test_discord_bots_queue_integration,
        test_emotional_systems_queue_integration,
        test_scripts_queue_integration,
        test_inter_system_communication,
        test_queue_monitoring,
        test_error_handling,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            print()

    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All comprehensive queue integration tests passed!")
        return True
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
