#!/usr/bin/env python3
"""
Disaster System
Environmental events affecting DigiDrones with SSHP and HP damage
"""

import random
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta


class DisasterSystem:
    """Disaster System for DigiDrones"""

    def __init__(self):
        self.disaster_types = {
            "fire": {
                "name": "Fire",
                "sshp_damage": 3,
                "hp_damage": 2,
                "target_parts": ["torso", "arms"],
                "frequency": 0.15,
                "description": "🔥 A raging fire sweeps through the area!",
            },
            "water": {
                "name": "Flood",
                "sshp_damage": 4,
                "hp_damage": 2,
                "target_parts": ["legs"],
                "frequency": 0.12,
                "description": "🌊 A sudden flood engulfs the area!",
            },
            "earthquake": {
                "name": "Earthquake",
                "sshp_damage": 5,
                "hp_damage": 3,
                "target_parts": ["head", "torso", "arms", "legs", "heart"],
                "frequency": 0.10,
                "description": "🌋 The ground shakes violently!",
            },
            "meteor": {
                "name": "Meteor Strike",
                "sshp_damage": 5,
                "hp_damage": 2,
                "target_parts": ["head", "torso", "arms", "legs", "heart"],
                "frequency": 0.08,
                "description": "☄️ A meteor crashes from the sky!",
            },
            "starvation": {
                "name": "Starvation",
                "sshp_damage": 3,
                "hp_damage": 1,
                "target_parts": ["torso", "heart"],
                "frequency": 0.20,
                "description": "🍽️ Food supplies are running low!",
            },
            "disease": {
                "name": "Disease",
                "sshp_damage": 2,
                "hp_damage": 1,
                "target_parts": ["head", "heart"],
                "frequency": 0.18,
                "description": "🦠 A mysterious disease spreads!",
            },
        }

        self.evolutionary_traits = {
            "fire_survivor": {
                "name": "Fire Survivor",
                "description": "Resistant to fire damage",
                "unlock_condition": "survive_fire",
                "effect": "fire_resistance",
            },
            "water_adapted": {
                "name": "Water Adapted",
                "description": "Resistant to water damage",
                "unlock_condition": "survive_water",
                "effect": "water_resistance",
            },
            "earthquake_proof": {
                "name": "Earthquake Proof",
                "description": "Resistant to earthquake damage",
                "unlock_condition": "survive_earthquake",
                "effect": "earthquake_resistance",
            },
            "meteor_shield": {
                "name": "Meteor Shield",
                "description": "Resistant to meteor damage",
                "unlock_condition": "survive_meteor",
                "effect": "meteor_resistance",
            },
            "starvation_resistant": {
                "name": "Starvation Resistant",
                "description": "Resistant to starvation damage",
                "unlock_condition": "survive_starvation",
                "effect": "starvation_resistance",
            },
            "disease_immune": {
                "name": "Disease Immune",
                "description": "Resistant to disease damage",
                "unlock_condition": "survive_disease",
                "effect": "disease_resistance",
            },
        }

    def get_disaster_types(self) -> List[str]:
        """Get list of available disaster types"""
        return list(self.disaster_types.keys())

    def trigger_disaster(self, drones: List[Dict], tick: int) -> Dict:
        """Trigger a random disaster and apply damage to drones"""
        # Determine if a disaster should occur
        disaster_chance = self._calculate_disaster_chance(tick)

        if random.random() > disaster_chance:
            return {
                "disaster_occurred": False,
                "message": "The area remains peaceful...",
            }

        # Select disaster type based on frequency
        disaster_type = self._select_disaster_type()
        disaster_config = self.disaster_types[disaster_type]

        # Apply disaster to all drones
        damage_report = {
            "disaster_occurred": True,
            "disaster_type": disaster_type,
            "disaster_name": disaster_config["name"],
            "description": disaster_config["description"],
            "tick": tick,
            "affected_drones": 0,
            "destroyed_drones": 0,
            "damage_details": [],
        }

        for drone in drones:
            if drone.get("sshp", 0) <= 0:  # Skip already destroyed drones
                continue

            damage_detail = self._apply_disaster_to_drone(
                drone, disaster_type, disaster_config
            )
            damage_report["damage_details"].append(damage_detail)

            if damage_detail["drone_destroyed"]:
                damage_report["destroyed_drones"] += 1
            else:
                damage_report["affected_drones"] += 1

        return damage_report

    def _calculate_disaster_chance(self, tick: int) -> float:
        """Calculate disaster chance based on tick number"""
        # Base chance increases with time
        base_chance = 0.05 + (tick * 0.001)  # 5% base + 0.1% per tick
        return min(base_chance, 0.30)  # Cap at 30%

    def _select_disaster_type(self) -> str:
        """Select disaster type based on frequency weights"""
        disaster_types = list(self.disaster_types.keys())
        frequencies = [self.disaster_types[dt]["frequency"] for dt in disaster_types]

        return random.choices(disaster_types, weights=frequencies)[0]

    def _apply_disaster_to_drone(
        self, drone: Dict, disaster_type: str, disaster_config: Dict
    ) -> Dict:
        """Apply disaster damage to a single drone"""
        damage_detail = {
            "drone_id": drone.get("id"),
            "drone_name": drone.get("name"),
            "disaster_type": disaster_type,
            "sshp_damage": 0,
            "hp_damage": 0,
            "destroyed_parts": [],
            "drone_destroyed": False,
            "evolutionary_progress": [],
        }

        # Apply SSHP damage first
        sshp_damage = disaster_config["sshp_damage"]
        drone["sshp"] = max(0, drone["sshp"] - sshp_damage)
        damage_detail["sshp_damage"] = sshp_damage

        # Check if drone is destroyed by SSHP loss
        if drone["sshp"] <= 0:
            damage_detail["drone_destroyed"] = True
            return damage_detail

        # Apply HP damage to specific body parts
        target_parts = disaster_config["target_parts"]
        hp_damage = disaster_config["hp_damage"]

        for part_name in target_parts:
            if part_name in drone.get("body_parts", {}):
                part = drone["body_parts"][part_name]
                if not part.get("destroyed", False):
                    part["hp"] = max(0, part["hp"] - hp_damage)
                    damage_detail["hp_damage"] += hp_damage

                    if part["hp"] <= 0:
                        part["destroyed"] = True
                        damage_detail["destroyed_parts"].append(part_name)

                        # Check if critical part was destroyed
                        if part_name in ["head", "heart", "torso"]:
                            damage_detail["drone_destroyed"] = True
                            break

        # Update total HP
        drone["hp"] = sum(part["hp"] for part in drone.get("body_parts", {}).values())

        # Check evolutionary progress
        if not damage_detail["drone_destroyed"]:
            damage_detail["evolutionary_progress"] = self._check_evolutionary_progress(
                drone, disaster_type
            )

        return damage_detail

    def _check_evolutionary_progress(
        self, drone: Dict, disaster_type: str
    ) -> List[Dict]:
        """Check if drone has made evolutionary progress from surviving disaster"""
        progress = []

        # Track disaster survival
        disaster_survivals = drone.get("disaster_survivals", {})
        if disaster_type not in disaster_survivals:
            disaster_survivals[disaster_type] = 0
        disaster_survivals[disaster_type] += 1
        drone["disaster_survivals"] = disaster_survivals

        # Check for trait unlocks
        trait_key = f"{disaster_type}_survivor"
        if trait_key in self.evolutionary_traits:
            trait = self.evolutionary_traits[trait_key]
            required_survivals = 3  # Need to survive 3 times to unlock trait

            if disaster_survivals[disaster_type] >= required_survivals:
                # Check if trait is already unlocked
                unlocked_traits = drone.get("unlocked_traits", [])
                if trait_key not in unlocked_traits:
                    unlocked_traits.append(trait_key)
                    drone["unlocked_traits"] = unlocked_traits

                    progress.append(
                        {
                            "type": "trait_unlocked",
                            "trait": trait_key,
                            "name": trait["name"],
                            "description": trait["description"],
                        }
                    )

        # Check for evolution stage increase
        if disaster_survivals[disaster_type] % 5 == 0:  # Every 5 survivals
            current_stage = drone.get("evolution_stage", 1)
            new_stage = current_stage + 1
            drone["evolution_stage"] = new_stage

            progress.append(
                {
                    "type": "evolution_stage",
                    "old_stage": current_stage,
                    "new_stage": new_stage,
                    "description": f"Evolved to stage {new_stage}!",
                }
            )

        return progress

    def get_disaster_resistance(self, drone: Dict, disaster_type: str) -> float:
        """Calculate drone's resistance to a specific disaster type"""
        resistance = 0.0

        # Check for unlocked traits
        unlocked_traits = drone.get("unlocked_traits", [])
        trait_key = f"{disaster_type}_survivor"

        if trait_key in unlocked_traits:
            resistance += 0.5  # 50% damage reduction

        # Check for evolution stage bonus
        evolution_stage = drone.get("evolution_stage", 1)
        resistance += (evolution_stage - 1) * 0.1  # 10% per evolution stage

        return min(resistance, 0.8)  # Cap at 80% resistance

    def apply_resistance_to_damage(self, base_damage: int, resistance: float) -> int:
        """Apply resistance to damage calculation"""
        damage_reduction = int(base_damage * resistance)
        return max(1, base_damage - damage_reduction)  # Minimum 1 damage

    def get_disaster_summary(self, disaster_report: Dict) -> str:
        """Generate a human-readable summary of disaster results"""
        if not disaster_report["disaster_occurred"]:
            return disaster_report["message"]

        summary = f"**{disaster_report['disaster_name']}**\n"
        summary += f"{disaster_report['description']}\n\n"

        if disaster_report["destroyed_drones"] > 0:
            summary += (
                f"💀 **{disaster_report['destroyed_drones']} drones destroyed**\n"
            )

        if disaster_report["affected_drones"] > 0:
            summary += f"⚠️ **{disaster_report['affected_drones']} drones damaged**\n"

        # Add evolutionary progress
        evolution_count = 0
        for detail in disaster_report["damage_details"]:
            evolution_count += len(detail.get("evolutionary_progress", []))

        if evolution_count > 0:
            summary += f"✨ **{evolution_count} evolutionary breakthroughs!**\n"

        return summary

    def get_drone_evolutionary_status(self, drone: Dict) -> Dict:
        """Get detailed evolutionary status of a drone"""
        disaster_survivals = drone.get("disaster_survivals", {})
        unlocked_traits = drone.get("unlocked_traits", [])
        evolution_stage = drone.get("evolution_stage", 1)

        status = {
            "evolution_stage": evolution_stage,
            "total_disaster_survivals": sum(disaster_survivals.values()),
            "unlocked_traits": len(unlocked_traits),
            "disaster_survivals": disaster_survivals,
            "unlocked_traits_list": unlocked_traits,
            "trait_details": [],
        }

        # Get details for each unlocked trait
        for trait_key in unlocked_traits:
            if trait_key in self.evolutionary_traits:
                trait = self.evolutionary_traits[trait_key]
                status["trait_details"].append(
                    {
                        "key": trait_key,
                        "name": trait["name"],
                        "description": trait["description"],
                        "effect": trait["effect"],
                    }
                )

        return status

    def get_available_traits(self, drone: Dict) -> List[Dict]:
        """Get list of traits that can still be unlocked"""
        disaster_survivals = drone.get("disaster_survivals", {})
        unlocked_traits = drone.get("unlocked_traits", [])
        available_traits = []

        for trait_key, trait in self.evolutionary_traits.items():
            if trait_key not in unlocked_traits:
                disaster_type = trait_key.replace("_survivor", "")
                survivals = disaster_survivals.get(disaster_type, 0)
                required = 3

                available_traits.append(
                    {
                        "key": trait_key,
                        "name": trait["name"],
                        "description": trait["description"],
                        "progress": survivals,
                        "required": required,
                        "percentage": min(100, (survivals / required) * 100),
                    }
                )

        return available_traits
