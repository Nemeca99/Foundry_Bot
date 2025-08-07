#!/usr/bin/env python3
"""
Character Interaction Engine
Provides character-to-character interaction systems, dialogue generation, and relationship dynamics
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime
import random

from core.config import Config

# Add framework to path
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

from queue_manager import QueueProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InteractionType(Enum):
    """Types of character interactions"""

    CONVERSATION = "conversation"
    CONFLICT = "conflict"
    COLLABORATION = "collaboration"
    ROMANCE = "romance"
    FRIENDSHIP = "friendship"
    MENTORSHIP = "mentorship"
    RIVALRY = "rivalry"


class DialogueEmotion(Enum):
    """Emotional states for dialogue"""

    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    EXCITED = "excited"
    CALM = "calm"
    NERVOUS = "nervous"
    CONFIDENT = "confident"
    VULNERABLE = "vulnerable"
    PLAYFUL = "playful"
    SERIOUS = "serious"
    SUPPORTIVE = "supportive"


@dataclass
class DialogueLine:
    """Represents a single line of dialogue"""

    speaker: str
    content: str
    emotion: DialogueEmotion
    timestamp: str
    context: Dict[str, Any]


@dataclass
class CharacterInteraction:
    """Represents an interaction between characters"""

    interaction_id: str
    interaction_type: InteractionType
    participants: List[str]
    dialogue: List[DialogueLine]
    emotional_intensity: float
    relationship_impact: Dict[str, float]
    context: Dict[str, Any]
    timestamp: str


@dataclass
class CharacterDialogueProfile:
    """Dialogue profile for a specific character"""

    character_name: str
    speech_patterns: Dict[str, float]
    vocabulary_preferences: List[str]
    emotional_expressions: Dict[str, List[str]]
    dialogue_history: List[str]
    interaction_style: str


class CharacterInteractionEngine(QueueProcessor):
    """
    Character Interaction Engine
    Provides character-to-character interaction and dialogue generation
    """

    def __init__(self):
        super().__init__("character_interaction_engine")
        self.config = Config()
        # Use the current file's location to determine project root
        project_root = Path(__file__).parent.parent.parent
        self.interaction_data_dir = project_root / "models" / "interaction"
        self.interaction_data_dir.mkdir(parents=True, exist_ok=True)

        self.character_interactions = {}
        self.dialogue_profiles = {}
        self.interaction_templates = {}

        # Load existing interaction data
        self._load_interaction_data()
        self._initialize_dialogue_templates()

    def _load_interaction_data(self):
        """Load existing interaction data from disk"""
        interaction_file = self.interaction_data_dir / "interaction_data.json"
        if interaction_file.exists():
            try:
                with open(interaction_file, "r") as f:
                    data = json.load(f)
                    self.character_interactions = data.get("character_interactions", [])
                    self.character_dialogue_profiles = data.get(
                        "character_dialogue_profiles", {}
                    )
                    self.interaction_templates = data.get("interaction_templates", {})
                logger.info("Loaded existing interaction data")
            except Exception as e:
                logger.error(f"Error loading interaction data: {e}")

    def _save_interaction_data(self):
        """Save current interaction data to disk"""
        interaction_file = self.interaction_data_dir / "interaction_data.json"
        try:
            # Convert enum values to strings for JSON serialization
            serializable_interactions = []
            for interaction in self.character_interactions:
                if isinstance(interaction, dict):
                    # Already a dict, just ensure enum values are strings
                    interaction_copy = interaction.copy()
                    if "interaction_type" in interaction_copy and hasattr(
                        interaction_copy["interaction_type"], "value"
                    ):
                        interaction_copy["interaction_type"] = interaction_copy[
                            "interaction_type"
                        ].value
                    serializable_interactions.append(interaction_copy)
                else:
                    # Convert dataclass to dict with string enum values
                    interaction_dict = asdict(interaction)
                    interaction_dict["interaction_type"] = (
                        interaction.interaction_type.value
                    )
                    # Convert dialogue lines
                    serializable_dialogue = []
                    for line in interaction.dialogue:
                        line_dict = asdict(line)
                        line_dict["emotion"] = line.emotion.value
                        serializable_dialogue.append(line_dict)
                    interaction_dict["dialogue"] = serializable_dialogue
                    serializable_interactions.append(interaction_dict)

            data = {
                "character_interactions": serializable_interactions,
                "character_dialogue_profiles": self.character_dialogue_profiles,
                "interaction_templates": self.interaction_templates,
            }
            with open(interaction_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved interaction data")
        except Exception as e:
            logger.error(f"Error saving interaction data: {e}")

    def _initialize_dialogue_templates(self):
        """Initialize dialogue templates for different interaction types"""
        self.interaction_templates = {
            "conversation": {
                "greetings": [
                    "Hello, {other_character}. How are you today?",
                    "Good to see you, {other_character}.",
                    "Hey there, {other_character}. What's on your mind?",
                ],
                "responses": [
                    "I'm doing well, thank you for asking.",
                    "It's been an interesting day.",
                    "I have something I'd like to discuss.",
                ],
            },
            "conflict": {
                "challenges": [
                    "I don't agree with what you're saying, {other_character}.",
                    "You're wrong about this, and I can prove it.",
                    "I won't stand for this, {other_character}.",
                ],
                "defenses": [
                    "I have my reasons for thinking this way.",
                    "You don't understand the full situation.",
                    "I'm not backing down from this.",
                ],
            },
            "collaboration": {
                "proposals": [
                    "I think we could work together on this, {other_character}.",
                    "What if we combined our strengths?",
                    "I have an idea that might benefit us both.",
                ],
                "agreements": [
                    "That sounds like a good plan.",
                    "I'm willing to give it a try.",
                    "Let's see what we can accomplish together.",
                ],
            },
            "romance": {
                "expressions": [
                    "I've been thinking about you a lot lately, {other_character}.",
                    "You mean more to me than I can express.",
                    "I feel something special when I'm with you.",
                ],
                "responses": [
                    "I feel the same way about you.",
                    "You make my heart skip a beat.",
                    "I never thought I'd feel this way.",
                ],
            },
            "friendship": {
                "support": [
                    "I'm here for you, {other_character}. Always.",
                    "You can count on me, no matter what.",
                    "We're in this together, friend.",
                ],
                "appreciation": [
                    "Thank you for being such a good friend.",
                    "I'm lucky to have you in my life.",
                    "You always know how to make me feel better.",
                ],
            },
        }

    def create_character_dialogue_profile(
        self,
        character_name: str,
        speech_patterns: Dict[str, float] = None,
        vocabulary_preferences: List[str] = None,
        emotional_expressions: Dict[str, List[str]] = None,
        interaction_style: str = "neutral",
    ) -> CharacterDialogueProfile:
        """Create a dialogue profile for a character"""
        profile = CharacterDialogueProfile(
            character_name=character_name,
            speech_patterns=speech_patterns or {},
            vocabulary_preferences=vocabulary_preferences or [],
            emotional_expressions=emotional_expressions or {},
            dialogue_history=[],
            interaction_style=interaction_style,
        )

        self.character_dialogue_profiles[character_name] = asdict(profile)
        self._save_interaction_data()

        logger.info(f"Created dialogue profile for {character_name}")
        return profile

    def generate_dialogue(
        self,
        speaker: str,
        listener: str,
        interaction_type: InteractionType,
        emotion: DialogueEmotion = DialogueEmotion.CALM,
        context: Dict[str, Any] = None,
    ) -> DialogueLine:
        """Generate dialogue for a character interaction"""

        # Get character dialogue profiles
        speaker_profile = self.character_dialogue_profiles.get(speaker, {})
        listener_profile = self.character_dialogue_profiles.get(listener, {})

        # Get appropriate template
        templates = self.interaction_templates.get(interaction_type.value, {})

        # Generate dialogue based on interaction type and emotion
        if interaction_type == InteractionType.CONVERSATION:
            content = self._generate_conversation_dialogue(
                speaker, listener, emotion, templates
            )
        elif interaction_type == InteractionType.CONFLICT:
            content = self._generate_conflict_dialogue(
                speaker, listener, emotion, templates
            )
        elif interaction_type == InteractionType.COLLABORATION:
            content = self._generate_collaboration_dialogue(
                speaker, listener, emotion, templates
            )
        elif interaction_type == InteractionType.ROMANCE:
            content = self._generate_romance_dialogue(
                speaker, listener, emotion, templates
            )
        elif interaction_type == InteractionType.FRIENDSHIP:
            content = self._generate_friendship_dialogue(
                speaker, listener, emotion, templates
            )
        else:
            content = self._generate_generic_dialogue(speaker, listener, emotion)

        # Apply character-specific speech patterns
        content = self._apply_speech_patterns(content, speaker_profile)

        dialogue_line = DialogueLine(
            speaker=speaker,
            content=content,
            emotion=emotion,
            timestamp=datetime.now().isoformat(),
            context=context or {},
        )

        # Update character's dialogue history
        if speaker in self.character_dialogue_profiles:
            self.character_dialogue_profiles[speaker]["dialogue_history"].append(
                content
            )

        return dialogue_line

    def _generate_conversation_dialogue(
        self, speaker: str, listener: str, emotion: DialogueEmotion, templates: Dict
    ) -> str:
        """Generate conversation dialogue"""
        if emotion == DialogueEmotion.HAPPY:
            return f"I'm so glad to see you, {listener}! How have you been?"
        elif emotion == DialogueEmotion.EXCITED:
            return f"Hey {listener}! I have something amazing to tell you!"
        elif emotion == DialogueEmotion.SERIOUS:
            return f"{listener}, we need to talk about something important."
        else:
            greetings = templates.get("greetings", [])
            if greetings:
                return random.choice(greetings).format(other_character=listener)
            return f"Hello, {listener}. How are you?"

    def _generate_conflict_dialogue(
        self, speaker: str, listener: str, emotion: DialogueEmotion, templates: Dict
    ) -> str:
        """Generate conflict dialogue"""
        if emotion == DialogueEmotion.ANGRY:
            return f"I can't believe you would do that, {listener}! How could you?"
        elif emotion == DialogueEmotion.CONFIDENT:
            return f"You're wrong about this, {listener}, and I can prove it."
        else:
            challenges = templates.get("challenges", [])
            if challenges:
                return random.choice(challenges).format(other_character=listener)
            return f"I disagree with you, {listener}."

    def _generate_collaboration_dialogue(
        self, speaker: str, listener: str, emotion: DialogueEmotion, templates: Dict
    ) -> str:
        """Generate collaboration dialogue"""
        if emotion == DialogueEmotion.EXCITED:
            return f"Listen, {listener}! I have an idea that could change everything!"
        elif emotion == DialogueEmotion.CONFIDENT:
            return f"I think we could accomplish great things together, {listener}."
        else:
            proposals = templates.get("proposals", [])
            if proposals:
                return random.choice(proposals).format(other_character=listener)
            return f"What if we worked together on this, {listener}?"

    def _generate_romance_dialogue(
        self, speaker: str, listener: str, emotion: DialogueEmotion, templates: Dict
    ) -> str:
        """Generate romance dialogue"""
        if emotion == DialogueEmotion.VULNERABLE:
            return f"I've been thinking about you a lot lately, {listener}..."
        elif emotion == DialogueEmotion.CONFIDENT:
            return f"You make my heart skip a beat, {listener}."
        else:
            expressions = templates.get("expressions", [])
            if expressions:
                return random.choice(expressions).format(other_character=listener)
            return f"I care about you deeply, {listener}."

    def _generate_friendship_dialogue(
        self, speaker: str, listener: str, emotion: DialogueEmotion, templates: Dict
    ) -> str:
        """Generate friendship dialogue"""
        if emotion == DialogueEmotion.HAPPY:
            return f"I'm so grateful to have you as a friend, {listener}!"
        elif emotion == DialogueEmotion.SUPPORTIVE:
            return f"I'm here for you, {listener}. Always."
        else:
            support = templates.get("support", [])
            if support:
                return random.choice(support).format(other_character=listener)
            return f"You're a great friend, {listener}."

    def _generate_generic_dialogue(
        self, speaker: str, listener: str, emotion: DialogueEmotion
    ) -> str:
        """Generate generic dialogue"""
        if emotion == DialogueEmotion.HAPPY:
            return f"Hello, {listener}! It's wonderful to see you!"
        elif emotion == DialogueEmotion.SAD:
            return f"Hi, {listener}... I'm not feeling my best today."
        elif emotion == DialogueEmotion.ANGRY:
            return f"{listener}, we need to talk about this."
        else:
            return f"Hello, {listener}."

    def _apply_speech_patterns(self, content: str, profile: Dict) -> str:
        """Apply character-specific speech patterns to dialogue"""
        speech_patterns = profile.get("speech_patterns", {})
        vocabulary = profile.get("vocabulary_preferences", [])

        # Apply vocabulary preferences
        for word in vocabulary:
            if word.lower() in content.lower():
                # Character uses this word frequently
                pass

        # Apply speech patterns (simplified)
        if "formal" in speech_patterns and speech_patterns["formal"] > 0.7:
            content = content.replace("Hey", "Greetings")
            content = content.replace("Hi", "Hello")

        if "casual" in speech_patterns and speech_patterns["casual"] > 0.7:
            content = content.replace("Hello", "Hey")
            content = content.replace("Greetings", "Hi")

        return content

    def create_interaction(
        self,
        interaction_type: InteractionType,
        participants: List[str],
        dialogue_lines: List[DialogueLine] = None,
        emotional_intensity: float = 0.5,
        context: Dict[str, Any] = None,
    ) -> CharacterInteraction:
        """Create a character interaction"""
        interaction_id = f"interaction_{len(self.character_interactions)}"

        interaction = CharacterInteraction(
            interaction_id=interaction_id,
            interaction_type=interaction_type,
            participants=participants,
            dialogue=dialogue_lines or [],
            emotional_intensity=emotional_intensity,
            relationship_impact={},
            context=context or {},
            timestamp=datetime.now().isoformat(),
        )

        # Add to interactions list
        interaction_dict = asdict(interaction)
        interaction_dict["interaction_type"] = interaction.interaction_type.value
        # Convert dialogue lines
        serializable_dialogue = []
        for line in interaction.dialogue:
            line_dict = asdict(line)
            line_dict["emotion"] = line.emotion.value
            serializable_dialogue.append(line_dict)
        interaction_dict["dialogue"] = serializable_dialogue

        self.character_interactions.append(interaction_dict)
        self._save_interaction_data()

        logger.info(
            f"Created {interaction_type.value} interaction between {', '.join(participants)}"
        )
        return interaction

    def generate_interaction_sequence(
        self,
        character_a: str,
        character_b: str,
        interaction_type: InteractionType,
        num_exchanges: int = 3,
    ) -> CharacterInteraction:
        """Generate a sequence of dialogue exchanges between characters"""
        dialogue_lines = []

        for i in range(num_exchanges):
            # Alternate speakers
            speaker = character_a if i % 2 == 0 else character_b
            listener = character_b if i % 2 == 0 else character_a

            # Vary emotions based on interaction type
            if interaction_type == InteractionType.CONFLICT:
                emotion = DialogueEmotion.ANGRY if i == 0 else DialogueEmotion.SERIOUS
            elif interaction_type == InteractionType.ROMANCE:
                emotion = (
                    DialogueEmotion.VULNERABLE if i == 0 else DialogueEmotion.HAPPY
                )
            elif interaction_type == InteractionType.FRIENDSHIP:
                emotion = DialogueEmotion.HAPPY if i == 0 else DialogueEmotion.CALM
            else:
                emotion = DialogueEmotion.CALM

            dialogue_line = self.generate_dialogue(
                speaker, listener, interaction_type, emotion
            )
            dialogue_lines.append(dialogue_line)

        # Create the interaction
        interaction = self.create_interaction(
            interaction_type=interaction_type,
            participants=[character_a, character_b],
            dialogue_lines=dialogue_lines,
            emotional_intensity=(
                0.6 if interaction_type == InteractionType.CONFLICT else 0.4
            ),
        )

        return interaction

    def get_character_interactions(
        self, character_name: str, interaction_type: InteractionType = None
    ) -> List[Dict]:
        """Get interactions involving a character"""
        interactions = []

        for interaction in self.character_interactions:
            if character_name in interaction.get("participants", []):
                if (
                    interaction_type is None
                    or interaction.get("interaction_type") == interaction_type.value
                ):
                    interactions.append(interaction)

        return interactions

    def get_dialogue_profile(self, character_name: str) -> Dict:
        """Get a character's dialogue profile"""
        return self.character_dialogue_profiles.get(character_name, {})

    def update_dialogue_profile(
        self,
        character_name: str,
        speech_patterns: Dict[str, float] = None,
        vocabulary_preferences: List[str] = None,
        emotional_expressions: Dict[str, List[str]] = None,
        interaction_style: str = None,
    ):
        """Update a character's dialogue profile"""
        if character_name not in self.character_dialogue_profiles:
            self.create_character_dialogue_profile(character_name)

        profile = self.character_dialogue_profiles[character_name]

        if speech_patterns:
            profile["speech_patterns"].update(speech_patterns)
        if vocabulary_preferences:
            profile["vocabulary_preferences"].extend(vocabulary_preferences)
        if emotional_expressions:
            profile["emotional_expressions"].update(emotional_expressions)
        if interaction_style:
            profile["interaction_style"] = interaction_style

        self._save_interaction_data()
        logger.info(f"Updated dialogue profile for {character_name}")

    def get_interaction_summary(self, character_name: str) -> str:
        """Get a summary of a character's interactions"""
        interactions = self.get_character_interactions(character_name)

        if not interactions:
            return f"No interaction data available for {character_name}"

        summary_parts = []
        summary_parts.append(f"Interaction Summary for {character_name}:")
        summary_parts.append(f"- Total interactions: {len(interactions)}")

        # Count interaction types
        interaction_types = {}
        for interaction in interactions:
            interaction_type = interaction.get("interaction_type", "unknown")
            interaction_types[interaction_type] = (
                interaction_types.get(interaction_type, 0) + 1
            )

        summary_parts.append("- Interaction breakdown:")
        for interaction_type, count in interaction_types.items():
            summary_parts.append(f"  * {interaction_type}: {count}")

        # Get dialogue profile info
        profile = self.get_dialogue_profile(character_name)
        if profile:
            summary_parts.append(
                f"- Interaction style: {profile.get('interaction_style', 'neutral')}"
            )
            summary_parts.append(
                f"- Dialogue history entries: {len(profile.get('dialogue_history', []))}"
            )

        return "\n".join(summary_parts)

    def get_relationship_dynamics(
        self, character_a: str, character_b: str
    ) -> Dict[str, Any]:
        """Analyze relationship dynamics between two characters"""
        interactions = []

        for interaction in self.character_interactions:
            participants = interaction.get("participants", [])
            if character_a in participants and character_b in participants:
                interactions.append(interaction)

        if not interactions:
            return {
                "message": f"No interaction history between {character_a} and {character_b}"
            }

        # Analyze interaction patterns
        interaction_types = {}
        emotional_intensities = []
        total_dialogue_lines = 0

        for interaction in interactions:
            interaction_type = interaction.get("interaction_type", "unknown")
            interaction_types[interaction_type] = (
                interaction_types.get(interaction_type, 0) + 1
            )

            emotional_intensities.append(interaction.get("emotional_intensity", 0.0))
            total_dialogue_lines += len(interaction.get("dialogue", []))

        avg_emotional_intensity = (
            sum(emotional_intensities) / len(emotional_intensities)
            if emotional_intensities
            else 0.0
        )

        dynamics = {
            "total_interactions": len(interactions),
            "interaction_types": interaction_types,
            "average_emotional_intensity": avg_emotional_intensity,
            "total_dialogue_exchanges": total_dialogue_lines,
            "most_common_interaction_type": (
                max(interaction_types.items(), key=lambda x: x[1])[0]
                if interaction_types
                else None
            ),
        }

        return dynamics

    def reset_character_interactions(self, character_name: str):
        """Reset all interactions for a character"""
        # Remove interactions involving this character
        self.character_interactions = [
            interaction
            for interaction in self.character_interactions
            if character_name not in interaction.get("participants", [])
        ]

        # Remove dialogue profile
        if character_name in self.character_dialogue_profiles:
            del self.character_dialogue_profiles[character_name]

        self._save_interaction_data()
        logger.info(f"Reset all interactions for {character_name}")

    def reset_all_interactions(self):
        """Reset all interaction data"""
        self.character_interactions = []
        self.character_dialogue_profiles = {}
        self.interaction_templates = {}
        self._save_interaction_data()
        logger.info("Reset all interaction data")

    def _process_item(self, item):
        """Process queue items for character interaction engine operations"""
        try:
            # Extract operation type from data
            operation_type = item.data.get("type", "unknown")
            
            if operation_type == "create_dialogue_profile":
                return self._handle_create_dialogue_profile(item.data)
            elif operation_type == "generate_dialogue":
                return self._handle_generate_dialogue(item.data)
            elif operation_type == "create_interaction":
                return self._handle_create_interaction(item.data)
            elif operation_type == "generate_interaction_sequence":
                return self._handle_generate_interaction_sequence(item.data)
            elif operation_type == "get_character_interactions":
                return self._handle_get_character_interactions(item.data)
            elif operation_type == "get_dialogue_profile":
                return self._handle_get_dialogue_profile(item.data)
            elif operation_type == "update_dialogue_profile":
                return self._handle_update_dialogue_profile(item.data)
            elif operation_type == "get_interaction_summary":
                return self._handle_get_interaction_summary(item.data)
            elif operation_type == "get_relationship_dynamics":
                return self._handle_get_relationship_dynamics(item.data)
            elif operation_type == "reset_character_interactions":
                return self._handle_reset_character_interactions(item.data)
            elif operation_type == "reset_all_interactions":
                return self._handle_reset_all_interactions(item.data)
            else:
                # Pass unknown types to base class
                return super()._process_item(item)
        except Exception as e:
            logger.error(f"Error processing character interaction engine queue item: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_create_dialogue_profile(self, data):
        """Handle create dialogue profile requests"""
        try:
            character_name = data.get("character_name", "")
            speech_patterns = data.get("speech_patterns", {})
            vocabulary_preferences = data.get("vocabulary_preferences", [])
            emotional_expressions = data.get("emotional_expressions", {})
            interaction_style = data.get("interaction_style", "neutral")
            
            if character_name:
                profile = self.create_character_dialogue_profile(
                    character_name, speech_patterns, vocabulary_preferences, emotional_expressions, interaction_style
                )
                return {
                    "status": "success",
                    "profile": profile,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in create dialogue profile: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_generate_dialogue(self, data):
        """Handle generate dialogue requests"""
        try:
            speaker = data.get("speaker", "")
            listener = data.get("listener", "")
            interaction_type = data.get("interaction_type", "")
            emotion = data.get("emotion", "calm")
            context = data.get("context", {})
            
            if speaker and listener and interaction_type:
                if interaction_type == "conversation":
                    int_type = InteractionType.CONVERSATION
                elif interaction_type == "conflict":
                    int_type = InteractionType.CONFLICT
                elif interaction_type == "collaboration":
                    int_type = InteractionType.COLLABORATION
                elif interaction_type == "romance":
                    int_type = InteractionType.ROMANCE
                elif interaction_type == "friendship":
                    int_type = InteractionType.FRIENDSHIP
                elif interaction_type == "mentorship":
                    int_type = InteractionType.MENTORSHIP
                elif interaction_type == "rivalry":
                    int_type = InteractionType.RIVALRY
                else:
                    int_type = InteractionType.CONVERSATION
                
                if emotion == "happy":
                    emo = DialogueEmotion.HAPPY
                elif emotion == "sad":
                    emo = DialogueEmotion.SAD
                elif emotion == "angry":
                    emo = DialogueEmotion.ANGRY
                elif emotion == "excited":
                    emo = DialogueEmotion.EXCITED
                elif emotion == "calm":
                    emo = DialogueEmotion.CALM
                elif emotion == "nervous":
                    emo = DialogueEmotion.NERVOUS
                elif emotion == "confident":
                    emo = DialogueEmotion.CONFIDENT
                elif emotion == "vulnerable":
                    emo = DialogueEmotion.VULNERABLE
                elif emotion == "playful":
                    emo = DialogueEmotion.PLAYFUL
                elif emotion == "serious":
                    emo = DialogueEmotion.SERIOUS
                elif emotion == "supportive":
                    emo = DialogueEmotion.SUPPORTIVE
                else:
                    emo = DialogueEmotion.CALM
                
                dialogue = self.generate_dialogue(speaker, listener, int_type, emo, context)
                return {
                    "status": "success",
                    "dialogue": dialogue,
                    "speaker": speaker,
                    "listener": listener
                }
            else:
                return {"error": "Missing required parameters", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in generate dialogue: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_create_interaction(self, data):
        """Handle create interaction requests"""
        try:
            interaction_type = data.get("interaction_type", "")
            participants = data.get("participants", [])
            dialogue_lines = data.get("dialogue_lines", [])
            emotional_intensity = data.get("emotional_intensity", 0.5)
            context = data.get("context", {})
            
            if interaction_type and participants:
                if interaction_type == "conversation":
                    int_type = InteractionType.CONVERSATION
                elif interaction_type == "conflict":
                    int_type = InteractionType.CONFLICT
                elif interaction_type == "collaboration":
                    int_type = InteractionType.COLLABORATION
                elif interaction_type == "romance":
                    int_type = InteractionType.ROMANCE
                elif interaction_type == "friendship":
                    int_type = InteractionType.FRIENDSHIP
                elif interaction_type == "mentorship":
                    int_type = InteractionType.MENTORSHIP
                elif interaction_type == "rivalry":
                    int_type = InteractionType.RIVALRY
                else:
                    int_type = InteractionType.CONVERSATION
                
                interaction = self.create_interaction(int_type, participants, dialogue_lines, emotional_intensity, context)
                return {
                    "status": "success",
                    "interaction": interaction,
                    "interaction_type": interaction_type
                }
            else:
                return {"error": "Missing interaction_type or participants", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in create interaction: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_generate_interaction_sequence(self, data):
        """Handle generate interaction sequence requests"""
        try:
            character_a = data.get("character_a", "")
            character_b = data.get("character_b", "")
            interaction_type = data.get("interaction_type", "")
            num_exchanges = data.get("num_exchanges", 3)
            
            if character_a and character_b and interaction_type:
                if interaction_type == "conversation":
                    int_type = InteractionType.CONVERSATION
                elif interaction_type == "conflict":
                    int_type = InteractionType.CONFLICT
                elif interaction_type == "collaboration":
                    int_type = InteractionType.COLLABORATION
                elif interaction_type == "romance":
                    int_type = InteractionType.ROMANCE
                elif interaction_type == "friendship":
                    int_type = InteractionType.FRIENDSHIP
                elif interaction_type == "mentorship":
                    int_type = InteractionType.MENTORSHIP
                elif interaction_type == "rivalry":
                    int_type = InteractionType.RIVALRY
                else:
                    int_type = InteractionType.CONVERSATION
                
                sequence = self.generate_interaction_sequence(character_a, character_b, int_type, num_exchanges)
                return {
                    "status": "success",
                    "sequence": sequence,
                    "character_a": character_a,
                    "character_b": character_b
                }
            else:
                return {"error": "Missing required parameters", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in generate interaction sequence: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_character_interactions(self, data):
        """Handle get character interactions requests"""
        try:
            character_name = data.get("character_name", "")
            interaction_type = data.get("interaction_type", "")
            
            if character_name:
                if interaction_type:
                    if interaction_type == "conversation":
                        int_type = InteractionType.CONVERSATION
                    elif interaction_type == "conflict":
                        int_type = InteractionType.CONFLICT
                    elif interaction_type == "collaboration":
                        int_type = InteractionType.COLLABORATION
                    elif interaction_type == "romance":
                        int_type = InteractionType.ROMANCE
                    elif interaction_type == "friendship":
                        int_type = InteractionType.FRIENDSHIP
                    elif interaction_type == "mentorship":
                        int_type = InteractionType.MENTORSHIP
                    elif interaction_type == "rivalry":
                        int_type = InteractionType.RIVALRY
                    else:
                        int_type = None
                else:
                    int_type = None
                
                interactions = self.get_character_interactions(character_name, int_type)
                return {
                    "status": "success",
                    "interactions": interactions,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get character interactions: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_dialogue_profile(self, data):
        """Handle get dialogue profile requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                profile = self.get_dialogue_profile(character_name)
                return {
                    "status": "success",
                    "profile": profile,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get dialogue profile: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_update_dialogue_profile(self, data):
        """Handle update dialogue profile requests"""
        try:
            character_name = data.get("character_name", "")
            speech_patterns = data.get("speech_patterns", {})
            vocabulary_preferences = data.get("vocabulary_preferences", [])
            emotional_expressions = data.get("emotional_expressions", {})
            interaction_style = data.get("interaction_style", "")
            
            if character_name:
                self.update_dialogue_profile(character_name, speech_patterns, vocabulary_preferences, emotional_expressions, interaction_style)
                return {
                    "status": "success",
                    "message": f"Dialogue profile updated for {character_name}",
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in update dialogue profile: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_interaction_summary(self, data):
        """Handle get interaction summary requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                summary = self.get_interaction_summary(character_name)
                return {
                    "status": "success",
                    "summary": summary,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get interaction summary: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_relationship_dynamics(self, data):
        """Handle get relationship dynamics requests"""
        try:
            character_a = data.get("character_a", "")
            character_b = data.get("character_b", "")
            
            if character_a and character_b:
                dynamics = self.get_relationship_dynamics(character_a, character_b)
                return {
                    "status": "success",
                    "dynamics": dynamics,
                    "character_a": character_a,
                    "character_b": character_b
                }
            else:
                return {"error": "Missing character_a or character_b", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get relationship dynamics: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_reset_character_interactions(self, data):
        """Handle reset character interactions requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                self.reset_character_interactions(character_name)
                return {
                    "status": "success",
                    "message": f"Interactions reset for {character_name}",
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in reset character interactions: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_reset_all_interactions(self, data):
        """Handle reset all interactions requests"""
        try:
            self.reset_all_interactions()
            return {
                "status": "success",
                "message": "All interactions reset"
            }
        except Exception as e:
            logger.error(f"Error in reset all interactions: {e}")
            return {"error": str(e), "status": "failed"}


def initialize(framework=None):
    """Initialize the Character Interaction Engine"""
    return CharacterInteractionEngine()
