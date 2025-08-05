# Core Directory

This directory contains the core system components that support the Authoring Bot's functionality, including testing, utilities, setup, and deployment.

## Directories

### `tests/`
Contains comprehensive test suites for all bot components:
- **`run_all_tests.py`** - Main test runner that executes all test suites
- **`test_authoring_bot.py`** - Tests for Discord bot functionality and commands
- **`test_learning.py`** - Tests for learning engine and training data processing
- **`test_message_splitting.py`** - Tests for message processing and splitting logic
- **`test_model_connection.py`** - Tests for AI model connectivity and responses
- **`test_personality.py`** - Tests for personality engine and trait management
- **`test_personalization.py`** - Tests for personalization engine and user adaptation
- **`test_tool_use.py`** - Tests for tool manager and external integrations
- **`test_writing_assistant.py`** - Tests for writing assistant functionality

### `utils/`
Contains utility modules for system monitoring and status reporting:
- **`system_health.py`** - Comprehensive system health monitoring and diagnostics
- **`status_summary.py`** - Generates status summaries and system reports

### `setup/`
Contains bot setup and initialization utilities:
- **`setup_bot.py`** - Bot initialization and configuration setup

### `deployment/`
Contains deployment and production utilities:
- **`deploy.py`** - Production deployment scripts and configuration

## How It Works

1. **Testing**: The test suite validates all bot components work correctly
2. **Monitoring**: Utility modules provide system health and status information
3. **Setup**: Setup scripts handle bot initialization and configuration
4. **Deployment**: Deployment scripts manage production deployment

## Usage

- **Development**: Run tests with `python run_tests.py` or individual test files
- **Monitoring**: Use utility modules to check system health and status
- **Setup**: Use setup scripts for initial bot configuration
- **Deployment**: Use deployment scripts for production deployment

## Testing Strategy

The test suite follows a comprehensive approach:
- Unit tests for individual components
- Integration tests for plugin interactions
- End-to-end tests for complete workflows
- Mock testing for external dependencies
- Performance testing for critical functions 