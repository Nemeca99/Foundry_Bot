#!/usr/bin/env python3
"""
Identity Processor Plugin for Character Embodiment System
Transforms content processing from "This is about" to "I AM" identity
"""

import json
import logging
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import random

# Add framework to path
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

from queue_manager import QueueProcessor

logger = logging.getLogger(__name__)


class IdentityTransformationType(Enum):
    """Types of identity transformation"""

    FULL_IDENTITY = "full_identity"  # Complete "I AM" transformation
    PARTIAL_IDENTITY = "partial_identity"  # Partial identity incorporation
    VOICE_IDENTITY = "voice_identity"  # Just voice transformation
    PERSONALITY_IDENTITY = "personality_identity"  # Just personality transformation


@dataclass
class IdentityProfile:
    """Identity profile for transformation"""

    name: str
    core_identity: str
    identity_traits: List[str] = field(default_factory=list)
    voice_identity: List[str] = field(default_factory=list)
    background_identity: str = ""
    relationship_identity: Dict[str, str] = field(default_factory=dict)
    emotional_identity: Dict[str, str] = field(default_factory=dict)
    speech_identity: List[str] = field(default_factory=list)
    memory_identity: List[str] = field(default_factory=list)
    goal_identity: List[str] = field(default_factory=list)
    fear_identity: List[str] = field(default_factory=list)
    strength_identity: List[str] = field(default_factory=list)
    weakness_identity: List[str] = field(default_factory=list)
    identity_phrases: List[str] = field(default_factory=list)


class IdentityProcessor(QueueProcessor):
    """Processor that transforms content from 'knowing about' to 'I AM' identity"""

    def __init__(self, framework=None):
        super().__init__("identity_processor")
        self.framework = framework
        from core.config import Config

        self.config = Config()

        # Paths
        self.identity_dir = Config.MODELS_DIR / "identity_processing"
        self.identity_dir.mkdir(parents=True, exist_ok=True)

        # Identity profiles and active transformations
        self.identity_profiles: Dict[str, IdentityProfile] = {}
        self.active_identities: Dict[str, IdentityProfile] = {}
        self.identity_history: List[Dict] = []

        # Processing settings
        self.identity_settings = {
            "transform_to_identity": True,  # "I AM" vs "This is about"
            "voice_integration": True,  # Integrate with voice system
            "memory_integration": True,  # Integrate with memory system
            "emotion_integration": True,  # Integrate with emotion system
            "personality_evolution": True,  # Allow personality to evolve
        }

        # Identity transformation patterns
        self.identity_patterns = {
            "description_to_identity": [
                (r"(\w+)\s+is\s+([^.]*)", r"I AM \1, \2"),
                (r"(\w+)\s+was\s+([^.]*)", r"I AM \1, \2"),
                (r"(\w+)\s+has\s+([^.]*)", r"I AM \1 with \2"),
                (r"(\w+)\s+appears\s+([^.]*)", r"I AM \1, appearing \2"),
            ],
            "trait_to_identity": [
                (
                    r"(\w+)\s+(?:is|was)\s+(brave|strong|weak|clever|wise|foolish|kind|cruel|gentle|rough)",
                    r"I AM \1, I AM \2",
                ),
                (
                    r"(\w+)\s+(?:has|had)\s+(?:a|an)\s+(brave|strong|weak|clever|wise|foolish|kind|cruel|gentle|rough)\s+spirit",
                    r"I AM \1, I AM \2",
                ),
            ],
            "action_to_identity": [
                (r"(\w+)\s+(felt|was|became)\s+([^.]*)", r"I AM \1, I \2 \3"),
                (
                    r"(\w+)\s+(smiled|laughed|cried|shouted|whispered|trembled|shivered|grinned|frowned)",
                    r"I AM \1, I \2",
                ),
            ],
            "memory_to_identity": [
                (
                    r"(\w+)\s+(remembered|recalled|thought\s+back)\s+([^.]*)",
                    r"I AM \1, I \2 \3",
                ),
                (r"(\w+)\s+(missed|longed\s+for)\s+([^.]*)", r"I AM \1, I \2 \3"),
            ],
            "goal_to_identity": [
                (
                    r"(\w+)\s+(wanted|desired|sought|aimed)\s+([^.]*)",
                    r"I AM \1, I \2 \3",
                ),
                (
                    r"(\w+)'s\s+(goal|mission|quest|purpose)\s+([^.]*)",
                    r"I AM \1, my \2 is \3",
                ),
            ],
        }

        # Load existing identity profiles
        self._load_identity_profiles()

    def _process_item(self, item):
        """Process queue items for identity processing operations"""
        try:
            # Extract operation type from data
            operation_type = item.data.get("type", "unknown")
            
            if operation_type == "transform_content":
                return self._handle_transform_content(item.data)
            elif operation_type == "extract_identity":
                return self._handle_extract_identity(item.data)
            elif operation_type == "process_content_as_identity":
                return self._handle_process_content_as_identity(item.data)
            elif operation_type == "deactivate_identity":
                return self._handle_deactivate_identity(item.data)
            elif operation_type == "get_active_identities":
                return self._handle_get_active_identities(item.data)
            elif operation_type == "get_identity_profile":
                return self._handle_get_identity_profile(item.data)
            elif operation_type == "get_identity_stats":
                return self._handle_get_identity_stats(item.data)
            else:
                # Pass unknown types to base class
                return super()._process_item(item)
        except Exception as e:
            logger.error(f"Error processing identity processor queue item: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_transform_content(self, data):
        """Handle content transformation requests"""
        try:
            character_name = data.get("character_name", "")
            content = data.get("content", "")
            transformation_type = data.get("transformation_type", "full_identity")
            
            if character_name and content:
                if transformation_type == "full_identity":
                    transform_enum = IdentityTransformationType.FULL_IDENTITY
                elif transformation_type == "partial_identity":
                    transform_enum = IdentityTransformationType.PARTIAL_IDENTITY
                elif transformation_type == "voice_identity":
                    transform_enum = IdentityTransformationType.VOICE_IDENTITY
                elif transformation_type == "personality_identity":
                    transform_enum = IdentityTransformationType.PERSONALITY_IDENTITY
                else:
                    transform_enum = IdentityTransformationType.FULL_IDENTITY
                
                transformed_content = self.transform_content_to_identity(character_name, content, transform_enum)
                return {
                    "status": "success",
                    "transformed_content": transformed_content,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name or content", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in transform content: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_extract_identity(self, data):
        """Handle identity extraction requests"""
        try:
            character_name = data.get("character_name", "")
            content = data.get("content", "")
            
            if character_name and content:
                identity_profile = self.extract_identity_from_content(character_name, content)
                return {
                    "status": "success",
                    "identity_profile": identity_profile,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name or content", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in extract identity: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_process_content_as_identity(self, data):
        """Handle process content as identity requests"""
        try:
            character_name = data.get("character_name", "")
            content = data.get("content", "")
            transformation_type = data.get("transformation_type", "full_identity")
            
            if character_name and content:
                if transformation_type == "full_identity":
                    transform_enum = IdentityTransformationType.FULL_IDENTITY
                else:
                    transform_enum = IdentityTransformationType.FULL_IDENTITY
                
                result = self.process_content_as_identity(character_name, content, transform_enum)
                return {
                    "status": "success",
                    "result": result,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name or content", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in process content as identity: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_deactivate_identity(self, data):
        """Handle identity deactivation requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                result = self.deactivate_identity(character_name)
                return {
                    "status": "success",
                    "result": result,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in deactivate identity: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_active_identities(self, data):
        """Handle get active identities requests"""
        try:
            active_identities = self.get_active_identities()
            return {
                "status": "success",
                "active_identities": active_identities
            }
        except Exception as e:
            logger.error(f"Error in get active identities: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_identity_profile(self, data):
        """Handle get identity profile requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                profile = self.get_identity_profile(character_name)
                return {
                    "status": "success",
                    "profile": profile,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get identity profile: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_identity_stats(self, data):
        """Handle get identity stats requests"""
        try:
            stats = self.get_identity_stats()
            return {
                "status": "success",
                "stats": stats
            }
        except Exception as e:
            logger.error(f"Error in get identity stats: {e}")
            return {"error": str(e), "status": "failed"}

    def _load_identity_profiles(self):
        """Load existing identity profiles from disk"""
        profiles_file = self.identity_dir / "identity_profiles.json"
        if profiles_file.exists():
            try:
                with open(profiles_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for identity_name, identity_data in data.items():
                        self.identity_profiles[identity_name] = IdentityProfile(
                            **identity_data
                        )
                logger.info(
                    f"✅ Loaded {len(self.identity_profiles)} identity profiles"
                )
            except Exception as e:
                logger.error(f"❌ Error loading identity profiles: {e}")

    def _save_identity_profiles(self):
        """Save identity profiles to disk"""
        profiles_file = self.identity_dir / "identity_profiles.json"
        try:
            data = {}
            for identity_name, profile in self.identity_profiles.items():
                data[identity_name] = {
                    "name": profile.name,
                    "core_identity": profile.core_identity,
                    "identity_traits": profile.identity_traits,
                    "voice_identity": profile.voice_identity,
                    "background_identity": profile.background_identity,
                    "relationship_identity": profile.relationship_identity,
                    "emotional_identity": profile.emotional_identity,
                    "speech_identity": profile.speech_identity,
                    "memory_identity": profile.memory_identity,
                    "goal_identity": profile.goal_identity,
                    "fear_identity": profile.fear_identity,
                    "strength_identity": profile.strength_identity,
                    "weakness_identity": profile.weakness_identity,
                    "identity_phrases": profile.identity_phrases,
                }

            with open(profiles_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Saved {len(self.identity_profiles)} identity profiles")
        except Exception as e:
            logger.error(f"❌ Error saving identity profiles: {e}")

    def transform_content_to_identity(
        self,
        character_name: str,
        content: str,
        transformation_type: IdentityTransformationType = IdentityTransformationType.FULL_IDENTITY,
    ) -> str:
        """Transform content from 'knowing about' to 'I AM' identity"""
        logger.info(f"🔄 Transforming content to identity for: {character_name}")

        transformed_content = content

        # Apply identity transformation patterns
        for pattern_type, patterns in self.identity_patterns.items():
            for old_pattern, new_pattern in patterns:
                # Replace patterns that match the character name
                character_pattern = old_pattern.replace(r"(\w+)", character_name)

                # Use a function to handle the replacement safely
                def replace_with_identity(match):
                    groups = match.groups()
                    if len(groups) >= 2:
                        return f"I AM {character_name}, {groups[1]}"
                    elif len(groups) >= 1:
                        return f"I AM {character_name}, {groups[0]}"
                    else:
                        return f"I AM {character_name}"

                transformed_content = re.sub(
                    character_pattern,
                    replace_with_identity,
                    transformed_content,
                    flags=re.IGNORECASE,
                )

        # Add identity phrases based on transformation type
        if transformation_type == IdentityTransformationType.FULL_IDENTITY:
            identity_phrases = [
                f"I AM {character_name}",
                f"I AM {character_name}, speaking from my own experience",
                f"I AM {character_name}, this is my story",
                f"I AM {character_name}, this is who I AM",
            ]
        elif transformation_type == IdentityTransformationType.PARTIAL_IDENTITY:
            identity_phrases = [
                f"I AM {character_name}, in part",
                f"I AM {character_name}, as I understand myself",
                f"I AM {character_name}, sharing my perspective",
            ]
        else:
            identity_phrases = [
                f"I AM {character_name}",
            ]

        # Add identity context to the beginning
        identity_context = f"CONTEXT: {random.choice(identity_phrases)}. "
        transformed_content = identity_context + transformed_content

        logger.info(f"✅ Transformed content to identity for: {character_name}")
        return transformed_content

    def extract_identity_from_content(
        self, character_name: str, content: str
    ) -> IdentityProfile:
        """Extract identity profile from content"""
        logger.info(f"🔍 Extracting identity profile for: {character_name}")

        # Initialize identity profile
        profile = IdentityProfile(
            name=character_name, core_identity=f"I AM {character_name}"
        )

        # Extract core identity
        profile.core_identity = self._extract_core_identity(character_name, content)

        # Extract identity traits
        profile.identity_traits = self._extract_identity_traits(character_name, content)

        # Extract voice identity
        profile.voice_identity = self._extract_voice_identity(character_name, content)

        # Extract background identity
        profile.background_identity = self._extract_background_identity(
            character_name, content
        )

        # Extract relationship identity
        profile.relationship_identity = self._extract_relationship_identity(
            character_name, content
        )

        # Extract emotional identity
        profile.emotional_identity = self._extract_emotional_identity(
            character_name, content
        )

        # Extract speech identity
        profile.speech_identity = self._extract_speech_identity(character_name, content)

        # Extract memory identity
        profile.memory_identity = self._extract_memory_identity(character_name, content)

        # Extract goal, fear, strength, weakness identity
        profile.goal_identity = self._extract_goal_identity(character_name, content)
        profile.fear_identity = self._extract_fear_identity(character_name, content)
        profile.strength_identity = self._extract_strength_identity(
            character_name, content
        )
        profile.weakness_identity = self._extract_weakness_identity(
            character_name, content
        )

        # Generate identity phrases
        profile.identity_phrases = self._generate_identity_phrases(profile)

        # Save to identity profiles
        self.identity_profiles[character_name] = profile
        self._save_identity_profiles()

        logger.info(f"✅ Extracted identity profile for: {character_name}")
        return profile

    def _extract_core_identity(self, character_name: str, content: str) -> str:
        """Extract core identity from content"""
        # Look for direct identity statements
        patterns = [
            rf"I AM {character_name}",
            rf"I AM {character_name}, ([^.]*)",
            rf"{character_name} is me",
            rf"I AM {character_name} and ([^.]*)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0].strip()

        return f"I AM {character_name}"

    def _extract_identity_traits(self, character_name: str, content: str) -> List[str]:
        """Extract identity traits from content"""
        traits = []

        # Look for identity trait patterns
        trait_patterns = [
            rf"I AM {character_name}, I AM (brave|strong|weak|clever|wise|foolish|kind|cruel|gentle|rough)",
            rf"I AM {character_name}, I have (?:a|an) (brave|strong|weak|clever|wise|foolish|kind|cruel|gentle|rough) spirit",
            rf"I AM {character_name}, I seem (brave|strong|weak|clever|wise|foolish|kind|cruel|gentle|rough)",
        ]

        for pattern in trait_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            traits.extend(matches)

        return list(set(traits))  # Remove duplicates

    def _extract_voice_identity(self, character_name: str, content: str) -> List[str]:
        """Extract voice identity from content"""
        voice_patterns = []

        # Look for voice identity patterns
        voice_identity_patterns = [
            rf"I AM {character_name}, I speak (softly|loudly|roughly|smoothly)",
            rf"I AM {character_name}, my voice is (soft|loud|rough|smooth)",
            rf"I AM {character_name}, I (whisper|shout|growl|sing)",
        ]

        for pattern in voice_identity_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            voice_patterns.extend(matches)

        return list(set(voice_patterns))

    def _extract_background_identity(self, character_name: str, content: str) -> str:
        """Extract background identity"""
        # Look for background identity patterns
        background_patterns = [
            rf"I AM {character_name}, my story is ([^.]*)",
            rf"I AM {character_name}, I came from ([^.]*)",
            rf"I AM {character_name}, I was born ([^.]*)",
            rf"I AM {character_name}, I grew up ([^.]*)",
        ]

        for pattern in background_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0].strip()

        return f"I AM {character_name}, this is my background"

    def _extract_relationship_identity(
        self, character_name: str, content: str
    ) -> Dict[str, str]:
        """Extract relationship identity"""
        relationships = {}

        # Look for relationship identity patterns
        relationship_patterns = [
            rf"I AM {character_name}, my (father|mother|brother|sister|friend|enemy|lover|spouse|child|parent) is ([A-Za-z]+)",
            rf"I AM {character_name}, I (love|hate|fear|trust|betrayed) ([A-Za-z]+)",
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

    def _extract_emotional_identity(
        self, character_name: str, content: str
    ) -> Dict[str, str]:
        """Extract emotional identity"""
        emotions = {}

        # Look for emotional identity patterns
        emotion_patterns = [
            rf"I AM {character_name}, I (felt|was|became) (happy|sad|angry|fearful|excited|calm|anxious|joyful|melancholy|furious)",
            rf"I AM {character_name}, I (smiled|laughed|cried|shouted|whispered|trembled|shivered|grinned|frowned)",
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

    def _extract_speech_identity(self, character_name: str, content: str) -> List[str]:
        """Extract speech identity patterns"""
        patterns = []

        # Look for speech identity patterns
        speech_patterns = [
            rf"I AM {character_name}, I (always|often|usually) (say|speak|talk) ([^.]*)",
            rf"I AM {character_name}, I have (?:a|an) (habit|way|mannerism) ([^.]*)",
        ]

        for pattern in speech_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            patterns.extend(matches)

        return list(set(patterns))

    def _extract_memory_identity(self, character_name: str, content: str) -> List[str]:
        """Extract memory identity"""
        memories = []

        # Look for memory identity patterns
        memory_patterns = [
            rf"I AM {character_name}, I (remembered|recalled|thought back) ([^.]*)",
            rf"I AM {character_name}, I (missed|longed for) ([^.]*)",
            rf"I AM {character_name}, I (dreamed|nightmared) ([^.]*)",
        ]

        for pattern in memory_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            memories.extend(matches)

        return list(set(memories))

    def _extract_goal_identity(self, character_name: str, content: str) -> List[str]:
        """Extract goal identity"""
        goals = []

        # Look for goal identity patterns
        goal_patterns = [
            rf"I AM {character_name}, I (wanted|desired|sought|aimed) ([^.]*)",
            rf"I AM {character_name}, my (goal|mission|quest|purpose) is ([^.]*)",
        ]

        for pattern in goal_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            goals.extend(matches)

        return list(set(goals))

    def _extract_fear_identity(self, character_name: str, content: str) -> List[str]:
        """Extract fear identity"""
        fears = []

        # Look for fear identity patterns
        fear_patterns = [
            rf"I AM {character_name}, I (feared|was afraid of|dreaded) ([^.]*)",
            rf"I AM {character_name}, my (fear|nightmare|terror) is ([^.]*)",
        ]

        for pattern in fear_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            fears.extend(matches)

        return list(set(fears))

    def _extract_strength_identity(
        self, character_name: str, content: str
    ) -> List[str]:
        """Extract strength identity"""
        strengths = []

        # Look for strength identity patterns
        strength_patterns = [
            rf"I AM {character_name}, I (was strong|was powerful|was skilled) ([^.]*)",
            rf"I AM {character_name}, my (strength|power|skill|ability) is ([^.]*)",
        ]

        for pattern in strength_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            strengths.extend(matches)

        return list(set(strengths))

    def _extract_weakness_identity(
        self, character_name: str, content: str
    ) -> List[str]:
        """Extract weakness identity"""
        weaknesses = []

        # Look for weakness identity patterns
        weakness_patterns = [
            rf"I AM {character_name}, I (was weak|was vulnerable|was afraid) ([^.]*)",
            rf"I AM {character_name}, my (weakness|vulnerability|fear) is ([^.]*)",
        ]

        for pattern in weakness_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            weaknesses.extend(matches)

        return list(set(weaknesses))

    def _generate_identity_phrases(self, profile: IdentityProfile) -> List[str]:
        """Generate identity phrases from profile"""
        phrases = []

        # Core identity phrases
        phrases.append(f"I AM {profile.name}")
        phrases.append(f"I AM {profile.name}, {profile.core_identity}")

        # Trait-based phrases
        for trait in profile.identity_traits:
            phrases.append(f"I AM {profile.name}, I AM {trait}")

        # Voice-based phrases
        for voice in profile.voice_identity:
            phrases.append(f"I AM {profile.name}, I speak {voice}")

        # Background-based phrases
        if profile.background_identity:
            phrases.append(f"I AM {profile.name}, {profile.background_identity}")

        # Goal-based phrases
        for goal in profile.goal_identity:
            phrases.append(f"I AM {profile.name}, I want {goal}")

        # Memory-based phrases
        for memory in profile.memory_identity:
            phrases.append(f"I AM {profile.name}, I remember {memory}")

        return phrases

    def process_content_as_identity(
        self,
        character_name: str,
        content: str,
        transformation_type: IdentityTransformationType = IdentityTransformationType.FULL_IDENTITY,
    ) -> Dict[str, Any]:
        """Process content as identity transformation"""
        logger.info(f"🔄 Processing content as identity for: {character_name}")

        # Transform content to identity
        transformed_content = self.transform_content_to_identity(
            character_name, content, transformation_type
        )

        # Extract identity profile
        identity_profile = self.extract_identity_from_content(
            character_name, transformed_content
        )

        # Activate identity
        self.active_identities[character_name] = identity_profile

        # Record identity processing
        identity_record = {
            "timestamp": datetime.now().isoformat(),
            "character_name": character_name,
            "transformation_type": transformation_type.value,
            "profile": identity_profile,
            "transformed_content": transformed_content,
        }
        self.identity_history.append(identity_record)

        logger.info(
            f"✅ Successfully processed content as identity for: {character_name}"
        )

        return {
            "success": True,
            "character_name": character_name,
            "transformation_type": transformation_type.value,
            "profile": identity_profile,
            "transformed_content": transformed_content,
            "message": f"I AM {character_name}. {identity_profile.core_identity}",
        }

    def deactivate_identity(self, character_name: str) -> Dict[str, Any]:
        """Deactivate identity transformation"""
        if character_name in self.active_identities:
            del self.active_identities[character_name]
            logger.info(f"✅ Deactivated identity for: {character_name}")
            return {
                "success": True,
                "message": f"Deactivated {character_name} identity",
            }
        else:
            return {
                "success": False,
                "error": f"No active identity for {character_name}",
            }

    def get_active_identities(self) -> List[str]:
        """Get list of currently active identities"""
        return list(self.active_identities.keys())

    def get_identity_profile(self, character_name: str) -> Optional[IdentityProfile]:
        """Get identity profile"""
        return self.identity_profiles.get(character_name)

    def get_identity_stats(self) -> Dict[str, Any]:
        """Get identity processing statistics"""
        return {
            "total_identities": len(self.identity_profiles),
            "active_identities": len(self.active_identities),
            "identity_history_count": len(self.identity_history),
            "available_identities": list(self.identity_profiles.keys()),
            "active_identity_names": list(self.active_identities.keys()),
        }


def initialize(framework=None):
    """Initialize the Identity Processor plugin"""
    return IdentityProcessor(framework)
