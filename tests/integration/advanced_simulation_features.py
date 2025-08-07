#!/usr/bin/env python3
"""
Advanced Simulation Features for Simulacra Rancher
Enhances the main simulation with advanced behaviors and analytics
"""

import random
import time
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class UserBehaviorProfile:
    """Advanced user behavior profiling"""

    user_id: str
    username: str
    activity_pattern: str  # "morning", "afternoon", "evening", "night", "random"
    social_level: int  # 1-10
    risk_tolerance: int  # 1-10
    specialization: (
        str  # "hunter", "gatherer", "trader", "crafter", "social", "balanced"
    )
    personality_traits: List[str]
    preferred_channels: List[str]
    command_frequency: Dict[str, float]
    chat_style: str  # "formal", "casual", "emoji_heavy", "technical"
    timezone_offset: int  # Hours from UTC


class AdvancedUserSimulator:
    """Advanced user behavior simulation with realistic patterns"""

    def __init__(self):
        self.behavior_profiles = {}
        self.activity_history = {}
        self.social_networks = {}
        self.economic_behavior = {}

    def create_behavior_profile(
        self, user_id: str, username: str
    ) -> UserBehaviorProfile:
        """Create a realistic user behavior profile"""

        # Activity patterns based on real user behavior
        activity_patterns = ["morning", "afternoon", "evening", "night", "random"]
        weights = [0.15, 0.25, 0.30, 0.20, 0.10]  # Evening is most common

        # Specializations with realistic distribution
        specializations = [
            "hunter",
            "gatherer",
            "trader",
            "crafter",
            "social",
            "balanced",
        ]
        spec_weights = [0.20, 0.25, 0.15, 0.10, 0.15, 0.15]

        # Personality traits
        all_traits = [
            "competitive",
            "cooperative",
            "curious",
            "cautious",
            "impulsive",
            "strategic",
            "social",
            "independent",
            "creative",
            "analytical",
        ]

        profile = UserBehaviorProfile(
            user_id=user_id,
            username=username,
            activity_pattern=random.choices(activity_patterns, weights=weights)[0],
            social_level=random.randint(3, 10),
            risk_tolerance=random.randint(1, 10),
            specialization=random.choices(specializations, weights=spec_weights)[0],
            personality_traits=random.sample(all_traits, random.randint(2, 4)),
            preferred_channels=self._generate_preferred_channels(),
            command_frequency=self._generate_command_frequency(),
            chat_style=random.choice(["formal", "casual", "emoji_heavy", "technical"]),
            timezone_offset=random.randint(-12, 12),
        )

        self.behavior_profiles[user_id] = profile
        return profile

    def _generate_preferred_channels(self) -> List[str]:
        """Generate realistic channel preferences"""
        channels = ["general", "commands", "trading", "hunting", "crafting", "chat"]
        num_channels = random.randint(2, 4)
        return random.sample(channels, num_channels)

    def _generate_command_frequency(self) -> Dict[str, float]:
        """Generate realistic command usage patterns"""
        commands = {
            "!daily": random.uniform(0.8, 1.0),  # High frequency
            "!gather": random.uniform(0.6, 0.9),  # High frequency
            "!hunt": random.uniform(0.4, 0.8),  # Medium-high
            "!trade": random.uniform(0.3, 0.7),  # Medium
            "!craft": random.uniform(0.2, 0.6),  # Medium
            "!chat": random.uniform(0.1, 0.5),  # Low-medium
            "!profile": random.uniform(0.1, 0.3),  # Low
            "!personality": random.uniform(0.05, 0.2),  # Very low
            "!leaderboard": random.uniform(0.1, 0.4),  # Low-medium
            "!kingdom": random.uniform(0.05, 0.3),  # Low
        }
        return commands

    def should_user_act(self, user_id: str, current_time: datetime) -> bool:
        """Determine if user should act based on their behavior profile"""
        if user_id not in self.behavior_profiles:
            return random.random() < 0.7  # Default 70% chance

        profile = self.behavior_profiles[user_id]
        hour = current_time.hour

        # Activity patterns based on time of day
        if profile.activity_pattern == "morning":
            return 6 <= hour <= 12 and random.random() < 0.8
        elif profile.activity_pattern == "afternoon":
            return 12 <= hour <= 18 and random.random() < 0.8
        elif profile.activity_pattern == "evening":
            return 18 <= hour <= 24 and random.random() < 0.8
        elif profile.activity_pattern == "night":
            return (0 <= hour <= 6 or 22 <= hour <= 24) and random.random() < 0.6
        else:  # random
            return random.random() < 0.7

    def generate_user_command(self, user_id: str) -> Tuple[str, List[str]]:
        """Generate realistic command based on user profile"""
        if user_id not in self.behavior_profiles:
            return self._generate_random_command()

        profile = self.behavior_profiles[user_id]

        # Weight commands based on user's frequency preferences
        commands = list(profile.command_frequency.keys())
        weights = list(profile.command_frequency.values())

        # Boost commands based on specialization
        if profile.specialization == "hunter":
            weights[commands.index("!hunt")] *= 1.5
        elif profile.specialization == "gatherer":
            weights[commands.index("!gather")] *= 1.5
        elif profile.specialization == "trader":
            weights[commands.index("!trade")] *= 1.5
        elif profile.specialization == "crafter":
            weights[commands.index("!craft")] *= 1.5
        elif profile.specialization == "social":
            weights[commands.index("!chat")] *= 1.5

        # Normalize weights
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]

        command = random.choices(commands, weights=weights)[0]
        args = self._generate_command_args(command, profile)

        return command, args

    def _generate_random_command(self) -> Tuple[str, List[str]]:
        """Generate a random command for users without profiles"""
        commands = [
            ("!daily", []),
            ("!gather", []),
            ("!hunt", []),
            ("!trade", ["stone", "5", "10"]),
            ("!craft", ["stone_pickaxe"]),
            ("!chat", ["Hello there!"]),
            ("!profile", []),
            ("!personality", []),
            ("!leaderboard", []),
            ("!kingdom", []),
        ]
        return random.choice(commands)

    def _generate_command_args(
        self, command: str, profile: UserBehaviorProfile
    ) -> List[str]:
        """Generate realistic command arguments based on user profile"""
        if command == "!trade":
            items = ["stone", "wood", "iron", "gold", "crystal"]
            item = random.choice(items)
            amount = random.randint(1, 20)
            price = random.randint(5, 50)
            return [item, str(amount), str(price)]
        elif command == "!craft":
            recipes = ["stone_pickaxe", "wood_sword", "iron_armor", "gold_ring"]
            return [random.choice(recipes)]
        elif command == "!chat":
            messages = self._generate_chat_message(profile)
            return [messages]
        else:
            return []

    def _generate_chat_message(self, profile: UserBehaviorProfile) -> str:
        """Generate realistic chat messages based on user's chat style"""
        base_messages = [
            "How's everyone doing?",
            "Anyone want to trade?",
            "Great hunt today!",
            "The AI is getting smarter...",
            "Anyone else notice the patterns?",
            "This game is addictive!",
            "What's your favorite activity?",
            "The kingdom system is interesting",
            "Anyone else having fun?",
            "The memories are fascinating",
        ]

        message = random.choice(base_messages)

        # Apply chat style modifications
        if profile.chat_style == "emoji_heavy":
            emojis = ["😊", "🎮", "⚡", "🔥", "💎", "🏆", "🎯", "🚀", "💪", "🌟"]
            message += " " + random.choice(emojis) * random.randint(1, 3)
        elif profile.chat_style == "technical":
            technical_terms = [
                "algorithm",
                "optimization",
                "efficiency",
                "protocol",
                "system",
            ]
            message += f" The {random.choice(technical_terms)} is quite impressive."
        elif profile.chat_style == "formal":
            message = message.replace("!", ".").replace("?", "?")
            message += " I find this quite engaging."

        return message


class SimulationAnalytics:
    """Advanced analytics for simulation results"""

    def __init__(self):
        self.metrics = {
            "user_activity": {},
            "command_usage": {},
            "channel_activity": {},
            "economic_flow": {},
            "social_interactions": {},
            "performance_metrics": {},
        }

    def analyze_simulation_results(self, results_file: str) -> Dict[str, Any]:
        """Analyze simulation results and generate insights"""
        try:
            with open(results_file, "r") as f:
                data = json.load(f)

            analysis = {
                "summary": self._generate_summary(data),
                "user_insights": self._analyze_user_behavior(data),
                "economic_analysis": self._analyze_economy(data),
                "performance_metrics": self._analyze_performance(data),
                "recommendations": self._generate_recommendations(data),
            }

            return analysis
        except Exception as e:
            return {"error": f"Failed to analyze results: {str(e)}"}

    def _generate_summary(self, data: Dict) -> Dict[str, Any]:
        """Generate executive summary of simulation"""
        stats = data.get("simulation_stats", {})

        return {
            "total_messages": stats.get("total_messages", 0),
            "bot_responses": stats.get("bot_responses", 0),
            "commands_processed": stats.get("commands_processed", 0),
            "errors": stats.get("errors", 0),
            "success_rate": self._calculate_success_rate(stats),
            "average_response_time": stats.get("average_response_time", 0),
            "peak_concurrent_users": stats.get("peak_concurrent_users", 0),
        }

    def _analyze_user_behavior(self, data: Dict) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        user_stats = data.get("user_stats", {})

        return {
            "total_users": len(user_stats),
            "active_users": len(
                [u for u in user_stats.values() if u.get("activity_count", 0) > 0]
            ),
            "most_active_user": self._find_most_active_user(user_stats),
            "user_retention_rate": self._calculate_retention_rate(user_stats),
            "command_preferences": self._analyze_command_preferences(data),
        }

    def _analyze_economy(self, data: Dict) -> Dict[str, Any]:
        """Analyze economic activity"""
        return {
            "total_trades": self._count_trades(data),
            "average_trade_value": self._calculate_average_trade_value(data),
            "most_traded_item": self._find_most_traded_item(data),
            "economic_balance": self._assess_economic_balance(data),
        }

    def _analyze_performance(self, data: Dict) -> Dict[str, Any]:
        """Analyze system performance"""
        stats = data.get("simulation_stats", {})

        return {
            "response_time_distribution": self._analyze_response_times(stats),
            "error_rate": stats.get("errors", 0)
            / max(stats.get("commands_processed", 1), 1),
            "throughput": stats.get("commands_processed", 0)
            / max(stats.get("duration_seconds", 1), 1),
            "system_stability": self._assess_system_stability(stats),
        }

    def _generate_recommendations(self, data: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Analyze error patterns
        if data.get("simulation_stats", {}).get("errors", 0) > 0:
            recommendations.append(
                "Investigate error patterns to improve system stability"
            )

        # Analyze user engagement
        user_stats = data.get("user_stats", {})
        if len(user_stats) > 0:
            active_users = len(
                [u for u in user_stats.values() if u.get("activity_count", 0) > 0]
            )
            if active_users / len(user_stats) < 0.7:
                recommendations.append("Consider improving user engagement mechanisms")

        # Analyze economic balance
        if self._assess_economic_balance(data) == "unbalanced":
            recommendations.append("Review economic balance and resource distribution")

        return recommendations

    def _calculate_success_rate(self, stats: Dict) -> float:
        """Calculate command success rate"""
        total_commands = stats.get("commands_processed", 0)
        errors = stats.get("errors", 0)
        if total_commands == 0:
            return 0.0
        return (total_commands - errors) / total_commands

    def _find_most_active_user(self, user_stats: Dict) -> str:
        """Find the most active user"""
        if not user_stats:
            return "None"

        most_active = max(
            user_stats.items(), key=lambda x: x[1].get("activity_count", 0)
        )
        return most_active[0]

    def _calculate_retention_rate(self, user_stats: Dict) -> float:
        """Calculate user retention rate"""
        if not user_stats:
            return 0.0

        active_users = len(
            [u for u in user_stats.values() if u.get("activity_count", 0) > 0]
        )
        return active_users / len(user_stats)

    def _count_trades(self, data: Dict) -> int:
        """Count total trades in simulation"""
        # This would need to be implemented based on actual data structure
        return 0

    def _calculate_average_trade_value(self, data: Dict) -> float:
        """Calculate average trade value"""
        # This would need to be implemented based on actual data structure
        return 0.0

    def _find_most_traded_item(self, data: Dict) -> str:
        """Find the most traded item"""
        # This would need to be implemented based on actual data structure
        return "Unknown"

    def _assess_economic_balance(self, data: Dict) -> str:
        """Assess economic balance"""
        # This would need to be implemented based on actual data structure
        return "balanced"

    def _analyze_response_times(self, stats: Dict) -> Dict[str, float]:
        """Analyze response time distribution"""
        return {
            "average": stats.get("average_response_time", 0),
            "min": stats.get("min_response_time", 0),
            "max": stats.get("max_response_time", 0),
        }

    def _assess_system_stability(self, stats: Dict) -> str:
        """Assess overall system stability"""
        error_rate = stats.get("errors", 0) / max(stats.get("commands_processed", 1), 1)

        if error_rate < 0.01:
            return "excellent"
        elif error_rate < 0.05:
            return "good"
        elif error_rate < 0.10:
            return "fair"
        else:
            return "poor"

    def _analyze_command_preferences(self, data: Dict) -> Dict[str, int]:
        """Analyze command usage preferences"""
        # This would need to be implemented based on actual data structure
        return {}


class SimulationVisualizer:
    """Create visualizations of simulation results"""

    def __init__(self):
        self.figures = []

    def create_activity_chart(self, results_file: str, output_file: str = None):
        """Create activity timeline chart"""
        try:
            with open(results_file, "r") as f:
                data = json.load(f)

            # Extract activity data
            message_sample = data.get("message_sample", [])

            if not message_sample:
                print("No message data available for visualization")
                return

            # Create timeline
            timestamps = [msg.get("timestamp", "") for msg in message_sample]
            authors = [msg.get("author", "") for msg in message_sample]

            # Convert timestamps to datetime objects
            times = []
            for ts in timestamps:
                try:
                    if isinstance(ts, str):
                        times.append(datetime.fromisoformat(ts.replace("Z", "+00:00")))
                    else:
                        times.append(datetime.now())
                except:
                    times.append(datetime.now())

            # Create the plot
            plt.figure(figsize=(12, 6))
            plt.scatter(times, authors, alpha=0.6)
            plt.title("User Activity Timeline")
            plt.xlabel("Time")
            plt.ylabel("Users")
            plt.xticks(rotation=45)
            plt.tight_layout()

            if output_file:
                plt.savefig(output_file)
                print(f"Activity chart saved to: {output_file}")
            else:
                plt.show()

        except Exception as e:
            print(f"Error creating activity chart: {e}")

    def create_command_usage_chart(self, results_file: str, output_file: str = None):
        """Create command usage distribution chart"""
        try:
            with open(results_file, "r") as f:
                data = json.load(f)

            # Extract command data
            bot_history = data.get("bot_command_history", [])

            if not bot_history:
                print("No command history available for visualization")
                return

            # Count command usage
            command_counts = {}
            for entry in bot_history:
                command = entry.get("command", "unknown")
                command_counts[command] = command_counts.get(command, 0) + 1

            # Create the plot
            plt.figure(figsize=(10, 6))
            commands = list(command_counts.keys())
            counts = list(command_counts.values())

            plt.bar(commands, counts)
            plt.title("Command Usage Distribution")
            plt.xlabel("Commands")
            plt.ylabel("Usage Count")
            plt.xticks(rotation=45)
            plt.tight_layout()

            if output_file:
                plt.savefig(output_file)
                print(f"Command usage chart saved to: {output_file}")
            else:
                plt.show()

        except Exception as e:
            print(f"Error creating command usage chart: {e}")


class SimulationStressTester:
    """Advanced stress testing for the simulation"""

    def __init__(self):
        self.stress_scenarios = {
            "high_concurrency": self._high_concurrency_test,
            "rapid_commands": self._rapid_commands_test,
            "memory_pressure": self._memory_pressure_test,
            "network_latency": self._network_latency_test,
            "data_corruption": self._data_corruption_test,
        }

    def run_stress_test(
        self, scenario: str, simulation_instance, duration_minutes: int = 5
    ):
        """Run a specific stress test scenario"""
        if scenario not in self.stress_scenarios:
            print(f"Unknown stress scenario: {scenario}")
            return

        print(f"Running stress test: {scenario}")
        start_time = time.time()

        try:
            self.stress_scenarios[scenario](simulation_instance, duration_minutes)
            end_time = time.time()
            print(f"Stress test completed in {end_time - start_time:.2f} seconds")
        except Exception as e:
            print(f"Stress test failed: {e}")

    def _high_concurrency_test(self, simulation_instance, duration_minutes: int):
        """Test high concurrent user activity"""
        # Simulate many users acting simultaneously
        pass

    def _rapid_commands_test(self, simulation_instance, duration_minutes: int):
        """Test rapid command processing"""
        # Send commands very quickly
        pass

    def _memory_pressure_test(self, simulation_instance, duration_minutes: int):
        """Test memory pressure scenarios"""
        # Simulate memory-intensive operations
        pass

    def _network_latency_test(self, simulation_instance, duration_minutes: int):
        """Test network latency scenarios"""
        # Simulate network delays
        pass

    def _data_corruption_test(self, simulation_instance, duration_minutes: int):
        """Test data corruption scenarios"""
        # Simulate data corruption
        pass


# Export the main classes for easy import
__all__ = [
    "AdvancedUserSimulator",
    "SimulationAnalytics",
    "SimulationVisualizer",
    "SimulationStressTester",
    "UserBehaviorProfile",
]
