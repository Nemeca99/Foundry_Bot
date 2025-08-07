#!/usr/bin/env python3
"""
Enhanced Configuration Management with Environment Variables and Setup Wizard
Eliminates manual config file editing and provides graceful fallbacks
"""

import os
import json
import getpass
from pathlib import Path


# Default settings
DEFAULT_SETTINGS = {
    "privacy": {
        "allow_memory_storage": True,
        "allow_analytics": True,
        "share_feedback_anonymously": False,
    },
    "notifications": {
        "enable_notifications": True,
        "notify_on_updates": True,
        "notify_on_features": True,
        "quiet_mode": False,
    },
    "interaction": {
        "response_length": "normal",
        "personality_mode": "balanced",
        "auto_respond": True,
        "use_emojis": True,
    },
    "memory": {
        "memory_retention_days": 30,
        "auto_cleanup_old_memories": True,
        "memory_priority": "normal",
    },
    "channels": {
        "preferred_channels": [],
        "ignore_channels": [],
        "auto_monitor_channels": True,
    },
    "custom": {"timezone": "UTC", "language": "en", "theme_preference": "auto"},
}


# Lyra Blackwall Phase 2 - Configuration


class Config:
    """
    Central configuration for Lyra Blackwall Phase 2.
    Contains all system, model, and runtime settings.
    """

    # Discord settings
    DISCORD_BOT_TOKEN = "your_token_here"
    TARGET_CHANNEL_ID = "channel_id_here"

    # Model endpoints
    CONTEXT_PROCESSOR_API_URL = "http://localhost:11434"
    CONTEXT_PROCESSOR_MODEL = "qwen/qwen3-8b"
    PERSONALITY_GENERATOR_API_URL = "http://localhost:1234"
    PERSONALITY_GENERATOR_MODEL = "qwen/qwen3-8b"

    # Memory system
    MEMORY_PATH = "data/user_memory"
    MAX_MEMORY_ITEMS = 1000

    # Council of Seven
    COUNCIL_VOTING_THRESHOLD = 0.6
    FRAGMENT_WEIGHT_DECAY = 0.95
    VP_OVERRIDE_THRESHOLD = 0.8

    # Linguistic processing
    NOUN_BOOST = 3.0
    VERB_BOOST = 2.5
    ADJECTIVE_BOOST = 2.0
    SWEAR_WORD_MULTIPLIER = 2.0
    DIRECT_REFERENCE_MULTIPLIER = 1.5
    IDIOM_BOOST = 2.0
    EXCLAMATION_MULTIPLIER = 1.1
    QUESTION_MULTIPLIER = 1.1

    # Black Hole Protocol
    BLACK_HOLE_ENABLED = False
    KNOWLEDGE_CONSUMPTION_LIMIT = 1000000
    ETHICAL_OVERRIDE_ENABLED = False

    # System
    LOG_LEVEL = "INFO"
    RESPONSE_DELAY = 7  # seconds


class BotConfig:
    """Enhanced configuration with environment variables and setup wizard"""

    def __init__(self):
        # Core Discord Configuration
        self.DISCORD_BOT_TOKEN = self._get_discord_token()
        self.COMMAND_PREFIX = os.getenv("LYRA_COMMAND_PREFIX", "!")
        self.TARGET_CHANNEL_ID = self._get_channel_id()

        # AI Configuration
        self.LM_STUDIO_URL = os.getenv("LYRA_LM_STUDIO_URL", "http://localhost:1234")
        self.OLLAMA_URL = os.getenv("LYRA_OLLAMA_URL", "http://localhost:11434")
        self.DEFAULT_MODEL = os.getenv("LYRA_DEFAULT_MODEL", "qwen/qwen3-8b")

        # System Configuration
        self.MAX_RESPONSE_LENGTH = int(os.getenv("LYRA_MAX_RESPONSE_LENGTH", "2000"))
        self.AI_TIMEOUT_SECONDS = int(os.getenv("LYRA_AI_TIMEOUT", "300"))
        self.HEARTBEAT_INTERVAL = int(os.getenv("LYRA_HEARTBEAT_INTERVAL", "600"))

        # File Paths
        self.DATA_DIR = Path(os.getenv("LYRA_DATA_DIR", "data"))
        self.MEMORY_DIR = Path(os.getenv("LYRA_MEMORY_DIR", "Core_Memory"))
        self.DISCORD_MEMORY_DIR = self.MEMORY_DIR / "discord_memory"
        self.USER_MEMORIES_DIR = self.MEMORY_DIR / "user_memories"
        self.LOGS_DIR = Path(os.getenv("LYRA_LOGS_DIR", "logs"))

        # Feature Flags
        self.ENABLE_QUANTUM_KITCHEN = (
            os.getenv("LYRA_ENABLE_QUANTUM", "true").lower() == "true"
        )
        self.ENABLE_MEMORY_SYSTEM = (
            os.getenv("LYRA_ENABLE_MEMORY", "true").lower() == "true"
        )
        self.ENABLE_ANALYTICS = (
            os.getenv("LYRA_ENABLE_ANALYTICS", "true").lower() == "true"
        )

        # Ensure directories exist
        self._create_directories()

        # Validate configuration
        self._validate_config()

    def _get_discord_token(self):
        """Get Discord token with fallback to setup wizard"""
        # Try environment variable first
        token = os.getenv("DISCORD_BOT_TOKEN")
        if token:
            return token

        # Try config file
        config_file = Path("config/config.json")
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    config_data = json.load(f)
                    token = config_data.get("discord_bot_token")
                    if token:
                        return token
            except Exception:
                pass

        # Setup wizard as last resort
        return self._setup_wizard()

    def _get_channel_id(self):
        """Get target channel ID from environment or config"""
        channel_id = os.getenv("LYRA_TARGET_CHANNEL_ID")
        if channel_id:
            return int(channel_id)

        # Try config file
        config_file = Path("config/config.json")
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    config_data = json.load(f)
                    channel_id = config_data.get("target_channel_id")
                    if channel_id:
                        return int(channel_id)
            except Exception:
                pass

        return None  # Optional - bot will work without specific channel

    def _setup_wizard(self):
        """Interactive setup wizard for first-time configuration"""
        print("🤖 Lyra Blackwall Alpha - First Time Setup")
        print("=" * 50)
        print("Welcome! Let's get your bot configured.")
        print("You can also set these as environment variables later.")
        print()

        # Get Discord token
        print("1. Discord Bot Token")
        print("   Get this from: https://discord.com/developers/applications")
        token = getpass.getpass("   Enter your Discord bot token: ").strip()

        # Get optional channel ID
        print("\n2. Target Channel ID (Optional)")
        print("   This is the channel where the bot will be most active.")
        channel_input = input("   Enter channel ID (or press Enter to skip): ").strip()
        channel_id = int(channel_input) if channel_input.isdigit() else None

        # Save to config file
        config_data = {
            "discord_bot_token": token,
            "target_channel_id": channel_id,
            "setup_completed": True,
        }

        config_file = Path("config/config.json")
        try:
            with open(config_file, "w") as f:
                json.dump(config_data, f, indent=2)
            print(f"\n✅ Configuration saved to {config_file}")
        except Exception as e:
            print(f"\n⚠️ Could not save config file: {e}")
            print("You can set environment variables instead:")
            print(f"   export DISCORD_BOT_TOKEN='{token}'")
            if channel_id:
                print(f"   export LYRA_TARGET_CHANNEL_ID='{channel_id}'")

        print("\n🚀 Setup complete! Starting bot...")
        return token

    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            self.DATA_DIR,
            self.MEMORY_DIR,
            self.DISCORD_MEMORY_DIR,
            self.USER_MEMORIES_DIR,
            self.LOGS_DIR,
            self.DATA_DIR / "analytics",
            self.DATA_DIR / "system_data",
            self.DATA_DIR / "user_data",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _validate_config(self):
        """Validate critical configuration"""
        # Skip validation if SKIP_CONFIG_VALIDATION is set
        if os.getenv('SKIP_CONFIG_VALIDATION') == '1':
            return
            
        if not self.DISCORD_BOT_TOKEN:
            raise ValueError("Discord bot token is required!")

        if len(self.DISCORD_BOT_TOKEN) < 50:
            raise ValueError("Discord bot token appears to be invalid (too short)")

    def get_env_status(self):
        """Get status of environment configuration"""
        status = {
            "discord_token_set": bool(os.getenv("DISCORD_BOT_TOKEN")),
            "channel_id_set": bool(os.getenv("LYRA_TARGET_CHANNEL_ID")),
            "lm_studio_url": self.LM_STUDIO_URL,
            "ollama_url": self.OLLAMA_URL,
            "data_directory": str(self.DATA_DIR),
            "features": {
                "quantum_kitchen": self.ENABLE_QUANTUM_KITCHEN,
                "memory_system": self.ENABLE_MEMORY_SYSTEM,
                "analytics": self.ENABLE_ANALYTICS,
            },
        }
        return status

    def print_config_help(self):
        """Print help for environment variable configuration"""
        print("🔧 Lyra Blackwall Alpha - Environment Variables")
        print("=" * 50)
        print("Required:")
        print("  DISCORD_BOT_TOKEN - Your Discord bot token")
        print()
        print("Optional:")
        print("  LYRA_TARGET_CHANNEL_ID - Specific channel for bot activity")
        print("  LYRA_COMMAND_PREFIX - Command prefix (default: !)")
        print("  LYRA_LM_STUDIO_URL - LM Studio URL (default: http://localhost:1234)")
        print("  LYRA_OLLAMA_URL - Ollama URL (default: http://localhost:11434)")
        print("  LYRA_DEFAULT_MODEL - Default AI model (default: qwen/qwen3-8b)")
        print("  LYRA_MAX_RESPONSE_LENGTH - Max response length (default: 2000)")
        print("  LYRA_AI_TIMEOUT - AI response timeout (default: 300)")
        print("  LYRA_HEARTBEAT_INTERVAL - Heartbeat interval (default: 600)")
        print("  LYRA_DATA_DIR - Data directory (default: data)")
        print("  LYRA_LOGS_DIR - Logs directory (default: logs)")
        print()
        print("Feature Flags (true/false):")
        print("  LYRA_ENABLE_QUANTUM - Enable quantum kitchen (default: true)")
        print("  LYRA_ENABLE_MEMORY - Enable memory system (default: true)")
        print("  LYRA_ENABLE_ANALYTICS - Enable analytics (default: true)")


# Backward compatibility
DISCORD_BOT_TOKEN = None
COMMAND_PREFIX = None

# Create global config instance
try:
    config = BotConfig()
    # Export for backward compatibility
    DISCORD_BOT_TOKEN = config.DISCORD_BOT_TOKEN
    COMMAND_PREFIX = config.COMMAND_PREFIX
except Exception as e:
    print(f"❌ Configuration error: {e}")
    print("Run with --help for configuration assistance")
    raise
