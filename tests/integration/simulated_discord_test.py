#!/usr/bin/env python3
"""
Simulated Discord Environment for Real-Time Testing
Interact with the bot as a real player to test all systems
"""

import sys
import os
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import random

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class SimulatedDiscordUser:
    """Simulates a Discord user interacting with the bot"""

    def __init__(self, user_id: str, username: str, is_bot: bool = False):
        self.user_id = user_id
        self.username = username
        self.is_bot = is_bot
        self.rp = 0
        self.resources = {}
        self.memories = []
        self.hunting_history = []

    def __str__(self):
        return f"@{self.username} ({self.user_id})"


class SimulatedDiscordChannel:
    """Simulates a Discord channel"""

    def __init__(self, channel_id: str, channel_name: str, channel_type: str = "text"):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_type = channel_type
        self.messages = []

    def send_message(
        self, user: SimulatedDiscordUser, content: str, is_bot: bool = False
    ):
        """Send a message to the channel"""
        message = {
            "id": f"msg_{len(self.messages)}_{int(time.time())}",
            "author": user,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "is_bot": is_bot,
        }
        self.messages.append(message)
        return message


class SimulatedDiscordBot:
    """Simulates the Discord bot with all systems integrated"""

    def __init__(self):
        self.users = {}
        self.channels = {}
        self.current_user = None
        self.current_channel = None

        # Initialize all core systems
        self._init_systems()

    def _init_systems(self):
        """Initialize all core systems"""
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

            self.memory_system = ConsolidatedMemorySystem(simple_mode=True)
            self.economy = RPEconomy()
            self.hunting_system = HuntingSystem()
            self.resource_system = ResourceSystem()
            self.leaderboard = ExclusiveLeaderboard()
            self.personality_system = ConsolidatedPersonalitySystem()
            self.ai_circuit_breaker = AICircuitBreaker()
            self.trade_system = TradeSystem()
            self.kingdom_system = KingdomSystem()
            self.network_consciousness = NetworkConsciousness()

            # Initialize databases
            self.hunting_system._init_database()
            self.resource_system._init_database()
            self.trade_system._init_database()

            print("✅ All systems initialized successfully!")

        except Exception as e:
            print(f"❌ Error initializing systems: {e}")
            raise

    def create_user(self, user_id: str, username: str) -> SimulatedDiscordUser:
        """Create a new simulated Discord user"""
        user = SimulatedDiscordUser(user_id, username)
        self.users[user_id] = user
        return user

    def create_channel(
        self, channel_id: str, channel_name: str
    ) -> SimulatedDiscordChannel:
        """Create a new simulated Discord channel"""
        channel = SimulatedDiscordChannel(channel_id, channel_name)
        self.channels[channel_id] = channel
        return channel

    def set_current_user(self, user: SimulatedDiscordUser):
        """Set the current user for interactions"""
        self.current_user = user

    def set_current_channel(self, channel: SimulatedDiscordChannel):
        """Set the current channel for interactions"""
        self.current_channel = channel

    def process_command(self, command: str) -> str:
        """Process a Discord command and return the bot's response"""
        if not self.current_user or not self.current_channel:
            return "❌ Error: No user or channel set"

        try:
            parts = command.split()
            cmd = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []

            # Process different commands
            if cmd == "!help":
                return self._handle_help()
            elif cmd == "!rp":
                return self._handle_rp()
            elif cmd == "!gather":
                return self._handle_gather(args)
            elif cmd == "!hunt":
                return self._handle_hunt(args)
            elif cmd == "!trade":
                return self._handle_trade(args)
            elif cmd == "!leaderboard":
                return self._handle_leaderboard()
            elif cmd == "!kingdoms":
                return self._handle_kingdoms()
            elif cmd == "!daily":
                return self._handle_daily()
            elif cmd == "!memory":
                return self._handle_memory(args)
            elif cmd == "!personality":
                return self._handle_personality(args)
            else:
                return (
                    f"❓ Unknown command: {cmd}. Type `!help` for available commands."
                )

        except Exception as e:
            return f"❌ Error processing command: {str(e)}"

    def _handle_help(self) -> str:
        """Handle !help command"""
        help_text = """
🎮 **Simulacra Rancher Commands**

💰 **Economy:**
  `!rp` - Check your RP balance
  `!daily` - Claim daily bonus

🌲 **Resources:**
  `!gather <resource> <quality>` - Gather resources
  `!hunt <spawn_id> <rp_cost>` - Hunt Simulacra

🤝 **Trading:**
  `!trade <buyer_id> <item> <amount> <price>` - Create trade offer

🏆 **Competition:**
  `!leaderboard` - View top players
  `!kingdoms` - View kingdoms

🧠 **AI Features:**
  `!memory <type> <content>` - Store memory
  `!personality <message>` - Test AI personality

Type any command to test the system!
        """
        return help_text.strip()

    def _handle_rp(self) -> str:
        """Handle !rp command"""
        user = self.current_user

        # Get user's RP from economy system
        player_data = {"rp": user.rp}

        return f"💰 **{user.username}** has **{player_data['rp']} RP**"

    def _handle_gather(self, args: List[str]) -> str:
        """Handle !gather command"""
        if len(args) < 2:
            return "❌ Usage: `!gather <resource> <quality>`"

        resource_type = args[0]
        quality = args[1]
        user = self.current_user

        # Start gathering
        self.resource_system.start_gathering(user.user_id, resource_type, quality)

        # Get updated resources
        resources = self.resource_system.get_user_resources(user.user_id)

        return f"🌲 **{user.username}** gathered **{resource_type}** ({quality} quality)\n📦 Resources: {resources}"

    def _handle_hunt(self, args: List[str]) -> str:
        """Handle !hunt command"""
        if len(args) < 2:
            return "❌ Usage: `!hunt <spawn_id> <rp_cost>`"

        spawn_id = args[0]
        rp_cost = int(args[1])
        user = self.current_user

        # Check if user has enough RP
        if user.rp < rp_cost:
            return f"❌ **{user.username}** doesn't have enough RP! Need {rp_cost} RP, have {user.rp} RP"

        # Attempt to catch
        from core.hunting_system import HuntingEvent

        spawn_event = self.hunting_system.create_spawn_event(
            HuntingEvent.WILD_SPAWN, self.current_channel.channel_id
        )

        catch_result = self.hunting_system.attempt_catch(
            user.user_id, spawn_event["spawn_id"], rp_cost
        )

        if catch_result.get("success"):
            # Deduct RP
            user.rp -= rp_cost
            return f"🎯 **{user.username}** successfully caught a Simulacra! (-{rp_cost} RP)\n💰 Remaining RP: {user.rp}"
        else:
            return f"❌ **{user.username}** failed to catch the Simulacra: {catch_result.get('error', 'Unknown error')}"

    def _handle_trade(self, args: List[str]) -> str:
        """Handle !trade command"""
        if len(args) < 4:
            return "❌ Usage: `!trade <buyer_id> <item> <amount> <price>`"

        buyer_id = args[0]
        item = args[1]
        amount = int(args[2])
        price = int(args[3])
        user = self.current_user

        # Create trade offer
        trade_result = self.trade_system.create_trade_offer(
            user.user_id, buyer_id, item, amount, price
        )

        if trade_result.get("success"):
            return f"🤝 **{user.username}** created trade offer: {amount}x {item} for {price} RP"
        else:
            return f"❌ Trade failed: {trade_result.get('error', 'Unknown error')}"

    def _handle_leaderboard(self) -> str:
        """Handle !leaderboard command"""
        top_10 = self.leaderboard.get_top_10()

        if not top_10:
            return "🏆 **Leaderboard is empty**"

        leaderboard_text = "🏆 **Top 10 Players**\n"
        for i, entry in enumerate(top_10[:10], 1):
            leaderboard_text += f"{i}. **{entry.username}** - {entry.rp_earned} RP\n"

        return leaderboard_text

    def _handle_kingdoms(self) -> str:
        """Handle !kingdoms command"""
        kingdoms = self.kingdom_system.get_all_kingdoms()

        kingdoms_text = "👑 **Available Kingdoms**\n"
        for kingdom in kingdoms:
            kingdoms_text += f"• **{kingdom['name']}** - {kingdom['element']}\n"

        return kingdoms_text

    def _handle_daily(self) -> str:
        """Handle !daily command"""
        user = self.current_user

        # Give daily bonus
        daily_bonus = 50
        user.rp += daily_bonus

        return f"🎁 **{user.username}** claimed daily bonus: +{daily_bonus} RP\n💰 Total RP: {user.rp}"

    def _handle_memory(self, args: List[str]) -> str:
        """Handle !memory command"""
        if len(args) < 2:
            return "❌ Usage: `!memory <type> <content>`"

        memory_type = args[0]
        content = " ".join(args[1:])
        user = self.current_user

        # Store memory
        self.memory_system.store_user_memory(user.user_id, memory_type, content)

        return f"🧠 **{user.username}** stored memory: {memory_type} - {content}"

    def _handle_personality(self, args: List[str]) -> str:
        """Handle !personality command"""
        if not args:
            return "❌ Usage: `!personality <message>`"

        message = " ".join(args)
        user = self.current_user

        # Process with personality system
        emotional_state = self.personality_system.process_input(user.user_id, message)

        return f"🧠 **{user.username}** personality response:\n{emotional_state}"


class SimulatedDiscordTester:
    """Main tester class for simulated Discord interactions"""

    def __init__(self):
        self.bot = SimulatedDiscordBot()
        self.test_scenarios = []

    def setup_test_environment(self):
        """Set up the test environment with users and channels"""
        print("🎮 Setting up Simulated Discord Environment...")

        # Create test users
        self.player1 = self.bot.create_user("123456789", "Travis")
        self.player2 = self.bot.create_user("987654321", "TestUser")

        # Create test channels
        self.general_channel = self.bot.create_channel("111111111", "general")
        self.hunting_channel = self.bot.create_channel("222222222", "hunting")

        # Set initial state
        self.bot.set_current_user(self.player1)
        self.bot.set_current_channel(self.general_channel)

        print(f"✅ Created users: {self.player1}, {self.player2}")
        print(
            f"✅ Created channels: {self.general_channel.channel_name}, {self.hunting_channel.channel_name}"
        )
        print(f"🎯 Current user: {self.bot.current_user}")
        print(f"📺 Current channel: {self.bot.current_channel.channel_name}")

    def run_interactive_test(self):
        """Run interactive testing session"""
        print("\n" + "=" * 60)
        print("🎮 SIMULATED DISCORD TESTING SESSION")
        print("=" * 60)
        print("You are now interacting with the Simulacra Rancher bot!")
        print("Type Discord commands to test the system.")
        print("Type 'help' for available commands, 'quit' to exit.")
        print("=" * 60)

        while True:
            try:
                # Get user input
                user_input = input(f"\n{self.bot.current_user.username}> ").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    print("👋 Thanks for testing! Goodbye!")
                    break
                elif user_input.lower() == "help":
                    print(self.bot._handle_help())
                    continue
                elif user_input.lower() == "switch":
                    # Switch between users
                    if self.bot.current_user == self.player1:
                        self.bot.set_current_user(self.player2)
                        print(f"🔄 Switched to user: {self.bot.current_user}")
                    else:
                        self.bot.set_current_user(self.player1)
                        print(f"🔄 Switched to user: {self.bot.current_user}")
                    continue
                elif user_input.lower() == "channel":
                    # Switch between channels
                    if self.bot.current_channel == self.general_channel:
                        self.bot.set_current_channel(self.hunting_channel)
                        print(
                            f"📺 Switched to channel: {self.bot.current_channel.channel_name}"
                        )
                    else:
                        self.bot.set_current_channel(self.general_channel)
                        print(
                            f"📺 Switched to channel: {self.bot.current_channel.channel_name}"
                        )
                    continue
                elif user_input.lower() == "status":
                    # Show current status
                    print(f"👤 User: {self.bot.current_user}")
                    print(f"📺 Channel: {self.bot.current_channel.channel_name}")
                    print(f"💰 RP: {self.bot.current_user.rp}")
                    continue

                # Process command
                if user_input.startswith("!"):
                    response = self.bot.process_command(user_input)
                    print(f"\n🤖 Bot: {response}")
                else:
                    print(
                        "💬 (Type commands starting with '!' to interact with the bot)"
                    )

            except KeyboardInterrupt:
                print("\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def run_automated_test_scenarios(self):
        """Run automated test scenarios"""
        print("\n🤖 Running Automated Test Scenarios...")

        scenarios = [
            ("Basic Commands", ["!help", "!rp", "!daily"]),
            (
                "Resource Gathering",
                ["!gather wood normal", "!gather stone rare", "!gather metal epic"],
            ),
            ("Hunting System", ["!hunt 123 50", "!hunt 456 100"]),
            (
                "Trading System",
                ["!trade 987654321 wood 5 25", "!trade 987654321 stone 3 50"],
            ),
            ("Leaderboard & Kingdoms", ["!leaderboard", "!kingdoms"]),
            (
                "AI Features",
                [
                    "!memory gameplay First hunting session",
                    "!personality I'm excited to hunt Simulacra!",
                ],
            ),
        ]

        for scenario_name, commands in scenarios:
            print(f"\n🎯 Testing: {scenario_name}")
            self.bot.set_current_user(self.player1)
            self.bot.set_current_channel(self.general_channel)

            for command in commands:
                print(f"  📝 {self.bot.current_user.username}> {command}")
                response = self.bot.process_command(command)
                print(f"  🤖 Bot: {response}")
                time.sleep(0.5)  # Small delay for readability

        print("\n✅ Automated test scenarios completed!")


def main():
    """Main function to run the simulated Discord testing"""
    tester = SimulatedDiscordTester()

    print("🚀 Starting Simulated Discord Testing Environment")
    print("=" * 60)

    # Set up environment
    tester.setup_test_environment()

    # Ask user what type of testing they want
    print("\n🎯 Choose testing mode:")
    print("1. Interactive testing (you type commands)")
    print("2. Automated testing (predefined scenarios)")
    print("3. Both")

    choice = input("\nEnter your choice (1/2/3): ").strip()

    if choice == "1":
        tester.run_interactive_test()
    elif choice == "2":
        tester.run_automated_test_scenarios()
    elif choice == "3":
        tester.run_automated_test_scenarios()
        print("\n" + "=" * 60)
        tester.run_interactive_test()
    else:
        print("❌ Invalid choice. Running interactive mode...")
        tester.run_interactive_test()


if __name__ == "__main__":
    main()
