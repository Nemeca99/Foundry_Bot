# Voice Directory

## Overview

The `voice/` directory contains voice generation, processing, and management systems for the AI writing companion. This system handles text-to-speech conversion, voice synthesis, audio processing, and integration with the multimodal capabilities.

## Structure

```
voice/
├── README.md                    # This documentation file
├── output/                      # Generated and processed voice files
└── enhanced_voice_generator.py  # Enhanced voice generation system
```

## Core Components

### Enhanced Voice Generator

The `enhanced_voice_generator.py` provides advanced voice generation capabilities:

#### Features:
- **Multiple Engines**: pyttsx3, gTTS, ElevenLabs, OpenAI TTS, Azure TTS
- **Voice Presets**: Romantic, seductive, nurturing, playful, mysterious, confident
- **Character Voices**: Specialized voices for different character types
- **Emotional Expression**: Emotion-aware voice generation
- **High Quality**: Multiple audio formats and quality levels
- **Real-time Processing**: Fast voice generation and playback

#### Usage:
```python
from voice.enhanced_voice_generator import EnhancedVoiceGenerator

generator = EnhancedVoiceGenerator()

# Initialize voice engines
generator.initialize_pyttsx3()

# Generate voice with pyttsx3
result = generator.generate_voice_with_pyttsx3(
    text="Hello, I am Luna, your AI writing companion.",
    voice_preset="romantic"
)

# Generate character voice
character_result = generator.generate_character_voice(
    text="Welcome to our creative journey together.",
    character_name="Luna",
    personality="romantic_mysterious"
)

# Generate voice with gTTS
gtts_result = generator.generate_voice_with_gtts(
    text="Let's create something beautiful together.",
    language="en",
    voice_preset="seductive"
)
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

Generate voices using local engines:

```python
# Generate voice with pyttsx3
result = generator.generate_voice_with_pyttsx3(
    text="Hello, welcome to our creative space.",
    voice_preset="romantic",
    speed=1.0,
    volume=0.8
)

# Play generated audio
if result["success"]:
    generator.play_audio_file(result["path"])
```

### API Generation

Generate voices using external APIs:

```python
# Generate with ElevenLabs API
result = generator.generate_voice_with_api(
    text="Let's explore the depths of creativity together.",
    voice_preset="seductive",
    api_type="elevenlabs"
)

# Generate with OpenAI TTS API
result = generator.generate_voice_with_api(
    text="The journey of writing begins with a single word.",
    voice_preset="nurturing",
    api_type="openai_tts"
)

# Generate with Azure TTS API
result = generator.generate_voice_with_api(
    text="Every story has a voice waiting to be heard.",
    voice_preset="confident",
    api_type="azure_tts"
)
```

### Character Voice Generation

Specialized character voice generation:

```python
# Generate character voice
character_result = generator.generate_character_voice(
    text="I'm here to help you create something amazing.",
    character_name="Luna",
    personality="romantic_mysterious",
    emotional_state="excited"
)

# Generate character in different moods
moods = ["romantic", "mysterious", "playful", "supportive"]
for mood in moods:
    mood_result = generator.generate_character_voice(
        text=f"I'm feeling {mood} today.",
        character_name="Luna",
        personality="romantic_mysterious",
        emotional_state=mood
    )
```

## Voice Presets

### Available Presets

The system includes multiple voice presets:

#### Romantic Preset
- **Description**: Warm, loving, emotionally expressive voice
- **Characteristics**: Soft tone, warm timbre, intimate delivery
- **Use Cases**: Romantic content, intimate conversations, love stories

#### Seductive Preset
- **Description**: Alluring, captivating, sensual voice
- **Characteristics**: Smooth delivery, captivating tone, sensual timbre
- **Use Cases**: Romantic scenes, intimate moments, sensual content

#### Nurturing Preset
- **Description**: Caring, supportive, protective voice
- **Characteristics**: Gentle tone, caring delivery, supportive timbre
- **Use Cases**: Supportive conversations, encouragement, care

#### Playful Preset
- **Description**: Light-hearted, fun, entertaining voice
- **Characteristics**: Cheerful tone, energetic delivery, fun timbre
- **Use Cases**: Casual conversations, entertainment, light content

#### Mysterious Preset
- **Description**: Enigmatic, intriguing, thoughtful voice
- **Characteristics**: Deep tone, thoughtful delivery, mysterious timbre
- **Use Cases**: Deep conversations, philosophical content, intrigue

#### Confident Preset
- **Description**: Self-assured, strong, inspiring voice
- **Characteristics**: Bold tone, assertive delivery, inspiring timbre
- **Use Cases**: Motivational content, leadership, guidance

### Preset Customization

Customize voice presets for specific needs:

```python
# Create custom voice preset
custom_preset = {
    "speed": 1.2,
    "pitch": 1.1,
    "volume": 0.9,
    "rate": 150,
    "voice_id": "custom_romantic_voice"
}

# Apply custom preset
result = generator.generate_voice_with_custom_preset(
    text="A beautiful custom voice experience.",
    custom_preset=custom_preset
)
```

## Voice Processing

### Audio Enhancement

Enhance generated voice files:

```python
from voice.processor import VoiceProcessor

processor = VoiceProcessor()

# Enhance voice quality
enhanced_voice = processor.enhance_voice(
    voice_path="output/generated_voice.wav",
    enhancement_type="quality_improvement"
)

# Apply voice effects
effected_voice = processor.apply_voice_effects(
    voice_path="output/generated_voice.wav",
    effects=["reverb", "echo", "compression"]
)
```

### Voice Composition

Compose multiple voice elements:

```python
# Mix voice with background music
mixed_audio = processor.mix_voice_with_music(
    voice_path="output/character_voice.wav",
    music_path="output/background_music.mp3",
    voice_volume=0.8,
    music_volume=0.3
)

# Create voice collage
voice_collage = processor.create_voice_collage(
    voice_files=["voice1.wav", "voice2.wav", "voice3.wav"],
    transition_effects=["fade", "crossfade"]
)
```

### Voice Formatting

Format voice files for different platforms:

```python
# Format for Discord
discord_voice = processor.format_for_discord(
    voice_path="output/generated_voice.wav",
    max_size=8000000,  # 8MB limit
    format="mp3"
)

# Format for social media
social_voice = processor.format_for_social_media(
    voice_path="output/generated_voice.wav",
    platform="instagram",
    duration_limit=60
)

# Format for streaming
streaming_voice = processor.format_for_streaming(
    voice_path="output/generated_voice.wav",
    quality="high",
    compression="aac"
)
```

## Emotional Integration

### Emotion-Aware Voice Generation

Generate voices that match emotional context:

```python
from astra_emotional_fragments.emotional_blender import EnhancedEmotionalBlender

emotional_blender = EnhancedEmotionalBlender()

# Analyze emotional context
emotional_context = emotional_blender.analyze_emotional_context(
    user_message="I'm feeling really happy and excited today"
)

# Generate emotionally-aware voice
emotionally_aware_voice = generator.generate_emotionally_aware_voice(
    text="I'm so glad you're feeling happy!",
    emotional_context=emotional_context,
    voice_preset="playful"
)
```

### Emotional Voice Mapping

Map emotions to voice characteristics:

```python
# Emotional voice mapping
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

# Apply emotional voice characteristics
result = generator.generate_voice_with_emotion(
    text="I understand how you feel.",
    emotion="romantic",
    voice_mapping=emotional_voice_mapping
)
```

## Integration with Other Systems

### Discord Integration

Voice integrates with Discord bot:

```python
# Generate and send voice to Discord
async def generate_and_send_voice(ctx, text: str, voice_preset: str):
    generator = EnhancedVoiceGenerator()
    
    # Generate voice
    result = generator.generate_voice_with_pyttsx3(text, voice_preset)
    
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

Voice integrates with multimodal systems:

```python
from framework.plugins.multimodal_orchestrator import MultimodalOrchestrator

orchestrator = MultimodalOrchestrator()

# Create character multimedia package
result = orchestrator.create_character_multimedia(
    character_name="Luna",
    character_description="A mysterious AI companion",
    style="romantic",
    include_voice=True,
    include_portrait=True,
    include_ambient=True
)
```

### Video Integration

Voice integrates with video generation:

```python
from video.enhanced_video_generator import EnhancedVideoGenerator

video_generator = EnhancedVideoGenerator()

# Create video with voice narration
video_with_voice = video_generator.create_video_with_audio(
    video_path="output/character_video.mp4",
    audio_path="output/character_voice.mp3",
    sync_type="narration"
)
```

## Performance Optimization

### Engine Optimization

Optimize voice generation performance:

```python
# Check engine availability
engines_available = generator.get_engine_status()

if engines_available.get("pyttsx3"):
    # Use local engine for fast generation
    result = generator.generate_voice_with_pyttsx3(
        text="Quick local voice generation",
        voice_preset="romantic"
    )
else:
    # Use API for high-quality generation
    result = generator.generate_voice_with_api(
        text="High-quality API voice generation",
        voice_preset="romantic",
        api_type="elevenlabs"
    )
```

### Batch Processing

Process multiple voice files efficiently:

```python
# Batch generate voices
texts = [
    "Welcome to our creative space.",
    "Let's explore your imagination.",
    "Together we can create something amazing."
]

batch_results = generator.generate_batch(
    texts=texts,
    voice_preset="romantic",
    batch_size=3
)
```

### Caching System

Cache generated voices for reuse:

```python
# Check if voice exists in cache
cached_voice = generator.check_cache(
    text="Hello, welcome to our creative space.",
    voice_preset="romantic"
)

if cached_voice:
    # Use cached voice
    result = {"success": True, "path": cached_voice}
else:
    # Generate new voice
    result = generator.generate_voice_with_pyttsx3(
        text="Hello, welcome to our creative space.",
        voice_preset="romantic"
    )
    # Cache the result
    generator.cache_voice(result["path"], text="Hello, welcome to our creative space.", voice_preset="romantic")
```

## Quality Control

### Voice Quality Assessment

Assess generated voice quality:

```python
from voice.quality import VoiceQualityAssessor

assessor = VoiceQualityAssessor()

# Assess voice quality
quality_score = assessor.assess_voice_quality(
    voice_path="output/generated_voice.wav",
    criteria=["clarity", "naturalness", "emotion", "consistency"]
)

# Filter low-quality voices
if quality_score < 0.7:
    # Regenerate with improved parameters
    result = generator.generate_voice_with_api(
        text="A beautiful voice experience",
        voice_preset="romantic",
        quality_boost=True
    )
```

### Style Consistency

Ensure voice style consistency:

```python
# Check style consistency
consistency_score = assessor.check_voice_style_consistency(
    voice_path="output/generated_voice.wav",
    target_style="romantic"
)

# Adjust style if needed
if consistency_score < 0.8:
    result = generator.adjust_voice_style(
        voice_path="output/generated_voice.wav",
        target_style="romantic",
        adjustment_strength=0.5
    )
```

## File Management

### Input Management

Manage input voice files:

```python
from voice.file_manager import VoiceFileManager

file_manager = VoiceFileManager()

# Organize input voice files
file_manager.organize_input_voices(
    source_directory="voice/input/",
    organization_type="by_category"
)

# Validate input voice files
validation_result = file_manager.validate_input_voices(
    voice_directory="voice/input/",
    validation_criteria=["format", "quality", "duration"]
)
```

### Output Management

Manage generated voice files:

```python
# Organize output voice files
file_manager.organize_output_voices(
    output_directory="voice/output/",
    organization_type="by_date_and_type"
)

# Clean old voice files
file_manager.clean_old_voices(
    directory="voice/output/",
    max_age_days=30
)

# Backup important voice files
file_manager.backup_voices(
    source_directory="voice/output/",
    backup_directory="voice/backups/",
    backup_type="incremental"
)
```

## Future Enhancements

Planned improvements:

1. **Advanced Voice Synthesis**: More sophisticated voice synthesis capabilities
2. **Real-time Generation**: Real-time voice generation and preview
3. **Interactive Voice**: Interactive voice editing capabilities
4. **Style Learning**: Learn and adapt to user voice preferences
5. **Batch Optimization**: Advanced batch processing and optimization
6. **Quality Prediction**: Predict voice quality before generation

## Best Practices

### Generation
- Use clear, well-structured text
- Specify voice style and emotion clearly
- Test different parameters for optimal results
- Cache frequently used voices

### Processing
- Maintain voice quality throughout processing
- Use appropriate formats for different uses
- Optimize file sizes for different platforms
- Backup important generated voices

### Integration
- Ensure seamless integration with Discord
- Maintain consistent quality across systems
- Optimize for user experience
- Monitor performance and quality metrics

## Support

For voice system support:

1. Check engine availability and initialization
2. Verify voice generation and processing
3. Test voice quality and performance
4. Monitor integration with other systems
5. Review file management and storage

The voice system provides comprehensive voice generation and processing capabilities for the AI writing companion, enabling rich audio content creation and integration with all multimodal features. 