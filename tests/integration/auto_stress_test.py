#!/usr/bin/env python3
"""
Automated Stress Test for Simulacra Rancher
Runs continuously until resources are exhausted, simulating real player behavior
"""

import sys
import os
import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class AutoStressTester:
    """Automated stress tester that runs continuously"""

    def __init__(self):
        self.test_results = []
        self.stats = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "rp_earned": 0,
            "rp_spent": 0,
            "resources_gathered": 0,
            "hunts_attempted": 0,
            "trades_made": 0,
            "memories_stored": 0,
            "start_time": None,
            "end_time": None,
        }
        self.running = False
        self._init_systems()

    def _init_systems(self):
        """Initialize all core systems"""
        try:
            from core.memory_system import ConsolidatedMemorySystem
            from core.economy import RPEconomy
            from core.hunting_system import HuntingSystem
            from core.resource_system import ResourceSystem
            from core.leaderboard import ExclusiveLeaderboard
            from core.personality_system import ConsolidatedPersonalitySystem
            from core.ai_circuit_breaker import AICircuitBreaker
            from core.trade_system import TradeSystem
            from core.kingdom_system import KingdomSystem
            from core.network_consciousness import NetworkConsciousness

            self.memory_system = ConsolidatedMemorySystem(simple_mode=True)
            self.economy = RPEconomy()
            self.hunting_system = HuntingSystem()
            self.resource_system = ResourceSystem()
            self.leaderboard = ExclusiveLeaderboard()
            self.personality_system = ConsolidatedPersonalitySystem()
            self.ai_circuit_breaker = AICircuitBreaker()
            self.trade_system = TradeSystem()
            self.kingdom_system = KingdomSystem()
            self.network_consciousness = NetworkConsciousness()

            # Initialize databases
            self.hunting_system._init_database()
            self.resource_system._init_database()
            self.trade_system._init_database()

            print("✅ All systems initialized for stress testing!")

        except Exception as e:
            print(f"❌ Error initializing systems: {e}")
            raise

    def create_test_users(self, num_users: int = 5):
        """Create multiple test users for realistic testing"""
        self.users = []
        for i in range(num_users):
            user_id = f"stress_user_{i+1}"
            username = f"StressTester{i+1}"
            user = {
                "user_id": user_id,
                "username": username,
                "rp": 100,  # Start with some RP
                "resources": {},
                "memories": [],
                "hunting_history": [],
            }
            self.users.append(user)

        print(f"✅ Created {num_users} test users")
        return self.users

    def get_random_user(self):
        """Get a random user for testing"""
        return random.choice(self.users)

    def execute_command(self, user: Dict, command: str, args: List[str] = None) -> Dict:
        """Execute a command and return results"""
        if args is None:
            args = []

        result = {
            "command": command,
            "user": user["username"],
            "success": False,
            "response": "",
            "rp_change": 0,
            "timestamp": datetime.now().isoformat(),
        }

        try:
            if command == "daily":
                # Claim daily bonus
                daily_bonus = 50
                user["rp"] += daily_bonus
                result["success"] = True
                result["response"] = (
                    f"🎁 {user['username']} claimed daily bonus: +{daily_bonus} RP"
                )
                result["rp_change"] = daily_bonus
                self.stats["rp_earned"] += daily_bonus

            elif command == "gather":
                if len(args) >= 2:
                    resource_type = args[0]
                    quality = args[1]

                    # Start gathering
                    self.resource_system.start_gathering(
                        user["user_id"], resource_type, quality
                    )
                    resources = self.resource_system.get_user_resources(user["user_id"])

                    result["success"] = True
                    result["response"] = (
                        f"🌲 {user['username']} gathered {resource_type} ({quality})"
                    )
                    self.stats["resources_gathered"] += 1

            elif command == "hunt":
                if len(args) >= 2:
                    spawn_id = args[0]
                    rp_cost = int(args[1])

                    if user["rp"] >= rp_cost:
                        # Attempt to catch
                        from core.hunting_system import HuntingEvent

                        spawn_event = self.hunting_system.create_spawn_event(
                            HuntingEvent.WILD_SPAWN, "stress_test_channel"
                        )

                        catch_result = self.hunting_system.attempt_catch(
                            user["user_id"], spawn_event["spawn_id"], rp_cost
                        )

                        if catch_result.get("success"):
                            user["rp"] -= rp_cost
                            result["success"] = True
                            result["response"] = (
                                f"🎯 {user['username']} caught Simulacra! (-{rp_cost} RP)"
                            )
                            result["rp_change"] = -rp_cost
                            self.stats["rp_spent"] += rp_cost
                        else:
                            result["success"] = True
                            result["response"] = (
                                f"❌ {user['username']} failed to catch: {catch_result.get('error', 'Unknown')}"
                            )

                        self.stats["hunts_attempted"] += 1
                    else:
                        result["success"] = True
                        result["response"] = (
                            f"❌ {user['username']} needs {rp_cost} RP, has {user['rp']} RP"
                        )

            elif command == "trade":
                if len(args) >= 4:
                    buyer_id = args[0]
                    item = args[1]
                    amount = int(args[2])
                    price = int(args[3])

                    trade_result = self.trade_system.create_trade_offer(
                        user["user_id"], buyer_id, item, amount, price
                    )

                    if trade_result.get("success"):
                        result["success"] = True
                        result["response"] = (
                            f"🤝 {user['username']} created trade: {amount}x {item} for {price} RP"
                        )
                        self.stats["trades_made"] += 1
                    else:
                        result["success"] = True
                        result["response"] = (
                            f"❌ Trade failed: {trade_result.get('error', 'Unknown')}"
                        )

            elif command == "memory":
                if len(args) >= 2:
                    memory_type = args[0]
                    content = " ".join(args[1:])

                    self.memory_system.store_user_memory(
                        user["user_id"], memory_type, content
                    )

                    result["success"] = True
                    result["response"] = (
                        f"🧠 {user['username']} stored memory: {memory_type}"
                    )
                    self.stats["memories_stored"] += 1

            elif command == "personality":
                if args:
                    message = " ".join(args)
                    emotional_state = self.personality_system.process_input(
                        user["user_id"], message
                    )

                    result["success"] = True
                    result["response"] = f"🧠 {user['username']} personality processed"

            elif command == "leaderboard":
                top_10 = self.leaderboard.get_top_10()
                result["success"] = True
                result["response"] = (
                    f"🏆 Leaderboard checked ({len(top_10) if top_10 else 0} entries)"
                )

            elif command == "kingdoms":
                kingdoms = self.kingdom_system.get_all_kingdoms()
                result["success"] = True
                result["response"] = f"👑 Kingdoms checked ({len(kingdoms)} kingdoms)"

        except Exception as e:
            result["success"] = False
            result["response"] = f"❌ Error: {str(e)}"

        self.stats["total_commands"] += 1
        if result["success"]:
            self.stats["successful_commands"] += 1
        else:
            self.stats["failed_commands"] += 1

        return result

    def generate_random_command(self, user: Dict) -> tuple:
        """Generate a random command based on user state and probabilities"""
        commands = []

        # Always possible commands
        commands.extend([("daily", []), ("leaderboard", []), ("kingdoms", [])])

        # Resource gathering (30% chance)
        if random.random() < 0.3:
            resources = ["wood", "stone", "metal", "crystal", "essence"]
            qualities = ["normal", "rare", "epic", "legendary"]
            commands.append(
                ("gather", [random.choice(resources), random.choice(qualities)])
            )

        # Hunting (25% chance if user has RP)
        if random.random() < 0.25 and user["rp"] > 0:
            spawn_id = f"spawn_{random.randint(100, 999)}"
            rp_cost = random.randint(10, min(100, user["rp"]))
            commands.append(("hunt", [spawn_id, str(rp_cost)]))

        # Trading (15% chance)
        if random.random() < 0.15:
            buyer_id = f"buyer_{random.randint(100, 999)}"
            items = ["wood", "stone", "metal", "crystal"]
            amount = random.randint(1, 10)
            price = random.randint(10, 100)
            commands.append(
                ("trade", [buyer_id, random.choice(items), str(amount), str(price)])
            )

        # Memory storage (20% chance)
        if random.random() < 0.2:
            memory_types = ["gameplay", "social", "achievement", "learning"]
            contents = [
                "Completed a successful hunt",
                "Made a new friend",
                "Learned new strategy",
                "Achieved milestone",
                "Explored new area",
                "Discovered rare resource",
                "Joined kingdom",
                "Won competition",
            ]
            commands.append(
                ("memory", [random.choice(memory_types), random.choice(contents)])
            )

        # Personality interaction (10% chance)
        if random.random() < 0.1:
            messages = [
                "I'm feeling excited about hunting",
                "This game is really fun",
                "I want to improve my skills",
                "The community is great",
                "I love the kingdom system",
                "Trading is interesting",
                "I'm learning new strategies",
            ]
            commands.append(("personality", [random.choice(messages)]))

        if commands:
            return random.choice(commands)
        else:
            return ("daily", [])

    def should_continue_testing(self) -> bool:
        """Determine if testing should continue based on resource exhaustion"""
        # Check if any user has RP
        users_with_rp = sum(1 for user in self.users if user["rp"] > 0)

        # Check if we've been running for too long (safety)
        if self.stats["start_time"]:
            elapsed = datetime.now() - self.stats["start_time"]
            if elapsed.total_seconds() > 3600:  # 1 hour max
                print("⏰ Time limit reached (1 hour)")
                return False

        # Continue if at least one user has RP
        return users_with_rp > 0

    def print_status(self):
        """Print current test status"""
        elapsed = (
            datetime.now() - self.stats["start_time"]
            if self.stats["start_time"]
            else timedelta(0)
        )

        print(f"\n📊 STRESS TEST STATUS")
        print(f"⏱️  Running for: {elapsed}")
        print(f"📝 Total Commands: {self.stats['total_commands']}")
        print(f"✅ Successful: {self.stats['successful_commands']}")
        print(f"❌ Failed: {self.stats['failed_commands']}")
        print(f"💰 RP Earned: {self.stats['rp_earned']}")
        print(f"💸 RP Spent: {self.stats['rp_spent']}")
        print(f"🌲 Resources Gathered: {self.stats['resources_gathered']}")
        print(f"🎯 Hunts Attempted: {self.stats['hunts_attempted']}")
        print(f"🤝 Trades Made: {self.stats['trades_made']}")
        print(f"🧠 Memories Stored: {self.stats['memories_stored']}")

        # User status
        print(f"\n👥 USER STATUS:")
        for user in self.users:
            print(f"  {user['username']}: {user['rp']} RP")

    def run_continuous_stress_test(self, max_iterations: int = 10000):
        """Run continuous stress test until resources are exhausted"""
        print("🚀 Starting Continuous Stress Test")
        print("=" * 60)

        # Create test users
        self.create_test_users(5)

        # Initialize stats
        self.stats["start_time"] = datetime.now()
        self.running = True

        print(f"✅ Created {len(self.users)} test users")
        print(f"🎯 Target: Run until all users run out of RP")
        print(f"⏱️  Started at: {self.stats['start_time']}")
        print("=" * 60)

        iteration = 0

        try:
            while self.running and iteration < max_iterations:
                iteration += 1

                # Get random user
                user = self.get_random_user()

                # Generate random command
                command, args = self.generate_random_command(user)

                # Execute command
                result = self.execute_command(user, command, args)

                # Log significant events
                if result["rp_change"] != 0 or not result["success"]:
                    print(
                        f"📝 [{iteration:04d}] {user['username']} > {command} {' '.join(args)}"
                    )
                    print(f"     {result['response']}")

                # Print status every 100 iterations
                if iteration % 100 == 0:
                    self.print_status()

                # Check if we should continue
                if not self.should_continue_testing():
                    print("\n🏁 RESOURCE EXHAUSTION - All users out of RP!")
                    break

                # Small delay to prevent overwhelming
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("\n⏹️  Stress test interrupted by user")
        except Exception as e:
            print(f"\n❌ Stress test error: {e}")
        finally:
            self.running = False
            self.stats["end_time"] = datetime.now()
            self.print_final_results()

    def print_final_results(self):
        """Print final test results"""
        print("\n" + "=" * 60)
        print("📊 FINAL STRESS TEST RESULTS")
        print("=" * 60)

        if self.stats["start_time"] and self.stats["end_time"]:
            duration = self.stats["end_time"] - self.stats["start_time"]
            print(f"⏱️  Total Duration: {duration}")

        print(f"📝 Total Commands: {self.stats['total_commands']}")
        print(f"✅ Successful Commands: {self.stats['successful_commands']}")
        print(f"❌ Failed Commands: {self.stats['failed_commands']}")

        if self.stats["total_commands"] > 0:
            success_rate = (
                self.stats["successful_commands"] / self.stats["total_commands"]
            ) * 100
            print(f"📊 Success Rate: {success_rate:.1f}%")

        print(f"\n💰 Economy Stats:")
        print(f"  RP Earned: {self.stats['rp_earned']}")
        print(f"  RP Spent: {self.stats['rp_spent']}")
        print(f"  Net RP: {self.stats['rp_earned'] - self.stats['rp_spent']}")

        print(f"\n🎮 Gameplay Stats:")
        print(f"  Resources Gathered: {self.stats['resources_gathered']}")
        print(f"  Hunts Attempted: {self.stats['hunts_attempted']}")
        print(f"  Trades Made: {self.stats['trades_made']}")
        print(f"  Memories Stored: {self.stats['memories_stored']}")

        print(f"\n👥 Final User Status:")
        for user in self.users:
            print(f"  {user['username']}: {user['rp']} RP")

        # Save results
        self.save_results()

        print(f"\n💾 Results saved to: stress_test_results.json")

    def save_results(self):
        """Save test results to file"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "users": self.users,
            "test_results": self.test_results,
        }

        with open("stress_test_results.json", "w") as f:
            json.dump(results, f, indent=2)


def main():
    """Main function to run the stress test"""
    print("🔥 SIMULACRA RANCHER STRESS TEST")
    print("=" * 60)
    print("This will run continuously until all users run out of RP")
    print("Press Ctrl+C to stop early")
    print("=" * 60)

    tester = AutoStressTester()

    # Run the stress test
    tester.run_continuous_stress_test()


if __name__ == "__main__":
    main()
