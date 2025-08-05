#!/usr/bin/env python3
"""
Foundry Bot - Setup
===================

This is the main entry point for setting up the bot.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for setup"""
    print("🔧 Setting up Foundry Bot...")
    
    try:
        # Import and run the setup
        from core.setup.setup_bot import main as run_setup
        run_setup()
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 