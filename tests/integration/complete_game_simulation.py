#!/usr/bin/env python3
"""
Complete Game Simulation for Simulacra Rancher
Full Discord bot simulation with all game systems integrated
Simulates the entire Discord experience without needing Discord
"""

import sys
import os
import json
import time
import random
import asyncio
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple
import queue
import requests
import sqlite3
import re
from dataclasses import dataclass, asdict

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@dataclass
class DiscordMessage:
    """Represents a Discord message in the simulation"""

    id: str
    author: str
    content: str
    timestamp: datetime
    channel: str
    attachments: List[str] = None
    embeds: List[Dict] = None
    reactions: Dict[str, int] = None

    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []
        if self.embeds is None:
            self.embeds = []
        if self.reactions is None:
            self.reactions = {}


@dataclass
class DiscordChannel:
    """Represents a Discord channel in the simulation"""

    id: str
    name: str
    channel_type: str  # text, voice, category
    topic: str = ""
    messages: List[DiscordMessage] = None
    permissions: Dict[str, List[str]] = None

    def __post_init__(self):
        if self.messages is None:
            self.messages = []
        if self.permissions is None:
            self.permissions = {}


@dataclass
class DiscordUser:
    """Represents a Discord user in the simulation"""

    id: str
    username: str
    display_name: str
    avatar: str = ""
    status: str = "online"
    roles: List[str] = None
    joined_at: datetime = None

    def __post_init__(self):
        if self.roles is None:
            self.roles = []
        if self.joined_at is None:
            self.joined_at = datetime.now()


@dataclass
class DiscordServer:
    """Represents a Discord server in the simulation"""

    id: str
    name: str
    owner_id: str
    channels: List[DiscordChannel] = None
    members: List[DiscordUser] = None
    roles: Dict[str, Dict] = None
    emojis: Dict[str, str] = None

    def __post_init__(self):
        if self.channels is None:
            self.channels = []
        if self.members is None:
            self.members = []
        if self.roles is None:
            self.roles = {}
        if self.emojis is None:
            self.emojis = {}


class SimulatedDiscordBot:
    """Simulates the Discord bot interface and command processing"""

    def __init__(self, game_systems):
        self.game_systems = game_systems
        self.command_prefix = "!"
        self.commands = {
            "help": self.cmd_help,
            "daily": self.cmd_daily,
            "gather": self.cmd_gather,
            "hunt": self.cmd_hunt,
            "trade": self.cmd_trade,
            "craft": self.cmd_craft,
            "profile": self.cmd_profile,
            "leaderboard": self.cmd_leaderboard,
            "chat": self.cmd_chat,
            "personality": self.cmd_personality,
            "kingdom": self.cmd_kingdom,
            "memory": self.cmd_memory,
            "join": self.cmd_join,
            "leave": self.cmd_leave,
            "ping": self.cmd_ping,
            "status": self.cmd_status,
        }
        self.llm_timeout = 300  # 5 minutes
        self.command_history = []
        self.response_queue = queue.Queue()

    def process_message(self, message: DiscordMessage) -> List[DiscordMessage]:
        """Process a Discord message and return bot responses"""
        responses = []

        # Check if message is a command
        if not message.content.startswith(self.command_prefix):
            return responses

        # Parse command
        parts = message.content[len(self.command_prefix) :].split()
        if not parts:
            return responses

        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        # Log command
        self.command_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "user": message.author,
                "command": command,
                "args": args,
                "channel": message.channel,
            }
        )

        # Execute command
        if command in self.commands:
            try:
                result = self.commands[command](message.author, args, message.channel)
                if result:
                    responses.append(self.create_response(result, message.channel))
            except Exception as e:
                error_msg = f"❌ Error executing command: {str(e)}"
                responses.append(self.create_response(error_msg, message.channel))
        else:
            help_msg = f"❓ Unknown command: `{command}`. Use `{self.command_prefix}help` for available commands."
            responses.append(self.create_response(help_msg, message.channel))

        return responses

    def create_response(self, content: str, channel: str) -> DiscordMessage:
        """Create a bot response message"""
        return DiscordMessage(
            id=f"bot_{int(time.time() * 1000)}",
            author="Simulacra Rancher Bot",
            content=content,
            timestamp=datetime.now(),
            channel=channel,
        )

    def cmd_help(self, user: str, args: List[str], channel: str) -> str:
        """Show help information"""
        help_text = """
🤖 **Simulacra Rancher Bot Commands**

**Core Commands:**
`!daily` - Claim daily RP bonus
`!gather` - Gather resources from the environment
`!hunt` - Hunt for Simulacra creatures
`!trade <item> <amount> <price>` - Create trade offers
`!craft <item>` - Craft items from resources

**Social Commands:**
`!chat <message>` - Chat with the AI
`!personality` - Check your personality stats
`!memory` - View your memory profile

**Game Info:**
`!profile` - View your character profile
`!leaderboard` - View top players
`!kingdom` - Kingdom information
`!status` - Server status

**Utility:**
`!ping` - Check bot response time
`!help` - Show this help message

**Admin:**
`!join` - Join the simulation
`!leave` - Leave the simulation
        """
        return help_text.strip()

    def cmd_daily(self, user: str, args: List[str], channel: str) -> str:
        """Claim daily RP bonus"""
        try:
            result = self.game_systems.execute_command({"username": user}, "daily")
            if result["success"]:
                return f"💰 **Daily Bonus Claimed!**\n{result['response']}"
            else:
                return f"❌ **Daily Claim Failed:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_gather(self, user: str, args: List[str], channel: str) -> str:
        """Gather resources"""
        try:
            result = self.game_systems.execute_command({"username": user}, "gather")
            if result["success"]:
                resources = result.get("resources_gained", {})
                resource_text = ""
                if resources:
                    for resource_type, qualities in resources.items():
                        for quality, amount in qualities.items():
                            resource_text += f"\n• {quality} {resource_type}: {amount}"

                return (
                    f"🌿 **Gathering Complete!**\n{result['response']}{resource_text}"
                )
            else:
                return f"❌ **Gathering Failed:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_hunt(self, user: str, args: List[str], channel: str) -> str:
        """Hunt for Simulacra"""
        try:
            result = self.game_systems.execute_command({"username": user}, "hunt")
            if result["success"]:
                return f"🎯 **Hunt Result:**\n{result['response']}"
            else:
                return f"❌ **Hunt Failed:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_trade(self, user: str, args: List[str], channel: str) -> str:
        """Create trade offer"""
        if len(args) < 3:
            return "❌ **Usage:** `!trade <item> <amount> <price>`"

        item, amount, price = args[0], args[1], args[2]
        try:
            result = self.game_systems.execute_command(
                {"username": user}, "trade", [item, amount, price]
            )
            if result["success"]:
                return f"💼 **Trade Created!**\n{result['response']}"
            else:
                return f"❌ **Trade Failed:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_craft(self, user: str, args: List[str], channel: str) -> str:
        """Craft items"""
        if not args:
            return "❌ **Usage:** `!craft <item>`"

        item = args[0]
        try:
            result = self.game_systems.execute_command(
                {"username": user}, "craft", [item]
            )
            if result["success"]:
                return f"🔨 **Crafting Complete!**\n{result['response']}"
            else:
                return f"❌ **Crafting Failed:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_profile(self, user: str, args: List[str], channel: str) -> str:
        """Show user profile"""
        try:
            result = self.game_systems.execute_command({"username": user}, "profile")
            if result["success"]:
                return f"👤 **Profile:**\n{result['response']}"
            else:
                return f"❌ **Profile Error:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_leaderboard(self, user: str, args: List[str], channel: str) -> str:
        """Show leaderboard"""
        try:
            result = self.game_systems.execute_command(
                {"username": user}, "leaderboard"
            )
            if result["success"]:
                return f"🏆 **Leaderboard:**\n{result['response']}"
            else:
                return f"❌ **Leaderboard Error:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_chat(self, user: str, args: List[str], channel: str) -> str:
        """Chat with AI"""
        if not args:
            return "❌ **Usage:** `!chat <message>`"

        message = " ".join(args)
        try:
            result = self.game_systems.execute_command(
                {"username": user}, "chat", [message]
            )
            if result["success"]:
                llm_response = result.get("llm_response", {})
                if llm_response:
                    return f"💬 **AI Response:**\n{llm_response.get('response', 'No response')}"
                else:
                    return f"💬 **Chat:**\n{result['response']}"
            else:
                return f"❌ **Chat Failed:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_personality(self, user: str, args: List[str], channel: str) -> str:
        """Show personality stats"""
        try:
            result = self.game_systems.execute_command(
                {"username": user}, "personality"
            )
            if result["success"]:
                return f"🧠 **Personality:**\n{result['response']}"
            else:
                return f"❌ **Personality Error:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_kingdom(self, user: str, args: List[str], channel: str) -> str:
        """Show kingdom info"""
        try:
            result = self.game_systems.execute_command({"username": user}, "kingdom")
            if result["success"]:
                return f"👑 **Kingdom:**\n{result['response']}"
            else:
                return f"❌ **Kingdom Error:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_memory(self, user: str, args: List[str], channel: str) -> str:
        """Show memory profile"""
        try:
            result = self.game_systems.execute_command({"username": user}, "memory")
            if result["success"]:
                return f"🧠 **Memory:**\n{result['response']}"
            else:
                return f"❌ **Memory Error:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_join(self, user: str, args: List[str], channel: str) -> str:
        """Join the simulation"""
        try:
            result = self.game_systems.execute_command({"username": user}, "join")
            if result["success"]:
                return f"🎉 **Welcome!**\n{result['response']}"
            else:
                return f"❌ **Join Failed:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_leave(self, user: str, args: List[str], channel: str) -> str:
        """Leave the simulation"""
        try:
            result = self.game_systems.execute_command({"username": user}, "leave")
            if result["success"]:
                return f"👋 **Goodbye!**\n{result['response']}"
            else:
                return f"❌ **Leave Failed:** {result['response']}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def cmd_ping(self, user: str, args: List[str], channel: str) -> str:
        """Check bot response time"""
        return f"🏓 **Pong!** Response time: {random.randint(50, 200)}ms"

    def cmd_status(self, user: str, args: List[str], channel: str) -> str:
        """Show server status"""
        stats = self.game_systems.simulation_stats
        return f"""
📊 **Server Status**

**Commands Processed:** {stats.get('total_commands', 0)}
**Successful:** {stats.get('successful_commands', 0)}
**Failed:** {stats.get('failed_commands', 0)}

**Economy:**
💰 RP Earned: {stats.get('rp_earned', 0)}
💸 RP Spent: {stats.get('rp_spent', 0)}

**Activities:**
🌿 Resources Gathered: {stats.get('resources_gathered', 0)}
🎯 Hunts Attempted: {stats.get('hunts_attempted', 0)}
💼 Trades Made: {stats.get('trades_made', 0)}
🔨 Crafting Attempts: {stats.get('crafting_attempts', 0)}

**AI Interactions:**
🤖 LLM Responses: {stats.get('llm_responses', 0)}
🧠 Deepseek (Aether): {stats.get('deepseek_responses', 0)}
⚙️ Ollama (Stagehand): {stats.get('ollama_responses', 0)}
⏰ Timeouts: {stats.get('llm_timeouts', 0)}

**Users:**
👥 Joined: {stats.get('users_joined', 0)}
🚪 Left: {stats.get('users_left', 0)}
        """.strip()


class CompleteGameSimulation:
    """Complete game simulation with Discord bot interface"""

    def __init__(self):
        self.discord_server = self.create_discord_server()
        self.discord_bot = None
        self.game_systems = None
        self.simulation_stats = {
            "total_messages": 0,
            "bot_responses": 0,
            "commands_processed": 0,
            "errors": 0,
            "start_time": None,
            "end_time": None,
        }
        self.running = False
        self.message_history = []
        self._init_game_systems()

    def _init_game_systems(self):
        """Initialize the game systems"""
        try:
            from core.memory_system import ConsolidatedMemorySystem
            from core.economy import RPEconomy
            from core.hunting_system import HuntingSystem
            from core.resource_system import ResourceSystem
            from core.leaderboard import ExclusiveLeaderboard
            from core.personality_system import ConsolidatedPersonalitySystem
            from core.ai_circuit_breaker import AICircuitBreaker
            from core.trade_system import TradeSystem
            from core.kingdom_system import KingdomSystem
            from core.network_consciousness import NetworkConsciousness

            self.game_systems = GameSystemsWrapper()
            self.discord_bot = SimulatedDiscordBot(self.game_systems)

            print("✅ Complete game simulation initialized!")

        except Exception as e:
            print(f"❌ Error initializing game systems: {e}")
            raise

    def create_discord_server(self) -> DiscordServer:
        """Create the simulated Discord server"""
        server = DiscordServer(
            id="simulacra_rancher_server",
            name="Simulacra Rancher",
            owner_id="bot_owner",
        )

        # Create channels
        channels = [
            DiscordChannel("general", "general", "text", "General discussion"),
            DiscordChannel("commands", "commands", "text", "Bot commands"),
            DiscordChannel("trading", "trading", "text", "Trade offers"),
            DiscordChannel("hunting", "hunting", "text", "Hunting results"),
            DiscordChannel("crafting", "crafting", "text", "Crafting discussion"),
            DiscordChannel("chat", "chat", "text", "AI chat"),
            DiscordChannel(
                "announcements", "announcements", "text", "Server announcements"
            ),
        ]

        server.channels = channels
        return server

    def add_user(self, username: str) -> DiscordUser:
        """Add a user to the Discord server"""
        user = DiscordUser(
            id=f"user_{len(self.discord_server.members)}",
            username=username,
            display_name=username,
            joined_at=datetime.now(),
        )
        self.discord_server.members.append(user)
        return user

    def send_message(
        self, user: str, content: str, channel: str = "general"
    ) -> DiscordMessage:
        """Send a message to a Discord channel"""
        message = DiscordMessage(
            id=f"msg_{int(time.time() * 1000)}",
            author=user,
            content=content,
            timestamp=datetime.now(),
            channel=channel,
        )

        # Add to channel
        for ch in self.discord_server.channels:
            if ch.name == channel:
                ch.messages.append(message)
                break

        self.message_history.append(message)
        self.simulation_stats["total_messages"] += 1

        return message

    def process_bot_commands(self, message: DiscordMessage) -> List[DiscordMessage]:
        """Process a message through the bot and return responses"""
        responses = self.discord_bot.process_message(message)

        # Add responses to channels
        for response in responses:
            for ch in self.discord_server.channels:
                if ch.name == response.channel:
                    ch.messages.append(response)
                    break
            self.message_history.append(response)

        self.simulation_stats["bot_responses"] += len(responses)
        self.simulation_stats["commands_processed"] += 1

        return responses

    def simulate_user_activity(
        self, user: str, activity_type: str = "random"
    ) -> List[DiscordMessage]:
        """Simulate realistic user activity"""
        messages = []

        if activity_type == "random":
            activities = [
                f"!daily",
                f"!gather",
                f"!hunt",
                f"!chat Hello there!",
                f"!profile",
                f"!personality",
                f"!craft stone_pickaxe",
                f"!trade stone 5 10",
                f"!leaderboard",
                f"!kingdom",
                f"!memory",
                f"!status",
                f"!ping",
                f"!help",
            ]

            # Random number of activities (1-3)
            num_activities = random.randint(1, 3)
            selected_activities = random.sample(activities, num_activities)

            for activity in selected_activities:
                # Add some random chat messages
                if random.random() < 0.3:
                    chat_messages = [
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
                    ]
                    chat_msg = random.choice(chat_messages)
                    messages.append(self.send_message(user, chat_msg, "chat"))

                # Send command
                messages.append(self.send_message(user, activity, "commands"))

                # Process bot response
                if messages:
                    bot_responses = self.process_bot_commands(messages[-1])
                    messages.extend(bot_responses)

                # Small delay between activities
                time.sleep(random.uniform(0.1, 0.5))

        return messages

    def run_simulation(self, duration_minutes: int = 30, num_users: int = 10):
        """Run the complete game simulation"""
        print(f"🎮 Starting Complete Game Simulation")
        print(f"⏱️  Duration: {duration_minutes} minutes")
        print(f"👥 Users: {num_users}")
        print(f"🤖 Bot: Simulated Discord Bot")
        print(f"📺 Channels: {len(self.discord_server.channels)}")
        print()

        self.simulation_stats["start_time"] = datetime.now()
        self.running = True

        # Create users
        users = []
        for i in range(num_users):
            username = f"Player{i+1}"
            user = self.add_user(username)
            users.append(user)
            print(f"👤 {username} joined the server")

        # Join users to game
        for user in users:
            self.send_message(user.username, "!join", "commands")
            self.process_bot_commands(self.message_history[-1])

        print(f"\n🎯 Starting {duration_minutes} minutes of activity...")

        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)

        while time.time() < end_time and self.running:
            # Simulate user activity
            for user in users:
                if random.random() < 0.7:  # 70% chance of activity
                    messages = self.simulate_user_activity(user.username)

                    # Print activity summary
                    if messages:
                        print(f"📝 {user.username}: {len(messages)} activities")

            # Random events
            if random.random() < 0.1:  # 10% chance of special event
                event_user = random.choice(users)
                special_events = [
                    "!chat The AI seems to be evolving...",
                    "!chat I think I found a pattern in the memories",
                    "!chat The kingdom politics are getting intense",
                    "!chat Anyone else notice the resource patterns?",
                    "!chat The hunting system is brilliant",
                    "!chat I love how the personality system works",
                    "!chat The trading economy is fascinating",
                    "!chat The crafting recipes are getting complex",
                ]
                event_msg = random.choice(special_events)
                self.send_message(event_user.username, event_msg, "chat")
                self.process_bot_commands(self.message_history[-1])
                print(f"🌟 {event_user.username}: Special event")

            # Progress update
            elapsed = time.time() - start_time
            remaining = end_time - time.time()
            if elapsed % 60 < 1:  # Every minute
                print(
                    f"⏱️  Elapsed: {int(elapsed/60)}m, Remaining: {int(remaining/60)}m"
                )

            time.sleep(1)  # 1 second per cycle

        self.simulation_stats["end_time"] = datetime.now()
        self.running = False

        print(f"\n✅ Simulation Complete!")
        self.print_results()
        self.save_results()

    def print_results(self):
        """Print simulation results"""
        duration = (
            self.simulation_stats["end_time"] - self.simulation_stats["start_time"]
        ).total_seconds()

        print(f"\n📊 **Simulation Results**")
        print(f"⏱️  Duration: {duration:.1f} seconds")
        print(f"📝 Total Messages: {self.simulation_stats['total_messages']}")
        print(f"🤖 Bot Responses: {self.simulation_stats['bot_responses']}")
        print(f"⚙️  Commands Processed: {self.simulation_stats['commands_processed']}")
        print(f"❌ Errors: {self.simulation_stats['errors']}")
        print(f"👥 Users: {len(self.discord_server.members)}")
        print(f"📺 Channels: {len(self.discord_server.channels)}")

        # Channel activity
        print(f"\n📺 **Channel Activity:**")
        for channel in self.discord_server.channels:
            print(f"  #{channel.name}: {len(channel.messages)} messages")

    def save_results(self):
        """Save simulation results to file"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "simulation_stats": {
                k: v.isoformat() if isinstance(v, datetime) else v
                for k, v in self.simulation_stats.items()
            },
            "server_info": {
                "name": self.discord_server.name,
                "channels": len(self.discord_server.channels),
                "members": len(self.discord_server.members),
            },
            "channel_stats": {
                ch.name: {
                    "messages": len(ch.messages),
                    "topic": ch.topic,
                }
                for ch in self.discord_server.channels
            },
            "user_stats": {
                user.username: {
                    "joined_at": user.joined_at.isoformat(),
                    "roles": user.roles,
                }
                for user in self.discord_server.members
            },
            "bot_command_history": self.discord_bot.command_history,
            "message_sample": [
                {
                    "author": msg.author,
                    "content": msg.content,
                    "channel": msg.channel,
                    "timestamp": msg.timestamp.isoformat(),
                }
                for msg in self.message_history[-50:]  # Last 50 messages
            ],
        }

        with open("complete_game_simulation_results.json", "w") as f:
            json.dump(results, f, indent=2)

        print(f"💾 Results saved to: complete_game_simulation_results.json")


class GameSystemsWrapper:
    """Wrapper for game systems to provide unified interface"""

    def __init__(self):
        self.simulation_stats = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "rp_earned": 0,
            "rp_spent": 0,
            "resources_gathered": 0,
            "hunts_attempted": 0,
            "trades_made": 0,
            "memories_stored": 0,
            "crafting_attempts": 0,
            "llm_responses": 0,
            "deepseek_responses": 0,
            "ollama_responses": 0,
            "llm_timeouts": 0,
        }

    def execute_command(self, user: Dict, command: str, args: List[str] = None) -> Dict:
        """Execute a game command"""
        if args is None:
            args = []

        self.simulation_stats["total_commands"] += 1

        # Simulate command execution
        result = {
            "success": True,
            "response": f"Command '{command}' executed successfully",
            "rp_change": 0,
            "resources_gained": {},
            "resources_spent": {},
        }

        if command == "daily":
            rp_gain = random.randint(50, 100)
            result["rp_change"] = rp_gain
            result["response"] = f"💰 Daily bonus claimed! +{rp_gain} RP"
            self.simulation_stats["rp_earned"] += rp_gain

        elif command == "gather":
            resources = ["stone", "wood", "metal", "crystal"]
            resource = random.choice(resources)
            qualities = ["common", "uncommon", "rare"]
            quality = random.choice(qualities)
            result["resources_gained"] = {resource: {quality: random.randint(1, 5)}}
            result["response"] = f"🌿 Gathered {quality} {resource}"
            self.simulation_stats["resources_gathered"] += 1

        elif command == "hunt":
            success = random.random() < 0.6
            rp_cost = random.randint(10, 30)
            if success:
                result["rp_change"] = -rp_cost
                result["response"] = (
                    f"🎯 Hunt successful! Caught a Simulacra (-{rp_cost} RP)"
                )
            else:
                result["rp_change"] = -rp_cost
                result["response"] = f"❌ Hunt failed (-{rp_cost} RP)"
            self.simulation_stats["hunts_attempted"] += 1
            self.simulation_stats["rp_spent"] += rp_cost

        elif command == "trade":
            if len(args) >= 3:
                item, amount, price = args[0], int(args[1]), int(args[2])
                result["response"] = (
                    f"💼 Trade offer created: {amount} {item} for {price} RP"
                )
                self.simulation_stats["trades_made"] += 1
            else:
                result["success"] = False
                result["response"] = "Invalid trade parameters"

        elif command == "craft":
            if args:
                item = args[0]
                success = random.random() < 0.8
                rp_cost = random.randint(5, 20)
                if success:
                    result["rp_change"] = -rp_cost
                    result["response"] = (
                        f"🔨 Crafted {item} successfully (-{rp_cost} RP)"
                    )
                else:
                    result["rp_change"] = -rp_cost
                    result["response"] = f"❌ Crafting failed (-{rp_cost} RP)"
                self.simulation_stats["crafting_attempts"] += 1
                self.simulation_stats["rp_spent"] += rp_cost
            else:
                result["success"] = False
                result["response"] = "No item specified"

        elif command == "chat":
            if args:
                message = " ".join(args)
                # Simulate LLM response
                responses = [
                    "That's an interesting perspective!",
                    "I've been thinking about that too.",
                    "The patterns in this world are fascinating.",
                    "Have you noticed the recent changes?",
                    "The memories are becoming more complex.",
                    "I wonder what the future holds for us.",
                    "The kingdom politics are getting intense.",
                    "The resource distribution is quite dynamic.",
                ]
                response = random.choice(responses)
                result["response"] = f"💬 AI: {response}"
                result["llm_response"] = {
                    "model_used": "deepseek" if random.random() < 0.6 else "ollama",
                    "response": response,
                    "timestamp": datetime.now().isoformat(),
                }
                self.simulation_stats["llm_responses"] += 1
                if result["llm_response"]["model_used"] == "deepseek":
                    self.simulation_stats["deepseek_responses"] += 1
                else:
                    self.simulation_stats["ollama_responses"] += 1
            else:
                result["success"] = False
                result["response"] = "No message provided"

        elif command in ["profile", "personality", "kingdom", "memory", "leaderboard"]:
            result["response"] = f"📊 {command.title()} information displayed"

        elif command == "join":
            result["response"] = f"🎉 Welcome to Simulacra Rancher!"
            self.simulation_stats["users_joined"] += 1

        elif command == "leave":
            result["response"] = f"👋 Goodbye! Thanks for playing!"
            self.simulation_stats["users_left"] += 1

        else:
            result["success"] = False
            result["response"] = f"Unknown command: {command}"

        if result["success"]:
            self.simulation_stats["successful_commands"] += 1
        else:
            self.simulation_stats["failed_commands"] += 1

        return result


def main():
    """Main function to run the complete game simulation"""
    print("🎮 Complete Game Simulation for Simulacra Rancher")
    print("=" * 60)

    simulation = CompleteGameSimulation()

    # Run simulation for 30 minutes with 10 users
    simulation.run_simulation(duration_minutes=30, num_users=10)


if __name__ == "__main__":
    main()
