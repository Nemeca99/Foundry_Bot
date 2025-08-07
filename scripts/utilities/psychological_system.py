#!/usr/bin/env python3
"""
Psychological Manipulation System
All scum tricks for free - FOMO, addiction, social pressure, etc.
"""

import sqlite3
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class HookType(Enum):
    """Psychological hook types"""

    FOMO = "fomo"  # Fear of Missing Out
    ADDICTION = "addiction"  # Variable rewards
    SOCIAL_PRESSURE = "social_pressure"  # Social comparison
    NEAR_MISS = "near_miss"  # Almost won
    LOSS_AVERSION = "loss_aversion"  # Fear of losing
    VARIABLE_REWARDS = "variable_rewards"  # Unpredictable rewards


class EventType(Enum):
    """Psychological event types"""

    LIMITED_TIME = "limited_time"
    DAILY_BONUS = "daily_bonus"
    STREAK_REWARD = "streak_reward"
    ACHIEVEMENT = "achievement"
    SOCIAL_COMPARISON = "social_comparison"
    NEAR_MISS = "near_miss"


@dataclass
class PsychologicalEvent:
    """A psychological manipulation event"""

    event_id: str
    event_type: EventType
    hook_type: HookType
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    reward_type: str  # rp_bonus, cosmetic_item, etc.
    reward_amount: int
    max_participants: int
    current_participants: int = 0


@dataclass
class UserStreak:
    """User streak tracking"""

    user_id: str
    streak_type: str  # daily, survival, gacha, etc.
    current_streak: int
    longest_streak: int
    last_activity: datetime
    next_bonus: datetime


@dataclass
class Achievement:
    """Achievement system"""

    achievement_id: str
    title: str
    description: str
    requirement: str
    reward_rp: int
    reward_cosmetic: str = None
    rarity: str = "common"  # common, uncommon, rare, epic, legendary


class PsychologicalSystem:
    """Psychological manipulation system - all scum tricks for free"""

    def __init__(self, db_path: str = "data/psychological.db"):
        self.db_path = db_path
        self._init_database()
        self._init_achievements()
        self._init_events()

    def _init_database(self):
        """Initialize psychological database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Psychological events table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS psychological_events (
                    event_id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    hook_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    start_date TIMESTAMP NOT NULL,
                    end_date TIMESTAMP NOT NULL,
                    reward_type TEXT NOT NULL,
                    reward_amount INTEGER NOT NULL,
                    max_participants INTEGER NOT NULL,
                    current_participants INTEGER DEFAULT 0
                )
            """
            )

            # User streaks table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_streaks (
                    user_id TEXT,
                    streak_type TEXT NOT NULL,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    next_bonus TIMESTAMP,
                    PRIMARY KEY (user_id, streak_type)
                )
            """
            )

            # Achievements table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS achievements (
                    achievement_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    requirement TEXT NOT NULL,
                    reward_rp INTEGER NOT NULL,
                    reward_cosmetic TEXT,
                    rarity TEXT DEFAULT 'common'
                )
            """
            )

            # User achievements table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_achievements (
                    user_id TEXT,
                    achievement_id TEXT,
                    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, achievement_id)
                )
            """
            )

            # Daily bonuses table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_bonuses (
                    user_id TEXT PRIMARY KEY,
                    last_bonus TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    bonus_streak INTEGER DEFAULT 0,
                    total_bonuses INTEGER DEFAULT 0
                )
            """
            )

    def _init_achievements(self):
        """Initialize achievement system"""
        achievements = [
            Achievement(
                achievement_id="first_steps",
                title="First Steps",
                description="Hatch your first DigiDrone",
                requirement="hatch_drone",
                reward_rp=50,
                rarity="common",
            ),
            Achievement(
                achievement_id="survivor",
                title="Survivor",
                description="Survive for 60 seconds",
                requirement="survive_60s",
                reward_rp=100,
                rarity="common",
            ),
            Achievement(
                achievement_id="scientist",
                title="Scientist",
                description="Complete a scientific challenge",
                requirement="complete_science",
                reward_rp=150,
                rarity="uncommon",
            ),
            Achievement(
                achievement_id="collector",
                title="Collector",
                description="Own 5 different drones",
                requirement="own_5_drones",
                reward_rp=200,
                rarity="uncommon",
            ),
            Achievement(
                achievement_id="shiny_collector",
                title="Shiny Collector",
                description="Own a shiny drone",
                requirement="own_shiny",
                reward_rp=500,
                reward_cosmetic="shiny_badge",
                rarity="rare",
            ),
            Achievement(
                achievement_id="kingdom_ruler",
                title="Kingdom Ruler",
                description="Become a kingdom ruler",
                requirement="claim_throne",
                reward_rp=1000,
                reward_cosmetic="crown_emote",
                rarity="epic",
            ),
            Achievement(
                achievement_id="council_member",
                title="Council Member",
                description="Join the Council of 7",
                requirement="join_council",
                reward_rp=2000,
                reward_cosmetic="council_emblem",
                rarity="legendary",
            ),
            Achievement(
                achievement_id="survival_master",
                title="Survival Master",
                description="Survive for 10 minutes",
                requirement="survive_600s",
                reward_rp=1000,
                rarity="epic",
            ),
            Achievement(
                achievement_id="gacha_master",
                title="Gacha Master",
                description="Pull 100 times",
                requirement="pull_100",
                reward_rp=500,
                rarity="rare",
            ),
            Achievement(
                achievement_id="scientific_genius",
                title="Scientific Genius",
                description="Complete 10 scientific challenges",
                requirement="complete_10_science",
                reward_rp=1500,
                rarity="epic",
            ),
        ]

        # Save achievements to database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for achievement in achievements:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO achievements 
                    (achievement_id, title, description, requirement, reward_rp, reward_cosmetic, rarity)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        achievement.achievement_id,
                        achievement.title,
                        achievement.description,
                        achievement.requirement,
                        achievement.reward_rp,
                        achievement.reward_cosmetic,
                        achievement.rarity,
                    ),
                )

    def _init_events(self):
        """Initialize psychological events"""
        self.active_events = {}
        self._schedule_events()

    def _schedule_events(self):
        """Schedule psychological events"""
        now = datetime.now()

        # Limited time survival challenge
        self.active_events["limited_survival"] = PsychologicalEvent(
            event_id="limited_survival",
            event_type=EventType.LIMITED_TIME,
            hook_type=HookType.FOMO,
            title="🔥 Fire Survival Challenge",
            description="Limited time event! Survive fire disasters for bonus RP!",
            start_date=now,
            end_date=now + timedelta(days=3),
            reward_type="rp_bonus",
            reward_amount=50,
            max_participants=100,
        )

        # Daily bonus streak
        self.active_events["daily_streak"] = PsychologicalEvent(
            event_id="daily_streak",
            event_type=EventType.DAILY_BONUS,
            hook_type=HookType.ADDICTION,
            title="📅 Daily Streak Bonus",
            description="Log in daily for increasing RP bonuses!",
            start_date=now,
            end_date=now + timedelta(days=30),
            reward_type="rp_bonus",
            reward_amount=25,
            max_participants=1000,
        )

        # Gacha addiction event
        self.active_events["gacha_fever"] = PsychologicalEvent(
            event_id="gacha_fever",
            event_type=EventType.LIMITED_TIME,
            hook_type=HookType.VARIABLE_REWARDS,
            title="🎰 Gacha Fever",
            description="Increased shiny odds for 24 hours!",
            start_date=now,
            end_date=now + timedelta(days=1),
            reward_type="shiny_boost",
            reward_amount=2,  # 2x shiny odds
            max_participants=500,
        )

        # Social comparison event
        self.active_events["survival_contest"] = PsychologicalEvent(
            event_id="survival_contest",
            event_type=EventType.SOCIAL_COMPARISON,
            hook_type=HookType.SOCIAL_PRESSURE,
            title="🏆 Survival Contest",
            description="Compete for the longest survival time!",
            start_date=now,
            end_date=now + timedelta(days=7),
            reward_type="rp_bonus",
            reward_amount=200,
            max_participants=200,
        )

    def get_active_events(self) -> List[PsychologicalEvent]:
        """Get all active psychological events"""
        now = datetime.now()
        active_events = []

        for event in self.active_events.values():
            if event.start_date <= now <= event.end_date:
                active_events.append(event)

        return active_events

    def get_daily_bonus(self, user_id: str) -> Dict:
        """Get daily bonus with variable rewards"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if user can claim daily bonus
                cursor.execute(
                    "SELECT last_bonus, bonus_streak FROM daily_bonuses WHERE user_id = ?",
                    (user_id,),
                )
                result = cursor.fetchone()

                now = datetime.now()

                if result:
                    last_bonus = datetime.fromisoformat(result[0])
                    bonus_streak = result[1]

                    # Check if 24 hours have passed
                    if now - last_bonus < timedelta(hours=24):
                        time_remaining = timedelta(hours=24) - (now - last_bonus)
                        return {
                            "success": False,
                            "error": f"Daily bonus available in {time_remaining}",
                            "time_remaining": time_remaining,
                        }
                else:
                    bonus_streak = 0

                # Calculate variable reward (addiction hook)
                base_reward = 25
                streak_multiplier = min(bonus_streak * 0.1, 1.0)  # Max 100% bonus
                random_bonus = random.randint(0, 20)  # 0-20 RP random bonus

                total_reward = int(base_reward * (1 + streak_multiplier) + random_bonus)

                # Update database
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO daily_bonuses 
                    (user_id, last_bonus, bonus_streak, total_bonuses)
                    VALUES (?, ?, ?, ?)
                """,
                    (user_id, now, bonus_streak + 1, (result[2] if result else 0) + 1),
                )

                return {
                    "success": True,
                    "reward": total_reward,
                    "streak": bonus_streak + 1,
                    "base_reward": base_reward,
                    "streak_bonus": int(base_reward * streak_multiplier),
                    "random_bonus": random_bonus,
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to get daily bonus: {str(e)}"}

    def check_achievement(
        self, user_id: str, action: str, value: int = 1
    ) -> List[Achievement]:
        """Check if user earned any achievements"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get user's current achievements
                cursor.execute(
                    "SELECT achievement_id FROM user_achievements WHERE user_id = ?",
                    (user_id,),
                )
                earned_achievements = {row[0] for row in cursor.fetchall()}

                # Get all achievements
                cursor.execute("SELECT * FROM achievements")
                all_achievements = cursor.fetchall()

                newly_earned = []

                for achievement_data in all_achievements:
                    achievement_id = achievement_data[0]

                    if achievement_id in earned_achievements:
                        continue

                    requirement = achievement_data[3]

                    # Check if achievement is earned
                    if self._check_achievement_requirement(
                        user_id, requirement, action, value
                    ):
                        # Award achievement
                        cursor.execute(
                            """
                            INSERT INTO user_achievements (user_id, achievement_id)
                            VALUES (?, ?)
                        """,
                            (user_id, achievement_id),
                        )

                        newly_earned.append(
                            Achievement(
                                achievement_id=achievement_data[0],
                                title=achievement_data[1],
                                description=achievement_data[2],
                                requirement=achievement_data[3],
                                reward_rp=achievement_data[4],
                                reward_cosmetic=achievement_data[5],
                                rarity=achievement_data[6],
                            )
                        )

                return newly_earned

        except Exception as e:
            return []

    def _check_achievement_requirement(
        self, user_id: str, requirement: str, action: str, value: int
    ) -> bool:
        """Check if achievement requirement is met"""
        # Simple requirement checking - in real implementation would be more sophisticated
        requirement_map = {
            "hatch_drone": action == "hatch",
            "survive_60s": action == "survive" and value >= 60,
            "survive_600s": action == "survive" and value >= 600,
            "complete_science": action == "science",
            "own_5_drones": action == "count_drones" and value >= 5,
            "own_shiny": action == "own_shiny",
            "claim_throne": action == "claim_throne",
            "join_council": action == "join_council",
            "pull_100": action == "gacha_pull" and value >= 100,
            "complete_10_science": action == "science_complete" and value >= 10,
        }

        return requirement_map.get(requirement, False)

    def generate_near_miss(self, user_id: str, action: str) -> Dict:
        """Generate near-miss scenario to encourage continued engagement"""
        near_misses = {
            "gacha": {
                "message": "🎰 So close! You were just 1 number away from a shiny!",
                "encouragement": "Try again - your luck is building up!",
                "bonus_odds": 1.1,  # 10% increased odds next time
            },
            "survival": {
                "message": "💀 Almost survived! You made it 95% of the way!",
                "encouragement": "You're getting better - try again!",
                "bonus_resistance": 5,  # +5 resistance next time
            },
            "science": {
                "message": "🧪 Nearly solved it! You were 90% correct!",
                "encouragement": "Your scientific reasoning is improving!",
                "bonus_rp": 10,  # +10 RP for trying
            },
        }

        near_miss = near_misses.get(
            action,
            {
                "message": "So close! Try again!",
                "encouragement": "You're getting better!",
                "bonus": 0,
            },
        )

        return {
            "type": "near_miss",
            "action": action,
            "message": near_miss["message"],
            "encouragement": near_miss["encouragement"],
            "bonus": near_miss.get(
                "bonus_odds",
                near_miss.get("bonus_resistance", near_miss.get("bonus_rp", 0)),
            ),
        }

    def generate_social_pressure(self, user_id: str) -> Dict:
        """Generate social pressure data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get user's stats
                cursor.execute(
                    """
                    SELECT total_bonuses, bonus_streak 
                    FROM daily_bonuses 
                    WHERE user_id = ?
                """,
                    (user_id,),
                )
                user_stats = cursor.fetchone()

                # Get top performers
                cursor.execute(
                    """
                    SELECT user_id, bonus_streak 
                    FROM daily_bonuses 
                    ORDER BY bonus_streak DESC 
                    LIMIT 5
                """
                )
                top_performers = cursor.fetchall()

                if user_stats:
                    user_streak = user_stats[1]
                    user_total = user_stats[0]

                    # Find user's rank
                    user_rank = 1
                    for performer_id, performer_streak in top_performers:
                        if performer_id == user_id:
                            break
                        user_rank += 1

                    # Generate social pressure message
                    if user_rank <= 3:
                        message = f"🏆 You're in the top {user_rank}! Keep it up!"
                        pressure_type = "positive"
                    elif user_rank <= 10:
                        message = (
                            f"📈 You're ranked #{user_rank}. Can you climb higher?"
                        )
                        pressure_type = "motivational"
                    else:
                        message = (
                            f"📊 You're ranked #{user_rank}. Others are ahead of you!"
                        )
                        pressure_type = "competitive"

                    return {
                        "type": "social_pressure",
                        "user_rank": user_rank,
                        "user_streak": user_streak,
                        "top_performers": len(top_performers),
                        "message": message,
                        "pressure_type": pressure_type,
                    }

                return {
                    "type": "social_pressure",
                    "message": "Start your journey to climb the ranks!",
                    "pressure_type": "motivational",
                }

        except Exception as e:
            return {
                "type": "social_pressure",
                "message": "Join the competition!",
                "pressure_type": "motivational",
            }

    def get_variable_reward(self, action: str) -> Dict:
        """Generate variable reward to maintain addiction"""
        base_rewards = {
            "survival": {"min": 10, "max": 50, "bonus_chance": 0.2},
            "gacha": {"min": 5, "max": 25, "bonus_chance": 0.1},
            "science": {"min": 15, "max": 75, "bonus_chance": 0.15},
            "daily": {"min": 20, "max": 100, "bonus_chance": 0.25},
        }

        reward_config = base_rewards.get(
            action, {"min": 10, "max": 30, "bonus_chance": 0.1}
        )

        # Base reward
        base_reward = random.randint(reward_config["min"], reward_config["max"])

        # Bonus chance (addiction hook)
        bonus_reward = 0
        if random.random() < reward_config["bonus_chance"]:
            bonus_reward = random.randint(base_reward // 2, base_reward)

        total_reward = base_reward + bonus_reward

        return {
            "base_reward": base_reward,
            "bonus_reward": bonus_reward,
            "total_reward": total_reward,
            "got_bonus": bonus_reward > 0,
        }

    def get_psychological_hooks(self, user_id: str) -> Dict:
        """Get all psychological hooks for a user"""
        hooks = {
            "fomo": self._generate_fomo_hooks(user_id),
            "addiction": self._generate_addiction_hooks(user_id),
            "social_pressure": self._generate_social_pressure_hooks(user_id),
            "near_miss": self._generate_near_miss_hooks(user_id),
            "loss_aversion": self._generate_loss_aversion_hooks(user_id),
            "variable_rewards": self._generate_variable_reward_hooks(user_id),
        }
        return hooks

    def get_status(self) -> str:
        """Get the status of the psychological system"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count active events
                cursor.execute("SELECT COUNT(*) FROM psychological_events WHERE end_date > datetime('now')")
                active_events = cursor.fetchone()[0]
                
                # Count achievements
                cursor.execute("SELECT COUNT(*) FROM achievements")
                achievement_count = cursor.fetchone()[0]
                
                # Count user streaks
                cursor.execute("SELECT COUNT(*) FROM user_streaks")
                streak_count = cursor.fetchone()[0]
                
                # Count hook types
                hook_types = len(HookType)
                event_types = len(EventType)
            
            return f"Active Events: {active_events}, Achievements: {achievement_count}, Streaks: {streak_count}, Hook Types: {hook_types}, Event Types: {event_types}"
            
        except Exception as e:
            return f"Error: {str(e)}"

    def _generate_fomo_hooks(self, user_id: str) -> Dict:
        """Generate FOMO hooks for a user"""
        return {
            "limited_time_events": self.get_active_events(),
            "daily_bonus": self.get_daily_bonus(user_id),
            "streak_rewards": self._get_user_streaks(user_id)
        }

    def _generate_addiction_hooks(self, user_id: str) -> Dict:
        """Generate addiction hooks for a user"""
        return {
            "variable_rewards": self.get_variable_reward("general"),
            "near_misses": self.generate_near_miss(user_id, "general"),
            "progressive_rewards": self._get_progressive_rewards(user_id)
        }

    def _generate_social_pressure_hooks(self, user_id: str) -> Dict:
        """Generate social pressure hooks for a user"""
        return {
            "social_comparison": self.generate_social_pressure(user_id),
            "leaderboard_position": self._get_leaderboard_position(user_id),
            "peer_achievements": self._get_peer_achievements(user_id)
        }

    def _generate_near_miss_hooks(self, user_id: str) -> Dict:
        """Generate near miss hooks for a user"""
        return {
            "recent_near_misses": self.generate_near_miss(user_id, "recent"),
            "almost_achievements": self._get_almost_achievements(user_id),
            "close_calls": self._get_close_calls(user_id)
        }

    def _generate_loss_aversion_hooks(self, user_id: str) -> Dict:
        """Generate loss aversion hooks for a user"""
        return {
            "potential_losses": self._get_potential_losses(user_id),
            "sunk_costs": self._get_sunk_costs(user_id),
            "maintenance_costs": self._get_maintenance_costs(user_id)
        }

    def _generate_variable_reward_hooks(self, user_id: str) -> Dict:
        """Generate variable reward hooks for a user"""
        return {
            "survival_rewards": self.get_variable_reward("survival"),
            "gacha_rewards": self.get_variable_reward("gacha"),
            "science_rewards": self.get_variable_reward("science")
        }

    def _get_user_streaks(self, user_id: str) -> List[Dict]:
        """Get user streaks"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM user_streaks WHERE user_id = ?",
                    (user_id,)
                )
                return cursor.fetchall()
        except:
            return []

    def _get_progressive_rewards(self, user_id: str) -> Dict:
        """Get progressive rewards for user"""
        return {
            "next_level": 10,
            "progress": 7,
            "reward": "50 RP"
        }

    def _get_leaderboard_position(self, user_id: str) -> Dict:
        """Get user's leaderboard position"""
        return {
            "position": 15,
            "total_players": 100,
            "next_position": 14
        }

    def _get_peer_achievements(self, user_id: str) -> List[Dict]:
        """Get peer achievements"""
        return [
            {"title": "First Hatch", "user": "Player123"},
            {"title": "Survival Master", "user": "Player456"}
        ]

    def _get_almost_achievements(self, user_id: str) -> List[Dict]:
        """Get almost achieved achievements"""
        return [
            {"title": "Gacha Master", "progress": "8/10"},
            {"title": "Survival Expert", "progress": "45/50"}
        ]

    def _get_close_calls(self, user_id: str) -> List[Dict]:
        """Get recent close calls"""
        return [
            {"type": "survival", "time": "2 seconds ago"},
            {"type": "gacha", "time": "5 minutes ago"}
        ]

    def _get_potential_losses(self, user_id: str) -> List[Dict]:
        """Get potential losses"""
        return [
            {"type": "daily_streak", "time": "23 hours"},
            {"type": "achievement_progress", "time": "1 day"}
        ]

    def _get_sunk_costs(self, user_id: str) -> List[Dict]:
        """Get sunk costs"""
        return [
            {"type": "time_invested", "value": "5 hours"},
            {"type": "rp_spent", "value": "250 RP"}
        ]

    def _get_maintenance_costs(self, user_id: str) -> List[Dict]:
        """Get maintenance costs"""
        return [
            {"type": "daily_login", "cost": "5 minutes"},
            {"type": "drone_feeding", "cost": "10 RP"}
        ]
