#!/usr/bin/env python3
"""
Test script for Qwen3-8B model connection
"""

import sys
import requests
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def test_model_connection():
    """Test connection to Qwen3-8B model"""
    print("Testing Qwen3-8B Model Connection...")
    print("=" * 50)

    # Initialize framework
    framework = get_framework()
    config = framework.config

    print(f"Configuration:")
    print(f"   Model URL: {config['ollama_url']}")
    print(f"   Model Name: {config['ollama_model']}")
    print(f"   Max Tokens: {config['max_tokens']}")
    print(f"   Temperature: {config['temperature']}")
    print()

    # Test basic connection
    try:
        # Test if server is reachable
        response = requests.get(f"{config['ollama_url']}/api/tags", timeout=10)
        if response.status_code == 200:
            print("LM Studio server is reachable")

            # Check available models
            models = response.json()
            print(f"📋 Available models: {len(models.get('models', []))}")
            for model in models.get("models", []):
                print(f"   - {model.get('name', 'Unknown')}")
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to LM Studio server: {e}")
        return False

    # Test text generation
    print(f"\n🧪 Testing text generation...")

    try:
        if "text_generator" in framework.plugins:
            text_gen = framework.plugins["text_generator"]

            # Simple test prompt
            test_prompt = "Write a short paragraph about a mysterious forest."

            print(f"📝 Test prompt: {test_prompt}")
            print("⏳ Generating response...")

            response = text_gen.generate_text(test_prompt)

            if response:
                print("✅ Text generation successful!")
                print(f"📄 Response (first 200 chars): {response[:200]}...")
                print(f"📊 Response length: {len(response)} characters")
            else:
                print("❌ Text generation failed - no response received")
                return False

        else:
            print("❌ Text generator plugin not available")
            return False

    except Exception as e:
        print(f"❌ Text generation test failed: {e}")
        return False

    # Test authoring-specific generation
    print(f"\n📚 Testing authoring capabilities...")

    try:
        if "text_generator" in framework.plugins:
            text_gen = framework.plugins["text_generator"]

            # Test character development
            print("👤 Testing character development...")
            character_result = text_gen.develop_character(
                "Test Project",
                "Luna",
                "A mysterious young woman with magical abilities",
            )

            if character_result:
                print("✅ Character development successful!")
                print(
                    f"📄 Character profile (first 200 chars): {character_result[:200]}..."
                )
            else:
                print("❌ Character development failed")

            # Test chapter writing
            print("\n📝 Testing chapter writing...")
            chapter_result = text_gen.write_chapter(
                "Test Project",
                "The Beginning",
                "Write an opening chapter that introduces the main character in a fantasy setting",
            )

            if chapter_result:
                print("✅ Chapter writing successful!")
                print(
                    f"📄 Chapter content (first 200 chars): {chapter_result[:200]}..."
                )
            else:
                print("❌ Chapter writing failed")

    except Exception as e:
        print(f"❌ Authoring test failed: {e}")
        return False

    print(f"\n🎉 Model connection test completed successfully!")
    print(f"✅ Qwen3-8B is ready for authoring tasks!")
    return True


if __name__ == "__main__":
    test_model_connection()
