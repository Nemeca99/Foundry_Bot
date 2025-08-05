# Image Directory

## Overview

The `image/` directory contains image processing, generation, and management systems for the AI writing companion. This system handles image generation, processing, storage, and integration with the multimodal capabilities.

## Structure

```
image/
├── README.md                    # This documentation file
├── input/                       # Input images for processing
├── output/                      # Generated and processed images
└── enhanced_image_generator.py  # Enhanced image generation system
```

## Core Components

### Enhanced Image Generator

The `enhanced_image_generator.py` provides advanced image generation capabilities:

#### Features:
- **Multiple Models**: Local Stable Diffusion, Stable Diffusion WebUI API, DALL-E API
- **Style Presets**: Romantic, fantasy, modern, vintage, anime, realistic, artistic
- **High Quality**: 512x512 to 1920x1080 resolution support
- **CUDA Support**: GPU acceleration for faster generation
- **Character Portraits**: Specialized character portrait generation
- **Story Covers**: Book cover and story illustration generation

#### Usage:
```python
from image.enhanced_image_generator import EnhancedImageGenerator

generator = EnhancedImageGenerator()

# Load local model
generator.load_stable_diffusion_model()

# Generate image with local model
result = generator.generate_image_with_stable_diffusion(
    prompt="A beautiful sunset over the ocean",
    style="romantic"
)

# Generate character portrait
portrait_result = generator.generate_character_portrait(
    character_name="Luna",
    description="A mysterious AI companion with glowing eyes",
    style="romantic"
)

# Generate story cover
cover_result = generator.generate_story_cover(
    story_title="The Enchanted Garden",
    genre="fantasy",
    style="epic"
)
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

Generate images using local Stable Diffusion models:

```python
# Initialize local model
generator = EnhancedImageGenerator()
success = generator.load_stable_diffusion_model()

if success:
    # Generate image locally
    result = generator.generate_image_with_stable_diffusion(
        prompt="A romantic sunset scene",
        style="romantic",
        size=(512, 512)
    )
    
    if result["success"]:
        print(f"Image generated: {result['path']}")
```

### API Generation

Generate images using external APIs:

```python
# Generate with Stable Diffusion API
result = generator.generate_image_with_api(
    prompt="A fantasy castle in the clouds",
    style="fantasy",
    api_type="stable_diffusion"
)

# Generate with DALL-E API
result = generator.generate_image_with_api(
    prompt="A modern cityscape at night",
    style="modern",
    api_type="dalle"
)
```

### Character Generation

Specialized character portrait generation:

```python
# Generate character portrait
portrait_result = generator.generate_character_portrait(
    character_name="Luna",
    description="A mysterious AI companion with glowing eyes and flowing hair",
    style="romantic",
    mood="mysterious"
)

# Generate character in different poses
poses = ["standing", "sitting", "closeup", "full_body"]
for pose in poses:
    pose_result = generator.generate_character_portrait(
        character_name="Luna",
        description=f"Luna in {pose} pose",
        style="romantic",
        pose=pose
    )
```

## Style Presets

### Available Styles

The system includes multiple style presets:

#### Romantic Style
- **Description**: Soft, warm, intimate imagery
- **Characteristics**: Warm lighting, soft colors, intimate compositions
- **Use Cases**: Character portraits, romantic scenes, intimate moments

#### Fantasy Style
- **Description**: Magical, mystical, detailed artwork
- **Characteristics**: Rich colors, magical elements, detailed backgrounds
- **Use Cases**: Fantasy characters, magical scenes, epic landscapes

#### Modern Style
- **Description**: Contemporary, clean, professional imagery
- **Characteristics**: Clean lines, modern aesthetics, professional quality
- **Use Cases**: Modern characters, contemporary scenes, professional content

#### Vintage Style
- **Description**: Retro, classic, nostalgic imagery
- **Characteristics**: Retro colors, classic compositions, nostalgic elements
- **Use Cases**: Period pieces, retro characters, nostalgic scenes

#### Anime Style
- **Description**: Colorful, stylized, detailed anime artwork
- **Characteristics**: Bright colors, stylized features, detailed expressions
- **Use Cases**: Anime characters, stylized scenes, colorful artwork

#### Realistic Style
- **Description**: Photorealistic, sharp focus imagery
- **Characteristics**: High detail, realistic lighting, sharp focus
- **Use Cases**: Realistic portraits, detailed scenes, professional photography

#### Artistic Style
- **Description**: Creative, beautiful, masterpiece artwork
- **Characteristics**: Artistic composition, creative elements, beautiful aesthetics
- **Use Cases**: Artistic portraits, creative scenes, masterpiece artwork

### Style Customization

Customize styles for specific needs:

```python
# Create custom style
custom_style = {
    "prompt_modifier": "your custom style, detailed, high quality",
    "negative_prompt": "ugly, blurry, low quality",
    "guidance_scale": 7.5,
    "num_inference_steps": 50,
    "width": 512,
    "height": 512
}

# Apply custom style
result = generator.generate_image_with_custom_style(
    prompt="A beautiful character",
    custom_style=custom_style
)
```

## Image Processing

### Image Enhancement

Enhance generated images:

```python
from image.processor import ImageProcessor

processor = ImageProcessor()

# Enhance image quality
enhanced_image = processor.enhance_image(
    image_path="output/generated_image.png",
    enhancement_type="quality_improvement"
)

# Apply artistic effects
artistic_image = processor.apply_artistic_effects(
    image_path="output/generated_image.png",
    effects=["color_grading", "lighting_enhancement", "detail_enhancement"]
)
```

### Image Composition

Compose multiple images:

```python
# Composite character with background
composite_result = processor.composite_images(
    foreground="output/character_portrait.png",
    background="output/background_scene.png",
    composition_type="natural_blend"
)

# Create image collage
collage_result = processor.create_image_collage(
    images=["image1.png", "image2.png", "image3.png"],
    layout="grid_3x3"
)
```

### Image Formatting

Format images for different uses:

```python
# Format for Discord
discord_image = processor.format_for_discord(
    image_path="output/generated_image.png",
    max_size=(800, 800)
)

# Format for book cover
cover_image = processor.format_for_book_cover(
    image_path="output/generated_image.png",
    dimensions=(1200, 1600)
)

# Format for social media
social_image = processor.format_for_social_media(
    image_path="output/generated_image.png",
    platform="instagram"
)
```

## Integration with Other Systems

### Discord Integration

Images integrate with Discord bot:

```python
# Generate and send image to Discord
async def generate_and_send_image(ctx, prompt: str, style: str):
    generator = EnhancedImageGenerator()
    
    # Generate image
    result = generator.generate_image_with_stable_diffusion(prompt, style)
    
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

Images integrate with multimodal systems:

```python
from framework.plugins.multimodal_orchestrator import MultimodalOrchestrator

orchestrator = MultimodalOrchestrator()

# Create character multimedia package
result = orchestrator.create_character_multimedia(
    character_name="Luna",
    character_description="A mysterious AI companion",
    style="romantic",
    include_portrait=True,
    include_voice=True,
    include_ambient=True
)
```

### Emotional Integration

Images adapt to emotional context:

```python
from astra_emotional_fragments.emotional_blender import EnhancedEmotionalBlender

emotional_blender = EnhancedEmotionalBlender()

# Analyze emotional context
emotional_context = emotional_blender.analyze_emotional_context(
    user_message="I'm feeling really happy today"
)

# Generate emotionally-aware image
emotionally_aware_image = generator.generate_emotionally_aware_image(
    prompt="A character portrait",
    emotional_context=emotional_context,
    style="romantic"
)
```

## Performance Optimization

### GPU Acceleration

Optimize for GPU performance:

```python
# Check CUDA availability
cuda_available = generator.check_cuda_availability()

if cuda_available:
    # Use GPU acceleration
    result = generator.generate_image_with_gpu(
        prompt="A beautiful scene",
        style="romantic",
        gpu_memory_optimization=True
    )
else:
    # Use CPU fallback
    result = generator.generate_image_with_cpu(
        prompt="A beautiful scene",
        style="romantic"
    )
```

### Batch Processing

Process multiple images efficiently:

```python
# Batch generate images
prompts = [
    "A romantic sunset",
    "A fantasy castle",
    "A modern cityscape"
]

batch_results = generator.generate_batch(
    prompts=prompts,
    style="romantic",
    batch_size=3
)
```

### Caching System

Cache generated images for reuse:

```python
# Check if image exists in cache
cached_image = generator.check_cache(
    prompt="A romantic sunset",
    style="romantic"
)

if cached_image:
    # Use cached image
    result = {"success": True, "path": cached_image}
else:
    # Generate new image
    result = generator.generate_image_with_stable_diffusion(
        prompt="A romantic sunset",
        style="romantic"
    )
    # Cache the result
    generator.cache_image(result["path"], prompt="A romantic sunset", style="romantic")
```

## Quality Control

### Image Quality Assessment

Assess generated image quality:

```python
from image.quality import ImageQualityAssessor

assessor = ImageQualityAssessor()

# Assess image quality
quality_score = assessor.assess_image_quality(
    image_path="output/generated_image.png",
    criteria=["sharpness", "composition", "color_balance", "artistic_value"]
)

# Filter low-quality images
if quality_score < 0.7:
    # Regenerate with improved parameters
    result = generator.generate_image_with_stable_diffusion(
        prompt="A romantic sunset",
        style="romantic",
        quality_boost=True
    )
```

### Style Consistency

Ensure style consistency:

```python
# Check style consistency
consistency_score = assessor.check_style_consistency(
    image_path="output/generated_image.png",
    target_style="romantic"
)

# Adjust style if needed
if consistency_score < 0.8:
    result = generator.adjust_style(
        image_path="output/generated_image.png",
        target_style="romantic",
        adjustment_strength=0.5
    )
```

## File Management

### Input Management

Manage input images:

```python
from image.file_manager import ImageFileManager

file_manager = ImageFileManager()

# Organize input images
file_manager.organize_input_images(
    source_directory="image/input/",
    organization_type="by_category"
)

# Validate input images
validation_result = file_manager.validate_input_images(
    image_directory="image/input/",
    validation_criteria=["format", "size", "quality"]
)
```

### Output Management

Manage generated images:

```python
# Organize output images
file_manager.organize_output_images(
    output_directory="image/output/",
    organization_type="by_date_and_type"
)

# Clean old images
file_manager.clean_old_images(
    directory="image/output/",
    max_age_days=30
)

# Backup important images
file_manager.backup_images(
    source_directory="image/output/",
    backup_directory="image/backups/",
    backup_type="incremental"
)
```

## Future Enhancements

Planned improvements:

1. **Advanced Style Transfer**: More sophisticated style transfer capabilities
2. **Real-time Generation**: Real-time image generation and preview
3. **Interactive Editing**: Interactive image editing capabilities
4. **Style Learning**: Learn and adapt to user style preferences
5. **Batch Optimization**: Advanced batch processing and optimization
6. **Quality Prediction**: Predict image quality before generation

## Best Practices

### Generation
- Use clear, descriptive prompts
- Specify style and mood clearly
- Test different parameters for optimal results
- Cache frequently used images

### Processing
- Maintain image quality throughout processing
- Use appropriate formats for different uses
- Optimize file sizes for different platforms
- Backup important generated images

### Integration
- Ensure seamless integration with Discord
- Maintain consistent quality across systems
- Optimize for user experience
- Monitor performance and quality metrics

## Support

For image system support:

1. Check GPU availability and CUDA installation
2. Verify model loading and initialization
3. Test image generation with different prompts
4. Monitor quality and performance metrics
5. Review integration with other systems

The image system provides comprehensive image generation and processing capabilities for the AI writing companion, enabling rich visual content creation and integration with all multimodal features. 