#!/usr/bin/env python3
"""
Sim-Rancher Live Mod System
Player-driven game customization with RP-based progression
"""

import json
import sqlite3
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid


@dataclass
class ModTemplate:
    """Template for player-created mods"""

    mod_id: str
    creator_id: str
    name: str
    description: str
    category: str  # "economy", "personality", "body_parts", "behavior"
    cost_rp: int
    daily_upkeep: int
    effects: Dict[str, Any]
    requirements: Dict[str, Any]
    version: str = "1.0.0"
    approved: bool = False
    created_at: str = ""
    downloads: int = 0
    rating: float = 0.0


@dataclass
class PlayerModProfile:
    """Player's mod configuration"""

    user_id: str
    mod_slots: int = 10  # Base: 5 active, 5 stasis
    active_mods: List[str] = None  # List of active mod IDs
    stasis_mods: List[str] = None  # List of stasis mod IDs
    total_rp_spent: int = 0
    mod_subscription_cost: int = 0
    rp_modifiers: Dict[str, float] = None
    last_daily_claim: str = ""
    daily_claimed: bool = False


class ModSystem:
    """Core modding system for Sim-Rancher"""

    def __init__(self, db_path: str = "data/mods.db"):
        self.db_path = db_path
        self.mod_templates: Dict[str, ModTemplate] = {}
        self.player_profiles: Dict[str, PlayerModProfile] = {}
        self.global_multiplier = 1.0
        self.drones_alive = 0
        self.drones_ever_died = 1  # Prevent division by zero
        self.active_players = 0
        self.last_multiplier_update = time.time()

        self._init_database()
        self._load_mod_templates()
        self._load_player_profiles()

    def _init_database(self):
        """Initialize the mod database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS mod_templates (
                    mod_id TEXT PRIMARY KEY,
                    creator_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    cost_rp INTEGER NOT NULL,
                    daily_upkeep INTEGER NOT NULL,
                    effects TEXT NOT NULL,
                    requirements TEXT NOT NULL,
                    version TEXT DEFAULT '1.0.0',
                    approved BOOLEAN DEFAULT FALSE,
                    created_at TEXT NOT NULL,
                    downloads INTEGER DEFAULT 0,
                    rating REAL DEFAULT 0.0
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS player_mod_profiles (
                    user_id TEXT PRIMARY KEY,
                    mod_slots INTEGER DEFAULT 10,
                    active_mods TEXT DEFAULT '[]',
                    stasis_mods TEXT DEFAULT '[]',
                    total_rp_spent INTEGER DEFAULT 0,
                    mod_subscription_cost INTEGER DEFAULT 0,
                    rp_modifiers TEXT DEFAULT '{}',
                    last_daily_claim TEXT DEFAULT '',
                    daily_claimed BOOLEAN DEFAULT FALSE
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS global_stats (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """
            )

    def _load_mod_templates(self):
        """Load mod templates from database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM mod_templates")
            for row in cursor.fetchall():
                mod = ModTemplate(
                    mod_id=row[0],
                    creator_id=row[1],
                    name=row[2],
                    description=row[3],
                    category=row[4],
                    cost_rp=row[5],
                    daily_upkeep=row[6],
                    effects=json.loads(row[7]),
                    requirements=json.loads(row[8]),
                    version=row[9],
                    approved=bool(row[10]),
                    created_at=row[11],
                    downloads=row[12],
                    rating=row[13],
                )
                self.mod_templates[mod.mod_id] = mod

    def _load_player_profiles(self):
        """Load player mod profiles from database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM player_mod_profiles")
            for row in cursor.fetchall():
                profile = PlayerModProfile(
                    user_id=row[0],
                    mod_slots=row[1],
                    active_mods=json.loads(row[2]),
                    stasis_mods=json.loads(row[3]),
                    total_rp_spent=row[4],
                    mod_subscription_cost=row[5],
                    rp_modifiers=json.loads(row[6]),
                    last_daily_claim=row[7],
                    daily_claimed=bool(row[8]),
                )
                self.player_profiles[profile.user_id] = profile

    def create_mod_template(
        self,
        creator_id: str,
        name: str,
        description: str,
        category: str,
        cost_rp: int,
        daily_upkeep: int,
        effects: Dict[str, Any],
        requirements: Dict[str, Any],
    ) -> str:
        """Create a new mod template"""
        mod_id = str(uuid.uuid4())

        mod = ModTemplate(
            mod_id=mod_id,
            creator_id=creator_id,
            name=name,
            description=description,
            category=category,
            cost_rp=cost_rp,
            daily_upkeep=daily_upkeep,
            effects=effects,
            requirements=requirements,
            created_at=datetime.now().isoformat(),
        )

        # Save to database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO mod_templates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    mod.mod_id,
                    mod.creator_id,
                    mod.name,
                    mod.description,
                    mod.category,
                    mod.cost_rp,
                    mod.daily_upkeep,
                    json.dumps(mod.effects),
                    json.dumps(mod.requirements),
                    mod.version,
                    mod.approved,
                    mod.created_at,
                    mod.downloads,
                    mod.rating,
                ),
            )

        self.mod_templates[mod_id] = mod
        return mod_id

    def get_or_create_player_profile(self, user_id: str) -> PlayerModProfile:
        """Get or create a player's mod profile"""
        if user_id not in self.player_profiles:
            profile = PlayerModProfile(
                user_id=user_id, active_mods=[], stasis_mods=[], rp_modifiers={}
            )

            # Save to database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO player_mod_profiles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        profile.user_id,
                        profile.mod_slots,
                        json.dumps(profile.active_mods),
                        json.dumps(profile.stasis_mods),
                        profile.total_rp_spent,
                        profile.mod_subscription_cost,
                        json.dumps(profile.rp_modifiers),
                        profile.last_daily_claim,
                        profile.daily_claimed,
                    ),
                )

            self.player_profiles[user_id] = profile

        return self.player_profiles[user_id]

    def purchase_mod_slot(self, user_id: str, cost_rp: int) -> bool:
        """Purchase additional mod slots with RP"""
        profile = self.get_or_create_player_profile(user_id)

        # Check if player has enough RP (this would come from economy system)
        # For now, assume they have enough

        profile.mod_slots += 1
        profile.total_rp_spent += cost_rp

        # Update database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE player_mod_profiles 
                SET mod_slots = ?, total_rp_spent = ?
                WHERE user_id = ?
            """,
                (profile.mod_slots, profile.total_rp_spent, user_id),
            )

        return True

    def activate_mod(self, user_id: str, mod_id: str) -> bool:
        """Activate a mod for a player"""
        profile = self.get_or_create_player_profile(user_id)

        if mod_id not in self.mod_templates:
            return False

        mod = self.mod_templates[mod_id]

        # Check if player has space for active mods
        if len(profile.active_mods) >= profile.mod_slots // 2:  # Half slots for active
            return False

        # Check if mod is approved
        if not mod.approved:
            return False

        # Add to active mods
        if mod_id not in profile.active_mods:
            profile.active_mods.append(mod_id)
            profile.mod_subscription_cost += mod.daily_upkeep

            # Apply mod effects
            self._apply_mod_effects(profile, mod)

            # Update database
            self._save_player_profile(profile)

        return True

    def deactivate_mod(self, user_id: str, mod_id: str) -> bool:
        """Deactivate a mod for a player"""
        profile = self.get_or_create_player_profile(user_id)

        if mod_id in profile.active_mods:
            profile.active_mods.remove(mod_id)

            # Remove mod effects
            mod = self.mod_templates.get(mod_id)
            if mod:
                profile.mod_subscription_cost -= mod.daily_upkeep
                self._remove_mod_effects(profile, mod)

            # Update database
            self._save_player_profile(profile)
            return True

        return False

    def _apply_mod_effects(self, profile: PlayerModProfile, mod: ModTemplate):
        """Apply mod effects to player profile"""
        effects = mod.effects

        # Apply RP modifiers
        if "rp_modifiers" in effects:
            for key, value in effects["rp_modifiers"].items():
                profile.rp_modifiers[key] = profile.rp_modifiers.get(key, 1.0) * value

        # Apply other effects as needed
        # This would integrate with other game systems

    def _remove_mod_effects(self, profile: PlayerModProfile, mod: ModTemplate):
        """Remove mod effects from player profile"""
        effects = mod.effects

        # Remove RP modifiers
        if "rp_modifiers" in effects:
            for key, value in effects["rp_modifiers"].items():
                if key in profile.rp_modifiers:
                    profile.rp_modifiers[key] /= value

    def _save_player_profile(self, profile: PlayerModProfile):
        """Save player profile to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE player_mod_profiles 
                SET mod_slots = ?, active_mods = ?, stasis_mods = ?, 
                    total_rp_spent = ?, mod_subscription_cost = ?, 
                    rp_modifiers = ?, last_daily_claim = ?, daily_claimed = ?
                WHERE user_id = ?
            """,
                (
                    profile.mod_slots,
                    json.dumps(profile.active_mods),
                    json.dumps(profile.stasis_mods),
                    profile.total_rp_spent,
                    profile.mod_subscription_cost,
                    json.dumps(profile.rp_modifiers),
                    profile.last_daily_claim,
                    profile.daily_claimed,
                    profile.user_id,
                ),
            )

    def get_available_mods(self, category: str = None) -> List[ModTemplate]:
        """Get list of available mods"""
        mods = [mod for mod in self.mod_templates.values() if mod.approved]

        if category:
            mods = [mod for mod in mods if mod.category == category]

        return mods

    def get_player_mods(self, user_id: str) -> Dict[str, Any]:
        """Get player's mod information"""
        profile = self.get_or_create_player_profile(user_id)

        active_mods = [
            self.mod_templates[mod_id]
            for mod_id in profile.active_mods
            if mod_id in self.mod_templates
        ]

        return {
            "profile": asdict(profile),
            "active_mods": [asdict(mod) for mod in active_mods],
            "available_slots": profile.mod_slots // 2 - len(profile.active_mods),
        }


class GlobalRewardMultiplier:
    """Global Reward Multiplier System (SGRM)"""

    def __init__(self, mod_system: ModSystem):
        self.mod_system = mod_system
        self.multiplier = 1.0
        self.last_broadcast = time.time()
        self.broadcast_interval = 300  # 5 minutes

    def update_multiplier(
        self, drones_alive: int, active_players: int, drones_ever_died: int
    ):
        """Update the global reward multiplier"""
        if drones_ever_died == 0:
            drones_ever_died = 1  # Prevent division by zero

        # Calculate new multiplier
        new_multiplier = (drones_alive * active_players) / drones_ever_died

        # Apply caps
        self.multiplier = max(0.1, min(3.0, new_multiplier))

        # Update stats
        self.mod_system.drones_alive = drones_alive
        self.mod_system.active_players = active_players
        self.mod_system.drones_ever_died = drones_ever_died
        self.mod_system.global_multiplier = self.multiplier

        # Save to database
        with sqlite3.connect(self.mod_system.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO global_stats (key, value, updated_at) 
                VALUES (?, ?, ?)
            """,
                ("global_multiplier", str(self.multiplier), datetime.now().isoformat()),
            )

    def get_multiplier_message(self) -> str:
        """Get a random broadcast message for the multiplier"""
        messages = [
            (
                f"🌍 Current Reward Multiplier: {self.multiplier:.1f}x – world economy in decline!"
                if self.multiplier < 1.0
                else (
                    f"🌍 Current Reward Multiplier: {self.multiplier:.1f}x – economy stable!"
                    if self.multiplier < 1.5
                    else (
                        f"🌍 Current Reward Multiplier: {self.multiplier:.1f}x – thriving economy!"
                        if self.multiplier < 2.0
                        else f"🌍 Current Reward Multiplier: {self.multiplier:.1f}x – BOOMING economy! 🚀"
                    )
                )
            )
        ]

        return random.choice(messages)

    def should_broadcast(self) -> bool:
        """Check if it's time to broadcast the multiplier"""
        return time.time() - self.last_broadcast > self.broadcast_interval

    def apply_multiplier_to_reward(self, base_reward: float) -> float:
        """Apply the global multiplier to a reward"""
        return base_reward * self.multiplier


class ModTemplateGenerator:
    """Generate mod templates for players"""

    @staticmethod
    def create_economy_mod(
        creator_id: str,
        name: str,
        rp_gain_boost: float,
        cost_rp: int,
        daily_upkeep: int,
    ) -> ModTemplate:
        """Create an economy mod template"""
        effects = {"rp_modifiers": {"base_gain": rp_gain_boost}}

        requirements = {"min_level": 1, "rp_cost": cost_rp}

        return ModTemplate(
            mod_id=str(uuid.uuid4()),
            creator_id=creator_id,
            name=name,
            description=f"Increases RP gain by {(rp_gain_boost - 1) * 100:.1f}%",
            category="economy",
            cost_rp=cost_rp,
            daily_upkeep=daily_upkeep,
            effects=effects,
            requirements=requirements,
        )

    @staticmethod
    def create_personality_mod(
        creator_id: str,
        name: str,
        personality_traits: List[str],
        cost_rp: int,
        daily_upkeep: int,
    ) -> ModTemplate:
        """Create a personality mod template"""
        effects = {
            "personality_traits": personality_traits,
            "behavior_modifiers": {"chat_style": "enhanced", "social_bonus": 1.2},
        }

        requirements = {"min_level": 5, "rp_cost": cost_rp}

        return ModTemplate(
            mod_id=str(uuid.uuid4()),
            creator_id=creator_id,
            name=name,
            description=f"Adds personality traits: {', '.join(personality_traits)}",
            category="personality",
            cost_rp=cost_rp,
            daily_upkeep=daily_upkeep,
            effects=effects,
            requirements=requirements,
        )


# Export main classes
__all__ = [
    "ModSystem",
    "GlobalRewardMultiplier",
    "ModTemplateGenerator",
    "ModTemplate",
    "PlayerModProfile",
]
