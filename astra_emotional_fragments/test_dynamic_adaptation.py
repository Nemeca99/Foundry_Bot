#!/usr/bin/env python3
"""
Test script for Dynamic Emotion Adaptation
Demonstrates rapid context switching and emotional adaptation
"""

from dynamic_emotion_engine import DynamicEmotionEngine

def test_dynamic_adaptation():
    """Test the dynamic emotion adaptation system"""
    
    engine = DynamicEmotionEngine()
    
    print("🎭 Dynamic Emotion Adaptation Test")
    print("=" * 50)
    
    # Test scenarios that demonstrate rapid context switching
    scenarios = [
        # Romantic to Casual
        ("I want you so badly right now...", "romantic"),
        ("What should we have for dinner tonight?", "casual"),
        
        # Creative to Emotional
        ("I need help with my novel's plot", "creative"),
        ("I'm feeling really sad today", "emotional"),
        
        # Playful to Serious
        ("You're so funny!", "playful"),
        ("I have a serious problem I need to discuss", "serious"),
        
        # Professional to Romantic
        ("I have a big meeting tomorrow", "professional"),
        ("I miss your touch", "romantic"),
        
        # Casual to Creative
        ("How was your day?", "casual"),
        ("I'm writing a new chapter", "creative")
    ]
    
    print("\nTesting Rapid Context Switching:")
    print("-" * 30)
    
    for user_message, expected_context in scenarios:
        print(f"\nUser: {user_message}")
        print(f"Expected Context: {expected_context}")
        
        # Handle the context switch
        context_switch = engine.handle_rapid_context_switch(user_message)
        
        # Generate response
        response = engine.generate_contextual_response(user_message, context_switch)
        
        print(f"AI Response: {response}")
        print(f"Current Emotion: {engine.current_emotion}")
        print(f"Detected Topics: {context_switch['context']['topics']}")
        print(f"Action: {context_switch['action']}")
        
        if context_switch['action'] == 'transition':
            transition = context_switch['transition']
            print(f"Transition: {transition['from_emotion']} → {transition['to_emotion']}")
        
        print("-" * 50)

def test_specific_scenarios():
    """Test specific scenarios like sex to sunsets"""
    
    engine = DynamicEmotionEngine()
    
    print("\n🎭 Specific Scenario Tests")
    print("=" * 50)
    
    # Test the exact scenarios you mentioned
    scenarios = [
        ("I want to make love to you right now", "romantic"),
        ("What do you think about the sunset?", "casual"),
        ("I'm working on my book", "creative"),
        ("What should we have for dinner?", "casual"),
        ("I need you to dominate me", "romantic"),
        ("How's the weather today?", "casual")
    ]
    
    for user_message, expected_context in scenarios:
        print(f"\nUser: {user_message}")
        
        context_switch = engine.handle_rapid_context_switch(user_message)
        response = engine.generate_contextual_response(user_message, context_switch)
        
        print(f"AI Response: {response}")
        print(f"Emotion: {engine.current_emotion}")
        print(f"Context: {context_switch['context']['topics']}")

if __name__ == "__main__":
    test_dynamic_adaptation()
    test_specific_scenarios() 