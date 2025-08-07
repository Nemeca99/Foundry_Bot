#!/usr/bin/env python3
"""
Monthly Simulation Test for Simulacra Rancher
Simulates 30 days of real usage with realistic daily workloads
Tracks unique errors/issues for debugging without repetition
"""

import sys
import os
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
import threading

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class MonthlySimulationTester:
    """Monthly simulation tester with realistic daily workloads"""
    
    def __init__(self):
        self.test_results = []
        self.unique_errors = set()  # Track unique errors only
        self.unique_issues = set()  # Track unique issues only
        self.daily_stats = []
        self.monthly_stats = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "rp_earned": 0,
            "rp_spent": 0,
            "resources_gathered": 0,
            "hunts_attempted": 0,
            "trades_made": 0,
            "memories_stored": 0,
            "unique_errors": 0,
            "unique_issues": 0,
            "start_time": None,
            "end_time": None
        }
        self.running = False
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
            
            print("✅ All systems initialized for monthly simulation!")
            
        except Exception as e:
            print(f"❌ Error initializing systems: {e}")
            raise
    
    def create_realistic_users(self, num_users: int = 15):
        """Create realistic users with different activity patterns"""
        self.users = []
        user_types = [
            {"name": "Active", "daily_commands": 50, "rp_start": 200},
            {"name": "Casual", "daily_commands": 25, "rp_start": 150},
            {"name": "Hardcore", "daily_commands": 100, "rp_start": 300},
            {"name": "Newbie", "daily_commands": 15, "rp_start": 100},
            {"name": "Veteran", "daily_commands": 75, "rp_start": 250}
        ]
        
        for i in range(num_users):
            user_type = random.choice(user_types)
            user_id = f"monthly_user_{i+1}"
            username = f"{user_type['name']}User{i+1}"
            user = {
                "user_id": user_id,
                "username": username,
                "rp": user_type["rp_start"],
                "daily_commands": user_type["daily_commands"],
                "resources": {},
                "memories": [],
                "hunting_history": [],
                "daily_claimed": False,
                "user_type": user_type["name"]
            }
            self.users.append(user)
        
        print(f"✅ Created {num_users} realistic users with different activity patterns")
        return self.users
    
    def get_random_user(self):
        """Get a random user for testing"""
        return random.choice(self.users)
    
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
            "error_type": None
        }
        
        try:
            if command == "daily":
                # Claim daily bonus (only once per day)
                if not user.get("daily_claimed", False):
                    daily_bonus = 50
                    user["rp"] += daily_bonus
                    user["daily_claimed"] = True
                    result["success"] = True
                    result["response"] = f"🎁 {user['username']} claimed daily bonus: +{daily_bonus} RP"
                    result["rp_change"] = daily_bonus
                    self.monthly_stats["rp_earned"] += daily_bonus
                else:
                    result["success"] = True
                    result["response"] = f"⏰ {user['username']} already claimed daily bonus"
                
            elif command == "gather":
                if len(args) >= 2:
                    resource_type = args[0]
                    quality = args[1]
                    
                    # Start gathering
                    self.resource_system.start_gathering(user["user_id"], resource_type, quality)
                    resources = self.resource_system.get_user_resources(user["user_id"])
                    
                    result["success"] = True
                    result["response"] = f"🌲 {user['username']} gathered {resource_type} ({quality})"
                    self.monthly_stats["resources_gathered"] += 1
                    
            elif command == "hunt":
                if len(args) >= 2:
                    spawn_id = args[0]
                    rp_cost = int(args[1])
                    
                    if user["rp"] >= rp_cost:
                        try:
                            # Attempt to catch
                            from core.hunting_system import HuntingEvent
                            spawn_event = self.hunting_system.create_spawn_event(
                                HuntingEvent.WILD_SPAWN, "monthly_test_channel"
                            )
                            
                            catch_result = self.hunting_system.attempt_catch(
                                user["user_id"], spawn_event["spawn_id"], rp_cost
                            )
                            
                            if catch_result.get("success"):
                                user["rp"] -= rp_cost
                                result["success"] = True
                                result["response"] = f"🎯 {user['username']} caught Simulacra! (-{rp_cost} RP)"
                                result["rp_change"] = -rp_cost
                                self.monthly_stats["rp_spent"] += rp_cost
                            else:
                                result["success"] = True
                                result["response"] = f"❌ {user['username']} failed to catch: {catch_result.get('error', 'Unknown')}"
                            
                            self.monthly_stats["hunts_attempted"] += 1
                        except Exception as e:
                            error_msg = f"Database locked during hunt: {str(e)}"
                            self.unique_errors.add(error_msg)
                            result["success"] = False
                            result["response"] = f"🔒 Database locked, retry later"
                            result["error_type"] = "database_locked"
                    else:
                        result["success"] = True
                        result["response"] = f"❌ {user['username']} needs {rp_cost} RP, has {user['rp']} RP"
                        
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
                        result["response"] = f"🤝 {user['username']} created trade: {amount}x {item} for {price} RP"
                        self.monthly_stats["trades_made"] += 1
                    else:
                        result["success"] = True
                        result["response"] = f"❌ Trade failed: {trade_result.get('error', 'Unknown')}"
                        
            elif command == "memory":
                if len(args) >= 2:
                    memory_type = args[0]
                    content = " ".join(args[1:])
                    
                    self.memory_system.store_user_memory(user["user_id"], memory_type, content)
                    
                    result["success"] = True
                    result["response"] = f"🧠 {user['username']} stored memory: {memory_type}"
                    self.monthly_stats["memories_stored"] += 1
                    
            elif command == "personality":
                if args:
                    message = " ".join(args)
                    emotional_state = self.personality_system.process_input(user["user_id"], message)
                    
                    result["success"] = True
                    result["response"] = f"🧠 {user['username']} personality processed"
                    
            elif command == "leaderboard":
                top_10 = self.leaderboard.get_top_10()
                result["success"] = True
                result["response"] = f"🏆 Leaderboard checked ({len(top_10) if top_10 else 0} entries)"
                
            elif command == "kingdoms":
                kingdoms = self.kingdom_system.get_all_kingdoms()
                result["success"] = True
                result["response"] = f"👑 Kingdoms checked ({len(kingdoms)} kingdoms)"
                
        except Exception as e:
            error_msg = f"Command execution error: {str(e)}"
            self.unique_errors.add(error_msg)
            result["success"] = False
            result["response"] = f"❌ Error: {str(e)}"
            result["error_type"] = "execution_error"
            
        self.monthly_stats["total_commands"] += 1
        if result["success"]:
            self.monthly_stats["successful_commands"] += 1
        else:
            self.monthly_stats["failed_commands"] += 1
            
        return result
    
    def generate_daily_workload(self, user: Dict) -> List[tuple]:
        """Generate realistic daily workload for a user"""
        commands = []
        daily_commands = user["daily_commands"]
        
        # Daily bonus (always first)
        commands.append(("daily", []))
        
        # Distribute remaining commands based on user type
        remaining_commands = daily_commands - 1
        
        # Resource gathering (40% of remaining)
        gather_count = int(remaining_commands * 0.4)
        for _ in range(gather_count):
            resources = ["wood", "stone", "metal", "crystal", "essence"]
            qualities = ["normal", "rare", "epic", "legendary"]
            commands.append(("gather", [random.choice(resources), random.choice(qualities)]))
        
        # Hunting (30% of remaining)
        hunt_count = int(remaining_commands * 0.3)
        for _ in range(hunt_count):
            if user["rp"] > 20:
                spawn_id = f"spawn_{random.randint(100, 999)}"
                rp_cost = random.randint(10, min(50, user["rp"]))
                commands.append(("hunt", [spawn_id, str(rp_cost)]))
        
        # Trading (10% of remaining)
        trade_count = int(remaining_commands * 0.1)
        for _ in range(trade_count):
            buyer_id = f"buyer_{random.randint(100, 999)}"
            items = ["wood", "stone", "metal", "crystal"]
            amount = random.randint(1, 5)
            price = random.randint(10, 50)
            commands.append(("trade", [buyer_id, random.choice(items), str(amount), str(price)]))
        
        # Memory storage (15% of remaining)
        memory_count = int(remaining_commands * 0.15)
        for _ in range(memory_count):
            memory_types = ["gameplay", "social", "achievement", "learning"]
            contents = [
                "Completed a successful hunt",
                "Made a new friend",
                "Learned new strategy",
                "Achieved milestone",
                "Explored new area",
                "Discovered rare resource",
                "Joined kingdom",
                "Won competition",
                "Built something amazing",
                "Helped another player"
            ]
            commands.append(("memory", [random.choice(memory_types), random.choice(contents)]))
        
        # Personality interaction (5% of remaining)
        personality_count = int(remaining_commands * 0.05)
        for _ in range(personality_count):
            messages = [
                "I'm feeling excited about hunting",
                "This game is really fun",
                "I want to improve my skills",
                "The community is great",
                "I love the kingdom system",
                "Trading is interesting",
                "I'm learning new strategies",
                "The AI is so helpful",
                "I feel like I'm getting better",
                "This is my favorite game"
            ]
            commands.append(("personality", [random.choice(messages)]))
        
        return commands
    
    def run_daily_simulation(self, day: int) -> Dict:
        """Run one day of simulation"""
        print(f"\n📅 DAY {day}/30 - Starting daily simulation...")
        
        daily_stats = {
            "day": day,
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "rp_earned": 0,
            "rp_spent": 0,
            "resources_gathered": 0,
            "hunts_attempted": 0,
            "trades_made": 0,
            "memories_stored": 0,
            "errors": [],
            "issues": []
        }
        
        # Reset daily claimed status for all users
        for user in self.users:
            user["daily_claimed"] = False
        
        # Generate and execute daily workloads for all users
        for user in self.users:
            daily_workload = self.generate_daily_workload(user)
            
            for command, args in daily_workload:
                result = self.execute_command(user, command, args)
                
                # Track daily stats
                daily_stats["total_commands"] += 1
                if result["success"]:
                    daily_stats["successful_commands"] += 1
                else:
                    daily_stats["failed_commands"] += 1
                    if result["error_type"]:
                        daily_stats["errors"].append({
                            "user": user["username"],
                            "command": command,
                            "error": result["response"],
                            "error_type": result["error_type"]
                        })
                
                # Track specific stats
                if result["rp_change"] > 0:
                    daily_stats["rp_earned"] += result["rp_change"]
                elif result["rp_change"] < 0:
                    daily_stats["rp_spent"] += abs(result["rp_change"])
                
                if command == "gather":
                    daily_stats["resources_gathered"] += 1
                elif command == "hunt":
                    daily_stats["hunts_attempted"] += 1
                elif command == "trade":
                    daily_stats["trades_made"] += 1
                elif command == "memory":
                    daily_stats["memories_stored"] += 1
                
                # Small delay to prevent overwhelming
                time.sleep(0.001)
        
        # Print daily summary
        success_rate = (daily_stats["successful_commands"] / daily_stats["total_commands"]) * 100 if daily_stats["total_commands"] > 0 else 0
        print(f"📊 Day {day} Summary:")
        print(f"   Commands: {daily_stats['total_commands']} (Success: {success_rate:.1f}%)")
        print(f"   RP: +{daily_stats['rp_earned']} / -{daily_stats['rp_spent']}")
        print(f"   Activities: {daily_stats['resources_gathered']} gather, {daily_stats['hunts_attempted']} hunts, {daily_stats['trades_made']} trades, {daily_stats['memories_stored']} memories")
        print(f"   Errors: {len(daily_stats['errors'])}")
        
        return daily_stats
    
    def run_monthly_simulation(self):
        """Run 30 days of simulation"""
        print("🚀 Starting Monthly Simulation (30 Days)")
        print("="*60)
        
        # Create realistic users
        self.create_realistic_users(15)
        
        # Initialize stats
        self.monthly_stats["start_time"] = datetime.now()
        self.running = True
        
        print(f"✅ Created {len(self.users)} realistic users")
        print(f"🎯 Target: 30 days of realistic daily workloads")
        print(f"⏱️  Started at: {self.monthly_stats['start_time']}")
        print("="*60)
        
        try:
            for day in range(1, 31):
                if not self.running:
                    break
                
                # Run daily simulation
                daily_stats = self.run_daily_simulation(day)
                self.daily_stats.append(daily_stats)
                
                # Update monthly stats
                self.monthly_stats["total_commands"] += daily_stats["total_commands"]
                self.monthly_stats["successful_commands"] += daily_stats["successful_commands"]
                self.monthly_stats["failed_commands"] += daily_stats["failed_commands"]
                self.monthly_stats["rp_earned"] += daily_stats["rp_earned"]
                self.monthly_stats["rp_spent"] += daily_stats["rp_spent"]
                self.monthly_stats["resources_gathered"] += daily_stats["resources_gathered"]
                self.monthly_stats["hunts_attempted"] += daily_stats["hunts_attempted"]
                self.monthly_stats["trades_made"] += daily_stats["trades_made"]
                self.monthly_stats["memories_stored"] += daily_stats["memories_stored"]
                
                # Track unique errors and issues
                for error in daily_stats["errors"]:
                    error_key = f"{error['error_type']}: {error['error']}"
                    self.unique_errors.add(error_key)
                
                # Print weekly summary
                if day % 7 == 0:
                    self.print_weekly_summary(day)
                
        except KeyboardInterrupt:
            print("\n⏹️  Monthly simulation interrupted by user")
        except Exception as e:
            print(f"\n❌ Monthly simulation error: {e}")
        finally:
            self.running = False
            self.monthly_stats["end_time"] = datetime.now()
            self.print_final_results()
    
    def print_weekly_summary(self, current_day: int):
        """Print weekly summary"""
        week = current_day // 7
        print(f"\n📅 WEEK {week} SUMMARY (Days 1-{current_day})")
        print(f"📝 Total Commands: {self.monthly_stats['total_commands']}")
        print(f"✅ Success Rate: {(self.monthly_stats['successful_commands'] / self.monthly_stats['total_commands']) * 100:.1f}%")
        print(f"💰 Total RP: +{self.monthly_stats['rp_earned']} / -{self.monthly_stats['rp_spent']}")
        print(f"🎮 Activities: {self.monthly_stats['resources_gathered']} gather, {self.monthly_stats['hunts_attempted']} hunts")
        print(f"❌ Unique Errors: {len(self.unique_errors)}")
        print("="*60)
    
    def print_final_results(self):
        """Print final monthly results"""
        print("\n" + "="*60)
        print("📊 MONTHLY SIMULATION RESULTS")
        print("="*60)
        
        if self.monthly_stats["start_time"] and self.monthly_stats["end_time"]:
            duration = self.monthly_stats["end_time"] - self.monthly_stats["start_time"]
            print(f"⏱️  Total Duration: {duration}")
        
        print(f"📝 Total Commands: {self.monthly_stats['total_commands']}")
        print(f"✅ Successful Commands: {self.monthly_stats['successful_commands']}")
        print(f"❌ Failed Commands: {self.monthly_stats['failed_commands']}")
        
        if self.monthly_stats['total_commands'] > 0:
            success_rate = (self.monthly_stats['successful_commands'] / self.monthly_stats['total_commands']) * 100
            print(f"📊 Success Rate: {success_rate:.1f}%")
        
        print(f"\n💰 Economy Stats:")
        print(f"  RP Earned: {self.monthly_stats['rp_earned']}")
        print(f"  RP Spent: {self.monthly_stats['rp_spent']}")
        print(f"  Net RP: {self.monthly_stats['rp_earned'] - self.monthly_stats['rp_spent']}")
        
        print(f"\n🎮 Gameplay Stats:")
        print(f"  Resources Gathered: {self.monthly_stats['resources_gathered']}")
        print(f"  Hunts Attempted: {self.monthly_stats['hunts_attempted']}")
        print(f"  Trades Made: {self.monthly_stats['trades_made']}")
        print(f"  Memories Stored: {self.monthly_stats['memories_stored']}")
        
        print(f"\n👥 Final User Status:")
        for user in self.users:
            print(f"  {user['username']} ({user['user_type']}): {user['rp']} RP")
        
        print(f"\n❌ Unique Errors Found ({len(self.unique_errors)}):")
        for error in sorted(self.unique_errors):
            print(f"  • {error}")
        
        # Save results
        self.save_results()
        
        print(f"\n💾 Results saved to: monthly_simulation_results.json")
    
    def save_results(self):
        """Save monthly simulation results"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "monthly_stats": {
                k: v.isoformat() if isinstance(v, datetime) else v 
                for k, v in self.monthly_stats.items()
            },
            "users": self.users,
            "daily_stats": self.daily_stats,
            "unique_errors": list(self.unique_errors),
            "unique_issues": list(self.unique_issues)
        }
        
        with open("monthly_simulation_results.json", "w") as f:
            json.dump(results, f, indent=2)

def main():
    """Main function to run the monthly simulation"""
    print("📅 SIMULACRA RANCHER MONTHLY SIMULATION")
    print("="*60)
    print("Simulates 30 days of realistic daily workloads")
    print("Tracks unique errors/issues for debugging")
    print("Press Ctrl+C to stop early")
    print("="*60)
    
    tester = MonthlySimulationTester()
    
    # Run the monthly simulation
    tester.run_monthly_simulation()

if __name__ == "__main__":
    main() 