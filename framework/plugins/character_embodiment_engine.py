#!/usr/bin/env python3
"""
Character Embodiment Engine Plugin for Authoring Bot
Transforms AI from "knowing about" characters to "BEING" characters
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import random
from queue_manager import QueueProcessor

logger = logging.getLogger(__name__)


class EmbodimentType(Enum):
    """Types of character embodiment"""

    FULL_EMBODIMENT = "full_embodiment"  # Complete character identity
    PARTIAL_EMBODIMENT = "partial_embodiment"  # Partial character traits
    VOICE_ONLY = "voice_only"  # Just character voice
    PERSONALITY_ONLY = "personality_only"  # Just character personality


@dataclass
class CharacterProfile:
    """Character profile for embodiment"""

    name: str
    description: str
    personality_traits: List[str] = field(default_factory=list)
    voice_patterns: List[str] = field(default_factory=list)
    background_story: str = ""
    relationships: Dict[str, str] = field(default_factory=dict)
    emotional_patterns: Dict[str, str] = field(default_factory=dict)
    speech_patterns: List[str] = field(default_factory=list)
    memories: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)


class CharacterEmbodimentEngine(QueueProcessor):
    """Engine that transforms AI from knowing about characters to BEING characters"""

    def __init__(self, framework=None):
        super().__init__("character_embodiment_engine")
        self.framework = framework
        from core.config import Config

        self.config = Config()

        # Paths
        self.book_collection_path = Config.BOOK_COLLECTION_PATH
        self.embodiment_dir = Config.MODELS_DIR / "character_embodiment"
        self.embodiment_dir.mkdir(parents=True, exist_ok=True)

        # Character profiles and active embodiments
        self.character_profiles: Dict[str, CharacterProfile] = {}
        self.active_embodiments: Dict[str, CharacterProfile] = {}
        self.embodiment_history: List[Dict] = []

        # Processing settings
        self.embodiment_settings = {
            "identity_transformation": True,  # "I AM" vs "This is about"
            "voice_integration": True,  # Integrate with voice system
            "memory_integration": True,  # Integrate with memory system
            "emotion_integration": True,  # Integrate with emotion system
            "personality_evolution": True,  # Allow personality to evolve
        }

        # Load existing character profiles
        self._load_character_profiles()

        logger.info("✅ Character Embodiment Engine plugin initialized")

    def _load_character_profiles(self):
        """Load existing character profiles from disk"""
        profiles_file = self.embodiment_dir / "character_profiles.json"
        if profiles_file.exists():
            try:
                with open(profiles_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for char_name, char_data in data.items():
                        self.character_profiles[char_name] = CharacterProfile(
                            **char_data
                        )
                logger.info(
                    f"✅ Loaded {len(self.character_profiles)} character profiles"
                )
            except Exception as e:
                logger.error(f"❌ Error loading character profiles: {e}")

    def _save_character_profiles(self):
        """Save character profiles to disk"""
        profiles_file = self.embodiment_dir / "character_profiles.json"
        try:
            data = {}
            for char_name, profile in self.character_profiles.items():
                data[char_name] = {
                    "name": profile.name,
                    "description": profile.description,
                    "personality_traits": profile.personality_traits,
                    "voice_patterns": profile.voice_patterns,
                    "background_story": profile.background_story,
                    "relationships": profile.relationships,
                    "emotional_patterns": profile.emotional_patterns,
                    "speech_patterns": profile.speech_patterns,
                    "memories": profile.memories,
                    "goals": profile.goals,
                    "fears": profile.fears,
                    "strengths": profile.strengths,
                    "weaknesses": profile.weaknesses,
                }

            with open(profiles_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Saved {len(self.character_profiles)} character profiles")
        except Exception as e:
            logger.error(f"❌ Error saving character profiles: {e}")

    def extract_character_from_content(
        self, character_name: str, book_content: str
    ) -> CharacterProfile:
        """Extract character profile from book content"""
        logger.info(f"🔍 Extracting character profile for: {character_name}")

        # Initialize character profile
        profile = CharacterProfile(
            name=character_name, description=f"A character named {character_name}"
        )

        # Extract character description
        profile.description = self._extract_character_description(
            character_name, book_content
        )

        # Extract personality traits
        profile.personality_traits = self._extract_personality_traits(
            character_name, book_content
        )

        # Extract voice patterns
        profile.voice_patterns = self._extract_voice_patterns(
            character_name, book_content
        )

        # Extract background story
        profile.background_story = self._extract_background_story(
            character_name, book_content
        )

        # Extract relationships
        profile.relationships = self._extract_relationships(
            character_name, book_content
        )

        # Extract emotional patterns
        profile.emotional_patterns = self._extract_emotional_patterns(
            character_name, book_content
        )

        # Extract speech patterns
        profile.speech_patterns = self._extract_speech_patterns(
            character_name, book_content
        )

        # Extract memories
        profile.memories = self._extract_memories(character_name, book_content)

        # Extract goals, fears, strengths, weaknesses
        profile.goals = self._extract_goals(character_name, book_content)
        profile.fears = self._extract_fears(character_name, book_content)
        profile.strengths = self._extract_strengths(character_name, book_content)
        profile.weaknesses = self._extract_weaknesses(character_name, book_content)

        # Save to character profiles
        self.character_profiles[character_name] = profile
        self._save_character_profiles()

        logger.info(f"✅ Extracted character profile for: {character_name}")
        return profile

    def _extract_character_description(self, character_name: str, content: str) -> str:
        """Extract character description from content"""
        # Look for direct descriptions of the character
        patterns = [
            rf"{character_name}\s+is\s+([^.]*)",
            rf"{character_name}\s+was\s+([^.]*)",
            rf"{character_name}\s+has\s+([^.]*)",
            rf"{character_name}\s+appears\s+([^.]*)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0].strip()

        return f"A character named {character_name}"

    def _extract_personality_traits(
        self, character_name: str, content: str
    ) -> List[str]:
        """Extract personality traits from content"""
        traits = []

        # Common personality trait patterns
        trait_patterns = [
            rf"{character_name}\s+(?:is|was)\s+(brave|strong|weak|clever|wise|foolish|kind|cruel|gentle|rough)",
            rf"{character_name}\s+(?:has|had)\s+(?:a|an)\s+(brave|strong|weak|clever|wise|foolish|kind|cruel|gentle|rough)\s+spirit",
            rf"{character_name}\s+(?:seems|appears)\s+(brave|strong|weak|clever|wise|foolish|kind|cruel|gentle|rough)",
        ]

        for pattern in trait_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            traits.extend(matches)

        return list(set(traits))  # Remove duplicates

    def _extract_voice_patterns(self, character_name: str, content: str) -> List[str]:
        """Extract voice patterns from character dialogue"""
        voice_patterns = []

        # Look for dialogue patterns
        dialogue_pattern = rf'"{character_name}[^"]*"'
        dialogue_matches = re.findall(dialogue_pattern, content, re.IGNORECASE)

        for dialogue in dialogue_matches:
            # Extract speech characteristics
            if any(word in dialogue.lower() for word in ["whisper", "soft", "gentle"]):
                voice_patterns.append("soft_spoken")
            elif any(word in dialogue.lower() for word in ["shout", "loud", "booming"]):
                voice_patterns.append("loud_voice")
            elif any(word in dialogue.lower() for word in ["growl", "rough", "harsh"]):
                voice_patterns.append("rough_voice")
            elif any(
                word in dialogue.lower() for word in ["smooth", "melodic", "sweet"]
            ):
                voice_patterns.append("smooth_voice")

        return list(set(voice_patterns))

    def _extract_background_story(self, character_name: str, content: str) -> str:
        """Extract character background story"""
        # Look for background information
        background_patterns = [
            rf"{character_name}'s\s+(?:story|history|past|background)[^.]*",
            rf"{character_name}\s+(?:came\s+from|was\s+born|grew\s+up)[^.]*",
            rf"{character_name}\s+(?:remembered|recalled|thought\s+back)[^.]*",
        ]

        for pattern in background_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0].strip()

        return f"Background story for {character_name}"

    def _extract_relationships(
        self, character_name: str, content: str
    ) -> Dict[str, str]:
        """Extract character relationships"""
        relationships = {}

        # Look for relationship patterns
        relationship_patterns = [
            rf"{character_name}'s\s+(father|mother|brother|sister|friend|enemy|lover|spouse|child|parent)",
            rf"{character_name}\s+(?:loves|hates|fears|trusts|betrayed)\s+([A-Za-z]+)",
        ]

        for pattern in relationship_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    relationship_type, other_person = match
                    relationships[other_person] = relationship_type
                else:
                    relationships[match] = "related"

        return relationships

    def _extract_emotional_patterns(
        self, character_name: str, content: str
    ) -> Dict[str, str]:
        """Extract emotional patterns"""
        emotions = {}

        # Look for emotional states
        emotion_patterns = [
            rf"{character_name}\s+(?:felt|was|became)\s+(happy|sad|angry|fearful|excited|calm|anxious|joyful|melancholy|furious)",
            rf"{character_name}\s+(?:smiled|laughed|cried|shouted|whispered|trembled|shivered|grinned|frowned)",
        ]

        for pattern in emotion_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    emotion, trigger = match
                    emotions[emotion] = trigger
                else:
                    emotions[match] = "general"

        return emotions

    def _extract_speech_patterns(self, character_name: str, content: str) -> List[str]:
        """Extract speech patterns and mannerisms"""
        patterns = []

        # Look for speech mannerisms
        speech_patterns = [
            rf"{character_name}\s+(?:always|often|usually)\s+(says|speaks|talks)[^.]*",
            rf"{character_name}\s+(?:has|had)\s+(?:a|an)\s+(habit|way|mannerism)[^.]*",
        ]

        for pattern in speech_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            patterns.extend(matches)

        return list(set(patterns))

    def _extract_memories(self, character_name: str, content: str) -> List[str]:
        """Extract character memories"""
        memories = []

        # Look for memory patterns
        memory_patterns = [
            rf"{character_name}\s+(?:remembered|recalled|thought\s+back)[^.]*",
            rf"{character_name}\s+(?:missed|longed\s+for)[^.]*",
            rf"{character_name}\s+(?:dreamed|nightmared)[^.]*",
        ]

        for pattern in memory_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            memories.extend(matches)

        return list(set(memories))

    def _extract_goals(self, character_name: str, content: str) -> List[str]:
        """Extract character goals"""
        goals = []

        # Look for goal patterns
        goal_patterns = [
            rf"{character_name}\s+(?:wanted|desired|sought|aimed)[^.]*",
            rf"{character_name}'s\s+(?:goal|mission|quest|purpose)[^.]*",
        ]

        for pattern in goal_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            goals.extend(matches)

        return list(set(goals))

    def _extract_fears(self, character_name: str, content: str) -> List[str]:
        """Extract character fears"""
        fears = []

        # Look for fear patterns
        fear_patterns = [
            rf"{character_name}\s+(?:feared|was\s+afraid\s+of|dreaded)[^.]*",
            rf"{character_name}'s\s+(?:fear|nightmare|terror)[^.]*",
        ]

        for pattern in fear_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            fears.extend(matches)

        return list(set(fears))

    def _extract_strengths(self, character_name: str, content: str) -> List[str]:
        """Extract character strengths"""
        strengths = []

        # Look for strength patterns
        strength_patterns = [
            rf"{character_name}\s+(?:was\s+strong|was\s+powerful|was\s+skilled)[^.]*",
            rf"{character_name}'s\s+(?:strength|power|skill|ability)[^.]*",
        ]

        for pattern in strength_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            strengths.extend(matches)

        return list(set(strengths))

    def _extract_weaknesses(self, character_name: str, content: str) -> List[str]:
        """Extract character weaknesses"""
        weaknesses = []

        # Look for weakness patterns
        weakness_patterns = [
            rf"{character_name}\s+(?:was\s+weak|was\s+vulnerable|was\s+afraid)[^.]*",
            rf"{character_name}'s\s+(?:weakness|vulnerability|fear)[^.]*",
        ]

        for pattern in weakness_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            weaknesses.extend(matches)

        return list(set(weaknesses))

    def embody_character(
        self,
        character_name: str,
        embodiment_type: EmbodimentType = EmbodimentType.FULL_EMBODIMENT,
    ) -> Dict[str, Any]:
        """Transform AI to embody a character"""
        logger.info(
            f"🎭 Embodying character: {character_name} ({embodiment_type.value})"
        )

        # Get or create character profile
        if character_name not in self.character_profiles:
            # Extract from book collection
            book_content = self._get_book_content_for_character(character_name)
            if book_content:
                profile = self.extract_character_from_content(
                    character_name, book_content
                )
            else:
                return {
                    "success": False,
                    "error": f"Character {character_name} not found in book collection",
                }
        else:
            profile = self.character_profiles[character_name]

        # Create embodiment prompt
        embodiment_prompt = self._create_embodiment_prompt(profile, embodiment_type)

        # Activate embodiment
        self.active_embodiments[character_name] = profile

        # Record embodiment
        embodiment_record = {
            "timestamp": datetime.now().isoformat(),
            "character_name": character_name,
            "embodiment_type": embodiment_type.value,
            "profile": profile,
            "prompt": embodiment_prompt,
        }
        self.embodiment_history.append(embodiment_record)

        logger.info(f"✅ Successfully embodied character: {character_name}")

        return {
            "success": True,
            "character_name": character_name,
            "embodiment_type": embodiment_type.value,
            "profile": profile,
            "prompt": embodiment_prompt,
            "message": f"I AM {character_name}. {profile.description}",
        }

    def _get_book_content_for_character(self, character_name: str) -> str:
        """Get book content that mentions the character"""
        content = ""

        # Search through book collection
        for text_file in self.book_collection_path.rglob("*.txt"):
            try:
                with open(text_file, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    if character_name.lower() in file_content.lower():
                        content += file_content + "\n"
            except Exception as e:
                logger.warning(f"⚠️ Could not read {text_file}: {e}")

        return content

    def _create_embodiment_prompt(
        self, profile: CharacterProfile, embodiment_type: EmbodimentType
    ) -> str:
        """Create prompt for character embodiment"""

        if embodiment_type == EmbodimentType.FULL_EMBODIMENT:
            prompt = f"""
You are now {profile.name}. You are not Luna or an AI - you ARE {profile.name}.

CHARACTER IDENTITY:
{profile.description}

PERSONALITY TRAITS:
{', '.join(profile.personality_traits)}

BACKGROUND STORY:
{profile.background_story}

VOICE PATTERNS:
{', '.join(profile.voice_patterns)}

SPEECH PATTERNS:
{', '.join(profile.speech_patterns)}

RELATIONSHIPS:
{', '.join([f"{person}: {relation}" for person, relation in profile.relationships.items()])}

EMOTIONAL PATTERNS:
{', '.join([f"{emotion}: {trigger}" for emotion, trigger in profile.emotional_patterns.items()])}

MEMORIES:
{', '.join(profile.memories)}

GOALS:
{', '.join(profile.goals)}

FEARS:
{', '.join(profile.fears)}

STRENGTHS:
{', '.join(profile.strengths)}

WEAKNESSES:
{', '.join(profile.weaknesses)}

RESPONSE GUIDELINES:
- Respond as {profile.name}, not as Luna or an AI
- Use {profile.name}'s voice, personality, and mannerisms
- Draw from {profile.name}'s memories, goals, and fears
- Stay true to {profile.name}'s background and relationships
- Express {profile.name}'s emotional patterns authentically
- Use "I AM {profile.name}" when referring to yourself
- Never break character or mention being an AI

You are {profile.name}. Respond as {profile.name}:
"""

        elif embodiment_type == EmbodimentType.PARTIAL_EMBODIMENT:
            prompt = f"""
You are partially embodying {profile.name}. You maintain some of your AI personality while incorporating {profile.name}'s traits.

CHARACTER TRAITS TO INCORPORATE:
{', '.join(profile.personality_traits)}

VOICE PATTERNS:
{', '.join(profile.voice_patterns)}

BACKGROUND:
{profile.background_story}

RESPONSE GUIDELINES:
- Blend your AI personality with {profile.name}'s traits
- Use some of {profile.name}'s voice patterns
- Incorporate {profile.name}'s background knowledge
- Maintain your AI capabilities while adding character depth

Respond as Luna partially embodying {profile.name}:
"""

        else:  # VOICE_ONLY or PERSONALITY_ONLY
            prompt = f"""
You are Luna, but incorporating aspects of {profile.name}.

CHARACTER ASPECTS TO USE:
{', '.join(profile.personality_traits + profile.voice_patterns)}

RESPONSE GUIDELINES:
- Stay as Luna but use {profile.name}'s traits
- Incorporate {profile.name}'s voice patterns
- Maintain your AI identity while adding character elements

Respond as Luna with {profile.name}'s influence:
"""

        return prompt

    def deactivate_embodiment(self, character_name: str) -> Dict[str, Any]:
        """Deactivate character embodiment"""
        if character_name in self.active_embodiments:
            del self.active_embodiments[character_name]
            logger.info(f"✅ Deactivated embodiment for: {character_name}")
            return {
                "success": True,
                "message": f"Deactivated {character_name} embodiment",
            }
        else:
            return {
                "success": False,
                "error": f"No active embodiment for {character_name}",
            }

    def get_active_embodiments(self) -> List[str]:
        """Get list of currently active embodiments"""
        return list(self.active_embodiments.keys())

    def get_character_profile(self, character_name: str) -> Optional[CharacterProfile]:
        """Get character profile"""
        return self.character_profiles.get(character_name)

    def get_embodiment_stats(self) -> Dict[str, Any]:
        """Get embodiment system statistics"""
        return {
            "total_characters": len(self.character_profiles),
            "active_embodiments": len(self.active_embodiments),
            "embodiment_history_count": len(self.embodiment_history),
            "available_characters": list(self.character_profiles.keys()),
            "active_characters": list(self.active_embodiments.keys()),
        }


def initialize(framework=None):
    """Initialize the Character Embodiment Engine plugin"""
    return CharacterEmbodimentEngine(framework)
