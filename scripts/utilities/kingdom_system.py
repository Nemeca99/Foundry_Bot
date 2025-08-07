#!/usr/bin/env python3
"""
7 Kingdoms System with Council of 7
EVE Online-style faction system with Discord integration
"""

import sqlite3
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ElementType(Enum):
    """Element types for kingdoms"""

    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"
    LIGHTNING = "lightning"
    ICE = "ice"
    UNIFIED = "unified"  # Lyra's Dominion


class KingdomType(Enum):
    """Kingdom types with Council fragments"""

    LYRA_DOMINION = (
        "Lyra's Dominion",
        ElementType.UNIFIED,
        "lyra",
        "Unified Voice",
        "Gold/Purple",
    )
    FIRE_KINGDOM = (
        "Velastra's Passion Realm",
        ElementType.FIRE,
        "velastra",
        "Desire/Passion",
        "Red/Pink",
    )
    WATER_KINGDOM = (
        "Seraphis's Flow Realm",
        ElementType.WATER,
        "seraphis",
        "Adaptation/Fluidity",
        "Blue/Cyan",
    )
    EARTH_KINGDOM = (
        "Obelisk's Foundation Realm",
        ElementType.EARTH,
        "obelisk",
        "Stability/Growth",
        "Green/Brown",
    )
    AIR_KINGDOM = (
        "Echoe's Freedom Realm",
        ElementType.AIR,
        "echoe",
        "Liberty/Movement",
        "White/Silver",
    )
    LIGHTNING_KINGDOM = (
        "Blackwall's Power Realm",
        ElementType.LIGHTNING,
        "blackwall",
        "Energy/Force",
        "Yellow/Orange",
    )
    ICE_KINGDOM = (
        "Nyx's Mystery Realm",
        ElementType.ICE,
        "nyx",
        "Wisdom/Secrets",
        "Cyan/White",
    )


class SubscriptionTier(Enum):
    """Discord subscription tiers"""

    TIER_1 = ("Tier 1", 1, "Basic benefits")
    TIER_2 = ("Tier 2", 2, "Moderator rights")
    TIER_3 = ("Tier 3", 3, "Council eligibility")


@dataclass
class KingdomRuler:
    """Kingdom ruler data"""

    user_id: str
    username: str
    kingdom_type: KingdomType
    subscription_tier: SubscriptionTier
    appointed_at: datetime
    kingdom_power: int = 1000
    territory_control: int = 100


@dataclass
class KingdomCitizen:
    """Kingdom citizen data"""

    user_id: str
    username: str
    kingdom_type: KingdomType
    subscription_tier: SubscriptionTier
    joined_at: datetime
    contribution_points: int = 0


@dataclass
class CouncilProposal:
    """Council proposal data"""

    proposal_id: str
    proposer_id: str
    kingdom_type: KingdomType
    title: str
    description: str
    proposal_type: str  # war, alliance, policy, etc.
    created_at: datetime
    expires_at: datetime
    votes_for: int = 0
    votes_against: int = 0
    status: str = "active"  # active, passed, failed, expired


class KingdomSystem:
    """7 Kingdoms System with EVE Online-style mechanics"""

    def __init__(self, db_path: str = "data/kingdoms.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize kingdom database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Kingdom rulers table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS kingdom_rulers (
                    user_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    kingdom_type TEXT NOT NULL,
                    subscription_tier INTEGER NOT NULL,
                    appointed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    kingdom_power INTEGER DEFAULT 1000,
                    territory_control INTEGER DEFAULT 100
                )
            """
            )

            # Kingdom citizens table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS kingdom_citizens (
                    user_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    kingdom_type TEXT NOT NULL,
                    subscription_tier INTEGER NOT NULL,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    contribution_points INTEGER DEFAULT 0
                )
            """
            )

            # Council proposals table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS council_proposals (
                    proposal_id TEXT PRIMARY KEY,
                    proposer_id TEXT NOT NULL,
                    kingdom_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    proposal_type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    votes_for INTEGER DEFAULT 0,
                    votes_against INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'active'
                )
            """
            )

            # Kingdom wars table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS kingdom_wars (
                    war_id TEXT PRIMARY KEY,
                    attacker_kingdom TEXT NOT NULL,
                    defender_kingdom TEXT NOT NULL,
                    declared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    attacker_power INTEGER DEFAULT 0,
                    defender_power INTEGER DEFAULT 0
                )
            """
            )

            # Kingdom alliances table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS kingdom_alliances (
                    alliance_id TEXT PRIMARY KEY,
                    kingdom_1 TEXT NOT NULL,
                    kingdom_2 TEXT NOT NULL,
                    formed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            """
            )

    def get_kingdom_info(self, kingdom_type: KingdomType) -> Dict:
        """Get information about a kingdom"""
        kingdom_name, element, council_member, theme, colors = kingdom_type.value

        return {
            "name": kingdom_name,
            "element": element.value,
            "council_member": council_member,
            "theme": theme,
            "colors": colors,
            "kingdom_type": kingdom_type.name,
        }

    def get_all_kingdoms(self) -> List[Dict]:
        """Get all kingdoms"""
        return [self.get_kingdom_info(kingdom) for kingdom in KingdomType]

    def claim_throne(
        self,
        user_id: str,
        username: str,
        kingdom_type: KingdomType,
        subscription_tier: SubscriptionTier,
    ) -> Dict:
        """Claim throne of a kingdom"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if throne is already claimed
                cursor.execute(
                    "SELECT user_id FROM kingdom_rulers WHERE kingdom_type = ?",
                    (kingdom_type.name,),
                )
                existing_ruler = cursor.fetchone()

                if existing_ruler:
                    return {
                        "success": False,
                        "error": f"Throne already claimed by {existing_ruler[0]}",
                    }

                # Check subscription tier requirements
                if subscription_tier.value[1] < 3:
                    return {
                        "success": False,
                        "error": "Tier 3 subscription required to claim throne",
                    }

                # Claim the throne
                cursor.execute(
                    """
                    INSERT INTO kingdom_rulers 
                    (user_id, username, kingdom_type, subscription_tier, appointed_at)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        username,
                        kingdom_type.name,
                        subscription_tier.value[1],
                        datetime.now(),
                    ),
                )

                # Add as citizen
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO kingdom_citizens 
                    (user_id, username, kingdom_type, subscription_tier, joined_at)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        username,
                        kingdom_type.name,
                        subscription_tier.value[1],
                        datetime.now(),
                    ),
                )

                return {
                    "success": True,
                    "message": f"You have claimed the throne of {kingdom_type.value[0]}!",
                    "kingdom": self.get_kingdom_info(kingdom_type),
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to claim throne: {str(e)}"}

    def join_kingdom(
        self,
        user_id: str,
        username: str,
        kingdom_type: KingdomType,
        subscription_tier: SubscriptionTier,
    ) -> Dict:
        """Join a kingdom as a citizen"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if already a citizen
                cursor.execute(
                    "SELECT kingdom_type FROM kingdom_citizens WHERE user_id = ?",
                    (user_id,),
                )
                existing_citizenship = cursor.fetchone()

                if existing_citizenship:
                    return {
                        "success": False,
                        "error": f"You are already a citizen of {existing_citizenship[0]}",
                    }

                # Join kingdom
                cursor.execute(
                    """
                    INSERT INTO kingdom_citizens 
                    (user_id, username, kingdom_type, subscription_tier, joined_at)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        username,
                        kingdom_type.name,
                        subscription_tier.value[1],
                        datetime.now(),
                    ),
                )

                return {
                    "success": True,
                    "message": f"You have joined {kingdom_type.value[0]}!",
                    "kingdom": self.get_kingdom_info(kingdom_type),
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to join kingdom: {str(e)}"}

    def declare_war(
        self,
        attacker_user_id: str,
        attacker_kingdom: KingdomType,
        defender_kingdom: KingdomType,
    ) -> Dict:
        """Declare war on another kingdom"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if attacker is ruler
                cursor.execute(
                    "SELECT user_id FROM kingdom_rulers WHERE user_id = ? AND kingdom_type = ?",
                    (attacker_user_id, attacker_kingdom.name),
                )
                if not cursor.fetchone():
                    return {
                        "success": False,
                        "error": "Only kingdom rulers can declare war",
                    }

                # Check if already at war
                cursor.execute(
                    """
                    SELECT war_id FROM kingdom_wars 
                    WHERE (attacker_kingdom = ? AND defender_kingdom = ?) 
                    OR (attacker_kingdom = ? AND defender_kingdom = ?)
                    AND status = 'active'
                """,
                    (
                        attacker_kingdom.name,
                        defender_kingdom.name,
                        defender_kingdom.name,
                        attacker_kingdom.name,
                    ),
                )

                if cursor.fetchone():
                    return {
                        "success": False,
                        "error": "Already at war with this kingdom",
                    }

                # Get kingdom powers
                attacker_power = self._get_kingdom_power(attacker_kingdom)
                defender_power = self._get_kingdom_power(defender_kingdom)

                # Declare war
                war_id = f"war_{attacker_kingdom.name}_{defender_kingdom.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                cursor.execute(
                    """
                    INSERT INTO kingdom_wars 
                    (war_id, attacker_kingdom, defender_kingdom, attacker_power, defender_power)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        war_id,
                        attacker_kingdom.name,
                        defender_kingdom.name,
                        attacker_power,
                        defender_power,
                    ),
                )

                return {
                    "success": True,
                    "message": f"{attacker_kingdom.value[0]} has declared war on {defender_kingdom.value[0]}!",
                    "war_id": war_id,
                    "attacker_power": attacker_power,
                    "defender_power": defender_power,
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to declare war: {str(e)}"}

    def create_council_proposal(
        self,
        user_id: str,
        kingdom_type: KingdomType,
        title: str,
        description: str,
        proposal_type: str,
    ) -> Dict:
        """Create a council proposal"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if user is ruler
                cursor.execute(
                    "SELECT user_id FROM kingdom_rulers WHERE user_id = ? AND kingdom_type = ?",
                    (user_id, kingdom_type.name),
                )
                if not cursor.fetchone():
                    return {
                        "success": False,
                        "error": "Only kingdom rulers can create council proposals",
                    }

                # Create proposal
                proposal_id = f"proposal_{kingdom_type.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                expires_at = datetime.now() + timedelta(days=7)  # 7 days to vote

                cursor.execute(
                    """
                    INSERT INTO council_proposals 
                    (proposal_id, proposer_id, kingdom_type, title, description, proposal_type, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        proposal_id,
                        user_id,
                        kingdom_type.name,
                        title,
                        description,
                        proposal_type,
                        expires_at,
                    ),
                )

                return {
                    "success": True,
                    "message": f"Council proposal '{title}' created!",
                    "proposal_id": proposal_id,
                    "expires_at": expires_at,
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to create proposal: {str(e)}"}

    def vote_on_proposal(self, user_id: str, proposal_id: str, vote: str) -> Dict:
        """Vote on a council proposal"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if proposal exists and is active
                cursor.execute(
                    "SELECT kingdom_type, status, expires_at FROM council_proposals WHERE proposal_id = ?",
                    (proposal_id,),
                )
                proposal = cursor.fetchone()

                if not proposal:
                    return {"success": False, "error": "Proposal not found"}

                if proposal[1] != "active":
                    return {"success": False, "error": "Proposal is no longer active"}

                if datetime.now() > datetime.fromisoformat(proposal[2]):
                    return {"success": False, "error": "Voting period has expired"}

                # Check if user is ruler of the kingdom
                cursor.execute(
                    "SELECT user_id FROM kingdom_rulers WHERE user_id = ? AND kingdom_type = ?",
                    (user_id, proposal[0]),
                )
                if not cursor.fetchone():
                    return {
                        "success": False,
                        "error": "Only kingdom rulers can vote on proposals",
                    }

                # Update vote count
                if vote.lower() == "for":
                    cursor.execute(
                        "UPDATE council_proposals SET votes_for = votes_for + 1 WHERE proposal_id = ?",
                        (proposal_id,),
                    )
                elif vote.lower() == "against":
                    cursor.execute(
                        "UPDATE council_proposals SET votes_against = votes_against + 1 WHERE proposal_id = ?",
                        (proposal_id,),
                    )
                else:
                    return {
                        "success": False,
                        "error": "Invalid vote. Use 'for' or 'against'",
                    }

                return {"success": True, "message": f"Vote recorded: {vote}"}

        except Exception as e:
            return {"success": False, "error": f"Failed to vote: {str(e)}"}

    def get_active_proposals(self) -> List[Dict]:
        """Get all active council proposals"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT proposal_id, kingdom_type, title, description, proposal_type, 
                           created_at, expires_at, votes_for, votes_against
                    FROM council_proposals 
                    WHERE status = 'active' AND expires_at > ?
                    ORDER BY created_at DESC
                """,
                    (datetime.now(),),
                )

                proposals = []
                for row in cursor.fetchall():
                    proposals.append(
                        {
                            "proposal_id": row[0],
                            "kingdom_type": row[1],
                            "title": row[2],
                            "description": row[3],
                            "proposal_type": row[4],
                            "created_at": row[5],
                            "expires_at": row[6],
                            "votes_for": row[7],
                            "votes_against": row[8],
                        }
                    )

                return proposals

        except Exception as e:
            return []

    def get_kingdom_rulers(self) -> List[Dict]:
        """Get all kingdom rulers"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT user_id, username, kingdom_type, subscription_tier, 
                           appointed_at, kingdom_power, territory_control
                    FROM kingdom_rulers
                    ORDER BY kingdom_type
                """
                )

                rulers = []
                for row in cursor.fetchall():
                    rulers.append(
                        {
                            "user_id": row[0],
                            "username": row[1],
                            "kingdom_type": row[2],
                            "subscription_tier": row[3],
                            "appointed_at": row[4],
                            "kingdom_power": row[5],
                            "territory_control": row[6],
                        }
                    )

                return rulers

        except Exception as e:
            return []

    def get_kingdom_citizens(self, kingdom_type: KingdomType) -> List[Dict]:
        """Get citizens of a specific kingdom"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT user_id, username, subscription_tier, joined_at, contribution_points
                    FROM kingdom_citizens
                    WHERE kingdom_type = ?
                    ORDER BY contribution_points DESC
                """,
                    (kingdom_type.name,),
                )

                citizens = []
                for row in cursor.fetchall():
                    citizens.append(
                        {
                            "user_id": row[0],
                            "username": row[1],
                            "subscription_tier": row[2],
                            "joined_at": row[3],
                            "contribution_points": row[4],
                        }
                    )

                return citizens

        except Exception as e:
            return []

    def _get_kingdom_power(self, kingdom_type: KingdomType) -> int:
        """Calculate kingdom power based on citizens and ruler"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Count citizens
                cursor.execute(
                    "SELECT COUNT(*) FROM kingdom_citizens WHERE kingdom_type = ?",
                    (kingdom_type.name,),
                )
                citizen_count = cursor.fetchone()[0]

                # Get ruler power
                cursor.execute(
                    "SELECT kingdom_power FROM kingdom_rulers WHERE kingdom_type = ?",
                    (kingdom_type.name,),
                )
                ruler_power = cursor.fetchone()
                ruler_power = ruler_power[0] if ruler_power else 1000

                # Calculate total power
                total_power = ruler_power + (citizen_count * 100)

                return total_power

        except Exception as e:
            return 1000

    def get_elemental_benefits(self, element_type: ElementType) -> Dict:
        """Get benefits for each element type"""
        benefits = {
            ElementType.FIRE: {
                "combat_bonus": 1.2,
                "production_bonus": 1.1,
                "description": "Enhanced combat and production capabilities",
            },
            ElementType.WATER: {
                "survival_bonus": 1.3,
                "adaptation_bonus": 1.2,
                "description": "Improved survival and adaptation",
            },
            ElementType.EARTH: {
                "defense_bonus": 1.4,
                "growth_bonus": 1.2,
                "description": "Superior defense and growth",
            },
            ElementType.AIR: {
                "speed_bonus": 1.3,
                "mobility_bonus": 1.2,
                "description": "Enhanced speed and mobility",
            },
            ElementType.LIGHTNING: {
                "energy_bonus": 1.4,
                "power_bonus": 1.3,
                "description": "Increased energy and power",
            },
            ElementType.ICE: {
                "control_bonus": 1.3,
                "wisdom_bonus": 1.2,
                "description": "Enhanced control and wisdom",
            },
            ElementType.UNIFIED: {
                "all_bonus": 1.1,
                "balance_bonus": 1.2,
                "description": "Balanced bonuses across all areas",
            },
        }

        return benefits.get(element_type, {})

    def get_subscription_benefits(self, tier: SubscriptionTier) -> Dict:
        """Get benefits for a subscription tier"""
        benefits = {
            SubscriptionTier.TIER_1: {
                "name": "Tier 1",
                "description": "Basic kingdom benefits",
                "permissions": ["join_kingdom", "basic_chat"],
                "rp_bonus": 0.1,
                "color": "Green",
            },
            SubscriptionTier.TIER_2: {
                "name": "Tier 2", 
                "description": "Moderator rights and enhanced benefits",
                "permissions": ["join_kingdom", "moderate_chat", "manage_roles"],
                "rp_bonus": 0.25,
                "color": "Blue",
            },
            SubscriptionTier.TIER_3: {
                "name": "Tier 3",
                "description": "Council eligibility and maximum benefits", 
                "permissions": ["join_kingdom", "moderate_chat", "manage_roles", "council_vote"],
                "rp_bonus": 0.5,
                "color": "Purple",
            },
        }
        return benefits.get(tier, {})

    def get_status(self) -> str:
        """Get the status of the kingdom system"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count rulers
                cursor.execute("SELECT COUNT(*) FROM kingdom_rulers")
                ruler_count = cursor.fetchone()[0]
                
                # Count citizens
                cursor.execute("SELECT COUNT(*) FROM kingdom_citizens")
                citizen_count = cursor.fetchone()[0]
                
                # Count active proposals
                cursor.execute("SELECT COUNT(*) FROM council_proposals WHERE status = 'active'")
                proposal_count = cursor.fetchone()[0]
                
                # Count kingdoms with rulers
                cursor.execute("SELECT COUNT(DISTINCT kingdom_type) FROM kingdom_rulers")
                active_kingdoms = cursor.fetchone()[0]
            
            return f"Rulers: {ruler_count}, Citizens: {citizen_count}, Proposals: {proposal_count}, Active Kingdoms: {active_kingdoms}"
            
        except Exception as e:
            return f"Error: {str(e)}"
