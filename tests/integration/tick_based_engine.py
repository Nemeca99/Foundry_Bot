#!/usr/bin/env python3
"""
Tick-Based Engine
Real-time simulation with 1 tick/second heartbeat and exponential scaling
"""

import sys
import os
import json
import time
import random
import threading
from datetime import datetime
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
class TickUser:
    """User with tick-based progression"""

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
    last_tick: float = 0.0

    def __post_init__(self):
        self.last_tick = time.time()


@dataclass
class TickActivity:
    """Activity that consumes ticks"""

    user_id: str
    activity_type: str  # "hunt", "mod", "economy"
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
        # This makes compression cost scale with world entropy
        compression_multiplier = self.ticks_requested * global_multiplier

        return int(base_over_cost * compression_multiplier)


class TickBasedEngine:
    """Real-time tick-based engine with exponential scaling"""

    def __init__(self):
        self.mod_system = ModSystem("data/tick_based_mods.db")
        self.global_multiplier = GlobalRewardMultiplier(self.mod_system)

        self.users = {}
        self.active_activities = {}
        self.tick_count = 0
        self.tick_rate = 1.0  # 1 tick per second
        self.is_running = False
        self.thread = None

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
            "errors": [],
        }

        print("⏱️ Tick-Based Engine Initialized")
        print("🔧 Real-time simulation with exponential scaling")

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

    def create_test_users(self, count: int = 6):
        """Create test users with different types"""
        print(f"\n👥 Creating {count} tick-based test users...")

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
            user_id = f"tick_user_{i+1}"

            # Different RP based on user type
            rp_base = {
                UserType.NOOB: (50, 100),
                UserType.CASUAL: (100, 200),
                UserType.REGULAR: (200, 400),
                UserType.VETERAN: (400, 800),
                UserType.EXPERT: (800, 1500),
                UserType.MASTER: (1500, 3000),
            }

            min_rp, max_rp = rp_base[user_type]
            rp = random.randint(min_rp, max_rp)

            user = TickUser(
                id=user_id,
                name=f"{type_names[user_type]}{i+1}",
                user_type=user_type,
                rp=rp,
            )
            self.users[user_id] = user

        print(f"✅ Created {count} tick-based test users")

    def start_hunt_activity(self, user_id: str, ticks: int = 1):
        """Start a hunt activity with exponential scaling"""
        if user_id not in self.users:
            return False

        user = self.users[user_id]

        # Calculate cost with entropy compression
        base_cost = 100  # Base hunt cost
        activity = TickActivity(
            user_id=user_id,
            activity_type="hunt",
            ticks_requested=ticks,
            base_cost=base_cost,
            success_rate=self.get_hunt_success_rate(user.user_type),
        )
        # Calculate cost with current global multiplier
        activity.total_cost = activity.calculate_total_cost(
            self.global_multiplier.multiplier
        )

        # Check if user can afford it
        if user.rp < activity.total_cost:
            print(
                f"❌ {user.name} cannot afford hunt: {activity.total_cost} RP (has {user.rp} RP)"
            )
            return False

        # Deduct RP
        user.rp -= activity.total_cost
        user.total_rp_spent += activity.total_cost

        # Add to active activities
        self.active_activities[user_id] = activity
        user.current_activity = f"hunt({ticks}x)"

        print(
            f"🏹 {user.name} started hunt: {ticks}x ticks for {activity.total_cost} RP"
        )
        return True

    def start_mod_activity(self, user_id: str, ticks: int = 1):
        """Start a mod activity with exponential scaling"""
        if user_id not in self.users:
            return False

        user = self.users[user_id]

        # Calculate cost with entropy compression
        base_cost = 150  # Base mod cost
        activity = TickActivity(
            user_id=user_id,
            activity_type="mod",
            ticks_requested=ticks,
            base_cost=base_cost,
            success_rate=self.get_mod_success_rate(user.user_type),
        )
        # Calculate cost with current global multiplier
        activity.total_cost = activity.calculate_total_cost(
            self.global_multiplier.multiplier
        )

        # Check if user can afford it
        if user.rp < activity.total_cost:
            print(
                f"❌ {user.name} cannot afford mod: {activity.total_cost} RP (has {user.rp} RP)"
            )
            return False

        # Deduct RP
        user.rp -= activity.total_cost
        user.total_rp_spent += activity.total_cost

        # Add to active activities
        self.active_activities[user_id] = activity
        user.current_activity = f"mod({ticks}x)"

        print(
            f"🔧 {user.name} started mod: {ticks}x ticks for {activity.total_cost} RP"
        )
        return True

    def start_economy_activity(self, user_id: str, ticks: int = 1):
        """Start an economy activity with exponential scaling"""
        if user_id not in self.users:
            return False

        user = self.users[user_id]

        # Calculate cost with entropy compression
        base_cost = 75  # Base economy cost
        activity = TickActivity(
            user_id=user_id,
            activity_type="economy",
            ticks_requested=ticks,
            base_cost=base_cost,
            success_rate=self.get_economy_success_rate(user.user_type),
        )
        # Calculate cost with current global multiplier
        activity.total_cost = activity.calculate_total_cost(
            self.global_multiplier.multiplier
        )

        # Check if user can afford it
        if user.rp < activity.total_cost:
            print(
                f"❌ {user.name} cannot afford economy: {activity.total_cost} RP (has {user.rp} RP)"
            )
            return False

        # Deduct RP
        user.rp -= activity.total_cost
        user.total_rp_spent += activity.total_cost

        # Add to active activities
        self.active_activities[user_id] = activity
        user.current_activity = f"econ({ticks}x)"

        print(
            f"💰 {user.name} started economy: {ticks}x ticks for {activity.total_cost} RP"
        )
        return True

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
        """Process one tick for all active activities"""
        self.tick_count += 1
        self.stats["total_ticks"] += 1

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

                    print(
                        f"✅ {user.name} {activity.activity_type} SUCCESS: +{int(final_reward)} RP"
                    )
                else:
                    print(f"❌ {user.name} {activity.activity_type} FAILED: No reward")

                activity.is_complete = True
                user.current_activity = "idle"
                completed_activities.append(user_id)
                self.stats["activities_completed"] += 1

        # Remove completed activities
        for user_id in completed_activities:
            del self.active_activities[user_id]

    def display_status(self):
        """Display beautiful real-time status"""
        self.clear_screen()

        print("⏱️ TICK-BASED ENGINE - REAL-TIME SIMULATION")
        print("=" * 80)
        print(
            f"⏰ Tick: {self.tick_count} | Rate: {self.tick_rate:.1f} ticks/sec | Active: {len(self.active_activities)}"
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

        # Show user status
        print("\n👥 USER STATUS:")
        print("-" * 60)
        for user_id, user in self.users.items():
            status_color = "green" if user.current_activity == "idle" else "yellow"
            activity_display = (
                user.current_activity if user.current_activity != "idle" else "IDLE"
            )

            print(
                f"  {user.name:<12} RP: {user.rp:4d} | Activity: {self.colors[status_color]}{activity_display}{self.colors['reset']}"
            )

        # Show statistics
        print("\n📊 STATISTICS:")
        print("-" * 60)
        print(f"  Total Ticks: {self.stats['total_ticks']}")
        print(f"  Total Activities: {self.stats['total_activities']}")
        print(f"  Activities Completed: {self.stats['activities_completed']}")
        print(f"  Total RP Earned: {self.stats['total_rp_earned']}")
        print(f"  Total RP Spent: {self.stats['total_rp_spent']}")

        # Show global multiplier
        print(f"\n🌍 Global Multiplier: {self.global_multiplier.multiplier:.2f}x")

        print("\n" + "=" * 80)
        print("Commands: !hunt <ticks> | !mod <ticks> | !econ <ticks> | !quit")
        print("=" * 80)

    def run_command(self, command: str):
        """Process user command"""
        parts = command.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()

        if cmd == "!hunt" and len(parts) >= 2:
            try:
                ticks = int(parts[1])
                if ticks > 0:
                    # Start hunt for first available user
                    for user_id in self.users:
                        if user_id not in self.active_activities:
                            self.start_hunt_activity(user_id, ticks)
                            break
            except ValueError:
                print("❌ Invalid tick count")

        elif cmd == "!mod" and len(parts) >= 2:
            try:
                ticks = int(parts[1])
                if ticks > 0:
                    # Start mod for first available user
                    for user_id in self.users:
                        if user_id not in self.active_activities:
                            self.start_mod_activity(user_id, ticks)
                            break
            except ValueError:
                print("❌ Invalid tick count")

        elif cmd == "!econ" and len(parts) >= 2:
            try:
                ticks = int(parts[1])
                if ticks > 0:
                    # Start economy for first available user
                    for user_id in self.users:
                        if user_id not in self.active_activities:
                            self.start_economy_activity(user_id, ticks)
                            break
            except ValueError:
                print("❌ Invalid tick count")

        elif cmd == "!quit":
            self.stop()

    def tick_loop(self):
        """Main tick loop"""
        while self.is_running:
            start_time = time.time()

            # Process tick
            self.process_tick()

            # Update global multiplier occasionally
            if self.tick_count % 10 == 0:
                self.global_multiplier.update_multiplier(
                    drones_alive=random.randint(50, 200),
                    active_players=len(self.users),
                    drones_ever_died=random.randint(10, 100),
                )

            # Display status
            self.display_status()

            # Wait for next tick
            elapsed = time.time() - start_time
            sleep_time = max(0, (1.0 / self.tick_rate) - elapsed)
            time.sleep(sleep_time)

    def start(self):
        """Start the tick-based engine"""
        print("🚀 Starting Tick-Based Engine...")
        print("⏱️ 1 tick/second heartbeat with exponential scaling")
        print("💰 RP = Time, exponential cost scaling for multiple ticks")
        print("=" * 80)

        self.create_test_users(6)

        # Start some initial activities
        self.start_hunt_activity("tick_user_1", 3)
        self.start_mod_activity("tick_user_2", 2)
        self.start_economy_activity("tick_user_3", 4)

        self.is_running = True
        self.thread = threading.Thread(target=self.tick_loop)
        self.thread.daemon = True
        self.thread.start()

        # Command input loop
        try:
            while self.is_running:
                command = input()
                self.run_command(command)
        except KeyboardInterrupt:
            print("\n⏸️ Interrupted by user")
            self.stop()

    def stop(self):
        """Stop the tick-based engine"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1)

        print("\n🎉 Tick-Based Engine Stopped")
        print("=" * 80)
        self.save_results()

    def save_results(self):
        """Save final results"""
        results_file = "tick_based_results.json"

        with open(results_file, "w") as f:
            json.dump(
                {
                    "test_timestamp": datetime.now().isoformat(),
                    "final_tick_count": self.tick_count,
                    "stats": self.stats,
                    "user_summary": {
                        user_id: {
                            "name": user.name,
                            "user_type": user.user_type.value,
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
                    "global_multiplier": self.global_multiplier.multiplier,
                },
                f,
                indent=2,
            )

        print(f"📊 Results saved to: {results_file}")


def main():
    """Main function"""
    print("🚀 Starting Tick-Based Engine")
    print("=" * 60)

    engine = TickBasedEngine()
    engine.start()


if __name__ == "__main__":
    main()
