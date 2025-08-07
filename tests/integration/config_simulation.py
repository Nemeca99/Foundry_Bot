#!/usr/bin/env python3
"""
Simulation Configuration
Easy way to customize simulation parameters
"""

# Simulation Settings
SIMULATION_DURATION_MINUTES = 30
NUM_USERS = 10

# User Behavior Settings
USER_ACTIVITY_CHANCE = 0.7  # 70% chance of activity per user per cycle
SPECIAL_EVENT_CHANCE = 0.1  # 10% chance of special events
CHAT_MESSAGE_CHANCE = 0.3   # 30% chance of random chat messages

# Activity Distribution
ACTIVITIES_PER_USER = (1, 3)  # Random range of activities per user
DELAY_BETWEEN_ACTIVITIES = (0.1, 0.5)  # Random delay range in seconds

# Discord Server Settings
DISCORD_CHANNELS = [
    {"name": "general", "topic": "General discussion"},
    {"name": "commands", "topic": "Bot commands"},
    {"name": "trading", "topic": "Trade offers"},
    {"name": "hunting", "topic": "Hunting results"},
    {"name": "crafting", "topic": "Crafting discussion"},
    {"name": "chat", "topic": "AI chat"},
    {"name": "announcements", "topic": "Server announcements"},
]

# Chat Messages for Realistic Behavior
CHAT_MESSAGES = [
    "How's everyone doing?",
    "Anyone want to trade?",
    "Great hunt today!",
    "The AI is getting smarter...",
    "Anyone else notice the patterns?",
    "This game is addictive!",
    "What's your favorite activity?",
    "The kingdom system is interesting",
    "Anyone else having fun?",
    "The memories are fascinating",
    "The resource gathering is getting intense",
    "I love the personality system",
    "The trading economy is fascinating",
    "Anyone else notice the AI responses?",
    "The hunting mechanics are brilliant",
]

# Special Events
SPECIAL_EVENTS = [
    "!chat The AI seems to be evolving...",
    "!chat I think I found a pattern in the memories",
    "!chat The kingdom politics are getting intense",
    "!chat Anyone else notice the resource patterns?",
    "!chat The hunting system is brilliant",
    "!chat I love how the personality system works",
    "!chat The trading economy is fascinating",
    "!chat The crafting recipes are getting complex",
    "!chat The AI responses are getting more sophisticated",
    "!chat I wonder what the future holds for us",
]

# Game Commands to Test
GAME_COMMANDS = [
    "!daily",
    "!gather", 
    "!hunt",
    "!chat Hello there!",
    "!profile",
    "!personality",
    "!craft stone_pickaxe",
    "!trade stone 5 10",
    "!leaderboard",
    "!kingdom",
    "!memory",
    "!status",
    "!ping",
    "!help",
]

# LLM Settings
LLM_TIMEOUT_SECONDS = 300  # 5 minutes
LLM_FALLBACK_RESPONSES = [
    "That's an interesting perspective!",
    "I've been thinking about that too.",
    "The patterns in this world are fascinating.",
    "Have you noticed the recent changes?",
    "The memories are becoming more complex.",
    "I wonder what the future holds for us.",
    "The kingdom politics are getting intense.",
    "The resource distribution is quite dynamic.",
]

# Output Settings
SAVE_RESULTS = True
PRINT_PROGRESS = True
PRINT_DETAILED_LOGS = False  # Set to True for verbose output 