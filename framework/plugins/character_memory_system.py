#!/usr/bin/env python3
"""
Character Memory System
Provides character-specific memory and knowledge, backstory integration, and relationship mapping
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime

from core.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Types of memories that can be stored"""

    PERSONAL_EXPERIENCE = "personal_experience"
    RELATIONSHIP_MEMORY = "relationship_memory"
    KNOWLEDGE_MEMORY = "knowledge_memory"
    EMOTIONAL_MEMORY = "emotional_memory"
    SKILL_MEMORY = "skill_memory"
    BACKSTORY_MEMORY = "backstory_memory"


class MemoryImportance(Enum):
    """Importance levels for memories"""

    CRITICAL = "critical"
    IMPORTANT = "important"
    MODERATE = "moderate"
    MINOR = "minor"
    TRIVIAL = "trivial"


@dataclass
class Memory:
    """Represents a single memory"""

    memory_id: str
    memory_type: MemoryType
    importance: MemoryImportance
    content: str
    character_name: str
    associated_characters: List[str]
    emotional_context: Dict[str, float]
    timestamp: str
    context: Dict[str, Any]


@dataclass
class CharacterMemory:
    """Memory profile for a specific character"""

    character_name: str
    memories: List[Memory]
    knowledge_base: Dict[str, Any]
    relationships: Dict[str, Dict[str, Any]]
    backstory: Dict[str, Any]
    skills: List[str]
    personality_traits: List[str]


@dataclass
class Relationship:
    """Represents a relationship between characters"""

    character_a: str
    character_b: str
    relationship_type: str
    strength: float  # 0.0 to 1.0
    trust_level: float  # 0.0 to 1.0
    emotional_bond: float  # 0.0 to 1.0
    shared_experiences: List[str]
    relationship_history: List[str]


class CharacterMemorySystem:
    """
    Character Memory System
    Provides character-specific memory and knowledge management
    """

    def __init__(self):
        self.config = Config()
        # Use the current file's location to determine project root
        project_root = Path(__file__).parent.parent.parent
        self.memory_data_dir = project_root / "models" / "memory"
        self.memory_data_dir.mkdir(parents=True, exist_ok=True)

        self.character_memories = {}
        self.relationships = {}
        self.memory_cache = {}

        # Load existing memory data
        self._load_memory_data()

    def _load_memory_data(self):
        """Load existing memory data from disk"""
        memory_file = self.memory_data_dir / "memory_data.json"
        if memory_file.exists():
            try:
                with open(memory_file, "r") as f:
                    data = json.load(f)
                    self.character_memories = data.get("character_memories", {})
                    self.relationships = data.get("relationships", {})
                    self.memory_cache = data.get("memory_cache", {})
                logger.info("Loaded existing memory data")
            except Exception as e:
                logger.error(f"Error loading memory data: {e}")

    def _save_memory_data(self):
        """Save current memory data to disk"""
        memory_file = self.memory_data_dir / "memory_data.json"
        try:
            # Convert enum values to strings for JSON serialization
            serializable_memories = {}
            for character, memory_data in self.character_memories.items():
                if isinstance(memory_data, dict):
                    serializable_memories[character] = memory_data
                else:
                    # Convert CharacterMemory to dict
                    memory_dict = asdict(memory_data)
                    # Convert memory list
                    serializable_memories_list = []
                    for memory in memory_data.memories:
                        memory_dict_item = asdict(memory)
                        memory_dict_item["memory_type"] = memory.memory_type.value
                        memory_dict_item["importance"] = memory.importance.value
                        serializable_memories_list.append(memory_dict_item)
                    memory_dict["memories"] = serializable_memories_list
                    serializable_memories[character] = memory_dict

            data = {
                "character_memories": serializable_memories,
                "relationships": self.relationships,
                "memory_cache": self.memory_cache,
            }
            with open(memory_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved memory data")
        except Exception as e:
            logger.error(f"Error saving memory data: {e}")

    def add_memory(
        self,
        character_name: str,
        memory_type: MemoryType,
        content: str,
        importance: MemoryImportance = MemoryImportance.MODERATE,
        associated_characters: List[str] = None,
        emotional_context: Dict[str, float] = None,
        context: Dict[str, Any] = None,
    ) -> Memory:
        """
        Add a memory for a character

        Args:
            character_name: Name of the character
            memory_type: Type of memory
            content: Memory content
            importance: Importance level of the memory
            associated_characters: Other characters involved
            emotional_context: Emotional context of the memory
            context: Additional context

        Returns:
            Memory object
        """
        memory_id = f"memory_{len(self._get_character_memories(character_name))}"

        memory = Memory(
            memory_id=memory_id,
            memory_type=memory_type,
            importance=importance,
            content=content,
            character_name=character_name,
            associated_characters=associated_characters or [],
            emotional_context=emotional_context or {},
            timestamp=datetime.now().isoformat(),
            context=context or {},
        )

        # Add to character's memory
        self._add_memory_to_character(character_name, memory)

        # Update relationships if other characters are involved
        if associated_characters:
            self._update_relationships_from_memory(character_name, memory)

        # Save memory data
        self._save_memory_data()

        logger.info(f"Added {memory_type.value} memory for {character_name}")
        return memory

    def _get_character_memories(self, character_name: str) -> List[Memory]:
        """Get all memories for a character"""
        if character_name not in self.character_memories:
            return []

        memory_data = self.character_memories[character_name]
        if isinstance(memory_data, dict):
            # Convert dict back to CharacterMemory object
            memories = []
            for memory_dict in memory_data.get("memories", []):
                memory = Memory(
                    memory_id=memory_dict["memory_id"],
                    memory_type=MemoryType(memory_dict["memory_type"]),
                    importance=MemoryImportance(memory_dict["importance"]),
                    content=memory_dict["content"],
                    character_name=memory_dict["character_name"],
                    associated_characters=memory_dict["associated_characters"],
                    emotional_context=memory_dict["emotional_context"],
                    timestamp=memory_dict["timestamp"],
                    context=memory_dict["context"],
                )
                memories.append(memory)
            return memories
        else:
            return memory_data.memories

    def _add_memory_to_character(self, character_name: str, memory: Memory):
        """Add memory to character's memory profile"""
        if character_name not in self.character_memories:
            self.character_memories[character_name] = {
                "character_name": character_name,
                "memories": [],
                "knowledge_base": {},
                "relationships": {},
                "backstory": {},
                "skills": [],
                "personality_traits": [],
            }

        character_data = self.character_memories[character_name]

        # Add memory to list
        memory_dict = asdict(memory)
        memory_dict["memory_type"] = memory.memory_type.value
        memory_dict["importance"] = memory.importance.value
        character_data["memories"].append(memory_dict)

        # Update knowledge base based on memory type
        self._update_knowledge_base(character_name, memory)

        # Update personality traits
        self._update_personality_traits(character_name, memory)

    def _update_knowledge_base(self, character_name: str, memory: Memory):
        """Update character's knowledge base based on memory"""
        character_data = self.character_memories[character_name]

        if memory.memory_type == MemoryType.KNOWLEDGE_MEMORY:
            # Extract knowledge from memory content
            knowledge_keywords = re.findall(
                r"\b(know|learn|understand|discover|find)\b",
                memory.content,
                re.IGNORECASE,
            )
            if knowledge_keywords:
                knowledge_topic = memory.content[:50] + "..."
                character_data["knowledge_base"][knowledge_topic] = {
                    "source": memory.memory_id,
                    "confidence": memory.importance.value,
                    "timestamp": memory.timestamp,
                }

        elif memory.memory_type == MemoryType.SKILL_MEMORY:
            # Extract skills from memory content
            skill_keywords = re.findall(
                r"\b(skill|ability|talent|capability|expertise)\b",
                memory.content,
                re.IGNORECASE,
            )
            if skill_keywords:
                skill_name = (
                    memory.content.split()[0]
                    if memory.content.split()
                    else "unknown_skill"
                )
                if skill_name not in character_data["skills"]:
                    character_data["skills"].append(skill_name)

    def _update_personality_traits(self, character_name: str, memory: Memory):
        """Update character's personality traits based on memory"""
        character_data = self.character_memories[character_name]

        # Extract personality traits from memory content
        trait_keywords = {
            "brave": r"\b(brave|courageous|bold|fearless)\b",
            "kind": r"\b(kind|gentle|compassionate|caring)\b",
            "intelligent": r"\b(intelligent|smart|clever|wise)\b",
            "loyal": r"\b(loyal|faithful|devoted|trustworthy)\b",
            "curious": r"\b(curious|inquisitive|interested|exploring)\b",
        }

        for trait, pattern in trait_keywords.items():
            if re.search(pattern, memory.content, re.IGNORECASE):
                if trait not in character_data["personality_traits"]:
                    character_data["personality_traits"].append(trait)

    def _update_relationships_from_memory(self, character_name: str, memory: Memory):
        """Update relationships based on memory"""
        for other_character in memory.associated_characters:
            relationship_key = f"{character_name}_{other_character}"
            reverse_key = f"{other_character}_{character_name}"

            # Use the alphabetical order for consistent keys
            if relationship_key > reverse_key:
                relationship_key = reverse_key

            if relationship_key not in self.relationships:
                self.relationships[relationship_key] = {
                    "character_a": min(character_name, other_character),
                    "character_b": max(character_name, other_character),
                    "relationship_type": "acquaintance",
                    "strength": 0.1,
                    "trust_level": 0.1,
                    "emotional_bond": 0.1,
                    "shared_experiences": [],
                    "relationship_history": [],
                }

            # Update relationship based on memory
            relationship = self.relationships[relationship_key]
            relationship["shared_experiences"].append(memory.memory_id)
            relationship["relationship_history"].append(
                f"{memory.timestamp}: {memory.content[:50]}..."
            )

            # Adjust relationship strength based on memory importance
            importance_multiplier = {
                MemoryImportance.CRITICAL: 0.3,
                MemoryImportance.IMPORTANT: 0.2,
                MemoryImportance.MODERATE: 0.1,
                MemoryImportance.MINOR: 0.05,
                MemoryImportance.TRIVIAL: 0.02,
            }

            relationship["strength"] = min(
                1.0, relationship["strength"] + importance_multiplier[memory.importance]
            )

    def get_character_memories(
        self, character_name: str, memory_type: MemoryType = None
    ) -> List[Memory]:
        """Get memories for a character, optionally filtered by type"""
        memories = self._get_character_memories(character_name)

        if memory_type:
            memories = [m for m in memories if m.memory_type == memory_type]

        return memories

    def get_character_knowledge(self, character_name: str) -> Dict[str, Any]:
        """Get character's knowledge base"""
        if character_name not in self.character_memories:
            return {}

        character_data = self.character_memories[character_name]
        return character_data.get("knowledge_base", {})

    def get_character_relationships(self, character_name: str) -> List[Dict[str, Any]]:
        """Get character's relationships"""
        relationships = []

        for relationship_key, relationship_data in self.relationships.items():
            if (
                relationship_data["character_a"] == character_name
                or relationship_data["character_b"] == character_name
            ):
                relationships.append(relationship_data)

        return relationships

    def get_character_skills(self, character_name: str) -> List[str]:
        """Get character's skills"""
        if character_name not in self.character_memories:
            return []

        character_data = self.character_memories[character_name]
        return character_data.get("skills", [])

    def get_character_personality_traits(self, character_name: str) -> List[str]:
        """Get character's personality traits"""
        if character_name not in self.character_memories:
            return []

        character_data = self.character_memories[character_name]
        return character_data.get("personality_traits", [])

    def add_backstory(
        self,
        character_name: str,
        backstory_content: str,
        backstory_type: str = "general",
    ) -> bool:
        """Add backstory information for a character"""
        if character_name not in self.character_memories:
            self.character_memories[character_name] = {
                "character_name": character_name,
                "memories": [],
                "knowledge_base": {},
                "relationships": {},
                "backstory": {},
                "skills": [],
                "personality_traits": [],
            }

        character_data = self.character_memories[character_name]
        character_data["backstory"][backstory_type] = {
            "content": backstory_content,
            "timestamp": datetime.now().isoformat(),
        }

        # Create a backstory memory
        self.add_memory(
            character_name=character_name,
            memory_type=MemoryType.BACKSTORY_MEMORY,
            content=backstory_content,
            importance=MemoryImportance.IMPORTANT,
            context={"backstory_type": backstory_type},
        )

        self._save_memory_data()
        logger.info(f"Added {backstory_type} backstory for {character_name}")
        return True

    def get_character_backstory(self, character_name: str) -> Dict[str, Any]:
        """Get character's backstory"""
        if character_name not in self.character_memories:
            return {}

        character_data = self.character_memories[character_name]
        return character_data.get("backstory", {})

    def search_memories(self, character_name: str, query: str) -> List[Memory]:
        """Search character's memories for specific content"""
        memories = self._get_character_memories(character_name)

        matching_memories = []
        query_lower = query.lower()

        for memory in memories:
            if (
                query_lower in memory.content.lower()
                or query_lower in memory.character_name.lower()
                or any(
                    query_lower in char.lower() for char in memory.associated_characters
                )
            ):
                matching_memories.append(memory)

        return matching_memories

    def get_memory_summary(self, character_name: str) -> str:
        """Get a summary of character's memories"""
        if character_name not in self.character_memories:
            return f"No memory data available for {character_name}"

        memories = self._get_character_memories(character_name)
        knowledge = self.get_character_knowledge(character_name)
        relationships = self.get_character_relationships(character_name)
        skills = self.get_character_skills(character_name)
        traits = self.get_character_personality_traits(character_name)

        summary_parts = []
        summary_parts.append(f"Memory Summary for {character_name}:")
        summary_parts.append(f"- Total memories: {len(memories)}")
        summary_parts.append(f"- Knowledge items: {len(knowledge)}")
        summary_parts.append(f"- Relationships: {len(relationships)}")
        summary_parts.append(f"- Skills: {len(skills)}")
        summary_parts.append(f"- Personality traits: {len(traits)}")

        if memories:
            # Group memories by type
            memory_types = {}
            for memory in memories:
                memory_type = memory.memory_type.value
                if memory_type not in memory_types:
                    memory_types[memory_type] = 0
                memory_types[memory_type] += 1

            summary_parts.append("- Memory breakdown:")
            for memory_type, count in memory_types.items():
                summary_parts.append(f"  * {memory_type}: {count}")

        if skills:
            summary_parts.append(f"- Skills: {', '.join(skills)}")

        if traits:
            summary_parts.append(f"- Personality traits: {', '.join(traits)}")

        return "\n".join(summary_parts)

    def get_relationship_summary(self, character_a: str, character_b: str) -> str:
        """Get a summary of the relationship between two characters"""
        relationship_key = (
            f"{min(character_a, character_b)}_{max(character_a, character_b)}"
        )

        if relationship_key not in self.relationships:
            return f"No relationship data between {character_a} and {character_b}"

        relationship = self.relationships[relationship_key]

        summary_parts = []
        summary_parts.append(f"Relationship Summary: {character_a} ↔ {character_b}")
        summary_parts.append(
            f"- Relationship type: {relationship['relationship_type']}"
        )
        summary_parts.append(f"- Strength: {relationship['strength']:.2f}")
        summary_parts.append(f"- Trust level: {relationship['trust_level']:.2f}")
        summary_parts.append(f"- Emotional bond: {relationship['emotional_bond']:.2f}")
        summary_parts.append(
            f"- Shared experiences: {len(relationship['shared_experiences'])}"
        )

        if relationship["relationship_history"]:
            summary_parts.append("- Recent interactions:")
            for interaction in relationship["relationship_history"][
                -3:
            ]:  # Last 3 interactions
                summary_parts.append(f"  * {interaction}")

        return "\n".join(summary_parts)

    def reset_character_memories(self, character_name: str):
        """Reset all memories for a character"""
        if character_name in self.character_memories:
            del self.character_memories[character_name]

        # Remove relationships involving this character
        keys_to_remove = []
        for key in self.relationships:
            if (
                self.relationships[key]["character_a"] == character_name
                or self.relationships[key]["character_b"] == character_name
            ):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.relationships[key]

        self._save_memory_data()
        logger.info(f"Reset all memories for {character_name}")

    def reset_all_memories(self):
        """Reset all memory data"""
        self.character_memories = {}
        self.relationships = {}
        self.memory_cache = {}
        self._save_memory_data()
        logger.info("Reset all memory data")


def initialize(framework=None):
    """Initialize the Character Memory System"""
    return CharacterMemorySystem()
