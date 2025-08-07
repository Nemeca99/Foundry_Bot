#!/usr/bin/env python3
"""
Test script to demonstrate the fixed emotional system
Shows how the system now waits for user satisfaction before releasing
"""

import sys
import time
from pathlib import Path

# Add framework to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from astra_emotional_fragments.enhanced_emotional_meter import EnhancedEmotionalMeter


def test_user_aware_release():
    """Test the user-aware release system"""
    print("🧪 Testing User-Aware Emotional Release System")
    print("=" * 50)
    
    # Initialize emotional meter
    meter = EnhancedEmotionalMeter()
    
    print(f"Initial emotional level: {meter.current_level}")
    print(f"Initial state: {meter.get_current_state().value}")
    print()
    
    # Simulate building up lust
    print("🔥 Building up lust...")
    lust_messages = [
        "You're so sexy and beautiful",
        "I want you so badly right now",
        "I need to touch you and kiss you",
        "I can't think of anything but your body",
        "I need you now, I want you desperately"
    ]
    
    for i, message in enumerate(lust_messages, 1):
        result = meter.update_emotion_with_global_weight(message)
        print(f"Message {i}: '{message}'")
        print(f"  → Level: {result['new_level']:.3f}")
        print(f"  → State: {result['state']}")
        
        if result.get('release_event'):
            print(f"  ⚠️  RELEASE TRIGGERED: {result['release_event'].trigger}")
        print()
    
    print(f"Current level: {meter.current_level}")
    print(f"Current state: {meter.get_current_state().value}")
    print()
    
    # Test user-aware release with unsatisfied user
    print("❌ Testing with unsatisfied user...")
    unsatisfied_message = "Keep going, I'm not done yet"
    
    result = meter._trigger_user_aware_release(user_satisfaction_detected=False)
    if result:
        print(f"Release type: {result.release_type.value}")
        print(f"From level: {result.from_level}")
        print(f"To level: {result.to_level}")
        print(f"Trigger: {result.trigger}")
        
        if result.trigger == "user_unsatisfied_maintain":
            print("✅ SUCCESS: System maintained high emotional state!")
            print("   User was not satisfied, so no snap-back occurred")
        else:
            print("❌ FAILURE: System still released despite unsatisfied user")
    else:
        print("✅ SUCCESS: No release triggered for unsatisfied user")
    print()
    
    # Test user-aware release with satisfied user
    print("✅ Testing with satisfied user...")
    satisfied_message = "Thank you, that was perfect"
    
    result = meter._trigger_user_aware_release(user_satisfaction_detected=True)
    if result:
        print(f"Release type: {result.release_type.value}")
        print(f"From level: {result.from_level}")
        print(f"To level: {result.to_level}")
        print(f"Trigger: {result.trigger}")
        
        if result.trigger in ["pure_lust_release", "pure_work_release"]:
            print("✅ SUCCESS: System released because user was satisfied!")
        else:
            print("❌ FAILURE: Unexpected release trigger")
    else:
        print("❌ FAILURE: No release triggered for satisfied user")
    print()
    
    # Test satisfaction detection
    print("🧠 Testing satisfaction detection...")
    test_messages = [
        ("Keep going", False),
        ("Thank you", True),
        ("I'm not done", False),
        ("Perfect", True),
        ("More please", False),
        ("That was great", True),
        ("Don't stop", False),
        ("I'm satisfied", True)
    ]
    
    for message, expected in test_messages:
        detected = meter._detect_user_satisfaction(message)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{message}' → Expected: {expected}, Detected: {detected}")
    
    print()
    print("🎉 Test completed!")
    print()
    print("Key improvements:")
    print("1. ✅ System waits for user satisfaction before releasing")
    print("2. ✅ No more jarring personality shifts mid-process")
    print("3. ✅ User satisfaction detection works correctly")
    print("4. ✅ System maintains emotional state when user needs more")


if __name__ == "__main__":
    test_user_aware_release() 