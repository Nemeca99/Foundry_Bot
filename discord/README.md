# Discord Directory

## Overview

The `discord/` directory contains the Discord bot interface and all Discord-related functionality for the AI writing companion. This system provides the primary user interface through Discord commands, enabling users to interact with all AI capabilities through a familiar chat interface. **ALL DISCORD BOTS NOW HAVE COMPREHENSIVE QUEUE INTEGRATION!**

## Structure

```
discord/
├── README.md                    # This documentation file
├── authoring_bot.py             # Main Discord bot interface (WITH QUEUE SYSTEM)
├── character_system_bot.py      # Character system bot (WITH QUEUE SYSTEM)
├── enhanced_luna_bot.py         # Enhanced Luna bot (WITH QUEUE SYSTEM)
├── writing_assistant_bot.py     # Writing assistant bot (WITH QUEUE SYSTEM)
├── enhanced_multimodal_commands.py # Enhanced multimodal Discord commands
└── core/                        # Discord bot core components
```

## 🔄 **COMPREHENSIVE QUEUE SYSTEM**

### **Queue System Integration**
All Discord bots inherit from `QueueProcessor` and implement queue-based communication:

- **AuthoringBot**: Queue-based authoring operations
- **CharacterSystemBot**: Queue-based character system operations
- **EnhancedLunaBot**: Queue-based emotional system operations
- **WritingAssistantBot**: Queue-based writing assistance operations

### **Queue System Benefits**
1. **Loose Coupling**: Discord bots communicate without direct dependencies
2. **Bottleneck Detection**: Real-time monitoring of bot performance
3. **Error Isolation**: Failures in one bot don't affect others
4. **Scalable Architecture**: Bots can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting

### **Discord Bot Queue Integration Pattern**
```python
class DiscordBot(commands.Bot, QueueProcessor):
    def __init__(self):
        commands.Bot.__init__(self, ...)
        QueueProcessor.__init__(self, "discord_bot_name")
        # Bot initialization
    
    def _process_item(self, item):
        """Process queue items for Discord operations"""
        operation_type = item.data.get("type", "unknown")
        
        if operation_type == "discord_operation":
            return self._handle_discord_operation(item.data)
        else:
            return super()._process_item(item)
```

## Core Components

### authoring_bot.py

The main Discord bot interface that provides:

#### Features:
- **Command System**: Comprehensive Discord command system
- **Natural Language Processing**: @mention functionality for natural conversation
- **Error Handling**: Robust error handling and user feedback
- **Permission Management**: User authorization and permission control
- **Message Processing**: Long message splitting and formatting
- **Plugin Integration**: Integration with all framework plugins
- **Queue Integration**: Queue-based communication with other systems

#### Key Commands:

##### Writing Assistant Commands
```bash
!create-project "Name" "Genre" "Audience" word_count
!write-chapter <project> <title> <requirements>
!develop-character <project> <character> <requirements>
!generate-plot <project> <requirements>
!autocomplete <project> <text>
!expand <project> <scene>
!describe <project> <element> <context>
!rewrite <project> <text>
!dialogue <project> <characters> <situation>
!brainstorm <element> <genre> <context>
```

##### AI Tools Commands
```bash
!tools <your request>
!personality show
!personality-test <type>
!learning-summary
!modify-message <type> <message>
!reward-learning <activity> <level>
!punish-learning <opportunity> <severity>
```

##### Emotional System Commands
```bash
!test-emotion <message>
!blend-emotions <primary> [secondary] [tertiary]
!test-prompt-injection <message>
```

##### Multimodal Commands
```bash
!generate-multimodal <prompt> [media_types] [style]
!create-character-media <name> <description>
!create-story-media <title> <genre> <description>
!generate-image <prompt> [style]
!generate-voice <text> [style]
!generate-video <prompt> [duration]
!generate-sound <prompt> [style]
```

##### Enhanced Multimodal Commands
```bash
!enhanced-image <prompt> [style] [model]
!enhanced-voice <text> [preset] [engine]
!enhanced-video <prompt> [style] [api]
!enhanced-audio <type> [preset]
!enhanced-character <name> <description>
!enhanced-story <title> <genre> <description>
!system-status
!available-styles [system]
```

### character_system_bot.py

The character system Discord bot that provides:

#### Features:
- **Character Embodiment**: Character creation and management
- **Character Memory**: Character-specific memory and knowledge
- **Character Interaction**: Character-to-character dialogue
- **Character Development**: Character growth and evolution
- **Queue Integration**: Queue-based communication with character systems

#### Key Commands:
```bash
!create-character <name> <description>
!embody-character <character_name>
!character-memory <character> <memory>
!character-interaction <character1> <character2> <situation>
!character-development <character> <development_type>
!character-status <character>
```

### enhanced_luna_bot.py

The enhanced Luna Discord bot that provides:

#### Features:
- **Emotional System**: Sophisticated emotional processing
- **Global Weight Calculation**: Comprehensive emotional analysis
- **Dual-Release Mechanism**: Natural emotional cycles
- **Real-Time Adaptation**: Emotional state changes with context
- **Queue Integration**: Queue-based communication with emotional systems

#### Key Commands:
```bash
!luna <message>
!weights <message>
!status
!history
!release
!reset
!build <emotion>
```

### writing_assistant_bot.py

The writing assistant Discord bot that provides:

#### Features:
- **Writing Assistance**: Comprehensive writing help
- **Project Management**: Writing project organization
- **Content Generation**: Automated content creation
- **Writing Analysis**: Content analysis and improvement
- **Queue Integration**: Queue-based communication with writing systems

#### Key Commands:
```bash
!writing-help <topic>
!create-writing-project <name> <genre>
!generate-content <project> <type> <requirements>
!analyze-writing <text>
!improve-writing <text> <aspect>
!writing-status <project>
```

### enhanced_multimodal_commands.py

Enhanced Discord commands for advanced multimodal functionality:

#### Features:
- **Enhanced Image Generation**: Multiple models and styles
- **Enhanced Voice Generation**: Multiple TTS engines
- **Enhanced Video Generation**: Multiple APIs and styles
- **Enhanced Audio Processing**: Effects and analysis
- **Character Multimedia**: Complete character packages
- **Story Multimedia**: Complete story packages
- **System Monitoring**: Status and capability reporting

#### Usage Examples:
```bash
# Enhanced image generation
!enhanced-image "A romantic sunset" romantic local
!enhanced-image "Fantasy castle" fantasy api

# Enhanced voice generation
!enhanced-voice "Hello, I am Luna" romantic pyttsx3
!enhanced-voice "Welcome to our story" seductive gtts

# Enhanced video generation
!enhanced-video "A romantic scene" romantic runway_ml
!enhanced-video "Fantasy castle" fantasy replicate

# Enhanced audio processing
!enhanced-audio romantic
!enhanced-audio ambient nature

# Character and story packages
!enhanced-character Luna "A mysterious AI companion"
!enhanced-story "The Enchanted Garden" fantasy "A magical story"

# System monitoring
!system-status
!available-styles all
```

## Discord Bot Architecture

### Command Processing

The bot processes commands through a structured system with queue integration:

```python
# Command registration with queue integration
@bot.command(name="write-chapter")
async def write_chapter(ctx, project_name: str, chapter_title: str, *, requirements: str):
    """Write a chapter for a project"""
    # Send request through queue system
    result = await send_to_queue("writing_assistant", {
        "type": "write_chapter",
        "project": project_name,
        "title": chapter_title,
        "requirements": requirements
    })
    await ctx.send(result)

# Natural language processing with queue integration
@bot.event
async def on_message(ctx):
    """Handle natural language messages"""
    if ctx.author.bot:
        return
    
    # Process @mentions for natural conversation through queue system
    if bot.user.mentioned_in(ctx):
        response = await handle_natural_language(ctx, ctx.content)
        await ctx.send(response)
```

### Error Handling

Comprehensive error handling for all commands with queue integration:

```python
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors with queue integration"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Invalid argument: {error}")
    else:
        # Log error through queue system
        await log_error_to_queue("discord_bot", str(error))
        await ctx.send(f"❌ An error occurred: {str(error)}")
```

### Message Processing

Handles long messages and complex formatting with queue integration:

```python
async def _send_long_message(self, ctx, message: str, prefix: str = ""):
    """Send long messages by splitting if necessary with queue integration"""
    if len(message) <= 1900:
        await ctx.send(f"{prefix}{message}")
    else:
        # Split message into chunks through queue system
        chunks = await process_message_splitting(message, 1900)
        for chunk in chunks:
            await ctx.send(f"{prefix}{chunk}")
```

## Integration with Framework

### Plugin Integration

The Discord bot integrates with all framework plugins through queue system:

```python
# Get framework instance through queue system
framework = get_framework()

# Access plugins through queue system
writing_assistant = framework.get_plugin("writing_assistant")
personality_engine = framework.get_plugin("personality_engine")
multimodal_orchestrator = framework.get_plugin("multimodal_orchestrator")

# Use plugins in commands through queue system
result = await send_to_queue("writing_assistant", {
    "type": "generate_chapter",
    "project_name": project_name,
    "chapter_title": chapter_title,
    "requirements": requirements
})

response = await send_to_queue("personality_engine", {
    "type": "generate_response",
    "message": message,
    "emotional_context": emotional_context
})

multimodal_result = await send_to_queue("multimodal_orchestrator", {
    "type": "create_character_multimedia",
    "character_name": character_name,
    "description": description
})
```

### Enhanced Systems Integration

Integration with enhanced multimodal systems through queue system:

```python
# Enhanced image generation through queue system
result = await send_to_queue("image_generator", {
    "type": "generate_character_portrait",
    "character_name": character_name,
    "description": description,
    "style": style
})

# Enhanced voice generation through queue system
result = await send_to_queue("voice_generator", {
    "type": "generate_character_voice",
    "text": text,
    "character_name": character_name,
    "personality": personality
})

# Enhanced audio processing through queue system
result = await send_to_queue("audio_processor", {
    "type": "generate_sound_with_preset",
    "preset_name": preset_name
})
```

## User Experience

### Natural Language Processing

Users can interact naturally through @mentions with queue integration:

```python
# Example: User types "@Luna I'm feeling creative today"
# Bot responds with emotionally-aware, creative content through queue system
response = await handle_natural_language(ctx, message)
```

### Command Help System

Comprehensive help system for all commands with queue integration:

```bash
!help                    # Show all available commands
!help write-chapter      # Show specific command help
!help enhanced-image     # Show enhanced command help
```

### Rich Embeds

Commands use Discord embeds for rich formatting with queue integration:

```python
embed = discord.Embed(
    title="🎨 Enhanced Image Generated",
    description=f"**Prompt:** {prompt}",
    color=0x9B59B6
)
embed.add_field(name="Style", value=style, inline=True)
embed.add_field(name="Model", value=result.get("model", "unknown"), inline=True)
await ctx.send(embed=embed, file=file)
```

## Security and Permissions

### Authorization System

User authorization and permission control with queue integration:

```python
def _is_authorized(self, ctx) -> bool:
    """Check if user is authorized to use the bot through queue system"""
    # Add your authorization logic here with queue integration
    return True  # For now, allow all users
```

### Command Permissions

Different permission levels for commands with queue integration:

```python
# Admin commands with queue integration
@commands.has_permissions(administrator=True)
async def admin_command(ctx):
    """Admin-only command with queue integration"""
    pass

# User commands with queue integration
@commands.has_permissions(send_messages=True)
async def user_command(ctx):
    """User command with queue integration"""
    pass
```

## Performance Optimization

### Message Caching

Efficient message processing and caching with queue integration:

```python
# Cache frequently used responses through queue system
response_cache = {}

async def get_cached_response(key: str) -> str:
    """Get cached response or generate new one through queue system"""
    if key in response_cache:
        return response_cache[key]
    else:
        response = await generate_response_through_queue(key)
        response_cache[key] = response
        return response
```

### Rate Limiting

Prevent spam and abuse with queue integration:

```python
from discord.ext import commands
import asyncio

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}

    async def check_rate_limit(self, user_id: int) -> bool:
        """Check if user is within rate limits with queue integration"""
        current_time = time.time()
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Remove old requests
        self.requests[user_id] = [req for req in self.requests[user_id] 
                                if current_time - req < self.time_window]
        
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        self.requests[user_id].append(current_time)
        return True
```

## Testing

### Discord Bot Testing

Comprehensive testing for Discord functionality with queue integration:

```python
# Test command functionality with queue integration
async def test_discord_commands():
    """Test all Discord commands with queue integration"""
    # Test writing commands through queue system
    # Test AI tool commands through queue system
    # Test emotional system commands through queue system
    # Test multimodal commands through queue system
    pass

# Test enhanced commands with queue integration
async def test_enhanced_commands():
    """Test enhanced multimodal commands with queue integration"""
    # Test enhanced image generation through queue system
    # Test enhanced voice generation through queue system
    # Test enhanced video generation through queue system
    # Test enhanced audio processing through queue system
    pass
```

### Integration Testing

Test integration with framework systems through queue system:

```python
# Test framework integration with queue system
async def test_framework_integration():
    """Test Discord bot integration with framework through queue system"""
    framework = get_framework()
    
    # Test plugin access through queue system
    writing_assistant = framework.get_plugin("writing_assistant")
    personality_engine = framework.get_plugin("personality_engine")
    
    # Test command functionality through queue system
    result = await test_writing_commands(writing_assistant)
    personality_result = await test_personality_commands(personality_engine)
    
    return result and personality_result
```

## Configuration

### Bot Configuration

Discord bot configuration settings with queue integration:

```python
# Bot configuration with queue integration
bot_config = {
    "command_prefix": "!",
    "intents": discord.Intents.default(),
    "help_command": None,
    "case_insensitive": True
}

# Initialize bot with queue integration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=config["bot_prefix"],
    intents=intents,
    help_command=None
)
```

### Environment Variables

Required environment variables with queue integration:

```bash
# Discord bot token
DISCORD_TOKEN=your_discord_bot_token

# Bot prefix (optional, defaults to "!")
BOT_PREFIX=!

# Authorization settings
AUTHORIZED_USERS=user_id1,user_id2,user_id3

# Queue system settings
QUEUE_TIMEOUT=5
QUEUE_ALERT_THRESHOLD=100
```

## Deployment

### Production Deployment

Deploy the Discord bot to production with queue integration:

```bash
# Start the bot with queue integration
python start_bot.py

# Or run directly with queue integration
python discord/authoring_bot.py
```

### Docker Deployment

Docker configuration for Discord bot with queue integration:

```dockerfile
# Dockerfile for Discord bot with queue integration
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "start_bot.py"]
```

## Monitoring and Logging

### Logging System

Comprehensive logging for debugging with queue integration:

```python
import logging

# Configure logging with queue integration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Log command usage through queue system
logger.info(f"Command executed: {ctx.command} by {ctx.author}")
```

### Performance Monitoring

Monitor bot performance with queue integration:

```python
# Performance metrics with queue integration
performance_metrics = {
    "commands_executed": 0,
    "response_times": [],
    "error_count": 0,
    "user_interactions": {},
    "queue_performance": {}
}

# Track command execution through queue system
async def track_command_execution(ctx, command_name: str, response_time: float):
    """Track command execution metrics through queue system"""
    performance_metrics["commands_executed"] += 1
    performance_metrics["response_times"].append(response_time)
    
    user_id = str(ctx.author.id)
    if user_id not in performance_metrics["user_interactions"]:
        performance_metrics["user_interactions"][user_id] = 0
    performance_metrics["user_interactions"][user_id] += 1
```

## Queue System Benefits

### Achieved Benefits

1. **Loose Coupling**: Discord bots communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in one bot don't affect others
4. **Scalable Architecture**: Bots can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting system

### Queue System Features

- **QueueManager**: Central queue management and monitoring
- **QueueProcessor**: Base class for all Discord bots
- **QueueItem**: Standardized data structure for inter-system communication
- **SystemQueue**: Individual bot queue management
- **Alert System**: Configurable thresholds for warnings and critical alerts

## Future Enhancements

Planned improvements:

1. **Advanced Natural Language**: More sophisticated NLP processing
2. **Voice Commands**: Voice command support
3. **Slash Commands**: Discord slash command integration
4. **Advanced Permissions**: Role-based permission system
5. **Analytics Dashboard**: User interaction analytics
6. **Multi-language Support**: Internationalization support
7. **Queue System Enhancement**: Advanced queue features

## Best Practices

### Command Development
- Use clear, descriptive command names
- Provide comprehensive help text
- Handle errors gracefully
- Validate user input thoroughly
- Use queue system for all inter-system communication

### User Experience
- Provide immediate feedback for long operations
- Use rich embeds for better formatting
- Implement rate limiting to prevent abuse
- Maintain consistent command structure
- Monitor queue system performance

### Performance
- Cache frequently used responses
- Optimize database queries
- Monitor response times
- Implement proper error handling
- Monitor queue system metrics

## Support

For Discord bot support:

1. Check bot permissions and token
2. Verify command syntax and usage
3. Review error logs and messages
4. Test command functionality
5. Check framework integration
6. Monitor queue system performance

The Discord bot system provides the primary user interface for the AI writing companion, enabling users to access all features through an intuitive chat interface with comprehensive command support, natural language processing, and complete queue system integration for scalable, loosely-coupled architecture. 