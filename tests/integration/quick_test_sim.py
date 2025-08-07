#!/usr/bin/env python3
"""
Quick Test Simulation - 30 seconds
"""

import sys
import os
import json
import time
import random
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
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
class SimulationUser:
    """User in the full simulation"""

    id: str
    name: str
    user_type: UserType
    rp: int = 100
    total_rp_earned: int = 0
    total_rp_spent: int = 0
    hunt_ticks: int = 0
    hunt_successes: int = 0
    mod_ticks: int = 0
    mod_successes: int = 0
    economy_ticks: int = 0
    economy_successes: int = 0
    current_activity: str = "idle"
    last_activity: float = 0.0
    activity_cooldown: float = 0.0
    personality_traits: List[str] = None
    preferred_activities: List[str] = None

    def __post_init__(self):
        self.last_activity = time.time()
        if self.personality_traits is None:
            self.personality_traits = self.generate_personality()
        if self.preferred_activities is None:
            self.preferred_activities = self.generate_preferences()

    def generate_personality(self) -> List[str]:
        """Generate personality traits based on user type"""
        traits = {
            UserType.NOOB: ["curious", "cautious", "learning"],
            UserType.CASUAL: ["relaxed", "social", "balanced"],
            UserType.REGULAR: ["consistent", "strategic", "engaged"],
            UserType.VETERAN: ["experienced", "efficient", "helpful"],
            UserType.EXPERT: ["optimized", "competitive", "knowledgeable"],
            UserType.MASTER: ["legendary", "innovative", "influential"],
        }
        return traits.get(self.user_type, ["balanced"])

    def generate_preferences(self) -> List[str]:
        """Generate activity preferences based on user type"""
        preferences = {
            UserType.NOOB: ["hunt", "economy"],
            UserType.CASUAL: ["hunt", "mod", "economy"],
            UserType.REGULAR: ["hunt", "mod", "economy"],
            UserType.VETERAN: ["mod", "hunt", "economy"],
            UserType.EXPERT: ["mod", "economy", "hunt"],
            UserType.MASTER: ["mod", "economy", "hunt"],
        }
        return preferences.get(self.user_type, ["hunt", "mod", "economy"])


@dataclass
class SimulationActivity:
    """Activity in the full simulation"""

    user_id: str
    activity_type: str
    ticks_requested: int
    ticks_completed: int = 0
    base_cost: int = 100
    total_cost: int = 0
    success_rate: float = 0.5
    start_time: float = 0.0
    is_complete: bool = False

    def __post_init__(self):
        self.start_time = time.time()
        self.total_cost = self.calculate_total_cost()

    def calculate_total_cost(self, global_multiplier: float = 1.0) -> int:
        """Calculate entropy compression cost with global multiplier"""
        if self.ticks_requested <= 1:
            return self.base_cost

        # Base cost for going over 1 tick
        base_over_cost = self.base_cost * 2

        # Entropy compression: n × global_multiplier
        compression_multiplier = self.ticks_requested * global_multiplier

        return int(base_over_cost * compression_multiplier)


class QuickTestSimulation:
    """Quick test simulation - 30 seconds"""

    def __init__(self):
        self.mod_system = ModSystem("data/quick_test_mods.db")
        self.global_multiplier = GlobalRewardMultiplier(self.mod_system)

        self.users = {}
        self.active_activities = {}
        self.tick_count = 0
        self.tick_rate = 1.0  # 1 tick per second
        self.is_running = False
        self.thread = None

        # Quick test settings
        self.simulation_duration = 30  # 30 seconds
        self.user_count = 10  # Fewer users for quick test
        self.economy_cycles = []
        self.world_events = []

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

        self.stats = {
            "total_ticks": 0,
            "total_activities": 0,
            "total_rp_earned": 0,
            "total_rp_spent": 0,
            "activities_completed": 0,
            "economy_cycles": 0,
            "world_events": 0,
            "errors": [],
        }

        print("🌍 Quick Test Simulation Initialized")
        print("🎮 30-second test with 10 users")

    def print_colored(self, text: str, color: str = "white"):
        """Print colored text"""
        print(f"{self.colors.get(color, '')}{text}{self.colors['reset']}")

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")

    def create_progress_bar(
        self, percentage: float, width: int = 30, color: str = "green"
    ) -> str:
        """Create a beautiful progress bar"""
        filled_length = int(width * percentage / 100)
        bar = "█" * filled_length + "░" * (width - filled_length)
        return f"{self.colors[color]}[{bar}]{self.colors['reset']} {percentage:5.1f}%"

    def create_simulation_users(self):
        """Create realistic simulation users"""
        print(f"\n👥 Creating {self.user_count} test users...")

        user_types = list(UserType)
        type_names = {
            UserType.NOOB: "Noob",
            UserType.CASUAL: "Casual",
            UserType.REGULAR: "Regular",
            UserType.VETERAN: "Veteran",
            UserType.EXPERT: "Expert",
            UserType.MASTER: "Master",
        }

        for i in range(self.user_count):
            user_type = user_types[i % len(user_types)]
            user_id = f"test_user_{i+1}"

            # Different RP based on user type
            rp_base = {
                UserType.NOOB: (50, 150),
                UserType.CASUAL: (100, 300),
                UserType.REGULAR: (200, 600),
                UserType.VETERAN: (400, 1200),
                UserType.EXPERT: (800, 2000),
                UserType.MASTER: (1500, 4000),
            }

            min_rp, max_rp = rp_base[user_type]
            rp = random.randint(min_rp, max_rp)

            user = SimulationUser(
                id=user_id,
                name=f"{type_names[user_type]}{i+1}",
                user_type=user_type,
                rp=rp,
            )
            self.users[user_id] = user

        print(f"✅ Created {self.user_count} test users")

    def generate_user_activity(self, user_id: str):
        """Generate realistic user activity based on personality"""
        user = self.users[user_id]

        # Check if user is on cooldown
        if time.time() - user.last_activity < user.activity_cooldown:
            return

        # Determine activity based on preferences and personality
        activity_chance = random.random()

        if "hunt" in user.preferred_activities and activity_chance < 0.4:
            self.start_user_hunt(user_id)
        elif "mod" in user.preferred_activities and activity_chance < 0.7:
            self.start_user_mod(user_id)
        elif "economy" in user.preferred_activities and activity_chance < 0.9:
            self.start_user_economy(user_id)

    def start_user_hunt(self, user_id: str):
        """Start hunt activity for user"""
        user = self.users[user_id]

        # Determine tick amount based on user type and personality
        if "cautious" in user.personality_traits:
            ticks = random.randint(1, 3)
        elif "efficient" in user.personality_traits:
            ticks = random.randint(2, 5)
        elif "optimized" in user.personality_traits:
            ticks = random.randint(3, 8)
        else:
            ticks = random.randint(1, 5)

        base_cost = 100
        activity = SimulationActivity(
            user_id=user_id,
            activity_type="hunt",
            ticks_requested=ticks,
            base_cost=base_cost,
            success_rate=self.get_hunt_success_rate(user.user_type),
        )
        activity.total_cost = activity.calculate_total_cost(
            self.global_multiplier.multiplier
        )

        # Check if user can afford it
        if user.rp < activity.total_cost:
            return

        # Deduct RP and start activity
        user.rp -= activity.total_cost
        user.total_rp_spent += activity.total_cost
        user.current_activity = f"hunt({ticks}x)"
        user.last_activity = time.time()
        user.activity_cooldown = random.uniform(5, 15)

        self.active_activities[user_id] = activity
        self.stats["total_activities"] += 1

    def start_user_mod(self, user_id: str):
        """Start mod activity for user"""
        user = self.users[user_id]

        # Determine tick amount based on user type
        if user.user_type in [UserType.EXPERT, UserType.MASTER]:
            ticks = random.randint(2, 6)
        else:
            ticks = random.randint(1, 4)

        base_cost = 150
        activity = SimulationActivity(
            user_id=user_id,
            activity_type="mod",
            ticks_requested=ticks,
            base_cost=base_cost,
            success_rate=self.get_mod_success_rate(user.user_type),
        )
        activity.total_cost = activity.calculate_total_cost(
            self.global_multiplier.multiplier
        )

        if user.rp < activity.total_cost:
            return

        user.rp -= activity.total_cost
        user.total_rp_spent += activity.total_cost
        user.current_activity = f"mod({ticks}x)"
        user.last_activity = time.time()
        user.activity_cooldown = random.uniform(8, 20)

        self.active_activities[user_id] = activity
        self.stats["total_activities"] += 1

    def start_user_economy(self, user_id: str):
        """Start economy activity for user"""
        user = self.users[user_id]

        ticks = random.randint(1, 4)
        base_cost = 75
        activity = SimulationActivity(
            user_id=user_id,
            activity_type="economy",
            ticks_requested=ticks,
            base_cost=base_cost,
            success_rate=self.get_economy_success_rate(user.user_type),
        )
        activity.total_cost = activity.calculate_total_cost(
            self.global_multiplier.multiplier
        )

        if user.rp < activity.total_cost:
            return

        user.rp -= activity.total_cost
        user.total_rp_spent += activity.total_cost
        user.current_activity = f"econ({ticks}x)"
        user.last_activity = time.time()
        user.activity_cooldown = random.uniform(3, 10)

        self.active_activities[user_id] = activity
        self.stats["total_activities"] += 1

    def get_hunt_success_rate(self, user_type: UserType) -> float:
        """Get hunt success rate based on user type"""
        rates = {
            UserType.NOOB: 0.3,
            UserType.CASUAL: 0.5,
            UserType.REGULAR: 0.6,
            UserType.VETERAN: 0.7,
            UserType.EXPERT: 0.8,
            UserType.MASTER: 0.9,
        }
        return rates.get(user_type, 0.5)

    def get_mod_success_rate(self, user_type: UserType) -> float:
        """Get mod success rate based on user type"""
        rates = {
            UserType.NOOB: 0.2,
            UserType.CASUAL: 0.4,
            UserType.REGULAR: 0.6,
            UserType.VETERAN: 0.7,
            UserType.EXPERT: 0.8,
            UserType.MASTER: 0.95,
        }
        return rates.get(user_type, 0.5)

    def get_economy_success_rate(self, user_type: UserType) -> float:
        """Get economy success rate based on user type"""
        rates = {
            UserType.NOOB: 0.4,
            UserType.CASUAL: 0.6,
            UserType.REGULAR: 0.7,
            UserType.VETERAN: 0.8,
            UserType.EXPERT: 0.85,
            UserType.MASTER: 0.95,
        }
        return rates.get(user_type, 0.5)

    def process_tick(self):
        """Process one tick for all active activities and generate new activities"""
        self.tick_count += 1
        self.stats["total_ticks"] += 1

        # Generate new user activities
        for user_id in self.users:
            if user_id not in self.active_activities:
                self.generate_user_activity(user_id)

        # Process active activities
        completed_activities = []

        for user_id, activity in self.active_activities.items():
            activity.ticks_completed += 1
            user = self.users[user_id]

            # Check if activity is complete
            if activity.ticks_completed >= activity.ticks_requested:
                # Determine success
                success = random.random() < activity.success_rate

                if success:
                    # Calculate reward based on activity type
                    if activity.activity_type == "hunt":
                        reward = random.randint(20, 50)
                        user.hunt_successes += 1
                        user.hunt_ticks += activity.ticks_requested
                    elif activity.activity_type == "mod":
                        reward = random.randint(30, 80)
                        user.mod_successes += 1
                        user.mod_ticks += activity.ticks_requested
                    elif activity.activity_type == "economy":
                        reward = random.randint(40, 100)
                        user.economy_successes += 1
                        user.economy_ticks += activity.ticks_requested

                    # Apply global multiplier
                    final_reward = self.global_multiplier.apply_multiplier_to_reward(
                        reward
                    )
                    user.rp += int(final_reward)
                    user.total_rp_earned += int(final_reward)
                    self.stats["total_rp_earned"] += int(final_reward)

                activity.is_complete = True
                user.current_activity = "idle"
                completed_activities.append(user_id)
                self.stats["activities_completed"] += 1

        # Remove completed activities
        for user_id in completed_activities:
            del self.active_activities[user_id]

    def update_global_multiplier(self):
        """Update global multiplier based on simulation state"""
        active_users = len(
            [u for u in self.users.values() if u.current_activity != "idle"]
        )
        total_users = len(self.users)

        # Simulate economy cycles
        drones_alive = random.randint(50, 200)
        drones_ever_died = random.randint(10, 100)

        self.global_multiplier.update_multiplier(
            drones_alive=drones_alive,
            active_players=active_users,
            drones_ever_died=drones_ever_died,
        )

        # Record economy cycle
        self.economy_cycles.append(
            {
                "tick": self.tick_count,
                "multiplier": self.global_multiplier.multiplier,
                "active_users": active_users,
                "drones_alive": drones_alive,
                "drones_ever_died": drones_ever_died,
            }
        )
        self.stats["economy_cycles"] += 1

    def generate_world_event(self):
        """Generate random world events"""
        events = [
            "🌪️ Economic Collapse - Compression costs reduced!",
            "📈 Market Boom - Higher rewards for all activities!",
            "⚡ Energy Surge - Mod activities more efficient!",
            "🌿 Resource Abundance - Hunt activities more profitable!",
            "🔧 System Update - All activities temporarily boosted!",
            "🌍 Global Harmony - Balanced economy state!",
        ]

        if random.random() < 0.1:  # 10% chance per tick
            event = random.choice(events)
            self.world_events.append({"tick": self.tick_count, "event": event})
            self.stats["world_events"] += 1
            return event
        return None

    def display_simulation_status(self):
        """Display comprehensive simulation status"""
        self.clear_screen()

        print("🌍 QUICK TEST SIMULATION - 30 SECONDS")
        print("=" * 80)
        print(
            f"⏰ Tick: {self.tick_count}/30 | Rate: {self.tick_rate:.1f} ticks/sec | Users: {len(self.users)}"
        )
        print(
            f"🌍 Global Multiplier: {self.global_multiplier.multiplier:.2f}x | Active: {len(self.active_activities)}"
        )
        print("=" * 80)

        # Show active activities
        if self.active_activities:
            print("\n🎯 ACTIVE ACTIVITIES:")
            print("-" * 60)
            for user_id, activity in self.active_activities.items():
                user = self.users[user_id]
                progress = (activity.ticks_completed / activity.ticks_requested) * 100
                color = (
                    "green" if progress >= 70 else "yellow" if progress >= 50 else "red"
                )
                bar = self.create_progress_bar(progress, 25, color)

                print(
                    f"  {user.name:<12} {activity.activity_type.upper()}: {bar} ({activity.ticks_completed}/{activity.ticks_requested})"
                )
        else:
            print("\n💤 No active activities")

        # Show user summary
        print("\n👥 USER SUMMARY:")
        print("-" * 60)

        user_types = {}
        for user in self.users.values():
            if user.user_type not in user_types:
                user_types[user.user_type] = {"count": 0, "total_rp": 0, "active": 0}
            user_types[user.user_type]["count"] += 1
            user_types[user.user_type]["total_rp"] += user.rp
            if user.current_activity != "idle":
                user_types[user.user_type]["active"] += 1

        for user_type, stats in user_types.items():
            avg_rp = stats["total_rp"] // stats["count"] if stats["count"] > 0 else 0
            print(
                f"  {user_type.value.title():<10}: {stats['count']:2d} users, {stats['active']:2d} active, avg {avg_rp:4d} RP"
            )

        # Show statistics
        print("\n📊 SIMULATION STATISTICS:")
        print("-" * 60)
        print(f"  Total Ticks: {self.stats['total_ticks']}")
        print(f"  Total Activities: {self.stats['total_activities']}")
        print(f"  Activities Completed: {self.stats['activities_completed']}")
        print(f"  Total RP Earned: {self.stats['total_rp_earned']}")
        print(f"  Total RP Spent: {self.stats['total_rp_spent']}")
        print(f"  Economy Cycles: {self.stats['economy_cycles']}")
        print(f"  World Events: {self.stats['world_events']}")

        # Show recent world events
        if self.world_events:
            print(f"\n🌍 Recent World Events:")
            print("-" * 60)
            for event in self.world_events[-3:]:  # Show last 3 events
                print(f"  Tick {event['tick']}: {event['event']}")

        # Show economy trend
        if len(self.economy_cycles) >= 2:
            recent_trend = (
                self.economy_cycles[-1]["multiplier"]
                - self.economy_cycles[-2]["multiplier"]
            )
            trend_emoji = (
                "📈" if recent_trend > 0 else "📉" if recent_trend < 0 else "➡️"
            )
            print(f"\n{trend_emoji} Economy Trend: {recent_trend:+.2f}")

        print("\n" + "=" * 80)
        print("🌍 Quick Test - 30 seconds of complete game experience!")
        print("=" * 80)

    def simulation_loop(self):
        """Main simulation loop"""
        while self.is_running and self.tick_count < self.simulation_duration:
            start_time = time.time()

            # Process tick
            self.process_tick()

            # Update global multiplier every 10 ticks
            if self.tick_count % 10 == 0:
                self.update_global_multiplier()

            # Generate world events
            world_event = self.generate_world_event()
            if world_event:
                print(f"\n🎉 {world_event}")

            # Display status
            self.display_simulation_status()

            # Wait for next tick
            elapsed = time.time() - start_time
            sleep_time = max(0, (1.0 / self.tick_rate) - elapsed)
            time.sleep(sleep_time)

        # Simulation complete
        self.is_running = False

    def start_simulation(self):
        """Start the quick test simulation"""
        print("🚀 Starting Quick Test Simulation...")
        print("🌍 30-second test with 10 users")
        print("⏱️ 1 tick/second heartbeat with entropy compression")
        print("🌍 Dynamic economy cycles and world events")
        print("=" * 80)

        self.create_simulation_users()

        # Start some initial activities
        for i in range(3):
            user_id = f"test_user_{i+1}"
            if user_id in self.users:
                self.generate_user_activity(user_id)

        self.is_running = True
        self.thread = threading.Thread(target=self.simulation_loop)
        self.thread.daemon = True
        self.thread.start()

        # Wait for simulation to complete
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏸️ Simulation interrupted by user")
            self.stop()

    def stop(self):
        """Stop the simulation"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1)

        print("\n🎉 Quick Test Complete!")
        print("=" * 80)
        self.save_results()

    def save_results(self):
        """Save comprehensive simulation results"""
        results_file = "quick_test_results.json"

        with open(results_file, "w") as f:
            json.dump(
                {
                    "simulation_timestamp": datetime.now().isoformat(),
                    "final_tick_count": self.tick_count,
                    "stats": self.stats,
                    "economy_cycles": self.economy_cycles,
                    "world_events": self.world_events,
                    "user_summary": {
                        user_id: {
                            "name": user.name,
                            "user_type": user.user_type.value,
                            "personality_traits": user.personality_traits,
                            "preferred_activities": user.preferred_activities,
                            "rp": user.rp,
                            "total_rp_earned": user.total_rp_earned,
                            "total_rp_spent": user.total_rp_spent,
                            "hunt_ticks": user.hunt_ticks,
                            "hunt_successes": user.hunt_successes,
                            "mod_ticks": user.mod_ticks,
                            "mod_successes": user.mod_successes,
                            "economy_ticks": user.economy_ticks,
                            "economy_successes": user.economy_successes,
                        }
                        for user_id, user in self.users.items()
                    },
                    "final_global_multiplier": self.global_multiplier.multiplier,
                },
                f,
                indent=2,
            )

        print(f"📊 Results saved to: {results_file}")

        # Print summary
        print("\n📋 Test Summary:")
        print("-" * 50)
        print(f"👥 Users: {len(self.users)}")
        print(f"⏰ Duration: {self.tick_count} ticks ({self.tick_count} seconds)")
        print(
            f"🎯 Activities: {self.stats['total_activities']} started, {self.stats['activities_completed']} completed"
        )
        print(
            f"💰 RP Economy: {self.stats['total_rp_earned']} earned, {self.stats['total_rp_spent']} spent"
        )
        print(f"🌍 Economy Cycles: {self.stats['economy_cycles']}")
        print(f"🎉 World Events: {self.stats['world_events']}")
        print(f"🌍 Final Multiplier: {self.global_multiplier.multiplier:.2f}x")
        print("\n✅ Quick test successful! Full simulation ready to run!")


def main():
    """Main function"""
    print("🚀 Starting Quick Test Simulation")
    print("=" * 60)

    engine = QuickTestSimulation()
    engine.start_simulation()


if __name__ == "__main__":
    main()
