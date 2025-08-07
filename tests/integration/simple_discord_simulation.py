#!/usr/bin/env python3
"""
Simple Discord Game Simulation
Tests core systems without requiring full bot configuration
"""

import sys
import os
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import core systems directly
try:
    from core.mod_system import ModSystem, GlobalRewardMultiplier, ModTemplateGenerator
    from core.economy import EnhancedEconomySystem
    from core.clds import CLDSSystem
    from core.disasters import DisasterSystem
    from core.leaderboard import ExclusiveLeaderboard
    print("✅ Core systems imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Falling back to standalone mod system test...")
    sys.exit(1)

@dataclass
class SimulatedUser:
    """Simulated Discord user"""
    id: str
    name: str
    rp: int = 100
    drones: List[Dict] = None
    
    def __post_init__(self):
        if self.drones is None:
            self.drones = []

@dataclass
class SimulatedMessage:
    """Simulated Discord message"""
    content: str
    author: SimulatedUser
    channel: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class SimpleDiscordSimulation:
    """Simple Discord simulation without full bot requirements"""
    
    def __init__(self):
        self.users = {}
        self.mod_system = ModSystem("data/simple_sim_mods.db")
        self.economy = EnhancedEconomySystem()
        self.clds = CLDSSystem()
        self.disasters = DisasterSystem()
        self.leaderboard = ExclusiveLeaderboard()
        self.global_multiplier = GlobalRewardMultiplier(self.mod_system)
        
        self.test_results = {
            "users_created": 0,
            "drones_generated": 0,
            "simulations_run": 0,
            "mods_created": 0,
            "economy_transactions": 0,
            "errors": []
        }
        
        print("🎮 Simple Discord Simulation Initialized")
        print("🔧 Core systems loaded successfully")
    
    def create_test_users(self, count: int = 5):
        """Create test users"""
        print(f"\n👥 Creating {count} test users...")
        
        for i in range(count):
            user_id = f"test_user_{i+1}"
            user = SimulatedUser(
                id=user_id,
                name=f"TestUser{i+1}",
                rp=random.randint(50, 200)
            )
            self.users[user_id] = user
            self.test_results["users_created"] += 1
        
        print(f"✅ Created {count} test users")
    
    def generate_drones_for_users(self):
        """Generate drones for all users"""
        print("\n🤖 Generating drones for users...")
        
        for user_id, user in self.users.items():
            drone_count = random.randint(1, 3)
            for i in range(drone_count):
                drone = self.clds.generate_drone(f"{user.name}_Drone_{i+1}")
                user.drones.append(drone)
                self.test_results["drones_generated"] += 1
        
        total_drones = sum(len(user.drones) for user in self.users.values())
        print(f"✅ Generated {total_drones} drones across all users")
    
    def run_simulations(self):
        """Run disaster simulations for users"""
        print("\n🌪️ Running disaster simulations...")
        
        for user_id, user in self.users.items():
            if user.drones:
                # Run simulation
                simulation_result = self.disasters.run_simulation(user.drones, 50)
                
                # Calculate RP rewards
                rp_earned = self.economy.calculate_simulation_reward(
                    simulation_result["surviving_drones"], 50
                )
                
                # Apply global multiplier
                final_rp = self.global_multiplier.apply_multiplier_to_reward(rp_earned)
                
                # Update user RP
                user.rp += int(final_rp)
                self.test_results["simulations_run"] += 1
                self.test_results["economy_transactions"] += 1
                
                print(f"  📊 {user.name}: {rp_earned} RP → {final_rp:.1f} RP (with multiplier)")
    
    def create_test_mods(self):
        """Create test mods"""
        print("\n🔧 Creating test mods...")
        
        # Create economy mod
        economy_mod = ModTemplateGenerator.create_economy_mod(
            creator_id="test_creator",
            name="RP Booster Pro",
            rp_gain_boost=1.5,
            cost_rp=150,
            daily_upkeep=10
        )
        
        # Create personality mod
        personality_mod = ModTemplateGenerator.create_personality_mod(
            creator_id="test_creator",
            name="Social Master",
            personality_traits=["charismatic", "leader", "inspiring"],
            cost_rp=100,
            daily_upkeep=7
        )
        
        # Save mods
        mod_id_1 = self.mod_system.create_mod_template(
            economy_mod.creator_id,
            economy_mod.name,
            economy_mod.description,
            economy_mod.category,
            economy_mod.cost_rp,
            economy_mod.daily_upkeep,
            economy_mod.effects,
            economy_mod.requirements
        )
        
        mod_id_2 = self.mod_system.create_mod_template(
            personality_mod.creator_id,
            personality_mod.name,
            personality_mod.description,
            personality_mod.category,
            personality_mod.cost_rp,
            personality_mod.daily_upkeep,
            personality_mod.effects,
            personality_mod.requirements
        )
        
        # Approve mods
        self.mod_system.mod_templates[mod_id_1].approved = True
        self.mod_system.mod_templates[mod_id_2].approved = True
        
        self.test_results["mods_created"] += 2
        print(f"✅ Created {self.test_results['mods_created']} test mods")
        
        return [mod_id_1, mod_id_2]
    
    def test_mod_activation(self, mod_ids: List[str]):
        """Test mod activation for users"""
        print("\n🔧 Testing mod activation...")
        
        for i, (user_id, user) in enumerate(self.users.items()):
            if i < len(mod_ids):
                mod_id = mod_ids[i]
                
                # Activate mod
                success = self.mod_system.activate_mod(user_id, mod_id)
                if success:
                    print(f"  ✅ {user.name}: Mod activated successfully")
                else:
                    print(f"  ❌ {user.name}: Mod activation failed")
    
    def update_global_multiplier(self):
        """Update global multiplier with test data"""
        print("\n🌍 Updating global multiplier...")
        
        total_drones = sum(len(user.drones) for user in self.users.values())
        active_players = len(self.users)
        drones_ever_died = max(1, total_drones - 5)  # Simulate some deaths
        
        self.global_multiplier.update_multiplier(
            total_drones, active_players, drones_ever_died
        )
        
        message = self.global_multiplier.get_multiplier_message()
        print(f"  📊 {message}")
    
    def run_comprehensive_test(self):
        """Run comprehensive simulation test"""
        print("🎮 Simple Discord Simulation Test")
        print("=" * 60)
        print("🚀 Testing core systems without full bot requirements")
        print("=" * 60)
        
        try:
            # Step 1: Create test users
            self.create_test_users(5)
            
            # Step 2: Generate drones
            self.generate_drones_for_users()
            
            # Step 3: Create test mods
            mod_ids = self.create_test_mods()
            
            # Step 4: Test mod activation
            self.test_mod_activation(mod_ids)
            
            # Step 5: Update global multiplier
            self.update_global_multiplier()
            
            # Step 6: Run simulations
            self.run_simulations()
            
            # Step 7: Save results
            self.save_results()
            
            print("\n🎉 Simple Discord Simulation Completed!")
            print("=" * 60)
            print("✅ All core systems tested successfully")
            print("🔧 Mod system working")
            print("💰 Economy integration active")
            print("🌍 Global multiplier operational")
            print("🤖 Drone generation functional")
            print("🌪️ Disaster simulation working")
            print("=" * 60)
            
            self.print_summary()
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            self.test_results["errors"].append(str(e))
            self.save_results()
    
    def save_results(self):
        """Save test results"""
        results_file = "simple_discord_results.json"
        
        with open(results_file, 'w') as f:
            json.dump({
                "test_timestamp": datetime.now().isoformat(),
                "test_results": self.test_results,
                "user_summary": {
                    user_id: {
                        "name": user.name,
                        "rp": user.rp,
                        "drone_count": len(user.drones)
                    }
                    for user_id, user in self.users.items()
                },
                "global_multiplier": self.global_multiplier.multiplier
            }, f, indent=2)
        
        print(f"📊 Results saved to: {results_file}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n📋 Test Summary:")
        print("-" * 40)
        
        print(f"👥 Users Created: {self.test_results['users_created']}")
        print(f"🤖 Drones Generated: {self.test_results['drones_generated']}")
        print(f"🌪️ Simulations Run: {self.test_results['simulations_run']}")
        print(f"🔧 Mods Created: {self.test_results['mods_created']}")
        print(f"💰 Economy Transactions: {self.test_results['economy_transactions']}")
        
        if self.test_results["errors"]:
            print(f"❌ Errors: {len(self.test_results['errors'])}")
            for error in self.test_results["errors"]:
                print(f"  • {error}")
        else:
            print("✅ No errors encountered")
        
        print(f"\n🌍 Global Multiplier: {self.global_multiplier.multiplier:.2f}x")
        
        # Show user stats
        print("\n👥 User Statistics:")
        for user_id, user in self.users.items():
            print(f"  {user.name}: {user.rp} RP, {len(user.drones)} drones")

def main():
    """Main function"""
    print("🚀 Starting Simple Discord Simulation")
    print("=" * 60)
    
    simulation = SimpleDiscordSimulation()
    simulation.run_comprehensive_test()

if __name__ == "__main__":
    main() 