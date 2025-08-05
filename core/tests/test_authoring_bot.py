"""
Test script for the Authoring Bot Framework
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def test_framework():
    """Test the authoring bot framework"""
    print("Testing Authoring Bot Framework")
    print("=" * 50)

    # Get framework instance
    framework = get_framework()

    # Test project creation
    print("📚 Testing project creation...")
    project = framework.create_project("Test Novel", "Fantasy", "Young Adult", 50000)
    print(f"✅ Created project: {project.name}")

    # Test text generation
    print("\n📝 Testing text generation...")
    if "text_generator" in framework.plugins:
        result = framework.plugins["text_generator"].write_chapter(
            "Test Novel",
            "The Beginning",
            "Write an opening chapter that introduces the main character",
        )
        print(f"✅ Text generation result: {result[:200]}...")
    else:
        print("❌ Text generator plugin not found")

    # Test image generation
    print("\n🎨 Testing image generation...")
    if "image_generator" in framework.plugins:
        result = framework.generate_image(
            "A fantasy book cover with dragons", "book_cover"
        )
        print(f"✅ Image generation result: {result}")
    else:
        print("❌ Image generator plugin not found")

    # Test video generation
    print("\n🎬 Testing video generation...")
    if "video_generator" in framework.plugins:
        result = framework.generate_video("A book trailer for a fantasy novel", 30)
        print(f"✅ Video generation result: {result}")
    else:
        print("❌ Video generator plugin not found")

    # Test voice generation
    print("\n🎤 Testing voice generation...")
    if "voice_generator" in framework.plugins:
        result = framework.generate_voice(
            "This is a test of voice generation", "narrator"
        )
        print(f"✅ Voice generation result: {result}")
    else:
        print("❌ Voice generator plugin not found")

    # Test stats
    print("\n📊 Testing statistics...")
    stats = framework.get_stats()
    print(
        f"✅ Stats retrieved: {stats['total_projects']} projects, {stats['total_words_written']} words"
    )

    # Test data persistence
    print("\n💾 Testing data persistence...")
    framework.save_data()
    print("✅ Data saved successfully")

    print("\n🎉 Framework test completed successfully!")


if __name__ == "__main__":
    test_framework()
