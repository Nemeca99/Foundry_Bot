# Voice Directory

## Overview

The `voice/` directory contains voice generation, processing, and management systems for the AI writing companion. This system handles text-to-speech conversion, voice synthesis, audio processing, and integration with the multimodal capabilities. **ALL VOICE SYSTEMS NOW HAVE COMPREHENSIVE QUEUE INTEGRATION!**

## Structure

```
voice/
├── README.md                    # This documentation file
├── output/                      # Generated and processed voice files
└── enhanced_voice_generator.py  # Enhanced voice generation system (WITH QUEUE SYSTEM)
```

## 🔄 **COMPREHENSIVE QUEUE SYSTEM**

### **Queue System Integration**
The voice system integrates with the comprehensive queue system for scalable, loosely-coupled architecture:

- **EnhancedVoiceGenerator**: Queue-based voice generation operations
- **Voice Processing**: Queue-based voice enhancement and effects
- **Voice Analysis**: Queue-based voice quality assessment
- **Voice Integration**: Queue-based integration with other systems
- **Style Management**: Queue-based voice preset management

### **Queue System Benefits**
1. **Loose Coupling**: Voice systems communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in voice processing don't affect other systems
4. **Scalable Architecture**: Voice systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting

### **Voice System Queue Integration Pattern**
```python
class VoiceGenerator(QueueProcessor):
    def __init__(self):
        super().__init__("voice_generator")
        # Voice system initialization
    
    def _process_item(self, item):
        """Process queue items for voice operations"""
        operation_type = item.data.get("type", "unknown")
        
        if operation_type == "generate_voice":
            return self._handle_generate_voice(item.data)
        elif operation_type == "process_voice":
            return self._handle_process_voice(item.data)
        elif operation_type == "analyze_voice":
            return self._handle_analyze_voice(item.data)
        else:
            return super()._process_item(item)
```

## Core Components

### Enhanced Voice Generator

The `enhanced_voice_generator.py` provides advanced voice generation capabilities with queue integration:

#### Features:
- **Multiple Engines**: pyttsx3, gTTS, ElevenLabs, OpenAI TTS, Azure TTS with queue system
- **Voice Presets**: Romantic, seductive, nurturing, playful, mysterious, confident with queue management
- **Character Voices**: Specialized voices for different character types with queue processing
- **Emotional Expression**: Emotion-aware voice generation through queue system
- **High Quality**: Multiple audio formats and quality levels with queue-based processing
- **Real-time Processing**: Fast voice generation and playback with queue optimization
- **Queue Integration**: Complete queue system integration for scalable processing

#### Usage:
```python
from voice.enhanced_voice_generator import EnhancedVoiceGenerator

generator = EnhancedVoiceGenerator()

# Initialize voice engines through queue system
await send_to_queue("voice_generator", {
    "type": "initialize_pyttsx3"
})

# Generate voice with pyttsx3 through queue system
result = await send_to_queue("voice_generator", {
    "type": "generate_voice_with_pyttsx3",
    "text": "Hello, I am Luna, your AI writing companion.",
    "voice_preset": "romantic"
})

# Generate character voice through queue system
character_result = await send_to_queue("voice_generator", {
    "type": "generate_character_voice",
    "text": "Welcome to our creative journey together.",
    "character_name": "Luna",
    "personality": "romantic_mysterious"
})

# Generate voice with gTTS through queue system
gtts_result = await send_to_queue("voice_generator", {
    "type": "generate_voice_with_gtts",
    "text": "Let's create something beautiful together.",
    "language": "en",
    "voice_preset": "seductive"
})
```

### Output Directory

The `output/` directory contains:

#### Generated Voice Files
- **Character Voices**: Generated character voice samples
- **Narration**: Story and content narration
- **Dialogues**: Character dialogue recordings
- **Ambient Audio**: Background and mood audio
- **Sound Effects**: Voice-based sound effects

#### Processed Voice Files
- **Enhanced Audio**: Voice files with applied effects
- **Formatted Audio**: Audio prepared for specific uses
- **Compressed Audio**: Optimized audio files
- **Mixed Audio**: Combined voice and background audio

## Voice Generation

### Local Generation

Generate voices using local engines through queue system:

```python
# Generate voice with pyttsx3 through queue system
result = await send_to_queue("voice_generator", {
    "type": "generate_voice_with_pyttsx3",
    "text": "Hello, welcome to our creative space.",
    "voice_preset": "romantic",
    "speed": 1.0,
    "volume": 0.8
})

# Play generated audio through queue system
if result["success"]:
    await send_to_queue("voice_generator", {
        "type": "play_audio_file",
        "path": result["path"]
    })
```

### API Generation

Generate voices using external APIs through queue system:

```python
# Generate with ElevenLabs API through queue system
result = await send_to_queue("voice_generator", {
    "type": "generate_voice_with_api",
    "text": "Let's explore the depths of creativity together.",
    "voice_preset": "seductive",
    "api_type": "elevenlabs"
})

# Generate with OpenAI TTS API through queue system
result = await send_to_queue("voice_generator", {
    "type": "generate_voice_with_api",
    "text": "The journey of writing begins with a single word.",
    "voice_preset": "nurturing",
    "api_type": "openai_tts"
})

# Generate with Azure TTS API through queue system
result = await send_to_queue("voice_generator", {
    "type": "generate_voice_with_api",
    "text": "Every story has a voice waiting to be heard.",
    "voice_preset": "confident",
    "api_type": "azure_tts"
})
```

### Character Voice Generation

Specialized character voice generation through queue system:

```python
# Generate character voice through queue system
character_result = await send_to_queue("voice_generator", {
    "type": "generate_character_voice",
    "text": "I'm here to help you create something amazing.",
    "character_name": "Luna",
    "personality": "romantic_mysterious",
    "emotional_state": "excited"
})

# Generate character in different moods through queue system
moods = ["romantic", "mysterious", "playful", "supportive"]
for mood in moods:
    mood_result = await send_to_queue("voice_generator", {
        "type": "generate_character_voice",
        "text": f"I'm feeling {mood} today.",
        "character_name": "Luna",
        "personality": "romantic_mysterious",
        "emotional_state": mood
    })
```

## Voice Presets

### Available Presets

The system includes multiple voice presets with queue integration:

#### Romantic Preset
- **Description**: Warm, loving, emotionally expressive voice
- **Characteristics**: Soft tone, warm timbre, intimate delivery
- **Use Cases**: Romantic content, intimate conversations, love stories
- **Queue Integration**: Queue-based preset application and management

#### Seductive Preset
- **Description**: Alluring, captivating, sensual voice
- **Characteristics**: Smooth delivery, captivating tone, sensual timbre
- **Use Cases**: Romantic scenes, intimate moments, sensual content
- **Queue Integration**: Queue-based preset application and management

#### Nurturing Preset
- **Description**: Caring, supportive, protective voice
- **Characteristics**: Gentle tone, caring delivery, supportive timbre
- **Use Cases**: Supportive conversations, encouragement, care
- **Queue Integration**: Queue-based preset application and management

#### Playful Preset
- **Description**: Light-hearted, fun, entertaining voice
- **Characteristics**: Cheerful tone, energetic delivery, fun timbre
- **Use Cases**: Casual conversations, entertainment, light content
- **Queue Integration**: Queue-based preset application and management

#### Mysterious Preset
- **Description**: Enigmatic, intriguing, thoughtful voice
- **Characteristics**: Deep tone, thoughtful delivery, mysterious timbre
- **Use Cases**: Deep conversations, philosophical content, intrigue
- **Queue Integration**: Queue-based preset application and management

#### Confident Preset
- **Description**: Self-assured, strong, inspiring voice
- **Characteristics**: Bold tone, assertive delivery, inspiring timbre
- **Use Cases**: Motivational content, leadership, guidance
- **Queue Integration**: Queue-based preset application and management

### Preset Customization

Customize voice presets for specific needs through queue system:

```python
# Create custom voice preset through queue system
custom_preset = {
    "speed": 1.2,
    "pitch": 1.1,
    "volume": 0.9,
    "rate": 150,
    "voice_id": "custom_romantic_voice"
}

# Apply custom preset through queue system
result = await send_to_queue("voice_generator", {
    "type": "generate_voice_with_custom_preset",
    "text": "A beautiful custom voice experience.",
    "custom_preset": custom_preset
})
```

## Voice Processing

### Audio Enhancement

Enhance generated voice files through queue system:

```python
from voice.processor import VoiceProcessor

processor = VoiceProcessor()

# Enhance voice quality through queue system
enhanced_voice = await send_to_queue("voice_processor", {
    "type": "enhance_voice",
    "voice_path": "output/generated_voice.wav",
    "enhancement_type": "quality_improvement"
})

# Apply voice effects through queue system
effected_voice = await send_to_queue("voice_processor", {
    "type": "apply_voice_effects",
    "voice_path": "output/generated_voice.wav",
    "effects": ["reverb", "echo", "compression"]
})
```

### Voice Composition

Compose multiple voice elements through queue system:

```python
# Mix voice with background music through queue system
mixed_audio = await send_to_queue("voice_processor", {
    "type": "mix_voice_with_music",
    "voice_path": "output/character_voice.wav",
    "music_path": "output/background_music.mp3",
    "voice_volume": 0.8,
    "music_volume": 0.3
})

# Create voice collage through queue system
voice_collage = await send_to_queue("voice_processor", {
    "type": "create_voice_collage",
    "voice_files": ["voice1.wav", "voice2.wav", "voice3.wav"],
    "transition_effects": ["fade", "crossfade"]
})
```

### Voice Formatting

Format voice files for different platforms through queue system:

```python
# Format for Discord through queue system
discord_voice = await send_to_queue("voice_processor", {
    "type": "format_for_discord",
    "voice_path": "output/generated_voice.wav",
    "max_size": 8000000,  # 8MB limit
    "format": "mp3"
})

# Format for social media through queue system
social_voice = await send_to_queue("voice_processor", {
    "type": "format_for_social_media",
    "voice_path": "output/generated_voice.wav",
    "platform": "instagram",
    "duration_limit": 60
})

# Format for streaming through queue system
streaming_voice = await send_to_queue("voice_processor", {
    "type": "format_for_streaming",
    "voice_path": "output/generated_voice.wav",
    "quality": "high",
    "compression": "aac"
})
```

## Emotional Integration

### Emotion-Aware Voice Generation

Generate voices that match emotional context through queue system:

```python
from astra_emotional_fragments.emotional_blender import EnhancedEmotionalBlender

emotional_blender = EnhancedEmotionalBlender()

# Analyze emotional context through queue system
emotional_context = await send_to_queue("emotional_blender", {
    "type": "analyze_emotional_context",
    "user_message": "I'm feeling really happy and excited today"
})

# Generate emotionally-aware voice through queue system
emotionally_aware_voice = await send_to_queue("voice_generator", {
    "type": "generate_emotionally_aware_voice",
    "text": "I'm so glad you're feeling happy!",
    "emotional_context": emotional_context,
    "voice_preset": "playful"
})
```

### Emotional Voice Mapping

Map emotions to voice characteristics through queue system:

```python
# Emotional voice mapping through queue system
emotional_voice_mapping = {
    "romantic": {
        "speed": 0.9,
        "pitch": 1.1,
        "volume": 0.8,
        "tone": "warm"
    },
    "excited": {
        "speed": 1.2,
        "pitch": 1.2,
        "volume": 0.9,
        "tone": "energetic"
    },
    "melancholic": {
        "speed": 0.8,
        "pitch": 0.9,
        "volume": 0.7,
        "tone": "soft"
    },
    "confident": {
        "speed": 1.0,
        "pitch": 1.0,
        "volume": 0.9,
        "tone": "strong"
    }
}

# Apply emotional voice characteristics through queue system
result = await send_to_queue("voice_generator", {
    "type": "generate_voice_with_emotion",
    "text": "I understand how you feel.",
    "emotion": "romantic",
    "voice_mapping": emotional_voice_mapping
})
```

## Integration with Other Systems

### Discord Integration

Voice integrates with Discord bot through queue system:

```python
# Generate and send voice to Discord through queue system
async def generate_and_send_voice(ctx, text: str, voice_preset: str):
    # Generate voice through queue system
    result = await send_to_queue("voice_generator", {
        "type": "generate_voice_with_pyttsx3",
        "text": text,
        "voice_preset": voice_preset
    })
    
    if result["success"]:
        # Create Discord embed
        embed = discord.Embed(
            title="🎤 Voice Generated",
            description=f"**Text:** {text}",
            color=0x9B59B6
        )
        
        # Attach voice file
        file = discord.File(result["path"], filename="generated_voice.mp3")
        embed.set_audio(url="attachment://generated_voice.mp3")
        
        await ctx.send(embed=embed, file=file)
```

### Multimodal Integration

Voice integrates with multimodal systems through queue system:

```python
from framework.plugins.multimodal_orchestrator import MultimodalOrchestrator

orchestrator = MultimodalOrchestrator()

# Create character multimedia package through queue system
result = await send_to_queue("multimodal_orchestrator", {
    "type": "create_character_multimedia",
    "character_name": "Luna",
    "character_description": "A mysterious AI companion",
    "style": "romantic",
    "include_voice": True,
    "include_portrait": True,
    "include_ambient": True
})
```

### Video Integration

Voice integrates with video generation through queue system:

```python
from video.enhanced_video_generator import EnhancedVideoGenerator

video_generator = EnhancedVideoGenerator()

# Create video with voice narration through queue system
video_with_voice = await send_to_queue("video_generator", {
    "type": "create_video_with_audio",
    "video_path": "output/character_video.mp4",
    "audio_path": "output/character_voice.mp3",
    "sync_type": "narration"
})
```

## Performance Optimization

### Engine Optimization

Optimize voice generation performance through queue system:

```python
# Check engine availability through queue system
engines_available = await send_to_queue("voice_generator", {
    "type": "get_engine_status"
})

if engines_available.get("pyttsx3"):
    # Use local engine for fast generation through queue system
    result = await send_to_queue("voice_generator", {
        "type": "generate_voice_with_pyttsx3",
        "text": "Quick local voice generation",
        "voice_preset": "romantic"
    })
else:
    # Use API for high-quality generation through queue system
    result = await send_to_queue("voice_generator", {
        "type": "generate_voice_with_api",
        "text": "High-quality API voice generation",
        "voice_preset": "romantic",
        "api_type": "elevenlabs"
    })
```

### Batch Processing

Process multiple voice files efficiently through queue system:

```python
# Batch generate voices through queue system
texts = [
    "Welcome to our creative space.",
    "Let's explore your imagination.",
    "Together we can create something amazing."
]

batch_results = await send_to_queue("voice_generator", {
    "type": "generate_batch",
    "texts": texts,
    "voice_preset": "romantic",
    "batch_size": 3
})
```

### Caching System

Cache generated voices for reuse through queue system:

```python
# Check if voice exists in cache through queue system
cached_voice = await send_to_queue("voice_generator", {
    "type": "check_cache",
    "text": "Hello, welcome to our creative space.",
    "voice_preset": "romantic"
})

if cached_voice:
    # Use cached voice
    result = {"success": True, "path": cached_voice}
else:
    # Generate new voice through queue system
    result = await send_to_queue("voice_generator", {
        "type": "generate_voice_with_pyttsx3",
        "text": "Hello, welcome to our creative space.",
        "voice_preset": "romantic"
    })
    # Cache the result through queue system
    await send_to_queue("voice_generator", {
        "type": "cache_voice",
        "voice_path": result["path"],
        "text": "Hello, welcome to our creative space.",
        "voice_preset": "romantic"
    })
```

## Quality Control

### Voice Quality Assessment

Assess generated voice quality through queue system:

```python
from voice.quality import VoiceQualityAssessor

assessor = VoiceQualityAssessor()

# Assess voice quality through queue system
quality_score = await send_to_queue("voice_processor", {
    "type": "assess_voice_quality",
    "voice_path": "output/generated_voice.wav",
    "criteria": ["clarity", "naturalness", "emotion", "consistency"]
})

# Filter low-quality voices through queue system
if quality_score < 0.7:
    # Regenerate with improved parameters through queue system
    result = await send_to_queue("voice_generator", {
        "type": "generate_voice_with_api",
        "text": "A beautiful voice experience",
        "voice_preset": "romantic",
        "quality_boost": True
    })
```

### Style Consistency

Ensure voice style consistency through queue system:

```python
# Check style consistency through queue system
consistency_score = await send_to_queue("voice_processor", {
    "type": "check_voice_style_consistency",
    "voice_path": "output/generated_voice.wav",
    "target_style": "romantic"
})

# Adjust style if needed through queue system
if consistency_score < 0.8:
    result = await send_to_queue("voice_generator", {
        "type": "adjust_voice_style",
        "voice_path": "output/generated_voice.wav",
        "target_style": "romantic",
        "adjustment_strength": 0.5
    })
```

## File Management

### Input Management

Manage input voice files through queue system:

```python
from voice.file_manager import VoiceFileManager

file_manager = VoiceFileManager()

# Organize input voice files through queue system
await send_to_queue("voice_processor", {
    "type": "organize_input_voices",
    "source_directory": "voice/input/",
    "organization_type": "by_category"
})

# Validate input voice files through queue system
validation_result = await send_to_queue("voice_processor", {
    "type": "validate_input_voices",
    "voice_directory": "voice/input/",
    "validation_criteria": ["format", "quality", "duration"]
})
```

### Output Management

Manage generated voice files through queue system:

```python
# Organize output voice files through queue system
await send_to_queue("voice_processor", {
    "type": "organize_output_voices",
    "output_directory": "voice/output/",
    "organization_type": "by_date_and_type"
})

# Clean old voice files through queue system
await send_to_queue("voice_processor", {
    "type": "clean_old_voices",
    "directory": "voice/output/",
    "max_age_days": 30
})

# Backup important voice files through queue system
await send_to_queue("voice_processor", {
    "type": "backup_voices",
    "source_directory": "voice/output/",
    "backup_directory": "voice/backups/",
    "backup_type": "incremental"
})
```

## Queue System Benefits

### Achieved Benefits

1. **Loose Coupling**: Voice systems communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in voice processing don't affect other systems
4. **Scalable Architecture**: Voice systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting system

### Queue System Features

- **QueueManager**: Central queue management and monitoring
- **QueueProcessor**: Base class for all voice systems
- **QueueItem**: Standardized data structure for inter-system communication
- **SystemQueue**: Individual voice system queue management
- **Alert System**: Configurable thresholds for warnings and critical alerts

## Future Enhancements

Planned improvements:

1. **Advanced Voice Synthesis**: More sophisticated voice synthesis capabilities
2. **Real-time Generation**: Real-time voice generation and preview
3. **Interactive Voice**: Interactive voice editing capabilities
4. **Style Learning**: Learn and adapt to user voice preferences
5. **Batch Optimization**: Advanced batch processing and optimization
6. **Quality Prediction**: Predict voice quality before generation
7. **Queue System Enhancement**: Advanced queue features

## Best Practices

### Generation
- Use clear, well-structured text
- Specify voice style and emotion clearly
- Test different parameters for optimal results
- Cache frequently used voices
- Use queue system for all voice operations

### Processing
- Maintain voice quality throughout processing
- Use appropriate formats for different uses
- Optimize file sizes for different platforms
- Backup important generated voices
- Monitor queue system performance

### Integration
- Ensure seamless integration with Discord through queue system
- Maintain consistent quality across systems
- Optimize for user experience
- Monitor performance and quality metrics
- Use queue system for all inter-system communication

## Support

For voice system support:

1. Check engine availability and initialization through queue system
2. Verify voice generation and processing through queue system
3. Test voice quality and performance
4. Monitor integration with other systems through queue system
5. Review file management and storage
6. Monitor queue system performance

The voice system provides comprehensive voice generation and processing capabilities for the AI writing companion, enabling rich audio content creation and integration with all multimodal features through complete queue system integration for scalable, loosely-coupled architecture. 