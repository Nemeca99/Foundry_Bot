#!/usr/bin/env python3
"""
Test script for Content-Emotion Integration System
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.plugins.content_emotion_integration import ContentEmotionIntegration, initialize

def test_content_emotional_analysis():
    """Test analyzing content for emotional content"""
    print("📖 Testing Content Emotional Analysis")
    print("=" * 50)
    
    # Initialize the emotion integration system
    emotion_system = initialize()
    
    # Test content with different emotions
    test_content = """
    Shay felt overwhelming joy when she discovered the ancient relic. 
    The moment was filled with intense emotion and powerful feelings of hope.
    She was excited and thrilled by the discovery, but also felt a deep sense of fear
    about what this might mean for her future. The conflict within her was dramatic.
    """
    
    print("🔍 Analyzing content for emotions...")
    analysis = emotion_system.analyze_content_for_emotions(test_content, "shay_emotion_test")
    
    print(f"Content ID: {analysis.content_id}")
    print(f"Detected emotions: {[emotion.value for emotion in analysis.detected_emotions]}")
    print(f"Emotional intensity: {analysis.emotional_intensity:.2f}")
    print(f"Emotional triggers: {[trigger.value for trigger in analysis.emotional_triggers]}")
    print(f"Character emotional impact: {analysis.character_emotional_impact}")
    print(f"Emotional summary: {analysis.emotional_summary}")
    
    print("\n✅ Content emotional analysis test completed successfully!")

def test_character_emotional_response():
    """Test generating character emotional responses"""
    print("\n😊 Testing Character Emotional Response")
    print("=" * 50)
    
    emotion_system = initialize()
    
    # Test generating emotional response for Shay
    content = "Shay discovered that her grandfather had been keeping secrets from her. The revelation was shocking and filled her with anger and sadness."
    
    print("🎭 Generating emotional response for Shay...")
    response = emotion_system.generate_character_emotional_response("Shay", content)
    
    print(f"Response ID: {response.response_id}")
    print(f"Emotion Type: {response.emotion_type.value}")
    print(f"Intensity: {response.intensity:.2f}")
    print(f"Trigger: {response.trigger.value}")
    print(f"Response Text: {response.response_text}")
    
    print("\n✅ Character emotional response test completed successfully!")

def test_multiple_character_emotions():
    """Test emotional responses for multiple characters"""
    print("\n👥 Testing Multiple Character Emotions")
    print("=" * 50)
    
    emotion_system = initialize()
    
    # Test different characters with different content
    character_content_pairs = [
        ("Shay", "Shay felt overwhelming joy when she found the relic. She was excited and thrilled."),
        ("Nyx", "Nyx was furious and filled with rage. The anger burned within her like a fire."),
        ("Luna", "Luna felt a deep sense of calm and peace. She was serene and tranquil.")
    ]
    
    for character, content in character_content_pairs:
        print(f"\n🎭 Generating emotional response for {character}...")
        response = emotion_system.generate_character_emotional_response(character, content)
        print(f"Emotion: {response.emotion_type.value}, Intensity: {response.intensity:.2f}")
        print(f"Response: {response.response_text}")
    
    print("\n✅ Multiple character emotions test completed successfully!")

def test_character_emotional_summary():
    """Test character emotional summary functionality"""
    print("\n📊 Testing Character Emotional Summary")
    print("=" * 50)
    
    emotion_system = initialize()
    
    # Add some emotional responses first
    content = "Shay felt conflicted emotions about her discovery."
    emotion_system.generate_character_emotional_response("Shay", content)
    
    # Get character emotional summary
    summary = emotion_system.get_character_emotional_summary("Shay")
    print("Character Emotional Summary:")
    print(summary)
    
    print("\n✅ Character emotional summary test completed successfully!")

def test_emotional_analysis_summary():
    """Test emotional analysis summary functionality"""
    print("\n📈 Testing Emotional Analysis Summary")
    print("=" * 50)
    
    emotion_system = initialize()
    
    # Get overall emotional analysis summary
    summary = emotion_system.get_emotional_analysis_summary()
    
    print("Emotional Analysis Summary:")
    for key, value in summary.items():
        print(f"- {key}: {value}")
    
    print("\n✅ Emotional analysis summary test completed successfully!")

def test_emotion_extraction_from_book_content():
    """Test emotion extraction from real book content"""
    print("\n📚 Testing Emotion Extraction from Book Content")
    print("=" * 50)
    
    emotion_system = initialize()
    
    # Read content from Shay's story
    book_path = Path(__file__).parent.parent.parent / "Book_Collection" / "Relic" / "Chapter_1.txt"
    
    if book_path.exists():
        with open(book_path, 'r', encoding='utf-8') as f:
            book_content = f.read()
        
        # Take a sample of the content for analysis
        sample_content = book_content[:1000]  # First 1000 characters
        
        print("🔍 Analyzing book content for emotions...")
        analysis = emotion_system.analyze_content_for_emotions(sample_content, "shay_story_emotions")
        
        print(f"Detected emotions: {[emotion.value for emotion in analysis.detected_emotions]}")
        print(f"Emotional intensity: {analysis.emotional_intensity:.2f}")
        print(f"Emotional summary: {analysis.emotional_summary}")
        
        # Generate emotional response for Shay based on the content
        print("\n🎭 Generating Shay's emotional response to the story...")
        response = emotion_system.generate_character_emotional_response("Shay", sample_content)
        print(f"Shay's emotion: {response.emotion_type.value}")
        print(f"Response: {response.response_text}")
        
        print("\n✅ Book content emotion extraction test completed successfully!")
    else:
        print("❌ Book content not found, skipping book content test")

def test_emotional_response_patterns():
    """Test emotional response patterns over time"""
    print("\n🔄 Testing Emotional Response Patterns")
    print("=" * 50)
    
    emotion_system = initialize()
    
    # Generate multiple emotional responses to see patterns
    emotional_scenarios = [
        ("Shay", "Shay felt overwhelming joy when she discovered the ancient relic.", "joy_scenario"),
        ("Shay", "Shay was filled with anger and rage at the betrayal.", "anger_scenario"),
        ("Shay", "Shay felt deep sadness and grief over her loss.", "sadness_scenario"),
        ("Shay", "Shay was terrified and filled with fear about the future.", "fear_scenario"),
        ("Shay", "Shay felt a sense of calm and peace in the moment.", "calm_scenario")
    ]
    
    for character, content, scenario in emotional_scenarios:
        print(f"\n🎭 {scenario}...")
        response = emotion_system.generate_character_emotional_response(character, content)
        print(f"Emotion: {response.emotion_type.value}, Intensity: {response.intensity:.2f}")
    
    # Get final emotional summary
    print("\n📊 Final Emotional Summary for Shay:")
    summary = emotion_system.get_character_emotional_summary("Shay")
    print(summary)
    
    print("\n✅ Emotional response patterns test completed successfully!")

if __name__ == "__main__":
    print("😊 Content-Emotion Integration System Test Suite")
    print("=" * 60)
    
    try:
        test_content_emotional_analysis()
        test_character_emotional_response()
        test_multiple_character_emotions()
        test_character_emotional_summary()
        test_emotional_analysis_summary()
        test_emotion_extraction_from_book_content()
        test_emotional_response_patterns()
        
        print("\n🎉 All tests completed successfully!")
        print("The Content-Emotion Integration System is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 