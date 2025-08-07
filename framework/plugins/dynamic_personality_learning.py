#!/usr/bin/env python3
"""
Dynamic Personality Learning System
Allows AI to learn and adapt personality based on character interactions and story development
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

from core.config import Config

# Add framework to path
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

from queue_manager import QueueProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LearningType(Enum):
    """Types of learning that can occur"""

    CHARACTER_INTERACTION = "character_interaction"
    STORY_DEVELOPMENT = "story_development"
    EMOTIONAL_RESPONSE = "emotional_response"
    BEHAVIORAL_ADAPTATION = "behavioral_adaptation"
    COGNITIVE_EVOLUTION = "cognitive_evolution"


class LearningTrigger(Enum):
    """Triggers that initiate learning"""

    CHARACTER_EMBODIMENT = "character_embodiment"
    STORY_ARC = "story_arc"
    EMOTIONAL_EVENT = "emotional_event"
    CONFLICT_RESOLUTION = "conflict_resolution"
    RELATIONSHIP_CHANGE = "relationship_change"


@dataclass
class LearningEvent:
    """Represents a single learning event"""

    event_id: str
    learning_type: LearningType
    trigger: LearningTrigger
    content: str
    character_name: Optional[str]
    emotional_intensity: float  # 0.0 to 1.0
    personality_changes: Dict[str, float]
    timestamp: str
    context: Dict[str, Any]


@dataclass
class CharacterLearningProfile:
    """Learning profile for a specific character"""

    character_name: str
    learning_history: List[LearningEvent]
    personality_evolution: Dict[str, List[float]]
    relationship_dynamics: Dict[str, float]
    story_arc_participation: List[str]
    emotional_patterns: Dict[str, float]


@dataclass
class StoryLearningContext:
    """Context for story-driven learning"""

    story_id: str
    current_arc: str
    character_roles: Dict[str, str]
    plot_developments: List[str]
    emotional_climax: Optional[str]
    resolution_status: str


class DynamicPersonalityLearning(QueueProcessor):
    """
    Dynamic Personality Learning System
    Enables AI to learn and adapt personality through character interactions and story development
    """

    def __init__(self):
        super().__init__("dynamic_personality_learning")
        self.config = Config()
        # Use the current file's location to determine project root
        project_root = Path(__file__).parent.parent.parent
        self.learning_data_dir = project_root / "models" / "learning"
        self.learning_data_dir.mkdir(parents=True, exist_ok=True)

        self.learning_history = []
        self.character_profiles = {}
        self.story_contexts = {}
        self.learning_patterns = {}

        # Load existing learning data
        self._load_learning_data()

    def _load_learning_data(self):
        """Load existing learning data from disk"""
        learning_file = self.learning_data_dir / "learning_data.json"
        if learning_file.exists():
            try:
                with open(learning_file, "r") as f:
                    data = json.load(f)
                    self.learning_history = data.get("learning_history", [])
                    self.character_profiles = data.get("character_profiles", {})
                    self.story_contexts = data.get("story_contexts", {})
                    self.learning_patterns = data.get("learning_patterns", {})
                logger.info("Loaded existing learning data")
            except Exception as e:
                logger.error(f"Error loading learning data: {e}")

    def _save_learning_data(self):
        """Save current learning data to disk"""
        learning_file = self.learning_data_dir / "learning_data.json"
        try:
            # Convert enum values to strings for JSON serialization
            serializable_history = []
            for event in self.learning_history:
                if isinstance(event, dict):
                    # Already a dict, just ensure enum values are strings
                    event_copy = event.copy()
                    if "learning_type" in event_copy and hasattr(
                        event_copy["learning_type"], "value"
                    ):
                        event_copy["learning_type"] = event_copy["learning_type"].value
                    if "trigger" in event_copy and hasattr(
                        event_copy["trigger"], "value"
                    ):
                        event_copy["trigger"] = event_copy["trigger"].value
                    serializable_history.append(event_copy)
                else:
                    # Convert dataclass to dict with string enum values
                    event_dict = asdict(event)
                    event_dict["learning_type"] = event.learning_type.value
                    event_dict["trigger"] = event.trigger.value
                    serializable_history.append(event_dict)

            data = {
                "learning_history": serializable_history,
                "character_profiles": self.character_profiles,
                "story_contexts": self.story_contexts,
                "learning_patterns": self.learning_patterns,
            }
            with open(learning_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved learning data")
        except Exception as e:
            logger.error(f"Error saving learning data: {e}")

    def learn_from_character_interaction(
        self,
        character_name: str,
        interaction_content: str,
        emotional_intensity: float = 0.5,
        context: Dict[str, Any] = None,
    ) -> LearningEvent:
        """
        Learn from a character interaction

        Args:
            character_name: Name of the character being interacted with
            interaction_content: Content describing the interaction
            emotional_intensity: Intensity of the emotional response (0.0 to 1.0)
            context: Additional context for the interaction

        Returns:
            LearningEvent object tracking the learning
        """
        event_id = f"interaction_{len(self.learning_history)}"

        # Analyze interaction for personality changes
        personality_changes = self._analyze_interaction_for_changes(
            interaction_content, emotional_intensity
        )

        # Create learning event
        learning_event = LearningEvent(
            event_id=event_id,
            learning_type=LearningType.CHARACTER_INTERACTION,
            trigger=LearningTrigger.CHARACTER_EMBODIMENT,
            content=interaction_content,
            character_name=character_name,
            emotional_intensity=emotional_intensity,
            personality_changes=personality_changes,
            timestamp=datetime.now().isoformat(),
            context=context or {},
        )

        # Update character profile
        self._update_character_profile(character_name, learning_event)

        # Add to learning history (convert enum to string for JSON serialization)
        event_dict = asdict(learning_event)
        event_dict["learning_type"] = learning_event.learning_type.value
        event_dict["trigger"] = learning_event.trigger.value
        self.learning_history.append(event_dict)

        # Save learning data
        self._save_learning_data()

        logger.info(f"Learned from character interaction with {character_name}")
        return learning_event

    def learn_from_story_development(
        self,
        story_id: str,
        story_content: str,
        current_arc: str = "main",
        context: Dict[str, Any] = None,
    ) -> LearningEvent:
        """
        Learn from story development

        Args:
            story_id: Identifier for the story
            story_content: Content describing the story development
            current_arc: Current story arc
            context: Additional context for the story development

        Returns:
            LearningEvent object tracking the learning
        """
        event_id = f"story_{len(self.learning_history)}"

        # Analyze story development for personality changes
        personality_changes = self._analyze_story_for_changes(
            story_content, current_arc
        )

        # Create learning event
        learning_event = LearningEvent(
            event_id=event_id,
            learning_type=LearningType.STORY_DEVELOPMENT,
            trigger=LearningTrigger.STORY_ARC,
            content=story_content,
            character_name=None,
            emotional_intensity=self._calculate_story_emotional_intensity(
                story_content
            ),
            personality_changes=personality_changes,
            timestamp=datetime.now().isoformat(),
            context=context or {},
        )

        # Update story context
        self._update_story_context(story_id, current_arc, learning_event)

        # Add to learning history (convert enum to string for JSON serialization)
        event_dict = asdict(learning_event)
        event_dict["learning_type"] = learning_event.learning_type.value
        event_dict["trigger"] = learning_event.trigger.value
        self.learning_history.append(event_dict)

        # Save learning data
        self._save_learning_data()

        logger.info(f"Learned from story development in {story_id}")
        return learning_event

    def learn_from_emotional_response(
        self,
        emotion_type: str,
        response_content: str,
        intensity: float = 0.5,
        character_name: Optional[str] = None,
    ) -> LearningEvent:
        """
        Learn from an emotional response

        Args:
            emotion_type: Type of emotion (joy, anger, fear, etc.)
            response_content: Content describing the emotional response
            intensity: Intensity of the emotional response (0.0 to 1.0)
            character_name: Optional character name if related to a character

        Returns:
            LearningEvent object tracking the learning
        """
        event_id = f"emotion_{len(self.learning_history)}"

        # Analyze emotional response for personality changes
        personality_changes = self._analyze_emotion_for_changes(
            emotion_type, response_content, intensity
        )

        # Create learning event
        learning_event = LearningEvent(
            event_id=event_id,
            learning_type=LearningType.EMOTIONAL_RESPONSE,
            trigger=LearningTrigger.EMOTIONAL_EVENT,
            content=response_content,
            character_name=character_name,
            emotional_intensity=intensity,
            personality_changes=personality_changes,
            timestamp=datetime.now().isoformat(),
            context={"emotion_type": emotion_type},
        )

        # Add to learning history (convert enum to string for JSON serialization)
        event_dict = asdict(learning_event)
        event_dict["learning_type"] = learning_event.learning_type.value
        event_dict["trigger"] = learning_event.trigger.value
        self.learning_history.append(event_dict)

        # Save learning data
        self._save_learning_data()

        logger.info(f"Learned from emotional response: {emotion_type}")
        return learning_event

    def _analyze_interaction_for_changes(
        self, interaction_content: str, emotional_intensity: float
    ) -> Dict[str, float]:
        """Analyze character interaction for personality changes"""
        changes = {}

        # Analyze for empathy development
        empathy_matches = re.findall(
            r"feel\s+for|understand|compassion|empathy",
            interaction_content,
            re.IGNORECASE,
        )
        if empathy_matches:
            changes["empathy"] = len(empathy_matches) * 0.1 * emotional_intensity

        # Analyze for social skills
        social_matches = re.findall(
            r"communicate|connect|relate|bond", interaction_content, re.IGNORECASE
        )
        if social_matches:
            changes["social_skills"] = len(social_matches) * 0.1 * emotional_intensity

        # Analyze for emotional intelligence
        emotional_matches = re.findall(
            r"emotion|feeling|mood|sentiment", interaction_content, re.IGNORECASE
        )
        if emotional_matches:
            changes["emotional_intelligence"] = (
                len(emotional_matches) * 0.1 * emotional_intensity
            )

        # Analyze for conflict resolution
        conflict_matches = re.findall(
            r"resolve|conflict|dispute|agreement", interaction_content, re.IGNORECASE
        )
        if conflict_matches:
            changes["conflict_resolution"] = (
                len(conflict_matches) * 0.1 * emotional_intensity
            )

        return changes

    def _analyze_story_for_changes(
        self, story_content: str, current_arc: str
    ) -> Dict[str, float]:
        """Analyze story development for personality changes"""
        changes = {}

        # Analyze for character development
        development_matches = re.findall(
            r"grow|evolve|change|develop|transform", story_content, re.IGNORECASE
        )
        if development_matches:
            changes["character_development"] = len(development_matches) * 0.1

        # Analyze for plot understanding
        plot_matches = re.findall(
            r"plot|story|narrative|arc|journey", story_content, re.IGNORECASE
        )
        if plot_matches:
            changes["plot_understanding"] = len(plot_matches) * 0.1

        # Analyze for thematic awareness
        theme_matches = re.findall(
            r"theme|meaning|symbol|metaphor|allegory", story_content, re.IGNORECASE
        )
        if theme_matches:
            changes["thematic_awareness"] = len(theme_matches) * 0.1

        # Analyze for creative adaptation
        creative_matches = re.findall(
            r"creative|imaginative|innovative|original", story_content, re.IGNORECASE
        )
        if creative_matches:
            changes["creative_adaptation"] = len(creative_matches) * 0.1

        return changes

    def _analyze_emotion_for_changes(
        self, emotion_type: str, response_content: str, intensity: float
    ) -> Dict[str, float]:
        """Analyze emotional response for personality changes"""
        changes = {}

        # Base emotional trait development
        changes[f"{emotion_type}_sensitivity"] = intensity * 0.2

        # Analyze for emotional regulation
        regulation_matches = re.findall(
            r"control|manage|regulate|balance", response_content, re.IGNORECASE
        )
        if regulation_matches:
            changes["emotional_regulation"] = len(regulation_matches) * 0.1 * intensity

        # Analyze for emotional expression
        expression_matches = re.findall(
            r"express|show|display|demonstrate", response_content, re.IGNORECASE
        )
        if expression_matches:
            changes["emotional_expression"] = len(expression_matches) * 0.1 * intensity

        # Analyze for emotional understanding
        understanding_matches = re.findall(
            r"understand|comprehend|realize|recognize", response_content, re.IGNORECASE
        )
        if understanding_matches:
            changes["emotional_understanding"] = (
                len(understanding_matches) * 0.1 * intensity
            )

        return changes

    def _calculate_story_emotional_intensity(self, story_content: str) -> float:
        """Calculate emotional intensity from story content"""
        emotional_words = [
            "intense",
            "powerful",
            "dramatic",
            "emotional",
            "passionate",
            "fierce",
            "overwhelming",
            "profound",
            "deep",
            "strong",
        ]

        intensity = 0.0
        for word in emotional_words:
            matches = re.findall(word, story_content, re.IGNORECASE)
            intensity += len(matches) * 0.1

        return min(intensity, 1.0)

    def _update_character_profile(
        self, character_name: str, learning_event: LearningEvent
    ):
        """Update character learning profile"""
        if character_name not in self.character_profiles:
            self.character_profiles[character_name] = {
                "character_name": character_name,
                "learning_history": [],
                "personality_evolution": {},
                "relationship_dynamics": {},
                "story_arc_participation": [],
                "emotional_patterns": {},
            }

        profile = self.character_profiles[character_name]

        # Add learning event to history (convert enum to string for JSON serialization)
        event_dict = asdict(learning_event)
        event_dict["learning_type"] = learning_event.learning_type.value
        event_dict["trigger"] = learning_event.trigger.value
        profile["learning_history"].append(event_dict)

        # Update personality evolution
        for trait, change in learning_event.personality_changes.items():
            if trait not in profile["personality_evolution"]:
                profile["personality_evolution"][trait] = []
            profile["personality_evolution"][trait].append(change)

        # Update emotional patterns
        if learning_event.emotional_intensity > 0:
            emotion_type = learning_event.context.get("emotion_type", "general")
            if emotion_type not in profile["emotional_patterns"]:
                profile["emotional_patterns"][emotion_type] = 0.0
            profile["emotional_patterns"][
                emotion_type
            ] += learning_event.emotional_intensity

    def _update_story_context(
        self, story_id: str, current_arc: str, learning_event: LearningEvent
    ):
        """Update story learning context"""
        if story_id not in self.story_contexts:
            self.story_contexts[story_id] = {
                "story_id": story_id,
                "current_arc": current_arc,
                "character_roles": {},
                "plot_developments": [],
                "emotional_climax": None,
                "resolution_status": "ongoing",
            }

        context = self.story_contexts[story_id]

        # Update plot developments
        if learning_event.content:
            context["plot_developments"].append(learning_event.content[:100] + "...")

        # Update emotional climax if intensity is high
        if learning_event.emotional_intensity > 0.8:
            context["emotional_climax"] = learning_event.content[:100] + "..."

    def get_character_learning_summary(self, character_name: str) -> str:
        """Get a summary of character learning"""
        if character_name not in self.character_profiles:
            return f"No learning data available for {character_name}"

        profile = self.character_profiles[character_name]

        summary_parts = []
        summary_parts.append(f"Learning Summary for {character_name}:")

        # Learning events count
        summary_parts.append(
            f"- Total learning events: {len(profile['learning_history'])}"
        )

        # Personality evolution
        if profile["personality_evolution"]:
            summary_parts.append("- Personality evolution:")
            for trait, changes in profile["personality_evolution"].items():
                total_change = sum(changes)
                summary_parts.append(f"  * {trait}: +{total_change:.2f}")

        # Emotional patterns
        if profile["emotional_patterns"]:
            summary_parts.append("- Emotional patterns:")
            for emotion, intensity in profile["emotional_patterns"].items():
                summary_parts.append(f"  * {emotion}: {intensity:.2f}")

        return "\n".join(summary_parts)

    def get_story_learning_summary(self, story_id: str) -> str:
        """Get a summary of story learning"""
        if story_id not in self.story_contexts:
            return f"No learning data available for story {story_id}"

        context = self.story_contexts[story_id]

        summary_parts = []
        summary_parts.append(f"Story Learning Summary for {story_id}:")
        summary_parts.append(f"- Current arc: {context['current_arc']}")
        summary_parts.append(
            f"- Plot developments: {len(context['plot_developments'])}"
        )
        summary_parts.append(f"- Resolution status: {context['resolution_status']}")

        if context["emotional_climax"]:
            summary_parts.append(f"- Emotional climax: {context['emotional_climax']}")

        return "\n".join(summary_parts)

    def get_learning_patterns(self) -> Dict[str, Any]:
        """Get patterns in learning behavior"""
        patterns = {
            "total_learning_events": len(self.learning_history),
            "character_interactions": len(
                [
                    e
                    for e in self.learning_history
                    if e.get("learning_type") == "character_interaction"
                ]
            ),
            "story_developments": len(
                [
                    e
                    for e in self.learning_history
                    if e.get("learning_type") == "story_development"
                ]
            ),
            "emotional_responses": len(
                [
                    e
                    for e in self.learning_history
                    if e.get("learning_type") == "emotional_response"
                ]
            ),
            "characters_learned_from": list(self.character_profiles.keys()),
            "stories_learned_from": list(self.story_contexts.keys()),
        }

        return patterns

    def reset_learning_data(self):
        """Reset all learning data"""
        self.learning_history = []
        self.character_profiles = {}
        self.story_contexts = {}
        self.learning_patterns = {}
        self._save_learning_data()
        logger.info("Learning data reset")

    def _process_item(self, item):
        """Process queue items for dynamic personality learning operations"""
        try:
            # Extract operation type from data
            operation_type = item.data.get("type", "unknown")
            
            if operation_type == "learn_from_character_interaction":
                return self._handle_learn_from_character_interaction(item.data)
            elif operation_type == "learn_from_story_development":
                return self._handle_learn_from_story_development(item.data)
            elif operation_type == "learn_from_emotional_response":
                return self._handle_learn_from_emotional_response(item.data)
            elif operation_type == "get_character_learning_summary":
                return self._handle_get_character_learning_summary(item.data)
            elif operation_type == "get_story_learning_summary":
                return self._handle_get_story_learning_summary(item.data)
            elif operation_type == "get_learning_patterns":
                return self._handle_get_learning_patterns(item.data)
            elif operation_type == "reset_learning_data":
                return self._handle_reset_learning_data(item.data)
            else:
                # Pass unknown types to base class
                return super()._process_item(item)
        except Exception as e:
            logger.error(f"Error processing dynamic personality learning queue item: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_learn_from_character_interaction(self, data):
        """Handle character interaction learning requests"""
        try:
            character_name = data.get("character_name", "")
            interaction_content = data.get("interaction_content", "")
            emotional_intensity = data.get("emotional_intensity", 0.5)
            context = data.get("context", {})
            
            if character_name and interaction_content:
                learning_event = self.learn_from_character_interaction(
                    character_name, interaction_content, emotional_intensity, context
                )
                return {
                    "status": "success",
                    "learning_event": learning_event,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name or interaction_content", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in learn from character interaction: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_learn_from_story_development(self, data):
        """Handle story development learning requests"""
        try:
            story_id = data.get("story_id", "")
            story_content = data.get("story_content", "")
            current_arc = data.get("current_arc", "main")
            context = data.get("context", {})
            
            if story_id and story_content:
                learning_event = self.learn_from_story_development(
                    story_id, story_content, current_arc, context
                )
                return {
                    "status": "success",
                    "learning_event": learning_event,
                    "story_id": story_id
                }
            else:
                return {"error": "Missing story_id or story_content", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in learn from story development: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_learn_from_emotional_response(self, data):
        """Handle emotional response learning requests"""
        try:
            emotion_type = data.get("emotion_type", "")
            response_content = data.get("response_content", "")
            intensity = data.get("intensity", 0.5)
            character_name = data.get("character_name")
            
            if emotion_type and response_content:
                learning_event = self.learn_from_emotional_response(
                    emotion_type, response_content, intensity, character_name
                )
                return {
                    "status": "success",
                    "learning_event": learning_event,
                    "emotion_type": emotion_type
                }
            else:
                return {"error": "Missing emotion_type or response_content", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in learn from emotional response: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_character_learning_summary(self, data):
        """Handle get character learning summary requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                summary = self.get_character_learning_summary(character_name)
                return {
                    "status": "success",
                    "summary": summary,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get character learning summary: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_story_learning_summary(self, data):
        """Handle get story learning summary requests"""
        try:
            story_id = data.get("story_id", "")
            if story_id:
                summary = self.get_story_learning_summary(story_id)
                return {
                    "status": "success",
                    "summary": summary,
                    "story_id": story_id
                }
            else:
                return {"error": "Missing story_id", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get story learning summary: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_learning_patterns(self, data):
        """Handle get learning patterns requests"""
        try:
            patterns = self.get_learning_patterns()
            return {
                "status": "success",
                "patterns": patterns
            }
        except Exception as e:
            logger.error(f"Error in get learning patterns: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_reset_learning_data(self, data):
        """Handle reset learning data requests"""
        try:
            self.reset_learning_data()
            return {
                "status": "success",
                "message": "Learning data reset successfully"
            }
        except Exception as e:
            logger.error(f"Error in reset learning data: {e}")
            return {"error": str(e), "status": "failed"}


def initialize(framework=None):
    """Initialize the Dynamic Personality Learning System"""
    return DynamicPersonalityLearning()
