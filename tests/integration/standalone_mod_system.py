"""
Standalone Mod System for Simulation
Doesn't require Discord bot imports
"""

import sqlite3
import json
import random
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
import os


@dataclass
class ModTemplate:
    """Template for creating mods"""

    id: str
    name: str
    description: str
    category: str  # 'economy', 'personality', 'gameplay'
    cost: int
    duration: int  # days, 0 = permanent
    effects: Dict[str, Any]
    requirements: Dict[str, Any]
    max_uses: int = -1  # -1 = unlimited


@dataclass
class PlayerModProfile:
    """Player's mod profile and slots"""

    user_id: str
    username: str
    mod_slots: int = 3
    active_mods: List[str] = None  # List of active mod IDs
    owned_mods: List[str] = None  # List of owned mod IDs
    total_rp_earned: int = 0
    total_rp_spent: int = 0
    mod_purchases: int = 0

    def __post_init__(self):
        if self.active_mods is None:
            self.active_mods = []
        if self.owned_mods is None:
            self.owned_mods = []


class StandaloneModSystem:
    """Standalone mod system without Discord dependencies"""

    def __init__(self, db_path: str = "data/simulation_mods.db"):
        self.db_path = db_path
        self.ensure_db_directory()
        self.init_database()
        self.load_mod_templates()

    def ensure_db_directory(self):
        """Ensure the database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def init_database(self):
        """Initialize the database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Mod templates table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS mod_templates (
                    mod_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    cost INTEGER,
                    duration INTEGER,
                    effects TEXT,
                    requirements TEXT,
                    max_uses INTEGER DEFAULT -1
                )
            """
            )

            # Player profiles table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS player_profiles (
                    user_id TEXT PRIMARY KEY,
                    username TEXT,
                    mod_slots INTEGER DEFAULT 3,
                    active_mods TEXT,
                    owned_mods TEXT,
                    total_rp_earned INTEGER DEFAULT 0,
                    total_rp_spent INTEGER DEFAULT 0,
                    mod_purchases INTEGER DEFAULT 0
                )
            """
            )

            conn.commit()

    def load_mod_templates(self):
        """Load or create default mod templates"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM mod_templates")
            if cursor.fetchone()[0] == 0:
                self.create_default_templates()

    def create_default_templates(self):
        """Create default mod templates"""
        templates = [
            ModTemplate(
                id="rp_boost",
                name="RP Boost",
                description="Earn 20% more RP from all activities",
                category="economy",
                cost=100,
                duration=7,
                effects={"rp_multiplier": 1.2},
                requirements={"min_level": 1},
            ),
            ModTemplate(
                id="hunt_master",
                name="Hunt Master",
                description="Hunting activities cost 15% less RP",
                category="economy",
                cost=150,
                duration=5,
                effects={"hunt_cost_reduction": 0.15},
                requirements={"min_level": 2},
            ),
            ModTemplate(
                id="social_butterfly",
                name="Social Butterfly",
                description="Social activities are 25% more effective",
                category="personality",
                cost=80,
                duration=10,
                effects={"social_effectiveness": 1.25},
                requirements={"min_level": 1},
            ),
            ModTemplate(
                id="lucky_charm",
                name="Lucky Charm",
                description="10% chance to get bonus rewards",
                category="gameplay",
                cost=200,
                duration=3,
                effects={"bonus_chance": 0.1},
                requirements={"min_level": 3},
            ),
        ]

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for template in templates:
                cursor.execute(
                    """
                    INSERT INTO mod_templates 
                    (mod_id, name, description, category, cost, duration, effects, requirements, max_uses)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        template.id,
                        template.name,
                        template.description,
                        template.category,
                        template.cost,
                        template.duration,
                        json.dumps(template.effects),
                        json.dumps(template.requirements),
                        template.max_uses,
                    ),
                )
            conn.commit()

    def get_mod_template(self, mod_id: str) -> Optional[ModTemplate]:
        """Get a mod template by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mod_templates WHERE mod_id = ?", (mod_id,))
            row = cursor.fetchone()

            if row:
                return ModTemplate(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    category=row[3],
                    cost=row[4],
                    duration=row[5],
                    effects=json.loads(row[6]),
                    requirements=json.loads(row[7]),
                    max_uses=row[8],
                )
        return None

    def get_all_templates(self) -> List[ModTemplate]:
        """Get all mod templates"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mod_templates")
            rows = cursor.fetchall()

            templates = []
            for row in rows:
                templates.append(
                    ModTemplate(
                        id=row[0],
                        name=row[1],
                        description=row[2],
                        category=row[3],
                        cost=row[4],
                        duration=row[5],
                        effects=json.loads(row[6]),
                        requirements=json.loads(row[7]),
                        max_uses=row[8],
                    )
                )
            return templates

    def get_player_profile(self, user_id: str) -> Optional[PlayerModProfile]:
        """Get a player's mod profile"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM player_profiles WHERE user_id = ?", (user_id,)
            )
            row = cursor.fetchone()

            if row:
                return PlayerModProfile(
                    user_id=row[0],
                    username=row[1],
                    mod_slots=row[2],
                    active_mods=json.loads(row[3]) if row[3] else [],
                    owned_mods=json.loads(row[4]) if row[4] else [],
                    total_rp_earned=row[5],
                    total_rp_spent=row[6],
                    mod_purchases=row[7],
                )
        return None

    def create_player_profile(self, user_id: str, username: str) -> PlayerModProfile:
        """Create a new player profile"""
        profile = PlayerModProfile(user_id=user_id, username=username)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO player_profiles 
                (user_id, username, mod_slots, active_mods, owned_mods, total_rp_earned, total_rp_spent, mod_purchases)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    profile.user_id,
                    profile.username,
                    profile.mod_slots,
                    json.dumps(profile.active_mods),
                    json.dumps(profile.owned_mods),
                    profile.total_rp_earned,
                    profile.total_rp_spent,
                    profile.mod_purchases,
                ),
            )
            conn.commit()

        return profile

    def update_player_profile(self, profile: PlayerModProfile):
        """Update a player's profile in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE player_profiles 
                SET username = ?, mod_slots = ?, active_mods = ?, owned_mods = ?, 
                    total_rp_earned = ?, total_rp_spent = ?, mod_purchases = ?
                WHERE user_id = ?
            """,
                (
                    profile.username,
                    profile.mod_slots,
                    json.dumps(profile.active_mods),
                    json.dumps(profile.owned_mods),
                    profile.total_rp_earned,
                    profile.total_rp_spent,
                    profile.mod_purchases,
                    profile.user_id,
                ),
            )
            conn.commit()

    def purchase_mod(self, user_id: str, mod_id: str, rp_cost: int) -> bool:
        """Purchase a mod for a player"""
        profile = self.get_player_profile(user_id)
        if not profile:
            return False

        template = self.get_mod_template(mod_id)
        if not template:
            return False

        # Check if player can afford it
        if rp_cost < template.cost:
            return False

        # Check if player already owns it
        if mod_id in profile.owned_mods:
            return False

        # Purchase the mod
        profile.owned_mods.append(mod_id)
        profile.total_rp_spent += template.cost
        profile.mod_purchases += 1

        self.update_player_profile(profile)
        return True

    def activate_mod(self, user_id: str, mod_id: str) -> bool:
        """Activate a mod for a player"""
        profile = self.get_player_profile(user_id)
        if not profile:
            return False

        # Check if player owns the mod
        if mod_id not in profile.owned_mods:
            return False

        # Check if mod is already active
        if mod_id in profile.active_mods:
            return False

        # Check if player has available slots
        if len(profile.active_mods) >= profile.mod_slots:
            return False

        # Activate the mod
        profile.active_mods.append(mod_id)
        self.update_player_profile(profile)
        return True

    def deactivate_mod(self, user_id: str, mod_id: str) -> bool:
        """Deactivate a mod for a player"""
        profile = self.get_player_profile(user_id)
        if not profile:
            return False

        # Check if mod is active
        if mod_id not in profile.active_mods:
            return False

        # Deactivate the mod
        profile.active_mods.remove(mod_id)
        self.update_player_profile(profile)
        return True


class StandaloneGlobalRewardMultiplier:
    """Standalone global reward multiplier system"""

    def __init__(self, db_path: str = "data/simulation_global_multiplier.db"):
        self.db_path = db_path
        self.ensure_db_directory()
        self.init_database()

    def ensure_db_directory(self):
        """Ensure the database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def init_database(self):
        """Initialize the database table"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS global_multiplier (
                    id INTEGER PRIMARY KEY,
                    multiplier REAL DEFAULT 1.0,
                    drones_alive INTEGER DEFAULT 0,
                    active_players INTEGER DEFAULT 0,
                    drones_ever_died INTEGER DEFAULT 1,
                    last_updated REAL DEFAULT 0
                )
            """
            )

            # Insert default record if none exists
            cursor.execute("SELECT COUNT(*) FROM global_multiplier")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    """
                    INSERT INTO global_multiplier 
                    (multiplier, drones_alive, active_players, drones_ever_died, last_updated)
                    VALUES (1.0, 0, 0, 1, ?)
                """,
                    (time.time(),),
                )

            conn.commit()

    def calculate_multiplier(
        self, drones_alive: int, active_players: int, drones_ever_died: int
    ) -> float:
        """Calculate the global reward multiplier"""
        if drones_ever_died == 0:
            drones_ever_died = 1  # Prevent division by zero

        multiplier = (drones_alive * active_players) / drones_ever_died

        # Apply caps
        multiplier = max(0.1, min(3.0, multiplier))

        return round(multiplier, 2)

    def update_multiplier(
        self, drones_alive: int, active_players: int, drones_ever_died: int
    ):
        """Update the global multiplier"""
        multiplier = self.calculate_multiplier(
            drones_alive, active_players, drones_ever_died
        )

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE global_multiplier 
                SET multiplier = ?, drones_alive = ?, active_players = ?, 
                    drones_ever_died = ?, last_updated = ?
                WHERE id = 1
            """,
                (
                    multiplier,
                    drones_alive,
                    active_players,
                    drones_ever_died,
                    time.time(),
                ),
            )
            conn.commit()

    def get_current_multiplier(self) -> float:
        """Get the current global multiplier"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT multiplier FROM global_multiplier WHERE id = 1")
            result = cursor.fetchone()
            return result[0] if result else 1.0

    def get_multiplier_stats(self) -> Dict[str, Any]:
        """Get current multiplier statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM global_multiplier WHERE id = 1")
            row = cursor.fetchone()

            if row:
                return {
                    "multiplier": row[1],
                    "drones_alive": row[2],
                    "active_players": row[3],
                    "drones_ever_died": row[4],
                    "last_updated": row[5],
                }
        return {
            "multiplier": 1.0,
            "drones_alive": 0,
            "active_players": 0,
            "drones_ever_died": 1,
            "last_updated": time.time(),
        }

    def apply_multiplier_to_reward(self, base_reward: float) -> float:
        """Apply the global multiplier to a reward"""
        current_multiplier = self.get_current_multiplier()
        return base_reward * current_multiplier
