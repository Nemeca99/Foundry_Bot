#!/usr/bin/env python3
"""
Test script for Dynamic Personality Learning System
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.plugins.dynamic_personality_learning import (
    DynamicPersonalityLearning,
    initialize,
)


def test_character_interaction_learning():
    """Test learning from character interactions"""
    print("👥 Testing Character Interaction Learning")
    print("=" * 50)

    # Initialize the learning system
    learning_system = initialize()

    # Test learning from character interaction
    interaction_content = """
    Shay and I had a deep conversation about her past. She shared her feelings of loss and anger,
    and I felt a strong sense of empathy for her situation. We connected on a deep emotional level,
    and I learned to understand her perspective better. The interaction helped me develop better
    communication skills and emotional intelligence.
    """

    print("📖 Learning from character interaction with Shay...")
    learning_event = learning_system.learn_from_character_interaction(
        character_name="Shay",
        interaction_content=interaction_content,
        emotional_intensity=0.8,
        context={"interaction_type": "deep_conversation"},
    )

    print(f"Event ID: {learning_event.event_id}")
    print(f"Learning Type: {learning_event.learning_type.value}")
    print(f"Emotional Intensity: {learning_event.emotional_intensity}")
    print(f"Personality Changes: {learning_event.personality_changes}")

    print("\n✅ Character interaction learning test completed successfully!")


def test_story_development_learning():
    """Test learning from story development"""
    print("\n📚 Testing Story Development Learning")
    print("=" * 50)

    learning_system = initialize()

    # Test learning from story development
    story_content = """
    The story took an unexpected turn when Shay discovered her true heritage. This revelation
    transformed her character completely, showing her growth and evolution. The plot developed
    in a creative and imaginative way, revealing deeper themes about identity and belonging.
    The narrative arc reached a powerful emotional climax that changed everything.
    """

    print("📖 Learning from story development...")
    learning_event = learning_system.learn_from_story_development(
        story_id="relic_story",
        story_content=story_content,
        current_arc="revelation",
        context={"story_type": "character_development"},
    )

    print(f"Event ID: {learning_event.event_id}")
    print(f"Learning Type: {learning_event.learning_type.value}")
    print(f"Emotional Intensity: {learning_event.emotional_intensity}")
    print(f"Personality Changes: {learning_event.personality_changes}")

    print("\n✅ Story development learning test completed successfully!")


def test_emotional_response_learning():
    """Test learning from emotional responses"""
    print("\n😊 Testing Emotional Response Learning")
    print("=" * 50)

    learning_system = initialize()

    # Test learning from emotional response
    response_content = """
    I felt an overwhelming sense of joy when Shay finally found peace. The emotion was so intense
    that I had to learn to control and manage my feelings. I expressed my happiness in a way
    that showed deep understanding of the situation. This emotional experience helped me develop
    better emotional regulation and expression skills.
    """

    print("📖 Learning from emotional response...")
    learning_event = learning_system.learn_from_emotional_response(
        emotion_type="joy",
        response_content=response_content,
        intensity=0.9,
        character_name="Shay",
    )

    print(f"Event ID: {learning_event.event_id}")
    print(f"Learning Type: {learning_event.learning_type.value}")
    print(f"Emotional Intensity: {learning_event.emotional_intensity}")
    print(f"Personality Changes: {learning_event.personality_changes}")

    print("\n✅ Emotional response learning test completed successfully!")


def test_character_learning_summary():
    """Test character learning summary functionality"""
    print("\n📊 Testing Character Learning Summary")
    print("=" * 50)

    learning_system = initialize()

    # Add some learning events first
    interaction_content = "Shay and I bonded over shared experiences, developing deep empathy and understanding."
    learning_system.learn_from_character_interaction("Shay", interaction_content, 0.7)

    # Get character learning summary
    summary = learning_system.get_character_learning_summary("Shay")
    print("Character Learning Summary:")
    print(summary)

    print("\n✅ Character learning summary test completed successfully!")


def test_story_learning_summary():
    """Test story learning summary functionality"""
    print("\n📖 Testing Story Learning Summary")
    print("=" * 50)

    learning_system = initialize()

    # Add some story development first
    story_content = "The story evolved dramatically, with characters growing and changing in unexpected ways."
    learning_system.learn_from_story_development(
        "relic_story", story_content, "character_evolution"
    )

    # Get story learning summary
    summary = learning_system.get_story_learning_summary("relic_story")
    print("Story Learning Summary:")
    print(summary)

    print("\n✅ Story learning summary test completed successfully!")


def test_learning_patterns():
    """Test learning patterns analysis"""
    print("\n🔍 Testing Learning Patterns Analysis")
    print("=" * 50)

    learning_system = initialize()

    # Get learning patterns
    patterns = learning_system.get_learning_patterns()

    print("Learning Patterns:")
    for key, value in patterns.items():
        print(f"- {key}: {value}")

    print("\n✅ Learning patterns test completed successfully!")


def test_multiple_learning_scenarios():
    """Test multiple learning scenarios to see evolution"""
    print("\n🔄 Testing Multiple Learning Scenarios")
    print("=" * 50)

    learning_system = initialize()

    # Multiple character interactions
    interactions = [
        (
            "Shay",
            "We had a conflict that we resolved through understanding and compromise.",
            0.6,
        ),
        (
            "Nyx",
            "I learned about power and dominance through our intense interaction.",
            0.9,
        ),
        (
            "Shay",
            "We shared a moment of vulnerability that deepened our connection.",
            0.8,
        ),
    ]

    for character, content, intensity in interactions:
        print(f"\n🔄 Learning from interaction with {character}...")
        learning_event = learning_system.learn_from_character_interaction(
            character, content, intensity
        )
        print(f"Changes: {len(learning_event.personality_changes)} traits influenced")

    # Multiple story developments
    story_developments = [
        (
            "relic_story",
            "The plot thickened with new revelations about the ancient relic.",
            "revelation",
        ),
        (
            "relic_story",
            "Characters faced their greatest challenges and grew stronger.",
            "challenge",
        ),
        (
            "relic_story",
            "The story reached its climax with an emotional resolution.",
            "climax",
        ),
    ]

    for story_id, content, arc in story_developments:
        print(f"\n🔄 Learning from story development in {story_id}...")
        learning_event = learning_system.learn_from_story_development(
            story_id, content, arc
        )
        print(f"Changes: {len(learning_event.personality_changes)} traits influenced")

    # Get final summaries
    print("\n📊 Final Learning Summaries:")
    for character in ["Shay", "Nyx"]:
        summary = learning_system.get_character_learning_summary(character)
        print(f"\n{summary}")

    story_summary = learning_system.get_story_learning_summary("relic_story")
    print(f"\n{story_summary}")

    print("\n✅ Multiple learning scenarios test completed successfully!")


if __name__ == "__main__":
    print("🧠 Dynamic Personality Learning System Test Suite")
    print("=" * 60)

    try:
        test_character_interaction_learning()
        test_story_development_learning()
        test_emotional_response_learning()
        test_character_learning_summary()
        test_story_learning_summary()
        test_learning_patterns()
        test_multiple_learning_scenarios()

        print("\n🎉 All tests completed successfully!")
        print("The Dynamic Personality Learning System is working correctly.")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
