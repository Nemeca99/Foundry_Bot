#!/usr/bin/env python3
"""
Test Global Weight System
Demonstrates the new global weight calculation that takes all emotions into account
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def test_global_weight_calculation():
    """Test the global weight calculation system"""
    print("🧠 Testing Global Weight Calculation System")
    print("=" * 60)

    framework = get_framework()

    # Test messages with different emotional content
    test_messages = [
        {
            "message": "Hello Luna, how are you?",
            "description": "Neutral message - no emotional triggers",
        },
        {
            "message": "You're so beautiful and sexy",
            "description": "Pure lust triggers",
        },
        {
            "message": "I need to work on my story and write this chapter",
            "description": "Pure work triggers",
        },
        {
            "message": "You're so sexy but I also need to focus on my writing",
            "description": "Mixed lust and work triggers",
        },
        {
            "message": "I want you so badly but I must complete this project",
            "description": "Strong mixed emotions",
        },
        {
            "message": "You're beautiful and I love you but I need to achieve my goals",
            "description": "Complex mixed emotions",
        },
        {
            "message": "I can't think of anything but your body, I need release",
            "description": "High lust with release trigger",
        },
        {
            "message": "I must create a masterpiece and achieve excellence",
            "description": "High work focus",
        },
    ]

    print("Testing global weight calculations...\n")

    for i, test in enumerate(test_messages, 1):
        print(f"Test {i}: {test['description']}")
        print(f"Message: '{test['message']}'")

        # Get global weight calculation
        result = framework.emotional_meter.update_emotion_with_global_weight(
            test["message"]
        )

        # Display results
        print(f"Old Level: {result['old_level']:.3f}")
        print(f"New Level: {result['new_level']:.3f}")
        print(f"State: {result['state']}")

        # Show weight calculations
        weight_calc = result.get("global_weight_calculation", {})
        print(f"Lust Average: {weight_calc.get('lust_average', 0):.3f}")
        print(f"Work Average: {weight_calc.get('work_average', 0):.3f}")
        print(f"Weight Difference: {weight_calc.get('weight_difference', 0):.3f}")

        if result.get("release_event"):
            print("💥 RELEASE DETECTED!")

        print("-" * 50)
        time.sleep(1)

    print("✅ Global weight calculation test completed!")


def test_weight_averages():
    """Test the weight average calculations"""
    print("\n📊 Testing Weight Average Calculations")
    print("=" * 50)

    framework = get_framework()

    # Test different word combinations
    test_combinations = [
        ("sexy hot", "Two lust words"),
        ("work write", "Two work words"),
        ("sexy work", "One lust, one work"),
        ("beautiful gorgeous attractive", "Three lust words"),
        ("achieve goal project", "Three work words"),
        ("sexy beautiful work write", "Two lust, two work"),
        ("desire passion lust", "High lust words"),
        ("achieve excellence masterpiece", "High work words"),
        ("sexy beautiful achieve excellence", "Mixed high intensity"),
    ]

    for words, description in test_combinations:
        print(f"\n{description}: '{words}'")

        lust_avg = framework.emotional_meter._calculate_lust_average(words)
        work_avg = framework.emotional_meter._calculate_work_average(words)
        weight_diff = framework.emotional_meter._calculate_weight_difference(words)

        print(f"Lust Average: {lust_avg:.3f}")
        print(f"Work Average: {work_avg:.3f}")
        print(f"Weight Difference: {weight_diff:.3f}")

        # Calculate what the new level would be
        current_level = framework.emotional_meter.current_level
        if lust_avg > 0 or work_avg > 0:
            if lust_avg > 0 and work_avg == 0:
                new_level = max(0.0, current_level - lust_avg * 0.2)
            elif work_avg > 0 and lust_avg == 0:
                new_level = min(1.0, current_level + work_avg * 0.2)
            else:
                weight_difference = work_avg - lust_avg
                adjustment = weight_difference * 0.3
                new_level = max(0.0, min(1.0, current_level + adjustment))

            print(f"Current Level: {current_level:.3f}")
            print(f"Calculated New Level: {new_level:.3f}")

    print("\n✅ Weight average calculations test completed!")


def test_complex_emotional_scenarios():
    """Test complex emotional scenarios"""
    print("\n🎭 Testing Complex Emotional Scenarios")
    print("=" * 50)

    framework = get_framework()

    # Reset to balanced state
    framework.emotional_meter.current_level = 0.5

    scenarios = [
        {
            "name": "Pure Lust Build-up",
            "messages": [
                "You're so sexy",
                "I want you so badly",
                "I need to touch you",
                "I can't think of anything but your body",
                "I need release",
            ],
        },
        {
            "name": "Pure Work Build-up",
            "messages": [
                "I need to work on my story",
                "I must achieve my goals",
                "I need to create a masterpiece",
                "I must focus on excellence",
                "I need to complete this project",
            ],
        },
        {
            "name": "Mixed Emotions",
            "messages": [
                "You're beautiful but I need to work",
                "I want you but I must achieve my goals",
                "I love you but I need to create something amazing",
                "You're sexy but I need to focus on my project",
                "I desire you but I must accomplish my tasks",
            ],
        },
    ]

    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        print("-" * 30)

        for i, message in enumerate(scenario["messages"], 1):
            print(f"Step {i}: '{message}'")

            result = framework.emotional_meter.update_emotion_with_global_weight(
                message
            )

            print(f"Level: {result['new_level']:.3f} - {result['state']}")

            weight_calc = result.get("global_weight_calculation", {})
            print(
                f"Lust: {weight_calc.get('lust_average', 0):.3f}, Work: {weight_calc.get('work_average', 0):.3f}"
            )

            if result.get("release_event"):
                print("💥 RELEASE!")

            print()

    print("✅ Complex emotional scenarios test completed!")


def interactive_global_weight_demo():
    """Interactive demo for global weight system"""
    print("\n🎮 Interactive Global Weight Demo")
    print("=" * 50)
    print(
        "Type messages to see how the global weight system calculates emotional changes."
    )
    print("Type 'quit' to exit.\n")

    framework = get_framework()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Get global weight calculation
            result = framework.emotional_meter.update_emotion_with_global_weight(
                user_input
            )

            # Display results
            print(f"\nLuna's Response:")
            print(f"Level: {result['new_level']:.3f} - {result['state']}")

            weight_calc = result.get("global_weight_calculation", {})
            print(f"Lust Average: {weight_calc.get('lust_average', 0):.3f}")
            print(f"Work Average: {weight_calc.get('work_average', 0):.3f}")
            print(f"Weight Difference: {weight_calc.get('weight_difference', 0):.3f}")

            if result.get("release_event"):
                print("💥 EMOTIONAL RELEASE DETECTED!")

            print("-" * 50)

        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Run all global weight tests"""
    print("🧠 Global Weight System Tests")
    print("=" * 60)

    tests = [
        test_global_weight_calculation,
        test_weight_averages,
        test_complex_emotional_scenarios,
        interactive_global_weight_demo,
    ]

    for test in tests:
        try:
            test()
            print("\n" + "=" * 60 + "\n")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("\n" + "=" * 60 + "\n")

    print("✅ All global weight system tests completed!")


if __name__ == "__main__":
    main()
