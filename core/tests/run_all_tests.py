#!/usr/bin/env python3
"""
Comprehensive Test Runner for Authoring Bot
Runs all tests and provides detailed reports
"""

import sys
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime
import json

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestRunner:
    """Comprehensive test runner for all bot components"""

    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()

    def run_test(self, test_name: str, test_file: str) -> dict:
        """Run a single test and return results"""
        print(f"\nRunning {test_name}...")

        start_time = time.time()
        try:
            # Set up environment with proper Python path
            env = os.environ.copy()
            env["PYTHONPATH"] = str(project_root)

            result = subprocess.run(
                [sys.executable, test_file],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                env=env,
                cwd=project_root,
            )

            duration = time.time() - start_time
            success = result.returncode == 0

            return {
                "name": test_name,
                "file": test_file,
                "success": success,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                "name": test_name,
                "file": test_file,
                "success": False,
                "duration": duration,
                "stdout": "",
                "stderr": "Test timed out after 5 minutes",
                "returncode": -1,
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "name": test_name,
                "file": test_file,
                "success": False,
                "duration": duration,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
            }

    def run_all_tests(self):
        """Run all available tests"""
        print("Starting Comprehensive Test Suite")
        print("=" * 50)

        tests = [
            ("Model Connection", "core/tests/test_model_connection.py"),
            ("Writing Assistant", "core/tests/test_writing_assistant.py"),
            ("Personality Engine", "core/tests/test_personality.py"),
            ("Personalization", "core/tests/test_personalization.py"),
            ("Tool Use", "core/tests/test_tool_use.py"),
            ("Message Splitting", "core/tests/test_message_splitting.py"),
            ("Learning Engine", "core/tests/test_learning.py"),
            ("Authoring Bot", "core/tests/test_authoring_bot.py"),
        ]

        for test_name, test_file in tests:
            if os.path.exists(test_file):
                result = self.run_test(test_name, test_file)
                self.test_results[test_name] = result

                status = "PASS" if result["success"] else "FAIL"
                print(f"{status} {test_name} ({result['duration']:.2f}s)")
            else:
                print(f"SKIP {test_name} (file not found)")

    def generate_report(self):
        """Generate a comprehensive test report"""
        total_time = time.time() - self.start_time
        passed = sum(1 for r in self.test_results.values() if r["success"])
        failed = len(self.test_results) - passed

        print("\n" + "=" * 50)
        print("TEST SUMMARY REPORT")
        print("=" * 50)
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(
            f"Success Rate: {(passed/len(self.test_results)*100):.1f}%"
            if self.test_results
            else "0%"
        )
        print(f"Total Time: {total_time:.2f}s")

        if failed > 0:
            print("\nFAILED TESTS:")
            for name, result in self.test_results.items():
                if not result["success"]:
                    print(f"  - {name}: {result['stderr'][:100]}...")

        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": len(self.test_results),
                "passed": passed,
                "failed": failed,
                "success_rate": (
                    (passed / len(self.test_results) * 100) if self.test_results else 0
                ),
                "total_time": total_time,
            },
            "results": self.test_results,
        }

        report_file = "scripts/tests/test_report.json"
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)

        print(f"\nDetailed report saved to: {report_file}")

        return passed == len(self.test_results)


def main():
    """Main test runner"""
    runner = TestRunner()
    runner.run_all_tests()
    success = runner.generate_report()

    if success:
        print("\nAll tests passed! The bot is ready to use.")
        return 0
    else:
        print("\nSome tests failed. Please check the report for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
