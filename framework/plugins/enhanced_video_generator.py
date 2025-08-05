#!/usr/bin/env python3
"""
Enhanced Video Generation System
Integrates with multiple video generation models and APIs for high-quality video creation
"""

import os
import json
import time
import requests
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, ImageClip
from moviepy.video.fx import resize, crop
import pygame


class EnhancedVideoGenerator:
    """Enhanced video generation with multiple model support"""

    def __init__(self):
        self.output_dir = Path("video/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize video generation models
        self.video_presets = self._initialize_video_presets()
        self.available_models = {}
        
        # API configurations
        self.api_configs = {
            "runway_ml": {
                "url": "https://api.runwayml.com/v1/inference",
                "timeout": 120,
                "enabled": False  # Requires API key
            },
            "replicate": {
                "url": "https://api.replicate.com/v1/predictions",
                "timeout": 180,
                "enabled": False  # Requires API key
            },
            "stability_ai": {
                "url": "https://api.stability.ai/v1/generation/stable-video-diffusion",
                "timeout": 120,
                "enabled": False  # Requires API key
            }
        }
        
        # Initialize pygame for video playback
        pygame.init()

    def _initialize_video_presets(self) -> Dict:
        """Initialize video presets for different content types"""
        return {
            "romantic": {
                "style": "romantic, soft lighting, intimate, beautiful",
                "duration": 10,
                "fps": 24,
                "resolution": (1920, 1080),
                "description": "Romantic and intimate video style",
                "characteristics": ["soft", "intimate", "beautiful", "warm"]
            },
            "fantasy": {
                "style": "fantasy, magical, mystical, detailed",
                "duration": 15,
                "fps": 30,
                "resolution": (1920, 1080),
                "description": "Fantasy and magical video style",
                "characteristics": ["magical", "mystical", "detailed", "artistic"]
            },
            "modern": {
                "style": "modern, contemporary, clean, professional",
                "duration": 8,
                "fps": 24,
                "resolution": (1920, 1080),
                "description": "Modern and contemporary video style",
                "characteristics": ["clean", "professional", "contemporary", "sleek"]
            },
            "vintage": {
                "style": "vintage, retro, classic, nostalgic",
                "duration": 12,
                "fps": 24,
                "resolution": (1920, 1080),
                "description": "Vintage and retro video style",
                "characteristics": ["vintage", "retro", "classic", "nostalgic"]
            },
            "anime": {
                "style": "anime style, colorful, detailed, stylized",
                "duration": 10,
                "fps": 30,
                "resolution": (1920, 1080),
                "description": "Anime-style video",
                "characteristics": ["colorful", "stylized", "detailed", "anime"]
            },
            "realistic": {
                "style": "photorealistic, detailed, high quality, sharp focus",
                "duration": 10,
                "fps": 24,
                "resolution": (1920, 1080),
                "description": "Realistic video style",
                "characteristics": ["realistic", "detailed", "sharp", "natural"]
            },
            "artistic": {
                "style": "artistic, creative, beautiful, detailed, masterpiece",
                "duration": 15,
                "fps": 30,
                "resolution": (1920, 1080),
                "description": "Artistic and creative video style",
                "characteristics": ["artistic", "creative", "beautiful", "masterpiece"]
            },
            "default": {
                "style": "high quality, detailed, beautiful",
                "duration": 10,
                "fps": 24,
                "resolution": (1920, 1080),
                "description": "Default video style",
                "characteristics": ["high_quality", "detailed", "beautiful"]
            }
        }

    def generate_video_from_images(
        self, 
        image_paths: List[str], 
        style: str = "default",
        output_filename: str = None
    ) -> Dict:
        """Generate video from a sequence of images"""
        
        try:
            if not image_paths:
                return {
                    "success": False,
                    "error": "No image paths provided"
                }
            
            # Get video preset
            preset = self.video_presets.get(style, self.video_presets["default"])
            
            # Generate filename if not provided
            if output_filename is None:
                timestamp = int(time.time())
                output_filename = f"image_sequence_{timestamp}.mp4"
            
            filepath = self.output_dir / output_filename
            
            # Create video from images
            clips = []
            for image_path in image_paths:
                if os.path.exists(image_path):
                    # Create image clip
                    img_clip = ImageClip(image_path, duration=preset["duration"] / len(image_paths))
                    img_clip = img_clip.resize(preset["resolution"])
                    clips.append(img_clip)
            
            if not clips:
                return {
                    "success": False,
                    "error": "No valid images found"
                }
            
            # Concatenate clips
            final_clip = CompositeVideoClip(clips)
            
            # Write video file
            final_clip.write_videofile(
                str(filepath),
                fps=preset["fps"],
                codec='libx264',
                audio_codec='aac'
            )
            
            return {
                "success": True,
                "path": str(filepath),
                "style": style,
                "num_images": len(clips),
                "duration": preset["duration"],
                "resolution": preset["resolution"],
                "fps": preset["fps"],
                "engine": "moviepy_image_sequence"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating video from images: {str(e)}"
            }

    def generate_video_with_api(
        self, 
        prompt: str, 
        style: str = "default",
        api_type: str = "runway_ml"
    ) -> Dict:
        """Generate video using external APIs"""
        
        if api_type == "runway_ml":
            return self._generate_with_runway_ml_api(prompt, style)
        elif api_type == "replicate":
            return self._generate_with_replicate_api(prompt, style)
        elif api_type == "stability_ai":
            return self._generate_with_stability_ai_api(prompt, style)
        else:
            return {
                "success": False,
                "error": f"Unknown API type: {api_type}"
            }

    def _generate_with_runway_ml_api(self, prompt: str, style: str) -> Dict:
        """Generate video using Runway ML API"""
        
        config = self.api_configs["runway_ml"]
        if not config["enabled"]:
            return {
                "success": False,
                "error": "Runway ML API not enabled. Set RUNWAY_API_KEY environment variable."
            }
        
        api_key = os.getenv("RUNWAY_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "RUNWAY_API_KEY environment variable not set"
            }
        
        try:
            # Get video preset
            preset = self.video_presets.get(style, self.video_presets["default"])
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": f"{prompt}, {preset['style']}",
                "duration": preset["duration"],
                "fps": preset["fps"],
                "resolution": f"{preset['resolution'][0]}x{preset['resolution'][1]}"
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
                
                # Download video file
                video_url = result.get("video_url")
                if video_url:
                    video_response = requests.get(video_url)
                    video_data = video_response.content
                    
                    # Save video file
                    timestamp = int(time.time())
                    filename = f"runway_ml_generated_{timestamp}.mp4"
                    filepath = self.output_dir / filename
                    
                    with open(filepath, "wb") as f:
                        f.write(video_data)
                    
                    return {
                        "success": True,
                        "path": str(filepath),
                        "prompt": payload["prompt"],
                        "style": style,
                        "duration": preset["duration"],
                        "resolution": preset["resolution"],
                        "fps": preset["fps"],
                        "engine": "runway_ml"
                    }
                else:
                    return {
                        "success": False,
                        "error": "No video URL in response"
                    }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating video with Runway ML: {str(e)}"
            }

    def _generate_with_replicate_api(self, prompt: str, style: str) -> Dict:
        """Generate video using Replicate API"""
        
        config = self.api_configs["replicate"]
        if not config["enabled"]:
            return {
                "success": False,
                "error": "Replicate API not enabled. Set REPLICATE_API_TOKEN environment variable."
            }
        
        api_token = os.getenv("REPLICATE_API_TOKEN")
        if not api_token:
            return {
                "success": False,
                "error": "REPLICATE_API_TOKEN environment variable not set"
            }
        
        try:
            # Get video preset
            preset = self.video_presets.get(style, self.video_presets["default"])
            
            # Prepare API request
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "version": "a00d0b7a9f908351a96a9da65a1eab6d6f5b43f4f0b3a3f3a3f3a3f3a3f3a3f3a",
                "input": {
                    "prompt": f"{prompt}, {preset['style']}",
                    "num_frames": preset["duration"] * preset["fps"],
                    "fps": preset["fps"]
                }
            }
            
            # Make API request
            response = requests.post(
                config["url"],
                json=payload,
                headers=headers,
                timeout=config["timeout"]
            )
            
            if response.status_code == 201:
                result = response.json()
                prediction_id = result["id"]
                
                # Poll for completion
                while True:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_result = status_response.json()
                        
                        if status_result["status"] == "succeeded":
                            video_url = status_result["output"]
                            
                            # Download video file
                            video_response = requests.get(video_url)
                            video_data = video_response.content
                            
                            # Save video file
                            timestamp = int(time.time())
                            filename = f"replicate_generated_{timestamp}.mp4"
                            filepath = self.output_dir / filename
                            
                            with open(filepath, "wb") as f:
                                f.write(video_data)
                            
                            return {
                                "success": True,
                                "path": str(filepath),
                                "prompt": payload["input"]["prompt"],
                                "style": style,
                                "duration": preset["duration"],
                                "resolution": preset["resolution"],
                                "fps": preset["fps"],
                                "engine": "replicate"
                            }
                        elif status_result["status"] == "failed":
                            return {
                                "success": False,
                                "error": f"Video generation failed: {status_result.get('error', 'Unknown error')}"
                            }
                        else:
                            time.sleep(5)  # Wait before polling again
                    else:
                        return {
                            "success": False,
                            "error": f"Status check failed: {status_response.status_code}"
                        }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating video with Replicate: {str(e)}"
            }

    def _generate_with_stability_ai_api(self, prompt: str, style: str) -> Dict:
        """Generate video using Stability AI API"""
        
        config = self.api_configs["stability_ai"]
        if not config["enabled"]:
            return {
                "success": False,
                "error": "Stability AI API not enabled. Set STABILITY_API_KEY environment variable."
            }
        
        api_key = os.getenv("STABILITY_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "STABILITY_API_KEY environment variable not set"
            }
        
        try:
            # Get video preset
            preset = self.video_presets.get(style, self.video_presets["default"])
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "text_prompts": [
                    {
                        "text": f"{prompt}, {preset['style']}",
                        "weight": 1.0
                    }
                ],
                "cfg_scale": 7.5,
                "motion_bucket_id": 127,
                "width": preset["resolution"][0],
                "height": preset["resolution"][1]
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
                
                # Download video file
                video_data = base64.b64decode(result["artifacts"][0]["base64"])
                
                # Save video file
                timestamp = int(time.time())
                filename = f"stability_ai_generated_{timestamp}.mp4"
                filepath = self.output_dir / filename
                
                with open(filepath, "wb") as f:
                    f.write(video_data)
                
                return {
                    "success": True,
                    "path": str(filepath),
                    "prompt": payload["text_prompts"][0]["text"],
                    "style": style,
                    "duration": preset["duration"],
                    "resolution": preset["resolution"],
                    "fps": preset["fps"],
                    "engine": "stability_ai"
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating video with Stability AI: {str(e)}"
            }

    def create_character_video(
        self, 
        character_name: str,
        character_description: str,
        style: str = "romantic",
        duration: int = 10
    ) -> Dict:
        """Generate character video"""
        
        prompt = f"Video of {character_name}, {character_description}"
        return self.generate_video_with_api(prompt, style)

    def create_story_scene_video(
        self, 
        scene_description: str,
        style: str = "realistic",
        duration: int = 15
    ) -> Dict:
        """Generate story scene video"""
        
        return self.generate_video_with_api(scene_description, style)

    def create_video_with_audio(
        self, 
        video_path: str, 
        audio_path: str,
        output_filename: str = None
    ) -> Dict:
        """Combine video with audio"""
        
        try:
            if not os.path.exists(video_path):
                return {
                    "success": False,
                    "error": f"Video file not found: {video_path}"
                }
            
            if not os.path.exists(audio_path):
                return {
                    "success": False,
                    "error": f"Audio file not found: {audio_path}"
                }
            
            # Load video and audio
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            
            # Match audio duration to video
            if audio_clip.duration > video_clip.duration:
                audio_clip = audio_clip.subclip(0, video_clip.duration)
            elif audio_clip.duration < video_clip.duration:
                # Loop audio if it's shorter
                loops_needed = int(video_clip.duration / audio_clip.duration) + 1
                audio_clip = audio_clip.loop(loops_needed).subclip(0, video_clip.duration)
            
            # Combine video and audio
            final_clip = video_clip.set_audio(audio_clip)
            
            # Generate filename if not provided
            if output_filename is None:
                timestamp = int(time.time())
                output_filename = f"video_with_audio_{timestamp}.mp4"
            
            filepath = self.output_dir / output_filename
            
            # Write final video
            final_clip.write_videofile(
                str(filepath),
                codec='libx264',
                audio_codec='aac'
            )
            
            # Clean up
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            
            return {
                "success": True,
                "path": str(filepath),
                "video_path": video_path,
                "audio_path": audio_path,
                "duration": final_clip.duration,
                "engine": "moviepy_combine"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error combining video with audio: {str(e)}"
            }

    def create_video_collage(
        self, 
        video_paths: List[str], 
        layout: str = "grid",
        output_filename: str = "video_collage.mp4"
    ) -> Dict:
        """Create video collage from multiple videos"""
        
        try:
            if not video_paths:
                return {
                    "success": False,
                    "error": "No video paths provided"
                }
            
            # Load video clips
            clips = []
            for path in video_paths:
                if os.path.exists(path):
                    clip = VideoFileClip(path)
                    clips.append(clip)
            
            if not clips:
                return {
                    "success": False,
                    "error": "No valid videos found"
                }
            
            # Create collage based on layout
            if layout == "grid":
                # Arrange clips in a grid
                n = len(clips)
                cols = int(np.ceil(np.sqrt(n)))
                rows = int(np.ceil(n / cols))
                
                # Resize clips to fit grid
                target_width = 640 // cols
                target_height = 480 // rows
                
                resized_clips = []
                for clip in clips:
                    resized_clip = clip.resize((target_width, target_height))
                    resized_clips.append(resized_clip)
                
                # Create grid layout
                grid_clips = []
                for i in range(rows):
                    row_clips = []
                    for j in range(cols):
                        idx = i * cols + j
                        if idx < len(resized_clips):
                            # Position clip in grid
                            clip = resized_clips[idx].set_position((j * target_width, i * target_height))
                            row_clips.append(clip)
                    
                    if row_clips:
                        row_composite = CompositeVideoClip(row_clips, size=(640, target_height))
                        grid_clips.append(row_composite)
                
                if grid_clips:
                    final_clip = CompositeVideoClip(grid_clips, size=(640, 480))
                else:
                    final_clip = resized_clips[0]
            
            elif layout == "side_by_side":
                # Arrange clips side by side
                target_height = 480
                target_width = 640 // len(clips)
                
                resized_clips = []
                for i, clip in enumerate(clips):
                    resized_clip = clip.resize((target_width, target_height))
                    positioned_clip = resized_clip.set_position((i * target_width, 0))
                    resized_clips.append(positioned_clip)
                
                final_clip = CompositeVideoClip(resized_clips, size=(640, 480))
            
            else:
                # Default to concatenation
                final_clip = clips[0]
                for clip in clips[1:]:
                    final_clip = final_clip.concatenate_videoclips([clip])
            
            # Save video collage
            filepath = self.output_dir / output_filename
            
            final_clip.write_videofile(
                str(filepath),
                codec='libx264',
                audio_codec='aac'
            )
            
            # Clean up
            for clip in clips:
                clip.close()
            final_clip.close()
            
            return {
                "success": True,
                "path": str(filepath),
                "layout": layout,
                "num_videos": len(clips),
                "engine": "moviepy_collage"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating video collage: {str(e)}"
            }

    def get_available_styles(self) -> List[str]:
        """Get list of available video styles"""
        return list(self.video_presets.keys())

    def get_engine_status(self) -> Dict:
        """Get status of all video generation engines"""
        status = {
            "moviepy": True,  # Always available
            "api_configs": {}
        }
        
        for api_name, config in self.api_configs.items():
            status["api_configs"][api_name] = {
                "enabled": config["enabled"],
                "url": config["url"]
            }
        
        return status

    def test_api_connection(self, api_type: str = "runway_ml") -> Dict:
        """Test API connection"""
        
        if api_type == "runway_ml":
            api_key = os.getenv("RUNWAY_API_KEY")
            if not api_key:
                return {
                    "success": False,
                    "error": "RUNWAY_API_KEY not set"
                }
            
            try:
                headers = {"Authorization": f"Bearer {api_key}"}
                response = requests.get(
                    "https://api.runwayml.com/v1/models",
                    headers=headers,
                    timeout=5
                )
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

    def play_video_file(self, filepath: str) -> bool:
        """Play a video file (placeholder - would need proper video player integration)"""
        try:
            print(f"Video file ready for playback: {filepath}")
            # In a real implementation, this would open a video player
            return True
            
        except Exception as e:
            print(f"Error playing video file: {e}")
            return False


# Example usage
if __name__ == "__main__":
    generator = EnhancedVideoGenerator()
    
    # Test video generation from images
    print("Testing video generation from images...")
    # This would require actual image files
    # result = generator.generate_video_from_images(["image1.jpg", "image2.jpg"])
    # print(f"Video generation result: {result}")
    
    # Show available styles
    styles = generator.get_available_styles()
    print(f"Available video styles: {styles}")
    
    # Test API connection
    api_status = generator.test_api_connection()
    print(f"API status: {api_status}")
    
    # Show engine status
    engine_status = generator.get_engine_status()
    print(f"Engine status: {engine_status}") 