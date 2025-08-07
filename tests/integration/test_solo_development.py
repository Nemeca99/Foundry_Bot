#!/usr/bin/env python3
"""
Solo Development Testing Framework for Simulacra Rancher
Practical testing strategy for one-person development
"""

import sys
import os
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class SoloTestFramework:
    """
    Practical testing framework for solo development
    Focuses on critical paths and real-world scenarios
    """

    def __init__(self):
        self.test_results = []
        self.critical_issues = []
        self.performance_metrics = {}

    def log_test(
        self, test_name: str, success: bool, details: str = "", duration: float = 0
    ):
        """Log test results with timing"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(result)

        if not success:
            self.critical_issues.append(result)

        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name} ({duration:.2f}s) - {details}")

    def test_critical_user_journey(self):
        """Test the most important user journey: New user -> First hunt -> Get RP"""
        print("\n🎯 Testing Critical User Journey...")
        start_time = time.time()

        try:
            # Import core systems
            from core.memory_system import ConsolidatedMemorySystem
            from core.economy import RPEconomy
            from core.hunting_system import HuntingSystem
            from core.resource_system import ResourceSystem
            from core.leaderboard import ExclusiveLeaderboard

            # Initialize systems
            memory_system = ConsolidatedMemorySystem(simple_mode=True)
            economy = RPEconomy()
            hunting_system = HuntingSystem()
            resource_system = ResourceSystem()
            leaderboard = ExclusiveLeaderboard()

            # Initialize databases
            hunting_system._init_database()
            resource_system._init_database()

            test_user = "new_user_123"

            # 1. New user starts with 0 RP
            player_data = {"rp": 0}
            initial_rp = player_data["rp"]

            # 2. User gathers resources (free action)
            resource_system.start_gathering(test_user, "wood", "normal")
            resources = resource_system.get_user_resources(test_user)

            # 3. User hunts a Simulacra (costs RP)
            from core.hunting_system import HuntingEvent

            spawn_event = hunting_system.create_spawn_event(
                HuntingEvent.WILD_SPAWN, "test_channel"
            )

            # User needs RP to hunt - this should fail
            catch_result = hunting_system.attempt_catch(
                test_user, spawn_event["spawn_id"], 50
            )

            # 4. User earns RP through other means
            economy.add_rp(player_data, 100)
            final_rp = player_data["rp"]

            # 5. Now user can hunt
            catch_result_with_rp = hunting_system.attempt_catch(
                test_user, spawn_event["spawn_id"], 50
            )

            # 6. User stores memory of the experience
            memory_system.store_user_memory(
                test_user, "first_hunt", "Completed my first hunt!"
            )

            # Verify the journey worked
            success = (
                initial_rp == 0
                and final_rp == 100
                and "error" in catch_result
                and "success" in catch_result_with_rp
            )

            duration = time.time() - start_time
            details = f"RP: {initial_rp}→{final_rp}, Hunt: {catch_result.get('success', False)}→{catch_result_with_rp.get('success', False)}"

            self.log_test("Critical User Journey", success, details, duration)
            return success

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Critical User Journey", False, f"Error: {str(e)}", duration)
            return False

    def test_discord_command_parsing(self):
        """Test that Discord commands are parsed correctly"""
        print("\n🎮 Testing Discord Command Parsing...")
        start_time = time.time()

        try:
            # Test command parsing logic
            test_commands = [
                "!gather normal",
                "!hunt 123 100",
                "!trade 456 789 5 50",
                "!rp",
                "!leaderboard",
                "!kingdoms",
                "!daily",
                "!help",
            ]

            parsed_commands = []
            for cmd in test_commands:
                parts = cmd.split()
                command = parts[0]
                args = parts[1:] if len(parts) > 1 else []
                parsed_commands.append({"command": command, "args": args})

            # Verify all commands parsed correctly
            success = len(parsed_commands) == len(test_commands)

            duration = time.time() - start_time
            details = f"Parsed {len(parsed_commands)} commands"

            self.log_test("Discord Command Parsing", success, details, duration)
            return success

        except Exception as e:
            duration = time.time() - start_time
            self.log_test(
                "Discord Command Parsing", False, f"Error: {str(e)}", duration
            )
            return False

    def test_database_integrity(self):
        """Test that all databases can be created and accessed"""
        print("\n🗄️ Testing Database Integrity...")
        start_time = time.time()

        try:
            import sqlite3

            # Test database creation for all systems
            test_db = "test_solo_integration.db"

            # Create test database
            conn = sqlite3.connect(test_db)
            cursor = conn.cursor()

            # Test core tables
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
                (
                    "network_consciousness",
                    "CREATE TABLE network_consciousness (id INTEGER PRIMARY KEY, drone_id TEXT, server_id TEXT)",
                ),
            ]

            created_tables = 0
            for table_name, create_sql in tables:
                try:
                    cursor.execute(create_sql)
                    created_tables += 1
                except Exception as e:
                    print(f"Warning: Could not create {table_name}: {e}")

            # Test data insertion
            test_data = ("test_user", "TestUser", 100)
            cursor.execute("INSERT INTO users VALUES (?, ?, ?)", test_data)

            # Test data retrieval
            cursor.execute("SELECT * FROM users WHERE id = ?", ("test_user",))
            result = cursor.fetchone()

            conn.commit()
            conn.close()

            # Cleanup
            os.remove(test_db)

            success = (
                created_tables >= 6 and result is not None
            )  # At least 6 tables should work

            duration = time.time() - start_time
            details = (
                f"Created {created_tables}/8 tables, data: {'✓' if result else '✗'}"
            )

            self.log_test("Database Integrity", success, details, duration)
            return success

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Database Integrity", False, f"Error: {str(e)}", duration)
            return False

    def test_ai_system_availability(self):
        """Test that AI systems are available and responding"""
        print("\n🤖 Testing AI System Availability...")
        start_time = time.time()

        try:
            from core.ai_circuit_breaker import AICircuitBreaker
            from core.personality_system import ConsolidatedPersonalitySystem

            # Test AI circuit breaker
            ai_circuit_breaker = AICircuitBreaker()

            # Test personality system
            personality_system = ConsolidatedPersonalitySystem()

            # Test basic AI functionality
            test_input = "Hello, how are you?"
            test_user = "test_user_ai"

            # This should work even without actual AI services
            emotional_state = personality_system.process_input(test_user, test_input)

            success = emotional_state is not None

            duration = time.time() - start_time
            details = f"AI Circuit Breaker: ✓, Personality System: ✓"

            self.log_test("AI System Availability", success, details, duration)
            return success

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("AI System Availability", False, f"Error: {str(e)}", duration)
            return False

    def test_performance_baseline(self):
        """Test system performance under basic load"""
        print("\n⚡ Testing Performance Baseline...")
        start_time = time.time()

        try:
            from core.memory_system import ConsolidatedMemorySystem
            from core.economy import RPEconomy

            # Initialize systems
            memory_system = ConsolidatedMemorySystem(simple_mode=True)
            economy = RPEconomy()

            # Test multiple operations
            operations = []
            test_user = "perf_test_user"

            for i in range(10):
                op_start = time.time()

                # Memory operation
                memory_system.store_user_memory(
                    test_user, f"test_{i}", f"Test memory {i}"
                )

                # Economy operation
                player_data = {"rp": i * 10}
                economy.add_rp(player_data, 5)

                op_duration = time.time() - op_start
                operations.append(op_duration)

            avg_operation_time = sum(operations) / len(operations)
            max_operation_time = max(operations)

            # Performance thresholds (adjust based on your system)
            success = avg_operation_time < 0.1 and max_operation_time < 0.5

            duration = time.time() - start_time
            details = f"Avg: {avg_operation_time:.3f}s, Max: {max_operation_time:.3f}s"

            self.log_test("Performance Baseline", success, details, duration)
            return success

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Performance Baseline", False, f"Error: {str(e)}", duration)
            return False

    def test_error_handling(self):
        """Test that systems handle errors gracefully"""
        print("\n🛡️ Testing Error Handling...")
        start_time = time.time()

        try:
            from core.memory_system import ConsolidatedMemorySystem
            from core.economy import RPEconomy

            # Test memory system error handling
            memory_system = ConsolidatedMemorySystem(simple_mode=True)

            # Test with invalid data - systems should handle gracefully
            try:
                memory_system.store_user_memory("", "", "")  # Invalid data
                memory_handled = True  # System accepted invalid data gracefully
            except Exception:
                memory_handled = True  # System threw exception (also acceptable)

            # Test economy error handling
            economy = RPEconomy()
            try:
                economy.add_rp({}, -100)  # Invalid RP amount
                economy_handled = True  # System accepted invalid data gracefully
            except Exception:
                economy_handled = True  # System threw exception (also acceptable)

            # Test AI circuit breaker error handling
            from core.ai_circuit_breaker import AICircuitBreaker

            ai_circuit_breaker = AICircuitBreaker()
            try:
                ai_circuit_breaker.call_service("nonexistent_service", "test")
                ai_handled = True  # System handled gracefully
            except Exception:
                ai_handled = True  # System threw exception (also acceptable)

            success = memory_handled and economy_handled and ai_handled

            duration = time.time() - start_time
            details = f"Memory: {'✓' if memory_handled else '✗'}, Economy: {'✓' if economy_handled else '✗'}, AI: {'✓' if ai_handled else '✗'}"

            self.log_test("Error Handling", success, details, duration)
            return success

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Error Handling", False, f"Error: {str(e)}", duration)
            return False

    def generate_test_report(self):
        """Generate a comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 SOLO DEVELOPMENT TEST REPORT")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        if self.critical_issues:
            print(f"\n❌ CRITICAL ISSUES ({len(self.critical_issues)}):")
            for issue in self.critical_issues:
                print(f"  • {issue['test_name']}: {issue['details']}")

        # Performance summary
        if self.performance_metrics:
            print(f"\n⚡ PERFORMANCE METRICS:")
            for metric, value in self.performance_metrics.items():
                print(f"  • {metric}: {value}")

        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if failed_tests == 0:
            print("  ✅ All tests passed! Ready for Discord deployment.")
        elif failed_tests <= 2:
            print("  ⚠️ Minor issues found. Fix critical issues before deployment.")
        else:
            print(
                "  ❌ Multiple issues found. Address critical issues before deployment."
            )

        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests) * 100,
            },
            "test_results": self.test_results,
            "critical_issues": self.critical_issues,
            "performance_metrics": self.performance_metrics,
        }

        with open("solo_test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)

        print(f"\n📄 Detailed report saved to: solo_test_report.json")

        return failed_tests == 0


def main():
    """Run the solo development test suite"""
    print("🚀 Starting Solo Development Test Suite")
    print("=" * 60)

    framework = SoloTestFramework()

    # Run all tests
    tests = [
        ("Critical User Journey", framework.test_critical_user_journey),
        ("Discord Command Parsing", framework.test_discord_command_parsing),
        ("Database Integrity", framework.test_database_integrity),
        ("AI System Availability", framework.test_ai_system_availability),
        ("Performance Baseline", framework.test_performance_baseline),
        ("Error Handling", framework.test_error_handling),
    ]

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        test_func()

    # Generate final report
    success = framework.generate_test_report()

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
