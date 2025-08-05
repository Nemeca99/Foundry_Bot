#!/usr/bin/env python3
"""
Setup script for Authoring Bot
Helps configure Discord token and channel settings
"""

import os
from pathlib import Path


def setup_bot():
    """Interactive setup for the Authoring Bot"""
    print("🤖 Authoring Bot Setup")
    print("=" * 40)

    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Found existing .env file")
        response = (
            input("Do you want to update the configuration? (y/N): ").strip().lower()
        )
        if response not in ["y", "yes"]:
            print("Setup cancelled.")
            return
    else:
        print("📝 Creating new .env file...")

    # Get Discord token
    print("\n🔑 Discord Bot Token")
    print("Get your bot token from: https://discord.com/developers/applications")
    print("1. Go to Discord Developer Portal")
    print("2. Create a new application or select existing")
    print("3. Go to 'Bot' section")
    print("4. Copy the token")

    discord_token = input("\nEnter your Discord bot token: ").strip()
    if not discord_token:
        print("❌ Discord token is required!")
        return

    # Get user ID
    print("\n👤 Your Discord User ID")
    print("To get your user ID:")
    print("1. Enable Developer Mode in Discord (User Settings > Advanced)")
    print("2. Right-click your username and select 'Copy ID'")

    user_id = input("Enter your Discord user ID: ").strip()
    if not user_id:
        print("❌ User ID is required!")
        return

    # Get channel ID
    print("\n📺 Discord Channel ID")
    print("To get channel ID:")
    print("1. Enable Developer Mode in Discord")
    print("2. Right-click the channel and select 'Copy ID'")

    channel_id = input("Enter the channel ID where the bot should respond: ").strip()
    if not channel_id:
        print("❌ Channel ID is required!")
        return

    # Create .env file
    env_content = f"""# Authoring Bot Configuration
# Discord Settings
DISCORD_TOKEN={discord_token}
ALLOWED_USERS={user_id}
ALLOWED_CHANNELS={channel_id}
BOT_PREFIX=!

# LM Studio Settings
OLLAMA_BASE_URL=http://169.254.83.107:1234
OLLAMA_MODEL_NAME=qwen/qwen3-8b

# Text Generation Settings
MAX_TOKENS=1024
TEMPERATURE=0.85
TOP_P=0.92
TOP_K=50
REPEAT_PENALTY=1.15
REQUEST_TIMEOUT=600

# Learning Engine Settings
CHUNK_SIZE=1000
OVERLAP_SIZE=200
MAX_WORKERS=4
"""

    with open(".env", "w") as f:
        f.write(env_content)

    print("\n✅ Configuration saved to .env file!")
    print("\n📋 Next Steps:")
    print("1. Make sure your Discord bot is online")
    print("2. Invite the bot to your server with proper permissions")
    print("3. Test the bot with: python test_model_connection.py")
    print("4. Start the bot with: python start_authoring_bot.py")

    # Test configuration
    print("\n🧪 Testing configuration...")
    try:
        from config import Config

        Config.print_config()
        errors = Config.validate()
        if errors:
            print("\n❌ Configuration Errors:")
            for error in errors:
                print(f"   {error}")
        else:
            print("\n✅ Configuration is valid!")
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")


if __name__ == "__main__":
    setup_bot()
