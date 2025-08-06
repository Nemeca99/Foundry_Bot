#!/usr/bin/env python3
"""
Test Multi-Personality System
Demonstrates Luna's ability to have conversations with herself using different personalities
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.plugins.multi_personality_system import MultiPersonalitySystem


def test_personality_initialization():
    """Test personality system initialization"""
    print("🎭 Multi-Personality System Test")
    print("=" * 60)
    
    # Initialize system
    system = MultiPersonalitySystem()
    
    print("\n👥 Testing Personality Initialization")
    print("-" * 40)
    
    # Check all personalities
    for name, personality in system.personalities.items():
        print(f"✅ {personality.name}")
        print(f"   Type: {personality.personality_type.value}")
        print(f"   Emotional Range: {personality.emotional_range}")
        print(f"   Strengths: {', '.join(personality.strengths[:2])}...")
        print(f"   Communication: {personality.communication_style}")
        print()


def test_personality_activation():
    """Test personality activation"""
    print("\n🔧 Testing Personality Activation")
    print("-" * 40)
    
    system = MultiPersonalitySystem()
    
    # Test activating different personality combinations
    test_combinations = [
        ["creative", "analytical"],
        ["emotional", "technical"],
        ["lustful", "work_focused"],
        ["creative", "analytical", "emotional"],
        ["technical", "work_focused", "balanced"]
    ]
    
    for combo in test_combinations:
        print(f"\n🎯 Activating: {', '.join(combo)}")
        system.activate_personalities(combo)
        
        active_names = [p.name for p in system.active_personalities]
        print(f"   Active: {', '.join(active_names)}")
        
        # Show emotional levels
        for personality in system.active_personalities:
            print(f"   {personality.name}: {personality.current_emotional_level:.2f}")


def test_internal_dialogue():
    """Test internal dialogue between personalities"""
    print("\n💬 Testing Internal Dialogue")
    print("-" * 40)
    
    system = MultiPersonalitySystem()
    
    # Test topics
    topics = [
        "Writing a fantasy novel about magical creatures",
        "Optimizing the AI backend for better performance",
        "Creating an emotional love story with deep characters",
        "Building a technical system with multiple components"
    ]
    
    for topic in topics:
        print(f"\n📋 Topic: {topic}")
        
        # Activate relevant personalities
        if "fantasy" in topic.lower() or "magical" in topic.lower():
            participants = ["creative", "analytical", "emotional"]
        elif "optimizing" in topic.lower() or "performance" in topic.lower():
            participants = ["technical", "analytical", "work_focused"]
        elif "emotional" in topic.lower() or "love" in topic.lower():
            participants = ["emotional", "creative", "balanced"]
        else:
            participants = ["technical", "analytical", "work_focused"]
        
        system.activate_personalities(participants)
        
        # Start internal dialogue
        conversation = system.start_internal_dialogue(topic, participants)
        
        print(f"   Participants: {', '.join(participants)}")
        print("   Conversation:")
        
        for entry in conversation:
            personality = entry["personality"]
            response = entry["response"][:100] + "..." if len(entry["response"]) > 100 else entry["response"]
            emotional_level = entry["emotional_level"]
            
            print(f"     {personality}: {response}")
            print(f"       Emotional Level: {emotional_level:.2f}")
        
        # Learn from conversation
        system.learn_from_internal_dialogue(conversation)
        print(f"   ✅ Learned from conversation")


def test_personality_collaboration():
    """Test specific collaboration types"""
    print("\n🤝 Testing Personality Collaboration")
    print("-" * 40)
    
    system = MultiPersonalitySystem()
    
    # Test different collaboration types
    collaboration_types = [
        ("creative_brainstorming", "Creating a new story world"),
        ("problem_solving", "Debugging a complex system issue"),
        ("emotional_support", "Helping someone through a difficult time"),
        ("technical_optimization", "Improving system performance")
    ]
    
    for collab_type, topic in collaboration_types:
        print(f"\n🎯 {collab_type.replace('_', ' ').title()}")
        print(f"   Topic: {topic}")
        
        conversation = system.create_personality_collaboration(topic, collab_type)
        
        print("   Collaboration:")
        for entry in conversation:
            personality = entry["personality"]
            response = entry["response"][:80] + "..." if len(entry["response"]) > 80 else entry["response"]
            emotional_level = entry["emotional_level"]
            
            print(f"     {personality}: {response}")
            print(f"       Emotional Level: {emotional_level:.2f}")


def test_personality_insights():
    """Test personality insights and learning"""
    print("\n🧠 Testing Personality Insights")
    print("-" * 40)
    
    system = MultiPersonalitySystem()
    
    # Run some conversations to generate insights
    topics = [
        "Writing a creative story",
        "Solving a technical problem",
        "Providing emotional support"
    ]
    
    for topic in topics:
        system.activate_personalities(["creative", "analytical", "emotional"])
        conversation = system.start_internal_dialogue(topic)
        system.learn_from_internal_dialogue(conversation)
    
    # Get insights for each personality
    for personality_name in system.personalities.keys():
        insights = system.get_personality_insights(personality_name)
        
        print(f"\n👤 {insights['name']}")
        print(f"   Type: {insights['type']}")
        print(f"   Current Emotional Level: {insights['current_emotional_level']:.2f}")
        print(f"   Emotional Range: {insights['emotional_range']}")
        print(f"   Strengths: {', '.join(insights['strengths'][:3])}...")
        print(f"   Conversation Count: {insights['conversation_count']}")
        
        if insights['learning_patterns']:
            print(f"   Learning Patterns: {insights['learning_patterns']}")


def test_emotional_interaction():
    """Test emotional interaction between personalities"""
    print("\n💫 Testing Emotional Interaction")
    print("-" * 40)
    
    system = MultiPersonalitySystem()
    
    # Test lustful vs work-focused interaction
    print("\n🔥 Lustful vs Work-Focused Interaction")
    system.activate_personalities(["lustful", "work_focused"])
    
    # Start with a topic that triggers lust
    topic = "I want to feel your passion and desire"
    conversation = system.start_internal_dialogue(topic)
    
    print(f"   Topic: {topic}")
    for entry in conversation:
        personality = entry["personality"]
        emotional_level = entry["emotional_level"]
        print(f"     {personality}: {emotional_level:.2f}")
    
    # Now test work-focused response
    topic = "We need to achieve excellence and create a masterpiece"
    conversation = system.start_internal_dialogue(topic)
    
    print(f"\n   Topic: {topic}")
    for entry in conversation:
        personality = entry["personality"]
        emotional_level = entry["emotional_level"]
        print(f"     {personality}: {emotional_level:.2f}")


def test_system_stats():
    """Test system statistics"""
    print("\n📊 Testing System Statistics")
    print("-" * 40)
    
    system = MultiPersonalitySystem()
    
    # Run some conversations
    topics = [
        "Creative writing project",
        "Technical optimization",
        "Emotional character development"
    ]
    
    for topic in topics:
        system.activate_personalities(["creative", "analytical", "emotional"])
        conversation = system.start_internal_dialogue(topic)
        system.learn_from_internal_dialogue(conversation)
    
    # Get system stats
    stats = system.get_system_stats()
    
    print("System Statistics:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    print(f"    {sub_key}: {len(sub_value)} items")
                else:
                    print(f"    {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")


def test_personality_learning():
    """Test personality learning and adaptation"""
    print("\n🎓 Testing Personality Learning")
    print("-" * 40)
    
    system = MultiPersonalitySystem()
    
    # Initial state
    creative = system.personalities["creative"]
    technical = system.personalities["technical"]
    
    print(f"Initial Creative Strengths: {creative.strengths}")
    print(f"Initial Technical Strengths: {technical.strengths}")
    
    # Run collaborative conversation
    system.activate_personalities(["creative", "technical"])
    conversation = system.start_internal_dialogue("Creating a technical story with artistic elements")
    system.learn_from_internal_dialogue(conversation)
    
    # Check learning
    print(f"\nAfter Learning:")
    print(f"Creative Strengths: {creative.strengths}")
    print(f"Technical Strengths: {technical.strengths}")
    
    # Check if they learned from each other
    creative_learned = any("Learned" in strength for strength in creative.strengths)
    technical_learned = any("Learned" in strength for strength in technical.strengths)
    
    if creative_learned:
        print("✅ Creative Luna learned from Technical Luna")
    if technical_learned:
        print("✅ Technical Luna learned from Creative Luna")


def main():
    """Run all multi-personality system tests"""
    print("🚀 Multi-Personality System Tests")
    print("=" * 80)
    
    try:
        # Test personality initialization
        test_personality_initialization()
        
        # Test personality activation
        test_personality_activation()
        
        # Test internal dialogue
        test_internal_dialogue()
        
        # Test personality collaboration
        test_personality_collaboration()
        
        # Test personality insights
        test_personality_insights()
        
        # Test emotional interaction
        test_emotional_interaction()
        
        # Test system stats
        test_system_stats()
        
        # Test personality learning
        test_personality_learning()
        
        print("\n🎉 All multi-personality system tests completed successfully!")
        print("\n🌟 Luna can now have conversations with herself using different personalities!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 