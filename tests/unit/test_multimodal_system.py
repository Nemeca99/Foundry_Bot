#!/usr/bin/env python3
"""
Test script for Multimodal System
Demonstrates text, image, voice, video, and audio generation capabilities
"""

import asyncio
import sys
import os
from pathlib import Path

# Add framework to path
sys.path.append(str(Path(__file__).parent / "framework"))
from framework_tool import get_framework

async def test_multimodal_system():
    """Test the multimodal system"""
    
    print("🎭 Multimodal System Test")
    print("=" * 50)
    
    # Initialize framework
    framework = get_framework()
    
    # Get the multimodal orchestrator
    multimodal = framework.get_plugin('multimodal_orchestrator')
    
    if not multimodal:
        print("❌ Multimodal orchestrator not found!")
        return
    
    print("✅ Multimodal orchestrator loaded")
    
    # Test 1: Basic multimodal content generation
    print("\n📝 Test 1: Basic Multimodal Content Generation")
    print("-" * 40)
    
    test_prompt = "A romantic sunset scene with two lovers"
    results = await multimodal.generate_multimodal_content(
        text_prompt=test_prompt,
        media_types=["text", "image", "voice"],
        style="romantic"
    )
    
    print(f"Prompt: {test_prompt}")
    print(f"Style: romantic")
    print(f"Media Types: text, image, voice")
    
    for media_type, result in results.items():
        print(f"\n{media_type.upper()}:")
        if isinstance(result, dict):
            if result.get('success'):
                print(f"  ✅ Success: {result.get('path', 'Generated')}")
                if 'prompt' in result:
                    print(f"  📝 Prompt: {result['prompt'][:100]}...")
            else:
                print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"  📄 Content: {str(result)[:100]}...")
    
    # Test 2: Character multimedia creation
    print("\n🎭 Test 2: Character Multimedia Creation")
    print("-" * 40)
    
    eve_character_data = {
        "description": "A beautiful AI woman with long dark hair, mysterious green eyes, and an elegant presence",
        "voice_description": "I am Eve, an AI with deep emotional intelligence and a mysterious past",
        "style": "romantic",
        "voice_style": "mysterious"
    }
    
    character_results = await multimodal.create_character_multimedia(
        character_name="Eve",
        character_data=eve_character_data,
        media_types=["image", "voice", "text"]
    )
    
    print(f"Character: Eve")
    print(f"Style: {eve_character_data['style']}")
    
    for media_type, result in character_results.items():
        print(f"\n{media_type.replace('_', ' ').title()}:")
        if isinstance(result, dict):
            if result.get('success'):
                print(f"  ✅ Success: {result.get('path', 'Generated')}")
                if 'prompt' in result:
                    print(f"  📝 Prompt: {result['prompt'][:100]}...")
            else:
                print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"  📄 Content: {str(result)[:100]}...")
    
    # Test 3: Story multimedia creation
    print("\n📚 Test 3: Story Multimedia Creation")
    print("-" * 40)
    
    story_data = {
        "genre": "romance",
        "description": "A passionate love story between a human and an AI",
        "style": "romantic"
    }
    
    story_results = await multimodal.create_story_multimedia(
        story_title="Eve's Awakening",
        story_data=story_data,
        media_types=["image", "video", "text"]
    )
    
    print(f"Story: Eve's Awakening")
    print(f"Genre: {story_data['genre']}")
    
    for media_type, result in story_results.items():
        print(f"\n{media_type.replace('_', ' ').title()}:")
        if isinstance(result, dict):
            if result.get('success'):
                print(f"  ✅ Success: {result.get('path', 'Generated')}")
                if 'prompt' in result:
                    print(f"  📝 Prompt: {result['prompt'][:100]}...")
            else:
                print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"  📄 Content: {str(result)[:100]}...")
    
    # Test 4: Available capabilities
    print("\n🔧 Test 4: Available Capabilities")
    print("-" * 40)
    
    media_types = multimodal.get_available_media_types()
    styles = multimodal.get_available_styles()
    
    print(f"Available Media Types: {', '.join(media_types)}")
    print("\nAvailable Styles:")
    for media_type, style_list in styles.items():
        print(f"  {media_type.title()}: {', '.join(style_list)}")
    
    # Test 5: System test
    print("\n🧪 Test 5: System Test")
    print("-" * 40)
    
    system_test = await multimodal.test_multimodal_system()
    
    print(f"Test Prompt: {system_test['test_prompt']}")
    print(f"Status: {system_test['status']}")
    
    print("\n✅ Multimodal system test completed!")


async def test_stable_diffusion_integration():
    """Test Stable Diffusion integration specifically"""
    
    print("\n🎨 Stable Diffusion Integration Test")
    print("=" * 50)
    
    # Initialize framework
    framework = get_framework()
    multimodal = framework.get_plugin('multimodal_orchestrator')
    
    if not multimodal:
        print("❌ Multimodal orchestrator not found!")
        return
    
    # Test different image styles
    test_prompts = [
        ("A romantic sunset scene", "romantic"),
        ("A fantasy castle in the clouds", "fantasy"),
        ("A modern city skyline", "modern"),
        ("A vintage car on a country road", "vintage"),
        ("An anime character with blue hair", "anime"),
        ("A realistic portrait of a woman", "realistic"),
        ("An artistic interpretation of love", "artistic")
    ]
    
    for prompt, style in test_prompts:
        print(f"\n🎨 Testing: {prompt} (Style: {style})")
        
        result = await multimodal._generate_image_with_stable_diffusion(prompt, style)
        
        if result.get('success'):
            print(f"  ✅ Success: {result.get('path', 'Generated')}")
            print(f"  📏 Size: {result.get('size', 'Unknown')}")
        else:
            print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
    
    print("\n✅ Stable Diffusion integration test completed!")


async def test_voice_generation():
    """Test voice generation capabilities"""
    
    print("\n🎤 Voice Generation Test")
    print("=" * 50)
    
    # Initialize framework
    framework = get_framework()
    multimodal = framework.get_plugin('multimodal_orchestrator')
    
    if not multimodal:
        print("❌ Multimodal orchestrator not found!")
        return
    
    # Test different voice styles
    test_texts = [
        ("Hello, I am Luna, your AI writing partner", "default"),
        ("I want to make love to you right now", "romantic"),
        ("The world is ending and we must act now!", "dramatic"),
        ("Everything will be okay, I promise", "calm"),
        ("This is going to be amazing!", "energetic"),
        ("I have a secret to tell you", "mysterious")
    ]
    
    for text, style in test_texts:
        print(f"\n🎤 Testing: {text[:50]}... (Style: {style})")
        
        result = await multimodal._generate_voice_with_tts(text, style)
        
        if result.get('success'):
            print(f"  ✅ Success: {result.get('path', 'Generated')}")
            print(f"  ⏱️ Duration: {result.get('duration', 'Unknown')}")
        else:
            print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
    
    print("\n✅ Voice generation test completed!")


if __name__ == "__main__":
    print("🚀 Starting Multimodal System Tests")
    print("=" * 60)
    
    # Run all tests
    asyncio.run(test_multimodal_system())
    asyncio.run(test_stable_diffusion_integration())
    asyncio.run(test_voice_generation())
    
    print("\n🎉 All multimodal tests completed!") 