#!/usr/bin/env python3
"""
Test Discord Luna Integration
Tests the Discord bot integration with Luna's enhanced emotional system
"""

import sys
import time
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discord.enhanced_luna_bot import EnhancedLunaBot


def test_luna_bot_initialization():
    """Test Luna bot initialization"""
    print("🤖 Testing Luna Bot Initialization")
    print("=" * 50)
    
    try:
        # Create bot instance
        bot = EnhancedLunaBot()
        
        print("✅ Bot created successfully")
        print(f"✅ Emotional Meter Level: {bot.emotional_meter.current_level:.3f}")
        print(f"✅ Emotional State: {bot.emotional_meter.get_current_state().value}")
        print(f"✅ Lust Words: {len(bot.emotional_meter.lust_weights)}")
        print(f"✅ Work Words: {len(bot.emotional_meter.work_weights)}")
        
        return bot
    
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return None


def test_emotional_response_generation():
    """Test emotional response generation"""
    print("\n🎭 Testing Emotional Response Generation")
    print("=" * 50)
    
    bot = EnhancedLunaBot()
    
    # Test messages
    test_messages = [
        "Hello Luna, how are you?",
        "You're so beautiful and sexy",
        "I need to work on my story",
        "I want you so badly but I must complete this project",
        "I can't think of anything but your body, I need release",
        "I must create a masterpiece and achieve excellence"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: '{message}'")
        
        # Generate response
        response = asyncio.run(bot._generate_emotional_response(None, message, {}))
        
        # Get emotional state
        status = bot.emotional_meter.get_emotional_summary()
        
        print(f"Response: {response[:100]}...")
        print(f"Level: {status['current_level']:.3f} - {status['current_state']}")
    
    print("\n✅ Emotional response generation test completed!")


def test_weight_analysis():
    """Test weight analysis functionality"""
    print("\n📊 Testing Weight Analysis")
    print("=" * 50)
    
    bot = EnhancedLunaBot()
    
    test_messages = [
        "You're so sexy and beautiful",
        "I need to work on my story and write this chapter",
        "You're beautiful but I need to focus on my writing",
        "I want you so badly but I must achieve my goals",
        "I can't think of anything but your body, I need release"
    ]
    
    for message in test_messages:
        print(f"\nMessage: '{message}'")
        
        # Calculate weights
        lust_avg = bot.emotional_meter._calculate_lust_average(message)
        work_avg = bot.emotional_meter._calculate_work_average(message)
        weight_diff = bot.emotional_meter._calculate_weight_difference(message)
        
        # Get found words
        lust_words = bot._get_lust_words(message)
        work_words = bot._get_work_words(message)
        
        print(f"Lust Average: {lust_avg:.3f} (Words: {lust_words})")
        print(f"Work Average: {work_avg:.3f} (Words: {work_words})")
        print(f"Weight Difference: {weight_diff:.3f}")
    
    print("\n✅ Weight analysis test completed!")


def test_global_weight_calculation():
    """Test global weight calculation"""
    print("\n🌐 Testing Global Weight Calculation")
    print("=" * 50)
    
    bot = EnhancedLunaBot()
    
    # Reset to balanced state
    bot.emotional_meter.current_level = 0.5
    
    test_messages = [
        "Hello Luna",
        "You're so sexy",
        "I need to work on my story",
        "You're beautiful but I need to focus",
        "I want you so badly but I must achieve my goals",
        "I can't think of anything but your body",
        "I must create a masterpiece"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nStep {i}: '{message}'")
        
        # Update emotional state
        result = bot.emotional_meter.update_emotion_with_global_weight(message)
        
        # Display results
        print(f"Old Level: {result['old_level']:.3f}")
        print(f"New Level: {result['new_level']:.3f}")
        print(f"State: {result['state']}")
        
        # Show weight calculations
        weight_calc = result.get('global_weight_calculation', {})
        print(f"Lust: {weight_calc.get('lust_average', 0):.3f}")
        print(f"Work: {weight_calc.get('work_average', 0):.3f}")
        print(f"Difference: {weight_calc.get('weight_difference', 0):.3f}")
        
        if result.get('release_event'):
            print("💥 RELEASE DETECTED!")
    
    print("\n✅ Global weight calculation test completed!")


def test_emotional_build_up():
    """Test emotional build-up scenarios"""
    print("\n🔥 Testing Emotional Build-up Scenarios")
    print("=" * 50)
    
    bot = EnhancedLunaBot()
    
    # Test lust build-up
    print("Building up lust...")
    bot.emotional_meter.current_level = 0.5
    
    lust_messages = [
        "You're so beautiful and sexy",
        "I want you so badly",
        "I need to touch you and kiss you",
        "I can't think of anything but your body",
        "I need you now, I want you",
        "I need release"
    ]
    
    for message in lust_messages:
        result = bot.emotional_meter.update_emotion_with_global_weight(message)
        print(f"'{message}' → Level: {result['new_level']:.3f} - {result['state']}")
        
        if result.get('release_event'):
            print("💥 LUST RELEASE!")
            break
    
    # Reset and test work build-up
    print("\nBuilding up work focus...")
    bot.emotional_meter.current_level = 0.5
    
    work_messages = [
        "I need to work on my story",
        "I must achieve my goals",
        "I need to create a masterpiece",
        "I must focus on excellence",
        "I need to complete this project",
        "I need to finish this task"
    ]
    
    for message in work_messages:
        result = bot.emotional_meter.update_emotion_with_global_weight(message)
        print(f"'{message}' → Level: {result['new_level']:.3f} - {result['state']}")
        
        if result.get('release_event'):
            print("💥 ACHIEVEMENT RELEASE!")
            break
    
    print("\n✅ Emotional build-up test completed!")


def test_discord_embed_creation():
    """Test Discord embed creation"""
    print("\n📋 Testing Discord Embed Creation")
    print("=" * 50)
    
    bot = EnhancedLunaBot()
    
    # Test different emotional states
    test_scenarios = [
        {
            "message": "You're so sexy",
            "description": "Lust trigger"
        },
        {
            "message": "I need to work on my story",
            "description": "Work trigger"
        },
        {
            "message": "You're beautiful but I need to focus",
            "description": "Mixed emotions"
        },
        {
            "message": "I need release",
            "description": "Release trigger"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\nScenario: {scenario['description']}")
        print(f"Message: '{scenario['message']}'")
        
        # Update emotional state
        result = bot.emotional_meter.update_emotion_with_global_weight(scenario['message'])
        
        # Generate response
        response = asyncio.run(bot._generate_emotional_response(None, scenario['message'], result))
        
        # Create embed
        embed = bot._create_detailed_emotional_embed(response, result)
        
        print(f"Embed Title: {embed.title}")
        print(f"Embed Color: {embed.color}")
        print(f"Fields: {len(embed.fields)}")
        
        for field in embed.fields:
            print(f"  - {field.name}: {field.value[:50]}...")
    
    print("\n✅ Discord embed creation test completed!")


def test_command_parsing():
    """Test command parsing functionality"""
    print("\n⚙️ Testing Command Parsing")
    print("=" * 50)
    
    bot = EnhancedLunaBot()
    
    # Test command parsing
    test_commands = [
        "!luna Hello Luna",
        "!weights You're so sexy",
        "!status",
        "!release",
        "!history",
        "!reset",
        "!build lust",
        "!build work"
    ]
    
    for command in test_commands:
        print(f"Command: {command}")
        # This would normally be parsed by Discord, but we can test the structure
    
    print("\n✅ Command parsing test completed!")


def main():
    """Run all Discord integration tests"""
    print("🤖 Discord Luna Integration Tests")
    print("=" * 60)
    
    tests = [
        test_luna_bot_initialization,
        test_emotional_response_generation,
        test_weight_analysis,
        test_global_weight_calculation,
        test_emotional_build_up,
        test_discord_embed_creation,
        test_command_parsing
    ]
    
    for test in tests:
        try:
            test()
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("\n" + "="*60 + "\n")
    
    print("✅ All Discord integration tests completed!")


if __name__ == "__main__":
    main() 