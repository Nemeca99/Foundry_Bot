#!/usr/bin/env python3
"""
C.L.D.S. (Customizable Life-like Drones System)
Modular body parts with rarity tiers and stat mapping
"""

import random
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class RarityTier(Enum):
    COMMON = ("Common", "White", 1.0)
    UNCOMMON = ("Uncommon", "Green", 2.0)
    RARE = ("Rare", "Blue", 3.0)
    EPIC = ("Epic", "Purple", 5.0)
    LEGENDARY = ("Legendary", "Orange", 6.0)
    MYTHIC = ("Mythic", "Red", 8.0)

    @property
    def display_name(self):
        return self.value[0]

    @property
    def color(self):
        return self.value[1]

    @property
    def multiplier(self):
        return self.value[2]


@dataclass
class BodyPart:
    name: str
    rarity: RarityTier
    hp: int
    max_hp: int
    stats: Dict[str, int]
    special_effects: List[str]

    def is_critical(self) -> bool:
        """Check if this is a critical body part (head, heart, torso)"""
        return self.name.lower() in ["head", "heart", "torso"]

    def take_damage(self, damage: int) -> bool:
        """Take damage and return True if destroyed"""
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0


class CLDSSystem:
    """Customizable Life-like Drones System"""

    def __init__(self):
        self.body_parts = {
            "head": {"stats": ["INT", "CHA"], "base_hp": 20},
            "torso": {"stats": ["STR", "CON", "WIS"], "base_hp": 30},
            "arms": {"stats": ["STR", "DEX"], "base_hp": 15},
            "legs": {"stats": ["DEX"], "base_hp": 15},
            "heart": {"stats": ["CON", "WIS"], "base_hp": 25},
        }

        self.special_effects = {
            RarityTier.EPIC: [
                "enhanced_processing",
                "regeneration",
                "adaptive_defense",
            ],
            RarityTier.LEGENDARY: [
                "quantum_stability",
                "soul_resonance",
                "evolutionary_boost",
            ],
            RarityTier.MYTHIC: [
                "reality_bending",
                "consciousness_transcendence",
                "immortality_seed",
            ],
        }

    def generate_body_part(self, part_name: str) -> BodyPart:
        """Generate a random body part with rarity and stats"""
        if part_name not in self.body_parts:
            raise ValueError(f"Unknown body part: {part_name}")

        # Generate rarity (weighted towards lower tiers)
        rarity_weights = {
            RarityTier.COMMON: 50,
            RarityTier.UNCOMMON: 25,
            RarityTier.RARE: 15,
            RarityTier.EPIC: 7,
            RarityTier.LEGENDARY: 2,
            RarityTier.MYTHIC: 1,
        }

        rarity = random.choices(
            list(rarity_weights.keys()), weights=list(rarity_weights.values())
        )[0]

        # Generate stats
        part_config = self.body_parts[part_name]
        base_hp = part_config["base_hp"]
        stat_names = part_config["stats"]

        # Generate random stats (1-10 for common, higher for rarer)
        stats = {}
        for stat in stat_names:
            base_value = random.randint(1, 10)
            rarity_bonus = int((rarity.multiplier - 1) * 5)
            stats[stat] = base_value + rarity_bonus

        # Calculate HP with rarity multiplier
        max_hp = int(base_hp * rarity.multiplier)
        hp = max_hp

        # Add special effects for Epic+ parts
        special_effects = []
        if rarity in self.special_effects:
            num_effects = random.randint(1, min(2, len(self.special_effects[rarity])))
            special_effects = random.sample(self.special_effects[rarity], num_effects)

        return BodyPart(
            name=part_name,
            rarity=rarity,
            hp=hp,
            max_hp=max_hp,
            stats=stats,
            special_effects=special_effects,
        )

    def generate_drone(self, name: str) -> Dict:
        """Generate a complete DigiDrone with all body parts"""
        drone = {
            "id": f"drone_{random.randint(10000, 99999)}",
            "name": name,
            "body_parts": {},
            "total_stats": {},
            "hp": 0,
            "max_hp": 0,
            "sshp": 100,  # Soul HP starts at 100
            "max_sshp": 100,
            "created_at": None,
            "last_fed": None,
            "evolution_stage": 1,
        }

        # Generate all body parts
        for part_name in self.body_parts.keys():
            part = self.generate_body_part(part_name)
            drone["body_parts"][part_name] = {
                "name": part.name,
                "rarity": part.rarity.display_name,
                "color": part.rarity.color,
                "hp": part.hp,
                "max_hp": part.max_hp,
                "stats": part.stats,
                "special_effects": part.special_effects,
                "destroyed": False,
            }
            drone["hp"] += part.hp
            drone["max_hp"] += part.max_hp

        # Calculate total stats
        total_stats = {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
        for part_data in drone["body_parts"].values():
            for stat, value in part_data["stats"].items():
                total_stats[stat] += value

        drone["total_stats"] = total_stats

        return drone

    def calculate_drone_value(self, drone: Dict) -> int:
        """Calculate the RP value of a drone based on its parts"""
        total_value = 0
        for part_data in drone["body_parts"].values():
            # Find the rarity enum by display name
            rarity = None
            for rarity_enum in RarityTier:
                if rarity_enum.display_name == part_data["rarity"]:
                    rarity = rarity_enum
                    break
            if rarity:
                base_value = 10  # Base value per part
                total_value += int(base_value * rarity.multiplier)
        return total_value

    def apply_damage(self, drone: Dict, damage_type: str, damage_amount: int) -> Dict:
        """Apply damage to drone and return damage report"""
        damage_report = {
            "damage_type": damage_type,
            "total_damage": 0,
            "destroyed_parts": [],
            "drone_destroyed": False,
        }

        # Apply SSHP damage first
        if damage_type in [
            "fire",
            "water",
            "earthquake",
            "meteor",
            "starvation",
            "disease",
        ]:
            drone["sshp"] = max(0, drone["sshp"] - damage_amount)
            damage_report["total_damage"] += damage_amount

            # Check if drone is destroyed by SSHP loss
            if drone["sshp"] <= 0:
                damage_report["drone_destroyed"] = True
                return damage_report

        # Apply HP damage to specific parts based on damage type
        target_parts = self._get_damage_targets(damage_type)

        for part_name in target_parts:
            if part_name in drone["body_parts"]:
                part = drone["body_parts"][part_name]
                if not part["destroyed"]:
                    part["hp"] = max(0, part["hp"] - damage_amount)
                    damage_report["total_damage"] += damage_amount

                    if part["hp"] <= 0:
                        part["destroyed"] = True
                        damage_report["destroyed_parts"].append(part_name)

                        # Check if critical part was destroyed
                        if part_name in ["head", "heart", "torso"]:
                            damage_report["drone_destroyed"] = True
                            break

        # Update total HP
        drone["hp"] = sum(part["hp"] for part in drone["body_parts"].values())

        return damage_report

    def _get_damage_targets(self, damage_type: str) -> List[str]:
        """Get body parts targeted by specific damage types"""
        damage_targets = {
            "fire": ["torso", "arms"],
            "water": ["legs"],
            "earthquake": ["head", "torso", "arms", "legs", "heart"],
            "meteor": ["head", "torso", "arms", "legs", "heart"],
            "starvation": ["torso", "heart"],
            "disease": ["head", "heart"],
        }
        return damage_targets.get(damage_type, ["torso"])

    def heal_drone(self, drone: Dict, heal_amount: int) -> Dict:
        """Heal drone HP (not SSHP) and return heal report"""
        heal_report = {"healed_parts": [], "total_healed": 0}

        # Heal each part proportionally
        for part_name, part_data in drone["body_parts"].items():
            if part_data["hp"] < part_data["max_hp"]:
                heal_needed = part_data["max_hp"] - part_data["hp"]
                heal_given = min(heal_amount, heal_needed)

                part_data["hp"] += heal_given
                heal_report["total_healed"] += heal_given
                heal_report["healed_parts"].append(part_name)

                heal_amount -= heal_given
                if heal_amount <= 0:
                    break

        # Update total HP
        drone["hp"] = sum(part["hp"] for part in drone["body_parts"].values())

        return heal_report

    def get_drone_summary(self, drone: Dict) -> Dict:
        """Get a summary of drone stats and status"""
        active_parts = sum(
            1 for part in drone["body_parts"].values() if not part["destroyed"]
        )
        total_parts = len(drone["body_parts"])

        return {
            "id": drone["id"],
            "name": drone["name"],
            "hp": drone["hp"],
            "max_hp": drone["max_hp"],
            "sshp": drone["sshp"],
            "max_sshp": drone["max_sshp"],
            "active_parts": active_parts,
            "total_parts": total_parts,
            "health_percentage": (
                (drone["hp"] / drone["max_hp"] * 100) if drone["max_hp"] > 0 else 0
            ),
            "sshp_percentage": (
                (drone["sshp"] / drone["max_sshp"] * 100)
                if drone["max_sshp"] > 0
                else 0
            ),
            "total_stats": drone["total_stats"],
            "evolution_stage": drone.get("evolution_stage", 1),
            "value": self.calculate_drone_value(drone),
        }
