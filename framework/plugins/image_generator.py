#!/usr/bin/env python3
"""
BULMA HEADER PROTOCOL - FRAMEWORK/PLUGINS/IMAGE_GENERATOR_MERGED.PY
====================================================================

FILE IDENTITY:
- Name: Merged Image Generator Plugin for Authoring Bot
- Role: Handles book cover and illustration generation with enhanced capabilities
- Purpose: Generates images for authoring projects with multiple model support
- Location: framework/plugins/image_generator_merged.py (Merged image generation plugin)

BULMA USAGE PATTERNS:
- READ FIRST: This plugin handles all image generation for authoring
- MODIFICATIONS: Changes here affect image quality and style
- TESTING: Test image generation with various prompts and styles
- INTEGRATION: Works with local image generation models and APIs

KEY COMPONENTS:
1. ImageGenerator - Main image generation class
2. BookCoverGenerator - Specialized book cover creation
3. CharacterArtGenerator - Character illustration generation
4. SceneIllustrationGenerator - Scene and setting illustrations
5. Style Management - Different artistic styles and genres
6. Enhanced API Support - Multiple image generation APIs
7. Stable Diffusion Integration - Local model support

BULMA RESTRICTIONS:
- DO NOT modify image generation without testing quality
- DO NOT change style parameters without visual testing
- ALWAYS test generated images for appropriateness
- CHECK that image styles match project genres
- VERIFY image resolution and quality standards

ALWAYS READ THIS HEADER BEFORE MODIFYING THIS FILE.
This plugin is critical for visual authoring content.
"""

import os
import json
import time
import requests
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import logging

# Optional imports for enhanced functionality
try:
    import torch
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
    import numpy as np

    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False

logger = logging.getLogger(__name__)


class ImageGenerator:
    """Enhanced image generation plugin for authoring bot with multiple model support"""

    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config

        # Image generation settings
        self.image_styles = self._load_image_styles()
        self.output_dir = Path(__file__).parent.parent.parent / "image" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Enhanced functionality
        self.stable_diffusion = None
        self.model_cache = {}
        self.style_presets = self._initialize_style_presets()

        # API configurations
        self.api_configs = {
            "stable_diffusion": {
                "url": "http://localhost:7860",
                "timeout": 30,
                "enabled": True,
            },
            "openai_dalle": {
                "url": "https://api.openai.com/v1/images/generations",
                "timeout": 60,
                "enabled": False,  # Requires API key
            },
        }

        logger.info("✅ Merged Image Generator plugin initialized")

    def _load_image_styles(self) -> Dict[str, Dict[str, Any]]:
        """Load image generation styles for different genres"""
        return {
            "book_cover": {
                "fantasy": "epic fantasy book cover, detailed, professional, high quality, 4k",
                "romance": "romantic book cover, elegant, emotional, professional, high quality",
                "mystery": "mysterious book cover, dark atmosphere, suspenseful, professional",
                "scifi": "science fiction book cover, futuristic, technological, professional",
                "horror": "horror book cover, dark, frightening, atmospheric, professional",
                "young_adult": "young adult book cover, modern, relatable, engaging, professional",
                "historical": "historical book cover, period accurate, detailed, professional",
                "thriller": "thriller book cover, intense, action-packed, professional",
                "default": "professional book cover, high quality, detailed, 4k",
            },
            "character_art": {
                "fantasy": "fantasy character portrait, detailed, expressive, high quality",
                "modern": "modern character portrait, realistic, expressive, high quality",
                "anime": "anime character portrait, stylized, expressive, high quality",
                "cartoon": "cartoon character portrait, stylized, expressive, high quality",
                "default": "character portrait, detailed, expressive, high quality",
            },
            "scene_illustration": {
                "fantasy": "fantasy scene illustration, detailed, atmospheric, high quality",
                "modern": "modern scene illustration, realistic, atmospheric, high quality",
                "scifi": "science fiction scene illustration, futuristic, detailed, high quality",
                "historical": "historical scene illustration, period accurate, detailed, high quality",
                "default": "scene illustration, detailed, atmospheric, high quality",
            },
        }

    def _initialize_style_presets(self) -> Dict:
        """Initialize enhanced style presets for different image types"""
        return {
            "romantic": {
                "prompt_modifier": "romantic, soft lighting, intimate, beautiful, high quality, detailed",
                "negative_prompt": "ugly, blurry, low quality, distorted",
                "guidance_scale": 7.5,
                "num_inference_steps": 50,
            },
            "fantasy": {
                "prompt_modifier": "fantasy, magical, mystical, detailed, high quality, artistic",
                "negative_prompt": "realistic, mundane, blurry, low quality",
                "guidance_scale": 8.0,
                "num_inference_steps": 50,
            },
            "modern": {
                "prompt_modifier": "modern, contemporary, clean, high quality, detailed, professional",
                "negative_prompt": "vintage, old, blurry, low quality",
                "guidance_scale": 7.0,
                "num_inference_steps": 40,
            },
            "vintage": {
                "prompt_modifier": "vintage, retro, classic, detailed, high quality, nostalgic",
                "negative_prompt": "modern, contemporary, blurry, low quality",
                "guidance_scale": 7.5,
                "num_inference_steps": 50,
            },
            "anime": {
                "prompt_modifier": "anime style, colorful, detailed, high quality, stylized",
                "negative_prompt": "realistic, blurry, low quality, distorted",
                "guidance_scale": 8.5,
                "num_inference_steps": 50,
            },
            "realistic": {
                "prompt_modifier": "photorealistic, detailed, high quality, sharp focus",
                "negative_prompt": "cartoon, anime, blurry, low quality",
                "guidance_scale": 7.0,
                "num_inference_steps": 40,
            },
            "artistic": {
                "prompt_modifier": "artistic, creative, beautiful, detailed, high quality, masterpiece",
                "negative_prompt": "ugly, blurry, low quality, amateur",
                "guidance_scale": 8.0,
                "num_inference_steps": 50,
            },
            "default": {
                "prompt_modifier": "high quality, detailed, beautiful",
                "negative_prompt": "ugly, blurry, low quality",
                "guidance_scale": 7.5,
                "num_inference_steps": 50,
            },
        }

    def generate_image(self, prompt: str, style: str = "book_cover") -> str:
        """Generate an image using the specified style (basic functionality)"""
        try:
            # Enhance prompt with style information
            enhanced_prompt = self._enhance_prompt(prompt, style)

            # Try enhanced generation first, fallback to basic
            if ENHANCED_AVAILABLE and self.api_configs["stable_diffusion"]["enabled"]:
                result = self.generate_image_with_api(
                    enhanced_prompt, style, "stable_diffusion"
                )
                if result.get("success"):
                    return result["image_path"]

            # Fallback to basic generation
            image_path = self._generate_image_placeholder(enhanced_prompt, style)
            logger.info(f"✅ Generated image: {image_path}")
            return f"Image generated: {image_path}"

        except Exception as e:
            logger.error(f"❌ Failed to generate image: {e}")
            return f"Image generation failed: {e}"

    def _enhance_prompt(self, prompt: str, style: str) -> str:
        """Enhance prompt with style information"""
        if style in self.image_styles.get("book_cover", {}):
            style_prompt = self.image_styles["book_cover"][style]
            return f"{prompt}, {style_prompt}"
        return prompt

    def _generate_image_placeholder(self, prompt: str, style: str) -> str:
        """Generate a placeholder image (basic functionality)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{style}_{timestamp}.png"
        image_path = self.output_dir / filename

        # Create a simple placeholder image
        img = Image.new("RGB", (512, 512), color="lightblue")
        draw = ImageDraw.Draw(img)

        # Add text to placeholder
        try:
            font = ImageFont.load_default()
        except:
            font = None

        # Split prompt into lines
        words = prompt.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + word) < 30:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())

        # Draw text
        y_position = 50
        for line in lines[:5]:  # Limit to 5 lines
            draw.text((50, y_position), line, fill="black", font=font)
            y_position += 30

        img.save(image_path)
        return str(image_path)

    def generate_book_cover(self, project_name: str, description: str) -> str:
        """Generate a book cover for a project"""
        prompt = f"Book cover for '{project_name}': {description}"
        return self.generate_image(prompt, "book_cover")

    def generate_character_art(
        self, character_name: str, character_description: str, style: str = "default"
    ) -> str:
        """Generate character art"""
        prompt = f"Character portrait of {character_name}: {character_description}"
        return self.generate_image(prompt, "character_art")

    def generate_scene_illustration(
        self, scene_description: str, style: str = "default"
    ) -> str:
        """Generate scene illustration"""
        prompt = f"Scene illustration: {scene_description}"
        return self.generate_image(prompt, "scene_illustration")

    # Enhanced functionality methods
    def load_stable_diffusion_model(
        self, model_name: str = "runwayml/stable-diffusion-v1-5"
    ) -> bool:
        """Load Stable Diffusion model locally"""
        if not ENHANCED_AVAILABLE:
            logger.warning(
                "Enhanced functionality not available (torch/diffusers not installed)"
            )
            return False

        try:
            if model_name not in self.model_cache:
                logger.info(f"Loading Stable Diffusion model: {model_name}")
                self.stable_diffusion = StableDiffusionPipeline.from_pretrained(
                    model_name,
                    torch_dtype=(
                        torch.float16 if torch.cuda.is_available() else torch.float32
                    ),
                )

                if torch.cuda.is_available():
                    self.stable_diffusion = self.stable_diffusion.to("cuda")

                self.stable_diffusion.scheduler = (
                    DPMSolverMultistepScheduler.from_config(
                        self.stable_diffusion.scheduler.config
                    )
                )

                self.model_cache[model_name] = self.stable_diffusion
                logger.info("✅ Stable Diffusion model loaded successfully")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to load Stable Diffusion model: {e}")
            return False

    def generate_image_with_stable_diffusion(
        self,
        prompt: str,
        style: str = "default",
        width: int = 512,
        height: int = 512,
        seed: Optional[int] = None,
    ) -> Dict:
        """Generate image using Stable Diffusion locally"""
        if not ENHANCED_AVAILABLE or not self.stable_diffusion:
            return {"success": False, "error": "Stable Diffusion not available"}

        try:
            # Get style preset
            style_preset = self.style_presets.get(style, self.style_presets["default"])

            # Enhance prompt
            enhanced_prompt = f"{prompt}, {style_preset['prompt_modifier']}"

            # Generate image
            generator = torch.Generator(
                device="cuda" if torch.cuda.is_available() else "cpu"
            )
            if seed:
                generator.manual_seed(seed)

            image = self.stable_diffusion(
                prompt=enhanced_prompt,
                negative_prompt=style_preset["negative_prompt"],
                guidance_scale=style_preset["guidance_scale"],
                num_inference_steps=style_preset["num_inference_steps"],
                width=width,
                height=height,
                generator=generator,
            ).images[0]

            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sd_generated_{style}_{timestamp}.png"
            image_path = self.output_dir / filename
            image.save(image_path)

            return {
                "success": True,
                "image_path": str(image_path),
                "prompt": enhanced_prompt,
                "style": style,
                "seed": seed,
            }

        except Exception as e:
            logger.error(f"❌ Stable Diffusion generation failed: {e}")
            return {"success": False, "error": str(e)}

    def generate_image_with_api(
        self, prompt: str, style: str = "default", api_type: str = "stable_diffusion"
    ) -> Dict:
        """Generate image using API"""
        if api_type == "stable_diffusion":
            return self._generate_with_stable_diffusion_api(prompt, style)
        elif api_type == "openai_dalle":
            return self._generate_with_dalle_api(prompt, style)
        else:
            return {"success": False, "error": f"Unknown API type: {api_type}"}

    def _generate_with_stable_diffusion_api(self, prompt: str, style: str) -> Dict:
        """Generate image using Stable Diffusion API"""
        try:
            style_preset = self.style_presets.get(style, self.style_presets["default"])
            enhanced_prompt = f"{prompt}, {style_preset['prompt_modifier']}"

            payload = {
                "prompt": enhanced_prompt,
                "negative_prompt": style_preset["negative_prompt"],
                "guidance_scale": style_preset["guidance_scale"],
                "num_inference_steps": style_preset["num_inference_steps"],
                "width": 512,
                "height": 512,
            }

            response = requests.post(
                f"{self.api_configs['stable_diffusion']['url']}/sdapi/v1/txt2img",
                json=payload,
                timeout=self.api_configs["stable_diffusion"]["timeout"],
            )

            if response.status_code == 200:
                result = response.json()
                image_data = base64.b64decode(result["images"][0])

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sd_api_{style}_{timestamp}.png"
                image_path = self.output_dir / filename

                with open(image_path, "wb") as f:
                    f.write(image_data)

                return {
                    "success": True,
                    "image_path": str(image_path),
                    "prompt": enhanced_prompt,
                    "style": style,
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}

        except Exception as e:
            logger.error(f"❌ Stable Diffusion API generation failed: {e}")
            return {"success": False, "error": str(e)}

    def _generate_with_dalle_api(self, prompt: str, style: str) -> Dict:
        """Generate image using OpenAI DALL-E API"""
        # This would require OpenAI API key
        return {"success": False, "error": "DALL-E API not configured"}

    def generate_character_portrait(
        self, character_name: str, description: str, style: str = "romantic"
    ) -> Dict:
        """Generate character portrait with enhanced capabilities"""
        prompt = f"Character portrait of {character_name}: {description}"
        return self.generate_image_with_api(prompt, style, "stable_diffusion")

    def generate_story_cover(
        self, title: str, genre: str, description: str = "", style: str = "artistic"
    ) -> Dict:
        """Generate story cover with enhanced capabilities"""
        prompt = f"Book cover for '{title}': {description}"
        return self.generate_image_with_api(prompt, style, "stable_diffusion")

    def generate_scene_image(
        self, scene_description: str, style: str = "realistic"
    ) -> Dict:
        """Generate scene image with enhanced capabilities"""
        prompt = f"Scene illustration: {scene_description}"
        return self.generate_image_with_api(prompt, style, "stable_diffusion")

    def get_available_styles(self) -> Dict[str, List[str]]:
        """Get available styles for different image types"""
        return {
            "book_cover": list(self.image_styles["book_cover"].keys()),
            "character_art": list(self.image_styles["character_art"].keys()),
            "scene_illustration": list(self.image_styles["scene_illustration"].keys()),
            "enhanced_styles": list(self.style_presets.keys()),
        }

    def get_model_status(self) -> Dict:
        """Get status of available models and APIs"""
        return {
            "enhanced_available": ENHANCED_AVAILABLE,
            "stable_diffusion_local": self.stable_diffusion is not None,
            "stable_diffusion_api": self.api_configs["stable_diffusion"]["enabled"],
            "dalle_api": self.api_configs["openai_dalle"]["enabled"],
            "cuda_available": (
                torch.cuda.is_available() if ENHANCED_AVAILABLE else False
            ),
        }

    def test_api_connection(self, api_type: str = "stable_diffusion") -> Dict:
        """Test API connection"""
        try:
            if api_type == "stable_diffusion":
                response = requests.get(
                    f"{self.api_configs['stable_diffusion']['url']}/sdapi/v1/progress",
                    timeout=5,
                )
                return {"success": response.status_code == 200}
            else:
                return {"success": False, "error": f"Unknown API type: {api_type}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


def initialize(framework) -> ImageGenerator:
    """Initialize the merged image generator plugin"""
    return ImageGenerator(framework)
