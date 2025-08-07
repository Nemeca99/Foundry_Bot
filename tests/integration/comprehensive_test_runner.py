#!/usr/bin/env python3
"""
Comprehensive Test Runner for Sim-Rancher Live Mod System
Demonstrates all features with fancy output and detailed results
"""

import sys
import os
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ComprehensiveTestRunner:
    """Comprehensive test runner with fancy output"""

    def __init__(self):
        self.test_results = {}
        self.start_time = datetime.now()

    def print_header(self):
        """Print fancy header"""
        print("\n" + "=" * 80)
        print("🎮 SIM-RANCHER LIVE MOD SYSTEM - COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        print("🚀 Testing all systems and features")
        print("🔧 Mod System, Economy, Global Multiplier, Analytics")
        print("=" * 80)

    def print_section(self, title: str):
        """Print section header"""
        print(f"\n{'='*20} {title} {'='*20}")

    def run_test(
        self, test_name: str, command: str, description: str
    ) -> Dict[str, Any]:
        """Run a test and return results"""
        print(f"\n🧪 Running: {test_name}")
        print(f"📝 {description}")
        print("-" * 60)

        start_time = time.time()

        try:
            result = subprocess.run(
                ["python", command],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            duration = time.time() - start_time

            if result.returncode == 0:
                status = "✅ PASSED"
                print(f"✅ {test_name} completed successfully!")
            else:
                status = "❌ FAILED"
                print(f"❌ {test_name} failed!")
                print(f"Error: {result.stderr}")

            return {
                "name": test_name,
                "status": status,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

        except subprocess.TimeoutExpired:
            return {
                "name": test_name,
                "status": "⏰ TIMEOUT",
                "duration": 300,
                "stdout": "",
                "stderr": "Test timed out after 5 minutes",
                "returncode": -1,
            }
        except Exception as e:
            return {
                "name": test_name,
                "status": "💥 ERROR",
                "duration": time.time() - start_time,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
            }

    def run_all_tests(self):
        """Run all comprehensive tests"""
        self.print_header()

        tests = [
            {
                "name": "🔧 Standalone Mod System Test",
                "command": "standalone_mod_test.py",
                "description": "Tests mod creation, activation, and global multiplier",
            },
            {
                "name": "🎮 Discord Game Simulation",
                "command": "discord_game_simulation.py",
                "description": "Full Discord bot simulation with all systems",
            },
            {
                "name": "⚖️ Controlled Random Simulation",
                "command": "controlled_random_simulation.py --mode quick",
                "description": "Realistic human behavior with MOD system",
            },
        ]

        print(f"\n📊 Running {len(tests)} comprehensive tests...")

        for test in tests:
            result = self.run_test(test["name"], test["command"], test["description"])
            self.test_results[test["name"]] = result

            # Small delay between tests
            time.sleep(1)

        self.print_final_results()

    def print_final_results(self):
        """Print comprehensive final results"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 80)

        total_tests = len(self.test_results)
        passed_tests = len(
            [r for r in self.test_results.values() if "PASSED" in r["status"]]
        )
        failed_tests = total_tests - passed_tests

        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        total_duration = sum(r["duration"] for r in self.test_results.values())
        print(f"⏱️  Total Duration: {total_duration:.2f} seconds")

        print("\n" + "=" * 80)
        print("🎯 DETAILED RESULTS")
        print("=" * 80)

        for test_name, result in self.test_results.items():
            print(f"\n{result['status']} {test_name}")
            print(f"   Duration: {result['duration']:.2f}s")
            if result["stderr"]:
                print(f"   Error: {result['stderr'][:100]}...")

        # Save results
        self.save_results()

        print("\n" + "=" * 80)
        print("🎉 COMPREHENSIVE TEST SUITE COMPLETE!")
        print("=" * 80)

        if failed_tests == 0:
            print("🚀 ALL SYSTEMS OPERATIONAL!")
            print("🔧 Mod system fully functional")
            print("💰 Economy integration working")
            print("🌍 Global multiplier active")
            print("📊 Analytics and visualization ready")
        else:
            print(f"⚠️  {failed_tests} test(s) failed. Check the results for details.")

        print("=" * 80)

    def save_results(self):
        """Save test results to file"""
        results_file = "comprehensive_test_results.json"

        results_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": len(self.test_results),
                "passed_tests": len(
                    [r for r in self.test_results.values() if "PASSED" in r["status"]]
                ),
                "failed_tests": len(
                    [
                        r
                        for r in self.test_results.values()
                        if "PASSED" not in r["status"]
                    ]
                ),
                "total_duration": sum(
                    r["duration"] for r in self.test_results.values()
                ),
            },
            "test_results": self.test_results,
        }

        with open(results_file, "w") as f:
            json.dump(results_data, f, indent=2)

        print(f"\n📊 Results saved to: {results_file}")

    def show_system_status(self):
        """Show current system status"""
        print("\n🔧 SYSTEM STATUS CHECK")
        print("-" * 40)

        # Check if key files exist
        files_to_check = [
            "standalone_mod_test.py",
            "discord_game_simulation.py",
            "controlled_random_simulation.py",
            "fancy_startup.py",
            "README.md",
        ]

        for file in files_to_check:
            if os.path.exists(file):
                print(f"✅ {file}")
            else:
                print(f"❌ {file} (missing)")

        # Check if data directory exists
        if os.path.exists("../data"):
            print("✅ data/ directory")
        else:
            print("❌ data/ directory (missing)")

        print("-" * 40)


def main():
    """Main function"""
    runner = ComprehensiveTestRunner()

    # Show system status first
    runner.show_system_status()

    # Run all tests
    runner.run_all_tests()


if __name__ == "__main__":
    main()
