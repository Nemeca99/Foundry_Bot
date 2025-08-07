# Core Directory

## Overview

The `core/` directory contains the fundamental system components that provide essential functionality for the AI writing companion. These core systems handle deployment, setup, testing, and utility functions that support the entire application. **ALL CORE SYSTEMS NOW HAVE COMPREHENSIVE QUEUE INTEGRATION!**

## Structure

```
core/
├── README.md                    # This documentation file
├── deployment/                  # Deployment and production systems
│   └── deploy.py               # Deployment automation script
├── setup/                       # Setup and initialization systems
│   └── setup_bot.py            # Bot setup and configuration
├── tests/                       # Testing framework and test suites
│   ├── run_all_tests.py        # Main test runner
│   ├── test_authoring_bot.py   # Discord bot tests
│   ├── test_learning.py        # Learning system tests
│   ├── test_message_splitting.py # Message processing tests
│   ├── test_model_connection.py # Model connection tests
│   ├── test_personality.py     # Personality system tests
│   ├── test_personalization.py # Personalization tests
│   ├── test_tool_use.py        # Tool usage tests
│   ├── test_writing_assistant.py # Writing assistant tests
│   ├── test_queue_system.py    # Queue system tests
│   └── test_core_queue_integration.py # Core queue integration tests
├── utils/                       # Utility functions and helpers
│   ├── status_summary.py        # System status reporting
│   └── system_health.py         # System health monitoring
├── project_manager.py           # Project management system (WITH QUEUE SYSTEM)
├── system_dashboard.py          # System dashboard (WITH QUEUE SYSTEM)
├── analytics_dashboard.py       # Analytics dashboard (WITH QUEUE SYSTEM)
└── health_check.py              # Health check system (WITH QUEUE SYSTEM)
```

## 🔄 **COMPREHENSIVE QUEUE SYSTEM**

### **Queue System Integration**
All core systems inherit from `QueueProcessor` and implement queue-based communication:

- **ProjectManager**: Queue-based project management operations
- **SystemDashboard**: Queue-based system monitoring and control
- **AnalyticsDashboard**: Queue-based analytics and reporting
- **SystemHealthChecker**: Queue-based health monitoring
- **StatusSummary**: Queue-based status reporting

### **Queue System Benefits**
1. **Loose Coupling**: Core systems communicate without direct dependencies
2. **Bottleneck Detection**: Real-time monitoring of core system performance
3. **Error Isolation**: Failures in one core system don't affect others
4. **Scalable Architecture**: Core systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting

### **Core System Queue Integration Pattern**
```python
class CoreSystem(QueueProcessor):
    def __init__(self):
        super().__init__("core_system_name")
        # Core system initialization
    
    def _process_item(self, item):
        """Process queue items for core system operations"""
        operation_type = item.data.get("type", "unknown")
        
        if operation_type == "core_operation":
            return self._handle_core_operation(item.data)
        else:
            return super()._process_item(item)
```

## Core Components

### deployment/deploy.py

The deployment automation system that handles production deployment:

#### Features:
- **Environment Setup**: Configure production environment
- **Dependency Installation**: Install required packages
- **Service Configuration**: Configure Discord bot service
- **Health Checks**: Verify deployment success
- **Rollback Support**: Emergency rollback capabilities

#### Usage:
```bash
# Deploy to production
python core/deployment/deploy.py --environment production

# Deploy to staging
python core/deployment/deploy.py --environment staging

# Rollback deployment
python core/deployment/deploy.py --rollback
```

### setup/setup_bot.py

The bot setup and configuration system:

#### Features:
- **Environment Configuration**: Set up environment variables
- **Discord Bot Setup**: Configure Discord bot settings
- **Database Initialization**: Set up required databases
- **Plugin Loading**: Initialize and load plugins
- **Permission Setup**: Configure bot permissions

#### Usage:
```bash
# Initial setup
python core/setup/setup_bot.py --first-time

# Update configuration
python core/setup/setup_bot.py --update-config

# Reset configuration
python core/setup/setup_bot.py --reset
```

### tests/

Comprehensive testing framework for all system components:

#### Test Suites:

##### run_all_tests.py
- **Purpose**: Main test runner for all test suites
- **Features**: Parallel test execution, detailed reporting
- **Output**: Comprehensive test results and coverage reports

##### test_authoring_bot.py
- **Purpose**: Test Discord bot functionality
- **Tests**: Command handling, message processing, error handling
- **Coverage**: All Discord bot features and commands

##### test_learning.py
- **Purpose**: Test AI learning system
- **Tests**: Learning algorithms, adaptation, memory
- **Coverage**: Learning engine functionality

##### test_message_splitting.py
- **Purpose**: Test message processing system
- **Tests**: Message splitting, context analysis, processing
- **Coverage**: Message handling and processing

##### test_model_connection.py
- **Purpose**: Test AI model connections
- **Tests**: Model loading, API connections, response handling
- **Coverage**: All AI model integrations

##### test_personality.py
- **Purpose**: Test personality system
- **Tests**: Personality traits, emotional responses, character development
- **Coverage**: Personality engine functionality

##### test_personalization.py
- **Purpose**: Test personalization system
- **Tests**: User preferences, adaptation, customization
- **Coverage**: Personalization engine functionality

##### test_tool_use.py
- **Purpose**: Test tool usage system
- **Tests**: Tool integration, usage tracking, effectiveness
- **Coverage**: Tool management and usage

##### test_writing_assistant.py
- **Purpose**: Test writing assistant functionality
- **Tests**: Writing suggestions, content generation, editing
- **Coverage**: Writing assistant features

##### test_queue_system.py
- **Purpose**: Test queue system functionality
- **Tests**: Queue communication, system integration, error handling
- **Coverage**: Queue system functionality

##### test_core_queue_integration.py
- **Purpose**: Test core system queue integration
- **Tests**: Core system communication, queue processing, integration
- **Coverage**: Core system queue integration

#### Running Tests:
```bash
# Run all tests
python core/tests/run_all_tests.py

# Run specific test suite
python core/tests/test_authoring_bot.py

# Run tests with coverage
python core/tests/run_all_tests.py --coverage

# Run tests in parallel
python core/tests/run_all_tests.py --parallel

# Test queue system
python core/tests/test_queue_system.py

# Test core queue integration
python core/tests/test_core_queue_integration.py
```

### utils/

Utility functions and helper systems:

#### status_summary.py
- **Purpose**: Generate system status reports
- **Features**: Component health, performance metrics, error reporting
- **Output**: Detailed status summaries for monitoring
- **Queue Integration**: Queue-based status reporting

#### system_health.py
- **Purpose**: Monitor overall system health
- **Features**: Health checks, performance monitoring, alerting
- **Output**: Health status and recommendations
- **Queue Integration**: Queue-based health monitoring

#### Usage:
```python
from core.utils.status_summary import generate_status_summary
from core.utils.system_health import check_system_health

# Generate status report
status = generate_status_summary()
print(status)

# Check system health
health = check_system_health()
if health['overall_health'] == 'healthy':
    print("System is healthy")
else:
    print(f"System issues: {health['issues']}")
```

## System Integration

### Framework Integration

Core systems integrate with the main framework through queue system:

```python
from framework.framework_tool import get_framework
from core.utils.system_health import check_system_health

# Get framework instance
framework = get_framework()

# Check system health through queue system
health = check_system_health()

# Report status through queue system
if health['overall_health'] == 'healthy':
    framework.log_info("System is healthy")
else:
    framework.log_error(f"System issues detected: {health['issues']}")
```

### Discord Bot Integration

Core systems support Discord bot functionality through queue system:

```python
# Test Discord bot commands through queue system
from core.tests.test_authoring_bot import test_discord_commands

# Run bot tests
test_results = test_discord_commands()
print(f"Bot tests passed: {test_results['passed']}")
```

### Plugin Integration

Core systems support plugin management through queue system:

```python
# Test plugin functionality through queue system
from core.tests.test_tool_use import test_plugin_integration

# Run plugin tests
plugin_results = test_plugin_integration()
print(f"Plugin tests passed: {plugin_results['passed']}")
```

## Queue System Architecture

### Core System Queue Integration

All core systems follow the same queue integration pattern:

```python
class CoreSystem(QueueProcessor):
    def __init__(self):
        super().__init__("core_system_name")
        # Initialize core system components
    
    def _process_item(self, item):
        """Process queue items for core system operations"""
        operation_type = item.data.get("type", "unknown")
        
        if operation_type == "core_operation":
            return self._handle_core_operation(item.data)
        elif operation_type == "health_check":
            return self._handle_health_check(item.data)
        elif operation_type == "status_request":
            return self._handle_status_request(item.data)
        else:
            return super()._process_item(item)
    
    def _handle_core_operation(self, data):
        """Handle core system operations"""
        # Core system operation logic
        pass
    
    def _handle_health_check(self, data):
        """Handle health check requests"""
        # Health check logic
        pass
    
    def _handle_status_request(self, data):
        """Handle status requests"""
        # Status reporting logic
        pass
```

### Queue Communication Between Core Systems

Core systems communicate through the queue system:

```python
# Send data between core systems
queue_manager.send_to_system("project_manager", "system_dashboard", {
    "type": "project_update",
    "project_id": "project_123",
    "status": "completed"
})

# Get system status through queue
status = queue_manager.get_system_stats("project_manager")
print(f"Project manager queue size: {status['input_queue_size']}")
```

## Deployment Process

### Production Deployment

1. **Environment Setup**:
   ```bash
   python core/deployment/deploy.py --environment production
   ```

2. **Health Checks**:
   ```bash
   python core/utils/system_health.py --check-all
   ```

3. **Service Start**:
   ```bash
   python start_bot.py
   ```

### Staging Deployment

1. **Staging Setup**:
   ```bash
   python core/deployment/deploy.py --environment staging
   ```

2. **Test Execution**:
   ```bash
   python core/tests/run_all_tests.py
   ```

3. **Validation**:
   ```bash
   python core/utils/system_health.py --validate
   ```

## Testing Framework

### Test Categories

#### Unit Tests
- **Purpose**: Test individual components
- **Coverage**: Function-level testing
- **Speed**: Fast execution
- **Isolation**: Independent test execution

#### Integration Tests
- **Purpose**: Test component interactions
- **Coverage**: System-level testing
- **Speed**: Medium execution time
- **Dependencies**: Component dependencies

#### System Tests
- **Purpose**: Test entire system
- **Coverage**: End-to-end testing
- **Speed**: Slower execution
- **Environment**: Full system environment

#### Queue System Tests
- **Purpose**: Test queue system integration
- **Coverage**: Queue communication and processing
- **Speed**: Medium execution time
- **Dependencies**: Queue system dependencies

### Test Execution

```bash
# Run unit tests only
python core/tests/run_all_tests.py --unit

# Run integration tests only
python core/tests/run_all_tests.py --integration

# Run system tests only
python core/tests/run_all_tests.py --system

# Run queue system tests
python core/tests/test_queue_system.py

# Run all tests with coverage
python core/tests/run_all_tests.py --coverage --verbose
```

### Test Reporting

The testing framework provides detailed reporting:

- **Test Results**: Pass/fail status for each test
- **Coverage Reports**: Code coverage metrics
- **Performance Metrics**: Test execution times
- **Error Details**: Detailed error information
- **Recommendations**: Improvement suggestions
- **Queue System Metrics**: Queue performance and communication metrics

## Monitoring and Health

### System Health Monitoring

The core system provides comprehensive health monitoring through queue system:

#### Health Metrics
- **Component Status**: Individual component health
- **Performance Metrics**: Response times and throughput
- **Error Rates**: Error frequency and types
- **Resource Usage**: Memory, CPU, and disk usage
- **Dependency Status**: External service health
- **Queue Metrics**: Queue performance and communication

#### Health Checks
```python
from core.utils.system_health import perform_health_check

# Perform comprehensive health check through queue system
health = perform_health_check()

# Check specific components
discord_health = health['components']['discord_bot']
framework_health = health['components']['framework']
plugin_health = health['components']['plugins']
queue_health = health['components']['queue_system']
```

### Status Reporting

The system provides detailed status reports through queue system:

```python
from core.utils.status_summary import generate_detailed_summary

# Generate detailed status report through queue system
summary = generate_detailed_summary()

# Print component status
for component, status in summary['components'].items():
    print(f"{component}: {status['status']}")
```

## Configuration Management

### Environment Configuration

Core systems manage environment configuration through queue system:

```python
# Load configuration through queue system
from core.setup.setup_bot import load_configuration

config = load_configuration()

# Access configuration values
discord_token = config['discord_token']
database_url = config['database_url']
model_path = config['model_path']
```

### Configuration Validation

The system validates configuration through queue system:

```python
from core.setup.setup_bot import validate_configuration

# Validate configuration through queue system
validation_result = validate_configuration()

if validation_result['valid']:
    print("Configuration is valid")
else:
    print(f"Configuration errors: {validation_result['errors']}")
```

## Error Handling

### Comprehensive Error Handling

Core systems provide robust error handling through queue system:

```python
from core.utils.system_health import handle_system_error

try:
    # System operation through queue system
    result = perform_system_operation()
except Exception as e:
    # Handle error through queue system
    error_info = handle_system_error(e)
    print(f"Error handled: {error_info['message']}")
```

### Error Recovery

The system includes error recovery mechanisms through queue system:

```python
from core.utils.system_health import attempt_error_recovery

# Attempt error recovery through queue system
recovery_result = attempt_error_recovery(error_type, error_context)

if recovery_result['success']:
    print("Error recovered successfully")
else:
    print(f"Recovery failed: {recovery_result['reason']}")
```

## Performance Optimization

### System Optimization

Core systems include performance optimization through queue system:

```python
from core.utils.system_health import optimize_system_performance

# Optimize system performance through queue system
optimization_result = optimize_system_performance()

print(f"Performance improved: {optimization_result['improvement']}%")
```

### Resource Management

The system manages resources efficiently through queue system:

```python
from core.utils.system_health import monitor_resource_usage

# Monitor resource usage through queue system
usage = monitor_resource_usage()

print(f"CPU Usage: {usage['cpu']}%")
print(f"Memory Usage: {usage['memory']}%")
print(f"Disk Usage: {usage['disk']}%")
```

## Queue System Benefits

### Achieved Benefits

1. **Loose Coupling**: Core systems communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in one core system don't affect others
4. **Scalable Architecture**: Core systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting system

### Queue System Features

- **QueueManager**: Central queue management and monitoring
- **QueueProcessor**: Base class for all core systems
- **QueueItem**: Standardized data structure for inter-system communication
- **SystemQueue**: Individual system queue management
- **Alert System**: Configurable thresholds for warnings and critical alerts

## Future Enhancements

Planned improvements:

1. **Automated Deployment**: CI/CD pipeline integration
2. **Advanced Monitoring**: Real-time monitoring dashboard
3. **Performance Profiling**: Detailed performance analysis
4. **Automated Testing**: Continuous testing integration
5. **Configuration Management**: Advanced configuration system
6. **Error Prediction**: Predictive error detection
7. **Queue System Enhancement**: Advanced queue features

## Best Practices

### Development
- Write comprehensive tests for all components
- Follow error handling best practices
- Monitor system performance regularly
- Document all configuration options
- Use queue system for all inter-system communication

### Deployment
- Test thoroughly before production deployment
- Monitor system health after deployment
- Have rollback procedures ready
- Keep deployment logs for troubleshooting
- Monitor queue system performance

### Maintenance
- Regular health checks and monitoring
- Update dependencies regularly
- Review and optimize performance
- Maintain comprehensive documentation
- Monitor queue system metrics

## Support

For core system support:

1. Check system health and status through queue system
2. Review error logs and reports
3. Run comprehensive test suites
4. Verify configuration settings
5. Monitor resource usage
6. Check queue system performance

The core systems provide the foundation for reliable, scalable, and maintainable AI writing companion functionality with comprehensive queue system integration for loose coupling and error isolation. 