#!/usr/bin/env python3
"""
Test Personality Engine Plugin
Tests Luna's personality and learning capabilities
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def test_personality_engine():
    """Test the personality engine plugin"""
    print("Testing Personality Engine Plugin")
    print("=" * 50)

    try:
        # Get framework
        framework = get_framework()
        print("Framework loaded")

        # Get personality engine plugin
        personality_engine = framework.get_plugin("personality_engine")
        if not personality_engine:
            print("Personality Engine plugin not found")
            return False

        print("Personality Engine plugin loaded")

        # Test personality summary
        print("\nTesting personality summary...")
        summary = personality_engine.get_personality_summary()
        print(f"Personality summary generated ({len(summary)} characters)")
        print(f"   Preview: {summary[:100]}...")

        # Test personality context
        print("\nTesting personality context...")
        context = personality_engine.get_personality_context()
        print(f"Personality context generated ({len(context)} characters)")
        print(f"   Preview: {context[:100]}...")

        # Test learning from interaction
        print("\nTesting learning from interaction...")
        user_message = "I want to write a fantasy story about dragons and magic"
        bot_response = (
            "That sounds amazing! Let's create something incredible together!"
        )
        personality_engine.learn_from_interaction(
            user_message, bot_response, "story_planning"
        )
        print("Learned from interaction")

        # Test response adaptation
        print("\nTesting response adaptation...")
        base_response = "Here's a great idea for your fantasy story"
        adapted_response = personality_engine.generate_personality_response(
            base_response, user_message, "story_planning"
        )
        print(f"Response adapted ({len(adapted_response)} characters)")
        print(f"   Original: {base_response}")
        print(f"   Adapted: {adapted_response[:100]}...")

        # Test personality stats
        print("\nTesting personality stats...")
        stats = personality_engine.get_personality_stats()
        print(f"Personality stats generated")
        print(f"   Name: {stats['personality_name']}")
        print(f"   Traits: {len(stats['core_traits'])} traits")
        print(
            f"   Conversation patterns: {len(stats['conversation_patterns'])} patterns"
        )
        print(f"   User preferences: {len(stats['user_preferences'])} preferences")

        # Test personality evolution
        print("\nTesting personality evolution...")
        personality_engine.evolve_personality()
        print("Personality evolved")

        # Test with different user styles
        print("\nTesting different user styles...")

        # Formal user
        formal_message = "I would like to request assistance with character development for my novel."
        formal_response = personality_engine.generate_personality_response(
            "Here's a character development approach",
            formal_message,
            "character_development",
        )
        print(f"Formal style adaptation: {formal_response[:80]}...")

        # Casual user
        casual_message = "Hey! Can you help me brainstorm some cool plot ideas? 😊"
        casual_response = personality_engine.generate_personality_response(
            "Here are some plot ideas", casual_message, "brainstorming"
        )
        print(f"Casual style adaptation: {casual_response[:80]}...")

        # Learn from multiple interactions
        print("\nTesting multiple learning interactions...")
        interactions = [
            ("I love writing fantasy!", "Fantasy is amazing!", "enthusiasm"),
            ("This is really hard", "You can do it!", "encouragement"),
            ("I have a new idea", "That's brilliant!", "excitement"),
            ("Can you help me?", "Of course!", "support"),
        ]

        for user_msg, bot_resp, context in interactions:
            personality_engine.learn_from_interaction(user_msg, bot_resp, context)

        print("Learned from multiple interactions")

        # Test final stats
        print("\nTesting final learning stats...")
        final_stats = personality_engine.get_personality_stats()
        if final_stats["conversation_patterns"]:
            patterns = final_stats["conversation_patterns"]
            print(
                f"   Average message length: {patterns.get('avg_message_length', 0):.0f}"
            )
            print(f"   Emoji frequency: {patterns.get('emoji_frequency', 0)*100:.1f}%")
            print(f"   Formality level: {patterns.get('formality_level', 0)*100:.1f}%")

        if final_stats["user_preferences"]:
            print(
                f"   Top preferences: {list(final_stats['user_preferences'].keys())[:3]}"
            )

        print("\nAll Personality Engine tests completed successfully!")
        print("Luna is ready to be your AI writing partner!")
        return True

    except Exception as e:
        print(f"Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_personality_engine()
    sys.exit(0 if success else 1)
