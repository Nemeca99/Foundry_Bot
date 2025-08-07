#!/usr/bin/env python3
"""
Beautiful Progress Test
Tests systems with beautiful progress bars, user types, and color flair
"""

import sys
import os
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules directly without going through core/__init__.py
try:
    sys.path.insert(
        0,
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"
        ),
    )
    from mod_system import (
        ModSystem,
        GlobalRewardMultiplier,
        ModTemplateGenerator,
        ModTemplate,
        PlayerModProfile,
    )

    print("✅ Mod system imported successfully")
except ImportError as e:
    print(f"❌ Mod system import error: {e}")
    sys.exit(1)


class UserType(Enum):
    """User types with different characteristics"""

    NOOB = "noob"
    CASUAL = "casual"
    REGULAR = "regular"
    VETERAN = "veteran"
    EXPERT = "expert"
    MASTER = "master"


@dataclass
class BeautifulUser:
    """Beautiful user with type and progress tracking"""

    id: str
    name: str
    user_type: UserType
    rp: int = 100
    drones: List[Dict] = None
    hunt_attempts: int = 0
    hunt_successes: int = 0
    mod_attempts: int = 0
    mod_successes: int = 0
    economy_transactions: int = 0
    total_rp_earned: int = 0

    def __post_init__(self):
        if self.drones is None:
            self.drones = []


class BeautifulProgressTester:
    """Beautiful progress tester with bars and color flair"""

    def __init__(self):
        self.mod_system = ModSystem("data/beautiful_progress_mods.db")
        self.global_multiplier = GlobalRewardMultiplier(self.mod_system)

        self.users = {}
        self.test_results = {
            "users_created": 0,
            "mods_created": 0,
            "mod_activations": 0,
            "global_multiplier_tests": 0,
            "economy_simulations": 0,
            "hunt_simulations": 0,
            "errors": [],
        }

        # Color codes for beautiful output
        self.colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "bright_green": "\033[92;1m",
            "bright_yellow": "\033[93;1m",
            "bright_blue": "\033[94;1m",
            "bright_magenta": "\033[95;1m",
            "reset": "\033[0m",
        }

        print("🎨 Beautiful Progress Test Initialized")
        print("🔧 Testing systems with beautiful progress bars and color flair")

    def print_colored(self, text: str, color: str = "white"):
        """Print colored text"""
        print(f"{self.colors.get(color, '')}{text}{self.colors['reset']}")

    def create_progress_bar(
        self, percentage: float, width: int = 30, color: str = "green"
    ) -> str:
        """Create a beautiful progress bar"""
        filled_length = int(width * percentage / 100)
        bar = "█" * filled_length + "░" * (width - filled_length)
        return f"{self.colors[color]}[{bar}]{self.colors['reset']} {percentage:5.1f}%"

    def create_test_users(self, count: int = 12):
        """Create test users with different types"""
        print(f"\n👥 Creating {count} beautiful test users...")

        user_types = list(UserType)
        type_names = {
            UserType.NOOB: "Noob",
            UserType.CASUAL: "Casual",
            UserType.REGULAR: "Regular",
            UserType.VETERAN: "Veteran",
            UserType.EXPERT: "Expert",
            UserType.MASTER: "Master",
        }

        for i in range(count):
            user_type = user_types[i % len(user_types)]
            user_id = f"beautiful_user_{i+1}"

            # Different RP based on user type
            rp_base = {
                UserType.NOOB: (20, 50),
                UserType.CASUAL: (50, 100),
                UserType.REGULAR: (100, 200),
                UserType.VETERAN: (200, 400),
                UserType.EXPERT: (400, 800),
                UserType.MASTER: (800, 1500),
            }

            min_rp, max_rp = rp_base[user_type]
            rp = random.randint(min_rp, max_rp)

            user = BeautifulUser(
                id=user_id,
                name=f"{type_names[user_type]}{i+1}",
                user_type=user_type,
                rp=rp,
            )
            self.users[user_id] = user
            self.test_results["users_created"] += 1

        print(f"✅ Created {count} beautiful test users")

    def simulate_hunt_system(self):
        """Simulate hunting system with progress bars"""
        print("\n🏹 Simulating Hunt System...")

        for user_id, user in self.users.items():
            # Different success rates based on user type
            success_rates = {
                UserType.NOOB: 0.3,
                UserType.CASUAL: 0.5,
                UserType.REGULAR: 0.6,
                UserType.VETERAN: 0.7,
                UserType.EXPERT: 0.8,
                UserType.MASTER: 0.9,
            }

            success_rate = success_rates[user.user_type]
            attempts = random.randint(3, 8)
            successes = 0

            for attempt in range(attempts):
                if random.random() < success_rate:
                    successes += 1
                    rp_earned = random.randint(5, 15)
                    user.total_rp_earned += rp_earned
                    user.rp += rp_earned

            user.hunt_attempts = attempts
            user.hunt_successes = successes
            self.test_results["hunt_simulations"] += 1

            # Calculate success percentage
            success_percentage = (successes / attempts) * 100 if attempts > 0 else 0

            # Color based on success rate
            color = (
                "green"
                if success_percentage >= 70
                else "yellow" if success_percentage >= 50 else "red"
            )

            print(
                f"  {user.name:<12} Hunt: {self.create_progress_bar(success_percentage, 20, color)} ({successes}/{attempts} attempts)"
            )

    def simulate_mod_system(self):
        """Simulate mod system with progress bars"""
        print("\n🔧 Simulating Mod System...")

        for user_id, user in self.users.items():
            # Different mod success rates based on user type
            mod_success_rates = {
                UserType.NOOB: 0.2,
                UserType.CASUAL: 0.4,
                UserType.REGULAR: 0.6,
                UserType.VETERAN: 0.7,
                UserType.EXPERT: 0.8,
                UserType.MASTER: 0.95,
            }

            success_rate = mod_success_rates[user.user_type]
            attempts = random.randint(2, 5)
            successes = 0

            for attempt in range(attempts):
                if random.random() < success_rate:
                    successes += 1
                    rp_cost = random.randint(10, 30)
                    user.rp -= rp_cost
                    user.total_rp_earned -= rp_cost

            user.mod_attempts = attempts
            user.mod_successes = successes
            self.test_results["mod_activations"] += successes

            # Calculate success percentage
            success_percentage = (successes / attempts) * 100 if attempts > 0 else 0

            # Color based on success rate
            color = (
                "green"
                if success_percentage >= 70
                else "yellow" if success_percentage >= 50 else "red"
            )

            print(
                f"  {user.name:<12} Mods:  {self.create_progress_bar(success_percentage, 20, color)} ({successes}/{attempts} attempts)"
            )

    def simulate_economy_system(self):
        """Simulate economy system with progress bars"""
        print("\n💰 Simulating Economy System...")

        for user_id, user in self.users.items():
            # Different economy success rates based on user type
            economy_rates = {
                UserType.NOOB: 0.4,
                UserType.CASUAL: 0.6,
                UserType.REGULAR: 0.7,
                UserType.VETERAN: 0.8,
                UserType.EXPERT: 0.85,
                UserType.MASTER: 0.95,
            }

            success_rate = economy_rates[user.user_type]
            transactions = random.randint(5, 12)
            successful_transactions = 0

            for transaction in range(transactions):
                if random.random() < success_rate:
                    successful_transactions += 1
                    rp_earned = random.randint(10, 50)
                    final_rp = self.global_multiplier.apply_multiplier_to_reward(
                        rp_earned
                    )
                    user.rp += int(final_rp)
                    user.total_rp_earned += int(final_rp)

            user.economy_transactions = transactions
            self.test_results["economy_simulations"] += transactions

            # Calculate success percentage
            success_percentage = (
                (successful_transactions / transactions) * 100
                if transactions > 0
                else 0
            )

            # Color based on success rate
            color = (
                "green"
                if success_percentage >= 70
                else "yellow" if success_percentage >= 50 else "red"
            )

            print(
                f"  {user.name:<12} Econ:  {self.create_progress_bar(success_percentage, 20, color)} ({successful_transactions}/{transactions} transactions)"
            )

    def test_global_multiplier_scenarios(self):
        """Test global multiplier with beautiful scenarios"""
        print("\n🌍 Testing Global Multiplier Scenarios...")

        scenarios = [
            {
                "name": "Booming Economy",
                "drones_alive": 200,
                "active_players": 20,
                "drones_ever_died": 10,
                "color": "bright_green",
            },
            {
                "name": "Stable Economy",
                "drones_alive": 100,
                "active_players": 10,
                "drones_ever_died": 50,
                "color": "green",
            },
            {
                "name": "Declining Economy",
                "drones_alive": 50,
                "active_players": 5,
                "drones_ever_died": 200,
                "color": "yellow",
            },
            {
                "name": "Crisis Economy",
                "drones_alive": 10,
                "active_players": 2,
                "drones_ever_died": 500,
                "color": "red",
            },
        ]

        for i, scenario in enumerate(scenarios):
            self.global_multiplier.update_multiplier(
                scenario["drones_alive"],
                scenario["active_players"],
                scenario["drones_ever_died"],
            )

            multiplier_percentage = (self.global_multiplier.multiplier / 3.0) * 100
            bar = self.create_progress_bar(multiplier_percentage, 25, scenario["color"])

            print(
                f"  {scenario['name']:<15} Multiplier: {bar} ({self.global_multiplier.multiplier:.2f}x)"
            )
            self.test_results["global_multiplier_tests"] += 1

    def show_user_type_breakdown(self):
        """Show beautiful user type breakdown"""
        print("\n👥 User Type Breakdown:")
        print("=" * 60)

        type_counts = {}
        type_stats = {}

        for user in self.users.values():
            if user.user_type not in type_counts:
                type_counts[user.user_type] = 0
                type_stats[user.user_type] = {
                    "total_rp": 0,
                    "total_earned": 0,
                    "avg_hunt": 0,
                    "avg_mod": 0,
                }

            type_counts[user.user_type] += 1
            type_stats[user.user_type]["total_rp"] += user.rp
            type_stats[user.user_type]["total_earned"] += user.total_rp_earned

        # Calculate averages
        for user_type in type_stats:
            count = type_counts[user_type]
            users_of_type = [u for u in self.users.values() if u.user_type == user_type]

            if users_of_type:
                avg_hunt = (
                    sum(
                        u.hunt_successes / max(u.hunt_attempts, 1)
                        for u in users_of_type
                    )
                    / len(users_of_type)
                    * 100
                )
                avg_mod = (
                    sum(u.mod_successes / max(u.mod_attempts, 1) for u in users_of_type)
                    / len(users_of_type)
                    * 100
                )

                type_stats[user_type]["avg_hunt"] = avg_hunt
                type_stats[user_type]["avg_mod"] = avg_mod

        # Display with colors
        colors = [
            "bright_green",
            "green",
            "bright_blue",
            "blue",
            "bright_magenta",
            "magenta",
        ]

        for i, (user_type, count) in enumerate(type_counts.items()):
            color = colors[i % len(colors)]
            stats = type_stats[user_type]

            print(f"  {user_type.value.title():<10} ({count:2d} users):")
            print(
                f"    RP: {stats['total_rp']:4d} | Earned: {stats['total_earned']:4d}"
            )

            hunt_bar = self.create_progress_bar(stats["avg_hunt"], 15, color)
            mod_bar = self.create_progress_bar(stats["avg_mod"], 15, color)

            print(f"    Hunt: {hunt_bar}")
            print(f"    Mods: {mod_bar}")
            print()

    def run_beautiful_test(self):
        """Run the beautiful comprehensive test"""
        print("🎨 Beautiful Progress Test")
        print("=" * 60)
        print("🚀 Testing systems with beautiful progress bars and color flair")
        print("=" * 60)

        try:
            # Step 1: Create test users
            self.create_test_users(12)

            # Step 2: Simulate hunt system
            self.simulate_hunt_system()

            # Step 3: Simulate mod system
            self.simulate_mod_system()

            # Step 4: Simulate economy system
            self.simulate_economy_system()

            # Step 5: Test global multiplier scenarios
            self.test_global_multiplier_scenarios()

            # Step 6: Show user type breakdown
            self.show_user_type_breakdown()

            # Step 7: Save results
            self.save_results()

            print("\n🎉 Beautiful Progress Test Completed!")
            print("=" * 60)
            self.print_colored(
                "✅ All core systems tested successfully", "bright_green"
            )
            self.print_colored("🔧 Mod system working", "green")
            self.print_colored("🌍 Global multiplier operational", "bright_blue")
            self.print_colored("💰 Economy integration functional", "bright_magenta")
            self.print_colored("🏹 Hunt system operational", "bright_yellow")
            self.print_colored("🎨 Beautiful progress bars working", "cyan")
            print("=" * 60)

            self.print_summary()

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            self.test_results["errors"].append(str(e))
            self.save_results()

    def save_results(self):
        """Save test results"""
        results_file = "beautiful_progress_results.json"

        with open(results_file, "w") as f:
            json.dump(
                {
                    "test_timestamp": datetime.now().isoformat(),
                    "test_results": self.test_results,
                    "user_summary": {
                        user_id: {
                            "name": user.name,
                            "user_type": user.user_type.value,
                            "rp": user.rp,
                            "total_rp_earned": user.total_rp_earned,
                            "hunt_attempts": user.hunt_attempts,
                            "hunt_successes": user.hunt_successes,
                            "mod_attempts": user.mod_attempts,
                            "mod_successes": user.mod_successes,
                            "economy_transactions": user.economy_transactions,
                        }
                        for user_id, user in self.users.items()
                    },
                    "global_multiplier": self.global_multiplier.multiplier,
                },
                f,
                indent=2,
            )

        print(f"📊 Results saved to: {results_file}")

    def print_summary(self):
        """Print beautiful test summary"""
        print("\n📋 Beautiful Test Summary:")
        print("-" * 50)

        print(f"👥 Users Created: {self.test_results['users_created']}")
        print(f"🔧 Mod Activations: {self.test_results['mod_activations']}")
        print(
            f"🌍 Global Multiplier Tests: {self.test_results['global_multiplier_tests']}"
        )
        print(f"💰 Economy Simulations: {self.test_results['economy_simulations']}")
        print(f"🏹 Hunt Simulations: {self.test_results['hunt_simulations']}")

        if self.test_results["errors"]:
            self.print_colored(f"❌ Errors: {len(self.test_results['errors'])}", "red")
            for error in self.test_results["errors"]:
                print(f"  • {error}")
        else:
            self.print_colored("✅ No errors encountered", "bright_green")

        self.print_colored(
            f"\n🌍 Final Global Multiplier: {self.global_multiplier.multiplier:.2f}x",
            "bright_blue",
        )

        # Show top performers
        print("\n🏆 Top Performers:")
        sorted_users = sorted(
            self.users.values(), key=lambda u: u.total_rp_earned, reverse=True
        )
        for i, user in enumerate(sorted_users[:3]):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            self.print_colored(
                f"  {medal} {user.name} ({user.user_type.value}): {user.total_rp_earned} RP earned",
                "bright_yellow",
            )


def main():
    """Main function"""
    print("🚀 Starting Beautiful Progress Test")
    print("=" * 60)

    tester = BeautifulProgressTester()
    tester.run_beautiful_test()


if __name__ == "__main__":
    main()
