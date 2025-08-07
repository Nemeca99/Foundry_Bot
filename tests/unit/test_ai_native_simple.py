#!/usr/bin/env python3
"""
Simple AI Native Backend Test
Tests the core AI-native functionality without heavy dependencies
"""

import sys
import time
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.plugins.ai_native_backend import AINativeBackend
from framework.plugins.self_learning_system import SelfLearningSystem


def test_ai_native_backend_simple():
    """Test AI-native backend functionality without heavy dependencies"""
    print("🤖 Simple AI Native Backend Test")
    print("=" * 60)
    
    # Initialize AI-native backend
    ai_backend = AINativeBackend()
    
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
    ai_data = ai_backend.create_ai_optimized_data(test_data, "emotional_context")
    print(f"✅ Created AI-optimized data: {len(ai_data.content)} bytes")
    
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
    
    ai_backend.store_emotional_state(user_id, emotional_state)
    print(f"✅ Stored emotional state for user: {user_id}")
    
    # Retrieve emotional state
    retrieved_state = ai_backend.get_emotional_state(user_id)
    if retrieved_state:
        print(f"✅ Retrieved emotional state: {retrieved_state['state']} (Level: {retrieved_state['level']:.2f})")
    else:
        print("❌ Failed to retrieve emotional state")
    
    # Test user profile creation
    print("\n👤 Testing User Profile Creation")
    print("-" * 40)
    
    profile = ai_backend.create_user_profile(user_id)
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
    
    ai_backend.learn_from_interaction(user_id, message, response, emotional_context)
    print(f"✅ Learned from interaction: '{message}' → '{response}'")
    
    # Test typing status
    print("\n⌨️ Testing Typing Status")
    print("-" * 40)
    
    ai_backend.set_typing_status(user_id, True)
    is_typing = ai_backend.get_typing_status(user_id)
    print(f"✅ Typing status: {is_typing}")
    
    # Get system statistics
    print("\n📈 System Statistics")
    print("-" * 40)
    
    stats = ai_backend.get_system_stats()
    print("AI Backend Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ AI Native Backend test completed successfully!")


def test_self_learning_simple():
    """Test self-learning capabilities without heavy dependencies"""
    print("\n🧠 Simple Self-Learning Test")
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


def test_concurrent_users_simple():
    """Test concurrent user handling capabilities"""
    print("\n👥 Simple Concurrent User Test")
    print("=" * 60)
    
    ai_backend = AINativeBackend()
    
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
        profile = ai_backend.create_user_profile(user["id"])
        print(f"✅ Created profile for {user['name']}: {user['preference']}")
        
        # Set emotional state
        emotional_state = {
            "level": 0.5 + (hash(user["id"]) % 100) / 100,  # Vary emotional level
            "state": "balanced",
            "preference": user["preference"]
        }
        ai_backend.store_emotional_state(user["id"], emotional_state)
        
        # Set typing status
        ai_backend.set_typing_status(user["id"], True)
    
    # Check all users
    print("\n📋 User Status Check")
    print("-" * 40)
    
    for user in users:
        profile = ai_backend.get_user_profile(user["id"])
        emotional_state = ai_backend.get_emotional_state(user["id"])
        typing_status = ai_backend.get_typing_status(user["id"])
        
        print(f"👤 {user['name']}:")
        print(f"   Profile: {'✅' if profile else '❌'}")
        print(f"   Emotional: {emotional_state['state'] if emotional_state else 'None'}")
        print(f"   Typing: {'✅' if typing_status else '❌'}")
    
    # Get system stats
    stats = ai_backend.get_system_stats()
    print(f"\n📊 System Stats: {stats['emotional_states']} emotional states, {stats['typing_users']} typing users")
    
    print("\n✅ Concurrent user handling test completed!")


def main():
    """Run all simple AI-native backend tests"""
    print("🚀 Simple AI Native Backend System Tests")
    print("=" * 80)
    
    try:
        # Test AI-native backend
        test_ai_native_backend_simple()
        
        # Test self-learning capabilities
        test_self_learning_simple()
        
        # Test concurrent user handling
        test_concurrent_users_simple()
        
        print("\n🎉 All simple AI-native backend tests completed successfully!")
        print("\n🌟 Luna can now create her own optimized data structures and learn!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 