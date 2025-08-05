#!/usr/bin/env python3
"""
Foundry Bot - Test Runner
=========================

This is the main entry point for running all tests.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for running tests"""
    print("🧪 Running Foundry Bot Tests...")
    
    try:
        # Import and run the test runner
        from core.tests.run_all_tests import TestRunner
        
        runner = TestRunner()
        results = runner.run_all_tests()
        
        # Generate and display report
        report = runner.generate_report(results)
        print("\n" + "="*50)
        print("📊 TEST RESULTS")
        print("="*50)
        print(report)
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 