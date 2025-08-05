#!/usr/bin/env python3
"""
Foundry Bot - Main Entry Point
==============================

This is the main entry point for starting the Discord bot.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for the bot"""
    print("🤖 Starting Foundry Bot...")
    
    try:
        # Import and start the Discord bot
        from discord.authoring_bot import main as start_discord_bot
        start_discord_bot()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 