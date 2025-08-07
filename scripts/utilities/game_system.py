#!/usr/bin/env python3
"""
Simulacra Rancher Game System
Core game logic extracted from Discord bot functionality
"""

import asyncio
import json
import random
import logging
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("game_system.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Import our core systems
from .gpu_personality import GPUPersonalityEngine
from .cpu_backend import CPUBackendEngine
from .memory_system import ConsolidatedMemorySystem as MemorySystem
from .kingdom_system import KingdomSystem, KingdomType, SubscriptionTier
from .discord_channels import DiscordChannelStructure
from .psychological_system import PsychologicalSystem
from .resource_system import ResourceSystem, GatheringMode
from .hunting_system import HuntingSystem, HuntingEvent
from .trade_system import TradeSystem

# Import consciousness systems (if available)
try:
    from .personality_engine import PersonalityEngine
    from .quantum_consciousness_processor import QuantumConsciousnessProcessor
    from .context_processor import ContextProcessor
    from .personality_generator import PersonalityGenerator

    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False
    logger.warning("⚠️ Consciousness systems not available")


class SimulacraGameSystem:
    """Core Simulacra Rancher game system without Discord dependencies"""

    def __init__(self):
        # Initialize core AI engines
        self.gpu_personality = GPUPersonalityEngine()
        self.cpu_backend = CPUBackendEngine()
        self.memory_system = MemorySystem()

        # Initialize kingdom systems
        self.kingdom_system = KingdomSystem()
        self.channel_structure = DiscordChannelStructure()
        self.psychological_system = PsychologicalSystem()

        # Initialize new game systems
        self.resource_system = ResourceSystem()
        self.hunting_system = HuntingSystem()
        self.trade_system = TradeSystem()

        # Initialize consciousness systems (if available)
        if CONSCIOUSNESS_AVAILABLE:
            self.personality_engine = PersonalityEngine()
            self.consciousness_processor = QuantumConsciousnessProcessor(
                personality_engine=self.personality_engine,
                memory_system=self.memory_system,
            )
            self.context_processor = ContextProcessor(self, self.memory_system)
            self.personality_generator = PersonalityGenerator(self, self.memory_system)
            logger.info("✅ Consciousness systems initialized")
        else:
            self.personality_engine = None
            self.consciousness_processor = None
            self.context_processor = None
            self.personality_generator = None
            logger.warning("⚠️ Consciousness systems not available")

        # Game state
        self.active_simulations = {}
        self.daily_bonuses = {}

    # ===== GAME COMMANDS =====

    def hatch_drone(
        self, user_id: str, drone_type: str = "standard", name: str = None
    ) -> Dict[str, Any]:
        """Hatch a new DigiDrone"""
        try:
            if not name:
                name = f"Drone_{random.randint(1000, 9999)}"

            # Create drone using CPU backend
            drone = self.cpu_backend.create_drone(name)

            # Generate personality response using GPU
            personality_response = self.gpu_personality.generate_response(
                f"New DigiDrone '{name}' has been created!",
                context="drone_creation",
            )

            # Get drone stats
            stats = drone["total_stats"]

            # Get body parts info
            parts_info = []
            for part_name, part_data in drone["body_parts"].items():
                rarity_color = {
                    "Common": "⚪",
                    "Uncommon": "🟢",
                    "Rare": "🔵",
                    "Epic": "🟣",
                    "Legendary": "🟠",
                    "Mythic": "🔴",
                }.get(part_data["rarity"], "⚪")

                parts_info.append(
                    f"{rarity_color} {part_name.title()}: {part_data['rarity']}"
                )

            return {
                "success": True,
                "drone_name": name,
                "personality_response": personality_response,
                "stats": stats,
                "hp": drone["hp"],
                "max_hp": drone["max_hp"],
                "sshp": drone["sshp"],
                "max_sshp": drone["max_sshp"],
                "body_parts": parts_info,
                "value": self.cpu_backend.clds_system.calculate_drone_value(drone),
            }

        except Exception as e:
            logger.error(f"Error hatching drone: {e}")
            return {"success": False, "error": str(e)}

    def run_simulation(
        self, user_id: str, duration: int = 60, drone_count: int = 10
    ) -> Dict[str, Any]:
        """Run a survival simulation with DigiDrones"""
        try:
            # Calculate simulation cost
            cost = self.cpu_backend.calculate_simulation_cost(duration, drone_count)

            # Check if user has enough RP
            player_data = self.cpu_backend.get_player_data(user_id)
            if player_data["rp"] < cost:
                return {
                    "success": False,
                    "error": f"Not enough RP! You need {cost} RP, but have {player_data['rp']} RP",
                }

            # Spend RP
            self.cpu_backend.spend_rp(user_id, cost)

            # Run simulation
            simulation_result = self.cpu_backend.process_simulation_logic(
                user_id, duration, drone_count
            )

            return {
                "success": True,
                "cost": cost,
                "duration": duration,
                "drone_count": drone_count,
                "surviving_drones": simulation_result["surviving_drones"],
                "disasters": simulation_result.get("disasters", []),
                "rp_earned": simulation_result["rp_earned"],
                "net_rp": simulation_result["rp_earned"] - cost,
                "evolution": simulation_result.get("evolution"),
            }

        except Exception as e:
            logger.error(f"Error running simulation: {e}")
            return {"success": False, "error": str(e)}

    def perform_gacha(self, user_id: str, amount: int = 1) -> Dict[str, Any]:
        """Spend RP for random DigiDrones"""
        try:
            # Perform gacha pull
            gacha_result = self.cpu_backend.perform_gacha_pull(user_id, amount)

            if not gacha_result["success"]:
                return {"success": False, "error": gacha_result["message"]}

            return {
                "success": True,
                "amount": amount,
                "cost": gacha_result["cost"],
                "drones": gacha_result["drones"],
                "total_value": gacha_result["total_value"],
            }

        except Exception as e:
            logger.error(f"Error in gacha: {e}")
            return {"success": False, "error": str(e)}

    def get_drone_info(self, user_id: str, name: str) -> Dict[str, Any]:
        """Get detailed DigiDrone information"""
        try:
            # Get drone data
            drone_data = self.cpu_backend.get_drone_data(user_id, name)
            if not drone_data:
                return {"success": False, "error": f"DigiDrone '{name}' not found!"}

            # Get drone summary
            summary = self.cpu_backend.get_drone_summary(drone_data)

            # Generate personality response
            personality_response = self.gpu_personality.generate_response(
                f"User is checking on DigiDrone {name}. Current health: {summary['hp']}/{summary['max_hp']} HP, {summary['sshp']}/{summary['max_sshp']} SSHP",
                context="drone_interaction",
            )

            # Get evolution status
            evolution_status = self.cpu_backend.get_evolutionary_status(drone_data)

            return {
                "success": True,
                "drone_name": name,
                "personality_response": personality_response,
                "hp": summary["hp"],
                "max_hp": summary["max_hp"],
                "sshp": summary["sshp"],
                "max_sshp": summary["max_sshp"],
                "health_percentage": summary["health_percentage"],
                "sshp_percentage": summary["sshp_percentage"],
                "total_stats": summary["total_stats"],
                "evolution_stage": evolution_status["stage"],
                "evolution_traits": evolution_status["traits"],
                "value": summary["value"],
                "active_parts": summary["active_parts"],
                "total_parts": summary["total_parts"],
            }

        except Exception as e:
            logger.error(f"Error viewing drone: {e}")
            return {"success": False, "error": str(e)}

    def get_leaderboard(self) -> Dict[str, Any]:
        """Get the exclusive top 10 leaderboard"""
        try:
            leaderboard_data = self.cpu_backend.get_leaderboard_display()
            return {"success": True, "leaderboard": leaderboard_data}
        except Exception as e:
            logger.error(f"Error loading leaderboard: {e}")
            return {"success": False, "error": str(e)}

    def get_rp_status(self, user_id: str) -> Dict[str, Any]:
        """Check user's Reflection Points and ranking"""
        try:
            player_data = self.cpu_backend.get_player_data(user_id)
            player_stats = self.cpu_backend.get_player_stats(user_id)
            player_ranking = self.cpu_backend.get_player_ranking(user_id)

            return {
                "success": True,
                "current_rp": player_data["rp"],
                "total_earned": player_stats["total_earned"],
                "total_spent": player_stats["total_spent"],
                "ranking": player_ranking,
            }
        except Exception as e:
            logger.error(f"Error checking RP: {e}")
            return {"success": False, "error": str(e)}

    def claim_daily_bonus(self, user_id: str) -> Dict[str, Any]:
        """Claim daily RP bonus"""
        try:
            daily_result = self.cpu_backend.get_daily_bonus(user_id)
            return {
                "success": daily_result["success"],
                "bonus": daily_result.get("bonus", 0),
                "new_balance": daily_result.get("new_balance", 0),
                "next_bonus": daily_result.get("next_bonus", ""),
                "message": daily_result.get("message", ""),
            }
        except Exception as e:
            logger.error(f"Error claiming daily bonus: {e}")
            return {"success": False, "error": str(e)}

    def get_shop_items(self) -> Dict[str, Any]:
        """Get shop items"""
        try:
            shop_items = self.cpu_backend.get_shop_items()
            return {"success": True, "shop_items": shop_items}
        except Exception as e:
            logger.error(f"Error loading shop: {e}")
            return {"success": False, "error": str(e)}

    def purchase_item(self, user_id: str, item_name: str) -> Dict[str, Any]:
        """Purchase an item from the shop"""
        try:
            purchase_result = self.cpu_backend.purchase_item(user_id, item_name)
            return {
                "success": purchase_result["success"],
                "cost": purchase_result.get("cost", 0),
                "new_balance": purchase_result.get("new_balance", 0),
                "effect": purchase_result.get("effect", ""),
                "message": purchase_result.get("message", ""),
            }
        except Exception as e:
            logger.error(f"Error purchasing item: {e}")
            return {"success": False, "error": str(e)}

    # ===== SCIENTIFIC COMMANDS =====

    def get_scientific_capabilities(
        self, user_id: str, drone_name: str
    ) -> Dict[str, Any]:
        """Get scientific capabilities of a drone"""
        try:
            result = self.cpu_backend.get_drone_scientific_capabilities(
                user_id, drone_name
            )
            return result
        except Exception as e:
            logger.error(f"Error checking scientific capabilities: {e}")
            return {"error": str(e)}

    def perform_scientific_calculation(
        self, user_id: str, drone_name: str, capability: str, query: str
    ) -> Dict[str, Any]:
        """Have a drone perform a scientific calculation"""
        try:
            result = self.cpu_backend.perform_scientific_calculation(
                user_id, drone_name, capability, query
            )
            return result
        except Exception as e:
            logger.error(f"Error performing calculation: {e}")
            return {"success": False, "error": str(e)}

    def generate_scientific_challenge(
        self, user_id: str, drone_name: str
    ) -> Dict[str, Any]:
        """Generate a scientific challenge for a drone"""
        try:
            result = self.cpu_backend.generate_scientific_challenge(user_id, drone_name)
            return result
        except Exception as e:
            logger.error(f"Error generating challenge: {e}")
            return {"error": str(e)}

    # ===== KINGDOM COMMANDS =====

    def get_all_kingdoms(self) -> Dict[str, Any]:
        """Get all 7 kingdoms"""
        try:
            kingdoms = self.kingdom_system.get_all_kingdoms()
            return {"success": True, "kingdoms": kingdoms}
        except Exception as e:
            logger.error(f"Error loading kingdoms: {e}")
            return {"success": False, "error": str(e)}

    def join_kingdom(
        self, user_id: str, username: str, kingdom_name: str
    ) -> Dict[str, Any]:
        """Join a kingdom as a citizen"""
        try:
            # Map kingdom name to KingdomType
            kingdom_mapping = {
                "lyra": KingdomType.LYRA_DOMINION,
                "fire": KingdomType.FIRE_KINGDOM,
                "water": KingdomType.WATER_KINGDOM,
                "earth": KingdomType.EARTH_KINGDOM,
                "air": KingdomType.AIR_KINGDOM,
                "lightning": KingdomType.LIGHTNING_KINGDOM,
                "ice": KingdomType.ICE_KINGDOM,
            }

            kingdom = kingdom_mapping.get(kingdom_name.lower())
            if not kingdom:
                return {
                    "success": False,
                    "error": "Invalid kingdom! Use: lyra, fire, water, earth, air, lightning, ice",
                }

            # For now, assume Tier 1 subscription
            tier = SubscriptionTier.TIER_1

            result = self.kingdom_system.join_kingdom(user_id, username, kingdom, tier)
            return result

        except Exception as e:
            logger.error(f"Error joining kingdom: {e}")
            return {"success": False, "error": str(e)}

    def claim_kingdom_throne(
        self, user_id: str, username: str, kingdom_name: str
    ) -> Dict[str, Any]:
        """Claim kingdom throne (Tier 3 only)"""
        try:
            # Map kingdom name to KingdomType
            kingdom_mapping = {
                "lyra": KingdomType.LYRA_DOMINION,
                "fire": KingdomType.FIRE_KINGDOM,
                "water": KingdomType.WATER_KINGDOM,
                "earth": KingdomType.EARTH_KINGDOM,
                "air": KingdomType.AIR_KINGDOM,
                "lightning": KingdomType.LIGHTNING_KINGDOM,
                "ice": KingdomType.ICE_KINGDOM,
            }

            kingdom = kingdom_mapping.get(kingdom_name.lower())
            if not kingdom:
                return {
                    "success": False,
                    "error": "Invalid kingdom! Use: lyra, fire, water, earth, air, lightning, ice",
                }

            result = self.kingdom_system.claim_kingdom_throne(
                user_id, username, kingdom
            )
            return result

        except Exception as e:
            logger.error(f"Error claiming throne: {e}")
            return {"success": False, "error": str(e)}

    def get_kingdom_info(self, kingdom_name: str) -> Dict[str, Any]:
        """Get kingdom information"""
        try:
            # Map kingdom name to KingdomType
            kingdom_mapping = {
                "lyra": KingdomType.LYRA_DOMINION,
                "fire": KingdomType.FIRE_KINGDOM,
                "water": KingdomType.WATER_KINGDOM,
                "earth": KingdomType.EARTH_KINGDOM,
                "air": KingdomType.AIR_KINGDOM,
                "lightning": KingdomType.LIGHTNING_KINGDOM,
                "ice": KingdomType.ICE_KINGDOM,
            }

            kingdom = kingdom_mapping.get(kingdom_name.lower())
            if not kingdom:
                return {
                    "success": False,
                    "error": "Invalid kingdom! Use: lyra, fire, water, earth, air, lightning, ice",
                }

            kingdom_info = self.kingdom_system.get_kingdom_info(kingdom)
            advantages = self.kingdom_system.get_elemental_advantages(kingdom)

            return {
                "success": True,
                "kingdom_info": kingdom_info,
                "advantages": advantages,
            }

        except Exception as e:
            logger.error(f"Error loading kingdom info: {e}")
            return {"success": False, "error": str(e)}

    # ===== RESOURCE COMMANDS =====

    def start_gathering(
        self, user_id: str, channel_id: str, mode: str = "normal"
    ) -> Dict[str, Any]:
        """Start gathering resources"""
        try:
            gathering_mode = (
                GatheringMode.FARMING
                if mode.lower() == "farming"
                else GatheringMode.NORMAL
            )
            result = self.resource_system.start_gathering(
                user_id, channel_id, gathering_mode
            )
            return result
        except Exception as e:
            logger.error(f"Error starting gathering: {e}")
            return {"success": False, "error": str(e)}

    def stop_gathering(self, user_id: str) -> Dict[str, Any]:
        """Stop gathering resources"""
        try:
            result = self.resource_system.stop_gathering(user_id)
            return result
        except Exception as e:
            logger.error(f"Error stopping gathering: {e}")
            return {"success": False, "error": str(e)}

    def get_user_resources(self, user_id: str) -> Dict[str, Any]:
        """Get user's resource inventory"""
        try:
            resources = self.resource_system.get_user_resources(user_id)
            return {"success": True, "resources": resources}
        except Exception as e:
            logger.error(f"Error loading resources: {e}")
            return {"success": False, "error": str(e)}

    # ===== HUNTING COMMANDS =====

    def attempt_catch(
        self, user_id: str, spawn_id: str, rp_amount: int
    ) -> Dict[str, Any]:
        """Attempt to catch a Simulacra"""
        try:
            result = self.hunting_system.attempt_catch(user_id, spawn_id, rp_amount)
            return result
        except Exception as e:
            logger.error(f"Error hunting: {e}")
            return {"success": False, "error": str(e)}

    def get_active_spawns(self) -> Dict[str, Any]:
        """Get active Simulacra spawns"""
        try:
            spawns = self.hunting_system.get_active_spawns()
            return {"success": True, "spawns": spawns}
        except Exception as e:
            logger.error(f"Error loading spawns: {e}")
            return {"success": False, "error": str(e)}

    def get_hunting_stats(self) -> Dict[str, Any]:
        """Get hunting statistics"""
        try:
            stats = self.hunting_system.get_hunting_stats()
            ai_power = self.hunting_system.get_ai_power_level()
            return {"success": True, "stats": stats, "ai_power": ai_power}
        except Exception as e:
            logger.error(f"Error loading hunting stats: {e}")
            return {"success": False, "error": str(e)}

    # ===== TRADE COMMANDS =====

    def create_trade_offer(
        self, seller_id: str, buyer_id: str, item_id: str, quantity: int, price: int
    ) -> Dict[str, Any]:
        """Create a trade offer"""
        try:
            result = self.trade_system.create_trade_offer(
                seller_id, buyer_id, item_id, quantity, price
            )
            return result
        except Exception as e:
            logger.error(f"Error creating trade: {e}")
            return {"success": False, "error": str(e)}

    def accept_trade_offer(self, buyer_id: str, offer_id: str) -> Dict[str, Any]:
        """Accept a trade offer"""
        try:
            result = self.trade_system.accept_trade_offer(buyer_id, offer_id)
            return result
        except Exception as e:
            logger.error(f"Error accepting trade: {e}")
            return {"success": False, "error": str(e)}

    def decline_trade_offer(self, buyer_id: str, offer_id: str) -> Dict[str, Any]:
        """Decline a trade offer"""
        try:
            result = self.trade_system.decline_trade_offer(buyer_id, offer_id)
            return result
        except Exception as e:
            logger.error(f"Error declining trade: {e}")
            return {"success": False, "error": str(e)}

    def get_user_inventory(self, user_id: str) -> Dict[str, Any]:
        """Get user's inventory"""
        try:
            inventory = self.trade_system.get_user_inventory(user_id)
            return {"success": True, "inventory": inventory}
        except Exception as e:
            logger.error(f"Error loading inventory: {e}")
            return {"success": False, "error": str(e)}

    def get_user_trade_offers(self, user_id: str) -> Dict[str, Any]:
        """Get user's trade offers"""
        try:
            offers = self.trade_system.get_user_trade_offers(user_id)
            return {"success": True, "offers": offers}
        except Exception as e:
            logger.error(f"Error loading trades: {e}")
            return {"success": False, "error": str(e)}

    # ===== SYSTEM STATUS =====

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        try:
            status = {
                "consciousness": CONSCIOUSNESS_AVAILABLE
                and self.consciousness_processor is not None,
                "memory_system": self.memory_system is not None,
                "personality_engine": CONSCIOUSNESS_AVAILABLE
                and self.personality_engine is not None,
                "cpu_backend": self.cpu_backend is not None,
                "resource_system": self.resource_system is not None,
                "hunting_system": self.hunting_system is not None,
                "trade_system": self.trade_system is not None,
                "kingdom_system": self.kingdom_system is not None,
                "psychological_system": self.psychological_system is not None,
            }
            return {"success": True, "status": status}
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"success": False, "error": str(e)}

    def get_help_info(self) -> Dict[str, Any]:
        """Get help information for all commands"""
        help_info = {
            "core_commands": [
                "hatch [type] [name] - Create a new DigiDrone",
                "simulate [duration] [drones] - Run survival simulation",
                "gacha [amount] - Spend RP for random DigiDrones",
                "drone [name] - View DigiDrone details and chat",
            ],
            "economy_commands": [
                "rp - Check your Reflection Points",
                "daily - Claim daily RP bonus",
                "shop - View shop items",
                "buy [item] - Purchase shop items",
            ],
            "scientific_commands": [
                "science [drone] - View drone's scientific capabilities",
                "calculate [drone] [capability] [query] - Perform scientific calculation",
                "challenge [drone] - Generate scientific challenge",
            ],
            "kingdom_commands": [
                "kingdoms - List all 7 kingdoms",
                "join [kingdom] - Join a kingdom as citizen",
                "claim [kingdom] - Claim kingdom throne (Tier 3)",
                "kingdom [name] - View kingdom information",
            ],
            "resource_commands": [
                "gather [mode] - Start gathering resources (normal/farming)",
                "stop_gathering - Stop gathering resources",
                "resources - Show your resource inventory",
            ],
            "hunting_commands": [
                "hunt [spawn_id] [rp] - Attempt to catch Simulacra",
                "spawns - Show active Simulacra spawns",
                "hunting_stats - Show hunting statistics",
            ],
            "trade_commands": [
                "trade [buyer] [item] [quantity] [price] - Create trade offer",
                "accept_trade [offer_id] - Accept a trade offer",
                "decline_trade [offer_id] - Decline a trade offer",
                "inventory - Show your inventory",
                "trades - Show your trade offers",
            ],
        }
        return {"success": True, "help_info": help_info}
