#!/usr/bin/env python3
"""
Enhanced Audio Processing System
Generates sound clips and processes audio for multimodal content
"""

import os
import json
import time
import requests
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import pygame
import wave
import soundfile as sf
from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth, WhiteNoise
import librosa
import librosa.display
import matplotlib.pyplot as plt


class EnhancedAudioProcessor:
    """Enhanced audio processing with sound generation and manipulation"""

    def __init__(self):
        self.output_dir = Path("audio/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize audio presets
        self.sound_presets = self._initialize_sound_presets()
        self.audio_effects = self._initialize_audio_effects()

        # API configurations
        self.api_configs = {
            "elevenlabs": {
                "url": "https://api.elevenlabs.io/v1/generation",
                "timeout": 30,
                "enabled": False,  # Requires API key
            },
            "openai_audio": {
                "url": "https://api.openai.com/v1/audio/generations",
                "timeout": 60,
                "enabled": False,  # Requires API key
            },
        }

        # Initialize pygame for audio playback
        pygame.mixer.init()

    def _initialize_sound_presets(self) -> Dict:
        """Initialize sound presets for different content types"""
        return {
            "romantic": {
                "description": "Soft, warm, and intimate sounds",
                "characteristics": ["gentle", "warm", "intimate", "smooth"],
                "base_frequency": 440,
                "duration": 5.0,
                "volume": -20,
                "effects": ["reverb", "soft_compression"],
            },
            "seductive": {
                "description": "Alluring and captivating sounds",
                "characteristics": ["alluring", "captivating", "magnetic", "smooth"],
                "base_frequency": 523,
                "duration": 4.0,
                "volume": -15,
                "effects": ["echo", "delay"],
            },
            "confident": {
                "description": "Strong and self-assured sounds",
                "characteristics": ["strong", "assured", "clear", "authoritative"],
                "base_frequency": 659,
                "duration": 3.0,
                "volume": -10,
                "effects": ["compression", "brightness"],
            },
            "playful": {
                "description": "Light and cheerful sounds",
                "characteristics": ["cheerful", "light", "energetic", "fun"],
                "base_frequency": 784,
                "duration": 2.0,
                "volume": -12,
                "effects": ["chorus", "brightness"],
            },
            "mysterious": {
                "description": "Enigmatic and intriguing sounds",
                "characteristics": [
                    "enigmatic",
                    "intriguing",
                    "whispery",
                    "mysterious",
                ],
                "base_frequency": 330,
                "duration": 6.0,
                "volume": -25,
                "effects": ["reverb", "low_pass"],
            },
            "nurturing": {
                "description": "Caring and comforting sounds",
                "characteristics": ["caring", "comforting", "gentle", "warm"],
                "base_frequency": 392,
                "duration": 4.5,
                "volume": -18,
                "effects": ["soft_compression", "warmth"],
            },
            "anxious": {
                "description": "Nervous and uncertain sounds",
                "characteristics": ["nervous", "uncertain", "quick", "breathy"],
                "base_frequency": 587,
                "duration": 1.5,
                "volume": -8,
                "effects": ["tremolo", "distortion"],
            },
            "melancholic": {
                "description": "Sad and reflective sounds",
                "characteristics": ["sad", "reflective", "slow", "soft"],
                "base_frequency": 262,
                "duration": 7.0,
                "volume": -30,
                "effects": ["reverb", "low_pass"],
            },
            "default": {
                "description": "Clear and natural sounds",
                "characteristics": ["clear", "natural", "balanced", "pleasant"],
                "base_frequency": 440,
                "duration": 3.0,
                "volume": -15,
                "effects": ["compression"],
            },
        }

    def _initialize_audio_effects(self) -> Dict:
        """Initialize audio effects for sound processing"""
        return {
            "reverb": {
                "description": "Adds spatial depth and echo",
                "parameters": {"room_size": 0.8, "damping": 0.5},
            },
            "echo": {
                "description": "Creates repeating sound effect",
                "parameters": {"delay": 0.3, "feedback": 0.4},
            },
            "delay": {
                "description": "Creates time-delayed copies",
                "parameters": {"delay_time": 0.2, "feedback": 0.3},
            },
            "compression": {
                "description": "Reduces dynamic range",
                "parameters": {"threshold": -20, "ratio": 4},
            },
            "soft_compression": {
                "description": "Gentle dynamic range reduction",
                "parameters": {"threshold": -15, "ratio": 2},
            },
            "brightness": {
                "description": "Enhances high frequencies",
                "parameters": {"frequency": 3000, "gain": 3},
            },
            "warmth": {
                "description": "Enhances low frequencies",
                "parameters": {"frequency": 200, "gain": 2},
            },
            "chorus": {
                "description": "Creates rich, layered sound",
                "parameters": {"rate": 1.5, "depth": 0.3},
            },
            "tremolo": {
                "description": "Modulates volume over time",
                "parameters": {"rate": 5.0, "depth": 0.5},
            },
            "distortion": {
                "description": "Adds harmonic saturation",
                "parameters": {"drive": 0.3, "tone": 0.5},
            },
            "low_pass": {
                "description": "Filters high frequencies",
                "parameters": {"cutoff": 1000, "resonance": 0.5},
            },
        }

    def generate_sine_wave(
        self,
        frequency: float = 440.0,
        duration: float = 3.0,
        volume: float = -15.0,
        output_filename: str = None,
    ) -> Dict:
        """Generate a sine wave sound"""

        try:
            # Generate filename if not provided
            if output_filename is None:
                timestamp = int(time.time())
                output_filename = f"sine_wave_{frequency}hz_{timestamp}.wav"

            filepath = self.output_dir / output_filename

            # Generate sine wave
            sample_rate = 44100
            samples = int(duration * sample_rate)
            t = np.linspace(0, duration, samples, False)
            sine_wave = np.sin(2 * np.pi * frequency * t)

            # Apply volume
            volume_factor = 10 ** (volume / 20)
            sine_wave = sine_wave * volume_factor

            # Save as WAV file
            sf.write(str(filepath), sine_wave, sample_rate)

            return {
                "success": True,
                "path": str(filepath),
                "frequency": frequency,
                "duration": duration,
                "volume": volume,
                "engine": "numpy_sine",
            }

        except Exception as e:
            return {"success": False, "error": f"Error generating sine wave: {str(e)}"}

    def generate_sound_with_preset(
        self, preset_name: str = "default", output_filename: str = None
    ) -> Dict:
        """Generate sound using a preset"""

        preset = self.sound_presets.get(preset_name, self.sound_presets["default"])

        # Generate base sound
        result = self.generate_sine_wave(
            frequency=preset["base_frequency"],
            duration=preset["duration"],
            volume=preset["volume"],
            output_filename=output_filename,
        )

        if result["success"]:
            # Apply effects
            result = self.apply_audio_effects(result["path"], preset["effects"])
            result["preset"] = preset_name
            result["preset_data"] = preset

        return result

    def apply_audio_effects(
        self, audio_path: str, effects: List[str], output_filename: str = None
    ) -> Dict:
        """Apply audio effects to a sound file"""

        try:
            if not os.path.exists(audio_path):
                return {
                    "success": False,
                    "error": f"Audio file not found: {audio_path}",
                }

            # Load audio
            audio = AudioSegment.from_file(audio_path)

            # Apply effects
            for effect_name in effects:
                if effect_name in self.audio_effects:
                    effect = self.audio_effects[effect_name]
                    params = effect["parameters"]

                    if effect_name == "reverb":
                        # Simple reverb simulation
                        reverb = audio - 10
                        audio = audio.overlay(reverb, position=100)

                    elif effect_name == "echo":
                        # Echo effect
                        echo = audio - 15
                        audio = audio.overlay(
                            echo, position=int(params["delay"] * 1000)
                        )

                    elif effect_name == "delay":
                        # Delay effect
                        delay = audio - 20
                        audio = audio.overlay(
                            delay, position=int(params["delay_time"] * 1000)
                        )

                    elif effect_name == "compression":
                        # Compression effect
                        audio = audio.compress_dynamic_range(
                            threshold=params["threshold"], ratio=params["ratio"]
                        )

                    elif effect_name == "soft_compression":
                        # Soft compression
                        audio = audio.compress_dynamic_range(
                            threshold=params["threshold"], ratio=params["ratio"]
                        )

                    elif effect_name == "brightness":
                        # High frequency boost
                        audio = audio.high_pass_filter(params["frequency"])

                    elif effect_name == "warmth":
                        # Low frequency boost
                        audio = audio.low_pass_filter(params["frequency"])

                    elif effect_name == "chorus":
                        # Chorus effect (simplified)
                        chorus = audio + 3
                        audio = audio.overlay(chorus, position=50)

                    elif effect_name == "tremolo":
                        # Tremolo effect
                        tremolo = audio - 10
                        audio = audio.overlay(tremolo, position=100)

                    elif effect_name == "distortion":
                        # Distortion effect
                        audio = audio + params["drive"] * 10

                    elif effect_name == "low_pass":
                        # Low pass filter
                        audio = audio.low_pass_filter(params["cutoff"])

            # Generate filename if not provided
            if output_filename is None:
                timestamp = int(time.time())
                output_filename = f"processed_audio_{timestamp}.wav"

            filepath = self.output_dir / output_filename

            # Export processed audio
            audio.export(str(filepath), format="wav")

            return {
                "success": True,
                "path": str(filepath),
                "original_path": audio_path,
                "effects_applied": effects,
                "engine": "pydub_effects",
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error applying audio effects: {str(e)}",
            }

    def generate_ambient_sound(
        self,
        sound_type: str = "nature",
        duration: float = 10.0,
        output_filename: str = None,
    ) -> Dict:
        """Generate ambient background sounds"""

        try:
            # Generate filename if not provided
            if output_filename is None:
                timestamp = int(time.time())
                output_filename = f"ambient_{sound_type}_{timestamp}.wav"

            filepath = self.output_dir / output_filename

            # Generate ambient sound based on type
            if sound_type == "nature":
                # Nature sounds (rain, wind, etc.)
                base_freq = 200
                noise = WhiteNoise().to_audio_segment(duration=duration * 1000)
                noise = noise.low_pass_filter(1000)
                noise = noise - 20  # Reduce volume

            elif sound_type == "ocean":
                # Ocean waves
                base_freq = 150
                noise = WhiteNoise().to_audio_segment(duration=duration * 1000)
                noise = noise.low_pass_filter(500)
                noise = noise - 15

            elif sound_type == "forest":
                # Forest ambience
                base_freq = 300
                noise = WhiteNoise().to_audio_segment(duration=duration * 1000)
                noise = noise.low_pass_filter(800)
                noise = noise - 18

            elif sound_type == "city":
                # City ambience
                base_freq = 400
                noise = WhiteNoise().to_audio_segment(duration=duration * 1000)
                noise = noise.high_pass_filter(200)
                noise = noise - 12

            else:
                # Default ambient
                base_freq = 250
                noise = WhiteNoise().to_audio_segment(duration=duration * 1000)
                noise = noise - 20

            # Export ambient sound
            noise.export(str(filepath), format="wav")

            return {
                "success": True,
                "path": str(filepath),
                "sound_type": sound_type,
                "duration": duration,
                "engine": "pydub_ambient",
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating ambient sound: {str(e)}",
            }

    def create_audio_mix(
        self,
        audio_paths: List[str],
        mix_type: str = "overlay",
        output_filename: str = None,
    ) -> Dict:
        """Create audio mix from multiple files"""

        try:
            if not audio_paths:
                return {"success": False, "error": "No audio paths provided"}

            # Load audio files
            audio_segments = []
            for path in audio_paths:
                if os.path.exists(path):
                    audio = AudioSegment.from_file(path)
                    audio_segments.append(audio)

            if not audio_segments:
                return {"success": False, "error": "No valid audio files found"}

            # Create mix based on type
            if mix_type == "overlay":
                # Overlay all audio files
                final_audio = audio_segments[0]
                for audio in audio_segments[1:]:
                    final_audio = final_audio.overlay(audio)

            elif mix_type == "concatenate":
                # Concatenate audio files
                final_audio = audio_segments[0]
                for audio in audio_segments[1:]:
                    final_audio = final_audio + audio

            elif mix_type == "crossfade":
                # Crossfade between audio files
                final_audio = audio_segments[0]
                for audio in audio_segments[1:]:
                    final_audio = final_audio.append(audio, crossfade=1000)

            else:
                # Default to overlay
                final_audio = audio_segments[0]
                for audio in audio_segments[1:]:
                    final_audio = final_audio.overlay(audio)

            # Generate filename if not provided
            if output_filename is None:
                timestamp = int(time.time())
                output_filename = f"audio_mix_{mix_type}_{timestamp}.wav"

            filepath = self.output_dir / output_filename

            # Export mixed audio
            final_audio.export(str(filepath), format="wav")

            return {
                "success": True,
                "path": str(filepath),
                "mix_type": mix_type,
                "num_files": len(audio_segments),
                "duration": len(final_audio) / 1000.0,
                "engine": "pydub_mix",
            }

        except Exception as e:
            return {"success": False, "error": f"Error creating audio mix: {str(e)}"}

    def generate_character_sound(
        self,
        character_name: str,
        character_personality: str = "romantic",
        sound_type: str = "voice",
    ) -> Dict:
        """Generate sound for a specific character"""

        # Map character personality to sound preset
        personality_to_preset = {
            "romantic": "romantic",
            "seductive": "seductive",
            "confident": "confident",
            "playful": "playful",
            "mysterious": "mysterious",
            "nurturing": "nurturing",
            "anxious": "anxious",
            "melancholic": "melancholic",
            "default": "default",
        }

        preset_name = personality_to_preset.get(character_personality, "default")

        if sound_type == "voice":
            return self.generate_sound_with_preset(preset_name)
        elif sound_type == "ambient":
            return self.generate_ambient_sound("nature", 5.0)
        else:
            return self.generate_sound_with_preset(preset_name)

    def analyze_audio_file(self, audio_path: str) -> Dict:
        """Analyze audio file properties"""

        try:
            if not os.path.exists(audio_path):
                return {
                    "success": False,
                    "error": f"Audio file not found: {audio_path}",
                }

            # Load audio with librosa
            y, sr = librosa.load(audio_path)

            # Calculate audio properties
            duration = len(y) / sr
            rms = np.sqrt(np.mean(y**2))
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]

            # Calculate tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

            # Calculate pitch
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_mean = np.mean(pitches[magnitudes > 0.1])

            return {
                "success": True,
                "path": audio_path,
                "duration": duration,
                "sample_rate": sr,
                "rms_energy": float(rms),
                "spectral_centroid_mean": float(np.mean(spectral_centroids)),
                "spectral_rolloff_mean": float(np.mean(spectral_rolloff)),
                "tempo": float(tempo),
                "pitch_mean": float(pitch_mean) if not np.isnan(pitch_mean) else 0.0,
                "engine": "librosa_analysis",
            }

        except Exception as e:
            return {"success": False, "error": f"Error analyzing audio file: {str(e)}"}

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

    def get_available_presets(self) -> List[str]:
        """Get list of available sound presets"""
        return list(self.sound_presets.keys())

    def get_available_effects(self) -> List[str]:
        """Get list of available audio effects"""
        return list(self.audio_effects.keys())

    def get_engine_status(self) -> Dict:
        """Get status of all audio processing engines"""
        status = {
            "pydub": True,  # Always available
            "librosa": True,  # Always available
            "numpy": True,  # Always available
            "api_configs": {},
        }

        for api_name, config in self.api_configs.items():
            status["api_configs"][api_name] = {
                "enabled": config["enabled"],
                "url": config["url"],
            }

        return status

    def test_api_connection(self, api_type: str = "elevenlabs") -> Dict:
        """Test API connection"""

        if api_type == "elevenlabs":
            api_key = os.getenv("ELEVENLABS_API_KEY")
            if not api_key:
                return {"success": False, "error": "ELEVENLABS_API_KEY not set"}

            try:
                headers = {"xi-api-key": api_key}
                response = requests.get(
                    "https://api.elevenlabs.io/v1/voices", headers=headers, timeout=5
                )
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                }
            except Exception as e:
                return {"success": False, "error": str(e)}

        return {"success": False, "error": f"Unknown API type: {api_type}"}


# Example usage
if __name__ == "__main__":
    processor = EnhancedAudioProcessor()

    # Test sine wave generation
    print("Testing sine wave generation...")
    result = processor.generate_sine_wave(440.0, 3.0, -15.0)
    print(f"Sine wave result: {result}")

    # Test preset generation
    print("Testing preset generation...")
    preset_result = processor.generate_sound_with_preset("romantic")
    print(f"Preset result: {preset_result}")

    # Test ambient sound generation
    print("Testing ambient sound generation...")
    ambient_result = processor.generate_ambient_sound("nature", 5.0)
    print(f"Ambient result: {ambient_result}")

    # Show available presets and effects
    presets = processor.get_available_presets()
    effects = processor.get_available_effects()
    print(f"Available presets: {presets}")
    print(f"Available effects: {effects}")

    # Test API connection
    api_status = processor.test_api_connection()
    print(f"API status: {api_status}")

    # Show engine status
    engine_status = processor.get_engine_status()
    print(f"Engine status: {engine_status}")
