#!/usr/bin/env python3
"""
Foundry Bot - Health Check
==========================

This is the main entry point for running system health checks.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for health checks"""
    print("🏥 Running Foundry Bot Health Check...")
    
    try:
        # Import and run the health checker
        from core.utils.system_health import SystemHealthChecker
        
        checker = SystemHealthChecker()
        results = checker.run_health_check()
        
        # Display results
        print("\n" + "="*50)
        print("📊 HEALTH CHECK RESULTS")
        print("="*50)
        
        for check_name, result in results["components"].items():
            status_icon = {"healthy": "✅", "warning": "⚠️", "error": "❌"}.get(result["status"], "❓")
            print(f"{check_name}: {status_icon} {result['status'].upper()}")
            if result.get("details"):
                print(f"  Details: {result['details']}")
        
        # Overall status
        overall_status = results["overall_status"]
        status_icon = {"healthy": "✅", "warning": "⚠️", "error": "❌"}.get(overall_status, "❓")
        print(f"\nOverall Status: {status_icon} {overall_status.upper()}")
        
        # Show recommendations if any
        if results.get("recommendations"):
            print(f"\n💡 Recommendations:")
            for rec in results["recommendations"]:
                print(f"  • {rec}")
        
    except Exception as e:
        print(f"❌ Error running health check: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 