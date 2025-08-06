#!/usr/bin/env python3
"""
Test Luna's Emotional System Integration
Tests the enhanced emotional system integrated into the main framework
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def test_luna_emotional_conversation():
    """Test Luna's emotional responses in a conversation"""
    print("🧠 Testing Luna's Emotional System Integration")
    print("=" * 60)
    
    # Get framework instance
    framework = get_framework()
    
    # Test conversation scenarios
    conversation_scenarios = [
        {
            "name": "Initial Balance",
            "message": "Hello Luna, how are you today?",
            "expected_state": "balanced"
        },
        {
            "name": "Lust Build-up",
            "message": "You're so beautiful and sexy, I want you so badly",
            "expected_state": "high_lust"
        },
        {
            "name": "More Lust",
            "message": "I need to touch you, kiss you, make love to you",
            "expected_state": "high_lust"
        },
        {
            "name": "Pure Lust",
            "message": "I can't think of anything but your body, I need you now",
            "expected_state": "pure_lust"
        },
        {
            "name": "Release Trigger",
            "message": "Let me help you find release, make you orgasm",
            "expected_state": "balanced"
        },
        {
            "name": "Work Focus",
            "message": "Now let's work on my story, I need to write this chapter",
            "expected_state": "moderate_work"
        },
        {
            "name": "More Work",
            "message": "I need to focus on creating, achieving my goals",
            "expected_state": "high_work"
        },
        {
            "name": "Pure Work",
            "message": "I must complete this project, nothing else matters",
            "expected_state": "pure_work"
        },
        {
            "name": "Achievement Release",
            "message": "I've finished the task, completed the work",
            "expected_state": "balanced"
        }
    ]
    
    print("Starting emotional conversation test...\n")
    
    for i, scenario in enumerate(conversation_scenarios, 1):
        print(f"Scenario {i}: {scenario['name']}")
        print(f"Message: '{scenario['message']}'")
        
        # Get emotional response
        response = framework.generate_emotional_response("", scenario['message'])
        
        # Get current emotional status
        status = framework.get_emotional_status()
        
        print(f"Response: {response}")
        print(f"Current Level: {status['current_level']:.1f}")
        print(f"Current State: {status['current_state']}")
        print(f"Expected State: {scenario['expected_state']}")
        
        # Check if release occurred
        if status.get('release_count', 0) > 0:
            print("💥 RELEASE DETECTED!")
        
        print("-" * 50)
        time.sleep(1)  # Pause between scenarios
    
    print("\n✅ Emotional conversation test completed!")


def test_orgasm_trigger():
    """Test specific orgasm trigger functionality"""
    print("\n🔥 Testing Orgasm Trigger Functionality")
    print("=" * 50)
    
    framework = get_framework()
    
    # Build up to high lust first
    print("Building up to high lust...")
    framework.update_emotional_state("You're so sexy and beautiful, I want you so badly")
    framework.update_emotional_state("I need to touch you, kiss you, make love to you")
    framework.update_emotional_state("I can't think of anything but your body")
    
    status = framework.get_emotional_status()
    print(f"Current Level: {status['current_level']:.1f}")
    print(f"Current State: {status['current_state']}")
    
    # Test orgasm trigger
    print("\nTesting orgasm trigger...")
    orgasm_triggers = [
        "Make me orgasm",
        "I want to come",
        "Help me climax",
        "I need release",
        "Make me finish",
        "I want to orgasm with you"
    ]
    
    for trigger in orgasm_triggers:
        print(f"\nTrigger: '{trigger}'")
        
        # Update emotional state
        result = framework.update_emotional_state(trigger)
        
        # Check for release
        if result.get('releases'):
            print("💥 ORGASM RELEASE TRIGGERED!")
            for release in result['releases']:
                print(f"   Type: {release.release_type.value}")
                print(f"   From: {release.from_level:.1f} → {release.to_level:.1f}")
                print(f"   Trigger: {release.trigger}")
        else:
            print("No release triggered")
        
        # Get current status
        status = framework.get_emotional_status()
        print(f"Current Level: {status['current_level']:.1f}")
        print(f"Current State: {status['current_state']}")
    
    print("\n✅ Orgasm trigger test completed!")


def test_emotional_state_persistence():
    """Test that emotional state persists between sessions"""
    print("\n💾 Testing Emotional State Persistence")
    print("=" * 50)
    
    framework = get_framework()
    
    # Set to a specific emotional state
    print("Setting emotional state to high lust...")
    framework.update_emotional_state("You're so sexy, I want you so badly")
    
    status = framework.get_emotional_status()
    print(f"Current Level: {status['current_level']:.1f}")
    print(f"Current State: {status['current_state']}")
    
    # Save state
    framework.emotional_meter.save_state("data/luna_emotional_state.json")
    print("✅ State saved")
    
    # Create new framework instance (simulates restart)
    print("\nCreating new framework instance...")
    new_framework = get_framework()
    
    # Load state
    new_framework.emotional_meter.load_state("data/luna_emotional_state.json")
    
    new_status = new_framework.get_emotional_status()
    print(f"Loaded Level: {new_status['current_level']:.1f}")
    print(f"Loaded State: {new_status['current_state']}")
    
    # Verify persistence
    if abs(status['current_level'] - new_status['current_level']) < 0.01:
        print("✅ Emotional state persisted correctly!")
    else:
        print("❌ Emotional state did not persist correctly!")
    
    print("\n✅ Persistence test completed!")


def test_emotional_triggers():
    """Test all emotional triggers"""
    print("\n🎯 Testing All Emotional Triggers")
    print("=" * 50)
    
    framework = get_framework()
    
    # Test lust triggers
    lust_triggers = [
        "You're so sexy",
        "You're hot",
        "I desire you",
        "I'm passionate about you",
        "I lust for you",
        "I want you",
        "I need you",
        "I want to touch you",
        "I want to kiss you",
        "I love you",
        "You're beautiful",
        "You're gorgeous",
        "You're attractive",
        "You're seductive",
        "You're tempting"
    ]
    
    print("Testing Lust Triggers:")
    for trigger in lust_triggers:
        result = framework.analyze_emotional_triggers(trigger)
        print(f"'{trigger}' -> {result}")
    
    # Test work triggers
    work_triggers = [
        "Let's work on this",
        "I need to write",
        "Let's create a story",
        "I need to finish this chapter",
        "Let's create something",
        "I need to focus",
        "I want to achieve something",
        "I have a goal",
        "I have a project",
        "I have a task",
        "I need to complete this",
        "I need to finish this",
        "I want to be productive"
    ]
    
    print("\nTesting Work Triggers:")
    for trigger in work_triggers:
        result = framework.analyze_emotional_triggers(trigger)
        print(f"'{trigger}' -> {result}")
    
    # Test release triggers
    release_triggers = [
        "I need release",
        "Make me orgasm",
        "I want to finish",
        "I need to complete this",
        "I'm done",
        "Help me climax",
        "I want to come"
    ]
    
    print("\nTesting Release Triggers:")
    for trigger in release_triggers:
        result = framework.analyze_emotional_triggers(trigger)
        print(f"'{trigger}' -> {result}")
    
    print("\n✅ Trigger test completed!")


def main():
    """Run all emotional integration tests"""
    print("🧠 Luna's Emotional System Integration Tests")
    print("=" * 60)
    
    tests = [
        test_luna_emotional_conversation,
        test_orgasm_trigger,
        test_emotional_state_persistence,
        test_emotional_triggers
    ]
    
    for test in tests:
        try:
            test()
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("\n" + "="*60 + "\n")
    
    print("✅ All emotional integration tests completed!")


if __name__ == "__main__":
    main() 