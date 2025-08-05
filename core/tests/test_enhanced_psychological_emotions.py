#!/usr/bin/env python3
"""
Test script for Enhanced Psychological Emotional System
Demonstrates Plutchik's wheel of emotions and Maslow's hierarchy integration
"""

import sys
import os
from pathlib import Path

# Add astra_emotional_fragments to path
sys.path.append(str(Path(__file__).parent / "astra_emotional_fragments"))

from emotional_blender import EnhancedEmotionalBlender
from dynamic_emotion_engine import EnhancedDynamicEmotionEngine


def test_enhanced_emotional_blender():
    """Test the enhanced emotional blender with psychological models"""

    print("🧠 Enhanced Emotional Blender Test")
    print("=" * 60)

    blender = EnhancedEmotionalBlender()

    # Test 1: Psychological analysis of emotions
    print("\n📊 Test 1: Psychological Analysis of Emotions")
    print("-" * 50)

    test_emotions = ["happy", "lustful", "anxious", "confident", "obsessed"]

    for emotion in test_emotions:
        print(f"\n🎭 Analyzing: {emotion}")

        # Plutchik analysis
        plutchik_analysis = blender.analyze_plutchik_emotion(emotion)
        print(f"  Plutchik: {plutchik_analysis.get('primary_emotion', 'Unknown')}")
        print(f"  Opposite: {plutchik_analysis.get('opposite', 'None')}")

        # Maslow analysis
        maslow_analysis = blender.analyze_maslow_needs(emotion)
        print(f"  Maslow Level: {maslow_analysis.get('maslow_level', 'Unknown')}")
        print(f"  Related Needs: {', '.join(maslow_analysis.get('needs', []))}")

        # Intensity analysis
        intensity_analysis = blender.calculate_emotional_intensity(emotion)
        print(
            f"  Intensity: {intensity_analysis.get('level', 'Unknown')} ({intensity_analysis.get('intensity', 0):.2f})"
        )

    # Test 2: Psychologically realistic emotion blending
    print("\n🔄 Test 2: Psychologically Realistic Emotion Blending")
    print("-" * 50)

    blend_scenarios = [
        ("happy", ["lustful"], "Joyful desire with physical attraction"),
        ("melancholic", ["lustful"], "Melancholic desire with physical longing"),
        ("anxious", ["excited"], "Nervous excitement with safety concerns"),
        ("jealous", ["protective"], "Possessive protection with esteem threat"),
        ("grateful", ["submissive"], "Thankful surrender with appreciation"),
    ]

    for primary, secondary, description in blend_scenarios:
        print(f"\n🔄 Blending: {primary} + {secondary}")
        print(f"  Description: {description}")

        blended = blender.blend_emotions_with_psychology(primary, secondary)

        print(f"  Result: {blended['name']}")
        print(f"  Description: {blended['description']}")

        # Show psychological analysis
        psych_analysis = blended["psychological_analysis"]
        print(f"  Plutchik: {psych_analysis['plutchik']['primary_emotion']}")
        print(f"  Maslow: {psych_analysis['maslow']['maslow_level']}")
        print(
            f"  Complexity: {psych_analysis['complexity']['level']} ({psych_analysis['complexity']['score']:.2f})"
        )

    # Test 3: Psychological profile matching
    print("\n🎯 Test 3: Psychological Profile Matching")
    print("-" * 50)

    # Find high-intensity trust emotions
    high_trust_emotions = blender.get_emotion_by_psychological_profile(
        plutchik_emotion="trust", intensity_level="intense"
    )
    print(f"High-intensity trust emotions: {high_trust_emotions}")

    # Find love/belonging emotions
    love_emotions = blender.get_emotion_by_psychological_profile(
        maslow_level="love_belonging"
    )
    print(f"Love/belonging emotions: {love_emotions}")

    # Find complex emotions
    complex_emotions = []
    for emotion_name in blender.fragments.keys():
        analysis = blender.blend_emotions_with_psychology(emotion_name, [])
        if analysis["psychological_analysis"]["complexity"]["level"] == "complex":
            complex_emotions.append(emotion_name)
    print(f"Complex emotions: {complex_emotions}")


def test_enhanced_dynamic_emotion_engine():
    """Test the enhanced dynamic emotion engine with psychological models"""

    print("\n🧠 Enhanced Dynamic Emotion Engine Test")
    print("=" * 60)

    engine = EnhancedDynamicEmotionEngine()

    # Test 1: Psychological context detection
    print("\n📊 Test 1: Psychological Context Detection")
    print("-" * 50)

    test_scenarios = [
        ("I want you so badly right now...", "Romantic, high intensity"),
        ("What should we have for dinner tonight?", "Casual, low intensity"),
        ("I need help with my novel's plot", "Creative, medium intensity"),
        ("I'm feeling really stressed about work", "Serious, high intensity"),
        ("The sunset is so beautiful today", "Casual, low intensity"),
        ("I trust you completely", "Intimate, medium intensity"),
    ]

    for message, expected in test_scenarios:
        print(f"\n💬 User: {message}")
        print(f"  Expected: {expected}")

        context = engine.detect_context_change(message)
        print(f"  Detected Topics: {context['topics']}")
        print(f"  Intensity: {context['intensity']}")
        print(f"  Psychological Context: {context['psychological_context']}")

    # Test 2: Psychologically realistic transitions
    print("\n🔄 Test 2: Psychologically Realistic Transitions")
    print("-" * 50)

    transition_scenarios = [
        ("I want you so badly right now...", "Romantic → Intimate"),
        ("What should we have for dinner tonight?", "Casual → Relaxed"),
        ("I need help with my novel's plot", "Creative → Excited"),
        ("I'm feeling really stressed about work", "Serious → Concerned"),
        ("The sunset is so beautiful today", "Casual → Appreciative"),
    ]

    for message, expected_transition in transition_scenarios:
        print(f"\n💬 User: {message}")
        print(f"  Expected: {expected_transition}")

        context_switch = engine.handle_psychologically_realistic_context_switch(message)
        response = engine.generate_psychologically_realistic_response(
            message, context_switch
        )

        print(f"  AI Response: {response}")
        print(f"  Emotion: {engine.current_emotion}")
        print(f"  Action: {context_switch['action']}")

        if "transition" in context_switch:
            transition = context_switch["transition"]
            print(f"  From: {transition.get('from_emotion', 'None')}")
            print(f"  To: {transition.get('to_emotion', 'None')}")
            print(f"  Complexity: {transition.get('transition_complexity', 'Unknown')}")

    # Test 3: Psychological state tracking
    print("\n📈 Test 3: Psychological State Tracking")
    print("-" * 50)

    # Simulate a conversation that affects psychological state
    conversation = [
        "I want you so badly right now...",
        "What should we have for dinner tonight?",
        "I need help with my novel's plot",
        "I'm feeling really stressed about work",
        "The sunset is so beautiful today",
    ]

    print("Simulating conversation effects on psychological state:")

    for i, message in enumerate(conversation, 1):
        print(f"\n💬 Message {i}: {message}")

        context = engine.detect_context_change(message)
        psychological_context = engine.update_psychological_context(message, context)

        print(f"  Maslow State:")
        for level, state in psychological_context["maslow_state"].items():
            print(
                f"    {level}: satisfied={state['satisfied']}, intensity={state['intensity']:.2f}"
            )

        print(f"  Plutchik State:")
        for emotion, state in psychological_context["plutchik_state"].items():
            print(
                f"    {emotion}: intensity={state['intensity']:.2f}, recent={state['recent']}"
            )

        readiness = psychological_context["readiness"]
        print(
            f"  Readiness: {readiness['readiness_for_change']:.2f} ({readiness['recommended_transition_speed']})"
        )


def test_psychological_complexity():
    """Test psychological complexity analysis"""

    print("\n🧠 Psychological Complexity Analysis")
    print("=" * 60)

    blender = EnhancedEmotionalBlender()

    # Test different complexity scenarios
    complexity_scenarios = [
        {
            "name": "Simple Blend",
            "emotions": ["happy", "playful"],
            "description": "Both positive emotions, same Maslow level",
        },
        {
            "name": "Moderate Blend",
            "emotions": ["happy", "lustful"],
            "description": "Different Maslow levels (love/belonging vs physiological)",
        },
        {
            "name": "Complex Blend",
            "emotions": ["melancholic", "lustful"],
            "description": "Opposite Plutchik emotions (sadness vs joy)",
        },
        {
            "name": "Very Complex Blend",
            "emotions": ["anxious", "excited", "grateful"],
            "description": "Multiple Maslow levels, mixed Plutchik emotions",
        },
    ]

    for scenario in complexity_scenarios:
        print(f"\n🔄 {scenario['name']}")
        print(f"  Description: {scenario['description']}")
        print(f"  Emotions: {scenario['emotions']}")

        blended = blender.create_psychologically_realistic_emotion(
            scenario["emotions"], context={"urgency": True, "intimacy": True}
        )

        complexity = blended["psychological_analysis"]["complexity"]
        print(f"  Complexity Score: {complexity['score']:.2f}")
        print(f"  Complexity Level: {complexity['level']}")
        print(f"  Maslow Levels: {complexity['maslow_levels_involved']}")
        print(f"  Description: {complexity['description']}")


def test_psychological_realistic_combinations():
    """Test psychologically realistic emotion combinations"""

    print("\n💡 Psychologically Realistic Combinations")
    print("=" * 60)

    blender = EnhancedEmotionalBlender()

    combinations = blender.suggest_psychologically_realistic_combinations()

    for i, combo in enumerate(combinations, 1):
        print(
            f"\n{i}. {combo['primary'].title()} + {', '.join(combo['secondary']).title()}"
        )
        print(f"   Description: {combo['description']}")
        print(f"   Psychological Basis: {combo['psychological_basis']}")

        # Create the blend
        blended = blender.blend_emotions_with_psychology(
            combo["primary"], combo["secondary"]
        )

        print(f"   Result: {blended['name']}")
        print(
            f"   Complexity: {blended['psychological_analysis']['complexity']['level']}"
        )


if __name__ == "__main__":
    print("🧠 Enhanced Psychological Emotional System Test")
    print("=" * 80)
    print("Testing Plutchik's wheel of emotions and Maslow's hierarchy integration")
    print("=" * 80)

    # Run all tests
    test_enhanced_emotional_blender()
    test_enhanced_dynamic_emotion_engine()
    test_psychological_complexity()
    test_psychological_realistic_combinations()

    print("\n🎉 All psychological emotional system tests completed!")
    print("\nKey Features Demonstrated:")
    print("✅ Plutchik's wheel of emotions analysis")
    print("✅ Maslow's hierarchy of needs integration")
    print("✅ Psychological complexity calculation")
    print("✅ Realistic emotion blending")
    print("✅ Dynamic psychological state tracking")
    print("✅ Context-aware emotional transitions")
