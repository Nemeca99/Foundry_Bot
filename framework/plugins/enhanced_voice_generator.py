#!/usr/bin/env python3
"""
Enhanced Voice Generation System
Integrates with multiple TTS models and APIs for high-quality voice generation
"""

import os
import json
import time
import requests
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pyttsx3
from gtts import gTTS
import pygame
import wave
import numpy as np


class EnhancedVoiceGenerator:
    """Enhanced voice generation with multiple TTS support"""

    def __init__(self):
        self.output_dir = Path("voice/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize TTS engines
        self.pyttsx3_engine = None
        self.voice_presets = self._initialize_voice_presets()
        self.available_voices = {}
        
        # API configurations
        self.api_configs = {
            "elevenlabs": {
                "url": "https://api.elevenlabs.io/v1/text-to-speech",
                "timeout": 30,
                "enabled": False  # Requires API key
            },
            "openai_tts": {
                "url": "https://api.openai.com/v1/audio/speech",
                "timeout": 60,
                "enabled": False  # Requires API key
            },
            "azure_tts": {
                "url": "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1",
                "timeout": 30,
                "enabled": False  # Requires API key
            }
        }
        
        # Initialize pygame for audio playback
        pygame.mixer.init()

    def _initialize_voice_presets(self) -> Dict:
        """Initialize voice presets for different character types"""
        return {
            "romantic": {
                "voice_id": "female_romantic",
                "rate": 150,
                "volume": 0.8,
                "pitch": 1.1,
                "description": "Soft, warm, and intimate voice",
                "characteristics": ["gentle", "warm", "intimate", "smooth"]
            },
            "seductive": {
                "voice_id": "female_seductive",
                "rate": 140,
                "volume": 0.9,
                "pitch": 1.2,
                "description": "Alluring and captivating voice",
                "characteristics": ["alluring", "captivating", "magnetic", "smooth"]
            },
            "confident": {
                "voice_id": "female_confident",
                "rate": 160,
                "volume": 0.9,
                "pitch": 1.0,
                "description": "Strong and self-assured voice",
                "characteristics": ["strong", "assured", "clear", "authoritative"]
            },
            "playful": {
                "voice_id": "female_playful",
                "rate": 170,
                "volume": 0.8,
                "pitch": 1.3,
                "description": "Light and cheerful voice",
                "characteristics": ["cheerful", "light", "energetic", "fun"]
            },
            "mysterious": {
                "voice_id": "female_mysterious",
                "rate": 130,
                "volume": 0.7,
                "pitch": 0.9,
                "description": "Enigmatic and intriguing voice",
                "characteristics": ["enigmatic", "intriguing", "whispery", "mysterious"]
            },
            "nurturing": {
                "voice_id": "female_nurturing",
                "rate": 145,
                "volume": 0.8,
                "pitch": 1.0,
                "description": "Caring and comforting voice",
                "characteristics": ["caring", "comforting", "gentle", "warm"]
            },
            "anxious": {
                "voice_id": "female_anxious",
                "rate": 180,
                "volume": 0.6,
                "pitch": 1.1,
                "description": "Nervous and uncertain voice",
                "characteristics": ["nervous", "uncertain", "quick", "breathy"]
            },
            "melancholic": {
                "voice_id": "female_melancholic",
                "rate": 120,
                "volume": 0.6,
                "pitch": 0.8,
                "description": "Sad and reflective voice",
                "characteristics": ["sad", "reflective", "slow", "soft"]
            },
            "default": {
                "voice_id": "female_default",
                "rate": 150,
                "volume": 0.8,
                "pitch": 1.0,
                "description": "Clear and natural voice",
                "characteristics": ["clear", "natural", "balanced", "pleasant"]
            }
        }

    def initialize_pyttsx3(self) -> bool:
        """Initialize pyttsx3 TTS engine"""
        try:
            self.pyttsx3_engine = pyttsx3.init()
            
            # Get available voices
            voices = self.pyttsx3_engine.getProperty('voices')
            for voice in voices:
                self.available_voices[voice.id] = {
                    "name": voice.name,
                    "languages": voice.languages,
                    "gender": voice.gender
                }
            
            # Set default properties
            self.pyttsx3_engine.setProperty('rate', 150)
            self.pyttsx3_engine.setProperty('volume', 0.8)
            
            return True
            
        except Exception as e:
            print(f"Error initializing pyttsx3: {e}")
            return False

    def generate_voice_with_pyttsx3(
        self, 
        text: str, 
        voice_preset: str = "default",
        output_filename: str = None
    ) -> Dict:
        """Generate voice using pyttsx3"""
        
        if self.pyttsx3_engine is None:
            success = self.initialize_pyttsx3()
            if not success:
                return {
                    "success": False,
                    "error": "Failed to initialize pyttsx3 engine"
                }
        
        try:
            # Get voice preset
            preset = self.voice_presets.get(voice_preset, self.voice_presets["default"])
            
            # Set voice properties
            self.pyttsx3_engine.setProperty('rate', preset["rate"])
            self.pyttsx3_engine.setProperty('volume', preset["volume"])
            
            # Try to set a female voice if available
            voices = self.pyttsx3_engine.getProperty('voices')
            if voices:
                # Look for a female voice
                for voice in voices:
                    if "female" in voice.name.lower() or "zira" in voice.name.lower():
                        self.pyttsx3_engine.setProperty('voice', voice.id)
                        break
            
            # Generate filename if not provided
            if output_filename is None:
                timestamp = int(time.time())
                output_filename = f"pyttsx3_generated_{timestamp}.wav"
            
            filepath = self.output_dir / output_filename
            
            # Save to file
            self.pyttsx3_engine.save_to_file(text, str(filepath))
            self.pyttsx3_engine.runAndWait()
            
            return {
                "success": True,
                "path": str(filepath),
                "text": text,
                "voice_preset": voice_preset,
                "engine": "pyttsx3",
                "preset": preset
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating voice with pyttsx3: {str(e)}"
            }

    def generate_voice_with_gtts(
        self, 
        text: str, 
        language: str = "en",
        output_filename: str = None
    ) -> Dict:
        """Generate voice using Google TTS (gTTS)"""
        
        try:
            # Generate filename if not provided
            if output_filename is None:
                timestamp = int(time.time())
                output_filename = f"gtts_generated_{timestamp}.mp3"
            
            filepath = self.output_dir / output_filename
            
            # Generate TTS
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(str(filepath))
            
            return {
                "success": True,
                "path": str(filepath),
                "text": text,
                "language": language,
                "engine": "gtts"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating voice with gTTS: {str(e)}"
            }

    def generate_voice_with_api(
        self, 
        text: str, 
        voice_preset: str = "default",
        api_type: str = "elevenlabs"
    ) -> Dict:
        """Generate voice using external APIs"""
        
        if api_type == "elevenlabs":
            return self._generate_with_elevenlabs_api(text, voice_preset)
        elif api_type == "openai_tts":
            return self._generate_with_openai_tts_api(text, voice_preset)
        elif api_type == "azure_tts":
            return self._generate_with_azure_tts_api(text, voice_preset)
        else:
            return {
                "success": False,
                "error": f"Unknown API type: {api_type}"
            }

    def _generate_with_elevenlabs_api(self, text: str, voice_preset: str) -> Dict:
        """Generate voice using ElevenLabs API"""
        
        config = self.api_configs["elevenlabs"]
        if not config["enabled"]:
            return {
                "success": False,
                "error": "ElevenLabs API not enabled. Set ELEVENLABS_API_KEY environment variable."
            }
        
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "ELEVENLABS_API_KEY environment variable not set"
            }
        
        try:
            # Get voice preset
            preset = self.voice_presets.get(voice_preset, self.voice_presets["default"])
            
            # Prepare API request
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            # Use appropriate voice ID based on preset
            voice_id_map = {
                "romantic": "21m00Tcm4TlvDq8ikWAM",  # Rachel
                "seductive": "EXAVITQu4vr4xnSDxMaL",  # Bella
                "confident": "AZnzlk1XvdvUeBnXmlld",  # Domi
                "playful": "VR6AewLTigWG4xSOukaG",   # Arnold
                "mysterious": "pNInz6obpgDQGcFmaJgB", # Adam
                "nurturing": "21m00Tcm4TlvDq8ikWAM", # Rachel
                "anxious": "VR6AewLTigWG4xSOukaG",   # Arnold
                "melancholic": "pNInz6obpgDQGcFmaJgB", # Adam
                "default": "21m00Tcm4TlvDq8ikWAM"    # Rachel
            }
            
            voice_id = voice_id_map.get(voice_preset, voice_id_map["default"])
            
            # Make API request
            response = requests.post(
                f"{config['url']}/{voice_id}",
                json=payload,
                headers=headers,
                timeout=config["timeout"]
            )
            
            if response.status_code == 200:
                # Save audio file
                timestamp = int(time.time())
                filename = f"elevenlabs_generated_{timestamp}.mp3"
                filepath = self.output_dir / filename
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                return {
                    "success": True,
                    "path": str(filepath),
                    "text": text,
                    "voice_preset": voice_preset,
                    "engine": "elevenlabs",
                    "voice_id": voice_id
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating voice with ElevenLabs: {str(e)}"
            }

    def _generate_with_openai_tts_api(self, text: str, voice_preset: str) -> Dict:
        """Generate voice using OpenAI TTS API"""
        
        config = self.api_configs["openai_tts"]
        if not config["enabled"]:
            return {
                "success": False,
                "error": "OpenAI TTS API not enabled. Set OPENAI_API_KEY environment variable."
            }
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "OPENAI_API_KEY environment variable not set"
            }
        
        try:
            # Map voice presets to OpenAI voices
            voice_map = {
                "romantic": "alloy",
                "seductive": "echo",
                "confident": "fable",
                "playful": "onyx",
                "mysterious": "nova",
                "nurturing": "alloy",
                "anxious": "echo",
                "melancholic": "nova",
                "default": "alloy"
            }
            
            voice = voice_map.get(voice_preset, voice_map["default"])
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "tts-1",
                "input": text,
                "voice": voice,
                "response_format": "mp3",
                "speed": 1.0
            }
            
            # Make API request
            response = requests.post(
                config["url"],
                json=payload,
                headers=headers,
                timeout=config["timeout"]
            )
            
            if response.status_code == 200:
                # Save audio file
                timestamp = int(time.time())
                filename = f"openai_tts_generated_{timestamp}.mp3"
                filepath = self.output_dir / filename
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                return {
                    "success": True,
                    "path": str(filepath),
                    "text": text,
                    "voice_preset": voice_preset,
                    "engine": "openai_tts",
                    "voice": voice
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating voice with OpenAI TTS: {str(e)}"
            }

    def _generate_with_azure_tts_api(self, text: str, voice_preset: str) -> Dict:
        """Generate voice using Azure TTS API"""
        
        config = self.api_configs["azure_tts"]
        if not config["enabled"]:
            return {
                "success": False,
                "error": "Azure TTS API not enabled. Set AZURE_SPEECH_KEY environment variable."
            }
        
        api_key = os.getenv("AZURE_SPEECH_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "AZURE_SPEECH_KEY environment variable not set"
            }
        
        try:
            # Map voice presets to Azure voices
            voice_map = {
                "romantic": "en-US-JennyNeural",
                "seductive": "en-US-AriaNeural",
                "confident": "en-US-JennyMultilingualNeural",
                "playful": "en-US-GuyNeural",
                "mysterious": "en-US-DavisNeural",
                "nurturing": "en-US-JennyNeural",
                "anxious": "en-US-AriaNeural",
                "melancholic": "en-US-DavisNeural",
                "default": "en-US-JennyNeural"
            }
            
            voice = voice_map.get(voice_preset, voice_map["default"])
            
            # Prepare API request
            headers = {
                "Ocp-Apim-Subscription-Key": api_key,
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
            }
            
            # Create SSML
            ssml = f"""
            <speak version='1.0' xml:lang='en-US'>
                <voice xml:lang='en-US' xml:gender='Female' name='{voice}'>
                    {text}
                </voice>
            </speak>
            """
            
            # Make API request
            response = requests.post(
                config["url"],
                data=ssml,
                headers=headers,
                timeout=config["timeout"]
            )
            
            if response.status_code == 200:
                # Save audio file
                timestamp = int(time.time())
                filename = f"azure_tts_generated_{timestamp}.mp3"
                filepath = self.output_dir / filename
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                return {
                    "success": True,
                    "path": str(filepath),
                    "text": text,
                    "voice_preset": voice_preset,
                    "engine": "azure_tts",
                    "voice": voice
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating voice with Azure TTS: {str(e)}"
            }

    def generate_character_voice(
        self, 
        text: str, 
        character_name: str,
        character_personality: str = "romantic"
    ) -> Dict:
        """Generate voice for a specific character"""
        
        # Map character personality to voice preset
        personality_to_voice = {
            "romantic": "romantic",
            "seductive": "seductive",
            "confident": "confident",
            "playful": "playful",
            "mysterious": "mysterious",
            "nurturing": "nurturing",
            "anxious": "anxious",
            "melancholic": "melancholic",
            "default": "default"
        }
        
        voice_preset = personality_to_voice.get(character_personality, "default")
        
        # Try different engines in order of preference
        engines = [
            ("pyttsx3", lambda: self.generate_voice_with_pyttsx3(text, voice_preset)),
            ("gtts", lambda: self.generate_voice_with_gtts(text)),
            ("elevenlabs", lambda: self.generate_voice_with_api(text, voice_preset, "elevenlabs")),
            ("openai_tts", lambda: self.generate_voice_with_api(text, voice_preset, "openai_tts"))
        ]
        
        for engine_name, engine_func in engines:
            try:
                result = engine_func()
                if result["success"]:
                    result["character_name"] = character_name
                    result["character_personality"] = character_personality
                    return result
            except Exception as e:
                print(f"Error with {engine_name}: {e}")
                continue
        
        return {
            "success": False,
            "error": "All voice generation engines failed"
        }

    def play_audio_file(self, filepath: str) -> bool:
        """Play an audio file"""
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            return True
            
        except Exception as e:
            print(f"Error playing audio file: {e}")
            return False

    def get_available_voices(self) -> Dict:
        """Get list of available voices"""
        return {
            "pyttsx3_voices": self.available_voices,
            "voice_presets": list(self.voice_presets.keys()),
            "api_configs": {name: {"enabled": config["enabled"]} for name, config in self.api_configs.items()}
        }

    def get_engine_status(self) -> Dict:
        """Get status of all voice generation engines"""
        status = {
            "pyttsx3": self.pyttsx3_engine is not None,
            "gtts": True,  # Always available
            "api_configs": {}
        }
        
        for api_name, config in self.api_configs.items():
            status["api_configs"][api_name] = {
                "enabled": config["enabled"],
                "url": config["url"]
            }
        
        return status

    def test_api_connection(self, api_type: str = "elevenlabs") -> Dict:
        """Test API connection"""
        
        if api_type == "elevenlabs":
            api_key = os.getenv("ELEVENLABS_API_KEY")
            if not api_key:
                return {
                    "success": False,
                    "error": "ELEVENLABS_API_KEY not set"
                }
            
            try:
                headers = {"xi-api-key": api_key}
                response = requests.get(
                    "https://api.elevenlabs.io/v1/voices",
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


# Example usage
if __name__ == "__main__":
    generator = EnhancedVoiceGenerator()
    
    # Test pyttsx3 initialization
    print("Initializing pyttsx3...")
    success = generator.initialize_pyttsx3()
    print(f"pyttsx3 initialized: {success}")
    
    # Test voice generation
    if success:
        result = generator.generate_voice_with_pyttsx3(
            "Hello, I'm Luna. How can I help you today?",
            voice_preset="romantic"
        )
        print(f"Voice generation result: {result}")
    
    # Test gTTS
    gtts_result = generator.generate_voice_with_gtts(
        "This is a test using Google Text-to-Speech."
    )
    print(f"gTTS result: {gtts_result}")
    
    # Show available voices
    voices = generator.get_available_voices()
    print(f"Available voices: {voices}")
    
    # Test API connection
    api_status = generator.test_api_connection()
    print(f"API status: {api_status}") 