#!/usr/bin/env python3
"""
Advanced Simulation Runner for Simulacra Rancher
Integrates all advanced features for comprehensive testing
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our advanced features
from advanced_simulation_features import (
    AdvancedUserSimulator,
    SimulationAnalytics,
    SimulationVisualizer,
    SimulationStressTester,
)

# Import the main simulation
from discord_game_simulation import DiscordGameSimulation


class AdvancedSimulationRunner:
    """Advanced simulation runner with comprehensive features"""

    def __init__(self):
        self.user_simulator = AdvancedUserSimulator()
        self.analytics = SimulationAnalytics()
        self.visualizer = SimulationVisualizer()
        self.stress_tester = SimulationStressTester()
        self.simulation = None
        self.results = {}

    def run_comprehensive_simulation(
        self,
        duration_minutes: int = 30,
        num_users: int = 10,
        enable_advanced_features: bool = True,
        enable_analytics: bool = True,
        enable_visualization: bool = True,
        stress_test_scenarios: List[str] = None,
    ):
        """Run a comprehensive simulation with all advanced features"""

        print("🚀 Starting Advanced Simulation")
        print("=" * 50)

        # Initialize the main simulation
        self.simulation = DiscordGameSimulation()

        # Create advanced user profiles if enabled
        if enable_advanced_features:
            print("👥 Creating advanced user behavior profiles...")
            self._create_advanced_user_profiles(num_users)

        # Run the main simulation
        print(
            f"🎮 Running simulation for {duration_minutes} minutes with {num_users} users..."
        )
        start_time = time.time()

        try:
            self.simulation.run_simulation(duration_minutes, num_users)
            simulation_time = time.time() - start_time
            print(f"✅ Simulation completed in {simulation_time:.2f} seconds")

        except Exception as e:
            print(f"❌ Simulation failed: {e}")
            return False

        # Run analytics if enabled
        if enable_analytics:
            print("📊 Running advanced analytics...")
            self._run_analytics()

        # Create visualizations if enabled
        if enable_visualization:
            print("📈 Creating visualizations...")
            self._create_visualizations()

        # Run stress tests if specified
        if stress_test_scenarios:
            print("🧪 Running stress tests...")
            self._run_stress_tests(stress_test_scenarios)

        print("🎉 Advanced simulation completed!")
        return True

    def _create_advanced_user_profiles(self, num_users: int):
        """Create advanced user behavior profiles"""
        usernames = [
            "Alex",
            "Sam",
            "Jordan",
            "Taylor",
            "Morgan",
            "Casey",
            "Riley",
            "Quinn",
            "Avery",
            "Blake",
            "Cameron",
            "Drew",
            "Emery",
            "Finley",
            "Gray",
            "Hayden",
        ]

        for i in range(num_users):
            username = usernames[i % len(usernames)] + str(i + 1)
            user_id = f"user_{i + 1}"
            profile = self.user_simulator.create_behavior_profile(user_id, username)
            print(
                f"  Created profile for {username}: {profile.specialization} ({profile.activity_pattern})"
            )

    def _run_analytics(self):
        """Run comprehensive analytics on simulation results"""
        try:
            results_file = "simulation/discord_simulation_results.json"
            if os.path.exists(results_file):
                analysis = self.analytics.analyze_simulation_results(results_file)

                # Save analytics results
                analytics_file = "simulation/advanced_analytics_results.json"
                with open(analytics_file, "w") as f:
                    json.dump(analysis, f, indent=2)

                print(f"📊 Analytics saved to: {analytics_file}")

                # Print key insights
                self._print_analytics_summary(analysis)
            else:
                print("⚠️  No simulation results found for analytics")

        except Exception as e:
            print(f"❌ Analytics failed: {e}")

    def _print_analytics_summary(self, analysis: Dict):
        """Print key analytics insights"""
        print("\n📈 Key Insights:")
        print("-" * 30)

        summary = analysis.get("summary", {})
        print(f"📝 Total Messages: {summary.get('total_messages', 0)}")
        print(f"🤖 Bot Responses: {summary.get('bot_responses', 0)}")
        print(f"⚙️  Commands Processed: {summary.get('commands_processed', 0)}")
        print(f"❌ Errors: {summary.get('errors', 0)}")
        print(f"📊 Success Rate: {summary.get('success_rate', 0):.1%}")

        user_insights = analysis.get("user_insights", {})
        print(f"👥 Total Users: {user_insights.get('total_users', 0)}")
        print(f"✅ Active Users: {user_insights.get('active_users', 0)}")
        print(f"🎯 Most Active: {user_insights.get('most_active_user', 'None')}")

        performance = analysis.get("performance_metrics", {})
        print(f"⚡ System Stability: {performance.get('system_stability', 'unknown')}")

        recommendations = analysis.get("recommendations", [])
        if recommendations:
            print("\n💡 Recommendations:")
            for rec in recommendations:
                print(f"  • {rec}")

    def _create_visualizations(self):
        """Create visualizations of simulation results"""
        try:
            results_file = "simulation/discord_simulation_results.json"
            if os.path.exists(results_file):
                # Create activity chart
                self.visualizer.create_activity_chart(
                    results_file, "simulation/activity_timeline.png"
                )

                # Create command usage chart
                self.visualizer.create_command_usage_chart(
                    results_file, "simulation/command_usage.png"
                )

                print("📊 Visualizations saved to simulation/ folder")
            else:
                print("⚠️  No simulation results found for visualization")

        except Exception as e:
            print(f"❌ Visualization failed: {e}")

    def _run_stress_tests(self, scenarios: List[str]):
        """Run specified stress test scenarios"""
        if not self.simulation:
            print("❌ No simulation instance available for stress testing")
            return

        for scenario in scenarios:
            try:
                self.stress_tester.run_stress_test(
                    scenario, self.simulation, duration_minutes=5
                )
            except Exception as e:
                print(f"❌ Stress test '{scenario}' failed: {e}")

    def run_quick_test(self):
        """Run a quick 5-minute test with basic features"""
        print("⚡ Running Quick Test (5 minutes)")
        return self.run_comprehensive_simulation(
            duration_minutes=5,
            num_users=5,
            enable_advanced_features=True,
            enable_analytics=True,
            enable_visualization=True,
        )

    def run_full_test(self):
        """Run a full 30-minute test with all features"""
        print("🏃 Running Full Test (30 minutes)")
        return self.run_comprehensive_simulation(
            duration_minutes=30,
            num_users=10,
            enable_advanced_features=True,
            enable_analytics=True,
            enable_visualization=True,
            stress_test_scenarios=["high_concurrency", "rapid_commands"],
        )

    def run_stress_test_only(self, scenarios: List[str] = None):
        """Run only stress tests"""
        if not scenarios:
            scenarios = ["high_concurrency", "rapid_commands", "memory_pressure"]

        print(f"🧪 Running Stress Tests: {', '.join(scenarios)}")

        # Initialize simulation without running full simulation
        self.simulation = DiscordGameSimulation()

        for scenario in scenarios:
            try:
                self.stress_tester.run_stress_test(
                    scenario, self.simulation, duration_minutes=3
                )
            except Exception as e:
                print(f"❌ Stress test '{scenario}' failed: {e}")


def main():
    """Main function for advanced simulation runner"""
    parser = argparse.ArgumentParser(description="Advanced Simulation Runner")
    parser.add_argument(
        "--mode",
        choices=["quick", "full", "stress"],
        default="quick",
        help="Simulation mode",
    )
    parser.add_argument(
        "--duration", type=int, default=5, help="Simulation duration in minutes"
    )
    parser.add_argument("--users", type=int, default=5, help="Number of users")
    parser.add_argument("--no-analytics", action="store_true", help="Disable analytics")
    parser.add_argument(
        "--no-visualization", action="store_true", help="Disable visualization"
    )
    parser.add_argument(
        "--stress-scenarios", nargs="+", help="Stress test scenarios to run"
    )

    args = parser.parse_args()

    runner = AdvancedSimulationRunner()

    if args.mode == "quick":
        success = runner.run_quick_test()
    elif args.mode == "full":
        success = runner.run_full_test()
    elif args.mode == "stress":
        runner.run_stress_test_only(args.stress_scenarios)
        success = True
    else:
        # Custom mode
        success = runner.run_comprehensive_simulation(
            duration_minutes=args.duration,
            num_users=args.users,
            enable_analytics=not args.no_analytics,
            enable_visualization=not args.no_visualization,
            stress_test_scenarios=args.stress_scenarios,
        )

    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Check the logs for details.")


if __name__ == "__main__":
    main()
