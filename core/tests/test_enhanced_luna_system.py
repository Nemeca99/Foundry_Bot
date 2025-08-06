#!/usr/bin/env python3
"""
Test Enhanced Luna Emotional System
Demonstrates the dual-release mechanism and emotional evolution
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from astra_emotional_fragments.enhanced_emotional_meter import EnhancedEmotionalMeter


def test_lust_build_up_and_release():
    """Test lust build-up to release cycle"""
    print("🔥 Testing Lust Build-up and Release Cycle")
    print("=" * 50)
    
    meter = EnhancedEmotionalMeter()
    
    # Start at balanced state
    print(f"Starting Level: {meter.current_level:.1f} - {meter.get_state_description()}")
    
    # Build up lust gradually
    lust_triggers = [
        ("You're so sexy", 0.2),
        ("I want you so badly", 0.3),
        ("I need to touch you", 0.2),
        ("The desire is overwhelming", 0.3),
        ("I can't think of anything else", 0.2)
    ]
    
    for trigger, intensity in lust_triggers:
        result = meter.update_emotion("lustful", intensity)
        print(f"\nTrigger: '{trigger}'")
        print(f"Level: {result['new_level']:.1f} - {result['description']}")
        
        if result.get('release_event'):
            release = result['release_event']
            print(f"💥 SEXUAL RELEASE TRIGGERED!")
            print(f"   Type: {release.release_type.value}")
            print(f"   From: {release.from_level:.1f} → {release.to_level:.1f}")
            print(f"   Trigger: {release.trigger}")
            break
    
    print(f"\nFinal Level: {meter.current_level:.1f} - {meter.get_state_description()}")


def test_work_build_up_and_release():
    """Test work build-up to release cycle"""
    print("\n💼 Testing Work Build-up and Release Cycle")
    print("=" * 50)
    
    meter = EnhancedEmotionalMeter()
    
    # Start at balanced state
    print(f"Starting Level: {meter.current_level:.1f} - {meter.get_state_description()}")
    
    # Build up work focus gradually
    work_triggers = [
        ("Let's work on the story", 0.2),
        ("I need to finish this chapter", 0.3),
        ("Focus on the writing", 0.2),
        ("Achieve something meaningful", 0.3),
        ("Complete this project", 0.2)
    ]
    
    for trigger, intensity in work_triggers:
        result = meter.update_emotion("work", intensity)
        print(f"\nTrigger: '{trigger}'")
        print(f"Level: {result['new_level']:.1f} - {result['description']}")
        
        if result.get('release_event'):
            release = result['release_event']
            print(f"🎯 ACHIEVEMENT RELEASE TRIGGERED!")
            print(f"   Type: {release.release_type.value}")
            print(f"   From: {release.from_level:.1f} → {release.to_level:.1f}")
            print(f"   Trigger: {release.trigger}")
            break
    
    print(f"\nFinal Level: {meter.current_level:.1f} - {meter.get_state_description()}")


def test_natural_return_to_balance():
    """Test natural return to balance"""
    print("\n⚖️ Testing Natural Return to Balance")
    print("=" * 50)
    
    meter = EnhancedEmotionalMeter()
    
    # Set to high lust
    meter.current_level = 0.2
    print(f"Starting Level: {meter.current_level:.1f} - {meter.get_state_description()}")
    
    # Let it naturally return to balance
    for i in range(10):
        result = meter.update_emotion("neutral")
        print(f"Step {i+1}: {result['new_level']:.1f} - {result['description']}")
        
        if abs(result['new_level'] - 0.5) < 0.01:
            print("✅ Reached balanced state!")
            break
    
    # Set to high work focus
    meter.current_level = 0.8
    print(f"\nStarting Level: {meter.current_level:.1f} - {meter.get_state_description()}")
    
    # Let it naturally return to balance
    for i in range(10):
        result = meter.update_emotion("neutral")
        print(f"Step {i+1}: {result['new_level']:.1f} - {result['description']}")
        
        if abs(result['new_level'] - 0.5) < 0.01:
            print("✅ Reached balanced state!")
            break


def test_emotional_state_transitions():
    """Test all emotional state transitions"""
    print("\n🎭 Testing All Emotional State Transitions")
    print("=" * 50)
    
    meter = EnhancedEmotionalMeter()
    
    # Test all states
    test_levels = [0.0, 0.1, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1.0]
    
    for level in test_levels:
        meter.current_level = level
        state = meter.get_current_state()
        description = meter.get_state_description()
        
        print(f"Level {level:.1f}: {state.value}")
        print(f"  Description: {description}")
        print()


def test_release_history():
    """Test release history tracking"""
    print("\n📊 Testing Release History Tracking")
    print("=" * 50)
    
    meter = EnhancedEmotionalMeter()
    
    # Trigger multiple releases
    print("Triggering multiple emotional releases...")
    
    # Sexual release
    meter.current_level = 0.0
    result = meter.update_emotion("release")
    if result.get('release_event'):
        print("✅ Sexual release recorded")
    
    # Achievement release
    meter.current_level = 1.0
    result = meter.update_emotion("release")
    if result.get('release_event'):
        print("✅ Achievement release recorded")
    
    # Show history
    history = meter.get_release_history()
    print(f"\nRelease History ({len(history)} events):")
    
    for i, release in enumerate(history, 1):
        print(f"  {i}. {release['release_type']} - {release['from_level']:.1f} → {release['to_level']:.1f}")
        print(f"     Trigger: {release['trigger']}")
        print(f"     Duration: {release['duration']:.1f}s")
        print()


def test_save_and_load_state():
    """Test saving and loading emotional state"""
    print("\n💾 Testing Save and Load State")
    print("=" * 50)
    
    meter = EnhancedEmotionalMeter()
    
    # Modify state
    meter.current_level = 0.3
    meter.update_emotion("lustful", 0.2)
    
    print(f"Current Level: {meter.current_level:.1f}")
    print(f"Release Count: {len(meter.release_history)}")
    
    # Save state
    test_file = "test_emotional_state.json"
    meter.save_state(test_file)
    print(f"✅ State saved to {test_file}")
    
    # Create new meter and load state
    new_meter = EnhancedEmotionalMeter()
    new_meter.load_state(test_file)
    
    print(f"Loaded Level: {new_meter.current_level:.1f}")
    print(f"Loaded Release Count: {len(new_meter.release_history)}")
    
    # Clean up
    import os
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"✅ Test file cleaned up")


def test_complex_interaction():
    """Test complex interaction scenario"""
    print("\n🎯 Testing Complex Interaction Scenario")
    print("=" * 50)
    
    meter = EnhancedEmotionalMeter()
    
    # Simulate a conversation
    interactions = [
        ("Hello Luna, how are you?", "neutral"),
        ("You look so beautiful today", "lustful"),
        ("I want to kiss you", "lustful"),
        ("But first, let's work on my story", "work"),
        ("I need to finish this chapter", "work"),
        ("You're distracting me with your beauty", "lustful"),
        ("Focus on the writing", "work"),
        ("I can't resist you", "lustful"),
        ("Let's take a break", "neutral")
    ]
    
    for i, (message, interaction_type) in enumerate(interactions, 1):
        print(f"\n{i}. Message: '{message}'")
        print(f"   Interaction Type: {interaction_type}")
        
        result = meter.update_emotion(interaction_type, 0.15)
        print(f"   Level: {result['new_level']:.1f} - {result['description']}")
        
        if result.get('release_event'):
            release = result['release_event']
            print(f"   💥 RELEASE: {release.release_type.value}")
    
    print(f"\nFinal Level: {meter.current_level:.1f} - {meter.get_state_description()}")


def main():
    """Run all tests"""
    print("🧠 Enhanced Luna Emotional System Tests")
    print("=" * 60)
    
    tests = [
        test_lust_build_up_and_release,
        test_work_build_up_and_release,
        test_natural_return_to_balance,
        test_emotional_state_transitions,
        test_release_history,
        test_save_and_load_state,
        test_complex_interaction
    ]
    
    for test in tests:
        try:
            test()
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("\n" + "="*60 + "\n")
    
    print("✅ All tests completed!")


if __name__ == "__main__":
    main() 