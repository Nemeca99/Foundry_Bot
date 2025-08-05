#!/usr/bin/env python3
"""
Enhanced Image Generation System
Integrates with Stable Diffusion and other image generation models
"""

import os
import json
import time
import requests
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import numpy as np


class EnhancedImageGenerator:
    """Enhanced image generation with multiple model support"""

    def __init__(self):
        self.output_dir = Path("image/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize models
        self.stable_diffusion = None
        self.model_cache = {}
        self.style_presets = self._initialize_style_presets()
        
        # API configurations
        self.api_configs = {
            "stable_diffusion": {
                "url": "http://localhost:7860",
                "timeout": 30,
                "enabled": True
            },
            "openai_dalle": {
                "url": "https://api.openai.com/v1/images/generations",
                "timeout": 60,
                "enabled": False  # Requires API key
            }
        }

    def _initialize_style_presets(self) -> Dict:
        """Initialize style presets for different image types"""
        return {
            "romantic": {
                "prompt_modifier": "romantic, soft lighting, intimate, beautiful, high quality, detailed",
                "negative_prompt": "ugly, blurry, low quality, distorted",
                "guidance_scale": 7.5,
                "num_inference_steps": 50
            },
            "fantasy": {
                "prompt_modifier": "fantasy, magical, mystical, detailed, high quality, artistic",
                "negative_prompt": "realistic, mundane, blurry, low quality",
                "guidance_scale": 8.0,
                "num_inference_steps": 50
            },
            "modern": {
                "prompt_modifier": "modern, contemporary, clean, high quality, detailed, professional",
                "negative_prompt": "vintage, old, blurry, low quality",
                "guidance_scale": 7.0,
                "num_inference_steps": 40
            },
            "vintage": {
                "prompt_modifier": "vintage, retro, classic, detailed, high quality, nostalgic",
                "negative_prompt": "modern, contemporary, blurry, low quality",
                "guidance_scale": 7.5,
                "num_inference_steps": 50
            },
            "anime": {
                "prompt_modifier": "anime style, colorful, detailed, high quality, stylized",
                "negative_prompt": "realistic, blurry, low quality, distorted",
                "guidance_scale": 8.5,
                "num_inference_steps": 50
            },
            "realistic": {
                "prompt_modifier": "photorealistic, detailed, high quality, sharp focus",
                "negative_prompt": "cartoon, anime, blurry, low quality",
                "guidance_scale": 7.0,
                "num_inference_steps": 40
            },
            "artistic": {
                "prompt_modifier": "artistic, creative, beautiful, detailed, high quality, masterpiece",
                "negative_prompt": "ugly, blurry, low quality, amateur",
                "guidance_scale": 8.0,
                "num_inference_steps": 50
            },
            "default": {
                "prompt_modifier": "high quality, detailed, beautiful",
                "negative_prompt": "ugly, blurry, low quality",
                "guidance_scale": 7.5,
                "num_inference_steps": 50
            }
        }

    def load_stable_diffusion_model(self, model_name: str = "runwayml/stable-diffusion-v1-5") -> bool:
        """Load Stable Diffusion model locally"""
        try:
            print(f"Loading Stable Diffusion model: {model_name}")
            
            # Use DPMSolverMultistepScheduler for faster inference
            scheduler = DPMSolverMultistepScheduler.from_pretrained(
                model_name, 
                subfolder="scheduler"
            )
            
            self.stable_diffusion = StableDiffusionPipeline.from_pretrained(
                model_name,
                scheduler=scheduler,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            if torch.cuda.is_available():
                self.stable_diffusion = self.stable_diffusion.to("cuda")
                print("Model loaded on GPU")
            else:
                print("Model loaded on CPU")
            
            return True
            
        except Exception as e:
            print(f"Error loading Stable Diffusion model: {e}")
            return False

    def generate_image_with_stable_diffusion(
        self, 
        prompt: str, 
        style: str = "default",
        width: int = 512,
        height: int = 512,
        seed: Optional[int] = None
    ) -> Dict:
        """Generate image using local Stable Diffusion model"""
        
        if self.stable_diffusion is None:
            return {
                "success": False,
                "error": "Stable Diffusion model not loaded. Use load_stable_diffusion_model() first."
            }
        
        try:
            # Get style preset
            style_preset = self.style_presets.get(style, self.style_presets["default"])
            
            # Enhance prompt with style
            enhanced_prompt = f"{prompt}, {style_preset['prompt_modifier']}"
            
            # Set seed for reproducibility
            if seed is not None:
                torch.manual_seed(seed)
                if torch.cuda.is_available():
                    torch.cuda.manual_seed(seed)
            
            # Generate image
            result = self.stable_diffusion(
                prompt=enhanced_prompt,
                negative_prompt=style_preset["negative_prompt"],
                width=width,
                height=height,
                guidance_scale=style_preset["guidance_scale"],
                num_inference_steps=style_preset["num_inference_steps"],
                num_images_per_prompt=1
            )
            
            # Save image
            timestamp = int(time.time())
            filename = f"sd_generated_{timestamp}.png"
            filepath = self.output_dir / filename
            
            image = result.images[0]
            image.save(filepath)
            
            return {
                "success": True,
                "path": str(filepath),
                "prompt": enhanced_prompt,
                "style": style,
                "size": f"{width}x{height}",
                "seed": seed,
                "model": "stable_diffusion_local"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating image: {str(e)}"
            }

    def generate_image_with_api(
        self, 
        prompt: str, 
        style: str = "default",
        api_type: str = "stable_diffusion"
    ) -> Dict:
        """Generate image using API (Stable Diffusion WebUI, DALL-E, etc.)"""
        
        if api_type == "stable_diffusion":
            return self._generate_with_stable_diffusion_api(prompt, style)
        elif api_type == "openai_dalle":
            return self._generate_with_dalle_api(prompt, style)
        else:
            return {
                "success": False,
                "error": f"Unknown API type: {api_type}"
            }

    def _generate_with_stable_diffusion_api(self, prompt: str, style: str) -> Dict:
        """Generate image using Stable Diffusion WebUI API"""
        
        config = self.api_configs["stable_diffusion"]
        if not config["enabled"]:
            return {
                "success": False,
                "error": "Stable Diffusion API not enabled"
            }
        
        try:
            # Get style preset
            style_preset = self.style_presets.get(style, self.style_presets["default"])
            
            # Prepare API request
            payload = {
                "prompt": f"{prompt}, {style_preset['prompt_modifier']}",
                "negative_prompt": style_preset["negative_prompt"],
                "width": 512,
                "height": 512,
                "cfg_scale": style_preset["guidance_scale"],
                "steps": style_preset["num_inference_steps"],
                "sampler_name": "DPM++ 2M Karras"
            }
            
            # Make API request
            response = requests.post(
                f"{config['url']}/sdapi/v1/txt2img",
                json=payload,
                timeout=config["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Decode base64 image
                image_data = base64.b64decode(result["images"][0])
                
                # Save image
                timestamp = int(time.time())
                filename = f"sd_api_generated_{timestamp}.png"
                filepath = self.output_dir / filename
                
                with open(filepath, "wb") as f:
                    f.write(image_data)
                
                return {
                    "success": True,
                    "path": str(filepath),
                    "prompt": payload["prompt"],
                    "style": style,
                    "size": f"{payload['width']}x{payload['height']}",
                    "model": "stable_diffusion_api"
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code}"
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Could not connect to Stable Diffusion WebUI. Make sure it's running on localhost:7860"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating image: {str(e)}"
            }

    def _generate_with_dalle_api(self, prompt: str, style: str) -> Dict:
        """Generate image using OpenAI DALL-E API"""
        
        config = self.api_configs["openai_dalle"]
        if not config["enabled"]:
            return {
                "success": False,
                "error": "DALL-E API not enabled. Set OPENAI_API_KEY environment variable."
            }
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "OPENAI_API_KEY environment variable not set"
            }
        
        try:
            # Get style preset
            style_preset = self.style_presets.get(style, self.style_presets["default"])
            
            # Prepare API request
            payload = {
                "model": "dall-e-3",
                "prompt": f"{prompt}, {style_preset['prompt_modifier']}",
                "size": "1024x1024",
                "quality": "standard",
                "n": 1
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Make API request
            response = requests.post(
                config["url"],
                json=payload,
                headers=headers,
                timeout=config["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result["data"][0]["url"]
                
                # Download image
                image_response = requests.get(image_url)
                image_data = image_response.content
                
                # Save image
                timestamp = int(time.time())
                filename = f"dalle_generated_{timestamp}.png"
                filepath = self.output_dir / filename
                
                with open(filepath, "wb") as f:
                    f.write(image_data)
                
                return {
                    "success": True,
                    "path": str(filepath),
                    "prompt": payload["prompt"],
                    "style": style,
                    "size": payload["size"],
                    "model": "dall-e-3"
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating image: {str(e)}"
            }

    def generate_character_portrait(
        self, 
        character_name: str, 
        description: str, 
        style: str = "romantic"
    ) -> Dict:
        """Generate character portrait"""
        
        prompt = f"Portrait of {character_name}, {description}"
        return self.generate_image_with_stable_diffusion(prompt, style)

    def generate_story_cover(
        self, 
        title: str, 
        genre: str, 
        description: str = "",
        style: str = "artistic"
    ) -> Dict:
        """Generate book cover"""
        
        prompt = f"Book cover for '{title}', {genre} novel"
        if description:
            prompt += f", {description}"
        
        return self.generate_image_with_stable_diffusion(prompt, style, width=512, height=768)

    def generate_scene_image(
        self, 
        scene_description: str, 
        style: str = "realistic"
    ) -> Dict:
        """Generate scene image"""
        
        return self.generate_image_with_stable_diffusion(scene_description, style)

    def create_image_collage(
        self, 
        image_paths: List[str], 
        layout: str = "grid",
        output_filename: str = "collage.png"
    ) -> Dict:
        """Create image collage from multiple images"""
        
        try:
            images = []
            for path in image_paths:
                if os.path.exists(path):
                    img = Image.open(path)
                    # Resize to standard size
                    img = img.resize((256, 256))
                    images.append(img)
            
            if not images:
                return {
                    "success": False,
                    "error": "No valid images found"
                }
            
            # Create collage based on layout
            if layout == "grid":
                # Calculate grid dimensions
                n = len(images)
                cols = int(np.ceil(np.sqrt(n)))
                rows = int(np.ceil(n / cols))
                
                # Create canvas
                canvas_width = cols * 256
                canvas_height = rows * 256
                canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
                
                # Place images
                for i, img in enumerate(images):
                    row = i // cols
                    col = i % cols
                    x = col * 256
                    y = row * 256
                    canvas.paste(img, (x, y))
            
            elif layout == "horizontal":
                canvas_width = len(images) * 256
                canvas_height = 256
                canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
                
                for i, img in enumerate(images):
                    x = i * 256
                    canvas.paste(img, (x, 0))
            
            elif layout == "vertical":
                canvas_width = 256
                canvas_height = len(images) * 256
                canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
                
                for i, img in enumerate(images):
                    y = i * 256
                    canvas.paste(img, (0, y))
            
            # Save collage
            filepath = self.output_dir / output_filename
            canvas.save(filepath)
            
            return {
                "success": True,
                "path": str(filepath),
                "layout": layout,
                "num_images": len(images)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating collage: {str(e)}"
            }

    def get_available_styles(self) -> List[str]:
        """Get list of available styles"""
        return list(self.style_presets.keys())

    def get_model_status(self) -> Dict:
        """Get status of all models and APIs"""
        status = {
            "local_stable_diffusion": self.stable_diffusion is not None,
            "cuda_available": torch.cuda.is_available(),
            "api_configs": {}
        }
        
        for api_name, config in self.api_configs.items():
            status["api_configs"][api_name] = {
                "enabled": config["enabled"],
                "url": config["url"]
            }
        
        return status

    def test_api_connection(self, api_type: str = "stable_diffusion") -> Dict:
        """Test API connection"""
        
        if api_type == "stable_diffusion":
            config = self.api_configs["stable_diffusion"]
            try:
                response = requests.get(f"{config['url']}/sdapi/v1/progress", timeout=5)
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        return {
            "success": False,
            "error": f"Unknown API type: {api_type}"
        }


# Example usage
if __name__ == "__main__":
    generator = EnhancedImageGenerator()
    
    # Test local model loading
    print("Loading Stable Diffusion model...")
    success = generator.load_stable_diffusion_model()
    print(f"Model loaded: {success}")
    
    # Test image generation
    if success:
        result = generator.generate_image_with_stable_diffusion(
            "A beautiful sunset over the ocean",
            style="romantic"
        )
        print(f"Image generation result: {result}")
    
    # Test API connection
    api_status = generator.test_api_connection()
    print(f"API status: {api_status}")
    
    # Show available styles
    styles = generator.get_available_styles()
    print(f"Available styles: {styles}") 