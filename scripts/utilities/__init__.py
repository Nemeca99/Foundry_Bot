"""
Lyra Blackwall Alpha - Core Systems Package
Main core systems for the Lyra AI platform
"""

__version__ = "0.3.0"
__author__ = "Travis Miner (Dev)"
__description__ = "Consolidated core systems for Lyra Blackwall Alpha AI platform"

from .bot import DiscordDigirancherBot as ConsolidatedDiscordBot
from .memory_system import ConsolidatedMemorySystem
from .personality_system import ConsolidatedPersonalitySystem
from .config import *

__all__ = [
    "ConsolidatedDiscordBot",
    "ConsolidatedMemorySystem",
    "ConsolidatedPersonalitySystem",
    "DISCORD_TOKEN",
    "COMMAND_PREFIX",
    "TARGET_CHANNEL_ID",
    "HEARTBEAT_INTERVAL",
    "MAX_RESPONSE_TIME",
]
