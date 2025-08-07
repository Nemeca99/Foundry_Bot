#!/usr/bin/env python3
"""
Resource Gathering System
Passive and active resource collection in Discord channels
"""

import asyncio
import random
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ResourceType(Enum):
    """Resource types for gathering"""

    WOOD = "wood"
    STONE = "stone"
    METAL = "metal"
    CRYSTAL = "crystal"
    ESSENCE = "essence"


class GatheringMode(Enum):
    """Gathering modes"""

    NORMAL = "normal"
    FARMING = "farming"  # Double rate, drains RP


@dataclass
class ResourceNode:
    """A resource gathering location"""

    channel_id: str
    resource_type: ResourceType
    base_rate: int = 1  # Resources per 10 seconds
    message_bonus: int = 1  # Bonus per message
    message_cooldown: int = 30  # Seconds between message bonuses
    farming_cost: int = 5  # RP per second in farming mode


class ResourceSystem:
    """Resource gathering system for Discord channels"""

    def __init__(self, db_path: str = "data/resources.db"):
        self.db_path = db_path
        self._init_database()
        self._init_resource_nodes()
        self.active_gatherers = (
            {}
        )  # user_id -> {channel_id, mode, last_gather, last_message}
        self.message_cooldowns = {}  # user_id -> {channel_id: last_message_time}

    def _init_database(self):
        """Initialize resource database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Resource inventory table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS resource_inventory (
                    user_id TEXT,
                    resource_type TEXT,
                    amount INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, resource_type)
                )
            """
            )

            # Gathering sessions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS gathering_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    total_gathered INTEGER DEFAULT 0,
                    rp_spent INTEGER DEFAULT 0
                )
            """
            )

            # Message bonuses table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS message_bonuses (
                    user_id TEXT,
                    channel_id TEXT,
                    last_message_time TIMESTAMP,
                    bonus_count INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, channel_id)
                )
            """
            )

    def _init_resource_nodes(self):
        """Initialize resource gathering nodes"""
        self.resource_nodes = {
            "wood": ResourceNode(
                channel_id="wood-1",  # Will be mapped to actual channel IDs
                resource_type=ResourceType.WOOD,
                base_rate=1,
                message_bonus=1,
                message_cooldown=30,
                farming_cost=5,
            ),
            "stone": ResourceNode(
                channel_id="stone-1",
                resource_type=ResourceType.STONE,
                base_rate=1,
                message_bonus=1,
                message_cooldown=30,
                farming_cost=5,
            ),
            "metal": ResourceNode(
                channel_id="metal-1",
                resource_type=ResourceType.METAL,
                base_rate=1,
                message_bonus=1,
                message_cooldown=30,
                farming_cost=5,
            ),
            "crystal": ResourceNode(
                channel_id="crystal-1",
                resource_type=ResourceType.CRYSTAL,
                base_rate=1,
                message_bonus=1,
                message_cooldown=30,
                farming_cost=5,
            ),
            "essence": ResourceNode(
                channel_id="essence-1",
                resource_type=ResourceType.ESSENCE,
                base_rate=1,
                message_bonus=1,
                message_cooldown=30,
                farming_cost=5,
            ),
        }

    def start_gathering(
        self, user_id: str, channel_id: str, mode: GatheringMode = GatheringMode.NORMAL
    ) -> Dict:
        """Start a gathering session"""
        # Find the resource type for this channel
        resource_type = None
        for node in self.resource_nodes.values():
            if node.channel_id == channel_id:
                resource_type = node.resource_type
                break

        if not resource_type:
            return {"success": False, "error": "Not a resource gathering channel"}

        # Check if already gathering
        if user_id in self.active_gatherers:
            return {"success": False, "error": "Already gathering in another channel"}

        # Start gathering session
        session_id = f"{user_id}_{channel_id}_{datetime.now().timestamp()}"
        self.active_gatherers[user_id] = {
            "session_id": session_id,
            "channel_id": channel_id,
            "resource_type": resource_type.value,
            "mode": mode.value,
            "start_time": datetime.now(),
            "last_gather": datetime.now(),
            "last_message": None,
        }

        # Record session in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO gathering_sessions 
                (session_id, user_id, channel_id, resource_type, mode)
                VALUES (?, ?, ?, ?, ?)
                """,
                (session_id, user_id, channel_id, resource_type.value, mode.value),
            )

        return {
            "success": True,
            "session_id": session_id,
            "resource_type": resource_type.value,
            "mode": mode.value,
            "message": f"Started gathering {resource_type.value} in {mode.value} mode",
        }

    def stop_gathering(self, user_id: str) -> Dict:
        """Stop a gathering session"""
        if user_id not in self.active_gatherers:
            return {"success": False, "error": "Not currently gathering"}

        session = self.active_gatherers[user_id]

        # Calculate final gathering results
        final_gather = self._calculate_gathering(user_id, session)

        # End session in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE gathering_sessions 
                SET end_time = CURRENT_TIMESTAMP, total_gathered = ?, rp_spent = ?
                WHERE session_id = ?
                """,
                (
                    final_gather["total_gathered"],
                    final_gather["rp_spent"],
                    session["session_id"],
                ),
            )

        # Remove from active gatherers
        del self.active_gatherers[user_id]

        return {
            "success": True,
            "total_gathered": final_gather["total_gathered"],
            "rp_spent": final_gather["rp_spent"],
            "message": f"Stopped gathering. Collected {final_gather['total_gathered']} resources",
        }

    def process_message_bonus(self, user_id: str, channel_id: str) -> Dict:
        """Process message bonus for resource gathering"""
        if user_id not in self.active_gatherers:
            return {"success": False, "error": "Not currently gathering"}

        session = self.active_gatherers[user_id]
        if session["channel_id"] != channel_id:
            return {"success": False, "error": "Not gathering in this channel"}

        # Check cooldown
        now = datetime.now()
        last_message = session.get("last_message")

        if last_message and (now - last_message).seconds < 30:  # 30 second cooldown
            return {"success": False, "error": "Message bonus on cooldown"}

        # Get resource node
        resource_type = session["resource_type"]
        node = None
        for n in self.resource_nodes.values():
            if n.resource_type.value == resource_type:
                node = n
                break

        if not node:
            return {"success": False, "error": "Invalid resource type"}

        # Add bonus resources
        bonus_amount = node.message_bonus
        if session["mode"] == GatheringMode.FARMING.value:
            bonus_amount *= 2

        self._add_resources(user_id, resource_type, bonus_amount)

        # Update last message time
        session["last_message"] = now

        return {
            "success": True,
            "bonus_amount": bonus_amount,
            "message": f"Message bonus! +{bonus_amount} {resource_type}",
        }

    def _calculate_gathering(self, user_id: str, session: Dict) -> Dict:
        """Calculate gathering results for a session"""
        now = datetime.now()
        start_time = session["start_time"]
        duration = (now - start_time).total_seconds()

        # Get resource node
        resource_type = session["resource_type"]
        node = None
        for n in self.resource_nodes.values():
            if n.resource_type.value == resource_type:
                node = n
                break

        if not node:
            return {"total_gathered": 0, "rp_spent": 0}

        # Calculate base gathering (every 10 seconds)
        base_gathers = int(duration / 10)
        base_amount = base_gathers * node.base_rate

        # Apply farming mode multiplier
        if session["mode"] == GatheringMode.FARMING.value:
            base_amount *= 2

        # Calculate RP cost for farming mode
        rp_spent = 0
        if session["mode"] == GatheringMode.FARMING.value:
            rp_spent = int(duration * node.farming_cost)

        # Add resources to inventory
        self._add_resources(user_id, resource_type, base_amount)

        return {"total_gathered": base_amount, "rp_spent": rp_spent}

    def _add_resources(self, user_id: str, resource_type: str, amount: int):
        """Add resources to user inventory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO resource_inventory (user_id, resource_type, amount, last_updated)
                VALUES (?, ?, COALESCE((SELECT amount FROM resource_inventory WHERE user_id = ? AND resource_type = ?), 0) + ?, CURRENT_TIMESTAMP)
                """,
                (user_id, resource_type, user_id, resource_type, amount),
            )

    def get_user_resources(self, user_id: str) -> Dict:
        """Get user's resource inventory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT resource_type, amount FROM resource_inventory 
                WHERE user_id = ?
                """,
                (user_id,),
            )
            results = cursor.fetchall()

        resources = {}
        for resource_type, amount in results:
            resources[resource_type] = amount

        return resources

    def get_gathering_status(self, user_id: str) -> Optional[Dict]:
        """Get current gathering status for a user"""
        if user_id not in self.active_gatherers:
            return None

        session = self.active_gatherers[user_id]
        duration = (datetime.now() - session["start_time"]).total_seconds()

        return {
            "channel_id": session["channel_id"],
            "resource_type": session["resource_type"],
            "mode": session["mode"],
            "duration": int(duration),
            "session_id": session["session_id"],
        }

    def get_resource_nodes(self) -> Dict:
        """Get all resource nodes"""
        return {
            name: {
                "channel_id": node.channel_id,
                "resource_type": node.resource_type.value,
                "base_rate": node.base_rate,
                "message_bonus": node.message_bonus,
                "message_cooldown": node.message_cooldown,
                "farming_cost": node.farming_cost,
            }
            for name, node in self.resource_nodes.items()
        }

    def get_status(self) -> str:
        """Get system status"""
        active_sessions = len(self.active_gatherers)
        return f"Resource System: {active_sessions} active gathering sessions"
