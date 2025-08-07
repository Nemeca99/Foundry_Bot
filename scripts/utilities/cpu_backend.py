#!/usr/bin/env python3
"""
CPU Backend Engine - Game Logic and Mechanics
Handles all game rules, database operations, and backend processing
"""

import sqlite3
import json
import random
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# Import game systems
from .clds import CLDSSystem
from .economy import EnhancedEconomySystem
from .disasters import DisasterSystem
from .leaderboard import ExclusiveLeaderboard
from .network_consciousness import NetworkConsciousness
from .dream_cycle import DreamCycleSystem
from .scientific_game_engine import ScientificGameEngine
from .survival_engine import SurvivalEngine, SurvivalStats

# Scientific integration is now part of scientific_game_engine
from .scientific_game_engine import ScientificGameEngine as ScientificIntegrationSystem
from .kingdom_system import KingdomSystem, KingdomType, SubscriptionTier
from .discord_channels import DiscordChannelStructure
from .psychological_system import PsychologicalSystem


class CPUBackendEngine:
    """CPU Backend Engine for game mechanics and logic"""

    def __init__(self):
        """Initialize the CPU backend with all game systems"""
        self.db_path = Path("data/digirancher.db")
        self.db_path.parent.mkdir(exist_ok=True)

        # Initialize all game systems
        self.clds_system = CLDSSystem()
        self.rp_economy = EnhancedEconomySystem()
        self.disaster_system = DisasterSystem()
        self.leaderboard = ExclusiveLeaderboard()
        self.network_consciousness = NetworkConsciousness()
        self.dream_cycle = DreamCycleSystem()
        self.scientific_engine = ScientificGameEngine()
        self.survival_engine = SurvivalEngine()
        self.scientific_integration = ScientificIntegrationSystem()
        self.kingdom_system = KingdomSystem()
        self.discord_channels = DiscordChannelStructure()
        self.psychological_system = PsychologicalSystem()

        # Initialize database
        self._init_database()

        print("⚙️ CPU Backend Engine initialized")
        print("   • C.L.D.S. System: Active")
        print("   • RP Economy: Active")
        print("   • Disaster System: Active")
        print("   • Leaderboard: Active")
        print("   • Network Consciousness: Active")
        print("   • Dream Cycle: Active")

    def _init_database(self):
        """Initialize SQLite database with all required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Players table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS players (
                    user_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    rp INTEGER DEFAULT 100,
                    total_earned INTEGER DEFAULT 0,
                    total_spent INTEGER DEFAULT 0,
                    daily_streak INTEGER DEFAULT 0,
                    last_daily TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Drones table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS drones (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    drone_data JSON NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_simulation TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES players (user_id)
                )
            """
            )

            # Simulations table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS simulations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    duration INTEGER NOT NULL,
                    drone_count INTEGER NOT NULL,
                    surviving_drones INTEGER NOT NULL,
                    rp_earned INTEGER NOT NULL,
                    disasters_triggered INTEGER DEFAULT 0,
                    evolutionary_events INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES players (user_id)
                )
            """
            )

            # Leaderboard table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    username TEXT NOT NULL,
                    ticks INTEGER NOT NULL,
                    drones INTEGER NOT NULL,
                    rp_earned INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Network consciousness table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS network_consciousness (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    drone_id TEXT NOT NULL,
                    server_id TEXT NOT NULL,
                    interaction_data JSON NOT NULL,
                    consciousness_level REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Dream cycles table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS dream_cycles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    drone_id TEXT NOT NULL,
                    dream_type TEXT NOT NULL,
                    consciousness_gain REAL NOT NULL,
                    dream_data JSON NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()

    def create_drone(self, name: str) -> Dict:
        """Create a new DigiDrone"""
        drone = self.clds_system.generate_drone(name)
        return drone

    def save_player_data(self, user_id: str, username: str, rp: int = 100):
        """Save or update player data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO players 
                (user_id, username, rp, last_active) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """,
                (user_id, username, rp),
            )
            conn.commit()

    def get_player_data(self, user_id: str) -> Dict:
        """Get player data, create if doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()

            if not row:
                # Create new player
                self.save_player_data(user_id, f"Player_{user_id[-4:]}", 100)
                return self.get_player_data(user_id)

            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))

    def save_drone_data(self, user_id: str, drone_id: str, drone_data: Dict):
        """Save drone data to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO drones 
                (id, user_id, name, drone_data) 
                VALUES (?, ?, ?, ?)
            """,
                (drone_id, user_id, drone_data["name"], json.dumps(drone_data)),
            )
            conn.commit()

    def get_drone_data(self, user_id: str, drone_name: str) -> Optional[Dict]:
        """Get drone data by name"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT drone_data FROM drones 
                WHERE user_id = ? AND name = ?
            """,
                (user_id, drone_name),
            )
            row = cursor.fetchone()

            if row:
                return json.loads(row[0])
            return None

    def get_player_drones(self, user_id: str) -> List[Dict]:
        """Get all drones for a player"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT drone_data FROM drones 
                WHERE user_id = ?
            """,
                (user_id,),
            )
            rows = cursor.fetchall()

            return [json.loads(row[0]) for row in rows]

    def calculate_simulation_cost(self, duration: int, drone_count: int) -> int:
        """Calculate simulation cost using RP economy"""
        return self.rp_economy.calculate_simulation_cost(duration, drone_count)

    def spend_rp(self, user_id: str, amount: int) -> bool:
        """Spend RP from player account"""
        return self.rp_economy.spend_rp(user_id, amount, self.db_path)

    def add_rp(self, user_id: str, amount: int) -> bool:
        """Add RP to player account"""
        return self.rp_economy.add_rp(user_id, amount, self.db_path)

    def process_simulation_logic(
        self, user_id: str, duration: int, drone_count: int
    ) -> Dict:
        """Process a complete simulation"""
        # Create drones for simulation
        drones = []
        for i in range(drone_count):
            drone = self.create_drone(f"SimDrone_{i+1}")
            drones.append(drone)

        # Run disaster simulation
        simulation_result = self.disaster_system.run_simulation(drones, duration)

        # Calculate RP rewards
        rp_earned = self.rp_economy.calculate_simulation_reward(
            simulation_result["surviving_drones"], duration
        )

        # Add RP to player
        self.add_rp(user_id, rp_earned)

        # Process evolution
        evolution_result = self.disaster_system.process_evolution(simulation_result)

        return {
            "surviving_drones": simulation_result["surviving_drones"],
            "total_drones": drone_count,
            "rp_earned": rp_earned,
            "disasters": simulation_result["disasters"],
            "evolution": evolution_result,
        }

    def perform_gacha_pull(self, user_id: str, amount: int) -> Dict:
        """Perform gacha pull for random DigiDrones"""
        return self.rp_economy.perform_gacha_pull(user_id, amount, self.db_path)

    def get_daily_bonus(self, user_id: str) -> Dict:
        """Get daily bonus for player"""
        return self.rp_economy.get_daily_bonus(user_id, self.db_path)

    def purchase_item(self, user_id: str, item_name: str) -> Dict:
        """Purchase item from shop"""
        return self.rp_economy.purchase_item(user_id, item_name, self.db_path)

    def get_shop_items(self) -> List[Dict]:
        """Get available shop items"""
        return self.rp_economy.get_shop_items()

    def submit_leaderboard_record(
        self, user_id: str, username: str, ticks: int, drones: int
    ):
        """Submit record to leaderboard"""
        self.leaderboard.submit_record(
            user_id, username, ticks, drones, 0, self.db_path
        )

    def get_leaderboard_display(self) -> List[Dict]:
        """Get leaderboard display data"""
        return self.leaderboard.get_top_entries(10, self.db_path)

    def get_player_ranking(self, user_id: str) -> Optional[Dict]:
        """Get player's ranking"""
        return self.leaderboard.get_player_ranking(user_id, self.db_path)

    def get_player_stats(self, user_id: str) -> Dict:
        """Get comprehensive player statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Get basic player data
            cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
            player_row = cursor.fetchone()

            if not player_row:
                return {
                    "total_earned": 0,
                    "total_spent": 0,
                    "total_runs": 0,
                    "best_run": 0,
                }

            # Get simulation stats
            cursor.execute(
                """
                SELECT COUNT(*), MAX(ticks), SUM(rp_earned), SUM(rp_spent)
                FROM simulations WHERE user_id = ?
            """,
                (user_id,),
            )
            sim_row = cursor.fetchone()

            total_runs = sim_row[0] if sim_row[0] else 0
            best_run = sim_row[1] if sim_row[1] else 0
            total_earned = sim_row[2] if sim_row[2] else 0
            total_spent = sim_row[3] if sim_row[3] else 0

            return {
                "total_earned": total_earned,
                "total_spent": total_spent,
                "total_runs": total_runs,
                "best_run": best_run,
            }

    def get_drone_summary(self, drone: Dict) -> Dict:
        """Get summary of drone stats and status"""
        return self.clds_system.get_drone_summary(drone)

    def get_evolutionary_status(self, drone: Dict) -> Dict:
        """Get evolutionary status of drone"""
        return self.disaster_system.get_evolutionary_status(drone)

    def get_available_traits(self, drone: Dict) -> List[str]:
        """Get available traits for drone"""
        return self.disaster_system.get_available_traits(drone)

    def get_global_stats(self) -> Dict:
        """Get global game statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total players
            cursor.execute("SELECT COUNT(*) FROM players")
            total_players = cursor.fetchone()[0]

            # Total simulations
            cursor.execute("SELECT COUNT(*) FROM simulations")
            total_simulations = cursor.fetchone()[0]

            # Total RP in economy
            cursor.execute("SELECT SUM(rp) FROM players")
            total_rp = cursor.fetchone()[0] or 0

            # Best run ever
            cursor.execute("SELECT MAX(ticks) FROM simulations")
            best_run = cursor.fetchone()[0] or 0

            return {
                "total_players": total_players,
                "total_simulations": total_simulations,
                "total_rp": total_rp,
                "best_run": best_run,
            }

    def get_achievements(self, user_id: str) -> List[Dict]:
        """Get player achievements"""
        achievements = []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Check various achievement conditions
            cursor.execute(
                "SELECT COUNT(*) FROM simulations WHERE user_id = ?", (user_id,)
            )
            total_runs = cursor.fetchone()[0]

            cursor.execute(
                "SELECT MAX(ticks) FROM simulations WHERE user_id = ?", (user_id,)
            )
            best_run = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM drones WHERE user_id = ?", (user_id,))
            total_drones = cursor.fetchone()[0]

            # Achievement checks
            if total_runs >= 1:
                achievements.append(
                    {
                        "name": "First Steps",
                        "description": "Complete your first simulation",
                        "icon": "🎯",
                    }
                )

            if total_runs >= 10:
                achievements.append(
                    {
                        "name": "Veteran",
                        "description": "Complete 10 simulations",
                        "icon": "🏆",
                    }
                )

            if best_run >= 100:
                achievements.append(
                    {
                        "name": "Survivor",
                        "description": "Survive 100 ticks in a simulation",
                        "icon": "🔥",
                    }
                )

            if total_drones >= 5:
                achievements.append(
                    {
                        "name": "Collector",
                        "description": "Own 5 DigiDrones",
                        "icon": "🤖",
                    }
                )

        return achievements

    def perform_scientific_calculation(
        self, user_id: str, drone_name: str, capability_name: str, query: str
    ) -> Dict[str, Any]:
        """Have a drone perform a scientific calculation"""
        drone = self.get_drone_data(user_id, drone_name)
        if not drone:
            return {"success": False, "error": "Drone not found"}

        result = self.scientific_engine.perform_scientific_calculation(
            drone, capability_name, query
        )

        if result["success"]:
            # Add RP reward to player
            self.add_rp(user_id, result["rp_reward"])

        return result

    def get_drone_scientific_capabilities(
        self, user_id: str, drone_name: str
    ) -> Dict[str, Any]:
        """Get scientific capabilities of a drone"""
        drone = self.get_drone_data(user_id, drone_name)
        if not drone:
            return {"error": "Drone not found"}

        capabilities = self.scientific_engine.get_available_calculations(drone)
        potential = self.scientific_engine.calculate_drone_scientific_potential(drone)

        return {
            "capabilities": capabilities,
            "potential": potential,
            "drone_name": drone_name,
        }

    def generate_scientific_challenge(
        self, user_id: str, drone_name: str
    ) -> Dict[str, Any]:
        """Generate a scientific challenge for a drone"""
        return self.scientific_integration.generate_challenge(user_id, drone_name)

    def get_status(self) -> str:
        """Get the status of the CPU backend engine"""
        try:
            # Check database connection
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM players")
                player_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM drones")
                drone_count = cursor.fetchone()[0]

            # Check system statuses
            systems_status = {
                "clds": "Active",
                "economy": "Active",
                "disasters": "Active",
                "leaderboard": "Active",
                "network_consciousness": "Active",
                "dream_cycle": "Active",
                "scientific_engine": "Active",
                "survival_engine": "Active",
                "scientific_integration": "Active",
                "kingdom_system": "Active",
                "discord_channels": "Active",
                "psychological_system": "Active",
            }

            return f"Players: {player_count}, Drones: {drone_count}, Systems: {len(systems_status)} active"

        except Exception as e:
            return f"Error: {str(e)}"
