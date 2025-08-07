# 🎮 **SIM-RANCHER MOD SYSTEM DOCUMENTATION**

## 🎯 **MOD SYSTEM OVERVIEW**

The Sim-Rancher Live Mod System allows players to create, share, and use custom modifications to the game, providing a "game within a game" experience with symbolic file structures and balance testing capabilities.

---

## 🏗️ **SYMBOLIC GAME STRUCTURE**

### **Concept**
The mod system uses a **symbolic game structure** that mirrors the real game's core folders (`core`, `modules`, `data`, `config`, `Core_Memory`) with symbolic files that can be modified for balance testing and then committed to the real files if successful.

### **File Structure**
```
simulation/
├── symbolic/
│   ├── core/              # Symbolic core files
│   │   ├── clds.py       # C.L.D.S. system overrides
│   │   ├── economy.py    # Economy system overrides
│   │   ├── hunting_system.py # Hunting system overrides
│   │   └── mod_system.py # Mod system implementation
│   ├── modules/           # Symbolic module files
│   ├── data/              # Symbolic data files
│   ├── config/            # Symbolic config files
│   └── Core_Memory/       # Symbolic memory files
└── mod_templates/         # Player-created mod templates
```

### **Symbolic File Management**
```python
class SymbolicFileManager:
    """Manages symbolic game files for mod testing."""
    
    def __init__(self):
        self.symbolic_files = {
            "core/clds.py": "simulation/symbolic/core/clds.py",
            "core/economy.py": "simulation/symbolic/core/economy.py",
            "core/hunting_system.py": "simulation/symbolic/core/hunting_system.py",
            "core/mod_system.py": "simulation/symbolic/core/mod_system.py"
        }
    
    def create_symbolic_structure(self):
        """Create symbolic file structure."""
        for real_path, symbolic_path in self.symbolic_files.items():
            if os.path.exists(real_path):
                os.makedirs(os.path.dirname(symbolic_path), exist_ok=True)
                shutil.copy2(real_path, symbolic_path)
    
    def apply_mod_to_symbolic(self, mod_template):
        """Apply mod changes to symbolic files."""
        for file_path, changes in mod_template.effects.items():
            if file_path in self.symbolic_files:
                symbolic_path = self.symbolic_files[file_path]
                self.apply_changes_to_file(symbolic_path, changes)
    
    def commit_symbolic_to_real(self):
        """Commit successful symbolic changes to real files."""
        for real_path, symbolic_path in self.symbolic_files.items():
            if os.path.exists(symbolic_path):
                shutil.copy2(symbolic_path, real_path)
```

---

## 🎯 **MOD TEMPLATE SYSTEM**

### **ModTemplate Class**
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

### **Mod Categories**
```python
MOD_CATEGORIES = {
    "core_values": {
        "name": "Core Values",
        "description": "Modify slots, RP gain, passive boosts",
        "examples": ["Increased RP gain", "More mod slots", "Faster cooldowns"]
    },
    "gameplay_features": {
        "name": "Gameplay Features", 
        "description": "New body parts, behavior traits, mutation lines",
        "examples": ["New drone types", "Special abilities", "Unique traits"]
    },
    "ai_behavior": {
        "name": "AI Behavior",
        "description": "Local AI behavior modifications",
        "examples": ["Personality changes", "Response patterns", "Learning rates"]
    },
    "economy": {
        "name": "Economy",
        "description": "Economic system modifications",
        "examples": ["Price changes", "Trade mechanics", "Resource rates"]
    }
}
```

### **Mod Template Generator**
```python
class ModTemplateGenerator:
    """Generates specific mod types with templates."""
    
    def generate_rp_boost_mod(self, creator_id: str, boost_percentage: int) -> ModTemplate:
        """Generate an RP boost mod."""
        return ModTemplate(
            mod_id=f"rp_boost_{int(time.time())}",
            creator_id=creator_id,
            name=f"+{boost_percentage}% RP Boost",
            description=f"Increases RP gain by {boost_percentage}%",
            category="core_values",
            cost_rp=100 * boost_percentage,
            daily_upkeep=10 * boost_percentage,
            effects={
                "core/economy.py": {
                    "rp_gain_multiplier": 1.0 + (boost_percentage / 100.0)
                }
            },
            requirements={
                "min_user_level": 5,
                "max_boost_percentage": 50
            }
        )
    
    def generate_slot_expansion_mod(self, creator_id: str, additional_slots: int) -> ModTemplate:
        """Generate a mod slot expansion mod."""
        return ModTemplate(
            mod_id=f"slot_expansion_{int(time.time())}",
            creator_id=creator_id,
            name=f"+{additional_slots} Mod Slots",
            description=f"Adds {additional_slots} additional mod slots",
            category="core_values",
            cost_rp=200 * additional_slots,
            daily_upkeep=20 * additional_slots,
            effects={
                "core/mod_system.py": {
                    "additional_mod_slots": additional_slots
                }
            },
            requirements={
                "min_user_level": 10,
                "max_additional_slots": 10
            }
        )
```

---

## 👤 **PLAYER MOD PROFILES**

### **PlayerModProfile Class**
```python
@dataclass
class PlayerModProfile:
    user_id: str
    mod_slots: int = 10
    active_mods: List[str] = None
    stasis_mods: List[str] = None
    total_rp_spent: int = 0
    mod_subscription_cost: int = 0
    rp_modifiers: Dict[str, float] = None
    last_daily_claim: str = ""
    daily_claimed: bool = False
    
    def __post_init__(self):
        if self.active_mods is None:
            self.active_mods = []
        if self.stasis_mods is None:
            self.stasis_mods = []
        if self.rp_modifiers is None:
            self.rp_modifiers = {}
```

### **Mod Management**
```python
class ModManager:
    """Manages player mod profiles and mod operations."""
    
    def activate_mod(self, user_id: str, mod_id: str) -> bool:
        """Activate a mod for a player."""
        profile = self.get_player_profile(user_id)
        mod_template = self.get_mod_template(mod_id)
        
        if not mod_template or not mod_template.approved:
            return False
        
        if len(profile.active_mods) >= profile.mod_slots:
            return False
        
        if mod_id not in profile.stasis_mods:
            return False
        
        # Move mod from stasis to active
        profile.stasis_mods.remove(mod_id)
        profile.active_mods.append(mod_id)
        
        # Apply mod effects
        self.apply_mod_effects(user_id, mod_template)
        
        # Update subscription cost
        profile.mod_subscription_cost += mod_template.daily_upkeep
        
        return True
    
    def deactivate_mod(self, user_id: str, mod_id: str) -> bool:
        """Deactivate a mod for a player."""
        profile = self.get_player_profile(user_id)
        mod_template = self.get_mod_template(mod_id)
        
        if mod_id not in profile.active_mods:
            return False
        
        # Move mod from active to stasis
        profile.active_mods.remove(mod_id)
        profile.stasis_mods.append(mod_id)
        
        # Remove mod effects
        self.remove_mod_effects(user_id, mod_template)
        
        # Update subscription cost
        profile.mod_subscription_cost -= mod_template.daily_upkeep
        
        return True
```

---

## 🌍 **GLOBAL REWARD MULTIPLIER (SGRM)**

### **Formula**
```python
def calculate_global_multiplier(self):
    """Calculate global reward multiplier based on player actions."""
    if self.drones_ever_died == 0:
        return 1.0
    
    multiplier = (self.drones_alive * self.active_players) / self.drones_ever_died
    return max(0.1, min(3.0, multiplier))
```

### **Implementation**
```python
class GlobalRewardMultiplier:
    """Manages the global reward multiplier system."""
    
    def __init__(self, mod_system):
        self.mod_system = mod_system
        self.drones_alive = 0
        self.drones_ever_died = 1
        self.active_players = 0
        self.last_multiplier_update = time.time()
        self.multiplier_history = []
    
    def update_multiplier(self):
        """Update the global multiplier."""
        new_multiplier = self.calculate_global_multiplier()
        
        # Record multiplier change
        self.multiplier_history.append({
            "timestamp": time.time(),
            "multiplier": new_multiplier,
            "drones_alive": self.drones_alive,
            "active_players": self.active_players,
            "drones_ever_died": self.drones_ever_died
        })
        
        # Keep only last 1000 entries
        if len(self.multiplier_history) > 1000:
            self.multiplier_history = self.multiplier_history[-1000:]
        
        return new_multiplier
    
    def broadcast_multiplier_status(self):
        """Broadcast multiplier status to players."""
        multiplier = self.calculate_global_multiplier()
        
        if multiplier >= 2.5:
            message = f"🚀 **ECONOMIC BOOM!** Global multiplier: {multiplier:.2f}x"
        elif multiplier >= 1.5:
            message = f"📈 **GROWTH PHASE** Global multiplier: {multiplier:.2f}x"
        elif multiplier <= 0.3:
            message = f"⚠️ **ECONOMIC COLLAPSE** Global multiplier: {multiplier:.2f}x"
        elif multiplier <= 0.5:
            message = f"📉 **RECESSION** Global multiplier: {multiplier:.2f}x"
        else:
            message = f"🌍 **STABLE ECONOMY** Global multiplier: {multiplier:.2f}x"
        
        return message
```

---

## 💰 **ENTROPY COMPRESSION ECONOMY**

### **Core Concept**
The Entropy Compression Economy System makes bulk actions "compress more entropy into a single tick," with players paying for this compression with exponentially scaling RP costs.

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

# During economic collapse (0.1x multiplier)
total_cost = (100 * 2) * (10 * 0.1) = 200 RP

# During economic boom (3.0x multiplier)  
total_cost = (100 * 2) * (10 * 3.0) = 6000 RP
```

### **Integration with Commands**
```python
def process_bulk_hunt(self, user_id: str, spawn_id: str, rp_amount: int, ticks: int):
    """Process a bulk hunting action."""
    base_cost = 100  # Base cost per hunt
    global_multiplier = self.global_multiplier.calculate_global_multiplier()
    
    # Calculate compression cost
    total_cost = self.calculate_compression_cost(base_cost, ticks, global_multiplier)
    
    if user.rp < total_cost:
        return {"success": False, "message": "Insufficient RP for bulk action"}
    
    # Deduct RP
    user.rp -= total_cost
    user.total_rp_spent += total_cost
    
    # Process hunts
    successes = 0
    for _ in range(ticks):
        if random.random() < self.get_hunt_success_rate(user):
            successes += 1
            user.gain_drone("hunt")
    
    return {
        "success": True,
        "hunts_attempted": ticks,
        "hunts_successful": successes,
        "total_cost": total_cost,
        "compression_multiplier": global_multiplier
    }
```

---

## 🎮 **MOD COMMANDS**

### **Mod Creation**
```bash
!mod create [name] [description] [category]  # Create new mod
!mod template [type]                          # Generate mod template
!mod submit [template]                        # Submit mod for approval
```

### **Mod Management**
```bash
!mod activate [mod_id]                        # Activate a mod
!mod deactivate [mod_id]                      # Deactivate a mod
!mod list                                     # List available mods
!mod info [mod_id]                            # Show mod details
```

### **Mod Marketplace**
```bash
!mod browse                                   # Browse public mods
!mod download [mod_id]                        # Download and install mod
!mod rate [mod_id] [rating]                   # Rate a mod
!mod search [query]                           # Search for mods
```

### **Mod Slots**
```bash
!mod slots                                    # Show mod slot status
!mod buy_slots [amount]                       # Buy additional mod slots
!mod upgrade_slots                            # Upgrade mod slot capacity
```

---

## 📊 **MOD ANALYTICS**

### **Mod Statistics**
```python
@dataclass
class ModAnalytics:
    total_mods_created: int = 0
    total_mods_downloaded: int = 0
    total_rp_spent_on_mods: int = 0
    average_mod_rating: float = 0.0
    most_popular_category: str = ""
    most_active_creator: str = ""
    
    def update_mod_created(self, mod_template: ModTemplate):
        """Update statistics when a mod is created."""
        self.total_mods_created += 1
        
        # Update category popularity
        category_counts = self.get_category_counts()
        if mod_template.category in category_counts:
            category_counts[mod_template.category] += 1
        else:
            category_counts[mod_template.category] = 1
        
        # Update most popular category
        self.most_popular_category = max(category_counts, key=category_counts.get)
    
    def update_mod_downloaded(self, mod_template: ModTemplate):
        """Update statistics when a mod is downloaded."""
        self.total_mods_downloaded += 1
        self.total_rp_spent_on_mods += mod_template.cost_rp
        mod_template.downloads += 1
```

### **Mod Performance Tracking**
```python
class ModPerformanceTracker:
    """Tracks mod performance and balance."""
    
    def track_mod_usage(self, mod_id: str, user_id: str, success: bool):
        """Track how a mod performs for a user."""
        tracking_data = {
            "mod_id": mod_id,
            "user_id": user_id,
            "timestamp": time.time(),
            "success": success,
            "user_rp": self.get_user_rp(user_id),
            "user_level": self.get_user_level(user_id)
        }
        
        self.mod_usage_data.append(tracking_data)
    
    def analyze_mod_balance(self, mod_id: str):
        """Analyze if a mod is balanced."""
        mod_usage = [data for data in self.mod_usage_data if data["mod_id"] == mod_id]
        
        if not mod_usage:
            return {"balanced": True, "reason": "No usage data"}
        
        success_rate = sum(1 for data in mod_usage if data["success"]) / len(mod_usage)
        avg_user_rp = sum(data["user_rp"] for data in mod_usage) / len(mod_usage)
        
        # Determine if mod is balanced
        if success_rate > 0.8:
            return {"balanced": False, "reason": "Too powerful", "success_rate": success_rate}
        elif success_rate < 0.2:
            return {"balanced": False, "reason": "Too weak", "success_rate": success_rate}
        else:
            return {"balanced": True, "success_rate": success_rate}
```

---

## 🔧 **MOD DEVELOPMENT TOOLS**

### **Mod Template Generator**
```python
class ModTemplateGenerator:
    """Generates mod templates for different categories."""
    
    def generate_core_values_template(self, creator_id: str) -> Dict[str, Any]:
        """Generate template for core values mods."""
        return {
            "name": "Core Values Mod",
            "description": "Modify slots, RP gain, passive boosts",
            "category": "core_values",
            "effects": {
                "rp_gain_multiplier": 1.0,
                "additional_mod_slots": 0,
                "cooldown_reduction": 0.0
            },
            "requirements": {
                "min_user_level": 1,
                "max_rp_gain_multiplier": 2.0,
                "max_additional_slots": 10
            }
        }
    
    def generate_gameplay_features_template(self, creator_id: str) -> Dict[str, Any]:
        """Generate template for gameplay features mods."""
        return {
            "name": "Gameplay Features Mod",
            "description": "New body parts, behavior traits, mutation lines",
            "category": "gameplay_features",
            "effects": {
                "new_drone_types": [],
                "special_abilities": [],
                "unique_traits": []
            },
            "requirements": {
                "min_user_level": 5,
                "max_new_types": 5,
                "max_abilities": 3
            }
        }
```

### **Mod Validation**
```python
class ModValidator:
    """Validates mod templates for safety and balance."""
    
    def validate_mod_template(self, mod_template: ModTemplate) -> Dict[str, Any]:
        """Validate a mod template."""
        errors = []
        warnings = []
        
        # Check required fields
        if not mod_template.name:
            errors.append("Mod name is required")
        if not mod_template.description:
            errors.append("Mod description is required")
        if mod_template.cost_rp < 0:
            errors.append("Cost cannot be negative")
        if mod_template.daily_upkeep < 0:
            errors.append("Daily upkeep cannot be negative")
        
        # Check effects
        for file_path, changes in mod_template.effects.items():
            if not self.is_valid_file_path(file_path):
                errors.append(f"Invalid file path: {file_path}")
            
            for variable, value in changes.items():
                if not self.is_safe_variable_change(variable, value):
                    errors.append(f"Unsafe variable change: {variable}")
        
        # Check requirements
        for requirement, value in mod_template.requirements.items():
            if not self.is_valid_requirement(requirement, value):
                errors.append(f"Invalid requirement: {requirement}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def is_safe_variable_change(self, variable: str, value: Any) -> bool:
        """Check if a variable change is safe."""
        safe_variables = [
            "rp_gain_multiplier", "additional_mod_slots", "cooldown_reduction",
            "new_drone_types", "special_abilities", "unique_traits"
        ]
        
        return variable in safe_variables
```

---

## 📈 **MOD ECONOMY**

### **Mod Pricing**
```python
class ModPricing:
    """Handles mod pricing and economics."""
    
    def calculate_mod_cost(self, mod_template: ModTemplate) -> int:
        """Calculate the cost of a mod based on its effects."""
        base_cost = 100
        
        # Add cost based on effects
        for file_path, changes in mod_template.effects.items():
            for variable, value in changes.items():
                if variable == "rp_gain_multiplier":
                    base_cost += int((value - 1.0) * 500)
                elif variable == "additional_mod_slots":
                    base_cost += value * 200
                elif variable == "cooldown_reduction":
                    base_cost += int(value * 300)
        
        return max(50, base_cost)
    
    def calculate_daily_upkeep(self, mod_template: ModTemplate) -> int:
        """Calculate daily upkeep for a mod."""
        base_upkeep = 5
        
        # Add upkeep based on effects
        for file_path, changes in mod_template.effects.items():
            for variable, value in changes.items():
                if variable == "rp_gain_multiplier":
                    base_upkeep += int((value - 1.0) * 10)
                elif variable == "additional_mod_slots":
                    base_upkeep += value * 2
                elif variable == "cooldown_reduction":
                    base_upkeep += int(value * 5)
        
        return max(1, base_upkeep)
```

### **Mod Marketplace**
```python
class ModMarketplace:
    """Manages the mod marketplace and transactions."""
    
    def list_mods(self, category: str = None, creator_id: str = None) -> List[ModTemplate]:
        """List available mods with optional filtering."""
        mods = self.get_all_mods()
        
        if category:
            mods = [mod for mod in mods if mod.category == category]
        
        if creator_id:
            mods = [mod for mod in mods if mod.creator_id == creator_id]
        
        # Sort by rating and downloads
        mods.sort(key=lambda x: (x.rating, x.downloads), reverse=True)
        
        return mods
    
    def search_mods(self, query: str) -> List[ModTemplate]:
        """Search for mods by name or description."""
        mods = self.get_all_mods()
        query_lower = query.lower()
        
        matching_mods = []
        for mod in mods:
            if (query_lower in mod.name.lower() or 
                query_lower in mod.description.lower()):
                matching_mods.append(mod)
        
        return matching_mods
```

---

## 🚀 **MOD DEPLOYMENT**

### **Mod Approval Process**
```python
class ModApprovalSystem:
    """Handles mod approval and deployment."""
    
    def submit_mod_for_approval(self, mod_template: ModTemplate) -> bool:
        """Submit a mod for approval."""
        # Validate mod
        validation = self.mod_validator.validate_mod_template(mod_template)
        if not validation["valid"]:
            return False
        
        # Simulate mod in test environment
        simulation_result = self.simulate_mod(mod_template)
        if not simulation_result["balanced"]:
            return False
        
        # Add to approval queue
        mod_template.approved = False
        mod_template.created_at = datetime.now().isoformat()
        
        self.approval_queue.append(mod_template)
        return True
    
    def simulate_mod(self, mod_template: ModTemplate) -> Dict[str, Any]:
        """Simulate a mod in a test environment."""
        # Create test environment
        test_engine = self.create_test_simulation()
        
        # Apply mod to test environment
        test_engine.apply_mod(mod_template)
        
        # Run simulation
        test_engine.run_simulation(ticks=1000)
        
        # Analyze results
        return test_engine.analyze_mod_balance(mod_template.mod_id)
```

### **Mod Deployment**
```python
class ModDeployment:
    """Handles mod deployment and updates."""
    
    def deploy_mod(self, mod_template: ModTemplate):
        """Deploy an approved mod."""
        # Add to active mods database
        self.active_mods[mod_template.mod_id] = mod_template
        
        # Update symbolic files
        self.symbolic_file_manager.apply_mod_to_symbolic(mod_template)
        
        # Notify players
        self.notify_players_of_new_mod(mod_template)
    
    def update_mod(self, mod_id: str, new_version: ModTemplate):
        """Update an existing mod."""
        old_mod = self.active_mods.get(mod_id)
        if not old_mod:
            return False
        
        # Validate update
        validation = self.mod_validator.validate_mod_template(new_version)
        if not validation["valid"]:
            return False
        
        # Update mod
        self.active_mods[mod_id] = new_version
        
        # Update symbolic files
        self.symbolic_file_manager.update_mod_in_symbolic(mod_id, new_version)
        
        # Notify players
        self.notify_players_of_mod_update(mod_id, new_version)
        
        return True
```

---

## 📚 **MOD DOCUMENTATION**

### **Mod Creation Guide**
```markdown
# Creating Your First Mod

## 1. Choose a Category
- **Core Values**: Modify slots, RP gain, passive boosts
- **Gameplay Features**: New body parts, behavior traits, mutation lines
- **AI Behavior**: Local AI behavior modifications
- **Economy**: Economic system modifications

## 2. Generate a Template
Use `!mod template [category]` to generate a template for your chosen category.

## 3. Customize Your Mod
Edit the template to add your desired effects and requirements.

## 4. Submit for Approval
Use `!mod submit [template]` to submit your mod for approval.

## 5. Wait for Approval
Your mod will be tested in a simulation environment before approval.
```

### **Mod Best Practices**
```markdown
# Mod Development Best Practices

## Balance
- Don't make mods too powerful or too weak
- Consider the impact on other players
- Test your mod thoroughly before submission

## Creativity
- Create unique and interesting effects
- Consider how your mod interacts with others
- Think about long-term game balance

## Community
- Share your mods with the community
- Get feedback from other players
- Collaborate on mod development
```

---

**Sim-Rancher Mod System Documentation - Complete mod system guide** 🎮📚 