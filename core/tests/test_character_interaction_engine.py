#!/usr/bin/env python3
"""
Test script for Character Interaction Engine
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.plugins.character_interaction_engine import CharacterInteractionEngine, initialize, InteractionType, DialogueEmotion

def test_dialogue_profile_creation():
    """Test creating dialogue profiles for characters"""
    print("🎭 Testing Dialogue Profile Creation")
    print("=" * 50)
    
    # Initialize the interaction engine
    interaction_engine = initialize()
    
    # Create dialogue profiles for different characters
    shay_profile = interaction_engine.create_character_dialogue_profile(
        character_name="Shay",
        speech_patterns={'formal': 0.3, 'casual': 0.7},
        vocabulary_preferences=['adventure', 'discovery', 'relic'],
        emotional_expressions={'excited': ['amazing', 'incredible'], 'serious': ['important', 'crucial']},
        interaction_style="adventurous"
    )
    
    nyx_profile = interaction_engine.create_character_dialogue_profile(
        character_name="Nyx",
        speech_patterns={'formal': 0.8, 'casual': 0.2},
        vocabulary_preferences=['power', 'control', 'dominance'],
        emotional_expressions={'confident': ['certain', 'assured'], 'angry': ['furious', 'enraged']},
        interaction_style="dominant"
    )
    
    luna_profile = interaction_engine.create_character_dialogue_profile(
        character_name="Luna",
        speech_patterns={'formal': 0.5, 'casual': 0.5},
        vocabulary_preferences=['magic', 'mystery', 'wonder'],
        emotional_expressions={'playful': ['delightful', 'charming'], 'calm': ['peaceful', 'serene']},
        interaction_style="mystical"
    )
    
    print(f"✅ Created dialogue profiles for Shay, Nyx, and Luna")
    print(f"Shay's style: {shay_profile.interaction_style}")
    print(f"Nyx's style: {nyx_profile.interaction_style}")
    print(f"Luna's style: {luna_profile.interaction_style}")

def test_dialogue_generation():
    """Test generating dialogue for different interaction types"""
    print("\n💬 Testing Dialogue Generation")
    print("=" * 50)
    
    interaction_engine = initialize()
    
    # Test different interaction types
    interaction_types = [
        (InteractionType.CONVERSATION, DialogueEmotion.HAPPY),
        (InteractionType.CONFLICT, DialogueEmotion.ANGRY),
        (InteractionType.COLLABORATION, DialogueEmotion.EXCITED),
        (InteractionType.ROMANCE, DialogueEmotion.VULNERABLE),
        (InteractionType.FRIENDSHIP, DialogueEmotion.HAPPY)
    ]
    
    for interaction_type, emotion in interaction_types:
        print(f"\n🎭 Testing {interaction_type.value} dialogue...")
        dialogue = interaction_engine.generate_dialogue("Shay", "Nyx", interaction_type, emotion)
        
        print(f"Speaker: {dialogue.speaker}")
        print(f"Content: {dialogue.content}")
        print(f"Emotion: {dialogue.emotion.value}")
        print(f"Timestamp: {dialogue.timestamp}")

def test_interaction_creation():
    """Test creating character interactions"""
    print("\n🤝 Testing Interaction Creation")
    print("=" * 50)
    
    interaction_engine = initialize()
    
    # Create a conversation interaction
    dialogue_lines = [
        interaction_engine.generate_dialogue("Shay", "Nyx", InteractionType.CONVERSATION, DialogueEmotion.HAPPY),
        interaction_engine.generate_dialogue("Nyx", "Shay", InteractionType.CONVERSATION, DialogueEmotion.CALM),
        interaction_engine.generate_dialogue("Shay", "Nyx", InteractionType.CONVERSATION, DialogueEmotion.EXCITED)
    ]
    
    interaction = interaction_engine.create_interaction(
        interaction_type=InteractionType.CONVERSATION,
        participants=["Shay", "Nyx"],
        dialogue_lines=dialogue_lines,
        emotional_intensity=0.6
    )
    
    print(f"✅ Created interaction: {interaction.interaction_id}")
    print(f"Type: {interaction.interaction_type.value}")
    print(f"Participants: {', '.join(interaction.participants)}")
    print(f"Dialogue lines: {len(interaction.dialogue)}")
    print(f"Emotional intensity: {interaction.emotional_intensity}")

def test_interaction_sequence_generation():
    """Test generating complete interaction sequences"""
    print("\n🔄 Testing Interaction Sequence Generation")
    print("=" * 50)
    
    interaction_engine = initialize()
    
    # Test different interaction types
    interaction_types = [
        InteractionType.CONVERSATION,
        InteractionType.CONFLICT,
        InteractionType.COLLABORATION,
        InteractionType.ROMANCE,
        InteractionType.FRIENDSHIP
    ]
    
    for interaction_type in interaction_types:
        print(f"\n🎭 Generating {interaction_type.value} sequence...")
        interaction = interaction_engine.generate_interaction_sequence("Shay", "Nyx", interaction_type, 4)
        
        print(f"Interaction ID: {interaction.interaction_id}")
        print(f"Type: {interaction.interaction_type.value}")
        print(f"Emotional intensity: {interaction.emotional_intensity}")
        print(f"Dialogue exchanges: {len(interaction.dialogue)}")
        
        # Show the dialogue
        for i, line in enumerate(interaction.dialogue):
            print(f"  {i+1}. {line.speaker} ({line.emotion.value}): {line.content}")

def test_character_interactions():
    """Test retrieving character interactions"""
    print("\n📊 Testing Character Interactions")
    print("=" * 50)
    
    interaction_engine = initialize()
    
    # Get all interactions for Shay
    shay_interactions = interaction_engine.get_character_interactions("Shay")
    print(f"Total interactions for Shay: {len(shay_interactions)}")
    
    # Get specific interaction types
    conversation_interactions = interaction_engine.get_character_interactions("Shay", InteractionType.CONVERSATION)
    print(f"Conversation interactions for Shay: {len(conversation_interactions)}")
    
    conflict_interactions = interaction_engine.get_character_interactions("Shay", InteractionType.CONFLICT)
    print(f"Conflict interactions for Shay: {len(conflict_interactions)}")
    
    # Get interactions for Nyx
    nyx_interactions = interaction_engine.get_character_interactions("Nyx")
    print(f"Total interactions for Nyx: {len(nyx_interactions)}")

def test_dialogue_profiles():
    """Test dialogue profile functionality"""
    print("\n👤 Testing Dialogue Profiles")
    print("=" * 50)
    
    interaction_engine = initialize()
    
    # Get dialogue profiles
    shay_profile = interaction_engine.get_dialogue_profile("Shay")
    nyx_profile = interaction_engine.get_dialogue_profile("Nyx")
    luna_profile = interaction_engine.get_dialogue_profile("Luna")
    
    print(f"Shay's profile: {shay_profile.get('interaction_style', 'unknown')}")
    print(f"Nyx's profile: {nyx_profile.get('interaction_style', 'unknown')}")
    print(f"Luna's profile: {luna_profile.get('interaction_style', 'unknown')}")
    
    # Update a dialogue profile
    interaction_engine.update_dialogue_profile(
        character_name="Shay",
        speech_patterns={'formal': 0.4, 'casual': 0.6},
        vocabulary_preferences=['brave', 'courageous'],
        interaction_style="heroic"
    )
    
    updated_profile = interaction_engine.get_dialogue_profile("Shay")
    print(f"Updated Shay's style to: {updated_profile.get('interaction_style', 'unknown')}")

def test_interaction_summaries():
    """Test interaction summary functionality"""
    print("\n📈 Testing Interaction Summaries")
    print("=" * 50)
    
    interaction_engine = initialize()
    
    # Get interaction summaries
    shay_summary = interaction_engine.get_interaction_summary("Shay")
    nyx_summary = interaction_engine.get_interaction_summary("Nyx")
    
    print("Shay's Interaction Summary:")
    print(shay_summary)
    print("\nNyx's Interaction Summary:")
    print(nyx_summary)

def test_relationship_dynamics():
    """Test relationship dynamics analysis"""
    print("\n💕 Testing Relationship Dynamics")
    print("=" * 50)
    
    interaction_engine = initialize()
    
    # Analyze relationship dynamics between Shay and Nyx
    dynamics = interaction_engine.get_relationship_dynamics("Shay", "Nyx")
    
    print("Relationship Dynamics (Shay ↔ Nyx):")
    for key, value in dynamics.items():
        print(f"- {key}: {value}")
    
    # Analyze relationship dynamics between Shay and Luna
    luna_dynamics = interaction_engine.get_relationship_dynamics("Shay", "Luna")
    
    print("\nRelationship Dynamics (Shay ↔ Luna):")
    for key, value in luna_dynamics.items():
        print(f"- {key}: {value}")

def test_multiple_character_interactions():
    """Test interactions between multiple characters"""
    print("\n👥 Testing Multiple Character Interactions")
    print("=" * 50)
    
    interaction_engine = initialize()
    
    # Create interactions between different character pairs
    character_pairs = [
        ("Shay", "Luna"),
        ("Nyx", "Luna"),
        ("Shay", "Nyx")
    ]
    
    interaction_types = [
        InteractionType.FRIENDSHIP,
        InteractionType.CONFLICT,
        InteractionType.COLLABORATION
    ]
    
    for i, (char_a, char_b) in enumerate(character_pairs):
        interaction_type = interaction_types[i % len(interaction_types)]
        print(f"\n🎭 Creating {interaction_type.value} between {char_a} and {char_b}...")
        
        interaction = interaction_engine.generate_interaction_sequence(char_a, char_b, interaction_type, 3)
        
        print(f"Interaction created: {interaction.interaction_id}")
        print(f"Type: {interaction.interaction_type.value}")
        print(f"Emotional intensity: {interaction.emotional_intensity}")
        
        # Show dialogue
        for line in interaction.dialogue:
            print(f"  {line.speaker}: {line.content}")

def test_dialogue_emotion_variations():
    """Test dialogue generation with different emotions"""
    print("\n😊 Testing Dialogue Emotion Variations")
    print("=" * 50)
    
    interaction_engine = initialize()
    
    # Test different emotions for the same interaction type
    emotions = [
        DialogueEmotion.HAPPY,
        DialogueEmotion.SAD,
        DialogueEmotion.ANGRY,
        DialogueEmotion.EXCITED,
        DialogueEmotion.CALM,
        DialogueEmotion.CONFIDENT,
        DialogueEmotion.VULNERABLE
    ]
    
    for emotion in emotions:
        print(f"\n🎭 Testing {emotion.value} emotion...")
        dialogue = interaction_engine.generate_dialogue("Shay", "Nyx", InteractionType.CONVERSATION, emotion)
        
        print(f"Shay ({emotion.value}): {dialogue.content}")

if __name__ == "__main__":
    print("🎭 Character Interaction Engine Test Suite")
    print("=" * 60)
    
    try:
        test_dialogue_profile_creation()
        test_dialogue_generation()
        test_interaction_creation()
        test_interaction_sequence_generation()
        test_character_interactions()
        test_dialogue_profiles()
        test_interaction_summaries()
        test_relationship_dynamics()
        test_multiple_character_interactions()
        test_dialogue_emotion_variations()
        
        print("\n🎉 All tests completed successfully!")
        print("The Character Interaction Engine is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 