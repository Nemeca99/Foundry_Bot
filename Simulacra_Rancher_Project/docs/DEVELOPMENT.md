# 👨‍💻 **SIM-RANCHER DEVELOPMENT GUIDE**

## 🎯 **DEVELOPMENT OVERVIEW**

This guide provides comprehensive information for developers contributing to the Sim-Rancher project, including coding standards, testing procedures, and contribution guidelines.

---

## 🛠️ **DEVELOPMENT ENVIRONMENT SETUP**

### **1. Prerequisites**
```bash
# Required Software
- Python 3.8+
- Git
- VS Code (recommended)
- Discord Developer Account
- LM Studio (for AI development)
- Ollama (for AI development)
```

### **2. Local Development Setup**
```bash
# Clone repository
git clone <repository-url>
cd Simulacra_Rancher_Project

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### **3. IDE Configuration**

#### **VS Code Settings**
```json
{
  "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### **Recommended Extensions**
- Python (Microsoft)
- Pylance
- Black Formatter
- Python Docstring Generator
- GitLens
- Discord Presence

---

## 📁 **PROJECT STRUCTURE**

### **Core Systems**
```
core/
├── bot.py                 # Main Discord bot
├── config.py              # Configuration management
├── mod_system.py          # Mod system implementation
├── clds.py               # C.L.D.S. body parts system
├── economy.py             # RP economy system
├── disasters.py           # Disaster and survival mechanics
├── hunting_system.py      # Hunting and catching system
├── kingdom_system.py      # 7 kingdoms system
├── leaderboard.py         # Exclusive leaderboard
├── resource_system.py     # Resource gathering
├── trade_system.py        # Player-to-player trading
├── scientific_game_engine.py # Physics calculations
├── survival_engine.py     # Survival mechanics
├── personality_system.py  # AI personality generation
├── psychological_system.py # Psychological manipulation
├── dream_cycle.py         # Dream cycle learning
├── network_consciousness.py # Network consciousness
├── health_monitor.py      # Health monitoring
├── gpu_personality.py     # GPU personality engine
├── cpu_backend.py         # CPU backend engine
├── ai_circuit_breaker.py  # AI failure protection
├── discord_channels.py    # Discord channel management
└── lyra_scp_prompt.py    # SCP lore integration
```

### **Modules**
```
modules/
├── ai_queue_system.py     # AI request queuing
├── analytics_system.py    # Analytics and tracking
├── autonomous_bot.py      # Autonomous bot features
├── bot_creator.py         # Bot creation tools
├── daydream_system.py     # Daydream mechanics
├── dream_cycle_manager.py # Dream cycle management
├── dynamic_channel_manager.py # Dynamic channel management
├── feedback_system.py     # User feedback system
├── greeter_system.py      # User greeting system
├── logic_block_engine.py  # Logic block processing
├── memory_system.py       # Memory management
├── personality_engine.py  # Personality generation
├── poll_system.py         # Polling system
├── premium_manager.py     # Premium feature management
├── privacy_manager.py     # Privacy controls
├── quantum_kitchen.py     # Quantum mechanics
├── reminder_system.py     # Reminder system
├── sesh_time_integration.py # Session time tracking
├── staggered_kitchen.py   # Staggered processing
├── three_tier_architecture.py # Three-tier architecture
└── user_settings.py       # User settings management
```

---

## 🎨 **CODING STANDARDS**

### **1. Python Style Guide**

#### **PEP 8 Compliance**
```python
# Use 4 spaces for indentation
def example_function():
    """Docstring for function."""
    if condition:
        do_something()
    else:
        do_something_else()

# Use snake_case for variables and functions
user_id = "123456789"
rp_balance = 1000

# Use PascalCase for classes
class UserProfile:
    def __init__(self, user_id: str):
        self.user_id = user_id
```

#### **Type Hints**
```python
from typing import List, Dict, Optional, Union

def calculate_rp_cost(
    base_cost: int,
    multiplier: float,
    user_level: int
) -> int:
    """Calculate RP cost with modifiers."""
    return int(base_cost * multiplier * (1 + user_level * 0.1))

def get_user_drones(user_id: str) -> List[Dict[str, Union[str, int]]]:
    """Get all drones for a user."""
    return []
```

#### **Docstrings**
```python
def hatch_drone(drone_type: str, name: str, user_id: str) -> Dict[str, Any]:
    """
    Create a new DigiDrone for a user.
    
    Args:
        drone_type: Type of drone to create (fire, water, earth, etc.)
        name: Name for the new drone
        user_id: Discord user ID of the owner
        
    Returns:
        Dictionary containing drone information
        
    Raises:
        ValueError: If drone_type is invalid
        InsufficientRPError: If user doesn't have enough RP
    """
    pass
```

### **2. Error Handling**

#### **Custom Exceptions**
```python
class SimRancherError(Exception):
    """Base exception for Sim-Rancher."""
    pass

class InsufficientRPError(SimRancherError):
    """Raised when user doesn't have enough RP."""
    pass

class DroneNotFoundError(SimRancherError):
    """Raised when drone is not found."""
    pass

class KingdomNotFoundError(SimRancherError):
    """Raised when kingdom is not found."""
    pass
```

#### **Error Handling Patterns**
```python
async def process_command(ctx, command_name: str, *args):
    """Process a Discord command with error handling."""
    try:
        result = await execute_command(command_name, *args)
        await ctx.send(f"✅ {result}")
    except InsufficientRPError:
        await ctx.send("❌ Insufficient RP for this action")
    except DroneNotFoundError:
        await ctx.send("❌ Drone not found")
    except Exception as e:
        logger.error(f"Unexpected error in {command_name}: {e}")
        await ctx.send("❌ An unexpected error occurred")
```

### **3. Logging**

#### **Structured Logging**
```python
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def log_user_action(user_id: str, action: str, details: Dict[str, Any]):
    """Log user actions in structured format."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "action": action,
        "details": details,
        "level": "INFO"
    }
    logger.info(json.dumps(log_entry))
```

---

## 🧪 **TESTING FRAMEWORK**

### **1. Unit Testing**

#### **Test Structure**
```python
# tests/test_economy.py
import pytest
from unittest.mock import Mock, patch
from core.economy import calculate_rp_cost, process_transaction

class TestEconomy:
    def test_calculate_rp_cost(self):
        """Test RP cost calculation."""
        cost = calculate_rp_cost(100, 1.5, 5)
        assert cost == 175  # 100 * 1.5 * (1 + 5 * 0.1)
    
    def test_insufficient_rp(self):
        """Test insufficient RP error."""
        with pytest.raises(InsufficientRPError):
            process_transaction("user123", 1000, 500)
    
    @patch('core.economy.get_user_rp')
    def test_successful_transaction(self, mock_get_rp):
        """Test successful transaction."""
        mock_get_rp.return_value = 1000
        result = process_transaction("user123", 500, 1000)
        assert result["success"] is True
```

#### **Test Configuration**
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### **2. Integration Testing**

#### **Discord Bot Testing**
```python
# tests/test_discord_bot.py
import pytest
from discord.ext.test import verify_message
from core.bot import bot

@pytest.mark.asyncio
async def test_hatch_command():
    """Test hatch command."""
    ctx = Mock()
    ctx.author.id = "123456789"
    
    await bot.get_command("hatch")(ctx, "fire", "TestDrone")
    
    verify_message(ctx, "✅ Drone created successfully")
```

#### **Database Testing**
```python
# tests/test_database.py
import pytest
from core.database import Database

@pytest.fixture
def test_db():
    """Create test database."""
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()

def test_user_creation(test_db):
    """Test user creation."""
    user_id = "123456789"
    test_db.create_user(user_id, "TestUser")
    
    user = test_db.get_user(user_id)
    assert user["name"] == "TestUser"
    assert user["rp"] == 100
```

### **3. Simulation Testing**

#### **Simulation Engine Tests**
```python
# tests/test_simulation.py
import pytest
from simulation.infinite_simulation_engine import InfiniteSimulationEngine

class TestSimulation:
    def test_user_creation(self):
        """Test user creation in simulation."""
        engine = InfiniteSimulationEngine()
        user = engine.create_user("test_user", "TestUser")
        
        assert user.id == "test_user"
        assert user.name == "TestUser"
        assert user.rp == 100
    
    def test_economy_simulation(self):
        """Test economy simulation."""
        engine = InfiniteSimulationEngine()
        engine.run_simulation(ticks=100)
        
        assert engine.global_multiplier >= 0.1
        assert engine.global_multiplier <= 3.0
```

---

## 🔄 **CONTRIBUTION WORKFLOW**

### **1. Git Workflow**

#### **Branch Naming**
```bash
# Feature branches
feature/add-new-drone-type
feature/improve-economy-system
feature/fix-hunting-bug

# Bug fix branches
fix/drone-creation-error
fix/memory-leak-issue
fix/database-connection-timeout

# Documentation branches
docs/update-api-reference
docs/add-deployment-guide
docs/fix-typos
```

#### **Commit Messages**
```bash
# Conventional commit format
feat: add new fire drone type
fix: resolve memory leak in simulation
docs: update API reference
test: add unit tests for economy system
refactor: improve error handling
style: format code with black
```

### **2. Pull Request Process**

#### **PR Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

### **3. Code Review Guidelines**

#### **Review Checklist**
- [ ] Code follows project style guidelines
- [ ] Appropriate error handling implemented
- [ ] Logging added for important operations
- [ ] Tests added for new functionality
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact considered

---

## 🚀 **DEVELOPMENT TOOLS**

### **1. Pre-commit Hooks**

#### **Git Hooks Configuration**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### **2. Development Scripts**

#### **Setup Script**
```bash
#!/bin/bash
# dev_setup.sh

echo "Setting up Sim-Rancher development environment..."

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial tests
pytest

echo "Development environment setup complete!"
```

#### **Testing Script**
```bash
#!/bin/bash
# run_tests.sh

echo "Running Sim-Rancher tests..."

# Run unit tests
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Run simulation tests
pytest tests/simulation/ -v

# Generate coverage report
pytest --cov=core --cov=modules --cov-report=html

echo "Tests completed!"
```

---

## 📊 **PERFORMANCE OPTIMIZATION**

### **1. Profiling Tools**

#### **cProfile Integration**
```python
import cProfile
import pstats

def profile_function(func, *args, **kwargs):
    """Profile a function and return statistics."""
    profiler = cProfile.Profile()
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    
    return result
```

#### **Memory Profiling**
```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Function that uses a lot of memory."""
    large_list = [i for i in range(1000000)]
    return sum(large_list)
```

### **2. Performance Monitoring**

#### **Response Time Tracking**
```python
import time
import functools

def track_performance(func):
    """Decorator to track function performance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper
```

---

## 🔧 **DEBUGGING GUIDE**

### **1. Common Issues**

#### **Discord Bot Issues**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check bot permissions
async def check_bot_permissions(guild):
    """Check if bot has required permissions."""
    bot_member = guild.get_member(bot.user.id)
    permissions = bot_member.guild_permissions
    
    required_permissions = [
        "send_messages",
        "use_slash_commands",
        "manage_roles",
        "embed_links"
    ]
    
    missing_permissions = []
    for permission in required_permissions:
        if not getattr(permissions, permission):
            missing_permissions.append(permission)
    
    return missing_permissions
```

#### **AI Model Issues**
```python
# Test AI model connectivity
async def test_ai_models():
    """Test AI model connections."""
    try:
        # Test LM Studio
        response = await test_lm_studio_connection()
        logger.info("LM Studio connection successful")
    except Exception as e:
        logger.error(f"LM Studio connection failed: {e}")
    
    try:
        # Test Ollama
        response = await test_ollama_connection()
        logger.info("Ollama connection successful")
    except Exception as e:
        logger.error(f"Ollama connection failed: {e}")
```

### **2. Debugging Tools**

#### **Interactive Debugger**
```python
import pdb

def debug_function():
    """Function with debugger breakpoint."""
    x = 1
    y = 2
    pdb.set_trace()  # Breakpoint here
    result = x + y
    return result
```

#### **Logging Configuration**
```python
# debug_config.py
import logging

def setup_debug_logging():
    """Setup detailed logging for debugging."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('debug.log'),
            logging.StreamHandler()
        ]
    )
```

---

## 📚 **LEARNING RESOURCES**

### **1. Project-Specific Documentation**
- **Architecture Guide**: `docs/ARCHITECTURE.md`
- **API Reference**: `docs/API_REFERENCE.md`
- **Deployment Guide**: `docs/DEPLOYMENT.md`
- **Simulation Guide**: `docs/SIMULATION.md`

### **2. External Resources**
- **Discord.py Documentation**: https://discordpy.readthedocs.io/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **Pytest Documentation**: https://docs.pytest.org/
- **Black Code Formatter**: https://black.readthedocs.io/

### **3. Community Resources**
- **Discord Developer Portal**: https://discord.com/developers/docs
- **Python Discord**: https://discord.gg/python
- **GitHub Issues**: Project issue tracker
- **Discord Server**: Community discussion

---

## 🎯 **CONTRIBUTION GUIDELINES**

### **1. Before Contributing**
- Read the project documentation
- Check existing issues and pull requests
- Join the Discord community
- Understand the project architecture

### **2. Development Process**
1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests for new functionality**
5. **Update documentation**
6. **Run the test suite**
7. **Submit a pull request**

### **3. Code Quality Standards**
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Add appropriate error handling
- Include logging for important operations
- Write unit tests for new features

### **4. Review Process**
- All code must be reviewed before merging
- Address review comments promptly
- Maintain a respectful and constructive environment
- Focus on code quality and functionality

---

**Sim-Rancher Development Guide - Complete development documentation for contributors** 👨‍💻📚 