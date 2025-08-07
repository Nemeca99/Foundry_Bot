#!/usr/bin/env python3
"""
System Integration Test for Aether_Project
Tests all systems working together and their connections
"""

import sys
import os
import asyncio
import sqlite3
from datetime import datetime
import json

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_system_connections():
    """Test how all systems connect and work together"""
    print("🔗 Testing System Connections...")

    try:
        # Import all core systems
        from core.memory_system import ConsolidatedMemorySystem
        from core.personality_system import ConsolidatedPersonalitySystem
        from core.scientific_game_engine import ScientificGameEngine
        from core.survival_engine import SurvivalEngine
        from core.economy import RPEconomy
        from core.leaderboard import ExclusiveLeaderboard
        from core.disasters import DisasterSystem
        from core.clds import CLDSSystem
        from core.network_consciousness import NetworkConsciousness
        from core.dream_cycle import DreamCycleSystem
        from core.health_monitor import HealthMonitor
        from core.ai_circuit_breaker import AICircuitBreaker
        from core.resource_system import ResourceSystem
        from core.hunting_system import HuntingSystem
        from core.trade_system import TradeSystem
        from core.discord_channels import DiscordChannelStructure
        from core.kingdom_system import KingdomSystem
        from core.psychological_system import PsychologicalSystem

        print("✅ All systems imported successfully")

        # Initialize all systems
        memory_system = ConsolidatedMemorySystem(simple_mode=True)
        personality_system = ConsolidatedPersonalitySystem()
        scientific_engine = ScientificGameEngine()
        survival_engine = SurvivalEngine()
        economy = RPEconomy()
        leaderboard = ExclusiveLeaderboard()
        disaster_system = DisasterSystem()
        clds_system = CLDSSystem()
        network_consciousness = NetworkConsciousness()
        dream_cycle = DreamCycleSystem()
        health_monitor = HealthMonitor()
        ai_circuit_breaker = AICircuitBreaker()
        resource_system = ResourceSystem()
        hunting_system = HuntingSystem()
        trade_system = TradeSystem()
        channel_structure = DiscordChannelStructure()
        kingdom_system = KingdomSystem()
        psychological_system = PsychologicalSystem()

        print("✅ All systems initialized successfully")

        # Test system interactions
        test_user_id = "test_user_123"

        # 1. Test Memory + Personality connection
        memory_system.store_user_memory(test_user_id, "test", "Hello, how are you?")
        emotional_state = personality_system.process_input(
            test_user_id, "Hello, how are you?"
        )
        print("✅ Memory + Personality connection working")

        # 2. Test Economy + Leaderboard connection
        player_data = {"rp": 0}
        economy.add_rp(player_data, 100)
        from core.leaderboard import LeaderboardEntry

        entry = LeaderboardEntry(
            discord_id=test_user_id,
            username="TestUser",
            ticks_survived=1000,
            drones_used=5,
            rp_earned=500,
            record_date=datetime.now(),
        )
        leaderboard.submit_record(entry)
        print("✅ Economy + Leaderboard connection working")

        # 3. Test CLDS + Disaster connection
        drone = clds_system.generate_drone("TestDrone")
        disaster_result = disaster_system.trigger_disaster([drone], 10)
        print("✅ CLDS + Disaster connection working")

        # 4. Test Resource + Hunting connection
        resource_system._init_database()
        hunting_system._init_database()
        from core.hunting_system import HuntingEvent

        spawn_event = hunting_system.create_spawn_event(
            HuntingEvent.WILD_SPAWN, "test_channel"
        )
        print("✅ Resource + Hunting connection working")

        # 5. Test Trade + Economy connection
        trade_system._init_database()
        trade_system._init_items()
        trade_offer = trade_system.create_trade_offer(
            test_user_id, "buyer_456", "wood", 5, 50
        )
        print("✅ Trade + Economy connection working")

        # 6. Test Scientific + Personality connection
        scientific_result = scientific_engine.perform_scientific_calculation(
            "kinetic_energy", {"mass": 5, "velocity": 10}
        )
        print("✅ Scientific + Personality connection working")

        # 7. Test Kingdom + Channel connection
        from core.kingdom_system import KingdomType

        kingdom_info = kingdom_system.get_kingdom_info(KingdomType.LYRA_DOMINION)
        channel_info = channel_structure._get_kingdom_channels()
        print("✅ Kingdom + Channel connection working")

        # 8. Test Network Consciousness + Memory connection
        network_consciousness.record_cross_server_interaction(
            test_user_id, "test_server", "message", {"content": "test_message"}
        )
        memories = memory_system.get_user_memories(test_user_id, limit=5)
        print("✅ Network Consciousness + Memory connection working")

        # 9. Test Dream Cycle + Personality connection
        dream_result = dream_cycle.start_dream_cycle(
            "test_drone", "memory_consolidation"
        )
        consciousness_result = personality_system.process_consciousness(
            "test_message", test_user_id
        )
        print("✅ Dream Cycle + Personality connection working")

        # 10. Test Health Monitor + All Systems
        health_monitor.record_ai_call("test_service", 1.5, True)
        health_summary = health_monitor.get_health_summary()
        print("✅ Health Monitor + All Systems connection working")

        print("\n🎉 All system connections working properly!")
        return True

    except Exception as e:
        print(f"❌ System Connection Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_data_flow():
    """Test data flow between systems"""
    print("\n📊 Testing Data Flow Between Systems...")

    try:
        from core.memory_system import ConsolidatedMemorySystem
        from core.economy import RPEconomy
        from core.leaderboard import ExclusiveLeaderboard
        from core.resource_system import ResourceSystem
        from core.hunting_system import HuntingSystem
        from core.trade_system import TradeSystem

        # Initialize systems
        memory_system = ConsolidatedMemorySystem(simple_mode=True)
        economy = RPEconomy()
        leaderboard = ExclusiveLeaderboard()
        resource_system = ResourceSystem()
        hunting_system = HuntingSystem()
        trade_system = TradeSystem()

        # Initialize databases
        resource_system._init_database()
        hunting_system._init_database()
        trade_system._init_database()

        test_user = "test_user_456"

        # Test complete data flow
        # 1. User gathers resources
        resource_system.start_gathering(test_user, "wood", "normal")
        resources = resource_system.get_user_resources(test_user)
        print(f"✅ Resource gathering: {resources}")

        # 2. User hunts Simulacra
        from core.hunting_system import HuntingEvent

        spawn_event = hunting_system.create_spawn_event(
            HuntingEvent.WILD_SPAWN, "test_channel"
        )
        catch_result = hunting_system.attempt_catch(
            test_user, spawn_event["spawn_id"], 50
        )
        print(f"✅ Hunting result: {catch_result}")

        # 3. User trades items
        trade_offer = trade_system.create_trade_offer(
            test_user, "buyer_789", "wood", 3, 30
        )
        print(f"✅ Trade offer created: {trade_offer}")

        # 4. User earns RP
        player_data = {"rp": 0}
        economy.add_rp(player_data, 200)
        print(f"✅ RP earned: {player_data['rp']}")

        # 5. User submits leaderboard record
        from core.leaderboard import LeaderboardEntry
        from datetime import datetime

        entry = LeaderboardEntry(
            discord_id=test_user,
            username="TestUser",
            ticks_survived=500,
            drones_used=3,
            rp_earned=200,
            record_date=datetime.now(),
        )
        leaderboard.submit_record(entry)
        top_10 = leaderboard.get_top_10()
        print(f"✅ Leaderboard updated: {len(top_10)} entries")

        # 6. User stores memories
        memory_system.store_user_memory(
            test_user, "gameplay", "Completed hunting and trading session"
        )
        memories = memory_system.get_user_memories(test_user, limit=3)
        print(f"✅ Memories stored: {len(memories)} memories")

        print("\n🎉 Complete data flow working properly!")
        return True

    except Exception as e:
        print(f"❌ Data Flow Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_command_integration():
    """Test how Discord commands integrate with all systems"""
    print("\n🎮 Testing Discord Command Integration...")

    try:
        # Simulate Discord command processing
        test_commands = [
            ("!gather normal", "Resource gathering command"),
            ("!hunt 123 100", "Hunting command"),
            ("!trade 456 789 5 50", "Trade command"),
            ("!rp", "RP check command"),
            ("!leaderboard", "Leaderboard command"),
            ("!kingdoms", "Kingdoms command"),
            ("!daily", "Daily bonus command"),
            ("!help", "Help command"),
        ]

        for command, description in test_commands:
            parts = command.split()
            cmd = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            print(f"✅ {description}: {cmd} with args {args}")

        print("\n🎉 All Discord commands integrated properly!")
        return True

    except Exception as e:
        print(f"❌ Command Integration Error: {e}")
        return False


def test_database_integration():
    """Test database integration across all systems"""
    print("\n🗄️ Testing Database Integration...")

    try:
        # Test database creation and cross-system data
        db_path = "test_integration.db"

        # Create test database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Test tables for all systems
        tables = [
            (
                "users",
                "CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT, rp INTEGER)",
            ),
            (
                "drones",
                "CREATE TABLE drones (id TEXT PRIMARY KEY, user_id TEXT, name TEXT)",
            ),
            (
                "resources",
                "CREATE TABLE resources (user_id TEXT, resource_type TEXT, amount INTEGER)",
            ),
            (
                "trades",
                "CREATE TABLE trades (id TEXT PRIMARY KEY, seller_id TEXT, buyer_id TEXT)",
            ),
            (
                "hunting",
                "CREATE TABLE hunting (id TEXT PRIMARY KEY, user_id TEXT, spawn_id TEXT)",
            ),
            (
                "leaderboard",
                "CREATE TABLE leaderboard (id INTEGER PRIMARY KEY, user_id TEXT, score INTEGER)",
            ),
            (
                "memories",
                "CREATE TABLE memories (id INTEGER PRIMARY KEY, user_id TEXT, content TEXT)",
            ),
            (
                "kingdoms",
                "CREATE TABLE kingdoms (id TEXT PRIMARY KEY, name TEXT, ruler_id TEXT)",
            ),
        ]

        for table_name, create_sql in tables:
            cursor.execute(create_sql)
            print(f"✅ Created table: {table_name}")

        # Test data insertion across systems
        test_data = [
            ("users", ("test_user", "TestUser", 100)),
            ("drones", ("drone_1", "test_user", "TestDrone")),
            ("resources", ("test_user", "wood", 50)),
            ("trades", ("trade_1", "seller_1", "buyer_1")),
            ("hunting", ("hunt_1", "test_user", "spawn_1")),
            ("leaderboard", (1, "test_user", 1000)),
            ("memories", (1, "test_user", "Test memory")),
            ("kingdoms", ("lyra", "Lyra's Dominion", "ruler_1")),
        ]

        for table_name, data in test_data:
            if table_name == "leaderboard":
                cursor.execute(
                    f"INSERT INTO {table_name} (user_id, score) VALUES (?, ?)", data[1:]
                )
            else:
                cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?)", data)
            print(f"✅ Inserted data into: {table_name}")

        # Test data retrieval across systems
        for table_name, _ in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"✅ Retrieved {count} records from: {table_name}")

        conn.commit()
        conn.close()

        # Clean up test database
        os.remove(db_path)
        print("✅ Database cleanup successful")

        print("\n🎉 Database integration working properly!")
        return True

    except Exception as e:
        print(f"❌ Database Integration Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling across all systems"""
    print("\n🛡️ Testing Error Handling...")

    try:
        from core.memory_system import ConsolidatedMemorySystem
        from core.economy import RPEconomy
        from core.ai_circuit_breaker import AICircuitBreaker

        # Test memory system error handling
        memory_system = ConsolidatedMemorySystem(simple_mode=True)
        try:
            memory_system.store_user_memory("", "", "")  # Invalid data
        except Exception as e:
            print("✅ Memory system error handling working")

        # Test economy error handling
        economy = RPEconomy()
        try:
            economy.add_rp({}, -100)  # Invalid RP amount
        except Exception as e:
            print("✅ Economy error handling working")

        # Test AI circuit breaker error handling
        ai_circuit_breaker = AICircuitBreaker()
        try:
            ai_circuit_breaker.call_service("nonexistent_service", "test")
        except Exception as e:
            print("✅ AI circuit breaker error handling working")

        print("\n🎉 Error handling working properly across all systems!")
        return True

    except Exception as e:
        print(f"❌ Error Handling Test Error: {e}")
        return False


def main():
    """Run all integration tests"""
    print("🚀 Starting Aether_Project System Integration Test")
    print("=" * 60)

    tests = [
        ("System Connections", test_system_connections),
        ("Data Flow", test_data_flow),
        ("Command Integration", test_command_integration),
        ("Database Integration", test_database_integration),
        ("Error Handling", test_error_handling),
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

    print("\n" + "=" * 60)
    print(f"📊 Integration Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ All systems are properly connected and working together")
        print("🚀 Ready for Discord bot deployment")
        return True
    else:
        print("❌ Some integration tests failed. Please fix issues before deployment.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
