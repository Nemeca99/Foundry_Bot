# Image Directory

## Overview

The `image/` directory contains image processing, generation, and management systems for the AI writing companion. This system handles image generation, processing, storage, and integration with the multimodal capabilities. **ALL IMAGE SYSTEMS NOW HAVE COMPREHENSIVE QUEUE INTEGRATION!**

## Structure

```
image/
├── README.md                    # This documentation file
├── input/                       # Input images for processing
├── output/                      # Generated and processed images
└── enhanced_image_generator.py  # Enhanced image generation system (WITH QUEUE SYSTEM)
```

## 🔄 **COMPREHENSIVE QUEUE SYSTEM**

### **Queue System Integration**
The image system integrates with the comprehensive queue system for scalable, loosely-coupled architecture:

- **EnhancedImageGenerator**: Queue-based image generation operations
- **Image Processing**: Queue-based image enhancement and effects
- **Image Analysis**: Queue-based image quality assessment
- **Image Integration**: Queue-based integration with other systems
- **Style Management**: Queue-based style preset management

### **Queue System Benefits**
1. **Loose Coupling**: Image systems communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in image processing don't affect other systems
4. **Scalable Architecture**: Image systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting

### **Image System Queue Integration Pattern**
```python
class ImageGenerator(QueueProcessor):
    def __init__(self):
        super().__init__("image_generator")
        # Image system initialization
    
    def _process_item(self, item):
        """Process queue items for image operations"""
        operation_type = item.data.get("type", "unknown")
        
        if operation_type == "generate_image":
            return self._handle_generate_image(item.data)
        elif operation_type == "process_image":
            return self._handle_process_image(item.data)
        elif operation_type == "analyze_image":
            return self._handle_analyze_image(item.data)
        else:
            return super()._process_item(item)
```

## Core Components

### Enhanced Image Generator

The `enhanced_image_generator.py` provides advanced image generation capabilities with queue integration:

#### Features:
- **Multiple Models**: Local Stable Diffusion, Stable Diffusion WebUI API, DALL-E API with queue integration
- **Style Presets**: Romantic, fantasy, modern, vintage, anime, realistic, artistic with queue management
- **High Quality**: 512x512 to 1920x1080 resolution support with queue-based processing
- **CUDA Support**: GPU acceleration for faster generation with queue optimization
- **Character Portraits**: Specialized character portrait generation through queue system
- **Story Covers**: Book cover and story illustration generation through queue system
- **Queue Integration**: Complete queue system integration for scalable processing

#### Usage:
```python
from image.enhanced_image_generator import EnhancedImageGenerator

generator = EnhancedImageGenerator()

# Load local model through queue system
await send_to_queue("image_generator", {
    "type": "load_stable_diffusion_model"
})

# Generate image with local model through queue system
result = await send_to_queue("image_generator", {
    "type": "generate_image_with_stable_diffusion",
    "prompt": "A beautiful sunset over the ocean",
    "style": "romantic"
})

# Generate character portrait through queue system
portrait_result = await send_to_queue("image_generator", {
    "type": "generate_character_portrait",
    "character_name": "Luna",
    "description": "A mysterious AI companion with glowing eyes",
    "style": "romantic"
})

# Generate story cover through queue system
cover_result = await send_to_queue("image_generator", {
    "type": "generate_story_cover",
    "story_title": "The Enchanted Garden",
    "genre": "fantasy",
    "style": "epic"
})
```

### Input Directory

The `input/` directory contains:

#### Reference Images
- **Character References**: Images for character development
- **Style References**: Images for style matching
- **Scene References**: Images for scene generation
- **Mood References**: Images for emotional tone

#### Processing Images
- **Base Images**: Images for enhancement and modification
- **Template Images**: Templates for consistent generation
- **Background Images**: Background images for composition

### Output Directory

The `output/` directory contains:

#### Generated Images
- **Character Portraits**: Generated character images
- **Story Covers**: Generated book covers
- **Scene Images**: Generated scene illustrations
- **Concept Art**: Generated concept artwork

#### Processed Images
- **Enhanced Images**: Images with applied effects
- **Composited Images**: Combined and layered images
- **Formatted Images**: Images prepared for specific uses

## Image Generation

### Local Generation

Generate images using local Stable Diffusion models through queue system:

```python
# Initialize local model through queue system
await send_to_queue("image_generator", {
    "type": "load_stable_diffusion_model"
})

# Generate image locally through queue system
result = await send_to_queue("image_generator", {
    "type": "generate_image_with_stable_diffusion",
    "prompt": "A romantic sunset scene",
    "style": "romantic",
    "size": (512, 512)
})

if result["success"]:
    print(f"Image generated: {result['path']}")
```

### API Generation

Generate images using external APIs through queue system:

```python
# Generate with Stable Diffusion API through queue system
result = await send_to_queue("image_generator", {
    "type": "generate_image_with_api",
    "prompt": "A fantasy castle in the clouds",
    "style": "fantasy",
    "api_type": "stable_diffusion"
})

# Generate with DALL-E API through queue system
result = await send_to_queue("image_generator", {
    "type": "generate_image_with_api",
    "prompt": "A modern cityscape at night",
    "style": "modern",
    "api_type": "dalle"
})
```

### Character Generation

Specialized character portrait generation through queue system:

```python
# Generate character portrait through queue system
portrait_result = await send_to_queue("image_generator", {
    "type": "generate_character_portrait",
    "character_name": "Luna",
    "description": "A mysterious AI companion with glowing eyes and flowing hair",
    "style": "romantic",
    "mood": "mysterious"
})

# Generate character in different poses through queue system
poses = ["standing", "sitting", "closeup", "full_body"]
for pose in poses:
    pose_result = await send_to_queue("image_generator", {
        "type": "generate_character_portrait",
        "character_name": "Luna",
        "description": f"Luna in {pose} pose",
        "style": "romantic",
        "pose": pose
    })
```

## Style Presets

### Available Styles

The system includes multiple style presets with queue integration:

#### Romantic Style
- **Description**: Soft, warm, intimate imagery
- **Characteristics**: Warm lighting, soft colors, intimate compositions
- **Use Cases**: Character portraits, romantic scenes, intimate moments
- **Queue Integration**: Queue-based style application and management

#### Fantasy Style
- **Description**: Magical, mystical, detailed artwork
- **Characteristics**: Rich colors, magical elements, detailed backgrounds
- **Use Cases**: Fantasy characters, magical scenes, epic landscapes
- **Queue Integration**: Queue-based style application and management

#### Modern Style
- **Description**: Contemporary, clean, professional imagery
- **Characteristics**: Clean lines, modern aesthetics, professional quality
- **Use Cases**: Modern characters, contemporary scenes, professional content
- **Queue Integration**: Queue-based style application and management

#### Vintage Style
- **Description**: Retro, classic, nostalgic imagery
- **Characteristics**: Retro colors, classic compositions, nostalgic elements
- **Use Cases**: Period pieces, retro characters, nostalgic scenes
- **Queue Integration**: Queue-based style application and management

#### Anime Style
- **Description**: Colorful, stylized, detailed anime artwork
- **Characteristics**: Bright colors, stylized features, detailed expressions
- **Use Cases**: Anime characters, stylized scenes, colorful artwork
- **Queue Integration**: Queue-based style application and management

#### Realistic Style
- **Description**: Photorealistic, sharp focus imagery
- **Characteristics**: High detail, realistic lighting, sharp focus
- **Use Cases**: Realistic portraits, detailed scenes, professional photography
- **Queue Integration**: Queue-based style application and management

#### Artistic Style
- **Description**: Creative, beautiful, masterpiece artwork
- **Characteristics**: Artistic composition, creative elements, beautiful aesthetics
- **Use Cases**: Artistic portraits, creative scenes, masterpiece artwork
- **Queue Integration**: Queue-based style application and management

### Style Customization

Customize styles for specific needs through queue system:

```python
# Create custom style through queue system
custom_style = {
    "prompt_modifier": "your custom style, detailed, high quality",
    "negative_prompt": "ugly, blurry, low quality",
    "guidance_scale": 7.5,
    "num_inference_steps": 50,
    "width": 512,
    "height": 512
}

# Apply custom style through queue system
result = await send_to_queue("image_generator", {
    "type": "generate_image_with_custom_style",
    "prompt": "A beautiful character",
    "custom_style": custom_style
})
```

## Image Processing

### Image Enhancement

Enhance generated images through queue system:

```python
from image.processor import ImageProcessor

processor = ImageProcessor()

# Enhance image quality through queue system
enhanced_image = await send_to_queue("image_processor", {
    "type": "enhance_image",
    "image_path": "output/generated_image.png",
    "enhancement_type": "quality_improvement"
})

# Apply artistic effects through queue system
artistic_image = await send_to_queue("image_processor", {
    "type": "apply_artistic_effects",
    "image_path": "output/generated_image.png",
    "effects": ["color_grading", "lighting_enhancement", "detail_enhancement"]
})
```

### Image Composition

Compose multiple images through queue system:

```python
# Composite character with background through queue system
composite_result = await send_to_queue("image_processor", {
    "type": "composite_images",
    "foreground": "output/character_portrait.png",
    "background": "output/background_scene.png",
    "composition_type": "natural_blend"
})

# Create image collage through queue system
collage_result = await send_to_queue("image_processor", {
    "type": "create_image_collage",
    "images": ["image1.png", "image2.png", "image3.png"],
    "layout": "grid_3x3"
})
```

### Image Formatting

Format images for different uses through queue system:

```python
# Format for Discord through queue system
discord_image = await send_to_queue("image_processor", {
    "type": "format_for_discord",
    "image_path": "output/generated_image.png",
    "max_size": (800, 800)
})

# Format for book cover through queue system
cover_image = await send_to_queue("image_processor", {
    "type": "format_for_book_cover",
    "image_path": "output/generated_image.png",
    "dimensions": (1200, 1600)
})

# Format for social media through queue system
social_image = await send_to_queue("image_processor", {
    "type": "format_for_social_media",
    "image_path": "output/generated_image.png",
    "platform": "instagram"
})
```

## Integration with Other Systems

### Discord Integration

Images integrate with Discord bot through queue system:

```python
# Generate and send image to Discord through queue system
async def generate_and_send_image(ctx, prompt: str, style: str):
    # Generate image through queue system
    result = await send_to_queue("image_generator", {
        "type": "generate_image_with_stable_diffusion",
        "prompt": prompt,
        "style": style
    })
    
    if result["success"]:
        # Create Discord embed
        embed = discord.Embed(
            title="🎨 Image Generated",
            description=f"**Prompt:** {prompt}",
            color=0x9B59B6
        )
        
        # Attach image file
        file = discord.File(result["path"], filename="generated_image.png")
        embed.set_image(url="attachment://generated_image.png")
        
        await ctx.send(embed=embed, file=file)
```

### Multimodal Integration

Images integrate with multimodal systems through queue system:

```python
from framework.plugins.multimodal_orchestrator import MultimodalOrchestrator

orchestrator = MultimodalOrchestrator()

# Create character multimedia package through queue system
result = await send_to_queue("multimodal_orchestrator", {
    "type": "create_character_multimedia",
    "character_name": "Luna",
    "character_description": "A mysterious AI companion",
    "style": "romantic",
    "include_portrait": True,
    "include_voice": True,
    "include_ambient": True
})
```

### Emotional Integration

Images adapt to emotional context through queue system:

```python
from astra_emotional_fragments.emotional_blender import EnhancedEmotionalBlender

emotional_blender = EnhancedEmotionalBlender()

# Analyze emotional context through queue system
emotional_context = await send_to_queue("emotional_blender", {
    "type": "analyze_emotional_context",
    "user_message": "I'm feeling really happy today"
})

# Generate emotionally-aware image through queue system
emotionally_aware_image = await send_to_queue("image_generator", {
    "type": "generate_emotionally_aware_image",
    "prompt": "A character portrait",
    "emotional_context": emotional_context,
    "style": "romantic"
})
```

## Performance Optimization

### GPU Acceleration

Optimize for GPU performance through queue system:

```python
# Check CUDA availability through queue system
cuda_available = await send_to_queue("image_generator", {
    "type": "check_cuda_availability"
})

if cuda_available:
    # Use GPU acceleration through queue system
    result = await send_to_queue("image_generator", {
        "type": "generate_image_with_gpu",
        "prompt": "A beautiful scene",
        "style": "romantic",
        "gpu_memory_optimization": True
    })
else:
    # Use CPU fallback through queue system
    result = await send_to_queue("image_generator", {
        "type": "generate_image_with_cpu",
        "prompt": "A beautiful scene",
        "style": "romantic"
    })
```

### Batch Processing

Process multiple images efficiently through queue system:

```python
# Batch generate images through queue system
prompts = [
    "A romantic sunset",
    "A fantasy castle",
    "A modern cityscape"
]

batch_results = await send_to_queue("image_generator", {
    "type": "generate_batch",
    "prompts": prompts,
    "style": "romantic",
    "batch_size": 3
})
```

### Caching System

Cache generated images for reuse through queue system:

```python
# Check if image exists in cache through queue system
cached_image = await send_to_queue("image_generator", {
    "type": "check_cache",
    "prompt": "A romantic sunset",
    "style": "romantic"
})

if cached_image:
    # Use cached image
    result = {"success": True, "path": cached_image}
else:
    # Generate new image through queue system
    result = await send_to_queue("image_generator", {
        "type": "generate_image_with_stable_diffusion",
        "prompt": "A romantic sunset",
        "style": "romantic"
    })
    # Cache the result through queue system
    await send_to_queue("image_generator", {
        "type": "cache_image",
        "image_path": result["path"],
        "prompt": "A romantic sunset",
        "style": "romantic"
    })
```

## Quality Control

### Image Quality Assessment

Assess generated image quality through queue system:

```python
from image.quality import ImageQualityAssessor

assessor = ImageQualityAssessor()

# Assess image quality through queue system
quality_score = await send_to_queue("image_processor", {
    "type": "assess_image_quality",
    "image_path": "output/generated_image.png",
    "criteria": ["sharpness", "composition", "color_balance", "artistic_value"]
})

# Filter low-quality images through queue system
if quality_score < 0.7:
    # Regenerate with improved parameters through queue system
    result = await send_to_queue("image_generator", {
        "type": "generate_image_with_stable_diffusion",
        "prompt": "A romantic sunset",
        "style": "romantic",
        "quality_boost": True
    })
```

### Style Consistency

Ensure style consistency through queue system:

```python
# Check style consistency through queue system
consistency_score = await send_to_queue("image_processor", {
    "type": "check_style_consistency",
    "image_path": "output/generated_image.png",
    "target_style": "romantic"
})

# Adjust style if needed through queue system
if consistency_score < 0.8:
    result = await send_to_queue("image_generator", {
        "type": "adjust_style",
        "image_path": "output/generated_image.png",
        "target_style": "romantic",
        "adjustment_strength": 0.5
    })
```

## File Management

### Input Management

Manage input images through queue system:

```python
from image.file_manager import ImageFileManager

file_manager = ImageFileManager()

# Organize input images through queue system
await send_to_queue("image_processor", {
    "type": "organize_input_images",
    "source_directory": "image/input/",
    "organization_type": "by_category"
})

# Validate input images through queue system
validation_result = await send_to_queue("image_processor", {
    "type": "validate_input_images",
    "image_directory": "image/input/",
    "validation_criteria": ["format", "size", "quality"]
})
```

### Output Management

Manage generated images through queue system:

```python
# Organize output images through queue system
await send_to_queue("image_processor", {
    "type": "organize_output_images",
    "output_directory": "image/output/",
    "organization_type": "by_date_and_type"
})

# Clean old images through queue system
await send_to_queue("image_processor", {
    "type": "clean_old_images",
    "directory": "image/output/",
    "max_age_days": 30
})

# Backup important images through queue system
await send_to_queue("image_processor", {
    "type": "backup_images",
    "source_directory": "image/output/",
    "backup_directory": "image/backups/",
    "backup_type": "incremental"
})
```

## Queue System Benefits

### Achieved Benefits

1. **Loose Coupling**: Image systems communicate without direct dependencies
2. **Bottleneck Detection**: Queue monitoring identifies performance issues
3. **Error Isolation**: Failures in image processing don't affect other systems
4. **Scalable Architecture**: Image systems can be scaled independently
5. **Real-time Monitoring**: Comprehensive metrics and alerting system

### Queue System Features

- **QueueManager**: Central queue management and monitoring
- **QueueProcessor**: Base class for all image systems
- **QueueItem**: Standardized data structure for inter-system communication
- **SystemQueue**: Individual image system queue management
- **Alert System**: Configurable thresholds for warnings and critical alerts

## Future Enhancements

Planned improvements:

1. **Advanced Style Transfer**: More sophisticated style transfer capabilities
2. **Real-time Generation**: Real-time image generation and preview
3. **Interactive Editing**: Interactive image editing capabilities
4. **Style Learning**: Learn and adapt to user style preferences
5. **Batch Optimization**: Advanced batch processing and optimization
6. **Quality Prediction**: Predict image quality before generation
7. **Queue System Enhancement**: Advanced queue features

## Best Practices

### Generation
- Use clear, descriptive prompts
- Specify style and mood clearly
- Test different parameters for optimal results
- Cache frequently used images
- Use queue system for all image operations

### Processing
- Maintain image quality throughout processing
- Use appropriate formats for different uses
- Optimize file sizes for different platforms
- Backup important generated images
- Monitor queue system performance

### Integration
- Ensure seamless integration with Discord through queue system
- Maintain consistent quality across systems
- Optimize for user experience
- Monitor performance and quality metrics
- Use queue system for all inter-system communication

## Support

For image system support:

1. Check GPU availability and CUDA installation
2. Verify model loading and initialization through queue system
3. Test image generation with different prompts through queue system
4. Monitor quality and performance metrics
5. Review integration with other systems through queue system
6. Monitor queue system performance

The image system provides comprehensive image generation and processing capabilities for the AI writing companion, enabling rich visual content creation and integration with all multimodal features through complete queue system integration for scalable, loosely-coupled architecture. 