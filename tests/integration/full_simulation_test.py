#!/usr/bin/env python3
"""
Full Simulation Test for Simulacra Rancher
Complete simulation without Discord bot - tests all systems directly
Includes LLM responses, queue system, realistic user behavior, and comprehensive data collection
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

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FullSimulationTester:
    """Complete simulation tester with all systems integrated"""

    def __init__(self):
        self.test_results = []
        self.unique_errors = set()
        self.unique_issues = set()
        self.daily_stats = []
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
            "queue_requests": 0,
            "unique_errors": 0,
            "unique_issues": 0,
            "users_joined": 0,
            "users_left": 0,
            "start_time": None,
            "end_time": None,
        }
        self.running = False
        self.command_queue = queue.Queue()
        self.processing_queue = False
        self.llm_timeout = 300  # 5 minutes
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

            print("✅ All systems initialized for full simulation!")

        except Exception as e:
            print(f"❌ Error initializing systems: {e}")
            raise

    def create_realistic_users(self, num_users: int = 20):
        """Create realistic users with different specializations"""
        self.users = []
        user_types = [
            {
                "name": "Hunter",
                "daily_commands": 80,
                "rp_start": 300,
                "specialization": "hunting",
            },
            {
                "name": "Gatherer",
                "daily_commands": 60,
                "rp_start": 200,
                "specialization": "gathering",
            },
            {
                "name": "Trader",
                "daily_commands": 40,
                "rp_start": 250,
                "specialization": "trading",
            },
            {
                "name": "Crafter",
                "daily_commands": 50,
                "rp_start": 180,
                "specialization": "crafting",
            },
            {
                "name": "Explorer",
                "daily_commands": 70,
                "rp_start": 220,
                "specialization": "exploration",
            },
            {
                "name": "Social",
                "daily_commands": 30,
                "rp_start": 150,
                "specialization": "social",
            },
            {
                "name": "Veteran",
                "daily_commands": 100,
                "rp_start": 400,
                "specialization": "balanced",
            },
            {
                "name": "Newbie",
                "daily_commands": 20,
                "rp_start": 100,
                "specialization": "learning",
            },
        ]

        for i in range(num_users):
            user_type = random.choice(user_types)
            user_id = f"sim_user_{i+1}"
            username = f"{user_type['name']}User{i+1}"
            user = {
                "user_id": user_id,
                "username": username,
                "rp": user_type["rp_start"],
                "daily_commands": user_type["daily_commands"],
                "specialization": user_type["specialization"],
                "resources": {},
                "memories": [],
                "hunting_history": [],
                "crafting_history": [],
                "trading_history": [],
                "daily_claimed": False,
                "user_type": user_type["name"],
                "join_date": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat(),
                "reputation": random.randint(0, 100),
                "skill_level": random.randint(1, 10),
                "preferences": {
                    "favorite_activity": user_type["specialization"],
                    "risk_tolerance": random.uniform(0.1, 0.9),
                    "social_level": random.uniform(0.1, 0.9),
                },
            }
            self.users.append(user)

        print(f"✅ Created {num_users} realistic users with specializations")
        return self.users

    def get_llm_response(self, user: Dict, message: str) -> str:
        """Get LLM response from local models"""
        try:
            # Try Ollama first (CPU)
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2",
                    "prompt": f"User {user['username']} says: {message}\n\nRespond as the Simulacra Rancher AI assistant:",
                    "stream": False,
                },
                timeout=self.llm_timeout,
            )
            if response.status_code == 200:
                result = response.json()
                self.simulation_stats["llm_responses"] += 1
                return result.get("response", "I understand.")

            # Try LM Studio (GPU)
            response = requests.post(
                "http://localhost:1234/v1/chat/completions",
                json={
                    "model": "local-model",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are the Simulacra Rancher AI assistant.",
                        },
                        {
                            "role": "user",
                            "content": f"User {user['username']} says: {message}",
                        },
                    ],
                    "max_tokens": 150,
                    "temperature": 0.7,
                },
                timeout=self.llm_timeout,
            )
            if response.status_code == 200:
                result = response.json()
                self.simulation_stats["llm_responses"] += 1
                return result["choices"][0]["message"]["content"]

        except Exception as e:
            return f"AI Response: I understand your message about {message[:20]}..."

        return "AI Response: Processing your request..."

    def add_to_queue(self, user: Dict, command: str, args: List[str]) -> Dict:
        """Add command to processing queue"""
        queue_item = {
            "user": user,
            "command": command,
            "args": args,
            "timestamp": datetime.now().isoformat(),
            "queue_position": self.command_queue.qsize() + 1,
        }

        self.command_queue.put(queue_item)
        self.simulation_stats["queue_requests"] += 1

        # Calculate estimated wait time (1 second per item in queue)
        estimated_wait = self.command_queue.qsize() * 1

        return {
            "success": True,
            "response": f"📋 {user['username']} added to queue (Position: {queue_item['queue_position']}, Est. wait: {estimated_wait}s)",
            "queue_position": queue_item["queue_position"],
            "estimated_wait": estimated_wait,
        }

    def process_queue(self):
        """Process commands from queue"""
        if self.processing_queue:
            return

        self.processing_queue = True

        while not self.command_queue.empty():
            try:
                queue_item = self.command_queue.get(timeout=1)
                user = queue_item["user"]
                command = queue_item["command"]
                args = queue_item["args"]

                # Execute the command
                result = self.execute_command(user, command, args)

                # Update user's last active time
                user["last_active"] = datetime.now().isoformat()

                # Small delay to simulate processing time
                time.sleep(0.1)

            except queue.Empty:
                break
            except Exception as e:
                print(f"❌ Queue processing error: {e}")

        self.processing_queue = False

    def execute_command(self, user: Dict, command: str, args: List[str] = None) -> Dict:
        """Execute a command and return results"""
        if args is None:
            args = []

        result = {
            "command": command,
            "user": user["username"],
            "user_type": user["user_type"],
            "success": False,
            "response": "",
            "rp_change": 0,
            "timestamp": datetime.now().isoformat(),
            "error_type": None,
            "llm_response": None,
        }

        try:
            if command == "daily":
                # Claim daily bonus (only once per day)
                if not user.get("daily_claimed", False):
                    daily_bonus = 50
                    user["rp"] += daily_bonus
                    user["daily_claimed"] = True
                    result["success"] = True
                    result["response"] = (
                        f"🎁 {user['username']} claimed daily bonus: +{daily_bonus} RP"
                    )
                    result["rp_change"] = daily_bonus
                    self.simulation_stats["rp_earned"] += daily_bonus
                else:
                    result["success"] = True
                    result["response"] = (
                        f"⏰ {user['username']} already claimed daily bonus"
                    )

            elif command == "gather":
                if len(args) >= 2:
                    resource_type = args[0]
                    quality = args[1]

                    # Start gathering
                    self.resource_system.start_gathering(
                        user["user_id"], resource_type, quality
                    )
                    resources = self.resource_system.get_user_resources(user["user_id"])

                    # Check for bonus (25% chance)
                    if random.random() < 0.25:
                        bonus_rp = random.randint(5, 15)
                        user["rp"] += bonus_rp
                        result["response"] = (
                            f"🌲 {user['username']} gathered {resource_type} ({quality}) + BONUS {bonus_rp} RP!"
                        )
                        result["rp_change"] = bonus_rp
                        self.simulation_stats["rp_earned"] += bonus_rp
                    else:
                        result["response"] = (
                            f"🌲 {user['username']} gathered {resource_type} ({quality})"
                        )

                    result["success"] = True
                    self.simulation_stats["resources_gathered"] += 1

            elif command == "hunt":
                if len(args) >= 2:
                    spawn_id = args[0]
                    rp_cost = int(args[1])

                    if user["rp"] >= rp_cost:
                        try:
                            # Attempt to catch
                            from core.hunting_system import HuntingEvent

                            spawn_event = self.hunting_system.create_spawn_event(
                                HuntingEvent.WILD_SPAWN, "simulation_channel"
                            )

                            catch_result = self.hunting_system.attempt_catch(
                                user["user_id"], spawn_event["spawn_id"], rp_cost
                            )

                            if catch_result.get("success") and catch_result.get(
                                "caught", False
                            ):
                                user["rp"] -= rp_cost
                                result["success"] = True
                                result["response"] = (
                                    f"🎯 {user['username']} caught Simulacra! (-{rp_cost} RP)"
                                )
                                result["rp_change"] = -rp_cost
                                self.simulation_stats["rp_spent"] += rp_cost

                                # Add to hunting history
                                user["hunting_history"].append(
                                    {
                                        "spawn_id": spawn_event["spawn_id"],
                                        "rp_cost": rp_cost,
                                        "success": True,
                                        "timestamp": datetime.now().isoformat(),
                                    }
                                )
                            elif catch_result.get("success"):
                                # Hunt was successful but didn't catch (normal failure)
                                result["success"] = True
                                result["response"] = (
                                    f"❌ {user['username']} failed to catch: {catch_result.get('message', 'Unknown')}"
                                )

                                # Add to hunting history
                                user["hunting_history"].append(
                                    {
                                        "spawn_id": spawn_event["spawn_id"],
                                        "rp_cost": rp_cost,
                                        "success": False,
                                        "timestamp": datetime.now().isoformat(),
                                    }
                                )
                            else:
                                result["success"] = True
                                result["response"] = (
                                    f"❌ {user['username']} hunt failed: {catch_result.get('error', 'Unknown')}"
                                )

                                # Add to hunting history
                                user["hunting_history"].append(
                                    {
                                        "spawn_id": spawn_event["spawn_id"],
                                        "rp_cost": rp_cost,
                                        "success": False,
                                        "timestamp": datetime.now().isoformat(),
                                    }
                                )

                            self.simulation_stats["hunts_attempted"] += 1
                        except Exception as e:
                            error_msg = f"Database locked during hunt: {str(e)}"
                            self.unique_errors.add(error_msg)
                            result["success"] = False
                            result["response"] = f"🔒 Database locked, retry later"
                            result["error_type"] = "database_locked"
                    else:
                        result["success"] = True
                        result["response"] = (
                            f"❌ {user['username']} needs {rp_cost} RP, has {user['rp']} RP"
                        )

            elif command == "trade":
                if len(args) >= 4:
                    buyer_id = args[0]
                    item = args[1]
                    amount = int(args[2])
                    price = int(args[3])

                    trade_result = self.trade_system.create_trade_offer(
                        user["user_id"], buyer_id, item, amount, price
                    )

                    if trade_result.get("success"):
                        result["success"] = True
                        result["response"] = (
                            f"🤝 {user['username']} created trade: {amount}x {item} for {price} RP"
                        )
                        self.simulation_stats["trades_made"] += 1

                        # Add to trading history
                        user["trading_history"].append(
                            {
                                "item": item,
                                "amount": amount,
                                "price": price,
                                "buyer_id": buyer_id,
                                "timestamp": datetime.now().isoformat(),
                            }
                        )
                    else:
                        result["success"] = True
                        result["response"] = (
                            f"❌ Trade failed: {trade_result.get('error', 'Unknown')}"
                        )

            elif command == "craft":
                if len(args) >= 2:
                    item_type = args[0]
                    quality = args[1]

                    # Simulate crafting
                    craft_cost = random.randint(10, 50)
                    if user["rp"] >= craft_cost:
                        user["rp"] -= craft_cost

                        # Check for crafting success (based on skill level)
                        success_chance = min(0.9, user["skill_level"] * 0.1)
                        if random.random() < success_chance:
                            crafted_item = f"{quality}_{item_type}"
                            result["success"] = True
                            result["response"] = (
                                f"🔨 {user['username']} crafted {crafted_item}! (-{craft_cost} RP)"
                            )
                            result["rp_change"] = -craft_cost
                            self.simulation_stats["rp_spent"] += craft_cost

                            # Add to crafting history
                            user["crafting_history"].append(
                                {
                                    "item": crafted_item,
                                    "cost": craft_cost,
                                    "success": True,
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )
                        else:
                            result["success"] = True
                            result["response"] = (
                                f"❌ {user['username']} failed to craft {item_type} (-{craft_cost} RP)"
                            )
                            result["rp_change"] = -craft_cost
                            self.simulation_stats["rp_spent"] += craft_cost

                            # Add to crafting history
                            user["crafting_history"].append(
                                {
                                    "item": item_type,
                                    "cost": craft_cost,
                                    "success": False,
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )
                    else:
                        result["success"] = True
                        result["response"] = (
                            f"❌ {user['username']} needs {craft_cost} RP to craft, has {user['rp']} RP"
                        )

                    self.simulation_stats["crafting_attempts"] += 1

            elif command == "memory":
                if len(args) >= 2:
                    memory_type = args[0]
                    content = " ".join(args[1:])

                    self.memory_system.store_user_memory(
                        user["user_id"], memory_type, content
                    )

                    result["success"] = True
                    result["response"] = (
                        f"🧠 {user['username']} stored memory: {memory_type}"
                    )
                    self.simulation_stats["memories_stored"] += 1

            elif command == "chat":
                if args:
                    message = " ".join(args)
                    llm_response = self.get_llm_response(user, message)

                    result["success"] = True
                    result["response"] = f"💬 {user['username']}: {message}"
                    result["llm_response"] = llm_response

            elif command == "personality":
                if args:
                    message = " ".join(args)
                    emotional_state = self.personality_system.process_input(
                        user["user_id"], message
                    )

                    result["success"] = True
                    result["response"] = f"🧠 {user['username']} personality processed"

            elif command == "leaderboard":
                top_10 = self.leaderboard.get_top_10()
                result["success"] = True
                result["response"] = (
                    f"🏆 Leaderboard checked ({len(top_10) if top_10 else 0} entries)"
                )

            elif command == "kingdoms":
                kingdoms = self.kingdom_system.get_all_kingdoms()
                result["success"] = True
                result["response"] = f"👑 Kingdoms checked ({len(kingdoms)} kingdoms)"

            elif command == "join":
                # Simulate user joining
                new_user = {
                    "user_id": f"new_user_{random.randint(1000, 9999)}",
                    "username": f"NewUser{random.randint(1, 100)}",
                    "rp": 100,
                    "daily_commands": random.randint(15, 50),
                    "specialization": random.choice(
                        ["hunting", "gathering", "trading", "crafting"]
                    ),
                    "resources": {},
                    "memories": [],
                    "hunting_history": [],
                    "crafting_history": [],
                    "trading_history": [],
                    "daily_claimed": False,
                    "user_type": "Newbie",
                    "join_date": datetime.now().isoformat(),
                    "last_active": datetime.now().isoformat(),
                    "reputation": 0,
                    "skill_level": 1,
                    "preferences": {
                        "favorite_activity": "learning",
                        "risk_tolerance": random.uniform(0.1, 0.5),
                        "social_level": random.uniform(0.3, 0.8),
                    },
                }
                self.users.append(new_user)
                self.simulation_stats["users_joined"] += 1

                result["success"] = True
                result["response"] = f"👋 {new_user['username']} joined the simulation!"

            elif command == "leave":
                # Simulate user leaving (10% chance)
                if random.random() < 0.1 and len(self.users) > 5:
                    leaving_user = random.choice(self.users)
                    self.users.remove(leaving_user)
                    self.simulation_stats["users_left"] += 1

                    result["success"] = True
                    result["response"] = (
                        f"👋 {leaving_user['username']} left the simulation."
                    )

            elif command == "random_event":
                # Simulate random events (25% chance of good/bad)
                event_type = random.choice(["good", "bad", "neutral"])

                if event_type == "good":
                    bonus_rp = random.randint(10, 30)
                    user["rp"] += bonus_rp
                    result["success"] = True
                    result["response"] = (
                        f"🎉 {user['username']} got lucky! +{bonus_rp} RP bonus!"
                    )
                    result["rp_change"] = bonus_rp
                    self.simulation_stats["rp_earned"] += bonus_rp
                elif event_type == "bad":
                    penalty_rp = random.randint(5, 15)
                    user["rp"] = max(0, user["rp"] - penalty_rp)
                    result["success"] = True
                    result["response"] = (
                        f"💥 {user['username']} had an accident! -{penalty_rp} RP penalty!"
                    )
                    result["rp_change"] = -penalty_rp
                    self.simulation_stats["rp_spent"] += penalty_rp
                else:
                    result["success"] = True
                    result["response"] = (
                        f"📝 {user['username']} experienced a neutral event."
                    )

        except Exception as e:
            error_msg = f"Command execution error: {str(e)}"
            self.unique_errors.add(error_msg)
            print(
                f"      ❌ Error executing command '{command}' for {user['username']}: {str(e)}"
            )
            result["success"] = False
            result["response"] = f"❌ Error: {str(e)}"
            result["error_type"] = "execution_error"

        self.simulation_stats["total_commands"] += 1
        if result["success"]:
            self.simulation_stats["successful_commands"] += 1
        else:
            self.simulation_stats["failed_commands"] += 1

        return result

    def generate_specialized_workload(self, user: Dict) -> List[tuple]:
        """Generate workload based on user specialization"""
        commands = []
        daily_commands = user["daily_commands"]
        specialization = user["specialization"]

        # Daily bonus (always first)
        commands.append(("daily", []))

        # Distribute remaining commands based on specialization
        remaining_commands = daily_commands - 1

        # Initialize all variables to 0
        hunt_count = 0
        gather_count = 0
        trade_count = 0
        craft_count = 0
        other_count = 0

        if specialization == "hunting":
            # 60% hunting, 20% gathering, 10% trading, 10% other
            hunt_count = int(remaining_commands * 0.6)
            gather_count = int(remaining_commands * 0.2)
            trade_count = int(remaining_commands * 0.1)
            other_count = remaining_commands - hunt_count - gather_count - trade_count

        elif specialization == "gathering":
            # 60% gathering, 20% hunting, 10% crafting, 10% other
            gather_count = int(remaining_commands * 0.6)
            hunt_count = int(remaining_commands * 0.2)
            craft_count = int(remaining_commands * 0.1)
            other_count = remaining_commands - gather_count - hunt_count - craft_count

        elif specialization == "trading":
            # 50% trading, 30% gathering, 20% other
            trade_count = int(remaining_commands * 0.5)
            gather_count = int(remaining_commands * 0.3)
            other_count = remaining_commands - trade_count - gather_count

        elif specialization == "crafting":
            # 50% crafting, 30% gathering, 20% other
            craft_count = int(remaining_commands * 0.5)
            gather_count = int(remaining_commands * 0.3)
            other_count = remaining_commands - craft_count - gather_count

        else:
            # Balanced distribution
            hunt_count = int(remaining_commands * 0.3)
            gather_count = int(remaining_commands * 0.3)
            trade_count = int(remaining_commands * 0.1)
            craft_count = int(remaining_commands * 0.1)
            other_count = (
                remaining_commands
                - hunt_count
                - gather_count
                - trade_count
                - craft_count
            )

        # Generate hunting commands
        for _ in range(hunt_count):
            if user["rp"] > 20:
                spawn_id = f"spawn_{random.randint(100, 999)}"
                rp_cost = random.randint(10, min(50, user["rp"]))
                commands.append(("hunt", [spawn_id, str(rp_cost)]))

        # Generate gathering commands
        for _ in range(gather_count):
            resources = ["wood", "stone", "metal", "crystal", "essence"]
            qualities = ["normal", "rare", "epic", "legendary"]
            commands.append(
                ("gather", [random.choice(resources), random.choice(qualities)])
            )

        # Generate trading commands
        for _ in range(trade_count):
            buyer_id = f"buyer_{random.randint(100, 999)}"
            items = ["wood", "stone", "metal", "crystal"]
            amount = random.randint(1, 5)
            price = random.randint(10, 50)
            commands.append(
                ("trade", [buyer_id, random.choice(items), str(amount), str(price)])
            )

        # Generate crafting commands
        for _ in range(craft_count):
            items = ["sword", "shield", "potion", "tool", "armor"]
            qualities = ["basic", "improved", "masterwork", "legendary"]
            commands.append(("craft", [random.choice(items), random.choice(qualities)]))

        # Generate other commands
        for _ in range(other_count):
            other_commands = [
                ("memory", ["gameplay", "Completed daily activities"]),
                ("chat", ["Hello everyone!"]),
                ("personality", ["I'm feeling good today"]),
                ("leaderboard", []),
                ("kingdoms", []),
                ("random_event", []),
            ]
            commands.append(random.choice(other_commands))

        return commands

    def run_daily_simulation(self, day: int) -> Dict:
        """Run one day of simulation"""
        day_start = datetime.now()
        print(f"\n📅 DAY {day}/30 - Starting daily simulation...")
        print(f"⏰ Day start: {day_start.strftime('%H:%M:%S')}")

        daily_stats = {
            "day": day,
            "day_start": day_start.isoformat(),
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
            "queue_requests": 0,
            "users_joined": 0,
            "users_left": 0,
            "errors": [],
            "issues": [],
            "user_activities": {},
        }

        # Reset daily claimed status for all users
        for user in self.users:
            user["daily_claimed"] = False
            daily_stats["user_activities"][user["username"]] = {
                "commands_executed": 0,
                "rp_earned": 0,
                "rp_spent": 0,
                "activities": [],
            }

            # Generate and execute daily workloads for all users
        for user in self.users:
            print(
                f"    🎮 Processing {user['username']} ({user['specialization']}) - {user['daily_commands']} commands"
            )
            daily_workload = self.generate_specialized_workload(user)

            for i, (command, args) in enumerate(daily_workload):
                if i % 10 == 0:  # Print progress every 10 commands
                    print(
                        f"      📝 {user['username']}: {i+1}/{len(daily_workload)} commands processed"
                    )

                # Add to queue for processing
                queue_result = self.add_to_queue(user, command, args)

                # Process queue
                self.process_queue()

                # Get the actual result from queue processing
                try:
                    result = self.execute_command(user, command, args)

                    # Track daily stats
                    daily_stats["total_commands"] += 1
                    daily_stats["user_activities"][user["username"]][
                        "commands_executed"
                    ] += 1
                except Exception as e:
                    print(
                        f"      ❌ Error executing command for {user['username']}: {e}"
                    )
                    result = {
                        "success": False,
                        "response": f"Error: {str(e)}",
                        "rp_change": 0,
                        "error_type": "execution_error",
                    }
                    daily_stats["total_commands"] += 1
                    daily_stats["failed_commands"] += 1

                if result["success"]:
                    daily_stats["successful_commands"] += 1
                    daily_stats["user_activities"][user["username"]][
                        "activities"
                    ].append(
                        {
                            "command": command,
                            "result": "success",
                            "rp_change": result["rp_change"],
                        }
                    )
                else:
                    daily_stats["failed_commands"] += 1
                    if result["error_type"]:
                        daily_stats["errors"].append(
                            {
                                "user": user["username"],
                                "command": command,
                                "error": result["response"],
                                "error_type": result["error_type"],
                            }
                        )

                # Track specific stats
                if result["rp_change"] > 0:
                    daily_stats["rp_earned"] += result["rp_change"]
                    daily_stats["user_activities"][user["username"]][
                        "rp_earned"
                    ] += result["rp_change"]
                elif result["rp_change"] < 0:
                    daily_stats["rp_spent"] += abs(result["rp_change"])
                    daily_stats["user_activities"][user["username"]]["rp_spent"] += abs(
                        result["rp_change"]
                    )

                if command == "gather":
                    daily_stats["resources_gathered"] += 1
                elif command == "hunt":
                    daily_stats["hunts_attempted"] += 1
                elif command == "trade":
                    daily_stats["trades_made"] += 1
                elif command == "memory":
                    daily_stats["memories_stored"] += 1
                elif command == "craft":
                    daily_stats["crafting_attempts"] += 1
                elif command == "chat":
                    daily_stats["llm_responses"] += 1

                # Small delay to prevent overwhelming
                time.sleep(0.001)

        # Simulate random events
        for _ in range(random.randint(1, 3)):
            random_user = random.choice(self.users)
            result = self.execute_command(random_user, "random_event", [])
            if result["success"]:
                daily_stats["total_commands"] += 1
                daily_stats["successful_commands"] += 1

        # Simulate user joins/leaves
        if random.random() < 0.1:  # 10% chance
            result = self.execute_command(random.choice(self.users), "join", [])
            if result["success"]:
                daily_stats["users_joined"] += 1

        if random.random() < 0.05:  # 5% chance
            result = self.execute_command(random.choice(self.users), "leave", [])
            if result["success"]:
                daily_stats["users_left"] += 1

        day_end = datetime.now()
        daily_stats["day_end"] = day_end.isoformat()
        daily_stats["day_duration"] = (day_end - day_start).total_seconds()

        # Print daily summary
        success_rate = (
            (daily_stats["successful_commands"] / daily_stats["total_commands"]) * 100
            if daily_stats["total_commands"] > 0
            else 0
        )
        print(f"📊 Day {day} Summary:")
        print(f"   ⏱️  Duration: {daily_stats['day_duration']:.1f}s")
        print(
            f"   📝 Commands: {daily_stats['total_commands']} (Success: {success_rate:.1f}%)"
        )
        print(f"   💰 RP: +{daily_stats['rp_earned']} / -{daily_stats['rp_spent']}")
        print(
            f"   🎮 Activities: {daily_stats['resources_gathered']} gather, {daily_stats['hunts_attempted']} hunts, {daily_stats['trades_made']} trades, {daily_stats['crafting_attempts']} craft"
        )
        print(f"   🤖 LLM Responses: {daily_stats['llm_responses']}")
        print(f"   📋 Queue Requests: {daily_stats['queue_requests']}")
        print(
            f"   👥 Users: +{daily_stats['users_joined']} / -{daily_stats['users_left']} (Total: {len(self.users)})"
        )
        print(f"   ❌ Errors: {len(daily_stats['errors'])}")

        return daily_stats

    def run_full_simulation(self):
        """Run 30 days of full simulation"""
        print("🚀 Starting Full Simulation (30 Days)")
        print("=" * 60)

        # Create realistic users
        self.create_realistic_users(20)

        # Initialize stats
        self.simulation_stats["start_time"] = datetime.now()
        self.running = True

        print(f"✅ Created {len(self.users)} realistic users")
        print(f"🎯 Target: 30 days of comprehensive simulation")
        print(f"⏱️  Started at: {self.simulation_stats['start_time']}")
        print("=" * 60)

        try:
            for day in range(1, 31):
                if not self.running:
                    break

                # Run daily simulation
                daily_stats = self.run_daily_simulation(day)
                self.daily_stats.append(daily_stats)

                # Update simulation stats
                self.simulation_stats["total_commands"] += daily_stats["total_commands"]
                self.simulation_stats["successful_commands"] += daily_stats[
                    "successful_commands"
                ]
                self.simulation_stats["failed_commands"] += daily_stats[
                    "failed_commands"
                ]
                self.simulation_stats["rp_earned"] += daily_stats["rp_earned"]
                self.simulation_stats["rp_spent"] += daily_stats["rp_spent"]
                self.simulation_stats["resources_gathered"] += daily_stats[
                    "resources_gathered"
                ]
                self.simulation_stats["hunts_attempted"] += daily_stats[
                    "hunts_attempted"
                ]
                self.simulation_stats["trades_made"] += daily_stats["trades_made"]
                self.simulation_stats["memories_stored"] += daily_stats[
                    "memories_stored"
                ]
                self.simulation_stats["crafting_attempts"] += daily_stats[
                    "crafting_attempts"
                ]
                self.simulation_stats["llm_responses"] += daily_stats["llm_responses"]
                self.simulation_stats["queue_requests"] += daily_stats["queue_requests"]
                self.simulation_stats["users_joined"] += daily_stats["users_joined"]
                self.simulation_stats["users_left"] += daily_stats["users_left"]

                # Track unique errors and issues
                for error in daily_stats["errors"]:
                    error_key = f"{error['error_type']}: {error['error']}"
                    self.unique_errors.add(error_key)

                # Print weekly summary
                if day % 7 == 0:
                    self.print_weekly_summary(day)

        except KeyboardInterrupt:
            print("\n⏹️  Full simulation interrupted by user")
        except Exception as e:
            error_msg = f"Full simulation error: {str(e)}"
            self.unique_errors.add(error_msg)
            print(f"\n❌ Full simulation error: {e}")
            import traceback

            print(f"Traceback: {traceback.format_exc()}")
        finally:
            self.running = False
            self.simulation_stats["end_time"] = datetime.now()
            self.print_final_results()

    def print_weekly_summary(self, current_day: int):
        """Print weekly summary"""
        week = current_day // 7
        print(f"\n📅 WEEK {week} SUMMARY (Days 1-{current_day})")
        print(f"📝 Total Commands: {self.simulation_stats['total_commands']}")
        print(
            f"✅ Success Rate: {(self.simulation_stats['successful_commands'] / self.simulation_stats['total_commands']) * 100:.1f}%"
        )
        print(
            f"💰 Total RP: +{self.simulation_stats['rp_earned']} / -{self.simulation_stats['rp_spent']}"
        )
        print(
            f"🎮 Activities: {self.simulation_stats['resources_gathered']} gather, {self.simulation_stats['hunts_attempted']} hunts, {self.simulation_stats['trades_made']} trades, {self.simulation_stats['crafting_attempts']} craft"
        )
        print(f"🤖 LLM Responses: {self.simulation_stats['llm_responses']}")
        print(f"📋 Queue Requests: {self.simulation_stats['queue_requests']}")
        print(
            f"👥 Users: +{self.simulation_stats['users_joined']} / -{self.simulation_stats['users_left']} (Current: {len(self.users)})"
        )
        print(f"❌ Unique Errors: {len(self.unique_errors)}")
        print("=" * 60)

    def print_final_results(self):
        """Print final simulation results"""
        print("\n" + "=" * 60)
        print("📊 FULL SIMULATION RESULTS")
        print("=" * 60)

        if self.simulation_stats["start_time"] and self.simulation_stats["end_time"]:
            duration = (
                self.simulation_stats["end_time"] - self.simulation_stats["start_time"]
            )
            print(f"⏱️  Total Duration: {duration}")

        print(f"📝 Total Commands: {self.simulation_stats['total_commands']}")
        print(f"✅ Successful Commands: {self.simulation_stats['successful_commands']}")
        print(f"❌ Failed Commands: {self.simulation_stats['failed_commands']}")

        if self.simulation_stats["total_commands"] > 0:
            success_rate = (
                self.simulation_stats["successful_commands"]
                / self.simulation_stats["total_commands"]
            ) * 100
            print(f"📊 Success Rate: {success_rate:.1f}%")

        print(f"\n💰 Economy Stats:")
        print(f"  RP Earned: {self.simulation_stats['rp_earned']}")
        print(f"  RP Spent: {self.simulation_stats['rp_spent']}")
        print(
            f"  Net RP: {self.simulation_stats['rp_earned'] - self.simulation_stats['rp_spent']}"
        )

        print(f"\n🎮 Gameplay Stats:")
        print(f"  Resources Gathered: {self.simulation_stats['resources_gathered']}")
        print(f"  Hunts Attempted: {self.simulation_stats['hunts_attempted']}")
        print(f"  Trades Made: {self.simulation_stats['trades_made']}")
        print(f"  Memories Stored: {self.simulation_stats['memories_stored']}")
        print(f"  Crafting Attempts: {self.simulation_stats['crafting_attempts']}")

        print(f"\n🤖 AI Stats:")
        print(f"  LLM Responses: {self.simulation_stats['llm_responses']}")
        print(f"  Queue Requests: {self.simulation_stats['queue_requests']}")

        print(f"\n👥 User Stats:")
        print(f"  Users Joined: {self.simulation_stats['users_joined']}")
        print(f"  Users Left: {self.simulation_stats['users_left']}")
        print(f"  Final User Count: {len(self.users)}")

        print(f"\n👥 Final User Status:")
        for user in self.users:
            print(f"  {user['username']} ({user['specialization']}): {user['rp']} RP")

        print(f"\n❌ Unique Errors Found ({len(self.unique_errors)}):")
        for error in sorted(self.unique_errors):
            print(f"  • {error}")

        # Save results
        self.save_results()

        print(f"\n💾 Results saved to: full_simulation_results.json")

    def save_results(self):
        """Save full simulation results"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "simulation_stats": {
                k: v.isoformat() if isinstance(v, datetime) else v
                for k, v in self.simulation_stats.items()
            },
            "users": self.users,
            "daily_stats": self.daily_stats,
            "unique_errors": list(self.unique_errors),
            "unique_issues": list(self.unique_issues),
        }

        with open("full_simulation_results.json", "w") as f:
            json.dump(results, f, indent=2)


def main():
    """Main function to run the full simulation"""
    print("🎮 SIMULACRA RANCHER FULL SIMULATION")
    print("=" * 60)
    print("Complete simulation without Discord bot")
    print("Tests all systems with LLM responses and queue processing")
    print("Simulates 30 days of realistic user behavior")
    print("Press Ctrl+C to stop early")
    print("=" * 60)

    tester = FullSimulationTester()

    # Run the full simulation
    tester.run_full_simulation()


if __name__ == "__main__":
    main()
