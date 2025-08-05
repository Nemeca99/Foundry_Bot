#!/usr/bin/env python3
"""
Enhanced Multimodal Discord Commands
Integrates with enhanced image, voice, video, and audio generation systems
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import discord
from discord.ext import commands
import shlex

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import enhanced systems
from framework.plugins.enhanced_image_generator import EnhancedImageGenerator
from framework.plugins.enhanced_voice_generator import EnhancedVoiceGenerator
from framework.plugins.enhanced_video_generator import EnhancedVideoGenerator
from framework.plugins.enhanced_audio_processor import EnhancedAudioProcessor
from framework.plugins.multimodal_orchestrator import MultimodalOrchestrator

logger = logging.getLogger(__name__)


class EnhancedMultimodalCommands:
    """Enhanced multimodal Discord commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.image_generator = EnhancedImageGenerator()
        self.voice_generator = EnhancedVoiceGenerator()
        self.video_generator = EnhancedVideoGenerator()
        self.audio_processor = EnhancedAudioProcessor()
        self.orchestrator = MultimodalOrchestrator()
        
        # Initialize systems
        self._initialize_systems()
        
    def _initialize_systems(self):
        """Initialize all enhanced systems"""
        try:
            # Initialize voice generator
            self.voice_generator.initialize_pyttsx3()
            logger.info("✅ Enhanced voice generator initialized")
            
            # Initialize image generator (will load model when needed)
            logger.info("✅ Enhanced image generator initialized")
            
            # Initialize video generator
            logger.info("✅ Enhanced video generator initialized")
            
            # Initialize audio processor
            logger.info("✅ Enhanced audio processor initialized")
            
            # Initialize orchestrator
            logger.info("✅ Enhanced multimodal orchestrator initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing enhanced systems: {e}")
    
    def setup_commands(self):
        """Set up all enhanced multimodal commands"""
        
        @self.bot.command(name="enhanced-image")
        async def enhanced_image_command(ctx, *, args: str = ""):
            """Generate enhanced images with multiple styles and models"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return
            
            try:
                # Parse arguments
                parsed_args = shlex.split(args)
                
                if len(parsed_args) < 1:
                    await ctx.send(
                        '❌ Please provide a prompt. Example: `!enhanced-image "A romantic sunset" romantic`'
                    )
                    return
                
                prompt = parsed_args[0]
                style = parsed_args[1] if len(parsed_args) > 1 else "default"
                model_type = parsed_args[2] if len(parsed_args) > 2 else "local"
                
                # Send initial response
                await ctx.send(f"🎨 Generating enhanced image: {prompt}")
                
                # Generate image
                if model_type == "api":
                    result = self.image_generator.generate_image_with_api(prompt, style)
                else:
                    result = self.image_generator.generate_image_with_stable_diffusion(prompt, style)
                
                if result["success"]:
                    # Create embed
                    embed = discord.Embed(
                        title="🎨 Enhanced Image Generated",
                        description=f"**Prompt:** {prompt}",
                        color=0x9B59B6
                    )
                    embed.add_field(name="Style", value=style, inline=True)
                    embed.add_field(name="Model", value=result.get("model", "unknown"), inline=True)
                    embed.add_field(name="Size", value=result.get("size", "unknown"), inline=True)
                    
                    # Try to attach the image file
                    try:
                        file = discord.File(result["path"], filename="generated_image.png")
                        embed.set_image(url="attachment://generated_image.png")
                        await ctx.send(embed=embed, file=file)
                    except Exception as e:
                        embed.add_field(name="File Path", value=result["path"], inline=False)
                        await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ Error generating image: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                await ctx.send(f"❌ Error in enhanced image generation: {str(e)}")
        
        @self.bot.command(name="enhanced-voice")
        async def enhanced_voice_command(ctx, *, args: str = ""):
            """Generate enhanced voice with multiple TTS engines"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return
            
            try:
                # Parse arguments
                parsed_args = shlex.split(args)
                
                if len(parsed_args) < 1:
                    await ctx.send(
                        '❌ Please provide text. Example: `!enhanced-voice "Hello, I am Luna" romantic`'
                    )
                    return
                
                text = parsed_args[0]
                voice_preset = parsed_args[1] if len(parsed_args) > 1 else "default"
                engine = parsed_args[2] if len(parsed_args) > 2 else "pyttsx3"
                
                # Send initial response
                await ctx.send(f"🎤 Generating enhanced voice: {text[:50]}...")
                
                # Generate voice
                if engine == "gtts":
                    result = self.voice_generator.generate_voice_with_gtts(text)
                elif engine == "api":
                    result = self.voice_generator.generate_voice_with_api(text, voice_preset)
                else:
                    result = self.voice_generator.generate_voice_with_pyttsx3(text, voice_preset)
                
                if result["success"]:
                    # Create embed
                    embed = discord.Embed(
                        title="🎤 Enhanced Voice Generated",
                        description=f"**Text:** {text}",
                        color=0x3498DB
                    )
                    embed.add_field(name="Voice Preset", value=voice_preset, inline=True)
                    embed.add_field(name="Engine", value=result.get("engine", "unknown"), inline=True)
                    embed.add_field(name="Duration", value=f"{result.get('duration', 'unknown')}s", inline=True)
                    
                    # Try to attach the audio file
                    try:
                        file = discord.File(result["path"], filename="generated_voice.mp3")
                        await ctx.send(embed=embed, file=file)
                    except Exception as e:
                        embed.add_field(name="File Path", value=result["path"], inline=False)
                        await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ Error generating voice: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                await ctx.send(f"❌ Error in enhanced voice generation: {str(e)}")
        
        @self.bot.command(name="enhanced-video")
        async def enhanced_video_command(ctx, *, args: str = ""):
            """Generate enhanced videos with multiple styles"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return
            
            try:
                # Parse arguments
                parsed_args = shlex.split(args)
                
                if len(parsed_args) < 1:
                    await ctx.send(
                        '❌ Please provide a prompt. Example: `!enhanced-video "A romantic sunset scene" romantic`'
                    )
                    return
                
                prompt = parsed_args[0]
                style = parsed_args[1] if len(parsed_args) > 1 else "default"
                api_type = parsed_args[2] if len(parsed_args) > 2 else "runway_ml"
                
                # Send initial response
                await ctx.send(f"🎬 Generating enhanced video: {prompt}")
                
                # Generate video
                result = self.video_generator.generate_video_with_api(prompt, style, api_type)
                
                if result["success"]:
                    # Create embed
                    embed = discord.Embed(
                        title="🎬 Enhanced Video Generated",
                        description=f"**Prompt:** {prompt}",
                        color=0xE74C3C
                    )
                    embed.add_field(name="Style", value=style, inline=True)
                    embed.add_field(name="Engine", value=result.get("engine", "unknown"), inline=True)
                    embed.add_field(name="Duration", value=f"{result.get('duration', 'unknown')}s", inline=True)
                    
                    # Try to attach the video file
                    try:
                        file = discord.File(result["path"], filename="generated_video.mp4")
                        await ctx.send(embed=embed, file=file)
                    except Exception as e:
                        embed.add_field(name="File Path", value=result["path"], inline=False)
                        await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ Error generating video: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                await ctx.send(f"❌ Error in enhanced video generation: {str(e)}")
        
        @self.bot.command(name="enhanced-audio")
        async def enhanced_audio_command(ctx, *, args: str = ""):
            """Generate enhanced audio with effects and analysis"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return
            
            try:
                # Parse arguments
                parsed_args = shlex.split(args)
                
                if len(parsed_args) < 1:
                    await ctx.send(
                        '❌ Please provide a sound type. Example: `!enhanced-audio romantic`'
                    )
                    return
                
                sound_type = parsed_args[0]
                preset = parsed_args[1] if len(parsed_args) > 1 else "romantic"
                
                # Send initial response
                await ctx.send(f"🎵 Generating enhanced audio: {sound_type}")
                
                # Generate audio
                if sound_type == "ambient":
                    result = self.audio_processor.generate_ambient_sound(preset, 5.0)
                else:
                    result = self.audio_processor.generate_sound_with_preset(preset)
                
                if result["success"]:
                    # Create embed
                    embed = discord.Embed(
                        title="🎵 Enhanced Audio Generated",
                        description=f"**Type:** {sound_type}",
                        color=0xF39C12
                    )
                    embed.add_field(name="Preset", value=preset, inline=True)
                    embed.add_field(name="Engine", value=result.get("engine", "unknown"), inline=True)
                    embed.add_field(name="Duration", value=f"{result.get('duration', 'unknown')}s", inline=True)
                    
                    # Try to attach the audio file
                    try:
                        file = discord.File(result["path"], filename="generated_audio.wav")
                        await ctx.send(embed=embed, file=file)
                    except Exception as e:
                        embed.add_field(name="File Path", value=result["path"], inline=False)
                        await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ Error generating audio: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                await ctx.send(f"❌ Error in enhanced audio generation: {str(e)}")
        
        @self.bot.command(name="enhanced-character")
        async def enhanced_character_command(ctx, character_name: str, *, description: str = ""):
            """Create enhanced character multimedia package"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return
            
            try:
                # Send initial response
                await ctx.send(f"👤 Creating enhanced character package for: {character_name}")
                
                # Create character multimedia
                result = self.orchestrator.create_character_multimedia(
                    character_name=character_name,
                    character_description=description or f"A character named {character_name}",
                    style="romantic",
                    include_portrait=True,
                    include_voice=True,
                    include_ambient=True,
                    include_video=False
                )
                
                if result["success"]:
                    # Create embed
                    embed = discord.Embed(
                        title=f"👤 Enhanced Character Package: {character_name}",
                        description=description or f"A character named {character_name}",
                        color=0x9B59B6
                    )
                    
                    # Add file information
                    for file_type, file_path in result["files"].items():
                        embed.add_field(
                            name=f"✅ {file_type.title()}",
                            value=f"Generated: {file_path}",
                            inline=False
                        )
                    
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ Error creating character package: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                await ctx.send(f"❌ Error in enhanced character creation: {str(e)}")
        
        @self.bot.command(name="enhanced-story")
        async def enhanced_story_command(ctx, story_title: str, genre: str, *, description: str = ""):
            """Create enhanced story multimedia package"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return
            
            try:
                # Send initial response
                await ctx.send(f"📚 Creating enhanced story package: {story_title}")
                
                # Create story multimedia
                result = self.orchestrator.create_story_multimedia(
                    story_title=story_title,
                    story_description=description or f"A {genre} story",
                    genre=genre,
                    include_cover=True,
                    include_scene=True,
                    include_ambient=True,
                    include_video=False
                )
                
                if result["success"]:
                    # Create embed
                    embed = discord.Embed(
                        title=f"📚 Enhanced Story Package: {story_title}",
                        description=f"Genre: {genre}\n{description or 'A compelling story'}",
                        color=0xE67E22
                    )
                    
                    # Add file information
                    for file_type, file_path in result["files"].items():
                        embed.add_field(
                            name=f"✅ {file_type.title()}",
                            value=f"Generated: {file_path}",
                            inline=False
                        )
                    
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ Error creating story package: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                await ctx.send(f"❌ Error in enhanced story creation: {str(e)}")
        
        @self.bot.command(name="system-status")
        async def system_status_command(ctx):
            """Show status of all enhanced multimodal systems"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return
            
            try:
                # Get status from all systems
                image_status = self.image_generator.get_model_status()
                voice_status = self.voice_generator.get_engine_status()
                video_status = self.video_generator.get_engine_status()
                audio_status = self.audio_processor.get_engine_status()
                
                # Create embed
                embed = discord.Embed(
                    title="🔧 Enhanced Multimodal System Status",
                    description="Status of all enhanced generation systems",
                    color=0x2ECC71
                )
                
                # Image system status
                image_health = "✅" if image_status.get("local_stable_diffusion") else "❌"
                embed.add_field(
                    name="🎨 Image Generation",
                    value=f"{image_health} Local SD: {image_status.get('local_stable_diffusion', False)}\n"
                          f"🔧 CUDA: {image_status.get('cuda_available', False)}\n"
                          f"🌐 APIs: {len(image_status.get('api_configs', {}))}",
                    inline=True
                )
                
                # Voice system status
                voice_health = "✅" if voice_status.get("pyttsx3") else "❌"
                embed.add_field(
                    name="🎤 Voice Generation",
                    value=f"{voice_health} pyttsx3: {voice_status.get('pyttsx3', False)}\n"
                          f"🌐 gTTS: {voice_status.get('gtts', False)}\n"
                          f"🔧 APIs: {len(voice_status.get('api_configs', {}))}",
                    inline=True
                )
                
                # Video system status
                video_health = "✅" if video_status.get("moviepy") else "❌"
                embed.add_field(
                    name="🎬 Video Generation",
                    value=f"{video_health} MoviePy: {video_status.get('moviepy', False)}\n"
                          f"🌐 APIs: {len(video_status.get('api_configs', {}))}",
                    inline=True
                )
                
                # Audio system status
                audio_health = "✅" if audio_status.get("pydub") else "❌"
                embed.add_field(
                    name="🎵 Audio Processing",
                    value=f"{audio_health} pydub: {audio_status.get('pydub', False)}\n"
                          f"📊 librosa: {audio_status.get('librosa', False)}\n"
                          f"🔢 numpy: {audio_status.get('numpy', False)}",
                    inline=True
                )
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"❌ Error getting system status: {str(e)}")
        
        @self.bot.command(name="available-styles")
        async def available_styles_command(ctx, system: str = "all"):
            """Show available styles for each system"""
            if not self._is_authorized(ctx):
                await ctx.send("❌ You are not authorized to use this bot.")
                return
            
            try:
                embed = discord.Embed(
                    title="🎭 Available Styles",
                    description="Styles available for each enhanced system",
                    color=0x9B59B6
                )
                
                if system in ["all", "image"]:
                    image_styles = self.image_generator.get_available_styles()
                    embed.add_field(
                        name="🎨 Image Styles",
                        value=", ".join(image_styles),
                        inline=False
                    )
                
                if system in ["all", "voice"]:
                    voice_info = self.voice_generator.get_available_voices()
                    voice_styles = voice_info.get("voice_presets", [])
                    embed.add_field(
                        name="🎤 Voice Styles",
                        value=", ".join(voice_styles),
                        inline=False
                    )
                
                if system in ["all", "video"]:
                    video_styles = self.video_generator.get_available_styles()
                    embed.add_field(
                        name="🎬 Video Styles",
                        value=", ".join(video_styles),
                        inline=False
                    )
                
                if system in ["all", "audio"]:
                    audio_presets = self.audio_processor.get_available_presets()
                    audio_effects = self.audio_processor.get_available_effects()
                    embed.add_field(
                        name="🎵 Audio Presets",
                        value=", ".join(audio_presets),
                        inline=False
                    )
                    embed.add_field(
                        name="🎛️ Audio Effects",
                        value=", ".join(audio_effects),
                        inline=False
                    )
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"❌ Error getting available styles: {str(e)}")
    
    def _is_authorized(self, ctx) -> bool:
        """Check if user is authorized to use the bot"""
        # Add your authorization logic here
        return True  # For now, allow all users


# Example usage
if __name__ == "__main__":
    # This would be used when integrating with the main Discord bot
    print("Enhanced Multimodal Commands module loaded")
    print("Import and use with main Discord bot") 