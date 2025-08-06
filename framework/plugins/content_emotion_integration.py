#!/usr/bin/env python3
"""
Content-Emotion Integration System
Integrates emotional system with content processing for character-driven emotional responses
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


class EmotionType(Enum):
    """Types of emotions that can be processed"""

    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    LOVE = "love"
    HATE = "hate"
    HOPE = "hope"
    DESPAIR = "despair"
    EXCITEMENT = "excitement"
    CALM = "calm"
    ANXIETY = "anxiety"
    CONFIDENCE = "confidence"
    VULNERABILITY = "vulnerability"


class EmotionTrigger(Enum):
    """Triggers that can cause emotional responses"""

    CHARACTER_INTERACTION = "character_interaction"
    STORY_EVENT = "story_event"
    MEMORY_RECALL = "memory_recall"
    ENVIRONMENTAL_FACTOR = "environmental_factor"
    PERSONAL_REFLECTION = "personal_reflection"
    CONFLICT_SITUATION = "conflict_situation"


@dataclass
class EmotionalResponse:
    """Represents an emotional response to content"""

    response_id: str
    emotion_type: EmotionType
    intensity: float  # 0.0 to 1.0
    trigger: EmotionTrigger
    content_context: str
    character_name: Optional[str]
    response_text: str
    timestamp: str
    context: Dict[str, Any]


@dataclass
class CharacterEmotionalProfile:
    """Emotional profile for a specific character"""

    character_name: str
    emotional_history: List[EmotionalResponse]
    emotional_patterns: Dict[str, float]
    emotional_triggers: Dict[str, List[str]]
    emotional_stability: float
    dominant_emotions: List[str]


@dataclass
class ContentEmotionalAnalysis:
    """Analysis of emotional content in text"""

    content_id: str
    detected_emotions: List[EmotionType]
    emotional_intensity: float
    emotional_triggers: List[EmotionTrigger]
    character_emotional_impact: Dict[str, float]
    emotional_summary: str


class ContentEmotionIntegration:
    """
    Content-Emotion Integration System
    Integrates emotional processing with content analysis for character-driven responses
    """

    def __init__(self):
        self.config = Config()
        # Use the current file's location to determine project root
        project_root = Path(__file__).parent.parent.parent
        self.emotion_data_dir = project_root / "models" / "emotion"
        self.emotion_data_dir.mkdir(parents=True, exist_ok=True)

        self.emotional_responses = []
        self.character_emotional_profiles = {}
        self.content_emotional_cache = {}

        # Load existing emotion data
        self._load_emotion_data()

    def _load_emotion_data(self):
        """Load existing emotion data from disk"""
        emotion_file = self.emotion_data_dir / "emotion_data.json"
        if emotion_file.exists():
            try:
                with open(emotion_file, "r") as f:
                    data = json.load(f)
                    self.emotional_responses = data.get("emotional_responses", [])
                    self.character_emotional_profiles = data.get(
                        "character_emotional_profiles", {}
                    )
                    self.content_emotional_cache = data.get(
                        "content_emotional_cache", {}
                    )
                logger.info("Loaded existing emotion data")
            except Exception as e:
                logger.error(f"Error loading emotion data: {e}")

    def _save_emotion_data(self):
        """Save current emotion data to disk"""
        emotion_file = self.emotion_data_dir / "emotion_data.json"
        try:
            # Convert enum values to strings for JSON serialization
            serializable_responses = []
            for response in self.emotional_responses:
                if isinstance(response, dict):
                    # Already a dict, just ensure enum values are strings
                    response_copy = response.copy()
                    if "emotion_type" in response_copy and hasattr(
                        response_copy["emotion_type"], "value"
                    ):
                        response_copy["emotion_type"] = response_copy[
                            "emotion_type"
                        ].value
                    if "trigger" in response_copy and hasattr(
                        response_copy["trigger"], "value"
                    ):
                        response_copy["trigger"] = response_copy["trigger"].value
                    serializable_responses.append(response_copy)
                else:
                    # Convert dataclass to dict with string enum values
                    response_dict = asdict(response)
                    response_dict["emotion_type"] = response.emotion_type.value
                    response_dict["trigger"] = response.trigger.value
                    serializable_responses.append(response_dict)

            data = {
                "emotional_responses": serializable_responses,
                "character_emotional_profiles": self.character_emotional_profiles,
                "content_emotional_cache": self.content_emotional_cache,
            }
            with open(emotion_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved emotion data")
        except Exception as e:
            logger.error(f"Error saving emotion data: {e}")

    def analyze_content_for_emotions(
        self, content: str, content_id: str = None
    ) -> ContentEmotionalAnalysis:
        """
        Analyze content for emotional content

        Args:
            content: The content to analyze
            content_id: Unique identifier for the content

        Returns:
            ContentEmotionalAnalysis object with emotional insights
        """
        if content_id is None:
            content_id = f"content_{len(self.content_emotional_cache)}"

        # Check cache first
        if content_id in self.content_emotional_cache:
            cached_data = self.content_emotional_cache[content_id]
            # Convert cached dict back to ContentEmotionalAnalysis object
            if isinstance(cached_data, dict):
                return ContentEmotionalAnalysis(
                    content_id=cached_data["content_id"],
                    detected_emotions=[
                        EmotionType(emotion)
                        for emotion in cached_data["detected_emotions"]
                    ],
                    emotional_intensity=cached_data["emotional_intensity"],
                    emotional_triggers=[
                        EmotionTrigger(trigger)
                        for trigger in cached_data["emotional_triggers"]
                    ],
                    character_emotional_impact=cached_data[
                        "character_emotional_impact"
                    ],
                    emotional_summary=cached_data["emotional_summary"],
                )
            return cached_data

        # Detect emotions in content
        detected_emotions = self._detect_emotions_in_content(content)

        # Calculate emotional intensity
        emotional_intensity = self._calculate_emotional_intensity(content)

        # Identify emotional triggers
        emotional_triggers = self._identify_emotional_triggers(content)

        # Analyze character emotional impact
        character_emotional_impact = self._analyze_character_emotional_impact(content)

        # Generate emotional summary
        emotional_summary = self._generate_emotional_summary(
            detected_emotions, emotional_intensity
        )

        analysis = ContentEmotionalAnalysis(
            content_id=content_id,
            detected_emotions=detected_emotions,
            emotional_intensity=emotional_intensity,
            emotional_triggers=emotional_triggers,
            character_emotional_impact=character_emotional_impact,
            emotional_summary=emotional_summary,
        )

        # Cache the result (convert to dict for JSON serialization)
        analysis_dict = {
            "content_id": analysis.content_id,
            "detected_emotions": [
                emotion.value for emotion in analysis.detected_emotions
            ],
            "emotional_intensity": analysis.emotional_intensity,
            "emotional_triggers": [
                trigger.value for trigger in analysis.emotional_triggers
            ],
            "character_emotional_impact": analysis.character_emotional_impact,
            "emotional_summary": analysis.emotional_summary,
        }
        self.content_emotional_cache[content_id] = analysis_dict

        return analysis

    def generate_character_emotional_response(
        self, character_name: str, content: str, context: Dict[str, Any] = None
    ) -> EmotionalResponse:
        """
        Generate an emotional response for a character based on content

        Args:
            character_name: Name of the character
            content: Content that triggers the emotional response
            context: Additional context for the response

        Returns:
            EmotionalResponse object
        """
        response_id = f"emotion_{len(self.emotional_responses)}"

        # Analyze content for emotions
        content_analysis = self.analyze_content_for_emotions(content)

        # Determine character's emotional response
        emotion_type = self._determine_character_emotion(
            character_name, content_analysis
        )
        intensity = self._calculate_character_emotion_intensity(
            character_name, content_analysis
        )
        trigger = self._identify_emotion_trigger(content_analysis)

        # Generate response text
        response_text = self._generate_emotional_response_text(
            character_name, emotion_type, intensity, content
        )

        # Create emotional response
        emotional_response = EmotionalResponse(
            response_id=response_id,
            emotion_type=emotion_type,
            intensity=intensity,
            trigger=trigger,
            content_context=content[:200] + "..." if len(content) > 200 else content,
            character_name=character_name,
            response_text=response_text,
            timestamp=datetime.now().isoformat(),
            context=context or {},
        )

        # Update character emotional profile
        self._update_character_emotional_profile(character_name, emotional_response)

        # Add to emotional responses
        response_dict = asdict(emotional_response)
        response_dict["emotion_type"] = emotional_response.emotion_type.value
        response_dict["trigger"] = emotional_response.trigger.value
        self.emotional_responses.append(response_dict)

        # Save emotion data
        self._save_emotion_data()

        logger.info(
            f"Generated emotional response for {character_name}: {emotion_type.value}"
        )
        return emotional_response

    def _detect_emotions_in_content(self, content: str) -> List[EmotionType]:
        """Detect emotions present in content"""
        emotions = []

        # Emotion detection patterns
        emotion_patterns = {
            EmotionType.JOY: [
                r"joy",
                r"happy",
                r"elated",
                r"ecstatic",
                r"pleased",
                r"delighted",
            ],
            EmotionType.SADNESS: [
                r"sad",
                r"melancholy",
                r"grief",
                r"sorrow",
                r"depressed",
                r"heartbroken",
            ],
            EmotionType.ANGER: [
                r"angry",
                r"rage",
                r"fury",
                r"wrath",
                r"irritated",
                r"furious",
            ],
            EmotionType.FEAR: [
                r"afraid",
                r"terrified",
                r"fear",
                r"dread",
                r"panic",
                r"anxious",
            ],
            EmotionType.SURPRISE: [
                r"surprised",
                r"astonished",
                r"amazed",
                r"stunned",
                r"shocked",
            ],
            EmotionType.DISGUST: [r"disgusted", r"repulsed", r"revolted", r"appalled"],
            EmotionType.LOVE: [
                r"love",
                r"cherish",
                r"adore",
                r"devotion",
                r"affection",
            ],
            EmotionType.HATE: [r"hate", r"loathe", r"despise", r"abhor", r"detest"],
            EmotionType.HOPE: [
                r"hope",
                r"optimistic",
                r"faith",
                r"belief",
                r"aspiration",
            ],
            EmotionType.DESPAIR: [r"despair", r"hopeless", r"desperate", r"forlorn"],
            EmotionType.EXCITEMENT: [
                r"excited",
                r"thrilled",
                r"enthusiastic",
                r"eager",
            ],
            EmotionType.CALM: [
                r"calm",
                r"peaceful",
                r"serene",
                r"tranquil",
                r"relaxed",
            ],
            EmotionType.ANXIETY: [
                r"anxious",
                r"worried",
                r"nervous",
                r"tense",
                r"stressed",
            ],
            EmotionType.CONFIDENCE: [
                r"confident",
                r"assured",
                r"certain",
                r"bold",
                r"brave",
            ],
            EmotionType.VULNERABILITY: [
                r"vulnerable",
                r"exposed",
                r"defenseless",
                r"helpless",
            ],
        }

        for emotion_type, patterns in emotion_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    emotions.append(emotion_type)
                    break

        return emotions

    def _calculate_emotional_intensity(self, content: str) -> float:
        """Calculate the overall emotional intensity of content"""
        intensity_words = [
            "intense",
            "powerful",
            "overwhelming",
            "profound",
            "deep",
            "strong",
            "fierce",
            "passionate",
            "dramatic",
            "emotional",
        ]

        intensity = 0.0
        for word in intensity_words:
            matches = re.findall(word, content, re.IGNORECASE)
            intensity += len(matches) * 0.1

        return min(intensity, 1.0)

    def _identify_emotional_triggers(self, content: str) -> List[EmotionTrigger]:
        """Identify emotional triggers in content"""
        triggers = []

        # Trigger patterns
        trigger_patterns = {
            EmotionTrigger.CHARACTER_INTERACTION: [
                r"interact",
                r"conversation",
                r"dialogue",
                r"speak",
            ],
            EmotionTrigger.STORY_EVENT: [
                r"event",
                r"happened",
                r"occurred",
                r"took place",
            ],
            EmotionTrigger.MEMORY_RECALL: [
                r"remember",
                r"recall",
                r"memory",
                r"thought of",
            ],
            EmotionTrigger.ENVIRONMENTAL_FACTOR: [
                r"weather",
                r"surroundings",
                r"environment",
                r"atmosphere",
            ],
            EmotionTrigger.PERSONAL_REFLECTION: [
                r"reflect",
                r"think",
                r"consider",
                r"contemplate",
            ],
            EmotionTrigger.CONFLICT_SITUATION: [
                r"conflict",
                r"dispute",
                r"argument",
                r"fight",
            ],
        }

        for trigger_type, patterns in trigger_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    triggers.append(trigger_type)
                    break

        return triggers

    def _analyze_character_emotional_impact(self, content: str) -> Dict[str, float]:
        """Analyze how content might impact different characters emotionally"""
        # This is a simplified analysis - in a real system, this would be more sophisticated
        impact = {}

        # Look for character names and emotional content
        character_names = re.findall(r"\b[A-Z][a-z]+\b", content)
        emotions = self._detect_emotions_in_content(content)

        for name in character_names:
            if name in ["Shay", "Nyx", "Luna"]:  # Known characters
                impact[name] = len(emotions) * 0.1

        return impact

    def _generate_emotional_summary(
        self, emotions: List[EmotionType], intensity: float
    ) -> str:
        """Generate a summary of emotional content"""
        if not emotions:
            return "No strong emotions detected in content."

        emotion_names = [emotion.value for emotion in emotions]
        summary = f"Detected emotions: {', '.join(emotion_names)}. "
        summary += f"Emotional intensity: {intensity:.2f}"

        return summary

    def _determine_character_emotion(
        self, character_name: str, content_analysis: ContentEmotionalAnalysis
    ) -> EmotionType:
        """Determine what emotion a character would feel based on content analysis"""
        # Get character's emotional profile
        profile = self.character_emotional_profiles.get(character_name, {})

        # If no profile exists, use the most common emotion in content
        if not profile or not content_analysis.detected_emotions:
            return EmotionType.CALM  # Default emotion

        # Consider character's emotional patterns and content emotions
        detected_emotions = content_analysis.detected_emotions
        if detected_emotions:
            # Return the first detected emotion (simplified logic)
            return detected_emotions[0]

        return EmotionType.CALM

    def _calculate_character_emotion_intensity(
        self, character_name: str, content_analysis: ContentEmotionalAnalysis
    ) -> float:
        """Calculate the intensity of a character's emotional response"""
        # Base intensity on content analysis
        base_intensity = content_analysis.emotional_intensity

        # Adjust based on character's emotional profile
        profile = self.character_emotional_profiles.get(character_name, {})
        if profile and "emotional_stability" in profile:
            stability = profile["emotional_stability"]
            # More stable characters have more moderate responses
            adjusted_intensity = base_intensity * (0.5 + stability * 0.5)
            return min(adjusted_intensity, 1.0)

        return base_intensity

    def _identify_emotion_trigger(
        self, content_analysis: ContentEmotionalAnalysis
    ) -> EmotionTrigger:
        """Identify what triggered the emotional response"""
        if content_analysis.emotional_triggers:
            return content_analysis.emotional_triggers[0]

        return EmotionTrigger.STORY_EVENT  # Default trigger

    def _generate_emotional_response_text(
        self,
        character_name: str,
        emotion_type: EmotionType,
        intensity: float,
        content: str,
    ) -> str:
        """Generate text describing the character's emotional response"""
        emotion_name = emotion_type.value

        if intensity > 0.8:
            intensity_desc = "overwhelming"
        elif intensity > 0.6:
            intensity_desc = "strong"
        elif intensity > 0.4:
            intensity_desc = "moderate"
        else:
            intensity_desc = "mild"

        response = f"{character_name} feels a {intensity_desc} sense of {emotion_name}."

        # Add context-specific details
        if "conflict" in content.lower():
            response += f" The situation has deeply affected {character_name}."
        elif "memory" in content.lower():
            response += f" This brings back powerful memories for {character_name}."

        return response

    def _update_character_emotional_profile(
        self, character_name: str, emotional_response: EmotionalResponse
    ):
        """Update a character's emotional profile"""
        if character_name not in self.character_emotional_profiles:
            self.character_emotional_profiles[character_name] = {
                "character_name": character_name,
                "emotional_history": [],
                "emotional_patterns": {},
                "emotional_triggers": {},
                "emotional_stability": 0.5,  # Default stability
                "dominant_emotions": [],
            }

        profile = self.character_emotional_profiles[character_name]

        # Add emotional response to history
        response_dict = asdict(emotional_response)
        response_dict["emotion_type"] = emotional_response.emotion_type.value
        response_dict["trigger"] = emotional_response.trigger.value
        profile["emotional_history"].append(response_dict)

        # Update emotional patterns
        emotion_name = emotional_response.emotion_type.value
        if emotion_name not in profile["emotional_patterns"]:
            profile["emotional_patterns"][emotion_name] = 0.0
        profile["emotional_patterns"][emotion_name] += emotional_response.intensity

        # Update emotional triggers
        trigger_name = emotional_response.trigger.value
        if trigger_name not in profile["emotional_triggers"]:
            profile["emotional_triggers"][trigger_name] = []
        profile["emotional_triggers"][trigger_name].append(emotion_name)

        # Update dominant emotions
        sorted_emotions = sorted(
            profile["emotional_patterns"].items(), key=lambda x: x[1], reverse=True
        )
        profile["dominant_emotions"] = [emotion for emotion, _ in sorted_emotions[:3]]

    def get_character_emotional_summary(self, character_name: str) -> str:
        """Get a summary of a character's emotional profile"""
        if character_name not in self.character_emotional_profiles:
            return f"No emotional data available for {character_name}"

        profile = self.character_emotional_profiles[character_name]

        summary_parts = []
        summary_parts.append(f"Emotional Summary for {character_name}:")
        summary_parts.append(
            f"- Total emotional responses: {len(profile['emotional_history'])}"
        )
        summary_parts.append(
            f"- Emotional stability: {profile['emotional_stability']:.2f}"
        )

        if profile["dominant_emotions"]:
            summary_parts.append(
                f"- Dominant emotions: {', '.join(profile['dominant_emotions'])}"
            )

        if profile["emotional_patterns"]:
            summary_parts.append("- Emotional patterns:")
            for emotion, intensity in profile["emotional_patterns"].items():
                summary_parts.append(f"  * {emotion}: {intensity:.2f}")

        return "\n".join(summary_parts)

    def get_emotional_analysis_summary(self) -> Dict[str, Any]:
        """Get a summary of all emotional analysis data"""
        summary = {
            "total_emotional_responses": len(self.emotional_responses),
            "characters_with_emotional_profiles": list(
                self.character_emotional_profiles.keys()
            ),
            "content_analyses_performed": len(self.content_emotional_cache),
            "most_common_emotions": self._get_most_common_emotions(),
            "emotional_intensity_distribution": self._get_emotional_intensity_distribution(),
        }

        return summary

    def _get_most_common_emotions(self) -> List[str]:
        """Get the most common emotions across all responses"""
        emotion_counts = {}

        for response in self.emotional_responses:
            emotion = response.get("emotion_type", "unknown")
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        sorted_emotions = sorted(
            emotion_counts.items(), key=lambda x: x[1], reverse=True
        )
        return [emotion for emotion, _ in sorted_emotions[:5]]

    def _get_emotional_intensity_distribution(self) -> Dict[str, int]:
        """Get distribution of emotional intensities"""
        distribution = {"low": 0, "medium": 0, "high": 0}

        for response in self.emotional_responses:
            intensity = response.get("intensity", 0.0)
            if intensity < 0.33:
                distribution["low"] += 1
            elif intensity < 0.67:
                distribution["medium"] += 1
            else:
                distribution["high"] += 1

        return distribution

    def reset_emotion_data(self):
        """Reset all emotion data"""
        self.emotional_responses = []
        self.character_emotional_profiles = {}
        self.content_emotional_cache = {}
        self._save_emotion_data()
        logger.info("Emotion data reset")


def initialize(framework=None):
    """Initialize the Content-Emotion Integration System"""
    return ContentEmotionIntegration()
