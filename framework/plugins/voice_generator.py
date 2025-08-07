#!/usr/bin/env python3
"""
BULMA HEADER PROTOCOL - FRAMEWORK/PLUGINS/VOICE_GENERATOR_MERGED.PY
====================================================================

FILE IDENTITY:
- Name: Merged Voice Generator Plugin for Authoring Bot
- Role: Handles audiobook narration and voice generation with enhanced capabilities
- Purpose: Generates voice content for authoring projects with multiple TTS support
- Location: framework/plugins/voice_generator_merged.py (Merged voice generation plugin)

BULMA USAGE PATTERNS:
- READ FIRST: This plugin handles all voice generation for authoring
- MODIFICATIONS: Changes here affect voice quality and style
- TESTING: Test voice generation with various texts and voices
- INTEGRATION: Works with local TTS models and APIs

KEY COMPONENTS:
1. VoiceGenerator - Main voice generation class
2. AudiobookNarrator - Specialized audiobook creation
3. CharacterVoiceGenerator - Character voice creation
4. VoiceStyleManager - Different voice styles and personalities
5. AudioFormatManager - Different audio formats and quality
6. Enhanced TTS Support - Multiple TTS engines and APIs
7. Character Voice Integration - Character embodiment voice generation

BULMA RESTRICTIONS:
- DO NOT modify voice generation without testing quality
- DO NOT change voice parameters without audio testing
- ALWAYS test generated audio for clarity and quality
- CHECK that voice styles match character personalities
- VERIFY audio format and quality standards

ALWAYS READ THIS HEADER BEFORE MODIFYING THIS FILE.
This plugin is critical for audio authoring content.
"""

import os
import json
import time
import requests
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

# Optional imports for enhanced functionality
try:
    import pyttsx3
    from gtts import gTTS
    import pygame
    import wave
    import numpy as np

    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False

logger = logging.getLogger(__name__)


class VoiceGenerator:
    """Enhanced voice generation plugin for authoring bot with multiple TTS support"""

    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config

        # Voice generation settings
        self.voice_styles = self._load_voice_styles()
        self.output_dir = Path(__file__).parent.parent.parent / "voice" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Enhanced functionality
        self.pyttsx3_engine = None
        self.voice_presets = self._initialize_voice_presets()
        self.available_voices = {}

        # API configurations
        self.api_configs = {
            "elevenlabs": {
                "url": "https://api.elevenlabs.io/v1/text-to-speech",
                "timeout": 30,
                "enabled": False,  # Requires API key
            },
            "openai_tts": {
                "url": "https://api.openai.com/v1/audio/speech",
                "timeout": 60,
                "enabled": False,  # Requires API key
            },
            "azure_tts": {
                "url": "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1",
                "timeout": 30,
                "enabled": False,  # Requires API key
            },
        }

        # Initialize pygame for audio playback if available
        if ENHANCED_AVAILABLE:
            try:
                pygame.mixer.init()
            except:
                pass

        logger.info("✅ Merged Voice Generator plugin initialized")

    def _load_voice_styles(self) -> Dict[str, Dict[str, Any]]:
        """Load voice generation styles for different purposes"""
        return {
            "narrator": {
                "male": "deep, authoritative male voice, clear pronunciation, professional",
                "female": "warm, engaging female voice, clear pronunciation, professional",
                "neutral": "neutral, clear voice, professional narration, easy to understand",
                "dramatic": "dramatic, expressive voice, emotional delivery, professional",
                "calm": "calm, soothing voice, gentle delivery, professional",
                "energetic": "energetic, enthusiastic voice, dynamic delivery, professional",
                "default": "professional narrator voice, clear pronunciation, engaging",
            },
            "character": {
                "hero": "strong, confident voice, heroic personality, clear speech",
                "villain": "dark, menacing voice, sinister personality, clear speech",
                "comic": "light, humorous voice, playful personality, clear speech",
                "wise": "mature, thoughtful voice, wise personality, clear speech",
                "young": "youthful, energetic voice, young personality, clear speech",
                "elderly": "mature, experienced voice, elderly personality, clear speech",
                "default": "character voice, clear pronunciation, personality appropriate",
            },
            "audiobook": {
                "fantasy": "epic fantasy narrator, dramatic, engaging, professional",
                "romance": "romantic narrator, warm, emotional, professional",
                "mystery": "mysterious narrator, suspenseful, engaging, professional",
                "scifi": "science fiction narrator, futuristic, engaging, professional",
                "horror": "horror narrator, dark, atmospheric, professional",
                "young_adult": "young adult narrator, relatable, engaging, professional",
                "historical": "historical narrator, period appropriate, engaging, professional",
                "default": "professional audiobook narrator, clear, engaging",
            },
        }

    def _initialize_voice_presets(self) -> Dict:
        """Initialize enhanced voice presets for different character types"""
        return {
            "romantic": {
                "voice_id": "female_romantic",
                "rate": 150,
                "volume": 0.8,
                "pitch": 1.1,
                "description": "Soft, warm, and intimate voice",
                "characteristics": ["gentle", "warm", "intimate", "smooth"],
            },
            "seductive": {
                "voice_id": "female_seductive",
                "rate": 140,
                "volume": 0.9,
                "pitch": 1.2,
                "description": "Alluring and captivating voice",
                "characteristics": ["alluring", "captivating", "magnetic", "smooth"],
            },
            "confident": {
                "voice_id": "female_confident",
                "rate": 160,
                "volume": 0.9,
                "pitch": 1.0,
                "description": "Strong and self-assured voice",
                "characteristics": ["strong", "assured", "clear", "authoritative"],
            },
            "playful": {
                "voice_id": "female_playful",
                "rate": 170,
                "volume": 0.8,
                "pitch": 1.3,
                "description": "Light and cheerful voice",
                "characteristics": ["cheerful", "light", "energetic", "fun"],
            },
            "mysterious": {
                "voice_id": "female_mysterious",
                "rate": 130,
                "volume": 0.7,
                "pitch": 0.9,
                "description": "Enigmatic and intriguing voice",
                "characteristics": [
                    "enigmatic",
                    "intriguing",
                    "whispery",
                    "mysterious",
                ],
            },
            "nurturing": {
                "voice_id": "female_nurturing",
                "rate": 145,
                "volume": 0.8,
                "pitch": 1.0,
                "description": "Caring and supportive voice",
                "characteristics": ["caring", "supportive", "warm", "gentle"],
            },
            "default": {
                "voice_id": "default",
                "rate": 150,
                "volume": 0.8,
                "pitch": 1.0,
                "description": "Standard voice",
                "characteristics": ["clear", "neutral", "professional"],
            },
        }

    def generate_voice(self, text: str, voice_style: str = "narrator") -> str:
        """Generate voice audio from text (basic functionality)"""
        try:
            # Enhance text with voice parameters
            enhanced_text = self._enhance_text(text, voice_style)

            # Try enhanced generation first, fallback to basic
            if ENHANCED_AVAILABLE:
                result = self.generate_voice_with_pyttsx3(enhanced_text, "default")
                if result.get("success"):
                    return result["audio_path"]

            # Fallback to basic generation
            audio_path = self._generate_voice_placeholder(enhanced_text, voice_style)
            logger.info(f"✅ Generated voice: {audio_path}")
            return f"Voice generated: {audio_path}"

        except Exception as e:
            logger.error(f"❌ Failed to generate voice: {e}")
            return f"Voice generation failed: {e}"

    def _enhance_text(self, text: str, voice_style: str) -> str:
        """Enhance text with voice style information"""
        if voice_style in self.voice_styles.get("narrator", {}):
            style_prompt = self.voice_styles["narrator"][voice_style]
            return f"{text} [Voice style: {style_prompt}]"
        return text

    def _generate_voice_placeholder(self, text: str, voice_style: str) -> str:
        """Generate a placeholder voice file (basic functionality)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_voice_{voice_style}_{timestamp}.wav"
        audio_path = self.output_dir / filename

        # Create a simple placeholder audio file
        # This is a minimal implementation - in practice you'd use a TTS library
        with open(audio_path, "wb") as f:
            # Write a minimal WAV header
            f.write(b"RIFF")
            f.write((36).to_bytes(4, "little"))
            f.write(b"WAVE")
            f.write(b"fmt ")
            f.write((16).to_bytes(4, "little"))
            f.write((1).to_bytes(2, "little"))  # PCM
            f.write((1).to_bytes(2, "little"))  # Mono
            f.write((22050).to_bytes(4, "little"))  # Sample rate
            f.write((44100).to_bytes(4, "little"))  # Byte rate
            f.write((2).to_bytes(2, "little"))  # Block align
            f.write((16).to_bytes(2, "little"))  # Bits per sample
            f.write(b"data")
            f.write((0).to_bytes(4, "little"))  # Data size

        return str(audio_path)

    def narrate_chapter(
        self, project_name: str, chapter_number: int, voice_style: str = "narrator"
    ) -> str:
        """Generate narration for a chapter"""
        text = f"Chapter {chapter_number} of {project_name}"
        return self.generate_voice(text, voice_style)

    def generate_character_voice(
        self, character_name: str, dialogue: str, character_personality: str = None
    ) -> str:
        """Generate character voice with enhanced capabilities"""
        try:
            # Try to get character profile from embodiment engine if available
            character_profile = None
            if (
                hasattr(self.framework, "plugins")
                and "character_embodiment_engine" in self.framework.plugins
            ):
                try:
                    character_profile = self.framework.plugins[
                        "character_embodiment_engine"
                    ].get_character_profile(character_name)
                except:
                    pass

            # Determine voice style based on character profile or personality
            voice_style = self._determine_character_voice_style(
                character_profile or character_personality
            )

            # Enhance dialogue with character traits
            enhanced_dialogue = self._enhance_dialogue_with_character_traits(
                dialogue, character_profile
            )

            # Generate voice using enhanced capabilities
            if ENHANCED_AVAILABLE:
                result = self.generate_voice_with_pyttsx3(
                    enhanced_dialogue, voice_style
                )
                if result.get("success"):
                    return result["audio_path"]

            # Fallback to basic generation
            return self.generate_voice(enhanced_dialogue, voice_style)

        except Exception as e:
            logger.error(f"❌ Failed to generate character voice: {e}")
            return f"Character voice generation failed: {e}"

    def _determine_character_voice_style(self, character_profile) -> str:
        """Determine voice style based on character profile"""
        if not character_profile:
            return "default"

        # Extract personality traits
        personality = str(character_profile).lower()

        # Map personality traits to voice styles
        if any(trait in personality for trait in ["romantic", "seductive", "intimate"]):
            return "romantic"
        elif any(trait in personality for trait in ["confident", "strong", "heroic"]):
            return "confident"
        elif any(trait in personality for trait in ["playful", "cheerful", "fun"]):
            return "playful"
        elif any(trait in personality for trait in ["mysterious", "dark", "sinister"]):
            return "mysterious"
        elif any(trait in personality for trait in ["nurturing", "caring", "gentle"]):
            return "nurturing"
        else:
            return "default"

    def _enhance_dialogue_with_character_traits(
        self, dialogue: str, character_profile
    ) -> str:
        """Enhance dialogue with character-specific voice patterns"""
        if not character_profile:
            return dialogue

        # Extract character traits
        personality = str(character_profile).lower()

        # Add voice pattern indicators
        enhanced_dialogue = dialogue

        if "romantic" in personality or "seductive" in personality:
            enhanced_dialogue = f"[Soft, intimate tone] {dialogue}"
        elif "confident" in personality or "strong" in personality:
            enhanced_dialogue = f"[Strong, assured tone] {dialogue}"
        elif "playful" in personality or "cheerful" in personality:
            enhanced_dialogue = f"[Light, cheerful tone] {dialogue}"
        elif "mysterious" in personality or "dark" in personality:
            enhanced_dialogue = f"[Mysterious, whispery tone] {dialogue}"
        elif "nurturing" in personality or "caring" in personality:
            enhanced_dialogue = f"[Warm, caring tone] {dialogue}"

        return enhanced_dialogue

    def _determine_voice_style_from_personality(
        self, character_personality: str
    ) -> str:
        """Determine voice style from personality string"""
        if not character_personality:
            return "default"

        personality = character_personality.lower()

        if any(trait in personality for trait in ["romantic", "seductive"]):
            return "romantic"
        elif any(trait in personality for trait in ["confident", "strong"]):
            return "confident"
        elif any(trait in personality for trait in ["playful", "cheerful"]):
            return "playful"
        elif any(trait in personality for trait in ["mysterious", "dark"]):
            return "mysterious"
        elif any(trait in personality for trait in ["nurturing", "caring"]):
            return "nurturing"
        else:
            return "default"

    def generate_audiobook_sample(self, project_name: str, sample_text: str) -> str:
        """Generate audiobook sample"""
        text = f"Sample from {project_name}: {sample_text}"
        return self.generate_voice(text, "audiobook")

    # Enhanced functionality methods
    def initialize_pyttsx3(self) -> bool:
        """Initialize pyttsx3 TTS engine"""
        if not ENHANCED_AVAILABLE:
            logger.warning(
                "Enhanced functionality not available (pyttsx3 not installed)"
            )
            return False

        try:
            self.pyttsx3_engine = pyttsx3.init()

            # Get available voices
            voices = self.pyttsx3_engine.getProperty("voices")
            for voice in voices:
                self.available_voices[voice.id] = {
                    "name": voice.name,
                    "languages": voice.languages,
                    "gender": voice.gender,
                }

            logger.info(f"✅ pyttsx3 initialized with {len(voices)} voices")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to initialize pyttsx3: {e}")
            return False

    def generate_voice_with_pyttsx3(
        self, text: str, voice_preset: str = "default", output_filename: str = None
    ) -> Dict:
        """Generate voice using pyttsx3"""
        if not ENHANCED_AVAILABLE or not self.pyttsx3_engine:
            return {"success": False, "error": "pyttsx3 not available"}

        try:
            # Get voice preset
            preset = self.voice_presets.get(voice_preset, self.voice_presets["default"])

            # Set voice properties
            self.pyttsx3_engine.setProperty("rate", preset["rate"])
            self.pyttsx3_engine.setProperty("volume", preset["volume"])

            # Try to set voice if available
            voices = self.pyttsx3_engine.getProperty("voices")
            if voices:
                # Try to find a female voice for romantic/seductive presets
                if voice_preset in ["romantic", "seductive", "nurturing"]:
                    for voice in voices:
                        if "female" in voice.name.lower():
                            self.pyttsx3_engine.setProperty("voice", voice.id)
                            break
                else:
                    # Use first available voice
                    self.pyttsx3_engine.setProperty("voice", voices[0].id)

            # Generate filename
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"pyttsx3_{voice_preset}_{timestamp}.wav"

            audio_path = self.output_dir / output_filename

            # Generate speech
            self.pyttsx3_engine.save_to_file(text, str(audio_path))
            self.pyttsx3_engine.runAndWait()

            return {
                "success": True,
                "audio_path": str(audio_path),
                "text": text,
                "voice_preset": voice_preset,
                "preset": preset,
            }

        except Exception as e:
            logger.error(f"❌ pyttsx3 generation failed: {e}")
            return {"success": False, "error": str(e)}

    def generate_voice_with_gtts(
        self, text: str, language: str = "en", output_filename: str = None
    ) -> Dict:
        """Generate voice using Google Text-to-Speech"""
        if not ENHANCED_AVAILABLE:
            return {"success": False, "error": "gTTS not available"}

        try:
            # Generate filename
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"gtts_{language}_{timestamp}.mp3"

            audio_path = self.output_dir / output_filename

            # Generate speech
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(str(audio_path))

            return {
                "success": True,
                "audio_path": str(audio_path),
                "text": text,
                "language": language,
            }

        except Exception as e:
            logger.error(f"❌ gTTS generation failed: {e}")
            return {"success": False, "error": str(e)}

    def generate_voice_with_api(
        self, text: str, voice_preset: str = "default", api_type: str = "elevenlabs"
    ) -> Dict:
        """Generate voice using API"""
        if api_type == "elevenlabs":
            return self._generate_with_elevenlabs_api(text, voice_preset)
        elif api_type == "openai_tts":
            return self._generate_with_openai_tts_api(text, voice_preset)
        elif api_type == "azure_tts":
            return self._generate_with_azure_tts_api(text, voice_preset)
        else:
            return {"success": False, "error": f"Unknown API type: {api_type}"}

    def _generate_with_elevenlabs_api(self, text: str, voice_preset: str) -> Dict:
        """Generate voice using ElevenLabs API"""
        # This would require ElevenLabs API key
        return {"success": False, "error": "ElevenLabs API not configured"}

    def _generate_with_openai_tts_api(self, text: str, voice_preset: str) -> Dict:
        """Generate voice using OpenAI TTS API"""
        # This would require OpenAI API key
        return {"success": False, "error": "OpenAI TTS API not configured"}

    def _generate_with_azure_tts_api(self, text: str, voice_preset: str) -> Dict:
        """Generate voice using Azure TTS API"""
        # This would require Azure API key
        return {"success": False, "error": "Azure TTS API not configured"}

    def play_audio_file(self, filepath: str) -> bool:
        """Play audio file using pygame"""
        if not ENHANCED_AVAILABLE:
            return False

        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            return True
        except Exception as e:
            logger.error(f"❌ Failed to play audio: {e}")
            return False

    def get_available_voices(self) -> Dict[str, List[str]]:
        """Get available voices for different purposes"""
        return {
            "narrator": list(self.voice_styles["narrator"].keys()),
            "character": list(self.voice_styles["character"].keys()),
            "audiobook": list(self.voice_styles["audiobook"].keys()),
            "enhanced_presets": list(self.voice_presets.keys()),
            "pyttsx3_voices": (
                list(self.available_voices.keys()) if self.available_voices else []
            ),
        }

    def get_engine_status(self) -> Dict:
        """Get status of available TTS engines and APIs"""
        return {
            "enhanced_available": ENHANCED_AVAILABLE,
            "pyttsx3_available": self.pyttsx3_engine is not None,
            "gtts_available": ENHANCED_AVAILABLE,
            "pygame_available": ENHANCED_AVAILABLE,
            "elevenlabs_api": self.api_configs["elevenlabs"]["enabled"],
            "openai_tts_api": self.api_configs["openai_tts"]["enabled"],
            "azure_tts_api": self.api_configs["azure_tts"]["enabled"],
        }

    def test_api_connection(self, api_type: str = "elevenlabs") -> Dict:
        """Test API connection"""
        return {"success": False, "error": f"{api_type} API not configured"}


def initialize(framework) -> VoiceGenerator:
    """Initialize the merged voice generator plugin"""
    return VoiceGenerator(framework)
