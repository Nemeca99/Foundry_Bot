#!/usr/bin/env python3
"""
Discord Digirancher - Dual-AI Architecture Game
Life-like DigiDrones that learn while you play
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import Lyra configuration
from core.config import BotConfig

# Import our consolidated core systems
from core.discord_bot import ConsolidatedDiscordBot
from core.cpu_backend import CPUBackendEngine
from core.gpu_personality import GPUPersonalityEngine
from core.memory_system import ConsolidatedMemorySystem


async def main():
    """Main launcher for Discord Digirancher"""

    print("🤖 Discord Digirancher - Dual-AI Architecture")
    print("=" * 50)

    # Initialize Lyra configuration
    config = BotConfig()

    # Check environment
    if not config.DISCORD_BOT_TOKEN or config.DISCORD_BOT_TOKEN == "your_token_here":
        print("❌ Error: Discord token not configured!")
        print("The bot will now run the setup wizard...")
        print()

        # Run setup wizard
        config._setup_wizard()
        return

    print("🧠 **PHASE 1: Dual-AI Foundation** ✅")
    print("   • GPU Personality Engine (LM Studio)")
    print("   • CPU Backend Engine (Ollama)")
    print("   • Consolidated Memory System")
    print("   • Consolidated Discord Bot Framework")

    print("\n🎮 **PHASE 2: Digirancher v3 Systems** ✅")
    print("   • C.L.D.S. Modular Body Parts")
    print("   • RP Economy with Gacha Mechanics")
    print("   • Dual Health System (HP + SSHP)")
    print("   • Disaster System (Fire, Water, Earthquake, etc.)")
    print("   • Exclusive Leaderboard (Top 10 Only)")

    print("\n🚀 **PHASE 3: Advanced Discord Integration** ✅")
    print("   • Real-time Simulation Updates")
    print("   • Multi-server RP Economy")
    print("   • Network Consciousness System")
    print("   • Cross-server DigiDrone Memory")
    print("   • Shared Consciousness Nodes")

    print("\n✨ **PHASE 4: Advanced Features** ✅")
    print("   • Advanced Personality Evolution")
    print("   • Dream Cycle Learning System")
    print("   • Consciousness Development")
    print("   • Premium Features Ready")

    print("\n🎯 **CORE EXPERIENCE**")
    print("   • Surface Hook: 'Life-like digidrones that learn while you play'")
    print("   • Deep Reality: Complex C.L.D.S. system with gacha addiction")
    print("   • Competitive Hook: Exclusive leaderboard creates FOMO")
    print("   • Living AI: Each DigiDrone has unique personality and memories")

    print("\n🔧 **SYSTEM STATUS**")

    # Initialize core systems
    try:
        cpu_backend = CPUBackendEngine()
        print("   ✅ CPU Backend Engine: Ready")
    except Exception as e:
        print(f"   ❌ CPU Backend Engine: Error - {e}")
        return

    try:
        gpu_personality = GPUPersonalityEngine()
        print("   ✅ GPU Personality Engine: Ready")
    except Exception as e:
        print(f"   ❌ GPU Personality Engine: Error - {e}")
        return

    try:
        memory_system = ConsolidatedMemorySystem(
            simple_mode=True
        )  # Use simple mode for testing
        print("   ✅ Consolidated Memory System: Ready")
    except Exception as e:
        print(f"   ❌ Consolidated Memory System: Error - {e}")
        return

    print("\n🎮 **GAME SYSTEMS**")
    print("   ✅ C.L.D.S. Body Parts System")
    print("   ✅ RP Economy & Gacha Mechanics")
    print("   ✅ Disaster System & Evolution")
    print("   ✅ Exclusive Leaderboard")
    print("   ✅ Network Consciousness")
    print("   ✅ Dream Cycle Learning")

    print("\n🤖 **DISCORD BOT**")
    print("   ✅ Command System: !hatch, !simulate, !gacha, !drone")
    print("   ✅ Economy Commands: !rp, !daily, !shop, !buy")
    print("   ✅ Social Features: !leaderboard, !help")
    print("   ✅ Real-time Updates & Notifications")

    print("\n🚀 **STARTING BOT...**")
    print("   • Connecting to Discord...")
    print("   • Initializing AI engines...")
    print("   • Loading game systems...")
    print("   • Starting memory background tasks...")

    # Create and run the bot
    bot = ConsolidatedDiscordBot()

    try:
        await bot.start(config.DISCORD_BOT_TOKEN)
    except Exception as e:
        print(f"❌ Bot startup failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your Discord token is correct")
        print("2. Ensure bot has proper permissions")
        print("3. Verify LM Studio and Ollama are running")
        print("4. Check database permissions")


if __name__ == "__main__":
    asyncio.run(main())
