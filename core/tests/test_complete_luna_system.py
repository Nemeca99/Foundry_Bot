#!/usr/bin/env python3
"""
Complete Luna System Test
Demonstrates the full enhanced Luna system with global weight calculation,
Discord integration, and emotional responses
"""

import sys
import time
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discord.enhanced_luna_bot import EnhancedLunaBot
from astra_emotional_fragments.enhanced_emotional_meter import EnhancedEmotionalMeter


def test_complete_luna_system():
    """Test the complete Luna system with all features"""
    print("🌟 Complete Luna System Test")
    print("=" * 60)
    
    # Initialize bot
    bot = EnhancedLunaBot()
    
    # Reset to balanced state
    bot.emotional_meter.current_level = 0.5
    print(f"🎯 Starting Level: {bot.emotional_meter.current_level:.3f} (Balanced)")
    
    # Test scenarios
    scenarios = [
        {
            "name": "Building Lust",
            "messages": [
                "You're so beautiful and sexy",
                "I want you so badly",
                "I need to touch you and kiss you",
                "I can't think of anything but your body",
                "I need you now, I want you",
                "I need release"
            ]
        },
        {
            "name": "Building Work Focus",
            "messages": [
                "I need to work on my story",
                "I must achieve my goals",
                "I need to create a masterpiece",
                "I must focus on excellence",
                "I need to complete this project",
                "I need to finish this task"
            ]
        },
        {
            "name": "Mixed Emotions",
            "messages": [
                "You're beautiful but I need to focus on my writing",
                "I want you but I must achieve my goals",
                "You're sexy but I need to work on my story",
                "I need you but I must create something amazing"
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🔥 {scenario['name']}")
        print("-" * 40)
        
        # Reset to balanced state
        bot.emotional_meter.current_level = 0.5
        
        for i, message in enumerate(scenario['messages'], 1):
            print(f"\nStep {i}: '{message}'")
            
            # Update emotional state
            result = bot.emotional_meter.update_emotion_with_global_weight(message)
            
            # Generate response
            response = asyncio.run(bot._generate_emotional_response(None, message, result))
            
            # Display results
            print(f"  Level: {result['old_level']:.3f} → {result['new_level']:.3f}")
            print(f"  State: {result['state']}")
            print(f"  Response: {response[:80]}...")
            
            # Show weight analysis
            weight_calc = result.get('global_weight_calculation', {})
            if weight_calc:
                lust_avg = weight_calc.get('lust_average', 0)
                work_avg = weight_calc.get('work_average', 0)
                weight_diff = weight_calc.get('weight_difference', 0)
                print(f"  Weights: Lust={lust_avg:.3f}, Work={work_avg:.3f}, Diff={weight_diff:.3f}")
            
            # Check for release
            if result.get('release_event'):
                release = result['release_event']
                print(f"  💥 RELEASE: {release.release_type.value} from {release.from_level:.3f} → {release.to_level:.3f}")
            
            time.sleep(0.5)  # Pause for dramatic effect
    
    print("\n✅ Complete Luna system test finished!")


def test_weight_analysis_demo():
    """Demonstrate weight analysis with various messages"""
    print("\n📊 Weight Analysis Demo")
    print("=" * 40)
    
    bot = EnhancedLunaBot()
    
    demo_messages = [
        "You're so sexy and beautiful",
        "I need to work on my story and write this chapter",
        "You're beautiful but I need to focus on my writing",
        "I want you so badly but I must achieve my goals",
        "I can't think of anything but your body, I need release",
        "I must create a masterpiece and achieve excellence",
        "You're hot but I need to be productive",
        "I desire you but I must accomplish my tasks"
    ]
    
    for message in demo_messages:
        print(f"\nMessage: '{message}'")
        
        # Calculate weights
        lust_avg = bot.emotional_meter._calculate_lust_average(message)
        work_avg = bot.emotional_meter._calculate_work_average(message)
        weight_diff = bot.emotional_meter._calculate_weight_difference(message)
        
        # Get found words
        lust_words = bot._get_lust_words(message)
        work_words = bot._get_work_words(message)
        
        print(f"  Lust Words: {lust_words}")
        print(f"  Work Words: {work_words}")
        print(f"  Lust Average: {lust_avg:.3f}")
        print(f"  Work Average: {work_avg:.3f}")
        print(f"  Weight Difference: {weight_diff:.3f}")
        
        # Determine bias
        if weight_diff > 0.1:
            bias = "Work"
        elif weight_diff < -0.1:
            bias = "Lust"
        else:
            bias = "Balanced"
        
        print(f"  Bias: {bias}")
    
    print("\n✅ Weight analysis demo completed!")


def test_emotional_states():
    """Test all emotional states"""
    print("\n🎭 Emotional States Test")
    print("=" * 40)
    
    bot = EnhancedLunaBot()
    
    # Test each emotional state
    test_levels = [
        (0.05, "Pure Lust"),
        (0.15, "High Lust"),
        (0.35, "Moderate Lust"),
        (0.50, "Balanced"),
        (0.65, "Moderate Work"),
        (0.85, "High Work"),
        (0.95, "Pure Work")
    ]
    
    for level, state_name in test_levels:
        print(f"\n{state_name} (Level: {level:.3f})")
        print("-" * 30)
        
        # Set level
        bot.emotional_meter.current_level = level
        
        # Generate response
        response = asyncio.run(bot._generate_emotional_response(None, "Test message", {}))
        
        print(f"Response: {response}")
    
    print("\n✅ Emotional states test completed!")


def test_release_triggers():
    """Test release trigger scenarios"""
    print("\n💥 Release Triggers Test")
    print("=" * 40)
    
    bot = EnhancedLunaBot()
    
    # Test sexual release
    print("Testing Sexual Release...")
    bot.emotional_meter.current_level = 0.05  # Pure lust
    
    release_messages = [
        "I need release",
        "I need to orgasm",
        "I need to finish",
        "I need to complete",
        "I need to climax",
        "I need to come"
    ]
    
    for message in release_messages:
        result = bot.emotional_meter.update_emotion_with_global_weight(message)
        print(f"'{message}' → Level: {result['new_level']:.3f}")
        
        if result.get('release_event'):
            release = result['release_event']
            print(f"  💥 SEXUAL RELEASE: {release.from_level:.3f} → {release.to_level:.3f}")
            break
    
    # Test achievement release
    print("\nTesting Achievement Release...")
    bot.emotional_meter.current_level = 0.95  # Pure work
    
    achievement_messages = [
        "I need to finish this task",
        "I need to complete this project",
        "I need to achieve my goals",
        "I need to accomplish this"
    ]
    
    for message in achievement_messages:
        result = bot.emotional_meter.update_emotion_with_global_weight(message)
        print(f"'{message}' → Level: {result['new_level']:.3f}")
        
        if result.get('release_event'):
            release = result['release_event']
            print(f"  💥 ACHIEVEMENT RELEASE: {release.from_level:.3f} → {release.to_level:.3f}")
            break
    
    print("\n✅ Release triggers test completed!")


def interactive_demo():
    """Interactive demo of the Luna system"""
    print("\n🎮 Interactive Luna Demo")
    print("=" * 40)
    print("Type messages to interact with Luna (type 'quit' to exit)")
    print("Commands:")
    print("  !status - Show current emotional status")
    print("  !reset - Reset to balanced state")
    print("  !weights <message> - Analyze weights")
    print("  !quit - Exit demo")
    
    bot = EnhancedLunaBot()
    bot.emotional_meter.current_level = 0.5
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.startswith('!status'):
                status = bot.emotional_meter.get_emotional_summary()
                print(f"Luna's Status: Level {status['current_level']:.3f} - {status['current_state']}")
            elif user_input.startswith('!reset'):
                bot.emotional_meter.current_level = 0.5
                print("Luna's emotional state reset to balanced (0.500)")
            elif user_input.startswith('!weights '):
                message = user_input[9:]  # Remove "!weights "
                lust_avg = bot.emotional_meter._calculate_lust_average(message)
                work_avg = bot.emotional_meter._calculate_work_average(message)
                weight_diff = bot.emotional_meter._calculate_weight_difference(message)
                print(f"Weight Analysis: Lust={lust_avg:.3f}, Work={work_avg:.3f}, Diff={weight_diff:.3f}")
            else:
                # Process normal message
                result = bot.emotional_meter.update_emotion_with_global_weight(user_input)
                response = asyncio.run(bot._generate_emotional_response(None, user_input, result))
                
                print(f"Luna: {response}")
                
                if result.get('release_event'):
                    release = result['release_event']
                    print(f"💥 {release.release_type.value.upper()} RELEASE!")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n✅ Interactive demo completed!")


def main():
    """Run all complete system tests"""
    print("🌟 Complete Luna System Test Suite")
    print("=" * 60)
    
    tests = [
        test_complete_luna_system,
        test_weight_analysis_demo,
        test_emotional_states,
        test_release_triggers
    ]
    
    for test in tests:
        try:
            test()
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("\n" + "="*60 + "\n")
    
    # Ask if user wants interactive demo
    try:
        response = input("Would you like to try the interactive demo? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_demo()
    except KeyboardInterrupt:
        pass
    
    print("✅ All complete Luna system tests finished!")


if __name__ == "__main__":
    main() 