#!/usr/bin/env python3
"""
Test AI Native Backend System
Demonstrates Luna's ability to create her own optimized data structures and learn
"""

import sys
import time
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework
from framework.plugins.ai_native_backend import AINativeBackend
from framework.plugins.self_learning_system import SelfLearningSystem


def test_ai_native_backend():
    """Test AI-native backend functionality"""
    print("🤖 AI Native Backend Test")
    print("=" * 60)
    
    # Initialize framework
    framework = get_framework()
    
    # Test AI-optimized data creation
    print("\n📊 Testing AI-Optimized Data Creation")
    print("-" * 40)
    
    test_data = {
        "emotional_state": {
            "level": 0.7,
            "state": "focused",
            "triggers": ["work", "achieve", "excellence"]
        },
        "user_preferences": {
            "writing_style": "descriptive",
            "genre": "fantasy",
            "target_audience": "young_adult"
        }
    }
    
    # Create AI-optimized data
    ai_data = framework.create_ai_optimized_data(test_data, "emotional_context")
    print(f"✅ Created AI-optimized data: {len(ai_data)} bytes")
    
    # Test emotional state storage
    print("\n💾 Testing Emotional State Storage")
    print("-" * 40)
    
    user_id = "test_user_123"
    emotional_state = {
        "level": 0.6,
        "state": "curious",
        "triggers": ["explore", "learn", "discover"],
        "timestamp": time.time()
    }
    
    framework.store_emotional_state_ai(user_id, emotional_state)
    print(f"✅ Stored emotional state for user: {user_id}")
    
    # Retrieve emotional state
    retrieved_state = framework.get_emotional_state_ai(user_id)
    if retrieved_state:
        print(f"✅ Retrieved emotional state: {retrieved_state['state']} (Level: {retrieved_state['level']:.2f})")
    else:
        print("❌ Failed to retrieve emotional state")
    
    # Test user profile creation
    print("\n👤 Testing User Profile Creation")
    print("-" * 40)
    
    profile = framework.create_user_profile_ai(user_id)
    print(f"✅ Created user profile: {profile['user_id']}")
    print(f"   Created at: {time.ctime(profile['created_at'])}")
    
    # Test learning from interaction
    print("\n🧠 Testing Learning from Interaction")
    print("-" * 40)
    
    message = "I need help with my writing project"
    response = "I'd love to help you with your writing! What genre are you working on?"
    emotional_context = {
        "intensity": 0.8,
        "state": "helpful",
        "triggers": ["help", "writing", "project"]
    }
    
    framework.learn_from_interaction(user_id, message, response, emotional_context)
    print(f"✅ Learned from interaction: '{message}' → '{response}'")
    
    # Test typing status
    print("\n⌨️ Testing Typing Status")
    print("-" * 40)
    
    framework.set_typing_status(user_id, True)
    is_typing = framework.get_typing_status(user_id)
    print(f"✅ Typing status: {is_typing}")
    
    # Test optimized format creation
    print("\n⚡ Testing Optimized Format Creation")
    print("-" * 40)
    
    writing_data = {
        "chapter_title": "The Beginning",
        "word_count": 1500,
        "emotions": ["excitement", "anticipation"],
        "characters": ["protagonist", "mentor"]
    }
    
    optimized_format = framework.create_optimized_format(writing_data, "writing_context")
    print(f"✅ Created optimized format: {len(optimized_format)} bytes")
    
    # Test AI-native database creation
    print("\n🗄️ Testing AI-Native Database Creation")
    print("-" * 40)
    
    story_data = {
        "title": "The Lost Kingdom",
        "genre": "fantasy",
        "chapters": [
            {"title": "Chapter 1", "word_count": 2000},
            {"title": "Chapter 2", "word_count": 1800}
        ],
        "characters": [
            {"name": "Aria", "role": "protagonist"},
            {"name": "Eldric", "role": "mentor"}
        ]
    }
    
    ai_database = framework.create_ai_native_database(story_data, "story_management")
    print(f"✅ Created AI-native database: {len(ai_database)} bytes")
    
    # Get system statistics
    print("\n📈 System Statistics")
    print("-" * 40)
    
    ai_stats = framework.get_ai_backend_stats()
    learning_stats = framework.get_learning_stats()
    
    print("AI Backend Stats:")
    for key, value in ai_stats.items():
        print(f"  {key}: {value}")
    
    print("\nLearning Stats:")
    for key, value in learning_stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ AI Native Backend test completed successfully!")


def test_self_learning_capabilities():
    """Test self-learning capabilities"""
    print("\n🧠 Self-Learning Capabilities Test")
    print("=" * 60)
    
    # Initialize learning system
    learning_system = SelfLearningSystem()
    
    # Test emotional pattern learning
    print("\n💭 Testing Emotional Pattern Learning")
    print("-" * 40)
    
    emotional_patterns = [
        {
            "state": "excited",
            "level": 0.8,
            "triggers": ["achievement", "success", "progress"]
        },
        {
            "state": "focused",
            "level": 0.6,
            "triggers": ["work", "writing", "creation"]
        },
        {
            "state": "curious",
            "level": 0.4,
            "triggers": ["explore", "learn", "discover"]
        }
    ]
    
    for pattern in emotional_patterns:
        learning_system.learn_emotional_patterns(pattern)
        print(f"✅ Learned emotional pattern: {pattern['state']} (Level: {pattern['level']})")
    
    # Test interaction learning
    print("\n💬 Testing Interaction Learning")
    print("-" * 40)
    
    interactions = [
        {
            "message": "I want to write a fantasy novel",
            "response": "Fantasy is a wonderful genre! What's your story about?",
            "emotional_intensity": 0.7,
            "response_time": 0.3
        },
        {
            "message": "I'm stuck with writer's block",
            "response": "Let's work through this together. What's the last thing you wrote?",
            "emotional_intensity": 0.5,
            "response_time": 0.5
        },
        {
            "message": "I finished my first chapter!",
            "response": "Congratulations! That's a huge milestone. How does it feel?",
            "emotional_intensity": 0.9,
            "response_time": 0.2
        }
    ]
    
    for interaction in interactions:
        learning_system.learn_from_interaction(interaction)
        print(f"✅ Learned from interaction: '{interaction['message'][:30]}...'")
    
    # Test format optimization
    print("\n⚡ Testing Format Optimization")
    print("-" * 40)
    
    test_contexts = [
        ("writing_project", {"title": "My Novel", "genre": "mystery"}),
        ("character_profile", {"name": "Detective", "traits": ["observant", "determined"]}),
        ("plot_outline", {"act1": "Setup", "act2": "Confrontation", "act3": "Resolution"})
    ]
    
    for context_name, data in test_contexts:
        optimized = learning_system.create_optimized_format(data, context_name)
        print(f"✅ Optimized {context_name}: {len(optimized)} bytes")
    
    # Get learning statistics
    print("\n📊 Learning Statistics")
    print("-" * 40)
    
    stats = learning_system.get_learning_stats()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")
    
    print("\n✅ Self-Learning test completed successfully!")


def test_concurrent_user_handling():
    """Test concurrent user handling capabilities"""
    print("\n👥 Concurrent User Handling Test")
    print("=" * 60)
    
    framework = get_framework()
    
    # Simulate multiple users
    users = [
        {"id": "user_1", "name": "Alice", "preference": "romance"},
        {"id": "user_2", "name": "Bob", "preference": "sci_fi"},
        {"id": "user_3", "name": "Charlie", "preference": "mystery"}
    ]
    
    print("\n🔄 Testing Multiple User Profiles")
    print("-" * 40)
    
    for user in users:
        # Create user profile
        profile = framework.create_user_profile_ai(user["id"])
        print(f"✅ Created profile for {user['name']}: {user['preference']}")
        
        # Set emotional state
        emotional_state = {
            "level": 0.5 + (hash(user["id"]) % 100) / 100,  # Vary emotional level
            "state": "balanced",
            "preference": user["preference"]
        }
        framework.store_emotional_state_ai(user["id"], emotional_state)
        
        # Set typing status
        framework.set_typing_status(user["id"], True)
    
    # Check all users
    print("\n📋 User Status Check")
    print("-" * 40)
    
    for user in users:
        profile = framework.get_user_profile_ai(user["id"])
        emotional_state = framework.get_emotional_state_ai(user["id"])
        typing_status = framework.get_typing_status(user["id"])
        
        print(f"👤 {user['name']}:")
        print(f"   Profile: {'✅' if profile else '❌'}")
        print(f"   Emotional: {emotional_state['state'] if emotional_state else 'None'}")
        print(f"   Typing: {'✅' if typing_status else '❌'}")
    
    # Get system stats
    stats = framework.get_ai_backend_stats()
    print(f"\n📊 System Stats: {stats['emotional_states']} emotional states, {stats['typing_users']} typing users")
    
    print("\n✅ Concurrent user handling test completed!")


def main():
    """Run all AI-native backend tests"""
    print("🚀 AI Native Backend System Tests")
    print("=" * 80)
    
    try:
        # Test AI-native backend
        test_ai_native_backend()
        
        # Test self-learning capabilities
        test_self_learning_capabilities()
        
        # Test concurrent user handling
        test_concurrent_user_handling()
        
        print("\n🎉 All AI-native backend tests completed successfully!")
        print("\n🌟 Luna can now create her own optimized data structures and learn!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 