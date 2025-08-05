#!/usr/bin/env python3
"""
Multimodal Orchestrator Plugin
Coordinates all media generation: text, voice, images, videos, sound clips
Integrates with Stable Diffusion and other multimodal models
"""

import os
import logging
import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
import requests
import base64
from PIL import Image
import io

logger = logging.getLogger(__name__)


class MultimodalOrchestrator:
    """Orchestrates all multimodal content generation"""

    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config
        
        # Initialize media generators
        self.image_generator = framework.get_plugin('image_generator')
        self.voice_generator = framework.get_plugin('voice_generator')
        self.video_generator = framework.get_plugin('video_generator')
        
        # Multimodal settings
        self.stable_diffusion_url = os.getenv("STABLE_DIFFUSION_URL", "http://localhost:7860")
        self.tts_url = os.getenv("TTS_URL", "http://localhost:5002")
        self.video_gen_url = os.getenv("VIDEO_GEN_URL", "http://localhost:7861")
        
        # Output directories
        self.output_dirs = {
            'image': Path(__file__).parent.parent.parent / "image" / "output",
            'voice': Path(__file__).parent.parent.parent / "voice" / "output", 
            'video': Path(__file__).parent.parent.parent / "video" / "output",
            'audio': Path(__file__).parent.parent.parent / "audio" / "output"
        }
        
        # Create output directories
        for dir_path in self.output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
            
        logger.info("✅ Multimodal Orchestrator initialized")

    async def generate_multimodal_content(self, 
                                        text_prompt: str,
                                        media_types: List[str] = None,
                                        style: str = "default",
                                        character_context: Dict = None) -> Dict[str, Any]:
        """Generate multiple types of media content based on a prompt"""
        
        if media_types is None:
            media_types = ["text", "image"]
            
        results = {}
        
        # Generate text response
        if "text" in media_types:
            results["text"] = await self._generate_text_response(text_prompt, character_context)
            
        # Generate image
        if "image" in media_types:
            results["image"] = await self._generate_image_with_stable_diffusion(text_prompt, style)
            
        # Generate voice
        if "voice" in media_types:
            results["voice"] = await self._generate_voice_with_tts(results.get("text", text_prompt), style)
            
        # Generate video
        if "video" in media_types:
            results["video"] = await self._generate_video_with_model(text_prompt, style)
            
        # Generate sound effects
        if "audio" in media_types:
            results["audio"] = await self._generate_sound_effects(text_prompt, style)
            
        return results

    async def _generate_text_response(self, prompt: str, character_context: Dict = None) -> str:
        """Generate text response using the prompt injection system"""
        try:
            # Import the prompt injection engine
            import sys
            sys.path.append(str(Path(__file__).parent.parent.parent / "astra_emotional_fragments"))
            from prompt_injection_engine import PromptInjectionEngine
            
            engine = PromptInjectionEngine()
            injection_result = engine.inject_emotional_context(prompt)
            
            # For now, return the injected prompt as the response
            # In a real implementation, this would be sent to the language model
            return injection_result['injected_prompt'][:500] + "..."
            
        except Exception as e:
            logger.error(f"Error generating text response: {e}")
            return f"Text response for: {prompt}"

    async def _generate_image_with_stable_diffusion(self, prompt: str, style: str = "default") -> Dict[str, Any]:
        """Generate image using Stable Diffusion API"""
        try:
            # Enhanced prompt for better image generation
            enhanced_prompt = self._enhance_image_prompt(prompt, style)
            
            # Stable Diffusion API call
            payload = {
                "prompt": enhanced_prompt,
                "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy",
                "steps": 20,
                "cfg_scale": 7.5,
                "width": 512,
                "height": 512,
                "sampler_name": "DPM++ 2M Karras"
            }
            
            response = requests.post(
                f"{self.stable_diffusion_url}/sdapi/v1/txt2img",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_data = base64.b64decode(result['images'][0])
                
                # Save image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = self.output_dirs['image'] / f"sd_generated_{timestamp}.png"
                
                with open(image_path, 'wb') as f:
                    f.write(image_data)
                
                return {
                    "success": True,
                    "path": str(image_path),
                    "prompt": enhanced_prompt,
                    "size": (512, 512)
                }
            else:
                logger.error(f"Stable Diffusion API error: {response.status_code}")
                return {"success": False, "error": f"API error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Error generating image with Stable Diffusion: {e}")
            return {"success": False, "error": str(e)}

    async def _generate_voice_with_tts(self, text: str, style: str = "default") -> Dict[str, Any]:
        """Generate voice using TTS model"""
        try:
            # Enhanced text for voice generation
            enhanced_text = self._enhance_voice_text(text, style)
            
            # TTS API call (placeholder for now)
            # In a real implementation, this would call your TTS model
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = self.output_dirs['voice'] / f"tts_generated_{timestamp}.wav"
            
            # Placeholder: create a dummy audio file
            with open(audio_path, 'w') as f:
                f.write("Placeholder audio file")
            
            return {
                "success": True,
                "path": str(audio_path),
                "text": enhanced_text,
                "duration": "10s"  # placeholder
            }
            
        except Exception as e:
            logger.error(f"Error generating voice: {e}")
            return {"success": False, "error": str(e)}

    async def _generate_video_with_model(self, prompt: str, style: str = "default") -> Dict[str, Any]:
        """Generate video using video generation model"""
        try:
            # Enhanced prompt for video generation
            enhanced_prompt = self._enhance_video_prompt(prompt, style)
            
            # Video generation API call (placeholder)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = self.output_dirs['video'] / f"video_generated_{timestamp}.mp4"
            
            # Placeholder: create a dummy video file
            with open(video_path, 'w') as f:
                f.write("Placeholder video file")
            
            return {
                "success": True,
                "path": str(video_path),
                "prompt": enhanced_prompt,
                "duration": "15s"  # placeholder
            }
            
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            return {"success": False, "error": str(e)}

    async def _generate_sound_effects(self, prompt: str, style: str = "default") -> Dict[str, Any]:
        """Generate sound effects based on prompt"""
        try:
            # Enhanced prompt for sound generation
            enhanced_prompt = self._enhance_sound_prompt(prompt, style)
            
            # Sound generation (placeholder)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = self.output_dirs['audio'] / f"sound_effect_{timestamp}.wav"
            
            # Placeholder: create a dummy sound file
            with open(audio_path, 'w') as f:
                f.write("Placeholder sound effect file")
            
            return {
                "success": True,
                "path": str(audio_path),
                "prompt": enhanced_prompt,
                "type": "sound_effect"
            }
            
        except Exception as e:
            logger.error(f"Error generating sound effects: {e}")
            return {"success": False, "error": str(e)}

    def _enhance_image_prompt(self, prompt: str, style: str) -> str:
        """Enhance prompt for better image generation"""
        style_enhancements = {
            "romantic": "romantic, intimate, soft lighting, beautiful, high quality, detailed",
            "fantasy": "fantasy, magical, mystical, detailed, high quality, artistic",
            "modern": "modern, contemporary, clean, high quality, detailed",
            "vintage": "vintage, retro, classic, high quality, detailed",
            "anime": "anime style, detailed, high quality, colorful",
            "realistic": "realistic, photorealistic, detailed, high quality",
            "artistic": "artistic, creative, detailed, high quality, beautiful",
            "default": "high quality, detailed, beautiful"
        }
        
        enhancement = style_enhancements.get(style, style_enhancements["default"])
        return f"{prompt}, {enhancement}"

    def _enhance_voice_text(self, text: str, style: str) -> str:
        """Enhance text for voice generation"""
        style_enhancements = {
            "romantic": "Speaking in a romantic, intimate tone",
            "dramatic": "Speaking with dramatic emphasis and emotion",
            "calm": "Speaking in a calm, soothing voice",
            "energetic": "Speaking with energy and enthusiasm",
            "mysterious": "Speaking in a mysterious, intriguing tone",
            "default": "Speaking naturally and clearly"
        }
        
        enhancement = style_enhancements.get(style, style_enhancements["default"])
        return f"{enhancement}: {text}"

    def _enhance_video_prompt(self, prompt: str, style: str) -> str:
        """Enhance prompt for video generation"""
        style_enhancements = {
            "romantic": "romantic scene, soft lighting, intimate, high quality video",
            "dramatic": "dramatic scene, intense lighting, emotional, high quality video",
            "fantasy": "fantasy scene, magical effects, mystical, high quality video",
            "modern": "modern scene, contemporary setting, high quality video",
            "default": "high quality video, smooth motion, detailed"
        }
        
        enhancement = style_enhancements.get(style, style_enhancements["default"])
        return f"{prompt}, {enhancement}"

    def _enhance_sound_prompt(self, prompt: str, style: str) -> str:
        """Enhance prompt for sound generation"""
        style_enhancements = {
            "romantic": "romantic atmosphere, soft ambient sounds",
            "dramatic": "dramatic sound effects, intense audio",
            "calm": "calm, peaceful ambient sounds",
            "energetic": "energetic, dynamic sound effects",
            "mysterious": "mysterious, atmospheric sounds",
            "default": "appropriate sound effects for the scene"
        }
        
        enhancement = style_enhancements.get(style, style_enhancements["default"])
        return f"{prompt}, {enhancement}"

    async def create_character_multimedia(self, 
                                        character_name: str,
                                        character_data: Dict,
                                        media_types: List[str] = None) -> Dict[str, Any]:
        """Create multimedia content for a specific character"""
        
        if media_types is None:
            media_types = ["image", "voice", "text"]
            
        # Create character-specific prompts
        image_prompt = f"Portrait of {character_name}, {character_data.get('description', '')}"
        voice_text = f"Hello, I am {character_name}. {character_data.get('voice_description', '')}"
        
        results = {}
        
        # Generate character image
        if "image" in media_types:
            results["character_image"] = await self._generate_image_with_stable_diffusion(
                image_prompt, character_data.get('style', 'default')
            )
            
        # Generate character voice sample
        if "voice" in media_types:
            results["character_voice"] = await self._generate_voice_with_tts(
                voice_text, character_data.get('voice_style', 'default')
            )
            
        # Generate character description
        if "text" in media_types:
            results["character_text"] = await self._generate_text_response(
                f"Describe {character_name} in detail", character_data
            )
            
        return results

    async def create_story_multimedia(self, 
                                     story_title: str,
                                     story_data: Dict,
                                     media_types: List[str] = None) -> Dict[str, Any]:
        """Create multimedia content for a story"""
        
        if media_types is None:
            media_types = ["image", "video", "text"]
            
        results = {}
        
        # Generate story cover image
        if "image" in media_types:
            cover_prompt = f"Book cover for '{story_title}', {story_data.get('genre', '')} genre"
            results["story_cover"] = await self._generate_image_with_stable_diffusion(
                cover_prompt, story_data.get('style', 'default')
            )
            
        # Generate story trailer video
        if "video" in media_types:
            trailer_prompt = f"Book trailer for '{story_title}', {story_data.get('description', '')}"
            results["story_trailer"] = await self._generate_video_with_model(
                trailer_prompt, story_data.get('style', 'default')
            )
            
        # Generate story summary
        if "text" in media_types:
            results["story_summary"] = await self._generate_text_response(
                f"Summarize the story '{story_title}'", story_data
            )
            
        return results

    def get_available_media_types(self) -> List[str]:
        """Get list of available media generation types"""
        return ["text", "image", "voice", "video", "audio"]

    def get_available_styles(self) -> Dict[str, List[str]]:
        """Get available styles for each media type"""
        return {
            "image": ["romantic", "fantasy", "modern", "vintage", "anime", "realistic", "artistic", "default"],
            "voice": ["romantic", "dramatic", "calm", "energetic", "mysterious", "default"],
            "video": ["romantic", "dramatic", "fantasy", "modern", "default"],
            "audio": ["romantic", "dramatic", "calm", "energetic", "mysterious", "default"]
        }

    async def test_multimodal_system(self) -> Dict[str, Any]:
        """Test the multimodal system with sample content"""
        
        test_prompt = "A romantic sunset scene with two lovers"
        
        results = await self.generate_multimodal_content(
            text_prompt=test_prompt,
            media_types=["text", "image", "voice"],
            style="romantic"
        )
        
        return {
            "test_prompt": test_prompt,
            "results": results,
            "status": "Test completed"
        }


def initialize(framework) -> MultimodalOrchestrator:
    """Initialize the multimodal orchestrator plugin"""
    return MultimodalOrchestrator(framework) 