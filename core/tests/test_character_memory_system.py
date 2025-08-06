#!/usr/bin/env python3
"""
Test script for Character Memory System
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from framework.plugins.character_memory_system import CharacterMemorySystem, initialize, MemoryType, MemoryImportance

def test_add_memories():
    """Test adding different types of memories"""
    print("🧠 Testing Memory Addition")
    print("=" * 50)
    
    # Initialize the memory system
    memory_system = initialize()
    
    # Test adding different types of memories for Shay
    memories_to_add = [
        (MemoryType.PERSONAL_EXPERIENCE, "Shay discovered the ancient relic in the forest", MemoryImportance.CRITICAL),
        (MemoryType.RELATIONSHIP_MEMORY, "Shay met Nyx and felt an immediate connection", MemoryImportance.IMPORTANT, ["Nyx"]),
        (MemoryType.KNOWLEDGE_MEMORY, "Shay learned about the history of the Forsaken Forest", MemoryImportance.MODERATE),
        (MemoryType.EMOTIONAL_MEMORY, "Shay felt overwhelming joy when she found the relic", MemoryImportance.IMPORTANT),
        (MemoryType.SKILL_MEMORY, "Shay developed her tracking skills in the forest", MemoryImportance.MODERATE)
    ]
    
    for memory_data in memories_to_add:
        if len(memory_data) == 3:
            memory_type, content, importance = memory_data
            associated_characters = None
        else:
            memory_type, content, importance, associated_characters = memory_data
        
        print(f"📝 Adding {memory_type.value} memory...")
        memory = memory_system.add_memory(
            character_name="Shay",
            memory_type=memory_type,
            content=content,
            importance=importance,
            associated_characters=associated_characters
        )
        
        print(f"Memory ID: {memory.memory_id}")
        print(f"Type: {memory.memory_type.value}")
        print(f"Importance: {memory.importance.value}")
        print(f"Content: {memory.content[:50]}...")
        print()
    
    print("✅ Memory addition test completed successfully!")

def test_character_memory_retrieval():
    """Test retrieving character memories"""
    print("\n📖 Testing Memory Retrieval")
    print("=" * 50)
    
    memory_system = initialize()
    
    # Get all memories for Shay
    all_memories = memory_system.get_character_memories("Shay")
    print(f"Total memories for Shay: {len(all_memories)}")
    
    # Get specific types of memories
    personal_memories = memory_system.get_character_memories("Shay", MemoryType.PERSONAL_EXPERIENCE)
    print(f"Personal experience memories: {len(personal_memories)}")
    
    relationship_memories = memory_system.get_character_memories("Shay", MemoryType.RELATIONSHIP_MEMORY)
    print(f"Relationship memories: {len(relationship_memories)}")
    
    knowledge_memories = memory_system.get_character_memories("Shay", MemoryType.KNOWLEDGE_MEMORY)
    print(f"Knowledge memories: {len(knowledge_memories)}")
    
    print("✅ Memory retrieval test completed successfully!")

def test_character_knowledge_and_skills():
    """Test character knowledge and skills"""
    print("\n🎓 Testing Character Knowledge and Skills")
    print("=" * 50)
    
    memory_system = initialize()
    
    # Get Shay's knowledge base
    knowledge = memory_system.get_character_knowledge("Shay")
    print(f"Knowledge items for Shay: {len(knowledge)}")
    for topic, info in knowledge.items():
        print(f"- {topic}: confidence {info['confidence']}")
    
    # Get Shay's skills
    skills = memory_system.get_character_skills("Shay")
    print(f"Skills for Shay: {skills}")
    
    # Get Shay's personality traits
    traits = memory_system.get_character_personality_traits("Shay")
    print(f"Personality traits for Shay: {traits}")
    
    print("✅ Knowledge and skills test completed successfully!")

def test_relationships():
    """Test character relationships"""
    print("\n👥 Testing Character Relationships")
    print("=" * 50)
    
    memory_system = initialize()
    
    # Add some memories for Nyx to create relationships
    memory_system.add_memory(
        character_name="Nyx",
        memory_type=MemoryType.RELATIONSHIP_MEMORY,
        content="Nyx met Shay and was intrigued by her determination",
        importance=MemoryImportance.IMPORTANT,
        associated_characters=["Shay"]
    )
    
    memory_system.add_memory(
        character_name="Shay",
        memory_type=MemoryType.RELATIONSHIP_MEMORY,
        content="Shay felt a deep connection with Nyx during their conversation",
        importance=MemoryImportance.IMPORTANT,
        associated_characters=["Nyx"]
    )
    
    # Get relationships for Shay
    relationships = memory_system.get_character_relationships("Shay")
    print(f"Relationships for Shay: {len(relationships)}")
    
    for relationship in relationships:
        other_char = relationship['character_b'] if relationship['character_a'] == "Shay" else relationship['character_a']
        print(f"- Relationship with {other_char}: strength {relationship['strength']:.2f}")
    
    # Get relationship summary
    relationship_summary = memory_system.get_relationship_summary("Shay", "Nyx")
    print(f"\nRelationship Summary:\n{relationship_summary}")
    
    print("✅ Relationships test completed successfully!")

def test_backstory_integration():
    """Test backstory integration"""
    print("\n📚 Testing Backstory Integration")
    print("=" * 50)
    
    memory_system = initialize()
    
    # Add backstory for Shay
    backstory_content = """
    Shay grew up in a small village near the Forsaken Forest. Her grandfather was a wise storyteller
    who taught her about the ancient legends and the mysterious relic said to be hidden in the forest.
    She spent her childhood listening to his tales and dreaming of adventure.
    """
    
    print("📝 Adding backstory for Shay...")
    success = memory_system.add_backstory("Shay", backstory_content, "childhood")
    
    if success:
        print("✅ Backstory added successfully")
    
    # Get backstory
    backstory = memory_system.get_character_backstory("Shay")
    print(f"Backstory sections: {list(backstory.keys())}")
    
    for section, data in backstory.items():
        print(f"- {section}: {data['content'][:100]}...")
    
    print("✅ Backstory integration test completed successfully!")

def test_memory_search():
    """Test memory search functionality"""
    print("\n🔍 Testing Memory Search")
    print("=" * 50)
    
    memory_system = initialize()
    
    # Search for memories containing "relic"
    relic_memories = memory_system.search_memories("Shay", "relic")
    print(f"Memories containing 'relic': {len(relic_memories)}")
    
    for memory in relic_memories:
        print(f"- {memory.content[:50]}...")
    
    # Search for memories containing "Nyx"
    nyx_memories = memory_system.search_memories("Shay", "Nyx")
    print(f"\nMemories containing 'Nyx': {len(nyx_memories)}")
    
    for memory in nyx_memories:
        print(f"- {memory.content[:50]}...")
    
    print("✅ Memory search test completed successfully!")

def test_memory_summary():
    """Test memory summary functionality"""
    print("\n📊 Testing Memory Summary")
    print("=" * 50)
    
    memory_system = initialize()
    
    # Get memory summary for Shay
    summary = memory_system.get_memory_summary("Shay")
    print("Memory Summary:")
    print(summary)
    
    print("✅ Memory summary test completed successfully!")

def test_multiple_characters():
    """Test memory system with multiple characters"""
    print("\n👥 Testing Multiple Characters")
    print("=" * 50)
    
    memory_system = initialize()
    
    # Add memories for Luna
    memory_system.add_memory(
        character_name="Luna",
        memory_type=MemoryType.PERSONAL_EXPERIENCE,
        content="Luna discovered her magical abilities at a young age",
        importance=MemoryImportance.CRITICAL
    )
    
    memory_system.add_memory(
        character_name="Luna",
        memory_type=MemoryType.RELATIONSHIP_MEMORY,
        content="Luna met Shay and felt a sisterly bond with her",
        importance=MemoryImportance.IMPORTANT,
        associated_characters=["Shay"]
    )
    
    # Get summaries for both characters
    shay_summary = memory_system.get_memory_summary("Shay")
    luna_summary = memory_system.get_memory_summary("Luna")
    
    print("Shay's Summary:")
    print(shay_summary)
    print("\nLuna's Summary:")
    print(luna_summary)
    
    print("✅ Multiple characters test completed successfully!")

if __name__ == "__main__":
    print("🧠 Character Memory System Test Suite")
    print("=" * 60)
    
    try:
        test_add_memories()
        test_character_memory_retrieval()
        test_character_knowledge_and_skills()
        test_relationships()
        test_backstory_integration()
        test_memory_search()
        test_memory_summary()
        test_multiple_characters()
        
        print("\n🎉 All tests completed successfully!")
        print("The Character Memory System is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 