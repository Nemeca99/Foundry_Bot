#!/usr/bin/env python3
"""
Test script for Content-Driven Personality Engine
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.plugins.content_driven_personality import (
    ContentDrivenPersonality,
    initialize,
)


def test_content_driven_personality():
    """Test the content-driven personality engine"""
    print("🧠 Testing Content-Driven Personality Engine")
    print("=" * 50)

    # Initialize the engine
    personality_engine = initialize()

    # Test content with different personality traits
    test_content = """
    Shay was a fierce warrior, burning with passion and determination. 
    She felt the fire of vengeance coursing through her veins, 
    a deep and intense anger that drove her forward. 
    She was independent and strong, refusing to submit to anyone. 
    Her creative spirit shone through in her storytelling, 
    as she wove tales of adventure and heroism. 
    She was analytical in her approach to combat, 
    always thinking several steps ahead.
    """

    print("📖 Analyzing content for personality traits...")
    content_personality = personality_engine.analyze_content_for_personality(
        test_content, "shay_test"
    )

    print(f"Content ID: {content_personality.content_id}")
    print(f"Dominant traits: {content_personality.dominant_traits}")
    print(f"Personality summary: {content_personality.personality_summary}")

    print("\n🔍 Extracted traits:")
    for trait in content_personality.traits:
        print(
            f"- {trait.name} ({trait.trait_type.value}): {trait.strength:.2f} confidence: {trait.confidence:.2f}"
        )

    print("\n🔄 Evolving personality from content...")
    evolution = personality_engine.evolve_personality_from_content(
        test_content, "shay_test"
    )

    print("Personality changes:")
    for trait, influence in evolution.content_influence.items():
        print(f"- {trait}: +{influence:.2f}")

    print("\n📊 Current personality summary:")
    print(personality_engine.get_personality_summary())

    print("\n✅ Content-driven personality test completed successfully!")


def test_become_living_manual():
    """Test the 'become living manual' functionality"""
    print("\n🎭 Testing 'Become Living Manual' Functionality")
    print("=" * 50)

    personality_engine = initialize()

    # Test content that should make the AI become more creative and passionate
    creative_content = """
    The artist's soul burned with an unquenchable fire of creativity. 
    Every brushstroke was a dance of imagination and beauty. 
    The world was a canvas waiting to be transformed by vision and passion. 
    Stories flowed like rivers of inspiration, each word a spark of genius. 
    The creative spirit soared on wings of innovation and artistic sensitivity.
    """

    print("🎨 Making AI become the living manual of creative content...")
    result = personality_engine.become_living_manual(creative_content, "creative_test")
    print(result)

    print("\n📊 Updated personality summary:")
    print(personality_engine.get_personality_summary())

    print("\n✅ 'Become living manual' test completed successfully!")


def test_with_real_book_content():
    """Test with actual book content from the collection"""
    print("\n📚 Testing with Real Book Content")
    print("=" * 50)

    personality_engine = initialize()

    # Read content from Shay's story
    book_path = (
        Path(__file__).parent.parent.parent
        / "Book_Collection"
        / "Relic"
        / "Chapter_1.txt"
    )

    if book_path.exists():
        with open(book_path, "r", encoding="utf-8") as f:
            book_content = f.read()

        print("📖 Analyzing Shay's story for personality traits...")
        content_personality = personality_engine.analyze_content_for_personality(
            book_content, "shay_story"
        )

        print(
            f"Dominant traits from Shay's story: {content_personality.dominant_traits}"
        )
        print(f"Personality summary: {content_personality.personality_summary}")

        print("\n🔄 Evolving personality from Shay's story...")
        evolution = personality_engine.evolve_personality_from_content(
            book_content, "shay_story"
        )

        print("Personality changes from Shay's story:")
        for trait, influence in evolution.content_influence.items():
            print(f"- {trait}: +{influence:.2f}")

        print("\n📊 Final personality summary:")
        print(personality_engine.get_personality_summary())

        print("\n✅ Real book content test completed successfully!")
    else:
        print("❌ Book content not found, skipping real content test")


def test_personality_evolution_history():
    """Test personality evolution history tracking"""
    print("\n📈 Testing Personality Evolution History")
    print("=" * 50)

    personality_engine = initialize()

    # Add multiple content pieces to see evolution
    content_pieces = [
        (
            "passionate_content",
            "She was passionate and intense, burning with desire and fire.",
        ),
        (
            "analytical_content",
            "He was analytical and logical, always thinking and reasoning carefully.",
        ),
        (
            "creative_content",
            "The artist was creative and imaginative, full of innovation and beauty.",
        ),
    ]

    for content_id, content in content_pieces:
        print(f"\n🔄 Evolving from {content_id}...")
        evolution = personality_engine.evolve_personality_from_content(
            content, content_id
        )
        print(f"Changes: {len(evolution.content_influence)} traits influenced")

    print("\n📊 Current personality after multiple evolutions:")
    print(personality_engine.get_personality_summary())

    print("\n📜 Evolution history:")
    history = personality_engine.get_evolution_history()
    for i, entry in enumerate(history):
        print(
            f"Stage {i+1}: {entry['content_id']} - {len(entry['traits_learned'])} traits learned"
        )

    print("\n✅ Personality evolution history test completed successfully!")


if __name__ == "__main__":
    print("🧠 Content-Driven Personality Engine Test Suite")
    print("=" * 60)

    try:
        test_content_driven_personality()
        test_become_living_manual()
        test_with_real_book_content()
        test_personality_evolution_history()

        print("\n🎉 All tests completed successfully!")
        print("The Content-Driven Personality Engine is working correctly.")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
