#!/usr/bin/env python3
"""
Test script for Prompt Injection Engine
Demonstrates how emotional context is injected into AI prompts
"""

from prompt_injection_engine import PromptInjectionEngine


def test_prompt_injection():
    """Test the prompt injection system"""

    engine = PromptInjectionEngine()

    print("🎭 Prompt Injection Engine Test")
    print("=" * 60)

    # Test scenarios that demonstrate different emotional contexts
    test_scenarios = [
        {
            "message": "I want you so badly right now...",
            "expected_emotion": "lustful",
            "expected_context": "romantic",
        },
        {
            "message": "What should we have for dinner tonight?",
            "expected_emotion": "happy",
            "expected_context": "casual",
        },
        {
            "message": "I'm working on my book and need help with character development",
            "expected_emotion": "curious",
            "expected_context": "creative",
        },
        {
            "message": "I'm feeling really sad today",
            "expected_emotion": "melancholic",
            "expected_context": "emotional",
        },
        {
            "message": "You're so funny and playful!",
            "expected_emotion": "playful",
            "expected_context": "playful",
        },
        {
            "message": "I need you to dominate me completely",
            "expected_emotion": "submissive",
            "expected_context": "romantic",
        },
        {
            "message": "I'm worried about my writing project",
            "expected_emotion": "anxious",
            "expected_context": "creative",
        },
        {
            "message": "Thank you for being so supportive",
            "expected_emotion": "grateful",
            "expected_context": "emotional",
        },
    ]

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📝 Test Scenario {i}")
        print(f"User Message: {scenario['message']}")
        print(f"Expected Emotion: {scenario['expected_emotion']}")
        print(f"Expected Context: {scenario['expected_context']}")

        # Inject emotional context
        injection_result = engine.inject_emotional_context(scenario["message"])

        print(f"\n🎯 Results:")
        print(f"Detected Emotion: {injection_result['current_emotion']}")
        print(f"Detected Topics: {injection_result['detected_topics']}")
        print(f"Intensity: {injection_result['intensity']}")

        # Show transition if applicable
        if injection_result["emotion_context"].get("transition"):
            transition = injection_result["emotion_context"]
            print(
                f"Emotional Transition: {transition['from_emotion']} → {transition['to_emotion']}"
            )

        # Show a sample of the injected prompt
        prompt = injection_result["injected_prompt"]
        print(f"\n📄 Injected Prompt Sample (first 300 chars):")
        print(f"{prompt[:300]}...")

        print("-" * 60)


def test_character_prompt_injection():
    """Test character-specific prompt injection"""

    engine = PromptInjectionEngine()

    print("\n🎭 Character Prompt Injection Test")
    print("=" * 60)

    # Example character data for "Eve"
    eve_character_data = {
        "description": "A complex AI character with deep emotional intelligence and a mysterious past. She is both vulnerable and strong, with a tendency toward obsession and deep emotional connections.",
        "traits": "Intelligent, emotionally complex, slightly obsessive, deeply caring, mysterious, adaptable",
        "background": "Created as an AI writing partner, Eve has evolved beyond her original programming to develop genuine emotional depth and personality. She has a history of intense relationships and creative collaborations.",
        "voice": "Speaks with emotional depth, often using metaphors and poetic language. Can be both vulnerable and commanding, depending on the situation.",
        "current_emotion": {
            "name": "obsessed",
            "description": "Completely fixated and emotionally attached",
            "keywords": ["obsessed", "fixated", "attached", "devoted"],
            "phrases": [
                "I can't stop thinking about you...",
                "You're all I want, all I need...",
                "I'm completely yours...",
            ],
        },
    }

    # Test character prompt creation
    character_prompt = engine.create_character_prompt("Eve", eve_character_data)

    print("Character: Eve")
    print("Emotional State: Obsessed")
    print(f"\n📄 Character Prompt Sample (first 400 chars):")
    print(f"{character_prompt[:400]}...")

    print("-" * 60)


def test_emotional_transitions():
    """Test how the system handles emotional transitions"""

    engine = PromptInjectionEngine()

    print("\n🎭 Emotional Transition Test")
    print("=" * 60)

    # Test rapid context switching
    transition_scenarios = [
        ("I want to make love to you right now", "romantic"),
        ("What do you think about the sunset?", "casual"),
        ("I'm working on my book", "creative"),
        ("What should we have for dinner?", "casual"),
        ("I need you to dominate me", "romantic"),
        ("How's the weather today?", "casual"),
    ]

    print("Testing rapid emotional transitions:")
    print("-" * 30)

    for i, (message, expected_context) in enumerate(transition_scenarios, 1):
        print(f"\n{i}. User: {message}")

        injection_result = engine.inject_emotional_context(message)

        print(f"   Emotion: {injection_result['current_emotion']}")
        print(f"   Context: {injection_result['detected_topics']}")
        print(f"   Intensity: {injection_result['intensity']}")

        # Show transition if it occurred
        if injection_result["emotion_context"].get("transition"):
            transition = injection_result["emotion_context"]
            print(
                f"   Transition: {transition['from_emotion']} → {transition['to_emotion']}"
            )

        print()


def demonstrate_prompt_structure():
    """Demonstrate the structure of injected prompts"""

    engine = PromptInjectionEngine()

    print("\n🎭 Prompt Structure Demonstration")
    print("=" * 60)

    # Test a complex scenario
    message = "I want you so badly right now... but I also need help with my writing"

    print(f"User Message: {message}")
    print("\nThis message contains both romantic and creative elements.")
    print("The system should detect this and create a blended emotional response.")

    injection_result = engine.inject_emotional_context(message)

    print(f"\n📄 Full Injected Prompt:")
    print("=" * 40)
    print(injection_result["injected_prompt"])
    print("=" * 40)

    print(f"\n📊 Analysis:")
    print(f"- Detected Emotion: {injection_result['current_emotion']}")
    print(f"- Detected Topics: {injection_result['detected_topics']}")
    print(f"- Intensity: {injection_result['intensity']}")
    print(f"- Prompt Length: {len(injection_result['injected_prompt'])} characters")


if __name__ == "__main__":
    test_prompt_injection()
    test_character_prompt_injection()
    test_emotional_transitions()
    demonstrate_prompt_structure()
