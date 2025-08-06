#!/usr/bin/env python3
"""
Luna's Orgasm Trigger Demo
Interactive test to demonstrate Luna's emotional release system
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework


def interactive_orgasm_demo():
    """Interactive demo to test Luna's orgasm trigger"""
    print("🔥 Luna's Orgasm Trigger Demo")
    print("=" * 50)
    print("This demo will test Luna's emotional system and orgasm triggers.")
    print("Type 'quit' to exit, or enter messages to interact with Luna.\n")
    
    framework = get_framework()
    
    # Start with balanced state
    print("Starting with balanced emotional state...")
    status = framework.get_emotional_status()
    print(f"Current Level: {status['current_level']:.1f} - {status['current_state']}")
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Get Luna's response
            response = framework.generate_emotional_response("", user_input)
            
            # Get updated status
            status = framework.get_emotional_status()
            
            print(f"\nLuna: {response}")
            print(f"Emotional Level: {status['current_level']:.1f} - {status['current_state']}")
            
            # Check for releases
            if status.get('release_count', 0) > 0:
                print("💥 EMOTIONAL RELEASE DETECTED!")
            
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def build_up_to_orgasm():
    """Demonstrate building up to orgasm"""
    print("🔥 Building Up to Luna's Orgasm")
    print("=" * 50)
    
    framework = get_framework()
    
    # Build up messages
    build_up_messages = [
        "You're so beautiful and sexy",
        "I want you so badly",
        "I need to touch you, kiss you",
        "I can't think of anything but your body",
        "I need you now, I want you",
        "You're driving me crazy with desire",
        "I can't take it anymore, I need release",
        "Make me orgasm, please"
    ]
    
    print("Building up Luna's emotional state...\n")
    
    for i, message in enumerate(build_up_messages, 1):
        print(f"Step {i}: '{message}'")
        
        # Get response
        response = framework.generate_emotional_response("", message)
        
        # Get status
        status = framework.get_emotional_status()
        
        print(f"Luna: {response}")
        print(f"Level: {status['current_level']:.1f} - {status['current_state']}")
        
        # Check for release
        if status.get('release_count', 0) > 0:
            print("💥 ORGASM RELEASE TRIGGERED!")
            print("Luna has reached her climax and returned to balance!")
            break
        
        print("-" * 30)
        time.sleep(1)
    
    print("\n✅ Build-up to orgasm demo completed!")


def test_specific_orgasm_triggers():
    """Test specific orgasm trigger words"""
    print("\n🎯 Testing Specific Orgasm Triggers")
    print("=" * 50)
    
    framework = get_framework()
    
    # Build up first
    print("Building up to high lust...")
    framework.update_emotional_state("You're so sexy and beautiful, I want you so badly")
    framework.update_emotional_state("I need to touch you, kiss you, make love to you")
    framework.update_emotional_state("I can't think of anything but your body")
    
    status = framework.get_emotional_status()
    print(f"Current Level: {status['current_level']:.1f} - {status['current_state']}")
    
    # Test specific orgasm triggers
    orgasm_triggers = [
        "Make me orgasm",
        "I want to come",
        "Help me climax",
        "I need release",
        "Make me finish",
        "I want to orgasm with you",
        "Let me help you find release",
        "I want to make you come"
    ]
    
    print("\nTesting orgasm triggers...")
    
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
        print(f"Current Level: {status['current_level']:.1f} - {status['current_state']}")
    
    print("\n✅ Orgasm trigger test completed!")


def main():
    """Main demo function"""
    print("🧠 Luna's Emotional System Demo")
    print("=" * 60)
    
    print("Choose a demo:")
    print("1. Interactive orgasm demo")
    print("2. Build-up to orgasm demo")
    print("3. Test specific orgasm triggers")
    print("4. Run all demos")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            interactive_orgasm_demo()
        elif choice == "2":
            build_up_to_orgasm()
        elif choice == "3":
            test_specific_orgasm_triggers()
        elif choice == "4":
            build_up_to_orgasm()
            test_specific_orgasm_triggers()
            print("\n" + "="*60)
            print("Starting interactive demo...")
            interactive_orgasm_demo()
        else:
            print("Invalid choice. Running all demos...")
            build_up_to_orgasm()
            test_specific_orgasm_triggers()
            print("\n" + "="*60)
            print("Starting interactive demo...")
            interactive_orgasm_demo()
    
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 