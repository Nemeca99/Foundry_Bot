# Framework Directory

This directory contains the core framework system that powers the Authoring Bot. It provides a modular plugin architecture for managing different functionalities.

## Files

### `framework_tool.py`
The main framework orchestration system that:
- Manages plugin loading and initialization
- Provides a unified interface for all bot functionalities
- Handles plugin communication and data sharing
- Coordinates between different components (Discord bot, personality engine, learning engine, etc.)
- Implements the core bot logic and message handling

## Plugins Directory (`plugins/`)

The plugins directory contains modular components that handle specific functionalities:

### Core AI Plugins
- **`personality_engine.py`** - Manages Luna's core personality traits, writing style, and conversation style
- **`personality_test_engine.py`** - Handles interactive personality tests and dynamic personality evolution with reward/punishment system
- **`enhanced_learning_engine.py`** - Advanced learning system with interaction analysis, concept extraction, and personality evolution
- **`personalization_engine.py`** - Adapts Luna's behavior based on user preferences and interaction history
- **`learning_engine.py`** - Basic learning and training data processing

### Content Generation Plugins
- **`text_generator.py`** - Handles text generation and creative writing assistance
- **`writing_assistant.py`** - Provides writing guidance, feedback, and story development tools
- **`image_generator.py`** - Generates images for book covers, character art, and illustrations
- **`voice_generator.py`** - Creates voice content and audio narration
- **`video_generator.py`** - Produces video content and book trailers

### Utility Plugins
- **`tool_manager.py`** - Manages external tools and API integrations

## How It Works

1. **Plugin Loading**: The framework automatically discovers and loads all Python files in the plugins directory
2. **Initialization**: Each plugin is initialized with access to the framework and other plugins
3. **Communication**: Plugins can communicate with each other through the framework
4. **Message Handling**: The framework routes messages to appropriate plugins based on content and context
5. **Data Persistence**: Plugins can save and load their state through the framework

## Usage

The framework is used by the main Discord bot (`discord/authoring_bot.py`) to handle all bot interactions. Plugins are automatically loaded when the bot starts up, and they work together to provide a comprehensive authoring assistant experience. 