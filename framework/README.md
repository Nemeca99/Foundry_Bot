# Framework Directory

## Overview

The `framework/` directory contains the core framework system that powers the entire AI writing companion. This is the heart of the system, providing plugin architecture, tool management, and the main framework interface.

## Structure

```
framework/
├── framework_tool.py          # Main framework interface and plugin manager
└── plugins/                   # Plugin system for extensible functionality
    ├── image_generator.py     # Basic image generation
    ├── learning_engine.py     # AI learning and adaptation system
    ├── personality_engine.py  # Personality management system
    ├── personalization_engine.py # User personalization system
    ├── text_generator.py      # Text generation capabilities
    ├── tool_manager.py        # Tool management and coordination
    ├── video_generator.py     # Basic video generation
    ├── voice_generator.py     # Basic voice generation
    ├── writing_assistant.py   # Writing assistance system
    ├── enhanced_image_generator.py      # Enhanced image generation with multiple models
    ├── enhanced_voice_generator.py     # Enhanced voice generation with multiple TTS engines
    ├── enhanced_video_generator.py     # Enhanced video generation with multiple APIs
    ├── enhanced_audio_processor.py     # Enhanced audio processing with effects
    └── multimodal_orchestrator.py     # Unified multimodal content coordination
```

## Core Components

### framework_tool.py

The main framework interface that provides:

- **Plugin Management**: Load, unload, and manage plugins dynamically
- **Configuration Management**: Centralized configuration handling
- **Tool Coordination**: Coordinate between different tools and systems
- **Error Handling**: Comprehensive error handling and logging
- **Extension System**: Easy plugin development and integration

#### Key Methods:
- `get_framework()` - Get the main framework instance
- `get_plugin(name)` - Retrieve a specific plugin
- `load_plugin(name)` - Load a plugin dynamically
- `get_config()` - Access framework configuration
- `register_tool(name, tool)` - Register new tools

### Plugin System

The plugin system allows for modular, extensible functionality:

#### Basic Plugins:
- **image_generator.py**: Basic image generation capabilities
- **voice_generator.py**: Basic voice generation capabilities
- **video_generator.py**: Basic video generation capabilities
- **text_generator.py**: Text generation and processing
- **writing_assistant.py**: Writing assistance and guidance

#### Enhanced Plugins:
- **enhanced_image_generator.py**: Advanced image generation with multiple models
- **enhanced_voice_generator.py**: Advanced voice generation with multiple TTS engines
- **enhanced_video_generator.py**: Advanced video generation with multiple APIs
- **enhanced_audio_processor.py**: Advanced audio processing with effects
- **multimodal_orchestrator.py**: Unified multimodal content coordination

#### AI System Plugins:
- **learning_engine.py**: AI learning and adaptation capabilities
- **personality_engine.py**: Personality management and emotional systems
- **personalization_engine.py**: User personalization and adaptation
- **tool_manager.py**: Tool coordination and management

## Usage

### Basic Framework Usage

```python
from framework.framework_tool import get_framework

# Get the main framework instance
framework = get_framework()

# Access a plugin
image_gen = framework.get_plugin("enhanced_image_generator")
voice_gen = framework.get_plugin("enhanced_voice_generator")

# Use plugins
image_result = image_gen.generate_character_portrait("Luna", "Mysterious AI", "romantic")
voice_result = voice_gen.generate_character_voice("Hello!", "Luna", "romantic")
```

### Plugin Development

To create a new plugin:

```python
class MyPlugin:
    def __init__(self):
        self.name = "my_plugin"
        self.version = "1.0.0"
    
    def initialize(self, framework):
        """Initialize the plugin with framework access"""
        self.framework = framework
        return True
    
    def my_method(self, *args, **kwargs):
        """Your plugin functionality"""
        return {"success": True, "result": "Hello from my plugin!"}
```

### Configuration

The framework uses a centralized configuration system:

```python
# Access configuration
config = framework.get_config()

# Get specific settings
bot_token = config.get("discord_token")
model_path = config.get("model_path")
```

## Plugin Architecture

### Plugin Interface

All plugins should implement:

1. **Initialization**: `initialize(framework)` method
2. **Configuration**: Access to framework configuration
3. **Error Handling**: Proper error handling and logging
4. **Documentation**: Clear method documentation

### Plugin Communication

Plugins can communicate through the framework:

```python
# Get another plugin
other_plugin = self.framework.get_plugin("enhanced_image_generator")

# Use other plugin's functionality
result = other_plugin.generate_image("A beautiful sunset")
```

### Plugin Lifecycle

1. **Loading**: Plugin is loaded and initialized
2. **Registration**: Plugin registers with framework
3. **Execution**: Plugin methods are called as needed
4. **Cleanup**: Plugin is properly cleaned up when unloaded

## Enhanced Systems Integration

The framework now includes enhanced multimodal systems:

### Enhanced Image Generation
- Multiple models (Stable Diffusion, APIs)
- Style presets and customization
- GPU acceleration support
- High-resolution output

### Enhanced Voice Generation
- Multiple TTS engines (pyttsx3, gTTS, APIs)
- Voice presets and character voices
- Audio playback integration
- Personality-based voice generation

### Enhanced Video Generation
- Multiple APIs (Runway ML, Replicate, Stability AI)
- Video creation from images
- Audio-video combination
- Professional video editing

### Enhanced Audio Processing
- Sound generation with presets
- Audio effects and analysis
- Ambient sound generation
- Audio mixing capabilities

### Multimodal Orchestration
- Unified coordination of all media types
- Complete character and story packages
- System health monitoring
- Seamless workflow integration

## Error Handling

The framework provides comprehensive error handling:

```python
try:
    result = plugin.some_method()
    if result.get("success"):
        # Handle success
        pass
    else:
        # Handle error
        logger.error(f"Plugin error: {result.get('error')}")
except Exception as e:
    logger.error(f"Framework error: {str(e)}")
```

## Logging

The framework uses structured logging:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Plugin initialized successfully")
logger.warning("Configuration missing, using defaults")
logger.error("Failed to generate content")
```

## Testing

Test the framework and plugins:

```bash
# Test the main framework
python -c "from framework.framework_tool import get_framework; f = get_framework(); print('Framework loaded successfully')"

# Test enhanced systems
python test_enhanced_multimodal_systems.py

# Test psychological systems
python test_enhanced_psychological_emotions.py
```

## Dependencies

The framework requires:

```bash
# Core dependencies
discord.py>=2.3.0
python-dotenv>=1.0.0
requests>=2.31.0

# Enhanced multimodal systems
torch>=2.0.0
diffusers>=0.34.0
transformers>=4.51.0
pyttsx3>=2.98
gTTS>=2.5.0
moviepy>=2.2.0
librosa>=0.10.0
pydub>=0.25.0
```

## Future Enhancements

Planned improvements:

1. **Plugin Marketplace**: Easy plugin distribution and installation
2. **Hot Reloading**: Plugin updates without restart
3. **Plugin Dependencies**: Automatic dependency management
4. **Plugin Versioning**: Version control and compatibility
5. **Plugin Testing**: Automated plugin testing framework
6. **Plugin Documentation**: Auto-generated plugin documentation

## Contributing

To contribute to the framework:

1. Follow the plugin interface guidelines
2. Include comprehensive error handling
3. Add proper logging and documentation
4. Test thoroughly before submission
5. Follow the existing code style and patterns

## Support

For framework support:

1. Check the logs for error messages
2. Verify plugin initialization
3. Test individual plugins
4. Check configuration settings
5. Review the documentation

The framework is the backbone of the entire AI writing companion system, providing the foundation for all enhanced capabilities and future expansions. 