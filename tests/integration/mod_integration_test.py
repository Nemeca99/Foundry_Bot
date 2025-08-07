#!/usr/bin/env python3
"""
Mod System Integration Test
Tests the complete mod system with economy integration
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our systems
from core.mod_system import ModSystem, GlobalRewardMultiplier, ModTemplateGenerator
from core.economy import EnhancedEconomySystem


class ModIntegrationTester:
    """Test the complete mod system integration"""

    def __init__(self):
        self.mod_system = ModSystem("data/test_mods.db")
        self.economy = EnhancedEconomySystem("data/test_economy.db")
        self.global_multiplier = GlobalRewardMultiplier(self.mod_system)

        # Test data
        self.test_users = [
            "test_user_1",
            "test_user_2",
            "test_user_3",
            "test_user_4",
            "test_user_5",
        ]

        self.test_mods = []
        self.test_results = {
            "mod_creation": [],
            "economy_integration": [],
            "global_multiplier": [],
            "daily_bonus": [],
            "mod_activation": [],
            "errors": [],
        }

    def run_comprehensive_test(self):
        """Run comprehensive mod system test"""
        print("🧪 Starting Mod System Integration Test")
        print("=" * 60)

        try:
            # Test 1: Create mod templates
            self._test_mod_creation()

            # Test 2: Economy integration
            self._test_economy_integration()

            # Test 3: Global multiplier system
            self._test_global_multiplier()

            # Test 4: Daily bonus system
            self._test_daily_bonus()

            # Test 5: Mod activation/deactivation
            self._test_mod_activation()

            # Test 6: Complex scenarios
            self._test_complex_scenarios()

            # Save results
            self._save_test_results()

            print("\n✅ Mod System Integration Test Completed!")
            self._print_summary()

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            self.test_results["errors"].append(str(e))
            self._save_test_results()

    def _test_mod_creation(self):
        """Test mod template creation"""
        print("\n📝 Testing Mod Creation...")

        # Create economy mod
        economy_mod = ModTemplateGenerator.create_economy_mod(
            creator_id="test_creator_1",
            name="RP Booster",
            rp_gain_boost=1.25,
            cost_rp=100,
            daily_upkeep=5,
        )

        # Create personality mod
        personality_mod = ModTemplateGenerator.create_personality_mod(
            creator_id="test_creator_2",
            name="Social Butterfly",
            personality_traits=["social", "charismatic", "friendly"],
            cost_rp=75,
            daily_upkeep=3,
        )

        # Save mods to system
        mod_id_1 = self.mod_system.create_mod_template(
            economy_mod.creator_id,
            economy_mod.name,
            economy_mod.description,
            economy_mod.category,
            economy_mod.cost_rp,
            economy_mod.daily_upkeep,
            economy_mod.effects,
            economy_mod.requirements,
        )

        mod_id_2 = self.mod_system.create_mod_template(
            personality_mod.creator_id,
            personality_mod.name,
            personality_mod.description,
            personality_mod.category,
            personality_mod.cost_rp,
            personality_mod.daily_upkeep,
            personality_mod.effects,
            personality_mod.requirements,
        )

        # Approve mods for testing
        self.mod_system.mod_templates[mod_id_1].approved = True
        self.mod_system.mod_templates[mod_id_2].approved = True

        self.test_mods = [mod_id_1, mod_id_2]

        self.test_results["mod_creation"].append(
            {"economy_mod": mod_id_1, "personality_mod": mod_id_2, "status": "success"}
        )

        print(f"  ✅ Created {len(self.test_mods)} mod templates")

    def _test_economy_integration(self):
        """Test economy system integration"""
        print("\n💰 Testing Economy Integration...")

        for user_id in self.test_users:
            # Give users some starting RP
            self.economy.earn_rp(user_id, 200, "Starting RP")

            # Test earning with different scenarios
            base_earnings = self.economy.earn_rp(user_id, 10, "Test Activity")

            # Get economy info
            economy_info = self.economy.get_user_economy_info(user_id)

            self.test_results["economy_integration"].append(
                {
                    "user_id": user_id,
                    "balance": economy_info["balance"],
                    "base_earnings": base_earnings,
                    "global_multiplier": economy_info["global_multiplier"],
                }
            )

        print(f"  ✅ Tested economy for {len(self.test_users)} users")

    def _test_global_multiplier(self):
        """Test global reward multiplier system"""
        print("\n🌍 Testing Global Multiplier System...")

        # Test different scenarios
        scenarios = [
            {
                "drones_alive": 100,
                "active_players": 10,
                "drones_ever_died": 50,
            },  # Good economy
            {
                "drones_alive": 50,
                "active_players": 5,
                "drones_ever_died": 200,
            },  # Declining economy
            {
                "drones_alive": 200,
                "active_players": 20,
                "drones_ever_died": 10,
            },  # Booming economy
            {
                "drones_alive": 10,
                "active_players": 2,
                "drones_ever_died": 500,
            },  # Crisis economy
        ]

        for i, scenario in enumerate(scenarios):
            self.global_multiplier.update_multiplier(
                scenario["drones_alive"],
                scenario["active_players"],
                scenario["drones_ever_died"],
            )

            message = self.global_multiplier.get_multiplier_message()

            self.test_results["global_multiplier"].append(
                {
                    "scenario": f"Scenario {i+1}",
                    "multiplier": self.global_multiplier.multiplier,
                    "message": message,
                    "drones_alive": scenario["drones_alive"],
                    "active_players": scenario["active_players"],
                    "drones_ever_died": scenario["drones_ever_died"],
                }
            )

        print(f"  ✅ Tested {len(scenarios)} multiplier scenarios")

    def _test_daily_bonus(self):
        """Test daily bonus system"""
        print("\n🎁 Testing Daily Bonus System...")

        for user_id in self.test_users:
            # Test daily bonus claim
            can_claim, bonus_amount = self.economy.check_daily_bonus(user_id)

            self.test_results["daily_bonus"].append(
                {
                    "user_id": user_id,
                    "can_claim": can_claim,
                    "bonus_amount": bonus_amount,
                    "balance_after": self.economy.get_user_balance(user_id),
                }
            )

        print(f"  ✅ Tested daily bonus for {len(self.test_users)} users")

    def _test_mod_activation(self):
        """Test mod activation and deactivation"""
        print("\n🔧 Testing Mod Activation...")

        for i, user_id in enumerate(self.test_users):
            if i < len(self.test_mods):
                mod_id = self.test_mods[i]

                # Test activation
                activation_success = self.economy.activate_mod(user_id, mod_id)

                # Get mod info
                mod_info = self.mod_system.get_player_mods(user_id)

                # Test deactivation
                deactivation_success = self.economy.deactivate_mod(user_id, mod_id)

                self.test_results["mod_activation"].append(
                    {
                        "user_id": user_id,
                        "mod_id": mod_id,
                        "activation_success": activation_success,
                        "deactivation_success": deactivation_success,
                        "mod_info": mod_info,
                    }
                )

        print(f"  ✅ Tested mod activation for {len(self.test_mods)} users")

    def _test_complex_scenarios(self):
        """Test complex scenarios with multiple systems"""
        print("\n🎯 Testing Complex Scenarios...")

        # Scenario 1: User with mods earning RP
        user_id = "complex_test_user"

        # Give user RP
        self.economy.earn_rp(user_id, 500, "Complex Test Starting RP")

        # Create and activate a mod
        if self.test_mods:
            mod_id = self.test_mods[0]
            self.economy.activate_mod(user_id, mod_id)

            # Earn RP with mod active
            earnings_with_mod = self.economy.earn_rp(user_id, 50, "Activity with Mod")

            # Deactivate mod
            self.economy.deactivate_mod(user_id, mod_id)

            # Earn RP without mod
            earnings_without_mod = self.economy.earn_rp(
                user_id, 50, "Activity without Mod"
            )

            # Get final economy info
            final_info = self.economy.get_user_economy_info(user_id)

            self.test_results["complex_scenarios"] = {
                "user_id": user_id,
                "earnings_with_mod": earnings_with_mod,
                "earnings_without_mod": earnings_without_mod,
                "final_balance": final_info["balance"],
                "mod_profile": final_info["mod_profile"],
            }

        print("  ✅ Tested complex scenario")

    def _save_test_results(self):
        """Save test results to file"""
        results_file = "simulation/mod_integration_results.json"

        with open(results_file, "w") as f:
            json.dump(
                {
                    "test_timestamp": datetime.now().isoformat(),
                    "test_results": self.test_results,
                    "summary": {
                        "total_tests": len(self.test_results) - 1,  # Exclude errors
                        "errors": len(self.test_results["errors"]),
                        "mods_created": len(self.test_mods),
                        "users_tested": len(self.test_users),
                    },
                },
                f,
                indent=2,
            )

        print(f"📊 Results saved to: {results_file}")

    def _print_summary(self):
        """Print test summary"""
        print("\n📋 Test Summary:")
        print("-" * 40)

        print(f"📝 Mod Creation: {len(self.test_results['mod_creation'])} tests")
        print(
            f"💰 Economy Integration: {len(self.test_results['economy_integration'])} tests"
        )
        print(
            f"🌍 Global Multiplier: {len(self.test_results['global_multiplier'])} tests"
        )
        print(f"🎁 Daily Bonus: {len(self.test_results['daily_bonus'])} tests")
        print(f"🔧 Mod Activation: {len(self.test_results['mod_activation'])} tests")

        if self.test_results["errors"]:
            print(f"❌ Errors: {len(self.test_results['errors'])}")
            for error in self.test_results["errors"]:
                print(f"  • {error}")
        else:
            print("✅ No errors encountered")

        # Print some key results
        if self.test_results["global_multiplier"]:
            latest_multiplier = self.test_results["global_multiplier"][-1]
            print(
                f"\n🌍 Latest Global Multiplier: {latest_multiplier['multiplier']:.2f}x"
            )
            print(f"📢 Message: {latest_multiplier['message']}")


def main():
    """Main test function"""
    print("🚀 Starting Mod System Integration Test")
    print("=" * 60)

    tester = ModIntegrationTester()
    tester.run_comprehensive_test()


if __name__ == "__main__":
    main()
