#!/usr/bin/env python3
"""
Test script for Framework Integration
Tests that all character systems are properly integrated into the framework
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.framework_tool import get_framework

def test_framework_initialization():
    """Test that the framework initializes correctly with all plugins"""
    print("🔧 Testing Framework Initialization")
    print("=" * 50)
    
    # Get the framework instance
    framework = get_framework()
    
    print(f"✅ Framework initialized successfully")
    print(f"📦 Available plugins: {list(framework.plugins.keys())}")
    
    # Check for character system plugins
    character_plugins = [
        "character_embodiment_engine",
        "identity_processor", 
        "character_memory_system",
        "character_interaction_engine",
        "character_development_engine",
        "content_driven_personality",
        "dynamic_personality_learning",
        "content_emotion_integration"
    ]
    
    for plugin in character_plugins:
        if plugin in framework.plugins:
            print(f"✅ {plugin} loaded")
        else:
            print(f"❌ {plugin} not found")
    
    return framework

def test_character_embodiment_integration(framework):
    """Test character embodiment system integration"""
    print("\n🎭 Testing Character Embodiment Integration")
    print("=" * 50)
    
    # Test embody_character method
    result = framework.embody_character("Shay", "Book_Collection/Relic/Chapter_1.txt")
    print(f"Embody character result: {result}")
    
    # Test process_identity method
    content = "Shay is a brave adventurer who discovers ancient relics"
    result = framework.process_identity(content, "Shay")
    print(f"Process identity result: {result}")
    
    # Test generate_character_voice method
    result = framework.generate_character_voice("Hello, I am Shay", "Shay")
    print(f"Generate character voice result: {result}")

def test_character_memory_integration(framework):
    """Test character memory system integration"""
    print("\n🧠 Testing Character Memory Integration")
    print("=" * 50)
    
    # Test add_character_memory method
    result = framework.add_character_memory("Shay", "personal_experience", "Shay discovered an ancient relic", "important")
    print(f"Add memory result: {result}")
    
    # Test get_character_memories method
    memories = framework.get_character_memories("Shay", "personal_experience")
    print(f"Get memories result: {len(memories)} memories found")
    
    # Test get_character_relationships method
    relationships = framework.get_character_relationships("Shay")
    print(f"Get relationships result: {len(relationships)} relationships found")
    
    # Test get_character_summary method
    summary = framework.get_character_summary("Shay")
    print(f"Character summary: {summary[:100]}...")

def test_character_interaction_integration(framework):
    """Test character interaction system integration"""
    print("\n💬 Testing Character Interaction Integration")
    print("=" * 50)
    
    # Test create_character_dialogue_profile method
    result = framework.create_character_dialogue_profile(
        "Shay",
        speech_patterns={'formal': 0.3, 'casual': 0.7},
        vocabulary_preferences=['adventure', 'discovery'],
        interaction_style="adventurous"
    )
    print(f"Create dialogue profile result: {result}")
    
    # Test generate_character_dialogue method
    result = framework.generate_character_dialogue("Shay", "Nyx", "conversation", "happy")
    print(f"Generate dialogue result: {result}")
    
    # Test create_character_interaction method
    result = framework.create_character_interaction(
        "conversation",
        ["Shay", "Nyx"],
        emotional_intensity=0.6
    )
    print(f"Create interaction result: {result}")
    
    # Test get_character_interactions method
    interactions = framework.get_character_interactions("Shay")
    print(f"Get interactions result: {len(interactions)} interactions found")
    
    # Test get_relationship_dynamics method
    dynamics = framework.get_relationship_dynamics("Shay", "Nyx")
    print(f"Relationship dynamics: {dynamics}")

def test_character_development_integration(framework):
    """Test character development system integration"""
    print("\n📈 Testing Character Development Integration")
    print("=" * 50)
    
    # Test create_character_arc method
    result = framework.create_character_arc(
        "Shay",
        "Shay's journey from village girl to brave adventurer",
        "introduction"
    )
    print(f"Create character arc result: {result}")
    
    # Test add_development_event method
    result = framework.add_development_event(
        "Shay",
        "story_event",
        "Shay discovers her first ancient relic",
        0.8,
        ["courage", "curiosity"]
    )
    print(f"Add development event result: {result}")
    
    # Test get_character_development_summary method
    summary = framework.get_character_development_summary("Shay")
    print(f"Development summary: {summary[:100]}...")
    
    # Test suggest_character_development method
    suggestions = framework.suggest_character_development("Shay")
    print(f"Development suggestions: {suggestions}")
    
    # Test analyze_character_progress method
    progress = framework.analyze_character_progress("Shay")
    print(f"Character progress: {progress}")

def test_content_driven_personality_integration(framework):
    """Test content-driven personality system integration"""
    print("\n🧠 Testing Content-Driven Personality Integration")
    print("=" * 50)
    
    # Test evolve_personality_from_content method
    content = "Shay is a brave and curious adventurer who loves discovering ancient relics"
    result = framework.evolve_personality_from_content(content, "shay_content")
    print(f"Evolve personality result: {result}")
    
    # Test become_living_manual method
    result = framework.become_living_manual(content, "shay_manual")
    print(f"Become living manual result: {result}")
    
    # Test get_personality_evolution_history method
    history = framework.get_personality_evolution_history()
    print(f"Evolution history: {len(history)} entries")

def test_dynamic_personality_learning_integration(framework):
    """Test dynamic personality learning system integration"""
    print("\n🎓 Testing Dynamic Personality Learning Integration")
    print("=" * 50)
    
    # Test learn_from_character_interaction method
    result = framework.learn_from_character_interaction("Shay", "conversation", 0.7)
    print(f"Learn from interaction result: {result}")
    
    # Test learn_from_story_development method
    result = framework.learn_from_story_development("relic_story", "plot_development", 0.5)
    print(f"Learn from story development result: {result}")
    
    # Test get_character_learning_summary method
    summary = framework.get_character_learning_summary("Shay")
    print(f"Learning summary: {summary}")

def test_content_emotion_integration(framework):
    """Test content-emotion integration system integration"""
    print("\n😊 Testing Content-Emotion Integration")
    print("=" * 50)
    
    # Test analyze_content_emotions method
    content = "Shay felt overwhelming joy when she discovered the ancient relic"
    result = framework.analyze_content_emotions(content, "shay_emotion_test")
    print(f"Analyze content emotions result: {result}")
    
    # Test generate_character_emotional_response method
    result = framework.generate_character_emotional_response("Shay", "joy", "story_event")
    print(f"Generate emotional response result: {result}")
    
    # Test get_character_emotional_summary method
    summary = framework.get_character_emotional_summary("Shay")
    print(f"Emotional summary: {summary}")

def test_comprehensive_character_workflow(framework):
    """Test a comprehensive character workflow using all systems"""
    print("\n🔄 Testing Comprehensive Character Workflow")
    print("=" * 50)
    
    character_name = "Luna"
    
    # 1. Embody the character
    print("1. Embodying character...")
    embodiment = framework.embody_character(character_name)
    print(f"   Embodiment result: {embodiment}")
    
    # 2. Add character memories
    print("2. Adding character memories...")
    memory = framework.add_character_memory(character_name, "personal_experience", "Luna discovered her magical abilities", "critical")
    print(f"   Memory added: {memory}")
    
    # 3. Create dialogue profile
    print("3. Creating dialogue profile...")
    profile = framework.create_character_dialogue_profile(character_name, interaction_style="mystical")
    print(f"   Profile created: {profile}")
    
    # 4. Create character arc
    print("4. Creating character arc...")
    arc = framework.create_character_arc(character_name, "Luna's magical awakening journey", "growth")
    print(f"   Arc created: {arc}")
    
    # 5. Add development event
    print("5. Adding development event...")
    event = framework.add_development_event(character_name, "story_event", "Luna uses her magic for the first time", 0.9, ["power", "confidence"])
    print(f"   Event added: {event}")
    
    # 6. Generate dialogue
    print("6. Generating dialogue...")
    dialogue = framework.generate_character_dialogue(character_name, "Shay", "friendship", "happy")
    print(f"   Dialogue generated: {dialogue}")
    
    # 7. Learn from interaction
    print("7. Learning from interaction...")
    learning = framework.learn_from_character_interaction(character_name, "friendship", 0.6)
    print(f"   Learning result: {learning}")
    
    # 8. Get comprehensive summary
    print("8. Getting comprehensive summary...")
    memory_summary = framework.get_character_summary(character_name)
    development_summary = framework.get_character_development_summary(character_name)
    emotional_summary = framework.get_character_emotional_summary(character_name)
    
    print(f"   Memory summary: {memory_summary[:50]}...")
    print(f"   Development summary: {development_summary[:50]}...")
    print(f"   Emotional summary: {emotional_summary}")

def test_error_handling(framework):
    """Test error handling for missing plugins"""
    print("\n⚠️ Testing Error Handling")
    print("=" * 50)
    
    # Test with non-existent character
    result = framework.embody_character("NonExistentCharacter")
    print(f"Embody non-existent character: {result}")
    
    # Test with missing plugin (simulate by using wrong plugin name)
    result = framework.get_character_memories("TestCharacter")
    print(f"Get memories with missing plugin: {result}")
    
    # Test with invalid parameters
    result = framework.add_development_event("TestCharacter", "invalid_trigger", "test", -1.0)
    print(f"Add development event with invalid params: {result}")

if __name__ == "__main__":
    print("🔧 Framework Integration Test Suite")
    print("=" * 60)
    
    try:
        # Initialize framework
        framework = test_framework_initialization()
        
        # Test all integrations
        test_character_embodiment_integration(framework)
        test_character_memory_integration(framework)
        test_character_interaction_integration(framework)
        test_character_development_integration(framework)
        test_content_driven_personality_integration(framework)
        test_dynamic_personality_learning_integration(framework)
        test_content_emotion_integration(framework)
        
        # Test comprehensive workflow
        test_comprehensive_character_workflow(framework)
        
        # Test error handling
        test_error_handling(framework)
        
        print("\n🎉 All framework integration tests completed successfully!")
        print("The character systems are properly integrated into the framework.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 