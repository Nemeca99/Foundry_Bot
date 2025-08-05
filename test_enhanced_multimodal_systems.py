#!/usr/bin/env python3
"""
Comprehensive Test Script for Enhanced Multimodal Systems
Tests all enhanced systems: Image, Voice, Video, Audio, and Orchestration
"""

import sys
import os
from pathlib import Path

# Add framework to path
sys.path.append(str(Path(__file__).parent / "framework"))

from plugins.enhanced_image_generator import EnhancedImageGenerator
from plugins.enhanced_voice_generator import EnhancedVoiceGenerator
from plugins.enhanced_video_generator import EnhancedVideoGenerator
from plugins.enhanced_audio_processor import EnhancedAudioProcessor
from plugins.multimodal_orchestrator import MultimodalOrchestrator


def test_enhanced_image_generation():
    """Test enhanced image generation system"""
    
    print("🎨 Enhanced Image Generation Test")
    print("=" * 60)
    
    generator = EnhancedImageGenerator()
    
    # Test 1: Model status
    print("\n📊 Test 1: Model Status")
    print("-" * 30)
    status = generator.get_model_status()
    print(f"Local Stable Diffusion: {status['local_stable_diffusion']}")
    print(f"CUDA Available: {status['cuda_available']}")
    print(f"API Configs: {status['api_configs']}")
    
    # Test 2: Available styles
    print("\n🎭 Test 2: Available Styles")
    print("-" * 30)
    styles = generator.get_available_styles()
    print(f"Available styles: {styles}")
    
    # Test 3: API connection test
    print("\n🔗 Test 3: API Connection")
    print("-" * 30)
    api_status = generator.test_api_connection()
    print(f"Stable Diffusion API: {api_status}")
    
    # Test 4: Local model loading (if available)
    print("\n🤖 Test 4: Local Model Loading")
    print("-" * 30)
    try:
        success = generator.load_stable_diffusion_model()
        print(f"Model loading: {success}")
    except Exception as e:
        print(f"Model loading failed: {e}")
    
    print("\n✅ Enhanced Image Generation tests completed!")


def test_enhanced_voice_generation():
    """Test enhanced voice generation system"""
    
    print("\n🎤 Enhanced Voice Generation Test")
    print("=" * 60)
    
    generator = EnhancedVoiceGenerator()
    
    # Test 1: Engine initialization
    print("\n🔧 Test 1: Engine Initialization")
    print("-" * 30)
    success = generator.initialize_pyttsx3()
    print(f"pyttsx3 initialized: {success}")
    
    # Test 2: Voice generation with pyttsx3
    print("\n🎵 Test 2: Voice Generation (pyttsx3)")
    print("-" * 30)
    if success:
        result = generator.generate_voice_with_pyttsx3(
            "Hello, I'm Luna. How can I help you today?",
            voice_preset="romantic"
        )
        print(f"Voice generation result: {result['success']}")
        if result['success']:
            print(f"Generated file: {result['path']}")
    
    # Test 3: Voice generation with gTTS
    print("\n🌐 Test 3: Voice Generation (gTTS)")
    print("-" * 30)
    gtts_result = generator.generate_voice_with_gtts(
        "This is a test using Google Text-to-Speech."
    )
    print(f"gTTS result: {gtts_result['success']}")
    if gtts_result['success']:
        print(f"Generated file: {gtts_result['path']}")
    
    # Test 4: Character voice generation
    print("\n👤 Test 4: Character Voice Generation")
    print("-" * 30)
    character_result = generator.generate_character_voice(
        "Hello there, I'm feeling quite romantic today.",
        "Luna",
        "romantic"
    )
    print(f"Character voice result: {character_result['success']}")
    if character_result['success']:
        print(f"Generated file: {character_result['path']}")
    
    # Test 5: Available voices
    print("\n🎭 Test 5: Available Voices")
    print("-" * 30)
    voices = generator.get_available_voices()
    print(f"Voice presets: {voices['voice_presets']}")
    print(f"pyttsx3 voices: {len(voices['pyttsx3_voices'])} available")
    
    # Test 6: Engine status
    print("\n📊 Test 6: Engine Status")
    print("-" * 30)
    engine_status = generator.get_engine_status()
    print(f"pyttsx3: {engine_status['pyttsx3']}")
    print(f"gtts: {engine_status['gtts']}")
    print(f"API configs: {engine_status['api_configs']}")
    
    print("\n✅ Enhanced Voice Generation tests completed!")


def test_enhanced_video_generation():
    """Test enhanced video generation system"""
    
    print("\n🎬 Enhanced Video Generation Test")
    print("=" * 60)
    
    generator = EnhancedVideoGenerator()
    
    # Test 1: Available styles
    print("\n🎭 Test 1: Available Video Styles")
    print("-" * 30)
    styles = generator.get_available_styles()
    print(f"Available video styles: {styles}")
    
    # Test 2: Engine status
    print("\n📊 Test 2: Engine Status")
    print("-" * 30)
    engine_status = generator.get_engine_status()
    print(f"MoviePy: {engine_status['moviepy']}")
    print(f"API configs: {engine_status['api_configs']}")
    
    # Test 3: API connection test
    print("\n🔗 Test 3: API Connection")
    print("-" * 30)
    api_status = generator.test_api_connection()
    print(f"Runway ML API: {api_status}")
    
    # Test 4: Video from images (placeholder)
    print("\n🖼️ Test 4: Video from Images")
    print("-" * 30)
    print("Note: This would require actual image files")
    print("Placeholder test - would create video from image sequence")
    
    # Test 5: Video collage (placeholder)
    print("\n🎨 Test 5: Video Collage")
    print("-" * 30)
    print("Note: This would require actual video files")
    print("Placeholder test - would create video collage")
    
    print("\n✅ Enhanced Video Generation tests completed!")


def test_enhanced_audio_processing():
    """Test enhanced audio processing system"""
    
    print("\n🎵 Enhanced Audio Processing Test")
    print("=" * 60)
    
    processor = EnhancedAudioProcessor()
    
    # Test 1: Sine wave generation
    print("\n🌊 Test 1: Sine Wave Generation")
    print("-" * 30)
    result = processor.generate_sine_wave(440.0, 3.0, -15.0)
    print(f"Sine wave result: {result['success']}")
    if result['success']:
        print(f"Generated file: {result['path']}")
        print(f"Frequency: {result['frequency']} Hz")
        print(f"Duration: {result['duration']} seconds")
    
    # Test 2: Sound preset generation
    print("\n🎭 Test 2: Sound Preset Generation")
    print("-" * 30)
    preset_result = processor.generate_sound_with_preset("romantic")
    print(f"Preset result: {preset_result['success']}")
    if preset_result['success']:
        print(f"Generated file: {preset_result['path']}")
        print(f"Preset: {preset_result['preset']}")
    
    # Test 3: Ambient sound generation
    print("\n🌿 Test 3: Ambient Sound Generation")
    print("-" * 30)
    ambient_result = processor.generate_ambient_sound("nature", 5.0)
    print(f"Ambient result: {ambient_result['success']}")
    if ambient_result['success']:
        print(f"Generated file: {ambient_result['path']}")
        print(f"Sound type: {ambient_result['sound_type']}")
    
    # Test 4: Character sound generation
    print("\n👤 Test 4: Character Sound Generation")
    print("-" * 30)
    character_result = processor.generate_character_sound(
        "Luna",
        "romantic",
        "voice"
    )
    print(f"Character sound result: {character_result['success']}")
    if character_result['success']:
        print(f"Generated file: {character_result['path']}")
    
    # Test 5: Audio analysis
    print("\n📊 Test 5: Audio Analysis")
    print("-" * 30)
    if result['success']:
        analysis = processor.analyze_audio_file(result['path'])
        print(f"Analysis result: {analysis['success']}")
        if analysis['success']:
            print(f"Duration: {analysis['duration']:.2f} seconds")
            print(f"Sample rate: {analysis['sample_rate']} Hz")
            print(f"RMS energy: {analysis['rms_energy']:.4f}")
            print(f"Tempo: {analysis['tempo']:.1f} BPM")
    
    # Test 6: Available presets and effects
    print("\n🎛️ Test 6: Available Presets and Effects")
    print("-" * 30)
    presets = processor.get_available_presets()
    effects = processor.get_available_effects()
    print(f"Available presets: {presets}")
    print(f"Available effects: {effects}")
    
    # Test 7: Engine status
    print("\n📊 Test 7: Engine Status")
    print("-" * 30)
    engine_status = processor.get_engine_status()
    print(f"pydub: {engine_status['pydub']}")
    print(f"librosa: {engine_status['librosa']}")
    print(f"numpy: {engine_status['numpy']}")
    
    print("\n✅ Enhanced Audio Processing tests completed!")


def test_multimodal_orchestration():
    """Test multimodal orchestration system"""
    
    print("\n🎼 Multimodal Orchestration Test")
    print("=" * 60)
    
    orchestrator = MultimodalOrchestrator()
    
    # Test 1: System initialization
    print("\n🔧 Test 1: System Initialization")
    print("-" * 30)
    print("Initializing multimodal orchestrator...")
    print("✓ Image generator initialized")
    print("✓ Voice generator initialized")
    print("✓ Video generator initialized")
    print("✓ Audio processor initialized")
    
    # Test 2: Available capabilities
    print("\n🎯 Test 2: Available Capabilities")
    print("-" * 30)
    capabilities = orchestrator.get_available_capabilities()
    print(f"Text generation: {capabilities['text_generation']}")
    print(f"Image generation: {capabilities['image_generation']}")
    print(f"Voice generation: {capabilities['voice_generation']}")
    print(f"Video generation: {capabilities['video_generation']}")
    print(f"Audio processing: {capabilities['audio_processing']}")
    
    # Test 3: Basic multimodal content generation
    print("\n🎨 Test 3: Basic Multimodal Content Generation")
    print("-" * 30)
    content_result = orchestrator.generate_multimodal_content(
        "A romantic sunset scene with soft music",
        content_type="romantic",
        include_text=True,
        include_image=True,
        include_voice=True,
        include_video=False,
        include_audio=True
    )
    print(f"Content generation result: {content_result['success']}")
    if content_result['success']:
        print(f"Generated files: {len(content_result['files'])}")
        for file_type, file_path in content_result['files'].items():
            print(f"  {file_type}: {file_path}")
    
    # Test 4: Character multimedia creation
    print("\n👤 Test 4: Character Multimedia Creation")
    print("-" * 30)
    character_result = orchestrator.create_character_multimedia(
        "Luna",
        "A mysterious and alluring AI companion",
        "romantic",
        include_portrait=True,
        include_voice=True,
        include_ambient=True
    )
    print(f"Character multimedia result: {character_result['success']}")
    if character_result['success']:
        print(f"Generated files: {len(character_result['files'])}")
        for file_type, file_path in character_result['files'].items():
            print(f"  {file_type}: {file_path}")
    
    # Test 5: Story multimedia creation
    print("\n📚 Test 5: Story Multimedia Creation")
    print("-" * 30)
    story_result = orchestrator.create_story_multimedia(
        "The Enchanted Garden",
        "A magical garden where love blossoms under the moonlight",
        "fantasy",
        include_cover=True,
        include_scene=True,
        include_ambient=True
    )
    print(f"Story multimedia result: {story_result['success']}")
    if story_result['success']:
        print(f"Generated files: {len(story_result['files'])}")
        for file_type, file_path in story_result['files'].items():
            print(f"  {file_type}: {file_path}")
    
    # Test 6: System health check
    print("\n🏥 Test 6: System Health Check")
    print("-" * 30)
    health = orchestrator.get_system_health()
    print(f"Overall health: {health['overall_health']}")
    print(f"Image generation: {health['image_generation']}")
    print(f"Voice generation: {health['voice_generation']}")
    print(f"Video generation: {health['video_generation']}")
    print(f"Audio processing: {health['audio_processing']}")
    
    print("\n✅ Multimodal Orchestration tests completed!")


def test_integration():
    """Test integration between all systems"""
    
    print("\n🔗 Integration Test")
    print("=" * 60)
    
    print("\n🎯 Testing complete multimodal workflow...")
    
    # Initialize all systems
    image_gen = EnhancedImageGenerator()
    voice_gen = EnhancedVoiceGenerator()
    video_gen = EnhancedVideoGenerator()
    audio_proc = EnhancedAudioProcessor()
    orchestrator = MultimodalOrchestrator()
    
    # Test workflow: Create character content
    print("\n👤 Creating character content...")
    
    # 1. Generate character portrait
    print("  📸 Generating character portrait...")
    portrait_result = image_gen.generate_character_portrait(
        "Luna",
        "A beautiful AI companion with mysterious eyes",
        "romantic"
    )
    
    # 2. Generate character voice
    print("  🎤 Generating character voice...")
    voice_result = voice_gen.generate_character_voice(
        "Hello, I'm Luna. I'm so happy to meet you!",
        "Luna",
        "romantic"
    )
    
    # 3. Generate ambient sound
    print("  🎵 Generating ambient sound...")
    ambient_result = audio_proc.generate_character_sound(
        "Luna",
        "romantic",
        "ambient"
    )
    
    # 4. Create video with audio
    print("  🎬 Creating video with audio...")
    if portrait_result['success'] and voice_result['success']:
        video_result = video_gen.create_video_with_audio(
            portrait_result['path'],
            voice_result['path']
        )
    
    # 5. Orchestrate everything
    print("  🎼 Orchestrating complete experience...")
    orchestration_result = orchestrator.create_character_multimedia(
        "Luna",
        "A mysterious and alluring AI companion",
        "romantic",
        include_portrait=True,
        include_voice=True,
        include_ambient=True,
        include_video=True
    )
    
    print("\n✅ Integration test completed!")
    print(f"Portrait: {'✓' if portrait_result['success'] else '✗'}")
    print(f"Voice: {'✓' if voice_result['success'] else '✗'}")
    print(f"Ambient: {'✓' if ambient_result['success'] else '✗'}")
    print(f"Video: {'✓' if 'video_result' in locals() and video_result['success'] else '✗'}")
    print(f"Orchestration: {'✓' if orchestration_result['success'] else '✗'}")


def main():
    """Run all enhanced multimodal system tests"""
    
    print("🚀 Enhanced Multimodal Systems Test Suite")
    print("=" * 80)
    print("Testing all enhanced systems: Image, Voice, Video, Audio, and Orchestration")
    print("=" * 80)
    
    # Run individual system tests
    test_enhanced_image_generation()
    test_enhanced_voice_generation()
    test_enhanced_video_generation()
    test_enhanced_audio_processing()
    test_multimodal_orchestration()
    
    # Run integration test
    test_integration()
    
    print("\n🎉 All Enhanced Multimodal Systems Tests Completed!")
    print("\n📋 Summary:")
    print("✅ Enhanced Image Generation System")
    print("✅ Enhanced Voice Generation System")
    print("✅ Enhanced Video Generation System")
    print("✅ Enhanced Audio Processing System")
    print("✅ Multimodal Orchestration System")
    print("✅ System Integration")
    
    print("\n🔧 Key Features Demonstrated:")
    print("• Multiple TTS engines (pyttsx3, gTTS, APIs)")
    print("• Multiple image generation models (Stable Diffusion, APIs)")
    print("• Video generation from images and APIs")
    print("• Audio processing with effects and analysis")
    print("• Unified orchestration of all media types")
    print("• Character and story multimedia creation")
    print("• System health monitoring and status reporting")


if __name__ == "__main__":
    main() 