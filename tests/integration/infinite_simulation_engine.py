"""
Infinite Simulation Engine - Sim-Rancher Live Mod System

FIXED COST SYSTEM:
- Base costs are FIXED (no inflation from base costs)
- Hunt: 100 RP, Mod: 150 RP, Economy: 75 RP, Fight: 200 RP
- Global multiplier applies FIRST to base cost, then entropy compression
- Global multiplier: (drones_alive * active_players) / drones_ever_died
- Caps: Max 3.0x, Min 0.1x
- Every action MUST cost RP (minimum 1 RP)

ENTROPY COMPRESSION:
- Multi-tick actions cost exponentially more
- Formula: (global_modified_cost * 2) * ticks_requested
- Global multiplier affects base cost before compression

ECONOMY BALANCE:
- High drone survival = higher multiplier = more expensive actions
- Mass drone deaths = lower multiplier = cheaper actions
- Player-driven feedback loop maintains economic balance
"""

import time
import random
import json
import os
import sys
import threading
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any

# Import standalone systems that don't require Discord
from standalone_mod_system import StandaloneModSystem, StandaloneGlobalRewardMultiplier


# Standalone economy system for simulation
class StandaloneEconomySystem:
    """Standalone economy system for simulation"""

    def __init__(self):
        self.mod_system = StandaloneModSystem()
        self.global_multiplier = StandaloneGlobalRewardMultiplier()
        self.transactions = []

    def earn_rp(self, user_id: str, amount: int, reason: str = "Activity") -> int:
        """Earn RP with global multiplier applied"""
        current_multiplier = self.global_multiplier.get_current_multiplier()
        modified_amount = int(amount * current_multiplier)

        # Update player profile
        profile = self.mod_system.get_player_profile(user_id)
        if profile:
            profile.total_rp_earned += modified_amount
            self.mod_system.update_player_profile(profile)

        return modified_amount

    def spend_rp(self, user_id: str, amount: int, reason: str = "Activity") -> bool:
        """Spend RP and track transaction"""
        # Update player profile
        profile = self.mod_system.get_player_profile(user_id)
        if profile:
            profile.total_rp_spent += amount
            self.mod_system.update_player_profile(profile)

        return True

    def get_user_rp(self, user_id: str) -> int:
        """Get user's current RP balance"""
        profile = self.mod_system.get_player_profile(user_id)
        if profile:
            return profile.total_rp_earned - profile.total_rp_spent
        return 0


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
    """User in the infinite simulation"""

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
    fight_ticks: int = 0
    fight_successes: int = 0
    current_activity: str = "idle"
    last_activity: float = 0.0
    activity_cooldown: float = 0.0
    personality_traits: List[str] = None
    preferred_activities: List[str] = None
    join_date: str = ""
    last_seen: float = 0.0
    is_online: bool = True
    days_active: int = 0

    # Drone tracking
    drone_count: int = 5
    total_drones_gained: int = 0
    total_drones_lost: int = 0
    max_drones: int = 20

    # Enhanced statistics
    total_activities_completed: int = 0
    total_events_participated: int = 0
    total_channel_moves: int = 0
    total_simulacra_deaths: int = 0
    current_concurrent_activities: int = 0
    max_concurrent_activities: int = 5

    # Event flocking
    event_preferences: Dict[str, float] = None
    last_event_reaction: float = 0.0

    def __post_init__(self):
        self.last_activity = time.time()
        self.last_seen = time.time()
        self.join_date = datetime.now().isoformat()
        if self.personality_traits is None:
            self.personality_traits = self.generate_personality()
        if self.preferred_activities is None:
            self.preferred_activities = self.generate_preferences()
        if self.event_preferences is None:
            self.event_preferences = {
                "hunt": 1.0,
                "mod": 1.0,
                "economy": 1.0,
                "fight": 1.0,
            }

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

    def update_online_status(self):
        """Update online status based on activity"""
        current_time = time.time()
        time_since_last_seen = current_time - self.last_seen

        # User goes offline after 5 minutes of inactivity
        if time_since_last_seen > 300:  # 5 minutes
            self.is_online = False
        else:
            self.is_online = True
            self.last_seen = current_time

    def can_start_activity(self) -> bool:
        """Check if user can start a new activity (max 5 concurrent)"""
        return self.current_concurrent_activities < self.max_concurrent_activities

    def start_activity(self):
        """Increment concurrent activity count"""
        self.current_concurrent_activities += 1

    def end_activity(self):
        """Decrement concurrent activity count"""
        self.current_concurrent_activities = max(
            0, self.current_concurrent_activities - 1
        )

    def lose_drone(self, reason: str = "unknown"):
        """Lose a drone and track the loss"""
        if self.drone_count > 0:
            self.drone_count -= 1
            self.total_drones_lost += 1
            self.total_simulacra_deaths += 1
            return True
        return False

    def gain_drone(self, reason: str = "unknown"):
        """Gain a drone and track the gain"""
        if self.drone_count < self.max_drones:
            self.drone_count += 1
            self.total_drones_gained += 1
            return True
        return False

    def react_to_event(self, event_type: str, is_positive: bool):
        """React to world events by adjusting preferences"""
        current_time = time.time()
        if current_time - self.last_event_reaction > 60:  # Only react once per minute
            self.last_event_reaction = current_time

            if is_positive:
                # Increase preference for related activities
                if "hunt" in event_type.lower():
                    self.event_preferences["hunt"] = min(
                        2.0, self.event_preferences["hunt"] * 1.5
                    )
                elif "mod" in event_type.lower():
                    self.event_preferences["mod"] = min(
                        2.0, self.event_preferences["mod"] * 1.5
                    )
                elif "economy" in event_type.lower():
                    self.event_preferences["economy"] = min(
                        2.0, self.event_preferences["economy"] * 1.5
                    )
                elif "fight" in event_type.lower():
                    self.event_preferences["fight"] = min(
                        2.0, self.event_preferences["fight"] * 1.5
                    )
            else:
                # Decrease preference for related activities
                if "hunt" in event_type.lower():
                    self.event_preferences["hunt"] = max(
                        0.5, self.event_preferences["hunt"] * 0.8
                    )
                elif "mod" in event_type.lower():
                    self.event_preferences["mod"] = max(
                        0.5, self.event_preferences["mod"] * 0.8
                    )
                elif "economy" in event_type.lower():
                    self.event_preferences["economy"] = max(
                        0.5, self.event_preferences["economy"] * 0.8
                    )
                elif "fight" in event_type.lower():
                    self.event_preferences["fight"] = max(
                        0.5, self.event_preferences["fight"] * 0.8
                    )


@dataclass
class SimulationActivity:
    """Activity in the infinite simulation"""

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
        # Cost will be calculated when activity is started with proper global multiplier

    def calculate_total_cost(self, global_multiplier: float = 1.0) -> int:
        """Calculate cost with global multiplier applied FIRST to base cost"""
        # Apply global multiplier to base cost FIRST (before entropy compression)
        global_modified_cost = int(self.base_cost * global_multiplier)

        # Ensure minimum cost of 1 RP (no free actions)
        if global_modified_cost < 1:
            global_modified_cost = 1

        if self.ticks_requested <= 1:
            return global_modified_cost

        # Entropy compression: base_over_cost × ticks_requested
        # (global multiplier already applied to base_cost above)
        base_over_cost = global_modified_cost * 2
        compression_cost = base_over_cost * self.ticks_requested

        return int(compression_cost)


class InfiniteSimulationEngine:
    """Infinite simulation engine with day tracking"""

    def __init__(self, mode="real_time"):
        self.mod_system = StandaloneModSystem("data/infinite_simulation_mods.db")
        self.global_multiplier = StandaloneGlobalRewardMultiplier(
            "data/infinite_simulation_global_multiplier.db"
        )
        self.economy_system = StandaloneEconomySystem()

        self.users = {}
        self.active_activities = {}
        self.tick_count = 0
        self.tick_rate = 1.0  # 1 tick per second
        self.is_running = False
        self.thread = None

        # Day tracking settings
        self.ticks_per_day = 86400  # 24 hours * 60 minutes * 60 seconds = 86400 ticks
        self.current_day = 1
        self.day_start_tick = 0

        # Simulation settings
        self.initial_user_count = 100  # Start with 100 users
        self.current_user_count = 100
        self.economy_cycles = []
        self.world_events = []
        self.daily_stats = []

        # Dynamic user management
        self.user_join_rate = 0.05  # 5% chance per day for new user
        self.user_leave_rate = 0.02  # 2% chance per day for user to leave
        self.max_users = 500  # Maximum users allowed
        self.min_users = 50  # Minimum users to maintain
        self.users_joined_today = 0
        self.users_left_today = 0
        self.total_users_joined = 0
        self.total_users_left = 0

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
            "days_completed": 0,
            "total_users_joined": 0,
            "total_users_left": 0,
            "peak_users": 100,
            "total_drones_gained": 0,
            "total_drones_lost": 0,
            "total_simulacra_deaths": 0,
            "total_channel_moves": 0,
            "errors": [],
        }

        self.idle_ticks = 0
        self.entropy_breach_active = False
        self.entropy_breach_bonus_users = set()

        self.simulation_mode = mode
        if mode == "fast":
            self.ticks_per_day = 8640  # 86400 / 10
            self.tick_rate = 1.0
            self.sim_seconds_per_tick = 10
            self.display_interval = 10  # Show status every 10 ticks
            mode_description = "FAST (1 tick = 10s)"
        elif mode == "daily":
            self.ticks_per_day = (
                86400  # 1 tick = 1 day, but we need 86400 ticks to represent that day
            )
            self.tick_rate = 1.0
            self.sim_seconds_per_tick = (
                1  # 1 real second = 1 tick, but 86400 ticks = 1 simulated day
            )
            self.display_interval = (
                1000  # Show status every 1000 ticks (about 11.6 minutes)
            )
            mode_description = "DAILY (86400 ticks = 1 day)"
        elif mode == "weekly":
            self.ticks_per_day = 604800  # 1 tick = 1 week, but we need 604800 ticks to represent that week
            self.tick_rate = 1.0
            self.sim_seconds_per_tick = (
                1  # 1 real second = 1 tick, but 604800 ticks = 1 simulated week
            )
            self.display_interval = (
                10000  # Show status every 10000 ticks (about 1.7 hours)
            )
            mode_description = "WEEKLY (604800 ticks = 1 week)"
        elif mode == "monthly":
            self.ticks_per_day = 2592000  # 1 tick = 1 month, but we need 2592000 ticks to represent that month
            self.tick_rate = 1.0
            self.sim_seconds_per_tick = (
                1  # 1 real second = 1 tick, but 2592000 ticks = 1 simulated month
            )
            self.display_interval = (
                100000  # Show status every 100000 ticks (about 1.1 days)
            )
            mode_description = "MONTHLY (2592000 ticks = 1 month)"
        else:  # real_time
            self.ticks_per_day = 86400
            self.tick_rate = 1.0
            self.sim_seconds_per_tick = 1
            self.display_interval = 1  # Show status every tick for real-time
            mode_description = "REAL TIME (1 tick = 1s)"

        print(f"\nSimulation Mode: {mode_description}\n")

        print("🌍 Infinite Simulation Engine Initialized")
        print("🎮 Runs indefinitely with day tracking")
        print(f"⏰ {self.ticks_per_day} ticks = 1 simulated day")
        print(f"⏱️ 1 real second = 1 tick")
        print(f"👥 Starting with {self.initial_user_count} users")
        print(f"📈 Dynamic user base: {self.min_users}-{self.max_users} users")

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

    def calculate_day_progress(self) -> float:
        """Calculate progress through current day"""
        ticks_into_day = self.tick_count - self.day_start_tick
        return (ticks_into_day / self.ticks_per_day) * 100

    def check_day_completion(self):
        """Check if a new day has started"""
        ticks_into_day = self.tick_count - self.day_start_tick

        if ticks_into_day >= self.ticks_per_day:
            # Day completed
            self.current_day += 1
            self.day_start_tick = self.tick_count
            self.stats["days_completed"] += 1

            # Record daily stats
            daily_stat = {
                "day": self.current_day - 1,  # The day that just completed
                "tick_count": self.tick_count,
                "total_activities": self.stats["total_activities"],
                "activities_completed": self.stats["activities_completed"],
                "total_rp_earned": self.stats["total_rp_earned"],
                "total_rp_spent": self.stats["total_rp_spent"],
                "economy_cycles": self.stats["economy_cycles"],
                "world_events": self.stats["world_events"],
                "global_multiplier": self.global_multiplier.get_current_multiplier(),
                "active_users": len(
                    [u for u in self.users.values() if u.current_activity != "idle"]
                ),
                "total_users": len(self.users),
                "online_users": len([u for u in self.users.values() if u.is_online]),
                "users_joined_today": self.users_joined_today,
                "users_left_today": self.users_left_today,
                "total_users_joined": self.stats["total_users_joined"],
                "total_users_left": self.stats["total_users_left"],
                "peak_users": self.stats["peak_users"],
                "timestamp": datetime.now().isoformat(),
            }
            self.daily_stats.append(daily_stat)

            print(f"\n🌅 DAY {self.current_day - 1} COMPLETED!")
            print(
                f"📊 Day Summary: {daily_stat['activities_completed']} activities, {daily_stat['total_rp_earned']} RP earned"
            )
            print(
                f"👥 Users: {daily_stat['total_users']} total, {daily_stat['online_users']} online"
            )
            print(
                f"📈 Growth: +{daily_stat['users_joined_today']} / -{daily_stat['users_left_today']}"
            )
            print(f"�� Global Multiplier: {daily_stat['global_multiplier']:.2f}x")
            print("=" * 80)

    def create_simulation_users(self):
        """Create realistic simulation users"""
        print(f"\n👥 Creating {self.initial_user_count} simulation users...")

        user_types = list(UserType)
        type_names = {
            UserType.NOOB: "Noob",
            UserType.CASUAL: "Casual",
            UserType.REGULAR: "Regular",
            UserType.VETERAN: "Veteran",
            UserType.EXPERT: "Expert",
            UserType.MASTER: "Master",
        }

        for i in range(self.initial_user_count):
            user_type = user_types[i % len(user_types)]
            user_id = f"sim_user_{i+1}"

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

        print(f"✅ Created {self.initial_user_count} simulation users")

    def add_new_user(self):
        """Add a new user to the simulation"""
        if len(self.users) >= self.max_users:
            return False

        user_types = list(UserType)
        type_names = {
            UserType.NOOB: "Noob",
            UserType.CASUAL: "Casual",
            UserType.REGULAR: "Regular",
            UserType.VETERAN: "Veteran",
            UserType.EXPERT: "Expert",
            UserType.MASTER: "Master",
        }

        # Choose user type with realistic distribution
        type_weights = {
            UserType.NOOB: 0.4,  # 40% new users
            UserType.CASUAL: 0.3,  # 30% casual users
            UserType.REGULAR: 0.2,  # 20% regular users
            UserType.VETERAN: 0.07,  # 7% veteran users
            UserType.EXPERT: 0.02,  # 2% expert users
            UserType.MASTER: 0.01,  # 1% master users
        }

        user_type = random.choices(
            user_types, weights=[type_weights[t] for t in user_types]
        )[0]

        # Generate unique user ID
        user_id = f"sim_user_{len(self.users) + 1}_{int(time.time())}"

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
            name=f"{type_names[user_type]}{len(self.users) + 1}",
            user_type=user_type,
            rp=rp,
        )

        self.users[user_id] = user
        self.current_user_count = len(self.users)
        self.users_joined_today += 1
        self.total_users_joined += 1
        self.stats["total_users_joined"] += 1

        if self.current_user_count > self.stats["peak_users"]:
            self.stats["peak_users"] = self.current_user_count

        return True

    def remove_user(self, user_id: str):
        """Remove a user from the simulation"""
        if user_id in self.users:
            del self.users[user_id]
            self.current_user_count = len(self.users)
            self.users_left_today += 1
            self.total_users_left += 1
            self.stats["total_users_left"] += 1
            return True
        return False

    def manage_user_population(self, num_changes, activity_summary):
        """Manage user population with realistic join/leave patterns"""
        current_population = len(self.users)

        # Determine if we should add or remove users based on current population
        if current_population <= self.min_users:
            # Low population - prioritize joins
            action = "join"
        elif current_population >= self.max_users:
            # High population - prioritize leaves
            action = "leave"
        else:
            # Balanced population - 50/50 chance
            action = random.choice(["join", "leave"])

        # Prefer to remove inactive users when leaving
        if action == "leave":
            inactive_users = [
                uid for uid, user in self.users.items() if not user.is_online
            ]
            active_users = [uid for uid, user in self.users.items() if user.is_online]

            # 70% chance to remove inactive user if available
            if inactive_users and random.random() < 0.7:
                users_to_remove = inactive_users
            else:
                users_to_remove = list(self.users.keys())

            # Remove users
            for _ in range(min(num_changes, len(users_to_remove))):
                if users_to_remove:
                    user_id = random.choice(users_to_remove)
                    users_to_remove.remove(user_id)
                    self.remove_user(user_id)
                    self.users_left_today += 1
                    self.total_users_left += 1
                    activity_summary["users_left"] += 1
        else:
            # Add users
            for _ in range(num_changes):
                if current_population < self.max_users:
                    self.add_new_user()
                    self.users_joined_today += 1
                    self.total_users_joined += 1
                    activity_summary["users_joined"] += 1

        # Update online status for all users
        for user in self.users.values():
            user.update_online_status()

    def simulate_channel_move(self, user_id: str) -> bool:
        """Simulate a user moving channels with 1% chance of drone death"""
        user = self.users[user_id]

        # 1% chance of simulacra death when moving channels
        if random.random() < 0.01:
            if user.lose_drone("channel_move"):
                user.total_channel_moves += 1
                return True

        # Regular channel move (no death)
        user.total_channel_moves += 1
        return True

    def generate_user_activity(self, user_id: str):
        """Generate realistic user activity based on personality and event preferences"""
        user = self.users[user_id]

        # Check if user can start more activities (max 5 concurrent)
        if not user.can_start_activity():
            return

        # Check if user is on cooldown
        if time.time() - user.last_activity < user.activity_cooldown:
            return

        # Determine activity based on preferences, personality, and event reactions
        activity_chances = {}

        # Base chances from preferences
        for activity in user.preferred_activities:
            if activity == "hunt":
                activity_chances["hunt"] = 0.4 * user.event_preferences["hunt"]
            elif activity == "mod":
                activity_chances["mod"] = 0.3 * user.event_preferences["mod"]
            elif activity == "economy":
                activity_chances["economy"] = 0.2 * user.event_preferences["economy"]

        # Add fighting chance (everyone can fight)
        activity_chances["fight"] = 0.1 * user.event_preferences["fight"]

        # Normalize chances
        total_chance = sum(activity_chances.values())
        if total_chance > 0:
            activity_chances = {
                k: v / total_chance for k, v in activity_chances.items()
            }
        else:
            # Default chances if no preferences
            activity_chances = {"hunt": 0.4, "mod": 0.3, "economy": 0.2, "fight": 0.1}

        # Choose activity based on weighted chances
        activities = list(activity_chances.keys())
        weights = list(activity_chances.values())

        if activities and weights:
            chosen_activity = random.choices(activities, weights=weights)[0]

            if chosen_activity == "hunt":
                self.start_user_hunt(user_id)
            elif chosen_activity == "mod":
                self.start_user_mod(user_id)
            elif chosen_activity == "economy":
                self.start_user_economy(user_id)
            elif chosen_activity == "fight":
                self.start_user_fight(user_id)

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
            self.global_multiplier.get_current_multiplier()
        )

        # Check if user can afford it
        if user.rp < activity.total_cost:
            return

        # Deduct RP and start activity
        user.rp -= activity.total_cost
        user.total_rp_spent += activity.total_cost
        user.start_activity()  # Increment concurrent activity count
        user.last_activity = time.time()
        user.activity_cooldown = random.uniform(5, 15)

        # Create unique activity ID for multiple concurrent activities
        activity_id = f"{user_id}_hunt_{int(time.time())}"
        self.active_activities[activity_id] = activity
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
            self.global_multiplier.get_current_multiplier()
        )

        if user.rp < activity.total_cost:
            return

        user.rp -= activity.total_cost
        user.total_rp_spent += activity.total_cost
        user.start_activity()  # Increment concurrent activity count
        user.last_activity = time.time()
        user.activity_cooldown = random.uniform(8, 20)

        # Create unique activity ID
        activity_id = f"{user_id}_mod_{int(time.time())}"
        self.active_activities[activity_id] = activity
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
            self.global_multiplier.get_current_multiplier()
        )

        if user.rp < activity.total_cost:
            return

        user.rp -= activity.total_cost
        user.total_rp_spent += activity.total_cost
        user.start_activity()  # Increment concurrent activity count
        user.last_activity = time.time()
        user.activity_cooldown = random.uniform(3, 10)

        # Create unique activity ID
        activity_id = f"{user_id}_econ_{int(time.time())}"
        self.active_activities[activity_id] = activity
        self.stats["total_activities"] += 1

    def start_user_fight(self, user_id: str):
        """Start a fight activity for a user"""
        user = self.users[user_id]
        if not user.can_start_activity():
            return

        # Create fight activity
        ticks = random.randint(2, 4)
        activity = SimulationActivity(
            user_id=user_id,
            activity_type="fight",
            ticks_requested=ticks,
            base_cost=25,
        )

        # Calculate cost with global multiplier
        total_cost = activity.calculate_total_cost(
            self.global_multiplier.get_current_multiplier()
        )

        # Check if user can afford it
        if user.rp >= total_cost:
            # Deduct RP
            user.rp -= total_cost
            user.total_rp_spent += total_cost

            # Start activity
            activity.ticks_remaining = ticks
            activity.total_cost = total_cost
            activity_id = f"{user_id}_fight_{int(time.time())}"
            self.active_activities[activity_id] = activity
            user.start_activity()
            self.stats["total_activities"] += 1

    def start_user_activity(self, user):
        """Start a new activity for a user"""
        if not user.can_start_activity():
            return

        # Choose activity type based on user preferences
        activity_type = random.choice(user.preferred_activities)

        # Determine ticks based on activity type
        if activity_type == "hunt":
            ticks = random.randint(3, 8)
            base_cost = 50
        elif activity_type == "mod":
            ticks = random.randint(5, 12)
            base_cost = 100
        elif activity_type == "economy":
            ticks = random.randint(2, 6)
            base_cost = 75
        elif activity_type == "fight":
            ticks = random.randint(2, 4)
            base_cost = 25
        else:
            ticks = random.randint(3, 6)
            base_cost = 50

        # Create activity
        activity = SimulationActivity(
            user_id=user.id,
            activity_type=activity_type,
            ticks_requested=ticks,
            base_cost=base_cost,
        )

        # Calculate cost with global multiplier
        total_cost = activity.calculate_total_cost(
            self.global_multiplier.get_current_multiplier()
        )

        # Check if user can afford it
        if user.rp >= total_cost:
            # Deduct RP
            user.rp -= total_cost
            user.total_rp_spent += total_cost

            # Start activity
            activity.ticks_remaining = ticks
            activity.total_cost = total_cost
            activity_id = f"{user.id}_{activity_type}_{int(time.time())}"
            self.active_activities[activity_id] = activity
            user.start_activity()

            # Update user stats
            if activity_type == "hunt":
                user.hunt_ticks += ticks
            elif activity_type == "mod":
                user.mod_ticks += ticks
            elif activity_type == "economy":
                user.economy_ticks += ticks
            elif activity_type == "fight":
                user.fight_ticks += ticks

    def get_activity_success_chance(self, user, activity_type: str) -> float:
        """Get success chance for an activity based on user type"""
        if activity_type == "hunt":
            return self.get_hunt_success_rate(user.user_type)
        elif activity_type == "mod":
            return self.get_mod_success_rate(user.user_type)
        elif activity_type == "economy":
            return self.get_economy_success_rate(user.user_type)
        elif activity_type == "fight":
            return self.get_fight_success_rate(user.user_type)
        else:
            return 0.5

    def calculate_activity_reward(self, user, activity_type: str) -> int:
        """Calculate reward for successful activity"""
        base_rewards = {"hunt": 50, "mod": 100, "economy": 75, "fight": 25}
        base_reward = base_rewards.get(activity_type, 50)

        # Apply global multiplier to reward
        return int(base_reward * self.global_multiplier.get_current_multiplier())

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

    def get_fight_success_rate(self, user_type: UserType) -> float:
        """Get fight success rate based on user type"""
        rates = {
            UserType.NOOB: 0.2,
            UserType.CASUAL: 0.4,
            UserType.REGULAR: 0.6,
            UserType.VETERAN: 0.7,
            UserType.EXPERT: 0.8,
            UserType.MASTER: 0.9,
        }
        return rates.get(user_type, 0.5)

    def check_for_stillness(self):
        """Detects if all users are idle for 50+ ticks and injects entropy event."""
        if all(u.current_activity == "idle" for u in self.users.values()):
            self.idle_ticks += 1
        else:
            self.idle_ticks = 0
            self.entropy_breach_active = False
            self.entropy_breach_bonus_users.clear()
        # Trigger at 50 idle ticks or at tick 601
        if (
            self.idle_ticks == 50 or self.tick_count == 601
        ) and not self.entropy_breach_active:
            self.inject_entropy_breach()

    def inject_entropy_breach(self):
        """Injects an entropy breach event: -1 RP to all idle users, +25 RP to first 5 to act."""
        for user in self.users.values():
            if user.current_activity == "idle":
                user.rp = max(0, user.rp - 1)
        eligible = [u for u in self.users.values() if u.current_activity == "idle"]
        bonus_users = random.sample(eligible, min(5, len(eligible)))
        self.entropy_breach_bonus_users = set(u.id for u in bonus_users)
        self.entropy_breach_active = True
        self.world_events.append(
            {
                "type": "entropy_breach",
                "description": f"[Tick {self.tick_count}] — Entropy Breach Detected. All RP-holders feel a cold weight descend… -1 RP to all inactive users. First 5 users to act this cycle will gain +25 RP bonus.",
                "is_positive": True,
                "timestamp": time.time(),
            }
        )
        print(
            f"\n🩸 [Tick {self.tick_count}] — Entropy Breach Detected. All RP-holders feel a cold weight descend… -1 RP to all inactive users. First 5 users to act this cycle will gain +25 RP bonus.\n"
        )

    def reward_entropy_breach_bonus(self, user):
        if self.entropy_breach_active and user.id in self.entropy_breach_bonus_users:
            user.rp += 25
            self.entropy_breach_bonus_users.remove(user.id)
            if not self.entropy_breach_bonus_users:
                self.entropy_breach_active = False

    def check_for_population_recovery_triggers(self):
        """Check if we need to trigger recovery mechanisms to bring players back"""
        current_population = len(self.users)

        # Calculate population decline rate
        population_change = 0  # Initialize to avoid UnboundLocalError
        if hasattr(self, "last_population_check"):
            population_change = current_population - self.last_population_check
            decline_rate = population_change / max(
                1, self.tick_count - self.last_population_check_tick
            )
        else:
            decline_rate = 0

        self.last_population_check = current_population
        self.last_population_check_tick = self.tick_count

        # Recovery triggers based on decline patterns
        recovery_triggers = []

        # 1. Major decline trigger (lost 20+ users in 50 ticks)
        if (
            population_change < -20
            and self.tick_count - self.last_population_check_tick < 50
        ):
            recovery_triggers.append("major_decline")

        # 2. Sustained decline trigger (consistently losing users)
        if decline_rate < -0.5 and current_population < 80:
            recovery_triggers.append("sustained_decline")

        # 3. Low population trigger (below 60 users)
        if current_population < 60:
            recovery_triggers.append("low_population")

        # 4. Elite player exodus (fewer than 5 Expert+Master)
        elite_count = len(
            [
                u
                for u in self.users.values()
                if u.user_type in [UserType.EXPERT, UserType.MASTER]
            ]
        )
        if elite_count < 5:
            recovery_triggers.append("elite_exodus")

        # 5. Activity decline (fewer than 5 active users)
        active_users = len(
            [u for u in self.users.values() if u.current_concurrent_activities > 0]
        )
        if active_users < 5:
            recovery_triggers.append("low_activity")

        return recovery_triggers

    def trigger_recovery_event(self, trigger_type: str):
        """Trigger a recovery event to bring players back"""
        recovery_events = {
            "major_decline": {
                "name": "🚀 MAJOR UPDATE - New Content Available!",
                "description": "New hunting zones, modding tools, and economy features!",
                "join_boost": 0.3,  # 30% higher join rate
                "leave_reduction": 0.5,  # 50% lower leave rate
                "duration": 100,  # 100 ticks
                "success_chance": 0.7,  # 70% chance of success
            },
            "sustained_decline": {
                "name": "💎 BONUS WEEKEND - Everything 50% Off!",
                "description": "All activities cost half RP, double rewards!",
                "join_boost": 0.2,
                "leave_reduction": 0.3,
                "duration": 80,
                "success_chance": 0.8,  # 80% chance of success
            },
            "low_population": {
                "name": "🎉 COMEBACK EVENT - Free Rewards!",
                "description": "Returning players get bonus RP and drones!",
                "join_boost": 0.4,
                "leave_reduction": 0.6,
                "duration": 120,
                "success_chance": 0.6,  # 60% chance of success
            },
            "elite_exodus": {
                "name": "🏆 ELITE TOURNAMENT - Special Rewards!",
                "description": "Exclusive content for Expert and Master players!",
                "join_boost": 0.1,
                "leave_reduction": 0.8,
                "duration": 60,
                "success_chance": 0.5,  # 50% chance of success
            },
            "low_activity": {
                "name": "⚡ ACTIVITY SURGE - Bonus RP Everywhere!",
                "description": "All activities give 2x RP rewards!",
                "join_boost": 0.25,
                "leave_reduction": 0.4,
                "duration": 90,
                "success_chance": 0.75,  # 75% chance of success
            },
        }

        if trigger_type in recovery_events:
            event = recovery_events[trigger_type]

            # Determine if the update is successful or backfires
            is_successful = random.random() < event["success_chance"]

            if is_successful:
                # Successful update
                print(f"\n🎮 {event['name']}")
                print(f"📢 {event['description']}")
                print(f"⏰ Duration: {event['duration']} ticks")
                print("✅ Players love the update!")
                print("=" * 80)

                # Apply positive recovery effects
                self.recovery_active = True
                self.recovery_event = event
                self.recovery_end_tick = self.tick_count + event["duration"]
                self.recovery_successful = True

                # Store original rates
                if not hasattr(self, "original_join_rate"):
                    self.original_join_rate = self.user_join_rate
                    self.original_leave_rate = self.user_leave_rate

                # Apply recovery rates
                self.user_join_rate *= 1 + event["join_boost"]
                self.user_leave_rate *= 1 - event["leave_reduction"]

            else:
                # Failed update - backfires!
                failed_events = {
                    "major_decline": {
                        "name": "🚨 MAJOR UPDATE - Pay-to-Win Changes!",
                        "description": "New content requires real money, players outraged!",
                        "join_penalty": 0.5,  # 50% lower join rate
                        "leave_boost": 0.8,  # 80% higher leave rate
                        "duration": 60,
                    },
                    "sustained_decline": {
                        "name": "💸 BONUS WEEKEND - Everything Costs More!",
                        "description": "Prices doubled, rewards halved, players angry!",
                        "join_penalty": 0.3,
                        "leave_boost": 0.6,
                        "duration": 40,
                    },
                    "low_population": {
                        "name": "🎭 COMEBACK EVENT - Buggy Release!",
                        "description": "Game crashes constantly, servers down!",
                        "join_penalty": 0.7,
                        "leave_boost": 0.9,
                        "duration": 80,
                    },
                    "elite_exodus": {
                        "name": "🏆 ELITE TOURNAMENT - Nerf Everything!",
                        "description": "All rewards reduced, elite players furious!",
                        "join_penalty": 0.2,
                        "leave_boost": 0.7,
                        "duration": 50,
                    },
                    "low_activity": {
                        "name": "⚡ ACTIVITY SURGE - Server Issues!",
                        "description": "Lag everywhere, activities broken!",
                        "join_penalty": 0.4,
                        "leave_boost": 0.5,
                        "duration": 70,
                    },
                }

                failed_event = failed_events[trigger_type]
                print(f"\n💥 {failed_event['name']}")
                print(f"📢 {failed_event['description']}")
                print(f"⏰ Duration: {failed_event['duration']} ticks")
                print("❌ Players hate the update!")
                print("=" * 80)

                # Apply negative effects
                self.recovery_active = True
                self.recovery_event = failed_event
                self.recovery_end_tick = self.tick_count + failed_event["duration"]
                self.recovery_successful = False

                # Store original rates
                if not hasattr(self, "original_join_rate"):
                    self.original_join_rate = self.user_join_rate
                    self.original_leave_rate = self.user_leave_rate

                # Apply penalty rates
                self.user_join_rate *= 1 - failed_event["join_penalty"]
                self.user_leave_rate *= 1 + failed_event["leave_boost"]

            return True
        return False

    def check_recovery_expiration(self):
        """Check if recovery event has expired and restore normal rates"""
        if hasattr(self, "recovery_active") and self.recovery_active:
            if self.tick_count >= self.recovery_end_tick:
                if hasattr(self, "recovery_successful") and self.recovery_successful:
                    print(
                        f"\n⏰ Recovery event '{self.recovery_event['name']}' has expired!"
                    )
                    print("🔄 Returning to normal population rates...")
                else:
                    print(
                        f"\n⏰ Failed update '{self.recovery_event['name']}' has expired!"
                    )
                    print("🔄 Returning to normal population rates...")
                print("=" * 80)

                # Restore original rates
                self.user_join_rate = self.original_join_rate
                self.user_leave_rate = self.original_leave_rate

                # Clear recovery state
                self.recovery_active = False
                self.recovery_event = None
                self.recovery_end_tick = None
                self.recovery_successful = None

    def process_tick(self):
        """Process one tick of the simulation"""
        self.tick_count += 1

        # Check for recovery triggers
        if self.tick_count % 10 == 0:  # Check every 10 ticks
            self.check_for_population_recovery_triggers()

        # Check for recovery expiration
        self.check_recovery_expiration()

        # Process active activities
        completed_activities = []
        activity_summary = {
            "hunt_success": 0,
            "hunt_fail": 0,
            "economy_success": 0,
            "economy_fail": 0,
            "mod_success": 0,
            "mod_fail": 0,
            "fight_success": 0,
            "fight_fail": 0,
            "users_joined": 0,
            "users_left": 0,
        }

        # Manage user population
        if random.random() < 0.8:  # 80% chance every tick
            dice_roll = random.randint(0, 6)
            if dice_roll > 0:
                self.manage_user_population(dice_roll, activity_summary)

        for activity_id, activity in self.active_activities.items():
            # Safety check: make sure user still exists
            if activity.user_id not in self.users:
                completed_activities.append(activity_id)
                continue
            user = self.users[activity.user_id]

            # Update activity progress
            activity.ticks_remaining -= 1

            if activity.ticks_remaining <= 0:
                # Activity completed
                completed_activities.append(activity_id)

                # Calculate success based on user type and activity
                success_chance = self.get_activity_success_chance(
                    user, activity.activity_type
                )
                is_successful = random.random() < success_chance

                if is_successful:
                    # Successful activity
                    reward = self.calculate_activity_reward(
                        user, activity.activity_type
                    )
                    user.rp += reward

                    # Track drone gains/losses for hunting
                    if activity.activity_type == "hunt":
                        if random.random() < 0.3:  # 30% chance to gain drone
                            user.drone_count += 1
                            self.stats["total_drones_gained"] += 1

                    # Track activity success
                    if activity.activity_type == "hunt":
                        activity_summary["hunt_success"] += 1
                    elif activity.activity_type == "economy":
                        activity_summary["economy_success"] += 1
                    elif activity.activity_type == "mod":
                        activity_summary["mod_success"] += 1
                    elif activity.activity_type == "fight":
                        activity_summary["fight_success"] += 1

                else:
                    # Failed activity
                    if activity.activity_type == "hunt":
                        activity_summary["hunt_fail"] += 1
                    elif activity.activity_type == "economy":
                        activity_summary["economy_fail"] += 1
                    elif activity.activity_type == "mod":
                        activity_summary["mod_fail"] += 1
                    elif activity.activity_type == "fight":
                        activity_summary["fight_fail"] += 1

        # Remove completed activities
        for activity_id in completed_activities:
            del self.active_activities[activity_id]

        # Start new activities for users
        for user_id, user in list(self.users.items()):
            if (
                len(
                    [a for a in self.active_activities.values() if a.user_id == user_id]
                )
                < user.max_concurrent_activities
            ):
                if random.random() < 0.3:  # 30% chance to start new activity
                    self.start_user_activity(user)

        # Update global multiplier
        self.update_global_multiplier()

        # Generate world events (reduced frequency)
        if random.random() < 0.01:  # 1% chance per tick (much less frequent)
            self.generate_world_event()

        # Update statistics
        self.stats["total_activities"] += len(completed_activities)
        self.stats["total_rp_earned"] += sum(user.rp for user in self.users.values())

        # Only show activity summary if there were significant activities
        total_activities = sum(activity_summary.values())
        if total_activities > 0:
            summary_parts = []
            if activity_summary["hunt_success"] > 0:
                summary_parts.append(f"🎯 {activity_summary['hunt_success']} hunts")
            if activity_summary["economy_success"] > 0:
                summary_parts.append(
                    f"💰 {activity_summary['economy_success']} economy"
                )
            if activity_summary["mod_success"] > 0:
                summary_parts.append(f"🔧 {activity_summary['mod_success']} mods")
            if activity_summary["fight_success"] > 0:
                summary_parts.append(f"⚔️ {activity_summary['fight_success']} fights")
            if activity_summary["users_joined"] > 0:
                summary_parts.append(f"➕ {activity_summary['users_joined']} joined")
            if activity_summary["users_left"] > 0:
                summary_parts.append(f"➖ {activity_summary['users_left']} left")

            if summary_parts:
                print(f"📊 Tick {self.tick_count}: {' | '.join(summary_parts)}")

        # Check for stillness and inject entropy if needed
        self.check_for_stillness()

    def update_global_multiplier(self):
        """Update global multiplier based on real simulation drone data"""
        active_users = len(
            [u for u in self.users.values() if u.current_activity != "idle"]
        )
        total_users = len(self.users)

        # Calculate real drone data from simulation
        total_drones_alive = sum(user.drone_count for user in self.users.values())
        total_drones_ever_died = self.stats["total_simulacra_deaths"]

        # Ensure we don't divide by zero
        if total_drones_ever_died == 0:
            total_drones_ever_died = 1

        self.global_multiplier.update_multiplier(
            drones_alive=total_drones_alive,
            active_players=active_users,
            drones_ever_died=total_drones_ever_died,
        )

        # Record economy cycle with real data
        self.economy_cycles.append(
            {
                "tick": self.tick_count,
                "day": self.current_day,
                "multiplier": self.global_multiplier.get_current_multiplier(),
                "active_users": active_users,
                "drones_alive": total_drones_alive,
                "drones_ever_died": total_drones_ever_died,
            }
        )
        self.stats["economy_cycles"] += 1

    def generate_world_event(self):
        """Generate random world events with reduced frequency"""
        events = [
            ("🌪️ Economic Collapse - Compression costs reduced!", "economy", False),
            ("📈 Market Boom - Higher rewards for all activities!", "economy", True),
            ("⚡ Energy Surge - Mod activities more efficient!", "mod", True),
            ("🌿 Resource Abundance - Hunt activities more profitable!", "hunt", True),
            ("🔧 System Update - All activities temporarily boosted!", "general", True),
            ("🌍 Global Harmony - Balanced economy state!", "general", True),
            ("⚔️ Arena Expansion - Fighting rewards increased!", "fight", True),
            ("💀 Death Wave - Increased simulacra mortality!", "general", False),
        ]

        # Reduced frequency: 2% chance per tick (was 10%)
        if random.random() < 0.02:
            event, event_type, is_positive = random.choice(events)

            # Make users react to the event (flocking behavior)
            for user in self.users.values():
                user.react_to_event(event_type, is_positive)
                user.total_events_participated += 1

            self.world_events.append(
                {
                    "tick": self.tick_count,
                    "day": self.current_day,
                    "event": event,
                    "type": event_type,
                    "is_positive": is_positive,
                }
            )
            self.stats["world_events"] += 1
            return event
        return None

    def display_simulation_status(self):
        """Display comprehensive simulation status"""
        self.clear_screen()

        day_progress = self.calculate_day_progress()

        print("🌍 INFINITE SIMULATION ENGINE - RUNNING INDEFINITELY")
        print("=" * 80)
        print(
            f"📅 Day: {self.current_day} | Progress: {day_progress:.1f}% | Tick: {self.tick_count}"
        )
        print(f"⏰ Rate: {self.tick_rate:.1f} ticks/sec | Users: {len(self.users)}")
        print(
            f"🌍 Global Multiplier: {self.global_multiplier.get_current_multiplier():.2f}x | Active: {len(self.active_activities)}"
        )
        print("=" * 80)

        # Show user base statistics
        online_users = len([u for u in self.users.values() if u.is_online])
        offline_users = len(self.users) - online_users

        print(f"\n👥 USER BASE STATISTICS:")
        print("-" * 60)
        print(f"  📊 Current Sub Count: {len(self.users)}")
        print(f"  🟢 Active/Online: {online_users}")
        print(f"  🔴 Offline: {offline_users}")
        print(f"  📈 Peak Users: {self.stats['peak_users']}")
        print(f"  ➕ Total Joined: {self.stats['total_users_joined']}")
        print(f"  ➖ Total Left: {self.stats['total_users_left']}")
        print(f"  📅 Today: +{self.users_joined_today} / -{self.users_left_today}")
        if self.stats["days_completed"] > 0:
            avg_growth = (
                self.stats["total_users_joined"] - self.stats["total_users_left"]
            ) / self.stats["days_completed"]
            print(f"  📊 Avg Daily Growth: {avg_growth:+.1f} users/day")

        # Calculate growth rate
        if self.stats["days_completed"] > 0:
            daily_growth = (
                self.stats["total_users_joined"] - self.stats["total_users_left"]
            ) / self.stats["days_completed"]
            print(f"  📊 Avg Daily Growth: {daily_growth:+.1f} users/day")

        # Show active activities (limit to 20 for readability)
        active_activities_list = list(self.active_activities.items())[:20]
        if active_activities_list:
            print("🎯 ACTIVE ACTIVITIES:")
            print("-" * 60)
            for activity_id, activity in active_activities_list:
                user = self.users.get(activity.user_id)
                if user:
                    # Calculate progress percentage
                    total_ticks = activity.ticks_requested
                    completed_ticks = total_ticks - activity.ticks_remaining
                    progress_percentage = (
                        (completed_ticks / total_ticks) * 100 if total_ticks > 0 else 0
                    )

                    # Create progress bar
                    bar_width = 30
                    filled_width = int((progress_percentage / 100) * bar_width)
                    bar = "█" * filled_width + "░" * (bar_width - filled_width)

                    print(
                        f"  {user.name:<12} {activity.activity_type.upper()}: [{bar}] {progress_percentage:5.1f}% ({completed_ticks}/{total_ticks})"
                    )

            if len(self.active_activities) > 20:
                remaining = len(self.active_activities) - 20
                print(f"  ... and {remaining} more activities")
        else:
            print("\n💤 No active activities")

        # Show user summary
        print("\n👥 USER SUMMARY:")
        print("-" * 60)

        user_types = {}
        total_drones = 0
        total_drones_gained = 0
        total_drones_lost = 0

        for user in self.users.values():
            if user.user_type not in user_types:
                user_types[user.user_type] = {
                    "count": 0,
                    "total_rp": 0,
                    "active": 0,
                    "online": 0,
                    "total_drones": 0,
                    "avg_concurrent": 0,
                }
            user_types[user.user_type]["count"] += 1
            user_types[user.user_type]["total_rp"] += user.rp
            user_types[user.user_type]["total_drones"] += user.drone_count
            user_types[user.user_type][
                "avg_concurrent"
            ] += user.current_concurrent_activities

            if user.current_concurrent_activities > 0:
                user_types[user.user_type]["active"] += 1
            if user.is_online:
                user_types[user.user_type]["online"] += 1

            total_drones += user.drone_count
            total_drones_gained += user.total_drones_gained
            total_drones_lost += user.total_drones_lost

        for user_type, stats in user_types.items():
            avg_rp = stats["total_rp"] // stats["count"] if stats["count"] > 0 else 0
            avg_drones = (
                stats["total_drones"] // stats["count"] if stats["count"] > 0 else 0
            )
            avg_concurrent = (
                stats["avg_concurrent"] / stats["count"] if stats["count"] > 0 else 0
            )
            print(
                f"  {user_type.value.title():<10}: {stats['count']:2d} users, {stats['online']:2d} online, {stats['active']:2d} active, avg {avg_rp:4d} RP, {avg_drones:2d} drones, {avg_concurrent:.1f} concurrent"
            )

        # Show statistics
        print("\n📊 SIMULATION STATISTICS:")
        print("-" * 60)
        print(f"  Total Ticks: {self.stats['total_ticks']}")
        print(f"  Days Completed: {self.stats['days_completed']}")
        print(f"  Total Activities: {self.stats['total_activities']}")
        print(f"  Activities Completed: {self.stats['activities_completed']}")
        print(f"  Total RP Earned: {self.stats['total_rp_earned']}")
        print(f"  Total RP Spent: {self.stats['total_rp_spent']}")
        print(f"  Economy Cycles: {self.stats['economy_cycles']}")
        print(f"  World Events: {self.stats['world_events']}")

        # Drone statistics
        print(f"\n🤖 DRONE STATISTICS:")
        print("-" * 60)
        print(f"  Total Drones: {total_drones}")
        print(f"  Total Gained: {total_drones_gained}")
        print(f"  Total Lost: {total_drones_lost}")
        print(f"  Net Change: {total_drones_gained - total_drones_lost:+d}")

        # Calculate average drones per user
        if len(self.users) > 0:
            avg_drones_per_user = total_drones / len(self.users)
            print(f"  Avg Drones/User: {avg_drones_per_user:.1f}")

        # Show recent world events
        if self.world_events:
            print("🌍 Recent World Events:")
            print("-" * 60)
            for event in self.world_events[-3:]:  # Show last 3 events
                event_emoji = "✅" if event.get("is_positive", True) else "❌"
                if "day" in event and "tick" in event:
                    print(
                        f"  {event_emoji} Day {event['day']}, Tick {event['tick']}: {event['event']}"
                    )
                else:
                    print(f"  {event_emoji} {event.get('event', 'Unknown event')}")

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

        # Show day progress bar
        day_bar = self.create_progress_bar(day_progress, 50, "cyan")
        print(f"\n📅 Day Progress: {day_bar}")

        print("\n" + "=" * 80)
        print("🌍 Infinite Simulation - Press Ctrl+C to stop")
        print("=" * 80)

    def simulation_loop(self):
        """Main simulation loop - runs indefinitely"""
        while self.is_running:
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

            # Display status based on display interval
            if self.tick_count % self.display_interval == 0:
                self.display_simulation_status()

            # Wait for next tick
            elapsed = time.time() - start_time
            sleep_time = max(0, (1.0 / self.tick_rate) - elapsed)
            time.sleep(sleep_time)

    def start_simulation(self):
        """Start the infinite simulation"""
        print("🚀 Starting Infinite Simulation Engine...")
        print("🌍 Runs indefinitely with day tracking")
        print(f"⏰ {self.ticks_per_day} ticks = 1 simulated day")
        print(f"⏱️ 1 real second = 1 tick")
        print(f"📺 Display every {self.display_interval} ticks")
        print(
            f"👥 {self.initial_user_count} users with different personalities and preferences"
        )
        print("📈 Dynamic user base with realistic growth/decline")
        print("🌍 Dynamic economy cycles and world events")
        print("=" * 80)

        self.create_simulation_users()

        # Start some initial activities
        for i in range(10):  # Start more activities with more users
            user_id = f"sim_user_{i+1}"
            if user_id in self.users:
                self.start_user_activity(self.users[user_id])

        self.is_running = True
        self.thread = threading.Thread(target=self.simulation_loop)
        self.thread.daemon = True
        self.thread.start()

        # Wait for simulation to complete (or be interrupted)
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

        print("\n🎉 Infinite Simulation Complete!")
        print("=" * 80)
        self.save_results()

    def save_results(self):
        """Save comprehensive simulation results"""
        results_file = "infinite_simulation_results.json"

        with open(results_file, "w") as f:
            json.dump(
                {
                    "simulation_timestamp": datetime.now().isoformat(),
                    "final_tick_count": self.tick_count,
                    "final_day": self.current_day,
                    "days_completed": self.stats["days_completed"],
                    "ticks_per_day": self.ticks_per_day,
                    "stats": self.stats,
                    "economy_cycles": self.economy_cycles,
                    "world_events": self.world_events,
                    "daily_stats": self.daily_stats,
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
                            "fight_ticks": user.fight_ticks,
                            "fight_successes": user.fight_successes,
                            "drone_count": user.drone_count,
                            "total_drones_gained": user.total_drones_gained,
                            "total_drones_lost": user.total_drones_lost,
                            "total_activities_completed": user.total_activities_completed,
                            "total_events_participated": user.total_events_participated,
                            "total_channel_moves": user.total_channel_moves,
                            "total_simulacra_deaths": user.total_simulacra_deaths,
                            "current_concurrent_activities": user.current_concurrent_activities,
                            "max_concurrent_activities": user.max_concurrent_activities,
                            "event_preferences": user.event_preferences,
                            "last_event_reaction": user.last_event_reaction,
                        }
                        for user_id, user in self.users.items()
                    },
                    "final_global_multiplier": self.global_multiplier.get_current_multiplier(),
                },
                f,
                indent=2,
            )

        print(f"📊 Results saved to: {results_file}")

        # Print summary
        print("\n📋 Simulation Summary:")
        print("-" * 50)
        print(f"👥 Users: {len(self.users)}")
        print(f"⏰ Duration: {self.tick_count} ticks ({self.tick_count} seconds)")
        print(
            f"📅 Days: {self.current_day} (completed: {self.stats['days_completed']})"
        )
        print(
            f"🎯 Activities: {self.stats['total_activities']} started, {self.stats['activities_completed']} completed"
        )
        print(
            f"💰 RP Economy: {self.stats['total_rp_earned']} earned, {self.stats['total_rp_spent']} spent"
        )
        print(f"🌍 Economy Cycles: {self.stats['economy_cycles']}")
        print(f"🎉 World Events: {self.stats['world_events']}")
        print(
            f"🌍 Final Multiplier: {self.global_multiplier.get_current_multiplier():.2f}x"
        )
        print(f"⏰ Tick-to-Day Ratio: {self.ticks_per_day} ticks = 1 day")


def main():
    """Main function"""
    import sys

    # Check for command line arguments
    mode = "real_time"  # default

    if len(sys.argv) > 1 and sys.argv[1] == "--mode" and len(sys.argv) > 2:
        mode = sys.argv[2]
        print(f"🚀 Starting Infinite Simulation Engine with {mode.upper()} mode")
        print("=" * 60)
    else:
        print("🚀 Starting Infinite Simulation Engine")
        print("=" * 60)

        print("Select simulation time scale:")
        print("1. Real Time (86400 ticks = 1 day)")
        print("2. Fast (8640 ticks = 1 day)")
        print("3. Daily (86400 ticks = 1 day)")
        print("4. Weekly (604800 ticks = 1 week)")
        print("5. Monthly (2592000 ticks = 1 month)")
        choice = input("Enter 1-5: ").strip()

        if choice == "2":
            mode = "fast"
        elif choice == "3":
            mode = "daily"
        elif choice == "4":
            mode = "weekly"
        elif choice == "5":
            mode = "monthly"
        else:
            mode = "real_time"

    engine = InfiniteSimulationEngine(mode=mode)
    engine.start_simulation()


if __name__ == "__main__":
    main()
