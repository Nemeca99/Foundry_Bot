#!/usr/bin/env python3
"""
Controlled Random Simulation Runner
Main simulation with realistic human behavior and symbolic game structure (MOD system)
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our symbolic game structure
from symbolic_game_structure import (
    SymbolicGameStructure,
    RealisticRandomGenerator,
    ControlledRandomSimulation,
    BalanceModification,
)


class ControlledRandomSimulationRunner:
    """Main runner for controlled random simulation with realistic human behavior"""

    def __init__(self, project_root: str = None):
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.project_root = Path(project_root)
        self.simulation = ControlledRandomSimulation(str(self.project_root))
        self.results = {}

    def run_full_simulation(
        self,
        tester_count: int = 100,
        duration_minutes: int = 30,
        enable_symbolic_structure: bool = True,
        enable_balance_testing: bool = True,
    ):
        """Run a full controlled random simulation"""

        print("🎮 Starting Controlled Random Simulation")
        print("=" * 60)
        print(f"📊 Generating {tester_count} realistic testers")
        print(f"⏰ Running for {duration_minutes} minutes")
        print(
            f"🏗️  Symbolic structure: {'Enabled' if enable_symbolic_structure else 'Disabled'}"
        )
        print(
            f"⚖️  Balance testing: {'Enabled' if enable_balance_testing else 'Disabled'}"
        )
        print("=" * 60)

        # Generate realistic testers
        print("\n👥 Generating realistic testers...")
        self.simulation.generate_testers(tester_count)

        # Create symbolic structure if enabled
        if enable_symbolic_structure:
            print("\n🏗️  Setting up symbolic game structure (MOD system)...")
            self.simulation.symbolic_structure.create_symbolic_structure()

        # Run the controlled simulation
        print(f"\n🎮 Running controlled random simulation...")
        start_time = time.time()

        try:
            self.simulation.run_controlled_simulation(duration_minutes)
            simulation_time = time.time() - start_time
            print(f"\n✅ Simulation completed in {simulation_time:.2f} seconds")

        except Exception as e:
            print(f"\n❌ Simulation failed: {e}")
            return False

        # Save results
        self._save_simulation_results()

        # Run balance analysis if enabled
        if enable_balance_testing:
            print("\n⚖️  Running balance analysis...")
            self._run_balance_analysis()

        print("\n🎉 Controlled random simulation completed!")
        return True

    def _save_simulation_results(self):
        """Save comprehensive simulation results"""
        results = {
            "simulation_info": {
                "timestamp": datetime.now().isoformat(),
                "project_root": str(self.project_root),
                "symbolic_structure_enabled": True,
                "mod_system": True,
            },
            "tester_statistics": self.simulation.simulation_stats,
            "tester_details": [
                {
                    "user_id": tester["user_id"],
                    "user_type": tester["user_type"],
                    "activity_pattern": tester["activity_pattern"],
                    "personality_traits": tester["personality_traits"],
                    "chat_style": tester["chat_style"],
                    "risk_tolerance": tester["risk_tolerance"],
                    "social_level": tester["social_level"],
                    "error_prone": tester["error_prone"],
                    "learning_curve": tester["learning_curve"],
                }
                for tester in self.simulation.testers
            ],
            "command_analysis": {
                "usage_distribution": self.simulation.simulation_stats[
                    "command_usage_distribution"
                ],
                "error_distribution": self.simulation.simulation_stats[
                    "error_distribution"
                ],
            },
            "mod_summary": self.simulation.symbolic_structure.get_mod_summary(),
        }

        # Save to file
        results_file = (
            self.project_root / "simulation" / "controlled_random_results.json"
        )
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"📊 Results saved to: {results_file}")

    def _run_balance_analysis(self):
        """Run analysis of balance changes and their effects"""
        print("  📈 Analyzing MOD modifications...")

        # List active modifications
        active_mods = self.simulation.symbolic_structure.list_active_modifications()

        if active_mods:
            print(
                f"  🔧 Active MODs: {sum(len(mods) for mods in active_mods.values())}"
            )
        else:
            print("  📋 No active MODs found")

    def run_quick_test(self, tester_count: int = 50, duration_minutes: int = 10):
        """Run a quick test with fewer testers and shorter duration"""
        print("⚡ Running Quick Controlled Random Test")
        return self.run_full_simulation(
            tester_count=tester_count,
            duration_minutes=duration_minutes,
            enable_symbolic_structure=True,
            enable_balance_testing=False,
        )

    def apply_modification(
        self,
        file_path: str,
        variable_name: str,
        new_value: Any,
        description: str = "",
        category: str = "general",
    ) -> bool:
        """Apply a MOD modification to override a specific variable"""
        print(f"🔧 Applying MOD: {variable_name} = {new_value} in {file_path}")

        success = self.simulation.symbolic_structure.apply_balance_modification(
            file_path, variable_name, new_value, description, category
        )

        if success:
            print(f"✅ MOD applied successfully")
            return True
        else:
            print(f"❌ Failed to apply MOD")
            return False

    def test_modification(
        self,
        file_path: str,
        variable_name: str,
        new_value: Any,
        description: str = "",
        category: str = "general",
    ) -> bool:
        """Test a specific MOD modification"""
        print(f"🧪 Testing MOD modification: {variable_name} = {new_value}")

        # Apply the modification
        success = self.apply_modification(
            file_path, variable_name, new_value, description, category
        )

        if success:
            print(f"✅ MOD applied, running quick test...")

            # Run a quick simulation to test the changes
            return self.run_quick_test(tester_count=25, duration_minutes=5)
        else:
            print(f"❌ Failed to apply MOD for testing")
            return False

    def commit_successful_modifications(self, target_file: str):
        """Commit successful MOD modifications to real game files"""
        print(f"💾 Committing MOD modifications for {target_file}")

        success = self.simulation.symbolic_structure.commit_successful_modifications(
            target_file
        )

        if success:
            print(f"✅ Successfully committed MODs to {target_file}")
        else:
            print(f"❌ Failed to commit MODs to {target_file}")

        return success

    def revert_modification(self, file_path: str, variable_name: str):
        """Revert a specific MOD modification"""
        print(f"🔄 Reverting MOD: {variable_name} in {file_path}")

        success = self.simulation.symbolic_structure.revert_modification(
            file_path, variable_name
        )

        if success:
            print(f"✅ Successfully reverted MOD for {variable_name}")
        else:
            print(f"❌ Failed to revert MOD for {variable_name}")

        return success

    def list_modifications(self):
        """List all active MOD modifications"""
        return self.simulation.symbolic_structure.list_active_modifications()


def main():
    """Main function for controlled random simulation"""
    parser = argparse.ArgumentParser(
        description="Controlled Random Simulation Runner (MOD System)"
    )
    parser.add_argument(
        "--mode",
        choices=["full", "quick", "mod", "test-mod", "commit", "revert", "list"],
        default="quick",
        help="Simulation mode",
    )
    parser.add_argument(
        "--testers", type=int, default=100, help="Number of testers to generate"
    )
    parser.add_argument(
        "--duration", type=int, default=30, help="Simulation duration in minutes"
    )
    parser.add_argument("--file", type=str, help="Target file for MOD operations")
    parser.add_argument("--variable", type=str, help="Variable name for MOD operations")
    parser.add_argument("--value", type=str, help="New value for MOD operations")
    parser.add_argument(
        "--description", type=str, default="", help="Description for MOD modification"
    )
    parser.add_argument(
        "--category", type=str, default="general", help="Category for MOD modification"
    )

    args = parser.parse_args()

    runner = ControlledRandomSimulationRunner()

    if args.mode == "full":
        success = runner.run_full_simulation(
            tester_count=args.testers, duration_minutes=args.duration
        )
    elif args.mode == "quick":
        success = runner.run_quick_test(
            tester_count=min(args.testers, 50), duration_minutes=min(args.duration, 10)
        )
    elif args.mode == "mod":
        if not all([args.file, args.variable, args.value]):
            print("❌ File, variable, and value required for MOD mode")
            return

        # Try to convert value to appropriate type
        try:
            if args.value.lower() in ["true", "false"]:
                value = args.value.lower() == "true"
            elif args.value.isdigit():
                value = int(args.value)
            elif args.value.replace(".", "").isdigit():
                value = float(args.value)
            else:
                value = args.value
        except:
            value = args.value

        success = runner.apply_modification(
            args.file, args.variable, value, args.description, args.category
        )
    elif args.mode == "test-mod":
        if not all([args.file, args.variable, args.value]):
            print("❌ File, variable, and value required for test-mod mode")
            return

        # Try to convert value to appropriate type
        try:
            if args.value.lower() in ["true", "false"]:
                value = args.value.lower() == "true"
            elif args.value.isdigit():
                value = int(args.value)
            elif args.value.replace(".", "").isdigit():
                value = float(args.value)
            else:
                value = args.value
        except:
            value = args.value

        success = runner.test_modification(
            args.file, args.variable, value, args.description, args.category
        )
    elif args.mode == "commit":
        if not args.file:
            print("❌ File required for commit mode")
            return

        success = runner.commit_successful_modifications(args.file)
    elif args.mode == "revert":
        if not all([args.file, args.variable]):
            print("❌ File and variable required for revert mode")
            return

        success = runner.revert_modification(args.file, args.variable)
    elif args.mode == "list":
        runner.list_modifications()
        success = True
    else:
        print("❌ Invalid mode specified")
        return

    if success:
        print("\n🎉 Operation completed successfully!")
    else:
        print("\n❌ Operation failed. Check the logs for details.")


if __name__ == "__main__":
    main()
