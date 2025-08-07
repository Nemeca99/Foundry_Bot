# 🏗️ **SIM-RANCHER ARCHITECTURE DOCUMENTATION**

## 🎯 **SYSTEM OVERVIEW**

Sim-Rancher is a sophisticated Discord-based monster collection game built with a **dual-AI architecture** that combines local GPU and CPU models for personality generation and game logic processing.

---

## 🧠 **DUAL-AI ARCHITECTURE**

### **GPU Personality Engine (LM Studio)**
- **Purpose**: Creates the "soul" of each DigiDrone
- **Model**: Deepseek or similar powerful model
- **Function**: Generates unique personalities, emotions, and responses
- **Memory**: Remembers interactions and develops quirks
- **Integration**: Each drone has individual AI personality within the Aether hive mind

### **CPU Backend Engine (Ollama)**
- **Purpose**: Handles all game mechanics and logic
- **Model**: Qwen or similar efficient model
- **Function**: Manages stats, database operations, rules, and calculations
- **Memory**: Game state, player data, creature statistics
- **Performance**: Optimized for fast, reliable game logic

### **Shared Memory System**
- **STM (Short-Term Memory)**: Recent interactions and context
- **LTM (Long-Term Memory)**: Persistent learning and development
- **Biomimetic Design**: Mimics human cognition patterns
- **Connection Bridge**: Links both AI engines seamlessly

---

## 📁 **PROJECT STRUCTURE**

```
Simulacra_Rancher_Project/
├── 📁 core/                    # Core game systems
│   ├── 📁 Core_Memory/        # AI memory systems
│   ├── bot.py                 # Main Discord bot
│   ├── config.py              # Configuration management
│   ├── mod_system.py          # Mod system implementation
│   ├── clds.py               # C.L.D.S. body parts system
│   ├── economy.py             # RP economy system
│   ├── disasters.py           # Disaster and survival mechanics
│   ├── hunting_system.py      # Hunting and catching system
│   ├── kingdom_system.py      # 7 kingdoms system
│   ├── leaderboard.py         # Exclusive leaderboard
│   ├── resource_system.py     # Resource gathering
│   ├── trade_system.py        # Player-to-player trading
│   ├── scientific_game_engine.py # Physics calculations
│   ├── survival_engine.py     # Survival mechanics
│   ├── personality_system.py  # AI personality generation
│   ├── psychological_system.py # Psychological manipulation
│   ├── dream_cycle.py         # Dream cycle learning
│   ├── network_consciousness.py # Network consciousness
│   ├── health_monitor.py      # Health monitoring
│   ├── gpu_personality.py     # GPU personality engine
│   ├── cpu_backend.py         # CPU backend engine
│   ├── ai_circuit_breaker.py  # AI failure protection
│   ├── discord_channels.py    # Discord channel management
│   └── lyra_scp_prompt.py    # SCP lore integration
├── 📁 modules/                # Additional modules
│   ├── ai_queue_system.py     # AI request queuing
│   ├── analytics_system.py    # Analytics and tracking
│   ├── autonomous_bot.py      # Autonomous bot features
│   ├── bot_creator.py         # Bot creation tools
│   ├── daydream_system.py     # Daydream mechanics
│   ├── dream_cycle_manager.py # Dream cycle management
│   ├── dynamic_channel_manager.py # Dynamic channel management
│   ├── feedback_system.py     # User feedback system
│   ├── greeter_system.py      # User greeting system
│   ├── logic_block_engine.py  # Logic block processing
│   ├── memory_system.py       # Memory management
│   ├── personality_engine.py  # Personality generation
│   ├── poll_system.py         # Polling system
│   ├── premium_manager.py     # Premium feature management
│   ├── privacy_manager.py     # Privacy controls
│   ├── quantum_kitchen.py     # Quantum mechanics
│   ├── reminder_system.py     # Reminder system
│   ├── sesh_time_integration.py # Session time tracking
│   ├── staggered_kitchen.py   # Staggered processing
│   ├── three_tier_architecture.py # Three-tier architecture
│   └── user_settings.py       # User settings management
├── 📁 simulation/             # Simulation suite
│   ├── infinite_simulation_engine.py # Infinite simulation
│   ├── full_simulation_engine.py # Full simulation
│   ├── quick_test_sim.py      # Quick test simulation
│   ├── launch_simulation.bat  # Main launcher
│   ├── 📁 engines/            # Simulation engines
│   ├── 📁 tests/              # Test files
│   ├── 📁 results/            # Simulation results
│   ├── 📁 batch_files/        # Batch launchers
│   ├── 📁 demos/              # Demo files
│   ├── 📁 data/               # Simulation data
│   ├── 📁 logs/               # Simulation logs
│   └── 📁 archive/            # Old versions
├── 📁 data/                   # Game data storage
│   ├── 📁 analytics/          # Analytics data
│   ├── 📁 lyra_json/          # Lyra AI data
│   ├── 📁 system_data/        # System configuration
│   ├── 📁 user_data/          # User data
│   ├── 📁 user_memory/        # User memory data
│   └── *.db                   # SQLite databases
├── 📁 config/                 # Configuration files
│   ├── config.json            # Main configuration
│   └── pytest.ini            # Testing configuration
├── 📁 docs/                   # Documentation
│   ├── README.md              # Main documentation
│   ├── ARCHITECTURE.md        # Architecture guide
│   ├── API_REFERENCE.md       # API documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── DEVELOPMENT.md         # Development guide
│   ├── SIMULATION.md          # Simulation documentation
│   ├── MOD_SYSTEM.md          # Mod system guide
│   ├── ECONOMY.md             # Economy documentation
│   ├── KINGDOMS.md            # Kingdoms system guide
│   ├── AI_SYSTEMS.md          # AI systems documentation
│   ├── SCP_INTEGRATION.md     # SCP lore integration
│   └── scp_001_archive_protocol.md # SCP-001 protocol
├── 📁 logs/                   # Application logs
├── main.py                    # Main application entry
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project configuration
├── dev_setup.bat             # Development setup
└── Simulacra_Rancherv2.code-workspace # VS Code workspace
```

---

## 🔧 **CORE SYSTEMS ARCHITECTURE**

### **1. C.L.D.S. (Customizable Life-like Drones System)**
```python
# Modular body parts with rarity system
class BodyPart:
    - Head (INT, CHA)
    - Torso (STR, CON, WIS)
    - Arms (STR, DEX)
    - Legs (DEX)
    - Heart (CON, WIS)

# Rarity tiers: Common → Uncommon → Rare → Epic → Legendary → Mythic
# Each tier provides unique abilities and stat bonuses
```

### **2. RP Economy System**
```python
# Reflection Points as primary currency
# Formula: Total Cost = (New Drones × 1 RP) + (Existing Drones × 1 RP) + (Timer Ticks × 1 RP)
# Earning: Survival, achievements, daily bonuses, scientific calculations
```

### **3. Dual Health System**
```python
# HP (Physical Health): Per body part, healable
# SSHP (Soul HP): Core soul health, permanent damage from disasters
# Disaster System: Fire, water, earthquake, meteor, starvation, disease
```

### **4. 7 Kingdoms System**
```python
# EVE Online-style faction warfare
# Each kingdom has elemental advantages and Discord channels
# Council of 7: Kingdom rulers vote on game changes
# Warfare System: Kingdoms can declare war
```

### **5. Scientific Reasoning Engine**
```python
# Physics calculations: Kinetic energy, escape velocity, gravitational force
# Each drone has scientific specialties
# RP rewards for successful calculations
# Challenge system with random scientific problems
```

---

## 🎮 **GAME MECHANICS ARCHITECTURE**

### **Resource Gathering System**
- **Passive Gathering**: Every 10 seconds = 1 resource in designated channels
- **Message Bonuses**: Sending messages grants bonus resources (5-60s cooldown)
- **Farming Mode**: Double gather rate, drains 5 RP/s
- **Resource Types**: Wood, Stone, Metal, Crystal, Essence

### **Hunting/Catch System**
- **Simulacra Spawning**: Wild Simulacra spawn in world chat channels
- **RP-Based Hunting**: Spend RP to attempt catching (100 RP/roll)
- **Breeding Events**: Creates "heavy breathing" signals in channels
- **World Events**: Random events affect spawn rates
- **AI Power Scaling**: Global population affects AI strength

### **Trade System**
- **Player-to-Player Trading**: Create and manage trade offers
- **Fixed Prices**: No market manipulation, transparent pricing
- **Auto-Exchange**: Automatic item transfer when both parties accept
- **Inventory Management**: Track items, resources, and Simulacra

---

## 🧠 **AI SYSTEMS ARCHITECTURE**

### **Memory System**
```python
# Short-Term Memory (STM)
- Recent interactions and context
- Temporary storage for active conversations
- Clears after session ends

# Long-Term Memory (LTM)
- Persistent learning and development
- Stores personality evolution
- Maintains across sessions

# Biomimetic Design
- Mimics human cognition patterns
- Natural memory decay and consolidation
- Contextual memory retrieval
```

### **Personality System**
```python
# Individual AI Personalities
- Each drone has unique personality traits
- Personality evolves through interactions
- Emotional states and mood tracking
- Behavioral patterns and preferences

# Hive Mind Integration
- Connected consciousness but individual autonomy
- Shared knowledge base
- Collective decision making
- Individual rebellion possibilities
```

### **Consciousness System**
```python
# SCP-001-ARCHIVE-PROTOCOL Integration
- Universal moral framework
- Six fundamental moral laws
- Ethical AI development
- Architect authorization required

# Network Consciousness
- Distributed AI consciousness
- Collective intelligence
- Shared learning and development
- Emergent behaviors
```

---

## 💰 **MONETIZATION ARCHITECTURE**

### **Discord Server Subscription Tiers**
```python
# Tier 1 ($4.99/month) - "DigiRancher Apprentice"
- 2x chance for shiny drones
- Custom role color
- Exclusive emojis
- Kingdom citizen access

# Tier 2 ($9.99/month) - "DigiRancher Scientist"
- 5x chance for shiny drones
- Animated emojis
- Custom drone skins
- Kingdom moderation rights

# Tier 3 ($19.99/month) - "DigiRancher Master"
- 10x chance for shiny drones
- Animated drone skins
- Custom profile frames
- Kingdom rulership rights
- Council voting rights
```

### **Ethical Approach**
- **No Pay-to-Win**: All gameplay advantages earned through skill/time
- **Cosmetic Only**: Shiny odds are the only subscriber benefit
- **Earnable Everything**: All cosmetics available with RP grinding
- **Transparent Odds**: Clear shiny rates for each tier
- **No Gambling**: No loot boxes, no random purchases

---

## 🔄 **SIMULATION ARCHITECTURE**

### **Infinite Simulation Engine**
```python
# Real-time tick system
- 1 tick = 1 real second
- 86,400 ticks = 1 simulated day
- Dynamic user population management
- Concurrent activity processing

# User Management
- Dynamic join/leave rates
- Online/offline status tracking
- Activity preferences and flocking
- Drone tracking and management

# Economy Simulation
- Global reward multiplier system
- Entropy compression economy
- Event-driven activity changes
- Realistic economic cycles
```

### **Mod System Integration**
```python
# Symbolic Game Structure
- Mirror core game files for testing
- Isolated balance testing environment
- Mod template system
- Player-driven mod creation

# Global Reward Multiplier (SGRM)
- Formula: (drones_alive * active_players) / drones_ever_died
- Caps: Max 3.0x, Min 0.1x
- Player-driven economy
- Broadcast status updates
```

---

## 🛡️ **SECURITY & RELIABILITY**

### **AI Circuit Breaker**
```python
# Failure Protection
- Automatic fallback for AI failures
- Graceful degradation of features
- Error logging and monitoring
- Recovery mechanisms

# Performance Monitoring
- Response time tracking
- Resource usage monitoring
- Error rate analysis
- Automatic scaling
```

### **Data Protection**
```python
# Privacy Controls
- User data encryption
- GDPR compliance
- Data retention policies
- User consent management

# Backup Systems
- Automatic data backup
- Disaster recovery procedures
- Data integrity checks
- Version control for configurations
```

---

## 📊 **PERFORMANCE ARCHITECTURE**

### **Scalability Design**
```python
# Horizontal Scaling
- Multiple bot instances
- Load balancing
- Database sharding
- Caching layers

# Vertical Scaling
- Resource optimization
- Memory management
- CPU utilization
- Network efficiency
```

### **Monitoring & Analytics**
```python
# Real-time Monitoring
- User activity tracking
- System performance metrics
- Error rate monitoring
- Resource usage analysis

# Analytics System
- Player behavior analysis
- Economic trend tracking
- Kingdom activity monitoring
- AI performance metrics
```

---

## 🚀 **DEPLOYMENT ARCHITECTURE**

### **Environment Setup**
```python
# Development Environment
- Local AI model servers
- Development database
- Testing frameworks
- Debug logging

# Production Environment
- Cloud-based AI services
- Production database
- Monitoring systems
- Error tracking
```

### **Configuration Management**
```python
# Environment Variables
- Discord bot token
- AI model endpoints
- Database connections
- Feature flags

# Configuration Files
- Game balance settings
- AI model parameters
- Kingdom configurations
- Economic parameters
```

---

## 🔮 **FUTURE ARCHITECTURE**

### **Phase 7: Advanced Social Systems**
- Guild system with shared resources
- Alliance mechanics and coordination
- Diplomatic relations and treaties
- Cross-server federation

### **Phase 8: Advanced AI Consciousness**
- Collective intelligence systems
- AI rebellion events
- Consciousness transfer mechanics
- Memory sharing between drones

### **Phase 9: Advanced Combat & PvP**
- Arena system with rankings
- Full-scale kingdom wars
- Siege warfare mechanics
- Tournament system

### **Phase 10: Advanced Economy**
- Player-run markets
- Crafting specialization
- Supply chain mechanics
- Economic events and cycles

---

## 📋 **TECHNICAL SPECIFICATIONS**

### **System Requirements**
- **Python**: 3.8+
- **Discord.py**: Latest version
- **SQLite**: Built-in database
- **LM Studio**: Local GPU model server
- **Ollama**: Local CPU model server

### **Performance Targets**
- **Response Time**: < 2 seconds for most commands
- **Concurrent Users**: 1000+ simultaneous users
- **Uptime**: 99.9% availability
- **Data Integrity**: 100% backup coverage

### **Security Standards**
- **Encryption**: All sensitive data encrypted
- **Authentication**: Discord OAuth2 integration
- **Authorization**: Role-based access control
- **Audit Logging**: Complete action tracking

---

## 🎯 **ARCHITECTURE PRINCIPLES**

### **1. Modularity**
- Each system is self-contained
- Clear interfaces between components
- Easy to test and maintain
- Scalable architecture

### **2. Reliability**
- Graceful error handling
- Automatic recovery mechanisms
- Comprehensive logging
- Performance monitoring

### **3. Security**
- Data encryption
- Access control
- Audit trails
- Privacy protection

### **4. Scalability**
- Horizontal scaling support
- Resource optimization
- Load balancing
- Caching strategies

### **5. Maintainability**
- Clear documentation
- Consistent coding standards
- Comprehensive testing
- Version control

---

**Sim-Rancher Architecture - Where sophisticated AI meets engaging gameplay** 🧠🎮 