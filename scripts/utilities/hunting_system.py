#!/usr/bin/env python3
"""
Hunting System for Catching Simulacra
RP-based hunting in world chat channels
"""

import asyncio
import random
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class HuntingEvent(Enum):
    """Types of hunting events"""

    BREEDING = "breeding"  # Heavy breathing signal
    WILD_SPAWN = "wild_spawn"  # Random spawn
    MIGRATION = "migration"  # Group movement
    TERRITORIAL = "territorial"  # Territory dispute


@dataclass
class SimulacraSpawn:
    """A Simulacra spawn event"""

    spawn_id: str
    event_type: HuntingEvent
    channel_id: str
    spawn_time: datetime
    duration: int = 300  # 5 minutes
    catch_cost: int = 100  # RP cost to attempt catch
    max_catches: int = 1  # Only 1 catch per spawn
    current_catches: int = 0
    is_active: bool = True


class HuntingSystem:
    """Hunting system for catching Simulacra"""

    def __init__(self, db_path: str = "data/hunting.db"):
        self.db_path = db_path
        self._init_database()
        self.active_spawns = {}  # spawn_id -> SimulacraSpawn
        self.world_channels = [
            "public-chat-1",
            "public-chat-2",
            "public-chat-3",
        ]  # World chat channels
        self.ai_power_level = 1.0  # Scales with global population

    def _init_database(self):
        """Initialize hunting database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Spawn events table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS spawn_events (
                    spawn_id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    spawn_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    duration INTEGER DEFAULT 300,
                    catch_cost INTEGER DEFAULT 100,
                    max_catches INTEGER DEFAULT 1,
                    current_catches INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """
            )

            # Catch attempts table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS catch_attempts (
                    attempt_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    spawn_id TEXT NOT NULL,
                    rp_spent INTEGER NOT NULL,
                    success BOOLEAN NOT NULL,
                    simulacra_id TEXT,
                    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (spawn_id) REFERENCES spawn_events (spawn_id)
                )
            """
            )

            # Global stats table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS hunting_stats (
                    stat_key TEXT PRIMARY KEY,
                    stat_value REAL DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

    def create_spawn_event(
        self, event_type: HuntingEvent, channel_id: str = None
    ) -> Dict:
        """Create a new Simulacra spawn event"""
        if channel_id is None:
            channel_id = random.choice(self.world_channels)

        spawn_id = f"{event_type.value}_{channel_id}_{datetime.now().timestamp()}"

        # Calculate catch cost based on AI power level
        base_cost = 100
        catch_cost = int(base_cost * self.ai_power_level)

        spawn = SimulacraSpawn(
            spawn_id=spawn_id,
            event_type=event_type,
            channel_id=channel_id,
            spawn_time=datetime.now(),
            duration=300,
            catch_cost=catch_cost,
            max_catches=1,
            current_catches=0,
            is_active=True,
        )

        self.active_spawns[spawn_id] = spawn

        # Record in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO spawn_events 
                (spawn_id, event_type, channel_id, spawn_time, duration, catch_cost, max_catches)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    spawn_id,
                    event_type.value,
                    channel_id,
                    spawn.spawn_time,
                    spawn.duration,
                    spawn.catch_cost,
                    spawn.max_catches,
                ),
            )

        return {
            "success": True,
            "spawn_id": spawn_id,
            "event_type": event_type.value,
            "channel_id": channel_id,
            "catch_cost": catch_cost,
            "message": self._get_spawn_message(event_type, channel_id),
        }

    def attempt_catch(self, user_id: str, spawn_id: str, rp_amount: int) -> Dict:
        """Attempt to catch a Simulacra"""
        if spawn_id not in self.active_spawns:
            return {"success": False, "error": "Spawn event not found or expired"}

        spawn = self.active_spawns[spawn_id]

        # Check if spawn is still active
        if not spawn.is_active:
            return {"success": False, "error": "Spawn event has expired"}

        # Check if max catches reached
        if spawn.current_catches >= spawn.max_catches:
            return {"success": False, "error": "Maximum catches reached for this spawn"}

        # Check if user has enough RP
        if rp_amount < spawn.catch_cost:
            return {
                "success": False,
                "error": f"Not enough RP. Need {spawn.catch_cost} RP",
            }

        # Calculate catch success rate
        success_rate = self._calculate_catch_success_rate(spawn.event_type)
        success = random.random() < success_rate

        # Record attempt
        attempt_id = f"{user_id}_{spawn_id}_{datetime.now().timestamp()}"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO catch_attempts 
                (attempt_id, user_id, spawn_id, rp_spent, success)
                VALUES (?, ?, ?, ?, ?)
                """,
                (attempt_id, user_id, spawn_id, rp_amount, success),
            )

        if success:
            # Generate caught Simulacra
            simulacra_id = self._generate_caught_simulacra(user_id, spawn.event_type)
            spawn.current_catches += 1

            # Update database with simulacra_id
            cursor.execute(
                """
                UPDATE catch_attempts SET simulacra_id = ? WHERE attempt_id = ?
                """,
                (simulacra_id, attempt_id),
            )

            # Increase AI power level
            self._increase_ai_power()

            return {
                "success": True,
                "caught": True,
                "simulacra_id": simulacra_id,
                "rp_spent": rp_amount,
                "message": f"🎉 Successfully caught a Simulacra! (Cost: {rp_amount} RP)",
            }
        else:
            return {
                "success": True,
                "caught": False,
                "rp_spent": rp_amount,
                "message": f"❌ The Simulacra escaped! (Cost: {rp_amount} RP)",
            }

    def _calculate_catch_success_rate(self, event_type: HuntingEvent) -> float:
        """Calculate catch success rate based on event type"""
        base_rates = {
            HuntingEvent.BREEDING: 0.8,  # 80% success
            HuntingEvent.WILD_SPAWN: 0.6,  # 60% success
            HuntingEvent.MIGRATION: 0.7,  # 70% success
            HuntingEvent.TERRITORIAL: 0.5,  # 50% success
        }

        base_rate = base_rates.get(event_type, 0.5)

        # AI power level affects difficulty
        difficulty_modifier = 1.0 - (self.ai_power_level - 1.0) * 0.1
        final_rate = base_rate * difficulty_modifier

        return max(0.1, min(0.9, final_rate))  # Clamp between 10% and 90%

    def _generate_caught_simulacra(self, user_id: str, event_type: HuntingEvent) -> str:
        """Generate a new Simulacra for the user"""
        # This would integrate with the C.L.D.S. system
        # For now, return a placeholder ID
        simulacra_id = f"simulacra_{user_id}_{datetime.now().timestamp()}"

        # TODO: Integrate with C.L.D.S. system to generate actual Simulacra
        # This would call the CLDSSystem to create a new drone

        return simulacra_id

    def _increase_ai_power(self):
        """Increase AI power level when Simulacra are caught"""
        self.ai_power_level += 0.01  # Small increase per catch

        # Update in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO hunting_stats (stat_key, stat_value, last_updated)
                VALUES ('ai_power_level', ?, CURRENT_TIMESTAMP)
                """,
                (self.ai_power_level,),
            )

    def _get_spawn_message(self, event_type: HuntingEvent, channel_id: str) -> str:
        """Get spawn event message"""
        messages = {
            HuntingEvent.BREEDING: f"🌊 **Heavy breathing detected in {channel_id}** - A breeding event has begun!",
            HuntingEvent.WILD_SPAWN: f"🌟 **Wild Simulacra spotted in {channel_id}** - Quick, before it escapes!",
            HuntingEvent.MIGRATION: f"🦅 **Migration event in {channel_id}** - A group of Simulacra is passing through!",
            HuntingEvent.TERRITORIAL: f"⚔️ **Territorial dispute in {channel_id}** - Simulacra are fighting for territory!",
        }
        return messages.get(event_type, f"🐾 **Simulacra activity in {channel_id}**")

    def get_active_spawns(self) -> List[Dict]:
        """Get all active spawn events"""
        active_spawns = []
        now = datetime.now()

        for spawn_id, spawn in self.active_spawns.items():
            # Check if spawn has expired
            if (now - spawn.spawn_time).total_seconds() > spawn.duration:
                spawn.is_active = False
                continue

            if spawn.is_active:
                active_spawns.append(
                    {
                        "spawn_id": spawn_id,
                        "event_type": spawn.event_type.value,
                        "channel_id": spawn.channel_id,
                        "catch_cost": spawn.catch_cost,
                        "max_catches": spawn.max_catches,
                        "current_catches": spawn.current_catches,
                        "time_remaining": spawn.duration
                        - int((now - spawn.spawn_time).total_seconds()),
                    }
                )

        return active_spawns

    def get_user_catch_history(self, user_id: str) -> List[Dict]:
        """Get user's catch history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT ca.attempt_id, ca.spawn_id, ca.rp_spent, ca.success, 
                       ca.simulacra_id, ca.attempt_time, se.event_type
                FROM catch_attempts ca
                JOIN spawn_events se ON ca.spawn_id = se.spawn_id
                WHERE ca.user_id = ?
                ORDER BY ca.attempt_time DESC
                LIMIT 20
                """,
                (user_id,),
            )
            results = cursor.fetchall()

        history = []
        for row in results:
            history.append(
                {
                    "attempt_id": row[0],
                    "spawn_id": row[1],
                    "rp_spent": row[2],
                    "success": bool(row[3]),
                    "simulacra_id": row[4],
                    "attempt_time": row[5],
                    "event_type": row[6],
                }
            )

        return history

    def get_ai_power_level(self) -> float:
        """Get current AI power level"""
        return self.ai_power_level

    def get_hunting_stats(self) -> Dict:
        """Get hunting statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total spawns
            cursor.execute("SELECT COUNT(*) FROM spawn_events")
            total_spawns = cursor.fetchone()[0]

            # Total catches
            cursor.execute("SELECT COUNT(*) FROM catch_attempts WHERE success = 1")
            total_catches = cursor.fetchone()[0]

            # Total attempts
            cursor.execute("SELECT COUNT(*) FROM catch_attempts")
            total_attempts = cursor.fetchone()[0]

            # Total RP spent
            cursor.execute("SELECT SUM(rp_spent) FROM catch_attempts")
            total_rp_spent = cursor.fetchone()[0] or 0

        return {
            "total_spawns": total_spawns,
            "total_catches": total_catches,
            "total_attempts": total_attempts,
            "success_rate": total_catches / max(1, total_attempts),
            "total_rp_spent": total_rp_spent,
            "ai_power_level": self.ai_power_level,
        }

    def cleanup_expired_spawns(self):
        """Clean up expired spawn events"""
        now = datetime.now()
        expired_spawns = []

        for spawn_id, spawn in self.active_spawns.items():
            if (now - spawn.spawn_time).total_seconds() > spawn.duration:
                spawn.is_active = False
                expired_spawns.append(spawn_id)

        # Remove expired spawns from active list
        for spawn_id in expired_spawns:
            del self.active_spawns[spawn_id]

        # Update database
        if expired_spawns:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE spawn_events 
                    SET is_active = FALSE 
                    WHERE spawn_id IN ({})
                    """.format(
                        ",".join(["?" for _ in expired_spawns])
                    ),
                    expired_spawns,
                )

    def get_status(self) -> str:
        """Get system status"""
        active_spawns = len([s for s in self.active_spawns.values() if s.is_active])
        return f"Hunting System: {active_spawns} active spawns, AI Power: {self.ai_power_level:.2f}"
