import time
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class SurvivalState(Enum):
    """Survival states for DigiDrones"""

    BREATHING = "breathing"
    COLLAPSING = "collapsing"
    DEAD = "dead"
    MUTATING = "mutating"


@dataclass
class SurvivalStats:
    """Core survival statistics"""

    hp: float = 100.0
    resistance: float = 10.0  # Percentage
    mutation_rate: float = 10.0  # Percentage
    entropy_drain: float = 5.0  # HP per second
    survival_time: float = 0.0  # Seconds
    last_breath: datetime = None

    def __post_init__(self):
        if self.last_breath is None:
            self.last_breath = datetime.now()


class EntropyEngine:
    """Advanced entropy drain system from original Simulacra"""

    def __init__(self):
        self.base_drain_rate = 5.0  # HP per second
        self.acceleration_rate = 0.01  # +1% per minute
        self.max_drain_rate = 50.0  # Maximum HP per second

    def calculate_drain(self, survival_time: float, resistance: float) -> float:
        """Calculate current entropy drain based on survival time and resistance"""
        # Base drain increases over time
        time_acceleration = survival_time / 60.0  # Minutes
        current_drain = self.base_drain_rate * (
            1 + (time_acceleration * self.acceleration_rate)
        )

        # Cap at maximum drain rate
        current_drain = min(current_drain, self.max_drain_rate)

        # Resistance reduces drain
        resistance_factor = max(0.1, 1.0 - (resistance / 100.0))
        final_drain = current_drain * resistance_factor

        return final_drain


class MutationEngine:
    """Advanced mutation system with time-based chance calculation"""

    def __init__(self):
        self.base_mutation_chance = 40.0  # Base 40% chance
        self.max_mutation_chance = 95.0  # Never reach 100%

    def calculate_mutation_chance(
        self, survival_time: float, mutation_rate: float
    ) -> float:
        """Calculate mutation chance using original Simulacra formula"""
        # Get two random rolls
        roll1 = random.uniform(0, 100)
        roll2 = random.uniform(0, 100)

        # Time factor (seconds)
        time_factor = survival_time

        # Calculate average with time smoothing
        average = (roll1 + roll2 + time_factor) / 3.0

        # Base chance with mutation rate modifier
        base_chance = self.base_mutation_chance + (mutation_rate * 0.5)

        # Final chance (never reaches 100%)
        final_chance = min(self.max_mutation_chance, base_chance)

        return final_chance, average

    def should_mutate(
        self, survival_time: float, mutation_rate: float
    ) -> Tuple[bool, float]:
        """Check if mutation should trigger"""
        chance, average = self.calculate_mutation_chance(survival_time, mutation_rate)

        # Mutation triggers if average is less than or equal to chance
        should_mutate = average <= chance

        return should_mutate, chance


class DisasterEngine:
    """Advanced disaster system with scaling damage"""

    def __init__(self):
        self.disaster_types = {
            "fire": {"base_damage": 7, "scaling": 7, "interval": 300},  # Every 5 min
            "flood": {"base_damage": 5, "scaling": 5, "interval": 240},  # Every 4 min
            "wind": {"base_damage": 3, "scaling": 3, "interval": 180},  # Every 3 min
            "lightning": {
                "base_damage": 10,
                "scaling": 10,
                "interval": 600,
            },  # Every 10 min
            "earthquake": {
                "base_damage": 8,
                "scaling": 8,
                "interval": 480,
            },  # Every 8 min
        }
        self.last_disasters = {}

    def should_trigger_disaster(self, disaster_type: str, survival_time: float) -> bool:
        """Check if disaster should trigger based on time intervals"""
        if disaster_type not in self.disaster_types:
            return False

        interval = self.disaster_types[disaster_type]["interval"]
        last_time = self.last_disasters.get(disaster_type, 0)

        return survival_time >= last_time + interval

    def calculate_disaster_damage(
        self, disaster_type: str, survival_time: float, resistance: float
    ) -> float:
        """Calculate disaster damage with scaling"""
        if disaster_type not in self.disaster_types:
            return 0.0

        disaster_data = self.disaster_types[disaster_type]
        base_damage = disaster_data["base_damage"]
        scaling = disaster_data["scaling"]

        # Damage scales with survival time (every 5 minutes)
        time_scaling = math.floor(survival_time / 300)  # 5 minutes
        scaled_damage = base_damage + (scaling * time_scaling)

        # Resistance reduces damage
        resistance_factor = max(0.1, 1.0 - (resistance / 100.0))
        final_damage = scaled_damage * resistance_factor

        return final_damage

    def trigger_disaster(self, disaster_type: str, survival_time: float) -> Dict:
        """Trigger a disaster and return damage info"""
        damage = self.calculate_disaster_damage(
            disaster_type, survival_time, 10.0
        )  # Default resistance
        self.last_disasters[disaster_type] = survival_time

        return {
            "type": disaster_type,
            "damage": damage,
            "message": f"🌪️ {disaster_type.title()} disaster strikes! Dealt {damage:.1f} damage!",
        }


class BreathingEngine:
    """Breathing rhythm system for visual feedback"""

    def __init__(self):
        self.breathing_cycle = 0
        self.breathing_messages = [
            "💨 You feel the winds scrape your skin",
            "🌬️ A gentle breeze whispers through",
            "💨 Your core pulses with life",
            "🌬️ The air crackles with energy",
            "💨 You sense the rhythm of existence",
            "🌬️ Time flows like breath",
            "💨 Your consciousness expands",
            "🌬️ Reality bends and flows",
        ]

    def get_breathing_message(self, survival_time: float) -> str:
        """Get breathing message based on survival time"""
        cycle = int(survival_time / 10) % len(self.breathing_messages)
        return self.breathing_messages[cycle]

    def get_breathing_emoji(self, survival_time: float) -> str:
        """Get breathing emoji animation"""
        cycle = int(survival_time / 2) % 4
        if cycle == 0:
            return "💨"  # Inhale
        elif cycle == 1:
            return "🌬️"  # Hold
        elif cycle == 2:
            return "💨"  # Exhale
        else:
            return "🌬️"  # Rest


class SurvivalEngine:
    """Main survival engine combining all systems"""

    def __init__(self):
        self.entropy_engine = EntropyEngine()
        self.mutation_engine = MutationEngine()
        self.disaster_engine = DisasterEngine()
        self.breathing_engine = BreathingEngine()

    def update_survival(self, stats: SurvivalStats, time_delta: float = 1.0) -> Dict:
        """Update survival state and return events"""
        events = []

        # Update survival time
        stats.survival_time += time_delta

        # Calculate entropy drain
        drain_rate = self.entropy_engine.calculate_drain(
            stats.survival_time, stats.resistance
        )
        stats.hp -= drain_rate * time_delta

        # Check for mutation
        should_mutate, mutation_chance = self.mutation_engine.should_mutate(
            stats.survival_time, stats.mutation_rate
        )

        if should_mutate:
            mutation_event = self._generate_mutation(stats)
            events.append(mutation_event)

        # Check for disasters
        for disaster_type in self.disaster_engine.disaster_types:
            if self.disaster_engine.should_trigger_disaster(
                disaster_type, stats.survival_time
            ):
                disaster_event = self.disaster_engine.trigger_disaster(
                    disaster_type, stats.survival_time
                )
                stats.hp -= disaster_event["damage"]
                events.append(disaster_event)

        # Check for death
        if stats.hp <= 0:
            stats.hp = 0
            events.append(
                {
                    "type": "death",
                    "message": "💀 Your DigiDrone has collapsed...",
                    "survival_time": stats.survival_time,
                }
            )

        # Add breathing message
        breathing_msg = self.breathing_engine.get_breathing_message(stats.survival_time)
        breathing_emoji = self.breathing_engine.get_breathing_emoji(stats.survival_time)

        events.append(
            {
                "type": "breathing",
                "message": f"{breathing_emoji} {breathing_msg}",
                "emoji": breathing_emoji,
            }
        )

        return {
            "events": events,
            "stats": stats,
            "drain_rate": drain_rate,
            "mutation_chance": mutation_chance,
        }

    def _generate_mutation(self, stats: SurvivalStats) -> Dict:
        """Generate a mutation event"""
        mutation_types = [
            {
                "name": "Solar Pulse",
                "hp_boost": 5,
                "mutation_boost": 0,
                "resistance_change": 0,
            },
            {
                "name": "Ironroot Core",
                "hp_boost": 0,
                "mutation_boost": 0,
                "resistance_change": 5,
            },
            {
                "name": "Quantum Root",
                "hp_boost": -5,
                "mutation_boost": 8,
                "resistance_change": -3,
            },
            {
                "name": "Crystalline Core",
                "hp_boost": 3,
                "mutation_boost": 0,
                "resistance_change": 7,
            },
            {
                "name": "Phantom Vine",
                "hp_boost": 0,
                "mutation_boost": 6,
                "resistance_change": -3,
            },
            {
                "name": "Void Essence",
                "hp_boost": -3,
                "mutation_boost": 10,
                "resistance_change": -5,
            },
            {
                "name": "Stellar Core",
                "hp_boost": 10,
                "mutation_boost": -2,
                "resistance_change": 0,
            },
            {
                "name": "Chaos Bloom",
                "hp_boost": -2,
                "mutation_boost": 12,
                "resistance_change": -2,
            },
        ]

        mutation = random.choice(mutation_types)

        # Apply mutation effects
        stats.hp = max(1, stats.hp + mutation["hp_boost"])
        stats.mutation_rate = max(
            1, min(50, stats.mutation_rate + mutation["mutation_boost"])
        )
        stats.resistance = max(
            0, min(90, stats.resistance + mutation["resistance_change"])
        )

        return {
            "type": "mutation",
            "name": mutation["name"],
            "message": f"🌱 {mutation['name']} mutation! HP: {mutation['hp_boost']:+d}, Mutation: {mutation['mutation_boost']:+d}, Resistance: {mutation['resistance_change']:+d}",
            "effects": mutation,
        }

    def get_survival_status(self, stats: SurvivalStats) -> str:
        """Get formatted survival status"""
        breathing_emoji = self.breathing_engine.get_breathing_emoji(stats.survival_time)

        # Format time
        hours = int(stats.survival_time // 3600)
        minutes = int((stats.survival_time % 3600) // 60)
        seconds = int(stats.survival_time % 60)

        if hours > 0:
            time_str = f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = f"{seconds}s"

        return f"{breathing_emoji} **Survival Time:** {time_str} | **HP:** {stats.hp:.1f} | **Resistance:** {stats.resistance:.1f}% | **Mutation Rate:** {stats.mutation_rate:.1f}%"
