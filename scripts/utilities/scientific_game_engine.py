#!/usr/bin/env python3
"""
Consolidated Scientific Game Engine
Integrates Scientific Reasoning Engine capabilities into DigiDrone game
Merges game integration and system integration functionality
"""

import sys
import os
from pathlib import Path
import math
import random
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum

# Add UML_RIS_Calc to path to import the Scientific Reasoning Engine
sys.path.append(str(Path(__file__).parent.parent / "UML_RIS_Calc"))

try:
    from scientific_reasoning_engine import (
        ScientificReasoningEngine,
        ValueWithUncertainty,
        EnhancedPhysicalConstants
    )
    SCIENTIFIC_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Scientific Reasoning Engine not available: {e}")
    SCIENTIFIC_ENGINE_AVAILABLE = False


class ScientificChallengeType(Enum):
    """Types of scientific challenges"""
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    MATHEMATICS = "mathematics"
    ENGINEERING = "engineering"
    BIOLOGY = "biology"
    ASTRONOMY = "astronomy"


@dataclass
class ScientificChallenge:
    """A scientific challenge for drones"""
    challenge_id: str
    challenge_type: ScientificChallengeType
    title: str
    description: str
    difficulty: int  # 1-10
    reward_rp: int
    required_capabilities: List[str]
    solution: str


@dataclass
class ScientificDroneCapability:
    """A scientific capability that a drone can perform"""
    name: str
    description: str
    physics_type: str  # "kinetic_energy", "escape_velocity", "gravitational_force", etc.
    required_stats: Dict[str, int]  # Stats needed to perform this calculation
    difficulty: int  # 1-10, higher = harder
    reward_multiplier: float  # RP reward multiplier for successful calculations


class ScientificGameEngine:
    """Consolidated scientific engine that integrates calculations and challenges into the DigiDrone game"""
    
    def __init__(self):
        self.scientific_engine = None
        if SCIENTIFIC_ENGINE_AVAILABLE:
            self.scientific_engine = ScientificReasoningEngine()
        
        # Define scientific capabilities drones can perform
        self.drone_capabilities = {
            "kinetic_energy": ScientificDroneCapability(
                name="Kinetic Energy Calculator",
                description="Calculate kinetic energy of objects",
                physics_type="kinetic_energy",
                required_stats={"INT": 3, "DEX": 2},
                difficulty=3,
                reward_multiplier=1.5
            ),
            "escape_velocity": ScientificDroneCapability(
                name="Escape Velocity Calculator", 
                description="Calculate escape velocity for celestial bodies",
                physics_type="escape_velocity",
                required_stats={"INT": 5, "WIS": 3},
                difficulty=6,
                reward_multiplier=2.0
            ),
            "gravitational_force": ScientificDroneCapability(
                name="Gravitational Force Calculator",
                description="Calculate gravitational force between objects",
                physics_type="gravitational_force", 
                required_stats={"INT": 4, "CON": 2},
                difficulty=4,
                reward_multiplier=1.8
            ),
            "dimensional_analysis": ScientificDroneCapability(
                name="Dimensional Analysis",
                description="Check dimensional consistency of equations",
                physics_type="dimensional_analysis",
                required_stats={"INT": 6, "WIS": 4},
                difficulty=7,
                reward_multiplier=2.5
            ),
            "uncertainty_propagation": ScientificDroneCapability(
                name="Uncertainty Propagation",
                description="Calculate uncertainty in complex calculations",
                physics_type="uncertainty_propagation",
                required_stats={"INT": 7, "WIS": 5},
                difficulty=8,
                reward_multiplier=3.0
            )
        }
        
        # Initialize challenge system
        self.challenges = self._init_challenges()
        self.active_challenges = {}
        self.drone_challenge_capabilities = self._init_drone_challenge_capabilities()

    def _init_drone_challenge_capabilities(self) -> Dict[str, List[str]]:
        """Initialize drone scientific capabilities for challenges"""
        return {
            "common": ["basic_physics", "simple_math"],
            "uncommon": ["advanced_physics", "chemistry", "statistics"],
            "rare": ["quantum_physics", "astronomy", "engineering"],
            "epic": ["theoretical_physics", "advanced_chemistry", "biophysics"],
            "legendary": [
                "all_sciences",
                "experimental_design",
                "scientific_reasoning",
            ],
        }

    def _init_challenges(self) -> Dict[str, ScientificChallenge]:
        """Initialize scientific challenges"""
        challenges = {}

        # Physics challenges
        challenges["kinetic_energy"] = ScientificChallenge(
            challenge_id="kinetic_energy",
            challenge_type=ScientificChallengeType.PHYSICS,
            title="Kinetic Energy Calculation",
            description="Calculate the kinetic energy of a moving object",
            difficulty=3,
            reward_rp=25,
            required_capabilities=["basic_physics"],
            solution="KE = 1/2 * m * v^2",
        )

        challenges["escape_velocity"] = ScientificChallenge(
            challenge_id="escape_velocity",
            challenge_type=ScientificChallengeType.PHYSICS,
            title="Escape Velocity",
            description="Calculate escape velocity from a planet",
            difficulty=6,
            reward_rp=50,
            required_capabilities=["advanced_physics"],
            solution="v = sqrt(2GM/r)",
        )

        challenges["quantum_state"] = ScientificChallenge(
            challenge_id="quantum_state",
            challenge_type=ScientificChallengeType.PHYSICS,
            title="Quantum State Analysis",
            description="Analyze quantum superposition states",
            difficulty=9,
            reward_rp=100,
            required_capabilities=["quantum_physics"],
            solution="|ψ⟩ = α|0⟩ + β|1⟩",
        )

        # Chemistry challenges
        challenges["molecular_weight"] = ScientificChallenge(
            challenge_id="molecular_weight",
            challenge_type=ScientificChallengeType.CHEMISTRY,
            title="Molecular Weight",
            description="Calculate molecular weight of compounds",
            difficulty=4,
            reward_rp=30,
            required_capabilities=["chemistry"],
            solution="Sum of atomic weights",
        )

        # Mathematics challenges
        challenges["calculus_integration"] = ScientificChallenge(
            challenge_id="calculus_integration",
            challenge_type=ScientificChallengeType.MATHEMATICS,
            title="Calculus Integration",
            description="Solve definite integrals",
            difficulty=7,
            reward_rp=60,
            required_capabilities=["advanced_math"],
            solution="∫f(x)dx = F(b) - F(a)",
        )

        return challenges
    
    def can_drone_perform_calculation(self, drone: Dict, capability_name: str) -> Dict[str, Any]:
        """Check if a drone can perform a specific scientific calculation"""
        if not SCIENTIFIC_ENGINE_AVAILABLE:
            return {
                "can_perform": False,
                "reason": "Scientific engine not available",
                "missing_stats": {},
                "success_chance": 0.0
            }
        
        if capability_name not in self.drone_capabilities:
            return {
                "can_perform": False,
                "reason": "Unknown capability",
                "missing_stats": {},
                "success_chance": 0.0
            }
        
        capability = self.drone_capabilities[capability_name]
        drone_stats = drone.get("total_stats", {})
        
        # Check if drone has required stats
        missing_stats = {}
        for stat, required in capability.required_stats.items():
            if drone_stats.get(stat, 0) < required:
                missing_stats[stat] = required - drone_stats.get(stat, 0)
        
        can_perform = len(missing_stats) == 0
        
        # Calculate success chance based on stats vs difficulty
        if can_perform:
            total_stat_bonus = sum(drone_stats.get(stat, 0) for stat in capability.required_stats.keys())
            success_chance = min(0.95, max(0.05, (total_stat_bonus - capability.difficulty * 2) / 10))
        else:
            success_chance = 0.0
        
        return {
            "can_perform": can_perform,
            "reason": f"Missing stats: {missing_stats}" if missing_stats else "Can perform",
            "missing_stats": missing_stats,
            "success_chance": success_chance,
            "capability": capability
        }
    
    def perform_scientific_calculation(self, drone: Dict, capability_name: str, 
                                     query: str) -> Dict[str, Any]:
        """Have a drone perform a scientific calculation"""
        if not SCIENTIFIC_ENGINE_AVAILABLE:
            return {
                "success": False,
                "error": "Scientific engine not available",
                "calculation_result": None,
                "rp_reward": 0
            }
        
        # Check if drone can perform this calculation
        capability_check = self.can_drone_perform_calculation(drone, capability_name)
        if not capability_check["can_perform"]:
            return {
                "success": False,
                "error": capability_check["reason"],
                "calculation_result": None,
                "rp_reward": 0
            }
        
        capability = capability_check["capability"]
        success_chance = capability_check["success_chance"]
        
        # Roll for success
        if random.random() > success_chance:
            return {
                "success": False,
                "error": "Calculation failed - drone's scientific skills insufficient",
                "calculation_result": None,
                "rp_reward": 0
            }
        
        try:
            # Perform the calculation using the scientific engine
            result = self.scientific_engine.process_natural_language_query(query)
            
            # Calculate RP reward based on difficulty and success
            base_reward = capability.difficulty * 5
            rp_reward = int(base_reward * capability.reward_multiplier)
            
            return {
                "success": True,
                "calculation_result": result,
                "rp_reward": rp_reward,
                "capability_used": capability.name,
                "difficulty": capability.difficulty
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Calculation error: {str(e)}",
                "calculation_result": None,
                "rp_reward": 0
            }
    
    def get_available_calculations(self, drone: Dict) -> List[Dict[str, Any]]:
        """Get list of calculations this drone can perform"""
        available = []
        
        for capability_name, capability in self.drone_capabilities.items():
            check = self.can_drone_perform_calculation(drone, capability_name)
            available.append({
                "name": capability_name,
                "capability": capability,
                "can_perform": check["can_perform"],
                "success_chance": check["success_chance"],
                "missing_stats": check["missing_stats"]
            })
        
        return available
    
    def generate_scientific_challenge(self, drone: Dict) -> Dict[str, Any]:
        """Generate a random scientific challenge for a drone"""
        if not SCIENTIFIC_ENGINE_AVAILABLE:
            return {
                "challenge_type": "none",
                "description": "Scientific engine not available",
                "query": "",
                "reward": 0
            }
        
        # Get available calculations
        available = self.get_available_calculations(drone)
        possible_challenges = [a for a in available if a["can_perform"]]
        
        if not possible_challenges:
            return {
                "challenge_type": "none", 
                "description": "Drone not capable of any scientific calculations",
                "query": "",
                "reward": 0
            }
        
        # Pick a random challenge
        challenge = random.choice(possible_challenges)
        capability = challenge["capability"]
        
        # Generate appropriate query based on capability type
        if capability.physics_type == "kinetic_energy":
            mass = random.uniform(1, 1000)
            velocity = random.uniform(1, 100)
            query = f"Calculate kinetic energy for mass {mass:.1f} kg moving at {velocity:.1f} m/s"
        elif capability.physics_type == "escape_velocity":
            bodies = ["Earth", "Moon", "Mars", "Jupiter"]
            body = random.choice(bodies)
            query = f"Calculate escape velocity for {body}"
        elif capability.physics_type == "gravitational_force":
            mass1 = random.uniform(1e6, 1e24)
            mass2 = random.uniform(1e6, 1e24)
            distance = random.uniform(1e6, 1e12)
            query = f"Calculate gravitational force between masses {mass1:.1e} kg and {mass2:.1e} kg at distance {distance:.1e} m"
        else:
            query = f"Perform {capability.name.lower()}"
        
        base_reward = capability.difficulty * 5
        reward = int(base_reward * capability.reward_multiplier)
        
        return {
            "challenge_type": capability.physics_type,
            "description": capability.description,
            "query": query,
            "reward": reward,
            "difficulty": capability.difficulty,
            "capability": capability.name
        }
    
    def apply_scientific_damage(self, drone: Dict, disaster_type: str) -> Dict[str, Any]:
        """Apply scientifically accurate damage based on physics"""
        if not SCIENTIFIC_ENGINE_AVAILABLE:
            return {"damage": 0, "reason": "Scientific engine not available"}
        
        # Use physics to calculate realistic damage
        if disaster_type == "meteor":
            # Calculate kinetic energy of meteor impact
            meteor_mass = random.uniform(100, 10000)  # kg
            meteor_velocity = random.uniform(10000, 50000)  # m/s
            
            try:
                ke_result = self.scientific_engine.calculate_kinetic_energy(meteor_mass, meteor_velocity)
                damage = int(ke_result["result"]["value"] / 1e6)  # Scale down for game
                return {
                    "damage": damage,
                    "reason": f"Meteor impact: {meteor_mass:.0f}kg at {meteor_velocity:.0f}m/s",
                    "physics_calculation": ke_result
                }
            except:
                return {"damage": random.randint(20, 50), "reason": "Meteor impact"}
        
        elif disaster_type == "earthquake":
            # Calculate seismic energy
            magnitude = random.uniform(4.0, 8.0)
            seismic_energy = 10 ** (1.5 * magnitude + 4.8)  # Joules
            damage = int(seismic_energy / 1e12)  # Scale down
            return {
                "damage": damage,
                "reason": f"Earthquake magnitude {magnitude:.1f}",
                "seismic_energy": seismic_energy
            }
        
        else:
            # Default damage for other disasters
            return {"damage": random.randint(5, 25), "reason": f"{disaster_type} damage"}
    
    def calculate_drone_scientific_potential(self, drone: Dict) -> Dict[str, Any]:
        """Calculate a drone's scientific potential and capabilities"""
        if not SCIENTIFIC_ENGINE_AVAILABLE:
            return {"potential": 0, "capabilities": []}
        
        drone_stats = drone.get("total_stats", {})
        total_intelligence = drone_stats.get("INT", 0)
        total_wisdom = drone_stats.get("WIS", 0)
        
        # Calculate scientific potential
        potential = (total_intelligence * 2 + total_wisdom) / 10
        
        # Determine capabilities
        capabilities = []
        for capability_name, capability in self.drone_capabilities.items():
            check = self.can_drone_perform_calculation(drone, capability_name)
            if check["can_perform"]:
                capabilities.append({
                    "name": capability_name,
                    "capability": capability.name,
                    "difficulty": capability.difficulty,
                    "success_chance": check["success_chance"]
                })
        
        return {
            "potential": potential,
            "capabilities": capabilities,
            "total_capabilities": len(capabilities),
            "max_difficulty": max([c["difficulty"] for c in capabilities]) if capabilities else 0
        }

    # Integration System Methods
    def get_drone_scientific_capabilities(self, drone_rarity: str) -> List[str]:
        """Get scientific capabilities for a drone based on rarity"""
        return self.drone_challenge_capabilities.get(drone_rarity.lower(), [])

    def can_solve_challenge(
        self, drone_capabilities: List[str], challenge: ScientificChallenge
    ) -> bool:
        """Check if a drone can solve a challenge"""
        return all(cap in drone_capabilities for cap in challenge.required_capabilities)

    def generate_challenge_for_drone(
        self, drone_rarity: str
    ) -> Optional[ScientificChallenge]:
        """Generate an appropriate challenge for a drone"""
        capabilities = self.get_drone_scientific_capabilities(drone_rarity)

        # Find challenges the drone can solve
        available_challenges = [
            challenge
            for challenge in self.challenges.values()
            if self.can_solve_challenge(capabilities, challenge)
        ]

        if not available_challenges:
            return None

        # Return a random challenge
        return random.choice(available_challenges)

    def perform_scientific_calculation(
        self, calculation_type: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform a scientific calculation using the Scientific Reasoning Engine"""
        if not self.scientific_engine:
            return {
                "success": False,
                "error": "Scientific Reasoning Engine not available",
            }

        try:
            if calculation_type == "kinetic_energy":
                mass = parameters.get("mass", 1.0)
                velocity = parameters.get("velocity", 1.0)

                # Use scientific engine for calculation
                result = self.scientific_engine.calculate_kinetic_energy(mass, velocity)

                return {
                    "success": True,
                    "calculation_type": "kinetic_energy",
                    "result": result.value,
                    "uncertainty": result.uncertainty,
                    "units": "Joules",
                }

            elif calculation_type == "escape_velocity":
                mass_planet = parameters.get("mass_planet", 5.97e24)
                radius_planet = parameters.get("radius_planet", 6.37e6)

                result = self.scientific_engine.calculate_escape_velocity(
                    mass_planet, radius_planet
                )

                return {
                    "success": True,
                    "calculation_type": "escape_velocity",
                    "result": result.value,
                    "uncertainty": result.uncertainty,
                    "units": "m/s",
                }

            else:
                return {
                    "success": False,
                    "error": f"Unknown calculation type: {calculation_type}",
                }

        except Exception as e:
            return {"success": False, "error": f"Calculation failed: {str(e)}"}

    def solve_challenge(
        self, challenge_id: str, drone_capabilities: List[str], user_solution: str
    ) -> Dict[str, Any]:
        """Attempt to solve a scientific challenge"""
        if challenge_id not in self.challenges:
            return {"success": False, "error": "Challenge not found"}

        challenge = self.challenges[challenge_id]

        # Check if drone can solve this challenge
        if not self.can_solve_challenge(drone_capabilities, challenge):
            return {"success": False, "error": "Drone lacks required capabilities"}

        # Simple solution checking (in real implementation, would be more sophisticated)
        solution_correct = (
            user_solution.lower().strip() == challenge.solution.lower().strip()
        )

        return {
            "success": True,
            "correct": solution_correct,
            "reward_rp": challenge.reward_rp if solution_correct else 0,
            "challenge": challenge,
        } 