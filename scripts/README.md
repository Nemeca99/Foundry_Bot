# Scripts Directory

## Overview

The `scripts/` directory contains utility scripts and automation tools for the AI writing companion. These scripts handle system setup, testing, bot launching, and various automation tasks. **ALL SCRIPT SYSTEMS NOW HAVE COMPREHENSIVE QUEUE INTEGRATION!**

## Structure

```
scripts/
├── README.md                    # This documentation file
├── start_bot.py                 # Bot launcher script (WITH QUEUE SYSTEM)
├── setup.py                     # System setup script (WITH QUEUE SYSTEM)
└── run_tests.py                 # Test runner script (WITH QUEUE SYSTEM)
```

## 🔄 **COMPREHENSIVE QUEUE SYSTEM**

### **Queue System Integration**
The scripts system integrates with the comprehensive queue system for scalable, loosely-coupled architecture:

- **StartBot**: Queue-based bot launching operations
- **SetupScript**: Queue-based system setup operations
- **TestRunner**: Queue-based test execution operations
- **Script Integration**: Queue-based integration with other systems
- **Automation Management**: Queue-based automation task management

### **Queue System Benefits**
1. **Loose Coupling**: Script systems communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in script operations don't affect other systems
4. **Scalable Architecture**: Script systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting

### **Script System Queue Integration Pattern**
```python
class ScriptManager(QueueProcessor):
    def __init__(self):
        super().__init__("script_manager")
        # Script system initialization
    
    def _process_item(self, item):
        """Process queue items for script operations"""
        operation_type = item.data.get("type", "unknown")
        
        if operation_type == "start_bot":
            return self._handle_start_bot(item.data)
        elif operation_type == "run_setup":
            return self._handle_run_setup(item.data)
        elif operation_type == "run_tests":
            return self._handle_run_tests(item.data)
        else:
            return super()._process_item(item)
```

## Core Components

### start_bot.py

The bot launcher script with queue integration:

#### Features:
- **Bot Initialization**: Initialize and start Discord bots through queue system
- **System Integration**: Integrate with framework and plugins through queue system
- **Error Handling**: Comprehensive error handling with queue-based logging
- **Configuration Management**: Load and apply configurations through queue system
- **Queue Integration**: Complete queue system integration for scalable launching

#### Usage:
```python
# Start bot through queue system
await send_to_queue("script_manager", {
    "type": "start_bot",
    "bot_type": "enhanced_luna_bot",
    "config": {
        "token": "your_discord_token",
        "prefix": "!",
        "intents": ["messages", "reactions"]
    }
})

# Check bot status through queue system
status = await send_to_queue("script_manager", {
    "type": "check_bot_status",
    "bot_name": "enhanced_luna_bot"
})
```

### setup.py

The system setup script with queue integration:

#### Features:
- **Dependency Installation**: Install required packages through queue system
- **Configuration Setup**: Set up system configurations through queue system
- **Directory Creation**: Create necessary directories through queue system
- **Environment Setup**: Configure environment variables through queue system
- **Queue Integration**: Complete queue system integration for scalable setup

#### Usage:
```python
# Run system setup through queue system
await send_to_queue("script_manager", {
    "type": "run_setup",
    "setup_type": "full",
    "options": {
        "install_dependencies": True,
        "create_directories": True,
        "setup_configurations": True
    }
})

# Check setup status through queue system
setup_status = await send_to_queue("script_manager", {
    "type": "check_setup_status"
})
```

### run_tests.py

The test runner script with queue integration:

#### Features:
- **Test Execution**: Run test suites through queue system
- **Test Discovery**: Discover and organize tests through queue system
- **Result Reporting**: Generate test reports through queue system
- **Performance Testing**: Run performance tests through queue system
- **Queue Integration**: Complete queue system integration for scalable testing

#### Usage:
```python
# Run all tests through queue system
await send_to_queue("script_manager", {
    "type": "run_tests",
    "test_suite": "all",
    "options": {
        "verbose": True,
        "generate_report": True,
        "performance_testing": True
    }
})

# Run specific test through queue system
await send_to_queue("script_manager", {
    "type": "run_tests",
    "test_suite": "queue_integration",
    "test_name": "test_final_queue_integration"
})
```

## Script Operations

### Bot Management

Manage Discord bots through queue system:

```python
# Start multiple bots through queue system
bots = ["enhanced_luna_bot", "writing_assistant_bot", "character_system_bot"]
for bot in bots:
    await send_to_queue("script_manager", {
        "type": "start_bot",
        "bot_type": bot,
        "config": {
            "token": "your_discord_token",
            "prefix": "!",
            "intents": ["messages", "reactions"]
        }
    })

# Stop bot through queue system
await send_to_queue("script_manager", {
    "type": "stop_bot",
    "bot_name": "enhanced_luna_bot"
})

# Restart bot through queue system
await send_to_queue("script_manager", {
    "type": "restart_bot",
    "bot_name": "enhanced_luna_bot"
})
```

### System Setup

Manage system setup through queue system:

```python
# Full system setup through queue system
await send_to_queue("script_manager", {
    "type": "run_setup",
    "setup_type": "full",
    "options": {
        "install_dependencies": True,
        "create_directories": True,
        "setup_configurations": True,
        "setup_database": True,
        "setup_queue_system": True
    }
})

# Partial setup through queue system
await send_to_queue("script_manager", {
    "type": "run_setup",
    "setup_type": "partial",
    "components": ["dependencies", "configurations"]
})

# Verify setup through queue system
verification_result = await send_to_queue("script_manager", {
    "type": "verify_setup",
    "components": ["all"]
})
```

### Test Execution

Execute tests through queue system:

```python
# Run comprehensive test suite through queue system
await send_to_queue("script_manager", {
    "type": "run_tests",
    "test_suite": "comprehensive",
    "options": {
        "verbose": True,
        "generate_report": True,
        "performance_testing": True,
        "queue_integration_testing": True
    }
})

# Run specific test categories through queue system
test_categories = ["queue_integration", "framework", "discord_bots", "emotional_systems"]
for category in test_categories:
    await send_to_queue("script_manager", {
        "type": "run_tests",
        "test_suite": category,
        "options": {
            "verbose": True,
            "generate_report": True
        }
    })

# Run performance tests through queue system
await send_to_queue("script_manager", {
    "type": "run_performance_tests",
    "test_types": ["queue_performance", "system_performance", "bot_performance"]
})
```

## Integration with Other Systems

### Framework Integration

Scripts integrate with the main framework through queue system:

```python
# Get framework instance through queue system
framework = await send_to_queue("framework", {
    "type": "get_framework"
})

# Initialize framework through queue system
await send_to_queue("script_manager", {
    "type": "initialize_framework",
    "framework_config": {
        "plugins": ["all"],
        "queue_system": True,
        "monitoring": True
    }
})

# Load plugins through queue system
plugins = ["personality_engine", "personalization_engine", "writing_assistant"]
for plugin in plugins:
    await send_to_queue("script_manager", {
        "type": "load_plugin",
        "plugin_name": plugin
    })
```

### Discord Integration

Scripts integrate with Discord bots through queue system:

```python
# Initialize Discord bots through queue system
bots = ["enhanced_luna_bot", "writing_assistant_bot"]
for bot in bots:
    await send_to_queue("script_manager", {
        "type": "initialize_discord_bot",
        "bot_name": bot,
        "config": {
            "token": "your_discord_token",
            "prefix": "!",
            "intents": ["messages", "reactions"]
        }
    })

# Start Discord bots through queue system
await send_to_queue("script_manager", {
    "type": "start_discord_bots",
    "bot_names": bots
})
```

### Queue System Integration

Scripts integrate with queue system management:

```python
# Initialize queue system through queue system
await send_to_queue("script_manager", {
    "type": "initialize_queue_system",
    "config": {
        "max_queue_size": 1000,
        "timeout": 30,
        "alert_thresholds": {
            "warning": 0.7,
            "critical": 0.9
        }
    }
})

# Monitor queue system through queue system
queue_status = await send_to_queue("script_manager", {
    "type": "monitor_queue_system"
})

# Clean up queue system through queue system
await send_to_queue("script_manager", {
    "type": "cleanup_queue_system"
})
```

## Performance Optimization

### Script Performance

Optimize script performance through queue system:

```python
# Check script performance through queue system
performance_metrics = await send_to_queue("script_manager", {
    "type": "check_script_performance",
    "script_name": "start_bot"
})

# Optimize script execution through queue system
await send_to_queue("script_manager", {
    "type": "optimize_script",
    "script_name": "start_bot",
    "optimization_type": "performance"
})
```

### Resource Management

Manage system resources through queue system:

```python
# Check system resources through queue system
resource_status = await send_to_queue("script_manager", {
    "type": "check_system_resources"
})

# Optimize resource usage through queue system
await send_to_queue("script_manager", {
    "type": "optimize_resources",
    "optimization_type": "memory_and_cpu"
})
```

## Error Handling

### Comprehensive Error Handling

Handle errors through queue system:

```python
# Handle script errors through queue system
await send_to_queue("script_manager", {
    "type": "handle_error",
    "error_type": "script_execution_error",
    "error_details": {
        "script": "start_bot",
        "error": "Connection failed",
        "timestamp": "2024-01-15T10:30:00Z"
    }
})

# Log errors through queue system
await send_to_queue("script_manager", {
    "type": "log_error",
    "error_data": {
        "level": "ERROR",
        "message": "Bot startup failed",
        "details": "Connection timeout"
    }
})
```

## Queue System Benefits

### Achieved Benefits

1. **Loose Coupling**: Script systems communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in script operations don't affect other systems
4. **Scalable Architecture**: Script systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting system

### Queue System Features

- **QueueManager**: Central queue management and monitoring
- **QueueProcessor**: Base class for all script systems
- **QueueItem**: Standardized data structure for inter-system communication
- **SystemQueue**: Individual script system queue management
- **Alert System**: Configurable thresholds for warnings and critical alerts

## Future Enhancements

Planned improvements:

1. **Advanced Automation**: More sophisticated automation capabilities
2. **Real-time Monitoring**: Real-time script monitoring and alerting
3. **Interactive Scripts**: Interactive script execution capabilities
4. **Script Learning**: Learn and adapt to system patterns
5. **Batch Optimization**: Advanced batch processing and optimization
6. **Performance Prediction**: Predict script performance before execution
7. **Queue System Enhancement**: Advanced queue features

## Best Practices

### Script Development
- Use queue system for all script operations
- Implement comprehensive error handling
- Monitor script performance continuously
- Use queue system for all inter-system communication

### Automation
- Maintain script reliability and consistency
- Use appropriate automation levels for different tasks
- Backup important script configurations
- Monitor queue system performance

### Integration
- Ensure seamless integration with other systems through queue system
- Maintain consistent data flow between components
- Optimize for user experience
- Monitor performance and quality metrics
- Use queue system for all inter-system communication

## Support

For script system support:

1. Check script initialization and configuration through queue system
2. Verify script execution and performance through queue system
3. Test script integration with other systems through queue system
4. Review script error handling and logging through queue system
5. Monitor script system performance
6. Monitor queue system performance

The scripts system provides essential automation and utility capabilities for the AI writing companion, enabling efficient system management and operation through complete queue system integration for scalable, loosely-coupled architecture. 