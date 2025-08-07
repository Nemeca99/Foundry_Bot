# Video Directory

## Overview

The `video/` directory contains video generation, processing, and management systems for the AI writing companion. This system handles video creation, editing, effects, and integration with the multimodal capabilities. **ALL VIDEO SYSTEMS NOW HAVE COMPREHENSIVE QUEUE INTEGRATION!**

## Structure

```
video/
├── README.md                    # This documentation file
├── output/                      # Generated and processed videos
└── enhanced_video_generator.py  # Enhanced video generation system (WITH QUEUE SYSTEM)
```

## 🔄 **COMPREHENSIVE QUEUE SYSTEM**

### **Queue System Integration**
The video system integrates with the comprehensive queue system for scalable, loosely-coupled architecture:

- **EnhancedVideoGenerator**: Queue-based video generation operations
- **Video Processing**: Queue-based video enhancement and effects
- **Video Analysis**: Queue-based video quality assessment
- **Video Integration**: Queue-based integration with other systems
- **Style Management**: Queue-based style preset management

### **Queue System Benefits**
1. **Loose Coupling**: Video systems communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in video processing don't affect other systems
4. **Scalable Architecture**: Video systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting

### **Video System Queue Integration Pattern**
```python
class VideoGenerator(QueueProcessor):
    def __init__(self):
        super().__init__("video_generator")
        # Video system initialization
    
    def _process_item(self, item):
        """Process queue items for video operations"""
        operation_type = item.data.get("type", "unknown")
        
        if operation_type == "generate_video":
            return self._handle_generate_video(item.data)
        elif operation_type == "process_video":
            return self._handle_process_video(item.data)
        elif operation_type == "analyze_video":
            return self._handle_analyze_video(item.data)
        else:
            return super()._process_item(item)
```

## Core Components

### Enhanced Video Generator

The `enhanced_video_generator.py` provides advanced video generation capabilities with queue integration:

#### Features:
- **Multiple APIs**: Runway ML, Replicate, Stability AI integration with queue system
- **Style Presets**: Romantic, fantasy, modern, vintage, anime, realistic, artistic with queue management
- **Video Types**: Character videos, story scenes, ambient videos, music videos with queue processing
- **Effects**: Transitions, filters, overlays, text animations with queue-based application
- **Audio Integration**: Video with synchronized audio through queue system
- **High Quality**: 720p to 4K resolution support with queue-based processing
- **Queue Integration**: Complete queue system integration for scalable processing

#### Usage:
```python
from video.enhanced_video_generator import EnhancedVideoGenerator

generator = EnhancedVideoGenerator()

# Generate video from images through queue system
result = await send_to_queue("video_generator", {
    "type": "generate_video_from_images",
    "image_paths": ["image1.png", "image2.png", "image3.png"],
    "duration": 10,
    "transition_effect": "fade"
})

# Generate character video through queue system
character_result = await send_to_queue("video_generator", {
    "type": "create_character_video",
    "character_name": "Luna",
    "description": "A mysterious AI companion",
    "style": "romantic",
    "duration": 15
})

# Generate story scene video through queue system
scene_result = await send_to_queue("video_generator", {
    "type": "create_story_scene_video",
    "scene_description": "A romantic sunset scene",
    "genre": "romance",
    "style": "romantic",
    "duration": 20
})
```

### Output Directory

The `output/` directory contains:

#### Generated Videos
- **Character Videos**: Generated character introduction videos
- **Story Scenes**: Generated story scene videos
- **Ambient Videos**: Background and mood videos
- **Music Videos**: Videos with synchronized music
- **Trailers**: Story and character trailers

#### Processed Videos
- **Enhanced Videos**: Videos with applied effects
- **Composited Videos**: Combined and layered videos
- **Formatted Videos**: Videos prepared for specific platforms

## Video Generation

### Local Generation

Generate videos using local tools through queue system:

```python
# Generate video from image sequence through queue system
result = await send_to_queue("video_generator", {
    "type": "generate_video_from_images",
    "image_paths": ["frame1.png", "frame2.png", "frame3.png"],
    "output_path": "output/character_video.mp4",
    "fps": 24,
    "duration": 10
})

# Create video collage through queue system
collage_result = await send_to_queue("video_generator", {
    "type": "create_video_collage",
    "video_paths": ["video1.mp4", "video2.mp4", "video3.mp4"],
    "layout": "grid_2x2",
    "output_path": "output/collage.mp4"
})
```

### API Generation

Generate videos using external APIs through queue system:

```python
# Generate with Runway ML API through queue system
result = await send_to_queue("video_generator", {
    "type": "generate_video_with_api",
    "prompt": "A romantic sunset scene",
    "style": "romantic",
    "api_type": "runway_ml",
    "duration": 15
})

# Generate with Replicate API through queue system
result = await send_to_queue("video_generator", {
    "type": "generate_video_with_api",
    "prompt": "A fantasy castle in the clouds",
    "style": "fantasy",
    "api_type": "replicate",
    "duration": 20
})

# Generate with Stability AI API through queue system
result = await send_to_queue("video_generator", {
    "type": "generate_video_with_api",
    "prompt": "A modern cityscape at night",
    "style": "modern",
    "api_type": "stability_ai",
    "duration": 15
})
```

### Character Video Generation

Specialized character video generation through queue system:

```python
# Generate character introduction video through queue system
intro_result = await send_to_queue("video_generator", {
    "type": "create_character_video",
    "character_name": "Luna",
    "description": "A mysterious AI companion with glowing eyes",
    "style": "romantic",
    "duration": 15,
    "include_audio": True
})

# Generate character in different scenes through queue system
scenes = ["romantic", "mysterious", "playful", "supportive"]
for scene in scenes:
    scene_result = await send_to_queue("video_generator", {
        "type": "create_character_video",
        "character_name": "Luna",
        "description": f"Luna in {scene} mood",
        "style": "romantic",
        "mood": scene,
        "duration": 10
    })
```

## Style Presets

### Available Styles

The system includes multiple video style presets with queue integration:

#### Romantic Style
- **Description**: Soft, warm, intimate video content
- **Characteristics**: Warm lighting, soft transitions, intimate compositions
- **Use Cases**: Character introductions, romantic scenes, intimate moments
- **Queue Integration**: Queue-based style application and management

#### Fantasy Style
- **Description**: Magical, mystical, epic video content
- **Characteristics**: Rich colors, magical effects, epic compositions
- **Use Cases**: Fantasy characters, magical scenes, epic landscapes
- **Queue Integration**: Queue-based style application and management

#### Modern Style
- **Description**: Contemporary, clean, professional video content
- **Characteristics**: Clean transitions, modern aesthetics, professional quality
- **Use Cases**: Modern characters, contemporary scenes, professional content
- **Queue Integration**: Queue-based style application and management

#### Vintage Style
- **Description**: Retro, classic, nostalgic video content
- **Characteristics**: Retro effects, classic compositions, nostalgic elements
- **Use Cases**: Period pieces, retro characters, nostalgic scenes
- **Queue Integration**: Queue-based style application and management

#### Anime Style
- **Description**: Colorful, stylized, detailed anime video content
- **Characteristics**: Bright colors, stylized effects, detailed animations
- **Use Cases**: Anime characters, stylized scenes, colorful content
- **Queue Integration**: Queue-based style application and management

#### Realistic Style
- **Description**: Photorealistic, sharp focus video content
- **Characteristics**: High detail, realistic lighting, sharp focus
- **Use Cases**: Realistic scenes, detailed environments, professional footage
- **Queue Integration**: Queue-based style application and management

#### Artistic Style
- **Description**: Creative, beautiful, masterpiece video content
- **Characteristics**: Artistic composition, creative effects, beautiful aesthetics
- **Use Cases**: Artistic scenes, creative content, masterpiece videos
- **Queue Integration**: Queue-based style application and management

### Style Customization

Customize video styles for specific needs through queue system:

```python
# Create custom video style through queue system
custom_style = {
    "transition_effects": ["fade", "slide", "zoom"],
    "color_grading": "warm_romantic",
    "text_effects": "elegant_typography",
    "audio_style": "ambient_romantic",
    "duration_range": (10, 30),
    "fps": 24
}

# Apply custom style through queue system
result = await send_to_queue("video_generator", {
    "type": "generate_video_with_custom_style",
    "prompt": "A beautiful character video",
    "custom_style": custom_style
})
```

## Video Processing

### Video Enhancement

Enhance generated videos through queue system:

```python
from video.processor import VideoProcessor

processor = VideoProcessor()

# Enhance video quality through queue system
enhanced_video = await send_to_queue("video_processor", {
    "type": "enhance_video",
    "video_path": "output/generated_video.mp4",
    "enhancement_type": "quality_improvement"
})

# Apply artistic effects through queue system
artistic_video = await send_to_queue("video_processor", {
    "type": "apply_artistic_effects",
    "video_path": "output/generated_video.mp4",
    "effects": ["color_grading", "lighting_enhancement", "motion_blur"]
})
```

### Video Composition

Compose multiple videos through queue system:

```python
# Composite character with background through queue system
composite_result = await send_to_queue("video_processor", {
    "type": "composite_videos",
    "foreground": "output/character_video.mp4",
    "background": "output/background_video.mp4",
    "composition_type": "natural_blend"
})

# Create video montage through queue system
montage_result = await send_to_queue("video_processor", {
    "type": "create_video_montage",
    "videos": ["video1.mp4", "video2.mp4", "video3.mp4"],
    "transition_effects": ["fade", "slide", "zoom"]
})
```

### Video Formatting

Format videos for different platforms through queue system:

```python
# Format for Discord through queue system
discord_video = await send_to_queue("video_processor", {
    "type": "format_for_discord",
    "video_path": "output/generated_video.mp4",
    "max_size": (800, 600),
    "max_duration": 25
})

# Format for social media through queue system
social_video = await send_to_queue("video_processor", {
    "type": "format_for_social_media",
    "video_path": "output/generated_video.mp4",
    "platform": "instagram",
    "aspect_ratio": "1:1"
})

# Format for streaming through queue system
streaming_video = await send_to_queue("video_processor", {
    "type": "format_for_streaming",
    "video_path": "output/generated_video.mp4",
    "quality": "high",
    "compression": "h264"
})
```

## Audio Integration

### Video with Audio

Create videos with synchronized audio through queue system:

```python
# Create video with background music through queue system
video_with_music = await send_to_queue("video_generator", {
    "type": "create_video_with_audio",
    "video_path": "output/character_video.mp4",
    "audio_path": "output/romantic_music.mp3",
    "sync_type": "background"
})

# Create video with voice narration through queue system
video_with_voice = await send_to_queue("video_generator", {
    "type": "create_video_with_audio",
    "video_path": "output/story_scene.mp4",
    "audio_path": "output/voice_narration.mp3",
    "sync_type": "narration"
})

# Create video with sound effects through queue system
video_with_effects = await send_to_queue("video_generator", {
    "type": "create_video_with_audio",
    "video_path": "output/action_scene.mp4",
    "audio_path": "output/sound_effects.mp3",
    "sync_type": "effects"
})
```

### Audio Processing

Process audio for video integration through queue system:

```python
# Process audio for video through queue system
processed_audio = await send_to_queue("video_processor", {
    "type": "process_audio_for_video",
    "audio_path": "input/audio.mp3",
    "video_duration": 15,
    "fade_in": 1.0,
    "fade_out": 1.0
})

# Synchronize audio with video through queue system
synced_result = await send_to_queue("video_processor", {
    "type": "synchronize_audio_video",
    "video_path": "output/video.mp4",
    "audio_path": "output/audio.mp3",
    "sync_points": [0, 5, 10, 15]
})
```

## Integration with Other Systems

### Discord Integration

Videos integrate with Discord bot through queue system:

```python
# Generate and send video to Discord through queue system
async def generate_and_send_video(ctx, prompt: str, style: str):
    # Generate video through queue system
    result = await send_to_queue("video_generator", {
        "type": "generate_video_with_api",
        "prompt": prompt,
        "style": style,
        "duration": 15
    })
    
    if result["success"]:
        # Create Discord embed
        embed = discord.Embed(
            title="🎬 Video Generated",
            description=f"**Prompt:** {prompt}",
            color=0x9B59B6
        )
        
        # Attach video file
        file = discord.File(result["path"], filename="generated_video.mp4")
        embed.set_video(url="attachment://generated_video.mp4")
        
        await ctx.send(embed=embed, file=file)
```

### Multimodal Integration

Videos integrate with multimodal systems through queue system:

```python
from framework.plugins.multimodal_orchestrator import MultimodalOrchestrator

orchestrator = MultimodalOrchestrator()

# Create character multimedia package through queue system
result = await send_to_queue("multimodal_orchestrator", {
    "type": "create_character_multimedia",
    "character_name": "Luna",
    "character_description": "A mysterious AI companion",
    "style": "romantic",
    "include_video": True,
    "include_audio": True,
    "include_portrait": True
})
```

### Emotional Integration

Videos adapt to emotional context through queue system:

```python
from astra_emotional_fragments.emotional_blender import EnhancedEmotionalBlender

emotional_blender = EnhancedEmotionalBlender()

# Analyze emotional context through queue system
emotional_context = await send_to_queue("emotional_blender", {
    "type": "analyze_emotional_context",
    "user_message": "I'm feeling really happy today"
})

# Generate emotionally-aware video through queue system
emotionally_aware_video = await send_to_queue("video_generator", {
    "type": "generate_emotionally_aware_video",
    "prompt": "A character video",
    "emotional_context": emotional_context,
    "style": "romantic"
})
```

## Performance Optimization

### Hardware Acceleration

Optimize for hardware performance through queue system:

```python
# Check hardware acceleration through queue system
hardware_available = await send_to_queue("video_generator", {
    "type": "check_hardware_acceleration"
})

if hardware_available:
    # Use hardware acceleration through queue system
    result = await send_to_queue("video_generator", {
        "type": "generate_video_with_hardware",
        "prompt": "A beautiful scene",
        "style": "romantic",
        "hardware_acceleration": True
    })
else:
    # Use software fallback through queue system
    result = await send_to_queue("video_generator", {
        "type": "generate_video_with_software",
        "prompt": "A beautiful scene",
        "style": "romantic"
    })
```

### Batch Processing

Process multiple videos efficiently through queue system:

```python
# Batch generate videos through queue system
prompts = [
    "A romantic sunset scene",
    "A fantasy castle",
    "A modern cityscape"
]

batch_results = await send_to_queue("video_generator", {
    "type": "generate_batch",
    "prompts": prompts,
    "style": "romantic",
    "batch_size": 3
})
```

### Caching System

Cache generated videos for reuse through queue system:

```python
# Check if video exists in cache through queue system
cached_video = await send_to_queue("video_generator", {
    "type": "check_cache",
    "prompt": "A romantic sunset",
    "style": "romantic"
})

if cached_video:
    # Use cached video
    result = {"success": True, "path": cached_video}
else:
    # Generate new video through queue system
    result = await send_to_queue("video_generator", {
        "type": "generate_video_with_api",
        "prompt": "A romantic sunset",
        "style": "romantic"
    })
    # Cache the result through queue system
    await send_to_queue("video_generator", {
        "type": "cache_video",
        "video_path": result["path"],
        "prompt": "A romantic sunset",
        "style": "romantic"
    })
```

## Quality Control

### Video Quality Assessment

Assess generated video quality through queue system:

```python
from video.quality import VideoQualityAssessor

assessor = VideoQualityAssessor()

# Assess video quality through queue system
quality_score = await send_to_queue("video_processor", {
    "type": "assess_video_quality",
    "video_path": "output/generated_video.mp4",
    "criteria": ["sharpness", "smoothness", "color_balance", "artistic_value"]
})

# Filter low-quality videos through queue system
if quality_score < 0.7:
    # Regenerate with improved parameters through queue system
    result = await send_to_queue("video_generator", {
        "type": "generate_video_with_api",
        "prompt": "A romantic sunset",
        "style": "romantic",
        "quality_boost": True
    })
```

### Style Consistency

Ensure style consistency through queue system:

```python
# Check style consistency through queue system
consistency_score = await send_to_queue("video_processor", {
    "type": "check_style_consistency",
    "video_path": "output/generated_video.mp4",
    "target_style": "romantic"
})

# Adjust style if needed through queue system
if consistency_score < 0.8:
    result = await send_to_queue("video_generator", {
        "type": "adjust_video_style",
        "video_path": "output/generated_video.mp4",
        "target_style": "romantic",
        "adjustment_strength": 0.5
    })
```

## File Management

### Input Management

Manage input videos through queue system:

```python
from video.file_manager import VideoFileManager

file_manager = VideoFileManager()

# Organize input videos through queue system
await send_to_queue("video_processor", {
    "type": "organize_input_videos",
    "source_directory": "video/input/",
    "organization_type": "by_category"
})

# Validate input videos through queue system
validation_result = await send_to_queue("video_processor", {
    "type": "validate_input_videos",
    "video_directory": "video/input/",
    "validation_criteria": ["format", "resolution", "duration"]
})
```

### Output Management

Manage generated videos through queue system:

```python
# Organize output videos through queue system
await send_to_queue("video_processor", {
    "type": "organize_output_videos",
    "output_directory": "video/output/",
    "organization_type": "by_date_and_type"
})

# Clean old videos through queue system
await send_to_queue("video_processor", {
    "type": "clean_old_videos",
    "directory": "video/output/",
    "max_age_days": 30
})

# Backup important videos through queue system
await send_to_queue("video_processor", {
    "type": "backup_videos",
    "source_directory": "video/output/",
    "backup_directory": "video/backups/",
    "backup_type": "incremental"
})
```

## Queue System Benefits

### Achieved Benefits

1. **Loose Coupling**: Video systems communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in video processing don't affect other systems
4. **Scalable Architecture**: Video systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting system

### Queue System Features

- **QueueManager**: Central queue management and monitoring
- **QueueProcessor**: Base class for all video systems
- **QueueItem**: Standardized data structure for inter-system communication
- **SystemQueue**: Individual video system queue management
- **Alert System**: Configurable thresholds for warnings and critical alerts

## Future Enhancements

Planned improvements:

1. **Advanced Video Effects**: More sophisticated video effects and transitions
2. **Real-time Generation**: Real-time video generation and preview
3. **Interactive Editing**: Interactive video editing capabilities
4. **Style Learning**: Learn and adapt to user style preferences
5. **Batch Optimization**: Advanced batch processing and optimization
6. **Quality Prediction**: Predict video quality before generation
7. **Queue System Enhancement**: Advanced queue features

## Best Practices

### Generation
- Use clear, descriptive prompts
- Specify style and mood clearly
- Test different parameters for optimal results
- Cache frequently used videos
- Use queue system for all video operations

### Processing
- Maintain video quality throughout processing
- Use appropriate formats for different platforms
- Optimize file sizes for different uses
- Backup important generated videos
- Monitor queue system performance

### Integration
- Ensure seamless integration with Discord through queue system
- Maintain consistent quality across systems
- Optimize for user experience
- Monitor performance and quality metrics
- Use queue system for all inter-system communication

## Support

For video system support:

1. Check API keys and service availability
2. Verify video generation and processing through queue system
3. Test video quality and performance
4. Monitor integration with other systems through queue system
5. Review file management and storage
6. Monitor queue system performance

The video system provides comprehensive video generation and processing capabilities for the AI writing companion, enabling rich video content creation and integration with all multimodal features through complete queue system integration for scalable, loosely-coupled architecture. 