#!/usr/bin/env python3
"""
Enhanced Emotional Blender
Provides psychologically realistic emotion blending and analysis
"""

import json
import random
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Add framework to path
framework_dir = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_dir))

from queue_manager import QueueProcessor

logger = logging.getLogger(__name__)


class PlutchikEmotion(Enum):
    """Plutchik's 8 primary emotions with their opposites and intensities"""

    JOY = "joy"
    TRUST = "trust"
    FEAR = "fear"
    SURPRISE = "surprise"
    SADNESS = "sadness"
    DISGUST = "disgust"
    ANGER = "anger"
    ANTICIPATION = "anticipation"


class MaslowLevel(Enum):
    """Maslow's hierarchy of needs levels"""

    PHYSIOLOGICAL = "physiological"
    SAFETY = "safety"
    LOVE_BELONGING = "love_belonging"
    ESTEEM = "esteem"
    SELF_ACTUALIZATION = "self_actualization"


class EnhancedEmotionalBlender(QueueProcessor):
    """
    Enhanced Emotional Blender
    Provides psychologically realistic emotion blending and analysis
    """

    def __init__(self):
        super().__init__("enhanced_emotional_blender")
        self.plutchik_wheel = self._initialize_plutchik_wheel()
        self.maslow_hierarchy = self._initialize_maslow_hierarchy()
        self.intensity_levels = self._initialize_intensity_levels()
        self.fragments = {}

        # Load emotional fragments
        self.load_fragments()

    def _process_item(self, item):
        """Process queue items for enhanced emotional blender operations"""
        try:
            # Extract operation type from data
            operation_type = item.data.get("type", "unknown")

            if operation_type == "blend_emotions_with_psychology":
                return self._handle_blend_emotions_with_psychology(item.data)
            elif operation_type == "create_psychologically_realistic_emotion":
                return self._handle_create_psychologically_realistic_emotion(item.data)
            elif operation_type == "suggest_psychologically_realistic_combinations":
                return self._handle_suggest_psychologically_realistic_combinations(
                    item.data
                )
            elif operation_type == "get_emotion_by_psychological_profile":
                return self._handle_get_emotion_by_psychological_profile(item.data)
            elif operation_type == "analyze_plutchik_emotion":
                return self._handle_analyze_plutchik_emotion(item.data)
            elif operation_type == "analyze_maslow_needs":
                return self._handle_analyze_maslow_needs(item.data)
            elif operation_type == "calculate_emotional_intensity":
                return self._handle_calculate_emotional_intensity(item.data)
            else:
                # Pass unknown types to base class
                return super()._process_item(item)
        except Exception as e:
            logger.error(f"Error processing enhanced emotional blender queue item: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_blend_emotions_with_psychology(self, data):
        """Handle blend emotions with psychology requests"""
        try:
            primary_emotion = data.get("primary_emotion", "")
            secondary_emotions = data.get("secondary_emotions", [])
            blend_ratio = data.get("blend_ratio", 0.7)
            context = data.get("context", {})

            if primary_emotion:
                result = self.blend_emotions_with_psychology(
                    primary_emotion, secondary_emotions, blend_ratio, context
                )
                return {
                    "status": "success",
                    "result": result,
                    "primary_emotion": primary_emotion,
                }
            else:
                return {"error": "Missing primary_emotion", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in blend emotions with psychology: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_create_psychologically_realistic_emotion(self, data):
        """Handle create psychologically realistic emotion requests"""
        try:
            emotions = data.get("emotions", [])
            weights = data.get("weights", [])
            context = data.get("context", {})

            if emotions:
                result = self.create_psychologically_realistic_emotion(
                    emotions, weights, context
                )
                return {"status": "success", "result": result, "emotions": emotions}
            else:
                return {"error": "Missing emotions", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in create psychologically realistic emotion: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_suggest_psychologically_realistic_combinations(self, data):
        """Handle suggest psychologically realistic combinations requests"""
        try:
            combinations = self.suggest_psychologically_realistic_combinations()
            return {"status": "success", "combinations": combinations}
        except Exception as e:
            logger.error(
                f"Error in suggest psychologically realistic combinations: {e}"
            )
            return {"error": str(e), "status": "failed"}

    def _handle_get_emotion_by_psychological_profile(self, data):
        """Handle get emotion by psychological profile requests"""
        try:
            plutchik_emotion = data.get("plutchik_emotion", "")
            maslow_level = data.get("maslow_level", "")
            intensity_level = data.get("intensity_level", "")

            emotions = self.get_emotion_by_psychological_profile(
                plutchik_emotion, maslow_level, intensity_level
            )
            return {
                "status": "success",
                "emotions": emotions,
                "plutchik_emotion": plutchik_emotion,
                "maslow_level": maslow_level,
                "intensity_level": intensity_level,
            }
        except Exception as e:
            logger.error(f"Error in get emotion by psychological profile: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_analyze_plutchik_emotion(self, data):
        """Handle analyze plutchik emotion requests"""
        try:
            emotion_name = data.get("emotion_name", "")
            if emotion_name:
                analysis = self.analyze_plutchik_emotion(emotion_name)
                return {
                    "status": "success",
                    "analysis": analysis,
                    "emotion_name": emotion_name,
                }
            else:
                return {"error": "Missing emotion_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in analyze plutchik emotion: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_analyze_maslow_needs(self, data):
        """Handle analyze maslow needs requests"""
        try:
            emotion_name = data.get("emotion_name", "")
            if emotion_name:
                analysis = self.analyze_maslow_needs(emotion_name)
                return {
                    "status": "success",
                    "analysis": analysis,
                    "emotion_name": emotion_name,
                }
            else:
                return {"error": "Missing emotion_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in analyze maslow needs: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_calculate_emotional_intensity(self, data):
        """Handle calculate emotional intensity requests"""
        try:
            emotion_name = data.get("emotion_name", "")
            context = data.get("context", {})

            if emotion_name:
                intensity = self.calculate_emotional_intensity(emotion_name, context)
                return {
                    "status": "success",
                    "intensity": intensity,
                    "emotion_name": emotion_name,
                }
            else:
                return {"error": "Missing emotion_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in calculate emotional intensity: {e}")
            return {"error": str(e), "status": "failed"}

    def _initialize_plutchik_wheel(self) -> Dict:
        """Initialize Plutchik's wheel of emotions with opposites and combinations"""
        return {
            PlutchikEmotion.JOY: {
                "opposite": PlutchikEmotion.SADNESS,
                "intensities": ["serenity", "joy", "ecstasy"],
                "combinations": {
                    PlutchikEmotion.TRUST: "love",
                    PlutchikEmotion.ANTICIPATION: "optimism",
                    PlutchikEmotion.SURPRISE: "delight",
                },
            },
            PlutchikEmotion.TRUST: {
                "opposite": PlutchikEmotion.DISGUST,
                "intensities": ["acceptance", "trust", "admiration"],
                "combinations": {
                    PlutchikEmotion.JOY: "love",
                    PlutchikEmotion.FEAR: "submission",
                    PlutchikEmotion.SURPRISE: "curiosity",
                },
            },
            PlutchikEmotion.FEAR: {
                "opposite": PlutchikEmotion.ANGER,
                "intensities": ["apprehension", "fear", "terror"],
                "combinations": {
                    PlutchikEmotion.SURPRISE: "awe",
                    PlutchikEmotion.SADNESS: "despair",
                    PlutchikEmotion.DISGUST: "shame",
                },
            },
            PlutchikEmotion.SURPRISE: {
                "opposite": PlutchikEmotion.ANTICIPATION,
                "intensities": ["distraction", "surprise", "amazement"],
                "combinations": {
                    PlutchikEmotion.SADNESS: "disappointment",
                    PlutchikEmotion.JOY: "delight",
                    PlutchikEmotion.FEAR: "awe",
                },
            },
            PlutchikEmotion.SADNESS: {
                "opposite": PlutchikEmotion.JOY,
                "intensities": ["pensiveness", "sadness", "grief"],
                "combinations": {
                    PlutchikEmotion.DISGUST: "remorse",
                    PlutchikEmotion.ANGER: "envy",
                    PlutchikEmotion.FEAR: "despair",
                },
            },
            PlutchikEmotion.DISGUST: {
                "opposite": PlutchikEmotion.TRUST,
                "intensities": ["boredom", "disgust", "loathing"],
                "combinations": {
                    PlutchikEmotion.ANGER: "contempt",
                    PlutchikEmotion.SADNESS: "remorse",
                    PlutchikEmotion.FEAR: "shame",
                },
            },
            PlutchikEmotion.ANGER: {
                "opposite": PlutchikEmotion.FEAR,
                "intensities": ["annoyance", "anger", "rage"],
                "combinations": {
                    PlutchikEmotion.ANTICIPATION: "aggressiveness",
                    PlutchikEmotion.DISGUST: "contempt",
                    PlutchikEmotion.SADNESS: "envy",
                },
            },
            PlutchikEmotion.ANTICIPATION: {
                "opposite": PlutchikEmotion.SURPRISE,
                "intensities": ["interest", "anticipation", "vigilance"],
                "combinations": {
                    PlutchikEmotion.JOY: "optimism",
                    PlutchikEmotion.ANGER: "aggressiveness",
                    PlutchikEmotion.TRUST: "hope",
                },
            },
        }

    def _initialize_maslow_hierarchy(self) -> Dict:
        """Initialize Maslow's hierarchy of needs with emotional implications"""
        return {
            MaslowLevel.PHYSIOLOGICAL: {
                "needs": ["hunger", "thirst", "sleep", "shelter", "sex"],
                "emotions": ["desperate", "lustful", "anxious", "relieved"],
                "satisfaction_emotions": ["content", "satisfied", "relieved"],
                "frustration_emotions": ["desperate", "anxious", "frustrated"],
            },
            MaslowLevel.SAFETY: {
                "needs": ["security", "stability", "protection", "order"],
                "emotions": ["protective", "anxious", "fearful", "secure"],
                "satisfaction_emotions": ["secure", "confident", "calm"],
                "frustration_emotions": ["anxious", "fearful", "worried"],
            },
            MaslowLevel.LOVE_BELONGING: {
                "needs": ["love", "affection", "belonging", "intimacy"],
                "emotions": ["nurturing", "seductive", "obsessed", "lonely"],
                "satisfaction_emotions": ["loving", "caring", "connected"],
                "frustration_emotions": ["lonely", "desperate", "obsessed"],
            },
            MaslowLevel.ESTEEM: {
                "needs": ["achievement", "recognition", "respect", "confidence"],
                "emotions": ["confident", "proud", "defiant", "insecure"],
                "satisfaction_emotions": ["confident", "proud", "accomplished"],
                "frustration_emotions": ["insecure", "defiant", "jealous"],
            },
            MaslowLevel.SELF_ACTUALIZATION: {
                "needs": ["creativity", "fulfillment", "purpose", "growth"],
                "emotions": ["inspired", "fulfilled", "curious", "excited"],
                "satisfaction_emotions": ["fulfilled", "inspired", "excited"],
                "frustration_emotions": ["unfulfilled", "restless", "curious"],
            },
        }

    def _initialize_intensity_levels(self) -> Dict:
        """Initialize emotional intensity levels with psychological basis"""
        return {
            "mild": {
                "intensity": 0.3,
                "characteristics": ["subtle", "gentle", "soft", "quiet"],
                "physiological": "slight changes in breathing, minor facial expressions",
                "behavioral": "calm responses, measured speech, relaxed posture",
            },
            "moderate": {
                "intensity": 0.6,
                "characteristics": ["noticeable", "clear", "evident", "apparent"],
                "physiological": "increased heart rate, more pronounced expressions",
                "behavioral": "engaged responses, varied speech patterns, active posture",
            },
            "intense": {
                "intensity": 0.9,
                "characteristics": ["strong", "powerful", "overwhelming", "passionate"],
                "physiological": "rapid breathing, intense expressions, physical reactions",
                "behavioral": "passionate responses, dramatic speech, animated gestures",
            },
        }

    def load_fragments(self):
        """Load all emotional fragments from files"""
        fragments_dir = Path(__file__).parent

        for fragment_file in fragments_dir.glob("*.md"):
            if fragment_file.name == "README.md":
                continue

            with open(fragment_file, "r") as f:
                content = f.read()

            # Parse fragment data
            lines = content.split("\n")
            name = lines[0].replace("# ", "").replace(" Fragment", "")

            # Extract weight
            weight_line = [l for l in lines if "**Weight**:" in l][0]
            weight_str = weight_line.split("**Weight**:")[1].strip()
            # Handle placeholder weights like [0.0-1.0]
            if weight_str.startswith("[") and weight_str.endswith("]"):
                weight = 0.5  # Default weight for placeholders
            else:
                weight = float(weight_str)

            # Extract description
            desc_line = [l for l in lines if "**Description**:" in l][0]
            description = desc_line.split("**Description**:")[1].strip()

            # Extract keywords
            keywords_line = [l for l in lines if "**Keywords**:" in l][0]
            keywords = [
                k.strip()
                for k in keywords_line.split("**Keywords**:")[1].strip().split(",")
            ]

            # Extract example phrases
            phrases = []
            in_phrases = False
            for line in lines:
                if "**Example Phrases:**" in line:
                    in_phrases = True
                    continue
                if in_phrases and line.strip().startswith("- "):
                    phrases.append(line.strip()[2:])
                elif in_phrases and line.strip() == "":
                    break

            self.fragments[name.lower()] = {
                "name": name,
                "weight": weight,
                "description": description,
                "keywords": keywords,
                "phrases": phrases,
            }

    def analyze_plutchik_emotion(self, emotion_name: str) -> Dict:
        """Analyze an emotion using Plutchik's wheel"""
        emotion_lower = emotion_name.lower()

        # Map our emotions to Plutchik's primary emotions
        emotion_mapping = {
            "happy": PlutchikEmotion.JOY,
            "sad": PlutchikEmotion.SADNESS,
            "angry": PlutchikEmotion.ANGER,
            "fearful": PlutchikEmotion.FEAR,
            "surprised": PlutchikEmotion.SURPRISE,
            "disgusted": PlutchikEmotion.DISGUST,
            "trusting": PlutchikEmotion.TRUST,
            "anticipating": PlutchikEmotion.ANTICIPATION,
            "lustful": PlutchikEmotion.JOY,  # Physical desire
            "seductive": PlutchikEmotion.TRUST,  # Building trust/connection
            "obsessed": PlutchikEmotion.ANTICIPATION,  # Focused anticipation
            "submissive": PlutchikEmotion.FEAR,  # Fear-based submission
            "protective": PlutchikEmotion.TRUST,  # Trust-based protection
            "nurturing": PlutchikEmotion.TRUST,  # Trust and care
            "melancholic": PlutchikEmotion.SADNESS,
            "reverent": PlutchikEmotion.TRUST,  # Deep trust/admiration
            "defiant": PlutchikEmotion.ANGER,  # Anger-based resistance
            "confident": PlutchikEmotion.TRUST,  # Self-trust
            "excited": PlutchikEmotion.JOY,  # Joyful excitement
            "curious": PlutchikEmotion.SURPRISE,  # Surprise-based curiosity
            "teasing": PlutchikEmotion.JOY,  # Joyful play
            "whimsical": PlutchikEmotion.SURPRISE,  # Surprise-based whimsy
            "mysterious": PlutchikEmotion.ANTICIPATION,  # Anticipation of unknown
            "anxious": PlutchikEmotion.FEAR,
            "jealous": PlutchikEmotion.ANGER,  # Anger-based jealousy
            "grateful": PlutchikEmotion.TRUST,  # Trust-based gratitude
            "desperate": PlutchikEmotion.FEAR,  # Fear-based desperation
            "embarrassed": PlutchikEmotion.SADNESS,  # Sadness-based embarrassment
            "relieved": PlutchikEmotion.JOY,  # Joyful relief
        }

        primary_emotion = emotion_mapping.get(emotion_lower)
        if not primary_emotion:
            return {"error": f"Unknown emotion: {emotion_name}"}

        plutchik_data = self.plutchik_wheel[primary_emotion]

        return {
            "primary_emotion": primary_emotion.value,
            "opposite": plutchik_data["opposite"].value,
            "intensities": plutchik_data["intensities"],
            "combinations": plutchik_data["combinations"],
            "psychological_basis": f"Based on Plutchik's {primary_emotion.value} emotion",
        }

    def analyze_maslow_needs(self, emotion_name: str) -> Dict:
        """Analyze an emotion using Maslow's hierarchy of needs"""
        emotion_lower = emotion_name.lower()

        # Map emotions to Maslow levels
        maslow_mapping = {
            "lustful": MaslowLevel.PHYSIOLOGICAL,
            "desperate": MaslowLevel.PHYSIOLOGICAL,
            "anxious": MaslowLevel.SAFETY,
            "protective": MaslowLevel.SAFETY,
            "seductive": MaslowLevel.LOVE_BELONGING,
            "obsessed": MaslowLevel.LOVE_BELONGING,
            "nurturing": MaslowLevel.LOVE_BELONGING,
            "confident": MaslowLevel.ESTEEM,
            "defiant": MaslowLevel.ESTEEM,
            "excited": MaslowLevel.SELF_ACTUALIZATION,
            "curious": MaslowLevel.SELF_ACTUALIZATION,
            "inspired": MaslowLevel.SELF_ACTUALIZATION,
            "happy": MaslowLevel.LOVE_BELONGING,  # Social connection
            "melancholic": MaslowLevel.LOVE_BELONGING,  # Loss of connection
            "angry": MaslowLevel.ESTEEM,  # Threat to esteem
            "fearful": MaslowLevel.SAFETY,  # Safety threat
            "grateful": MaslowLevel.LOVE_BELONGING,  # Appreciation of connection
            "jealous": MaslowLevel.ESTEEM,  # Threat to esteem/connection
            "relieved": MaslowLevel.SAFETY,  # Safety restored
            "embarrassed": MaslowLevel.ESTEEM,  # Threat to esteem
            "playful": MaslowLevel.LOVE_BELONGING,  # Social connection
            "teasing": MaslowLevel.LOVE_BELONGING,  # Social interaction
            "whimsical": MaslowLevel.SELF_ACTUALIZATION,  # Creative expression
            "mysterious": MaslowLevel.SELF_ACTUALIZATION,  # Self-discovery
            "dominant": MaslowLevel.ESTEEM,  # Power/control
            "submissive": MaslowLevel.SAFETY,  # Safety through yielding
            "reverent": MaslowLevel.LOVE_BELONGING,  # Deep connection
            "flustered": MaslowLevel.ESTEEM,  # Social anxiety
            "cold": MaslowLevel.SAFETY,  # Emotional protection
            "breaking": MaslowLevel.LOVE_BELONGING,  # Loss of connection
            "desperate": MaslowLevel.PHYSIOLOGICAL,  # Basic needs
        }

        maslow_level = maslow_mapping.get(emotion_lower)
        if not maslow_level:
            # Default to love_belonging for unknown emotions
            maslow_level = MaslowLevel.LOVE_BELONGING

        hierarchy_data = self.maslow_hierarchy[maslow_level]

        return {
            "maslow_level": maslow_level.value,
            "needs": hierarchy_data["needs"],
            "related_emotions": hierarchy_data["emotions"],
            "satisfaction_emotions": hierarchy_data["satisfaction_emotions"],
            "frustration_emotions": hierarchy_data["frustration_emotions"],
            "psychological_basis": f"Related to {maslow_level.value} needs",
        }

    def calculate_emotional_intensity(
        self, emotion_name: str, context: Dict = None
    ) -> Dict:
        """Calculate emotional intensity using psychological models"""
        emotion_lower = emotion_name.lower()

        # Base intensity from the emotion's weight
        base_intensity = self.fragments.get(emotion_lower, {}).get("weight", 0.5)

        # Context modifiers
        intensity_modifier = 1.0
        if context:
            if context.get("urgency", False):
                intensity_modifier *= 1.5
            if context.get("intimacy", False):
                intensity_modifier *= 1.3
            if context.get("familiarity", False):
                intensity_modifier *= 0.8  # More comfortable, less intense

        final_intensity = min(1.0, base_intensity * intensity_modifier)

        # Determine intensity level
        if final_intensity < 0.4:
            level = "mild"
        elif final_intensity < 0.7:
            level = "moderate"
        else:
            level = "intense"

        intensity_data = self.intensity_levels[level]

        return {
            "intensity": final_intensity,
            "level": level,
            "characteristics": intensity_data["characteristics"],
            "physiological": intensity_data["physiological"],
            "behavioral": intensity_data["behavioral"],
            "psychological_basis": f"Intensity level: {level} based on context and base emotion weight",
        }

    def blend_emotions_with_psychology(
        self,
        primary_emotion: str,
        secondary_emotions: List[str] = None,
        blend_ratio: float = 0.7,
        context: Dict = None,
    ) -> Dict:
        """Enhanced emotion blending with psychological analysis"""

        if secondary_emotions is None:
            secondary_emotions = []

        # Get primary emotion
        if primary_emotion.lower() not in self.fragments:
            raise ValueError(f"Unknown emotion: {primary_emotion}")

        primary = self.fragments[primary_emotion.lower()]

        # Psychological analysis
        plutchik_analysis = self.analyze_plutchik_emotion(primary_emotion)
        maslow_analysis = self.analyze_maslow_needs(primary_emotion)
        intensity_analysis = self.calculate_emotional_intensity(
            primary_emotion, context
        )

        # Blend with secondary emotions
        blended_description = primary["description"]
        blended_keywords = primary["keywords"].copy()
        blended_phrases = primary["phrases"].copy()

        secondary_analyses = []
        for emotion in secondary_emotions:
            if emotion.lower() in self.fragments:
                secondary = self.fragments[emotion.lower()]
                secondary_plutchik = self.analyze_plutchik_emotion(emotion)
                secondary_maslow = self.analyze_maslow_needs(emotion)

                secondary_analyses.append(
                    {
                        "emotion": emotion,
                        "plutchik": secondary_plutchik,
                        "maslow": secondary_maslow,
                    }
                )

                # Blend descriptions
                blended_description += f" Mixed with {secondary['description'].lower()}"

                # Blend keywords
                blended_keywords.extend(secondary["keywords"])

                # Blend phrases (weighted by blend_ratio)
                if random.random() < blend_ratio:
                    blended_phrases.extend(secondary["phrases"])

        # Calculate blended weight
        total_weight = primary["weight"]
        for emotion in secondary_emotions:
            if emotion.lower() in self.fragments:
                total_weight += self.fragments[emotion.lower()]["weight"]
        blended_weight = total_weight / (1 + len(secondary_emotions))

        # Psychological complexity analysis
        psychological_complexity = self._analyze_psychological_complexity(
            plutchik_analysis, maslow_analysis, secondary_analyses
        )

        return {
            "name": f"{primary['name']}_psychologically_blended",
            "weight": blended_weight,
            "description": blended_description,
            "keywords": list(set(blended_keywords)),  # Remove duplicates
            "phrases": blended_phrases,
            "psychological_analysis": {
                "plutchik": plutchik_analysis,
                "maslow": maslow_analysis,
                "intensity": intensity_analysis,
                "complexity": psychological_complexity,
            },
        }

    def _analyze_psychological_complexity(
        self,
        primary_plutchik: Dict,
        primary_maslow: Dict,
        secondary_analyses: List[Dict],
    ) -> Dict:
        """Analyze the psychological complexity of blended emotions"""

        complexity_score = 1.0  # Base complexity

        # Add complexity for multiple Maslow levels
        maslow_levels = {primary_maslow["maslow_level"]}
        for analysis in secondary_analyses:
            maslow_levels.add(analysis["maslow"]["maslow_level"])

        complexity_score += len(maslow_levels) * 0.3

        # Add complexity for opposing Plutchik emotions
        primary_opposite = primary_plutchik.get("opposite")
        for analysis in secondary_analyses:
            if analysis["plutchik"].get("opposite") == primary_opposite:
                complexity_score += 0.5  # High complexity for opposites

        # Determine complexity level
        if complexity_score < 1.5:
            level = "simple"
        elif complexity_score < 2.5:
            level = "moderate"
        else:
            level = "complex"

        return {
            "score": complexity_score,
            "level": level,
            "maslow_levels_involved": list(maslow_levels),
            "description": f"Psychological complexity: {level} ({complexity_score:.2f})",
        }

    def create_psychologically_realistic_emotion(
        self, emotions: List[str], weights: List[float] = None, context: Dict = None
    ) -> Dict:
        """Create a psychologically realistic emotion blend"""

        if weights is None:
            weights = [1.0] * len(emotions)

        if len(emotions) != len(weights):
            raise ValueError("Number of emotions must match number of weights")

        # Find the primary emotion (highest weight)
        primary_idx = weights.index(max(weights))
        primary_emotion = emotions[primary_idx]
        secondary_emotions = [e for i, e in enumerate(emotions) if i != primary_idx]

        return self.blend_emotions_with_psychology(
            primary_emotion, secondary_emotions, context=context
        )

    def suggest_psychologically_realistic_combinations(self) -> List[Dict]:
        """Suggest psychologically realistic emotion combinations"""

        combinations = [
            {
                "primary": "happy",
                "secondary": ["lustful"],
                "description": "Joyful desire - satisfaction of love/belonging needs with physical attraction",
                "psychological_basis": "Combines Plutchik's joy with physiological needs (Maslow)",
            },
            {
                "primary": "melancholic",
                "secondary": ["lustful"],
                "description": "Melancholic desire - unfulfilled love needs with physical longing",
                "psychological_basis": "Combines Plutchik's sadness with physiological needs (Maslow)",
            },
            {
                "primary": "anxious",
                "secondary": ["excited"],
                "description": "Nervous excitement - safety concerns with self-actualization drive",
                "psychological_basis": "Combines Plutchik's fear with joy (opposite emotions create tension)",
            },
            {
                "primary": "jealous",
                "secondary": ["protective"],
                "description": "Possessive protection - esteem threat with safety concerns",
                "psychological_basis": "Combines Plutchik's anger with trust (complex emotional state)",
            },
            {
                "primary": "grateful",
                "secondary": ["submissive"],
                "description": "Thankful surrender - appreciation of connection with safety-based yielding",
                "psychological_basis": "Combines trust-based gratitude with fear-based submission",
            },
            {
                "primary": "desperate",
                "secondary": ["seductive"],
                "description": "Urgent seduction - physiological desperation with love/belonging needs",
                "psychological_basis": "Combines fear-based desperation with trust-building seduction",
            },
            {
                "primary": "embarrassed",
                "secondary": ["playful"],
                "description": "Shy playfulness - esteem threat with joy-based play",
                "psychological_basis": "Combines sadness-based embarrassment with joy-based play",
            },
            {
                "primary": "relieved",
                "secondary": ["nurturing"],
                "description": "Calm care - safety restoration with love/belonging expression",
                "psychological_basis": "Combines joy-based relief with trust-based nurturing",
            },
            {
                "primary": "confident",
                "secondary": ["mysterious"],
                "description": "Bold mystery - esteem satisfaction with anticipation of unknown",
                "psychological_basis": "Combines trust-based confidence with anticipation-based mystery",
            },
            {
                "primary": "curious",
                "secondary": ["seductive"],
                "description": "Inquisitive seduction - self-actualization drive with love/belonging needs",
                "psychological_basis": "Combines surprise-based curiosity with trust-building seduction",
            },
        ]

        return combinations

    def get_emotion_by_psychological_profile(
        self,
        plutchik_emotion: str = None,
        maslow_level: str = None,
        intensity_level: str = None,
    ) -> List[str]:
        """Find emotions that match psychological criteria"""

        matching_emotions = []

        for emotion_name, emotion_data in self.fragments.items():
            matches_criteria = True

            # Check Plutchik emotion
            if plutchik_emotion:
                plutchik_analysis = self.analyze_plutchik_emotion(emotion_name)
                if plutchik_analysis.get("primary_emotion") != plutchik_emotion:
                    matches_criteria = False

            # Check Maslow level
            if maslow_level:
                maslow_analysis = self.analyze_maslow_needs(emotion_name)
                if maslow_analysis.get("maslow_level") != maslow_level:
                    matches_criteria = False

            # Check intensity level
            if intensity_level:
                intensity_analysis = self.calculate_emotional_intensity(emotion_name)
                if intensity_analysis.get("level") != intensity_level:
                    matches_criteria = False

            if matches_criteria:
                matching_emotions.append(emotion_name)

        return matching_emotions


# Backward compatibility - keep the original class name
class EmotionalBlender(EnhancedEmotionalBlender):
    """Backward compatibility wrapper for the enhanced emotional blender"""

    pass


# Example usage
if __name__ == "__main__":
    blender = EnhancedEmotionalBlender()

    # Example: Create a psychologically realistic "happy but lustful" emotion
    happy_lustful = blender.blend_emotions_with_psychology("happy", ["lustful"])
    print(f"Psychologically blended emotion: {happy_lustful['name']}")
    print(f"Description: {happy_lustful['description']}")
    print(f"Psychological analysis: {happy_lustful['psychological_analysis']}")
    print(f"Example phrase: {random.choice(happy_lustful['phrases'])}")

    # Example: Create a complex psychologically realistic emotion
    complex_emotion = blender.create_psychologically_realistic_emotion(
        ["sad", "lustful", "grateful"], [0.4, 0.8, 0.6]
    )
    print(f"\nComplex psychologically realistic emotion: {complex_emotion['name']}")
    print(f"Description: {complex_emotion['description']}")
    print(
        f"Psychological complexity: {complex_emotion['psychological_analysis']['complexity']}"
    )

    # Example: Find emotions by psychological profile
    high_intensity_trust_emotions = blender.get_emotion_by_psychological_profile(
        plutchik_emotion="trust", intensity_level="intense"
    )
    print(f"\nHigh-intensity trust emotions: {high_intensity_trust_emotions}")
