# 🔄 **SIM-RANCHER SIMULATION DOCUMENTATION**

## 🎯 **SIMULATION OVERVIEW**

The Sim-Rancher simulation suite provides comprehensive testing and validation of the game's core systems, including the mod system, economy, user behavior, and AI integration.

---

## 🚀 **QUICK START**

### **Main Launcher**
```bash
cd simulation
launch_simulation.bat
```

### **Direct Commands**
```bash
# Infinite simulation (runs until Ctrl+C)
python infinite_simulation_engine.py

# Full simulation (5 minutes)
python full_simulation_engine.py

# Quick test (30 seconds)
python quick_test_sim.py
```

---

## 📁 **SIMULATION STRUCTURE**

### **Organized Folder Structure**
```
simulation/
├── 📄 README.md                    # This documentation
├── 🚀 launch_simulation.bat        # Main launcher menu
├── 🌍 infinite_simulation_engine.py # Infinite simulation with day tracking
├── 🎮 full_simulation_engine.py    # 5-minute complete simulation
├── ⚡ quick_test_sim.py            # 30-second validation test
├── 📁 engines/                     # All simulation engines
├── 📁 tests/                       # Test files and validation
├── 📁 results/                     # All simulation results
├── 📁 batch_files/                 # Batch launcher files
├── 📁 demos/                       # Demo and example files
├── 📁 data/                        # Database files
├── 📁 logs/                        # Log files
└── 📁 archive/                     # Old versions
```

---

## 🌍 **INFINITE SIMULATION ENGINE**

### **Features**
- **Real-time Tick System**: 1 tick = 1 real second
- **Day Tracking**: 86,400 ticks = 1 simulated day (24 hours)
- **Dynamic User Population**: 100 initial users, realistic join/leave rates
- **Concurrent Activities**: Up to 5 activities per user simultaneously
- **Event Flocking**: Users react to positive/negative world events
- **Drone Tracking**: Gain/loss tracking, death on channel moves
- **Global Reward Multiplier**: Player-driven economy system

### **Configuration**
```python
# Simulation settings
self.ticks_per_day = 86400  # 24 hours * 60 minutes * 60 seconds
self.initial_user_count = 100
self.max_users = 500
self.min_users = 50
self.user_join_rate = 0.05  # 5% chance per day for new user
self.user_leave_rate = 0.02  # 2% chance per day for user to leave
```

### **User Types**
```python
@dataclass
class UserType(Enum):
    NOOB = "Noob"           # 0-100 RP, basic activities
    CASUAL = "Casual"       # 100-500 RP, moderate engagement
    REGULAR = "Regular"     # 500-1000 RP, consistent activity
    VETERAN = "Veteran"     # 1000-2000 RP, advanced features
    EXPERT = "Expert"       # 2000-5000 RP, mastery level
    MASTER = "Master"       # 5000+ RP, legendary status
```

### **Activities**
- **Hunting**: RP-based Simulacra catching
- **Modding**: Mod system testing and development
- **Economy**: Trading and resource management
- **Fighting**: New combat system with rewards/risks

---

## 🎮 **FULL SIMULATION ENGINE**

### **Features**
- **Complete Game Experience**: All systems active
- **20 Users**: Different personalities and preferences
- **Dynamic Economy**: Real-time economic cycles
- **World Events**: Random events affecting gameplay
- **5-Minute Duration**: Quick but comprehensive test

### **User Generation**
```python
def create_simulation_users(self):
    """Create users with different personalities."""
    user_types = [UserType.NOOB, UserType.CASUAL, UserType.REGULAR, 
                  UserType.VETERAN, UserType.EXPERT, UserType.MASTER]
    
    for i in range(self.user_count):
        user_type = random.choice(user_types)
        user = SimulationUser(
            id=f"user_{i}",
            name=f"User{i}",
            user_type=user_type,
            rp=random.randint(100, 5000),
            personality_traits=generate_personality_traits(),
            preferred_activities=generate_preferred_activities()
        )
        self.users[user.id] = user
```

---

## ⚡ **QUICK TEST SIMULATION**

### **Features**
- **30-Second Duration**: Fast validation test
- **10 Users**: Reduced complexity for quick testing
- **Core Systems**: Essential functionality testing
- **Error Detection**: Rapid issue identification

### **Test Coverage**
- User creation and management
- Activity generation and processing
- Economy calculations
- World event generation
- Basic statistics tracking

---

## 🎯 **MOD SYSTEM INTEGRATION**

### **Symbolic Game Structure**
```python
# Mirror core game files for isolated testing
symbolic_files = {
    "core/clds.py": "simulation/symbolic/clds.py",
    "core/economy.py": "simulation/symbolic/economy.py",
    "core/hunting_system.py": "simulation/symbolic/hunting_system.py"
}
```

### **Mod Template System**
```python
@dataclass
class ModTemplate:
    mod_id: str
    creator_id: str
    name: str
    description: str
    category: str
    cost_rp: int
    daily_upkeep: int
    effects: Dict[str, Any]
    requirements: Dict[str, Any]
    version: str = "1.0.0"
    approved: bool = False
    created_at: str = ""
    downloads: int = 0
    rating: float = 0.0
```

### **Global Reward Multiplier (SGRM)**
```python
def calculate_global_multiplier(self):
    """Calculate global reward multiplier."""
    if self.drones_ever_died == 0:
        return 1.0
    
    multiplier = (self.drones_alive * self.active_players) / self.drones_ever_died
    return max(0.1, min(3.0, multiplier))
```

---

## 💰 **ENTROPY COMPRESSION ECONOMY**

### **Formula**
```python
def calculate_compression_cost(self, base_cost: int, ticks_requested: int, global_multiplier: float) -> int:
    """Calculate cost for entropy compression."""
    compression_multiplier = max(0.1, min(3.0, global_multiplier))
    
    if ticks_requested <= 1:
        return base_cost
    
    # Exponential scaling for bulk actions
    total_cost = (base_cost * 2) * (ticks_requested * compression_multiplier)
    return int(total_cost)
```

### **Example Calculations**
```python
# 10x hunt with 100 RP base cost and 1.5x global multiplier
base_cost = 100
ticks = 10
global_multiplier = 1.5

total_cost = (100 * 2) * (10 * 1.5) = 3000 RP
```

---

## 📊 **SIMULATION STATISTICS**

### **User Statistics**
```python
@dataclass
class SimulationUser:
    id: str
    name: str
    user_type: UserType
    rp: int = 100
    total_rp_earned: int = 0
    total_rp_spent: int = 0
    
    # Activity tracking
    hunt_ticks: int = 0
    hunt_successes: int = 0
    mod_ticks: int = 0
    mod_successes: int = 0
    economy_ticks: int = 0
    economy_successes: int = 0
    fight_ticks: int = 0
    fight_successes: int = 0
    
    # Drone tracking
    drone_count: int = 5
    total_drones_gained: int = 0
    total_drones_lost: int = 0
    max_drones: int = 20
    
    # Enhanced statistics
    total_activities_completed: int = 0
    total_events_participated: int = 0
    total_channel_moves: int = 0
    total_simulacra_deaths: int = 0
    
    # Concurrent activities
    current_concurrent_activities: int = 0
    max_concurrent_activities: int = 5
    
    # Event flocking
    event_preferences: Dict[str, float] = None
    last_event_reaction: float = 0.0
```

### **Global Statistics**
```python
self.stats = {
    "total_ticks": 0,
    "total_users": 0,
    "active_users": 0,
    "total_rp_earned": 0,
    "total_rp_spent": 0,
    "total_activities": 0,
    "total_events": 0,
    "global_multiplier": 1.0,
    "drones_alive": 0,
    "drones_ever_died": 1,
    "active_players": 0,
    
    # User base statistics
    "total_users_joined": 0,
    "total_users_left": 0,
    "peak_users": 0,
    
    # Drone statistics
    "total_drones_gained": 0,
    "total_drones_lost": 0,
    "total_simulacra_deaths": 0,
    "total_channel_moves": 0
}
```

---

## 🎨 **DISPLAY SYSTEM**

### **Real-time Status Display**
```python
def display_simulation_status(self):
    """Display real-time simulation status."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 80)
    print("🌍 SIM-RANCHER INFINITE SIMULATION ENGINE")
    print("=" * 80)
    
    # Simulation info
    print(f"⏱️  Tick: {self.tick_count:,} | Day: {self.current_day} | Progress: {day_progress:.1f}%")
    print(f"🌍 Global Multiplier: {self.global_multiplier:.2f}x")
    print(f"👥 Active Users: {len(self.users)} | Online: {online_count}")
    print(f"🤖 Drones Alive: {self.drones_alive} | Total Died: {self.drones_ever_died}")
    
    # User base statistics
    print("\n" + "=" * 40)
    print("📊 USER BASE STATISTICS")
    print("=" * 40)
    print(f"Current Sub Count: {self.current_user_count}")
    print(f"Active/Online: {online_count} | Offline: {offline_count}")
    print(f"Peak Users: {self.stats['peak_users']}")
    print(f"Total Joined: {self.stats['total_users_joined']} | Total Left: {self.stats['total_users_left']}")
    print(f"Today: +{self.users_joined_today} | -{self.users_left_today}")
    print(f"Avg Daily Growth: {avg_daily_growth:.1f}")
    
    # Drone statistics
    print("\n" + "=" * 40)
    print("🤖 DRONE STATISTICS")
    print("=" * 40)
    print(f"Total Drones: {total_drones}")
    print(f"Total Gained: {self.stats['total_drones_gained']} | Total Lost: {self.stats['total_drones_lost']}")
    print(f"Net Change: {net_drone_change:+}")
    print(f"Avg Drones/User: {avg_drones_per_user:.1f}")
    
    # User summary
    print("\n" + "=" * 40)
    print("👥 USER SUMMARY")
    print("=" * 40)
    for user_type in UserType:
        users_of_type = [u for u in self.users.values() if u.user_type == user_type]
        if users_of_type:
            online_count = sum(1 for u in users_of_type if u.is_online)
            active_count = sum(1 for u in users_of_type if u.current_activity != "idle")
            avg_rp = sum(u.rp for u in users_of_type) / len(users_of_type)
            avg_drones = sum(u.drone_count for u in users_of_type) / len(users_of_type)
            avg_concurrent = sum(u.current_concurrent_activities for u in users_of_type) / len(users_of_type)
            
            print(f"{user_type.value:8} | {len(users_of_type):2} users | {online_count:2} online | {active_count:2} active | {avg_rp:6.0f} avg RP | {avg_drones:4.1f} drones | {avg_concurrent:4.1f} concurrent")
    
    # Recent world events
    print("\n" + "=" * 40)
    print("🌍 RECENT WORLD EVENTS")
    print("=" * 40)
    for event in self.world_events[-5:]:
        status = "✅" if event.get("is_positive", False) else "❌"
        print(f"{status} {event['description']}")
    
    print("\n" + "=" * 80)
    print("Press Ctrl+C to stop simulation")
    print("=" * 80)
```

---

## 🔄 **ACTIVITY SYSTEM**

### **Activity Generation**
```python
def generate_user_activity(self, user_id: str):
    """Generate a new activity for a user."""
    user = self.users[user_id]
    
    if not user.can_start_activity():
        return
    
    # Determine activity based on preferences and events
    if user.event_preferences and random.random() < 0.3:
        # Event-driven activity
        preferred_events = [k for k, v in user.event_preferences.items() if v > 0.5]
        if preferred_events:
            event_type = random.choice(preferred_events)
            activity_type = f"event_{event_type}"
        else:
            activity_type = random.choice(user.preferred_activities)
    else:
        # Normal activity
        activity_type = random.choice(user.preferred_activities)
    
    # Start activity
    if activity_type == "hunt":
        self.start_user_hunt(user_id)
    elif activity_type == "mod":
        self.start_user_mod(user_id)
    elif activity_type == "economy":
        self.start_user_economy(user_id)
    elif activity_type == "fight":
        self.start_user_fight(user_id)
```

### **Activity Processing**
```python
def process_activity(self, user_id: str, activity_id: str):
    """Process an ongoing activity."""
    user = self.users[user_id]
    activity = self.active_activities.get(activity_id)
    
    if not activity:
        return
    
    # Update activity progress
    activity["ticks"] += 1
    
    # Check for completion
    if activity["ticks"] >= activity["duration"]:
        # Complete activity
        success_rate = self.get_activity_success_rate(activity["type"], user)
        
        if random.random() < success_rate:
            # Success
            reward = self.calculate_activity_reward(activity["type"], user)
            user.rp += reward
            user.total_rp_earned += reward
            activity["success"] = True
        else:
            # Failure
            activity["success"] = False
        
        # End activity
        user.end_activity()
        del self.active_activities[activity_id]
        
        # Update statistics
        user.total_activities_completed += 1
```

---

## 🌍 **WORLD EVENTS**

### **Event Generation**
```python
def generate_world_event(self):
    """Generate a random world event."""
    if random.random() < 0.02:  # 2% chance per tick
        event_types = [
            "economic_boom", "economic_crash", "resource_surge", "resource_shortage",
            "drone_invasion", "peace_treaty", "technological_breakthrough", "natural_disaster"
        ]
        
        event_type = random.choice(event_types)
        is_positive = event_type in ["economic_boom", "resource_surge", "peace_treaty", "technological_breakthrough"]
        
        event = {
            "type": event_type,
            "description": f"World Event: {event_type.replace('_', ' ').title()}",
            "is_positive": is_positive,
            "timestamp": time.time()
        }
        
        self.world_events.append(event)
        
        # Update user preferences based on event
        for user in self.users.values():
            user.react_to_event(event_type, is_positive)
```

### **Event Flocking**
```python
def react_to_event(self, event_type: str, is_positive: bool):
    """Update user preferences based on world event."""
    if not self.event_preferences:
        self.event_preferences = {}
    
    # Adjust preferences based on event
    if is_positive:
        self.event_preferences[event_type] = self.event_preferences.get(event_type, 0.5) + 0.2
    else:
        self.event_preferences[event_type] = self.event_preferences.get(event_type, 0.5) - 0.1
    
    # Clamp values
    self.event_preferences[event_type] = max(0.0, min(1.0, self.event_preferences[event_type]))
    self.last_event_reaction = time.time()
```

---

## 🤖 **DRONE SYSTEM**

### **Drone Management**
```python
def gain_drone(self, reason: str = "activity") -> bool:
    """Gain a drone through activity."""
    if self.drone_count < self.max_drones:
        self.drone_count += 1
        self.total_drones_gained += 1
        return True
    return False

def lose_drone(self, reason: str = "activity") -> bool:
    """Lose a drone through activity or death."""
    if self.drone_count > 0:
        self.drone_count -= 1
        self.total_drones_lost += 1
        return True
    return False
```

### **Channel Move Death**
```python
def simulate_channel_move(self, user_id: str) -> bool:
    """Simulate a user moving channels with 1% chance of drone death."""
    user = self.users[user_id]
    
    # 1% chance of simulacra death when moving channels
    if random.random() < 0.01:
        if user.lose_drone("channel_move"):
            user.total_channel_moves += 1
            user.total_simulacra_deaths += 1
            return True
    
    # Regular channel move (no death)
    user.total_channel_moves += 1
    return True
```

---

## 📊 **RESULTS AND ANALYTICS**

### **Daily Statistics**
```python
def check_day_completion(self):
    """Check if a day has completed and record statistics."""
    if self.tick_count - self.day_start_tick >= self.ticks_per_day:
        # Day completed
        self.current_day += 1
        self.day_start_tick = self.tick_count
        
        # Record daily statistics
        daily_stat = {
            "day": self.current_day,
            "total_users": len(self.users),
            "online_users": sum(1 for u in self.users.values() if u.is_online),
            "users_joined_today": self.users_joined_today,
            "users_left_today": self.users_left_today,
            "total_users_joined": self.stats["total_users_joined"],
            "total_users_left": self.stats["total_users_left"],
            "peak_users": self.stats["peak_users"],
            "global_multiplier": self.global_multiplier,
            "total_rp_earned": self.stats["total_rp_earned"],
            "total_rp_spent": self.stats["total_rp_spent"],
            "total_activities": self.stats["total_activities"],
            "total_events": self.stats["total_events"],
            "drones_alive": self.drones_alive,
            "drones_ever_died": self.drones_ever_died
        }
        
        self.daily_stats.append(daily_stat)
        
        # Reset daily counters
        self.users_joined_today = 0
        self.users_left_today = 0
        
        print(f"\n📅 Day {self.current_day} completed!")
        print(f"👥 Users: {daily_stat['total_users']} | Online: {daily_stat['online_users']}")
        print(f"📈 Joined: +{daily_stat['users_joined_today']} | Left: -{daily_stat['users_left_today']}")
        print(f"🌍 Global Multiplier: {daily_stat['global_multiplier']:.2f}x")
```

### **Result Saving**
```python
def save_results(self):
    """Save simulation results to JSON file."""
    results = {
        "simulation_info": {
            "duration_ticks": self.tick_count,
            "duration_days": self.current_day,
            "final_global_multiplier": self.global_multiplier,
            "total_users": len(self.users),
            "peak_users": self.stats["peak_users"]
        },
        "statistics": self.stats,
        "daily_stats": self.daily_stats,
        "world_events": self.world_events[-50:],  # Last 50 events
        "user_summaries": []
    }
    
    # Add user summaries
    for user in self.users.values():
        user_summary = {
            "id": user.id,
            "name": user.name,
            "user_type": user.user_type.value,
            "final_rp": user.rp,
            "total_rp_earned": user.total_rp_earned,
            "total_rp_spent": user.total_rp_spent,
            "activities_completed": user.total_activities_completed,
            "events_participated": user.total_events_participated,
            "final_drone_count": user.drone_count,
            "drones_gained": user.total_drones_gained,
            "drones_lost": user.total_drones_lost,
            "simulacra_deaths": user.total_simulacra_deaths,
            "channel_moves": user.total_channel_moves
        }
        results["user_summaries"].append(user_summary)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"infinite_simulation_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Results saved to: {filename}")
```

---

## 🚀 **BATCH FILES**

### **Main Launcher**
```batch
@echo off
title Sim-Rancher Simulation Launcher
color 0A

echo.
echo ========================================
echo   Sim-Rancher Simulation Launcher
echo   Choose Your Simulation Experience
echo ========================================
echo.
echo 🌍 Available Simulations:
echo.
echo 1. Infinite Simulation (Runs until Ctrl+C)
echo    - Day tracking with 86,400 ticks/day
echo    - 100 users with personalities
echo    - Real-time economy cycles
echo.
echo 2. Full Simulation (5 minutes)
echo    - Complete game experience
echo    - 20 users with different types
echo    - Dynamic economy and world events
echo.
echo 3. Quick Test (30 seconds)
echo    - Fast validation test
echo    - 10 users for quick check
echo    - Basic functionality test
echo.
echo 4. View Results
echo    - Open results folder
echo.
echo 5. Clean Results
echo    - Delete old result files
echo.
echo 0. Exit
echo.
echo ========================================
echo.

set /p choice="Enter your choice (0-5): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Launching Infinite Simulation...
    call infinite_simulation.bat
) else if "%choice%"=="2" (
    echo.
    echo 🚀 Launching Full Simulation...
    call full_simulation.bat
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Launching Quick Test...
    python quick_test_sim.py
) else if "%choice%"=="4" (
    echo.
    echo 📁 Opening results folder...
    start results
) else if "%choice%"=="5" (
    echo.
    echo 🧹 Cleaning old results...
    del /q results\*.json
    echo ✅ Results cleaned!
    pause
) else if "%choice%"=="0" (
    echo.
    echo 👋 Goodbye!
    exit
) else (
    echo.
    echo ❌ Invalid choice. Please try again.
    pause
    goto :eof
)

echo.
echo ========================================
echo   Simulation Complete!
echo ========================================
echo.
pause
```

---

## 📈 **PERFORMANCE OPTIMIZATION**

### **Memory Management**
```python
def optimize_memory_usage(self):
    """Optimize memory usage during long simulations."""
    # Clear old world events (keep only last 100)
    if len(self.world_events) > 100:
        self.world_events = self.world_events[-100:]
    
    # Clear old daily stats (keep only last 30 days)
    if len(self.daily_stats) > 30:
        self.daily_stats = self.daily_stats[-30:]
    
    # Garbage collection
    import gc
    gc.collect()
```

### **Performance Monitoring**
```python
def monitor_performance(self):
    """Monitor simulation performance."""
    import psutil
    import time
    
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    cpu_usage = process.cpu_percent()
    
    if memory_usage > 1000:  # 1GB
        print(f"⚠️  High memory usage: {memory_usage:.1f} MB")
        self.optimize_memory_usage()
    
    if cpu_usage > 80:
        print(f"⚠️  High CPU usage: {cpu_usage:.1f}%")
```

---

## 🔧 **TROUBLESHOOTING**

### **Common Issues**

#### **1. Memory Issues**
```python
# Add to simulation loop
if self.tick_count % 1000 == 0:  # Every 1000 ticks
    self.optimize_memory_usage()
    self.monitor_performance()
```

#### **2. Display Issues**
```python
# Reduce display frequency for better performance
if self.tick_count % 10 == 0:  # Update every 10 ticks
    self.display_simulation_status()
```

#### **3. Database Issues**
```python
# Use in-memory database for simulation
import sqlite3
conn = sqlite3.connect(":memory:")
```

### **Debug Mode**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug information to display
if self.debug_mode:
    print(f"Debug: Active activities: {len(self.active_activities)}")
    print(f"Debug: Memory usage: {memory_usage:.1f} MB")
```

---

## 📚 **LEARNING RESOURCES**

### **Simulation Concepts**
- **Tick-based Systems**: Real-time simulation with fixed time steps
- **Event-driven Programming**: Responding to world events and user actions
- **Concurrent Processing**: Multiple activities running simultaneously
- **Statistical Analysis**: Tracking and analyzing simulation data

### **Related Documentation**
- **Architecture Guide**: `docs/ARCHITECTURE.md`
- **API Reference**: `docs/API_REFERENCE.md`
- **Development Guide**: `docs/DEVELOPMENT.md`
- **Mod System Guide**: `docs/MOD_SYSTEM.md`

---

**Sim-Rancher Simulation Documentation - Complete simulation suite guide** 🔄📚 