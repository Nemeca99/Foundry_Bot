# Discord Directory

## Overview

The `discord/` directory contains the Discord bot interface and all Discord-related functionality for the AI writing companion. This system provides the primary user interface through Discord commands, enabling users to interact with all AI capabilities through a familiar chat interface.

## Structure

```
discord/
├── README.md                    # This documentation file
├── authoring_bot.py             # Main Discord bot interface
├── enhanced_multimodal_commands.py # Enhanced multimodal Discord commands
└── core/                        # Discord bot core components
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

The bot processes commands through a structured system:

```python
# Command registration
@bot.command(name="write-chapter")
async def write_chapter(ctx, project_name: str, chapter_title: str, *, requirements: str):
    """Write a chapter for a project"""
    # Command implementation
    pass

# Natural language processing
@bot.event
async def on_message(ctx):
    """Handle natural language messages"""
    if ctx.author.bot:
        return
    
    # Process @mentions for natural conversation
    if bot.user.mentioned_in(ctx):
        response = await handle_natural_language(ctx, ctx.content)
        await ctx.send(response)
```

### Error Handling

Comprehensive error handling for all commands:

```python
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Invalid argument: {error}")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
```

### Message Processing

Handles long messages and complex formatting:

```python
async def _send_long_message(self, ctx, message: str, prefix: str = ""):
    """Send long messages by splitting if necessary"""
    if len(message) <= 1900:
        await ctx.send(f"{prefix}{message}")
    else:
        # Split message into chunks
        chunks = self._split_message(message, 1900)
        for chunk in chunks:
            await ctx.send(f"{prefix}{chunk}")
```

## Integration with Framework

### Plugin Integration

The Discord bot integrates with all framework plugins:

```python
# Get framework instance
framework = get_framework()

# Access plugins
writing_assistant = framework.get_plugin("writing_assistant")
personality_engine = framework.get_plugin("personality_engine")
multimodal_orchestrator = framework.get_plugin("multimodal_orchestrator")

# Use plugins in commands
result = writing_assistant.generate_chapter(project_name, chapter_title, requirements)
response = personality_engine.generate_response(message, emotional_context)
multimodal_result = multimodal_orchestrator.create_character_multimedia(character_name, description)
```

### Enhanced Systems Integration

Integration with enhanced multimodal systems:

```python
# Enhanced image generation
image_generator = EnhancedImageGenerator()
result = image_generator.generate_character_portrait(character_name, description, style)

# Enhanced voice generation
voice_generator = EnhancedVoiceGenerator()
result = voice_generator.generate_character_voice(text, character_name, personality)

# Enhanced audio processing
audio_processor = EnhancedAudioProcessor()
result = audio_processor.generate_sound_with_preset(preset_name)
```

## User Experience

### Natural Language Processing

Users can interact naturally through @mentions:

```python
# Example: User types "@Luna I'm feeling creative today"
# Bot responds with emotionally-aware, creative content
response = await handle_natural_language(ctx, message)
```

### Command Help System

Comprehensive help system for all commands:

```bash
!help                    # Show all available commands
!help write-chapter      # Show specific command help
!help enhanced-image     # Show enhanced command help
```

### Rich Embeds

Commands use Discord embeds for rich formatting:

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

User authorization and permission control:

```python
def _is_authorized(self, ctx) -> bool:
    """Check if user is authorized to use the bot"""
    # Add your authorization logic here
    return True  # For now, allow all users
```

### Command Permissions

Different permission levels for commands:

```python
# Admin commands
@commands.has_permissions(administrator=True)
async def admin_command(ctx):
    """Admin-only command"""
    pass

# User commands
@commands.has_permissions(send_messages=True)
async def user_command(ctx):
    """User command"""
    pass
```

## Performance Optimization

### Message Caching

Efficient message processing and caching:

```python
# Cache frequently used responses
response_cache = {}

async def get_cached_response(key: str) -> str:
    """Get cached response or generate new one"""
    if key in response_cache:
        return response_cache[key]
    else:
        response = await generate_response(key)
        response_cache[key] = response
        return response
```

### Rate Limiting

Prevent spam and abuse:

```python
from discord.ext import commands
import asyncio

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}

    async def check_rate_limit(self, user_id: int) -> bool:
        """Check if user is within rate limits"""
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

Comprehensive testing for Discord functionality:

```python
# Test command functionality
async def test_discord_commands():
    """Test all Discord commands"""
    # Test writing commands
    # Test AI tool commands
    # Test emotional system commands
    # Test multimodal commands
    pass

# Test enhanced commands
async def test_enhanced_commands():
    """Test enhanced multimodal commands"""
    # Test enhanced image generation
    # Test enhanced voice generation
    # Test enhanced video generation
    # Test enhanced audio processing
    pass
```

### Integration Testing

Test integration with framework systems:

```python
# Test framework integration
async def test_framework_integration():
    """Test Discord bot integration with framework"""
    framework = get_framework()
    
    # Test plugin access
    writing_assistant = framework.get_plugin("writing_assistant")
    personality_engine = framework.get_plugin("personality_engine")
    
    # Test command functionality
    result = await test_writing_commands(writing_assistant)
    personality_result = await test_personality_commands(personality_engine)
    
    return result and personality_result
```

## Configuration

### Bot Configuration

Discord bot configuration settings:

```python
# Bot configuration
bot_config = {
    "command_prefix": "!",
    "intents": discord.Intents.default(),
    "help_command": None,
    "case_insensitive": True
}

# Initialize bot
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

Required environment variables:

```bash
# Discord bot token
DISCORD_TOKEN=your_discord_bot_token

# Bot prefix (optional, defaults to "!")
BOT_PREFIX=!

# Authorization settings
AUTHORIZED_USERS=user_id1,user_id2,user_id3
```

## Deployment

### Production Deployment

Deploy the Discord bot to production:

```bash
# Start the bot
python start_bot.py

# Or run directly
python discord/authoring_bot.py
```

### Docker Deployment

Docker configuration for Discord bot:

```dockerfile
# Dockerfile for Discord bot
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "start_bot.py"]
```

## Monitoring and Logging

### Logging System

Comprehensive logging for debugging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Log command usage
logger.info(f"Command executed: {ctx.command} by {ctx.author}")
```

### Performance Monitoring

Monitor bot performance:

```python
# Performance metrics
performance_metrics = {
    "commands_executed": 0,
    "response_times": [],
    "error_count": 0,
    "user_interactions": {}
}

# Track command execution
async def track_command_execution(ctx, command_name: str, response_time: float):
    """Track command execution metrics"""
    performance_metrics["commands_executed"] += 1
    performance_metrics["response_times"].append(response_time)
    
    user_id = str(ctx.author.id)
    if user_id not in performance_metrics["user_interactions"]:
        performance_metrics["user_interactions"][user_id] = 0
    performance_metrics["user_interactions"][user_id] += 1
```

## Future Enhancements

Planned improvements:

1. **Advanced Natural Language**: More sophisticated NLP processing
2. **Voice Commands**: Voice command support
3. **Slash Commands**: Discord slash command integration
4. **Advanced Permissions**: Role-based permission system
5. **Analytics Dashboard**: User interaction analytics
6. **Multi-language Support**: Internationalization support

## Best Practices

### Command Development
- Use clear, descriptive command names
- Provide comprehensive help text
- Handle errors gracefully
- Validate user input thoroughly

### User Experience
- Provide immediate feedback for long operations
- Use rich embeds for better formatting
- Implement rate limiting to prevent abuse
- Maintain consistent command structure

### Performance
- Cache frequently used responses
- Optimize database queries
- Monitor response times
- Implement proper error handling

## Support

For Discord bot support:

1. Check bot permissions and token
2. Verify command syntax and usage
3. Review error logs and messages
4. Test command functionality
5. Check framework integration

The Discord bot system provides the primary user interface for the AI writing companion, enabling users to access all features through an intuitive chat interface with comprehensive command support and natural language processing. 