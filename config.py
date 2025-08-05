#!/usr/bin/env python3
"""
Configuration file for Authoring Bot
Set your Discord token and channel settings here
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Configuration settings for the Authoring Bot"""

    # Discord Bot Settings
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
    BOT_PREFIX = os.getenv("BOT_PREFIX", "!")

    # Allowed Users (Discord User IDs)
    # Add your Discord user ID here
    ALLOWED_USERS = os.getenv("ALLOWED_USERS", "141323625503522816").split(",")

    # Allowed Channels (Discord Channel IDs)
    # Add the channel IDs where the bot should respond
    ALLOWED_CHANNELS = os.getenv("ALLOWED_CHANNELS", "1400339350692171896").split(",")

    # LM Studio Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://169.254.83.107:1234")
    OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "qwen/qwen3-8b")

    # Text Generation Settings
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.85"))
    TOP_P = float(os.getenv("TOP_P", "0.92"))
    TOP_K = int(os.getenv("TOP_K", "50"))
    REPEAT_PENALTY = float(os.getenv("REPEAT_PENALTY", "1.15"))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "600"))  # 10 minutes timeout

    # Learning Engine Settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    OVERLAP_SIZE = int(os.getenv("OVERLAP_SIZE", "200"))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

    # Data Paths
    DATA_DIR = Path(__file__).parent / "data"
    MODELS_DIR = Path(__file__).parent / "models"
    TRAINING_DATA_DIR = MODELS_DIR / "training_data"

    # Wikipedia and Book Collection Paths
    WIKIPEDIA_PATH = Path("D:/wikipedia_deduplicated")
    BOOK_COLLECTION_PATH = Path(__file__).parent / "Book_Collection"

    # Output Directories
    IMAGE_OUTPUT_DIR = Path(__file__).parent / "image" / "output"
    VIDEO_OUTPUT_DIR = Path(__file__).parent / "video" / "output"
    VOICE_OUTPUT_DIR = Path(__file__).parent / "voice" / "output"

    @classmethod
    def validate(cls):
        """Validate configuration settings"""
        errors = []

        # Check Discord token
        if not cls.DISCORD_TOKEN:
            errors.append(
                "❌ DISCORD_TOKEN is not set. Please add your Discord bot token to config.py or .env file"
            )

        # Check allowed users
        if not cls.ALLOWED_USERS or cls.ALLOWED_USERS == [""]:
            errors.append(
                "❌ ALLOWED_USERS is not set. Please add your Discord user ID to config.py or .env file"
            )

        # Check allowed channels
        if not cls.ALLOWED_CHANNELS or cls.ALLOWED_CHANNELS == [""]:
            errors.append(
                "❌ ALLOWED_CHANNELS is not set. Please add your Discord channel ID to config.py or .env file"
            )

        # Check LM Studio connection
        if not cls.OLLAMA_BASE_URL:
            errors.append("❌ OLLAMA_BASE_URL is not set")

        # Check data paths
        if not cls.DATA_DIR.exists():
            cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

        if not cls.MODELS_DIR.exists():
            cls.MODELS_DIR.mkdir(parents=True, exist_ok=True)

        if not cls.TRAINING_DATA_DIR.exists():
            cls.TRAINING_DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Check Wikipedia path
        if not cls.WIKIPEDIA_PATH.exists():
            errors.append(f"⚠️  Wikipedia path not found: {cls.WIKIPEDIA_PATH}")

        # Check Book Collection path
        if not cls.BOOK_COLLECTION_PATH.exists():
            errors.append(
                f"⚠️  Book Collection path not found: {cls.BOOK_COLLECTION_PATH}"
            )

        return errors

    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("🔧 Authoring Bot Configuration")
        print("=" * 40)
        print(f"🤖 Discord Token: {'✅ Set' if cls.DISCORD_TOKEN else '❌ Not Set'}")
        print(f"📝 Bot Prefix: {cls.BOT_PREFIX}")
        print(f"👥 Allowed Users: {len(cls.ALLOWED_USERS)} users")
        print(f"📺 Allowed Channels: {len(cls.ALLOWED_CHANNELS)} channels")
        print(f"🧠 LM Studio URL: {cls.OLLAMA_BASE_URL}")
        print(f"🤖 Model: {cls.OLLAMA_MODEL_NAME}")
        print(f"📊 Max Tokens: {cls.MAX_TOKENS}")
        print(f"🌡️  Temperature: {cls.TEMPERATURE}")
        print(
            f"📚 Wikipedia Path: {'✅ Found' if cls.WIKIPEDIA_PATH.exists() else '❌ Not Found'}"
        )
        print(
            f"📖 Book Collection: {'✅ Found' if cls.BOOK_COLLECTION_PATH.exists() else '❌ Not Found'}"
        )
        print(f"💾 Data Directory: {cls.DATA_DIR}")
        print(f"🧠 Training Data: {cls.TRAINING_DATA_DIR}")


# Configuration validation
if __name__ == "__main__":
    Config.print_config()
    errors = Config.validate()
    if errors:
        print("\n❌ Configuration Errors:")
        for error in errors:
            print(f"   {error}")
    else:
        print("\n✅ Configuration is valid!")
