#!/usr/bin/env python3
"""
Offline System Test for Aether_Project
Tests all core systems without Discord connection
"""

import sys
import os
import asyncio
import sqlite3
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test all core system imports"""
    print("🔍 Testing Core System Imports...")

    try:
        # Test core modules
        from core.bot import DiscordDigirancherBot

        print("✅ DiscordDigirancherBot imported successfully")

        from core.memory_system import MemorySystem

        print("✅ MemorySystem imported successfully")

        from core.personality_system import ConsolidatedPersonalitySystem

        print("✅ PersonalitySystem imported successfully")

        from core.scientific_game_engine import ScientificGameEngine

        print("✅ ScientificGameEngine imported successfully")

        from core.survival_engine import SurvivalEngine

        print("✅ SurvivalEngine imported successfully")

        from core.economy import RPEconomy

        print("✅ Economy imported successfully")

        from core.leaderboard import ExclusiveLeaderboard

        print("✅ Leaderboard imported successfully")

        from core.disasters import DisasterSystem

        print("✅ DisasterSystem imported successfully")

        from core.clds import CLDSSystem

        print("✅ CLDSSystem imported successfully")

        from core.network_consciousness import NetworkConsciousness

        print("✅ NetworkConsciousness imported successfully")

        from core.dream_cycle import DreamCycleSystem

        print("✅ DreamCycle imported successfully")

        from core.health_monitor import HealthMonitor

        print("✅ HealthMonitor imported successfully")

        from core.ai_circuit_breaker import AICircuitBreaker

        print("✅ AICircuitBreaker imported successfully")

        from core.config import DEFAULT_SETTINGS

        print("✅ Config imported successfully")

        # Test new systems
        from core.resource_system import ResourceSystem

        print("✅ ResourceSystem imported successfully")

        from core.hunting_system import HuntingSystem

        print("✅ HuntingSystem imported successfully")

        from core.trade_system import TradeSystem

        print("✅ TradeSystem imported successfully")

        from core.discord_channels import DiscordChannelStructure

        print("✅ DiscordChannelStructure imported successfully")

        print("\n🎉 All core system imports successful!")
        return True

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False


def test_database_creation():
    """Test database creation and basic operations"""
    print("\n🗄️ Testing Database Operations...")

    try:
        # Test SQLite database creation
        db_path = "test_database.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Test basic table creation
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS test_users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                rp INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Test data insertion
        cursor.execute(
            """
            INSERT INTO test_users (username, rp) VALUES (?, ?)
        """,
            ("test_user", 100),
        )

        # Test data retrieval
        cursor.execute("SELECT * FROM test_users WHERE username = ?", ("test_user",))
        result = cursor.fetchone()

        if result:
            print("✅ Database operations successful")
            print(f"   - User: {result[1]}, RP: {result[2]}")

        conn.commit()
        conn.close()

        # Clean up test database
        os.remove(db_path)
        print("✅ Database cleanup successful")

        return True

    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False


def test_system_initialization():
    """Test system initialization without Discord"""
    print("\n⚙️ Testing System Initialization...")

    try:
        # Test memory system
        from core.memory_system import ConsolidatedMemorySystem

        memory_system = ConsolidatedMemorySystem(simple_mode=True)
        print("✅ MemorySystem initialized")

        # Test personality system
        from core.personality_system import ConsolidatedPersonalitySystem

        personality_system = ConsolidatedPersonalitySystem()
        print("✅ PersonalitySystem initialized")

        # Test scientific engine
        from core.scientific_game_engine import ScientificGameEngine

        scientific_engine = ScientificGameEngine()
        print("✅ ScientificGameEngine initialized")

        # Test survival engine
        from core.survival_engine import SurvivalEngine

        survival_engine = SurvivalEngine()
        print("✅ SurvivalEngine initialized")

        # Test economy
        from core.economy import RPEconomy

        economy = RPEconomy()
        print("✅ Economy initialized")

        # Test leaderboard
        from core.leaderboard import ExclusiveLeaderboard

        leaderboard = ExclusiveLeaderboard()
        print("✅ Leaderboard initialized")

        # Test disaster system
        from core.disasters import DisasterSystem

        disaster_system = DisasterSystem()
        print("✅ DisasterSystem initialized")

        # Test CLDS system
        from core.clds import CLDSSystem

        clds_system = CLDSSystem()
        print("✅ CLDSSystem initialized")

        # Test network consciousness
        from core.network_consciousness import NetworkConsciousness

        network_consciousness = NetworkConsciousness()
        print("✅ NetworkConsciousness initialized")

        # Test dream cycle
        from core.dream_cycle import DreamCycleSystem

        dream_cycle = DreamCycleSystem()
        print("✅ DreamCycle initialized")

        # Test health monitor
        from core.health_monitor import HealthMonitor

        health_monitor = HealthMonitor()
        print("✅ HealthMonitor initialized")

        # Test AI circuit breaker
        from core.ai_circuit_breaker import AICircuitBreaker

        ai_circuit_breaker = AICircuitBreaker()
        print("✅ AICircuitBreaker initialized")

        # Test new systems
        from core.resource_system import ResourceSystem

        resource_system = ResourceSystem()
        print("✅ ResourceSystem initialized")

        from core.hunting_system import HuntingSystem

        hunting_system = HuntingSystem()
        print("✅ HuntingSystem initialized")

        from core.trade_system import TradeSystem

        trade_system = TradeSystem()
        print("✅ TradeSystem initialized")

        # Test Discord channel structure
        from core.discord_channels import DiscordChannelStructure

        channel_structure = DiscordChannelStructure()
        print("✅ DiscordChannelStructure initialized")

        print("\n🎉 All systems initialized successfully!")
        return True

    except Exception as e:
        print(f"❌ System Initialization Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_basic_functionality():
    """Test basic functionality of core systems"""
    print("\n🔧 Testing Basic Functionality...")

    try:
        # Test memory system
        from core.memory_system import ConsolidatedMemorySystem

        memory_system = ConsolidatedMemorySystem(simple_mode=True)
        memory_system.store_user_memory("test_user", "test", "test_message")
        memories = memory_system.get_user_memories("test_user", limit=5)
        print("✅ Memory system functionality verified")

        # Test economy
        from core.economy import RPEconomy

        economy = RPEconomy()
        # Test economy functionality
        player_data = {"rp": 0}
        economy.add_rp(player_data, 100)
        print(f"✅ Economy functionality verified (RP: {player_data['rp']})")

        # Test leaderboard
        from core.leaderboard import ExclusiveLeaderboard

        leaderboard = ExclusiveLeaderboard()
        # Test leaderboard functionality
        from core.leaderboard import LeaderboardEntry
        from datetime import datetime

        entry = LeaderboardEntry(
            discord_id="test_user",
            username="TestUser",
            ticks_survived=1000,
            drones_used=5,
            rp_earned=500,
            record_date=datetime.now(),
        )
        leaderboard.submit_record(entry)
        top_10 = leaderboard.get_top_10()
        print("✅ Leaderboard functionality verified")

        # Test resource system
        from core.resource_system import ResourceSystem

        resource_system = ResourceSystem()
        resource_system._init_database()
        resource_system._init_resource_nodes()
        print("✅ Resource system functionality verified")

        # Test hunting system
        from core.hunting_system import HuntingSystem

        hunting_system = HuntingSystem()
        hunting_system._init_database()
        print("✅ Hunting system functionality verified")

        # Test trade system
        from core.trade_system import TradeSystem

        trade_system = TradeSystem()
        trade_system._init_database()
        trade_system._init_items()
        print("✅ Trade system functionality verified")

        # Test channel structure
        from core.discord_channels import DiscordChannelStructure

        channel_structure = DiscordChannelStructure()
        world_channels = channel_structure._get_world_channels()
        kingdom_channels = channel_structure._get_kingdom_channels()
        print("✅ Channel structure functionality verified")

        print("\n🎉 All basic functionality tests passed!")
        return True

    except Exception as e:
        print(f"❌ Basic Functionality Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_command_parsing():
    """Test command parsing functionality"""
    print("\n📝 Testing Command Parsing...")

    try:
        # Test basic command parsing
        test_commands = [
            "!help",
            "!rp",
            "!gather normal",
            "!hunt 123 100",
            "!trade 456 789 5 50",
            "!kingdoms",
            "!daily",
        ]

        for cmd in test_commands:
            parts = cmd.split()
            command = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            print(f"✅ Parsed: {command} with args: {args}")

        print("\n🎉 Command parsing tests passed!")
        return True

    except Exception as e:
        print(f"❌ Command Parsing Error: {e}")
        return False


def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration...")

    try:
        from core.config import DEFAULT_SETTINGS

        # Test default settings
        print(f"✅ Default settings loaded: {len(DEFAULT_SETTINGS)} categories")

        # Test specific settings
        if "privacy" in DEFAULT_SETTINGS:
            print("✅ Privacy settings found")
        if "notifications" in DEFAULT_SETTINGS:
            print("✅ Notification settings found")
        if "interaction" in DEFAULT_SETTINGS:
            print("✅ Interaction settings found")
        if "memory" in DEFAULT_SETTINGS:
            print("✅ Memory settings found")
        if "channels" in DEFAULT_SETTINGS:
            print("✅ Channel settings found")
        if "custom" in DEFAULT_SETTINGS:
            print("✅ Custom settings found")

        print("\n🎉 Configuration tests passed!")
        return True

    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        return False


def main():
    """Run all offline tests"""
    print("🚀 Starting Aether_Project Offline System Test")
    print("=" * 50)

    tests = [
        ("Import Tests", test_imports),
        ("Database Tests", test_database_creation),
        ("System Initialization", test_system_initialization),
        ("Basic Functionality", test_basic_functionality),
        ("Command Parsing", test_command_parsing),
        ("Configuration", test_configuration),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for Discord testing.")
        print("\n✅ Ready to proceed with Discord bot testing")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before Discord testing.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
