#!/usr/bin/env python3
"""
Test script for the Emotional Blender System
Demonstrates how to combine emotional fragments
"""

from emotional_blender import EmotionalBlender

def test_emotional_blending():
    """Test the emotional blending system"""
    
    blender = EmotionalBlender()
    
    print("🎭 Emotional Blender System Test")
    print("=" * 50)
    
    # Test 1: Simple blend
    print("\n1. Simple Blend: Happy + Lustful")
    happy_lustful = blender.blend_emotions("happy", ["lustful"])
    print(f"Result: {happy_lustful['name']}")
    print(f"Description: {happy_lustful['description']}")
    print(f"Keywords: {', '.join(happy_lustful['keywords'])}")
    print(f"Example phrases: {happy_lustful['phrases']}")
    
    # Test 2: Complex blend
    print("\n2. Complex Blend: Sad + Lustful + Grateful")
    complex_emotion = blender.create_complex_emotion(
        ["sad", "lustful", "grateful"], 
        [0.4, 0.8, 0.6]
    )
    print(f"Result: {complex_emotion['name']}")
    print(f"Description: {complex_emotion['description']}")
    print(f"Keywords: {', '.join(complex_emotion['keywords'])}")
    
    # Test 3: Suggested combinations
    print("\n3. Suggested Emotion Combinations:")
    combinations = blender.suggest_emotion_combinations()
    for primary, secondary, description in combinations[:5]:
        print(f"• {primary} + {', '.join(secondary)}: {description}")
    
    # Test 4: Keyword search
    print("\n4. Finding emotions by keywords:")
    lustful_emotions = blender.get_emotion_by_keywords(["lustful", "desire", "passionate"])
    print(f"Emotions with lust/desire keywords: {', '.join(lustful_emotions)}")
    
    # Test 5: Create a romantic blend
    print("\n5. Romantic Blend: Seductive + Submissive + Grateful")
    romantic_blend = blender.blend_emotions("seductive", ["submissive", "grateful"])
    print(f"Result: {romantic_blend['name']}")
    print(f"Description: {romantic_blend['description']}")
    print(f"Example phrases: {romantic_blend['phrases']}")

if __name__ == "__main__":
    test_emotional_blending() 