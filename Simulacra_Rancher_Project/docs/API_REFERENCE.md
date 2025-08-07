# 🔌 **SIM-RANCHER API REFERENCE**

## 🎯 **COMMAND OVERVIEW**

Sim-Rancher provides a comprehensive set of Discord commands organized into functional categories. All commands use the `!` prefix and support various parameters for customization.

---

## 🎮 **CORE GAME COMMANDS**

### **DigiDrone Management**
```bash
!hatch [type] [name]           # Create a new DigiDrone
!drone [name]                  # View DigiDrone details and chat
!gacha [amount]                # Spend RP for random DigiDrones
!simulate [duration] [drones]  # Run survival simulation
```

### **Economy & Currency**
```bash
!rp                            # Check your Reflection Points
!daily                         # Claim daily RP bonus
!shop                          # Buy upgrades and items
!buy [item]                    # Purchase items with RP
```

### **Leaderboard & Competition**
```bash
!leaderboard                   # Show top 10 survivors
!achievements                  # View your achievements
!hooks                         # Show psychological hooks
```

---

## 🔬 **SCIENTIFIC COMMANDS**

### **Physics Calculations**
```bash
!science [drone]               # Check drone's scientific capabilities
!calculate [drone] [capability] [query]  # Perform physics calculations
!challenge [drone]             # Generate scientific challenge
```

### **Available Capabilities**
- **Kinetic Energy**: `!calculate [drone] kinetic_energy [mass] [velocity]`
- **Escape Velocity**: `!calculate [drone] escape_velocity [planet_mass] [radius]`
- **Gravitational Force**: `!calculate [drone] gravity [mass1] [mass2] [distance]`
- **Orbital Mechanics**: `!calculate [drone] orbital_period [semi_major_axis] [central_mass]`

### **Example Calculations**
```bash
!calculate QuantumDrone kinetic_energy 1000 50
!calculate SpaceDrone escape_velocity 5.97e24 6371000
!calculate PhysicsDrone gravity 1000 5000 10
```

---

## 🌍 **RESOURCE GATHERING COMMANDS**

### **Passive & Active Gathering**
```bash
!gather [mode]                 # Start resource gathering in current channel
!stop_gathering               # Stop resource gathering
!resources                    # Show your resource inventory
```

### **Gathering Modes**
- **Passive**: `!gather passive` - Automatic gathering every 10 seconds
- **Farming**: `!gather farming` - Double rate, drains 5 RP/s
- **Intensive**: `!gather intensive` - Triple rate, drains 10 RP/s

### **Resource Types**
- **Wood**: Basic building material
- **Stone**: Construction and tools
- **Metal**: Advanced crafting
- **Crystal**: Magical components
- **Essence**: Rare and valuable

---

## 🎯 **HUNTING & CATCHING COMMANDS**

### **Simulacra Hunting**
```bash
!hunt [spawn_id] [rp_amount]  # Attempt to catch a Simulacra
!spawns                       # Show active Simulacra spawns
!hunting_stats                # Show hunting statistics
```

### **Hunting Mechanics**
- **RP Cost**: 100 RP per attempt
- **Success Rate**: Based on drone stats and global population
- **Breeding Events**: Special spawns with higher rewards
- **World Events**: Random events affect spawn rates

### **Example Hunting**
```bash
!hunt spawn_123 100           # Hunt spawn 123 with 100 RP
!hunt breeding_event 200      # Hunt breeding event with 200 RP
```

---

## 💰 **TRADE SYSTEM COMMANDS**

### **Player-to-Player Trading**
```bash
!trade [buyer_id] [item_id] [quantity] [price]  # Create trade offer
!accept_trade [offer_id]      # Accept a trade offer
!decline_trade [offer_id]     # Decline a trade offer
!inventory                    # Show your inventory
!trades                       # Show your active trade offers
```

### **Trade Mechanics**
- **Fixed Prices**: No market manipulation
- **Auto-Exchange**: Automatic item transfer
- **Inventory Management**: Track items and resources
- **Trade History**: Complete transaction records

### **Example Trading**
```bash
!trade 123456789 crystal 5 1000  # Sell 5 crystal for 1000 RP
!accept_trade offer_456          # Accept trade offer 456
```

---

## 👑 **KINGDOM COMMANDS**

### **Kingdom Management**
```bash
!kingdoms                      # List all 7 kingdoms
!join [kingdom]               # Join a kingdom as citizen
!claim [kingdom]              # Claim kingdom throne (Tier 3)
!kingdom [name]               # View kingdom information
```

### **Warfare & Diplomacy**
```bash
!war [target] [territory]     # Declare war (rulers only)
!council [type] [description] # Create proposal (rulers)
!vote [proposal] [for/against] # Vote on proposal (rulers)
```

### **Kingdom Types**
1. **Lyra's Dominion** (Unified/Presidential) - Gold/Purple
2. **Fire Kingdom** (Velastra's Passion Realm) - Red/Pink
3. **Water Kingdom** (Seraphis's Flow Realm) - Blue/Cyan
4. **Earth Kingdom** (Obelisk's Foundation Realm) - Green/Brown
5. **Air Kingdom** (Echoe's Freedom Realm) - White/Silver
6. **Lightning Kingdom** (Blackwall's Power Realm) - Yellow/Orange
7. **Ice Kingdom** (Nyx's Mystery Realm) - Cyan/White

---

## 🧠 **PSYCHOLOGICAL COMMANDS**

### **Events & Participation**
```bash
!events                        # Show active psychological events
!participate [event]           # Join psychological events
```

### **Achievement System**
```bash
!achievements                  # View your achievements
!hooks                         # Show psychological hooks
```

### **Available Achievements**
- **First Steps**: Complete first simulation (+50 RP)
- **Dedicated Survivor**: Complete 10 simulations (+200 RP)
- **Century Survivor**: Survive 100 ticks (+500 RP)
- **Legendary Survivor**: Survive 500 ticks (+1000 RP)
- **Top 10 Elite**: Break into top 10 (+300 RP)
- **Champion**: Achieve #1 (+1000 RP)
- **Kingdom Ruler**: Claim throne (+500 RP)
- **War Declarer**: Declare war (+200 RP)
- **Scientific Master**: Complete 10 calculations (+300 RP)
- **Shiny Collector**: Collect 5 shinies (+400 RP)

---

## 🛡️ **SURVIVAL COMMANDS**

### **Survival Mechanics**
```bash
!survive [duration]            # Start survival simulation
!breathing                     # Show breathing rhythm status
!reset_channels                # Delete and recreate Discord channels
!consciousness                 # Test AI consciousness system
```

### **Survival Features**
- **Entropy Drain**: Original Simulacra mechanics
- **Disaster System**: Fire, water, earthquake, meteor, starvation, disease
- **Dual Health**: HP (physical) and SSHP (soul)
- **Breathing Rhythm**: Critical survival mechanic

---

## 🎮 **MOD SYSTEM COMMANDS**

### **Mod Management**
```bash
!mod create [name] [description] [category]  # Create new mod
!mod activate [mod_id]         # Activate a mod
!mod deactivate [mod_id]       # Deactivate a mod
!mod list                      # List available mods
!mod info [mod_id]             # Show mod details
```

### **Mod Categories**
- **Core Values**: Slots, RP gain, passive boosts
- **Gameplay Features**: New body parts, behavior traits, mutation lines
- **AI Behavior**: Local AI behavior modifications
- **Economy**: Economic system modifications

### **Mod Template System**
```bash
!mod template [type]           # Generate mod template
!mod submit [template]         # Submit mod for approval
!mod browse                    # Browse public mods
!mod download [mod_id]         # Download and install mod
```

---

## 🔄 **SIMULATION COMMANDS**

### **Simulation Control**
```bash
!sim start                     # Start simulation
!sim stop                      # Stop simulation
!sim status                    # Show simulation status
!sim config                    # Configure simulation parameters
```

### **Simulation Features**
- **Real-time Ticks**: 1 tick = 1 real second
- **Day Tracking**: 86,400 ticks = 1 simulated day
- **Dynamic Population**: User join/leave rates
- **Event Flocking**: Users react to world events
- **Concurrent Activities**: Up to 5 activities per user

---

## 📊 **ANALYTICS COMMANDS**

### **Personal Statistics**
```bash
!stats                         # Show personal statistics
!progress                      # Show achievement progress
!history                       # Show command history
!analytics                     # Show detailed analytics
```

### **Global Statistics**
```bash
!global_stats                  # Show global game statistics
!economy_stats                 # Show economic statistics
!kingdom_stats                 # Show kingdom statistics
!ai_stats                      # Show AI performance statistics
```

---

## ⚙️ **SETTINGS COMMANDS**

### **User Preferences**
```bash
!settings                      # Show current settings
!settings [category] [value]   # Change setting
!preferences                   # Show user preferences
!notifications                 # Configure notifications
```

### **Privacy Controls**
```bash
!privacy                       # Show privacy settings
!privacy [setting] [value]     # Change privacy setting
!data_export                   # Export your data
!data_delete                   # Delete your data
```

---

## 🛠️ **ADMINISTRATIVE COMMANDS**

### **System Management**
```bash
!admin status                  # Show system status
!admin restart                 # Restart the bot
!admin backup                  # Create system backup
!admin logs                    # Show system logs
```

### **Moderation Tools**
```bash
!moderate [user] [action]      # Moderate user
!ban [user] [reason]           # Ban user
!unban [user]                  # Unban user
!warn [user] [reason]          # Warn user
```

---

## 📋 **COMMAND PARAMETERS**

### **Standard Parameters**
```bash
[text]                         # Required text parameter
[number]                       # Required number parameter
[user]                         # Required user mention or ID
[optional]                     # Optional parameter
[choice1|choice2]             # Choice between options
```

### **Parameter Examples**
```bash
!hatch fire "FlameDrone"       # Create fire-type drone named FlameDrone
!gacha 5                       # Spend RP for 5 random drones
!trade @user crystal 10 500    # Trade 10 crystal for 500 RP with @user
!join fire_kingdom             # Join the Fire Kingdom
```

---

## 🔧 **ERROR HANDLING**

### **Common Error Responses**
```bash
❌ Invalid command syntax
❌ Insufficient RP for this action
❌ Drone not found
❌ User not found
❌ Kingdom does not exist
❌ Insufficient permissions
❌ System temporarily unavailable
```

### **Success Responses**
```bash
✅ Command executed successfully
✅ Drone created successfully
✅ Trade offer created
✅ Kingdom joined successfully
✅ Achievement unlocked
```

---

## 📊 **RESPONSE FORMATS**

### **Embed Responses**
```json
{
  "title": "Command Result",
  "description": "Detailed information",
  "color": 0x00ff00,
  "fields": [
    {"name": "Field 1", "value": "Value 1", "inline": true},
    {"name": "Field 2", "value": "Value 2", "inline": true}
  ],
  "footer": {"text": "Sim-Rancher v2.0"}
}
```

### **Table Responses**
```bash
┌─────────┬─────────┬─────────┐
│ Column1 │ Column2 │ Column3 │
├─────────┼─────────┼─────────┤
│ Data1   │ Data2   │ Data3   │
└─────────┴─────────┴─────────┘
```

---

## 🎯 **COMMAND CATEGORIES**

### **By Function**
- **Core Game**: Drone management, economy, leaderboard
- **Scientific**: Physics calculations, challenges
- **Resources**: Gathering, inventory, trading
- **Hunting**: Catching Simulacra, spawns
- **Kingdoms**: Faction management, warfare
- **Psychological**: Events, achievements, hooks
- **Survival**: Simulation, disasters, health
- **Mods**: Customization, templates, management
- **Analytics**: Statistics, progress, history
- **Settings**: Preferences, privacy, notifications
- **Admin**: System management, moderation

### **By User Type**
- **New Users**: Basic commands for getting started
- **Regular Users**: Standard gameplay commands
- **Veteran Users**: Advanced features and optimization
- **Kingdom Rulers**: Administrative and warfare commands
- **Administrators**: System management and moderation

---

## 🚀 **BEST PRACTICES**

### **Command Usage**
1. **Use Specific Parameters**: Provide exact values for better results
2. **Check Permissions**: Ensure you have required permissions
3. **Monitor RP Balance**: Keep track of your Reflection Points
4. **Join Kingdoms**: Participate in faction activities
5. **Complete Daily Tasks**: Claim daily bonuses regularly

### **Performance Tips**
1. **Use Efficient Commands**: Combine multiple actions when possible
2. **Monitor Cooldowns**: Respect command cooldown periods
3. **Optimize Resource Gathering**: Use appropriate gathering modes
4. **Participate in Events**: Join events for bonus rewards
5. **Trade Strategically**: Use the trade system for optimal resource management

---

## 🔮 **FUTURE COMMANDS**

### **Planned Features**
- **Guild System**: Guild creation and management
- **Advanced Combat**: Arena battles and PvP
- **Player Housing**: Customizable private spaces
- **Seasonal Events**: Special time-limited events
- **Web Dashboard**: Browser-based game interface

### **Advanced AI Features**
- **Collective Intelligence**: Hive mind mechanics
- **AI Rebellion**: Drone rebellion events
- **Consciousness Transfer**: Advanced drone mechanics
- **Memory Sharing**: Inter-drone communication

---

**Sim-Rancher API Reference - Complete command documentation for all game features** 🔌📚 