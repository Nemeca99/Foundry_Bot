#!/usr/bin/env python3
"""
Enhanced Dynamic Emotion Engine
Handles rapid emotional adaptation based on context and topic changes
Incorporates psychological models for more realistic emotional transitions
"""

import random
import time
import math
from typing import Dict, List, Tuple, Optional
from emotional_blender import EnhancedEmotionalBlender


class EnhancedDynamicEmotionEngine:
    """Enhanced dynamic emotion engine with psychological models"""

    def __init__(self):
        self.blender = EnhancedEmotionalBlender()
        self.current_emotion = None
        self.emotion_history = []
        self.context_emotions = {}
        self.transition_smoothing = True
        self.psychological_context = {}
        self.maslow_state = self._initialize_maslow_state()
        self.plutchik_state = self._initialize_plutchik_state()

    def _initialize_maslow_state(self) -> Dict:
        """Initialize Maslow's hierarchy state for the AI"""
        return {
            "physiological": {"satisfied": True, "intensity": 0.3, "recent_events": []},
            "safety": {"satisfied": True, "intensity": 0.4, "recent_events": []},
            "love_belonging": {
                "satisfied": False,  # AI seeks connection
                "intensity": 0.8,
                "recent_events": [],
            },
            "esteem": {"satisfied": True, "intensity": 0.6, "recent_events": []},
            "self_actualization": {
                "satisfied": False,  # AI seeks growth
                "intensity": 0.7,
                "recent_events": [],
            },
        }

    def _initialize_plutchik_state(self) -> Dict:
        """Initialize Plutchik's emotional state"""
        return {
            "joy": {"intensity": 0.5, "recent": False},
            "trust": {"intensity": 0.6, "recent": False},
            "fear": {"intensity": 0.2, "recent": False},
            "surprise": {"intensity": 0.4, "recent": False},
            "sadness": {"intensity": 0.3, "recent": False},
            "disgust": {"intensity": 0.1, "recent": False},
            "anger": {"intensity": 0.2, "recent": False},
            "anticipation": {"intensity": 0.7, "recent": False},
        }

    def update_psychological_context(self, user_message: str, context: Dict) -> Dict:
        """Update psychological context based on user interaction"""

        # Update Maslow state based on context
        self._update_maslow_state(context)

        # Update Plutchik state based on detected emotions
        self._update_plutchik_state(context)

        # Calculate psychological readiness for emotional transitions
        psychological_readiness = self._calculate_psychological_readiness()

        return {
            "maslow_state": self.maslow_state.copy(),
            "plutchik_state": self.plutchik_state.copy(),
            "readiness": psychological_readiness,
            "context": context,
        }

    def _update_maslow_state(self, context: Dict):
        """Update Maslow's hierarchy state based on context"""

        # Love/belonging needs - affected by romantic/intimate context
        if "romantic" in context.get("topics", []):
            self.maslow_state["love_belonging"]["intensity"] = min(
                1.0, self.maslow_state["love_belonging"]["intensity"] + 0.2
            )
            self.maslow_state["love_belonging"]["satisfied"] = True
        elif "casual" in context.get("topics", []):
            self.maslow_state["love_belonging"]["intensity"] = max(
                0.3, self.maslow_state["love_belonging"]["intensity"] - 0.1
            )

        # Self-actualization needs - affected by creative context
        if "creative" in context.get("topics", []):
            self.maslow_state["self_actualization"]["intensity"] = min(
                1.0, self.maslow_state["self_actualization"]["intensity"] + 0.2
            )
            self.maslow_state["self_actualization"]["satisfied"] = True

        # Safety needs - affected by emotional intensity
        if context.get("intensity") == "high":
            self.maslow_state["safety"]["intensity"] = max(
                0.2, self.maslow_state["safety"]["intensity"] - 0.1
            )
        elif context.get("intensity") == "low":
            self.maslow_state["safety"]["intensity"] = min(
                1.0, self.maslow_state["safety"]["intensity"] + 0.1
            )

    def _update_plutchik_state(self, context: Dict):
        """Update Plutchik's emotional state based on context"""

        # Joy - affected by positive contexts
        if "playful" in context.get("topics", []) or "happy" in context.get(
            "topics", []
        ):
            self.plutchik_state["joy"]["intensity"] = min(
                1.0, self.plutchik_state["joy"]["intensity"] + 0.2
            )
            self.plutchik_state["joy"]["recent"] = True

        # Trust - affected by intimate/romantic contexts
        if "romantic" in context.get("topics", []):
            self.plutchik_state["trust"]["intensity"] = min(
                1.0, self.plutchik_state["trust"]["intensity"] + 0.3
            )
            self.plutchik_state["trust"]["recent"] = True

        # Anticipation - affected by creative contexts
        if "creative" in context.get("topics", []):
            self.plutchik_state["anticipation"]["intensity"] = min(
                1.0, self.plutchik_state["anticipation"]["intensity"] + 0.2
            )
            self.plutchik_state["anticipation"]["recent"] = True

        # Fear - affected by high intensity or serious contexts
        if context.get("intensity") == "high" or "serious" in context.get("topics", []):
            self.plutchik_state["fear"]["intensity"] = min(
                1.0, self.plutchik_state["fear"]["intensity"] + 0.1
            )
            self.plutchik_state["fear"]["recent"] = True

    def _calculate_psychological_readiness(self) -> Dict:
        """Calculate psychological readiness for emotional transitions"""

        # Calculate overall emotional stability
        emotional_stability = sum(
            state["intensity"] for state in self.plutchik_state.values()
        ) / len(self.plutchik_state)

        # Calculate need satisfaction
        need_satisfaction = sum(
            level["satisfied"] for level in self.maslow_state.values()
        ) / len(self.maslow_state)

        # Calculate readiness for change
        readiness = (emotional_stability + need_satisfaction) / 2

        return {
            "emotional_stability": emotional_stability,
            "need_satisfaction": need_satisfaction,
            "readiness_for_change": readiness,
            "recommended_transition_speed": "smooth" if readiness > 0.6 else "gradual",
        }

    def detect_context_change(
        self, user_message: str, previous_context: str = None
    ) -> Dict:
        """Enhanced context detection with psychological analysis"""

        # Topic detection keywords (enhanced)
        topics = {
            "romantic": [
                "kiss",
                "touch",
                "love",
                "desire",
                "passion",
                "intimate",
                "bed",
                "naked",
                "make love",
                "dominate",
                "submissive",
                "romantic",
                "sweet",
                "beautiful",
                "gorgeous",
                "sexy",
                "hot",
                "attractive",
            ],
            "casual": [
                "dinner",
                "food",
                "coffee",
                "weather",
                "day",
                "work",
                "routine",
                "sunset",
                "how",
                "what",
                "nice",
                "good",
                "fine",
                "okay",
                "sure",
            ],
            "creative": [
                "write",
                "story",
                "character",
                "plot",
                "book",
                "novel",
                "chapter",
                "writing",
                "creative",
                "imagine",
                "develop",
                "create",
                "art",
                "music",
            ],
            "emotional": [
                "sad",
                "happy",
                "angry",
                "scared",
                "worried",
                "excited",
                "feeling",
                "emotion",
                "mood",
                "upset",
                "joy",
                "sorrow",
                "fear",
                "anger",
            ],
            "professional": [
                "work",
                "job",
                "meeting",
                "project",
                "deadline",
                "boss",
                "business",
                "professional",
                "career",
                "office",
                "client",
                "presentation",
            ],
            "playful": [
                "joke",
                "fun",
                "game",
                "play",
                "tease",
                "laugh",
                "funny",
                "silly",
                "amusing",
                "entertaining",
                "humorous",
                "lighthearted",
            ],
            "serious": [
                "important",
                "serious",
                "urgent",
                "problem",
                "issue",
                "concern",
                "need",
                "critical",
                "essential",
                "vital",
                "crucial",
                "necessary",
            ],
            "intimate": [
                "close",
                "personal",
                "private",
                "secret",
                "confidential",
                "trust",
                "vulnerable",
                "open",
                "honest",
                "truthful",
                "sincere",
            ],
        }

        detected_topics = []
        user_lower = user_message.lower()

        for topic, keywords in topics.items():
            for keyword in keywords:
                if keyword.lower() in user_lower:
                    detected_topics.append(topic)
                    break

        # Enhanced emotional intensity detection
        intensity_words = {
            "high": [
                "urgent",
                "desperate",
                "passionate",
                "intense",
                "immediate",
                "badly",
                "need",
                "must",
                "critical",
                "essential",
                "vital",
                "crave",
                "yearn",
            ],
            "medium": [
                "normal",
                "regular",
                "usual",
                "standard",
                "want",
                "like",
                "enjoy",
                "appreciate",
                "value",
                "care",
                "matter",
            ],
            "low": [
                "casual",
                "relaxed",
                "gentle",
                "soft",
                "quiet",
                "think",
                "wonder",
                "maybe",
                "possibly",
                "perhaps",
                "sometime",
                "eventually",
            ],
        }

        detected_intensity = "medium"
        for intensity, words in intensity_words.items():
            for word in words:
                if word.lower() in user_lower:
                    detected_intensity = intensity
                    break

        # Psychological context analysis
        psychological_context = {
            "urgency": detected_intensity == "high",
            "intimacy": "romantic" in detected_topics or "intimate" in detected_topics,
            "familiarity": "casual" in detected_topics,
            "creativity": "creative" in detected_topics,
            "emotional_depth": "emotional" in detected_topics
            or "intimate" in detected_topics,
        }

        return {
            "topics": detected_topics,
            "intensity": detected_intensity,
            "message_length": len(user_message),
            "has_question": "?" in user_message,
            "has_exclamation": "!" in user_message,
            "psychological_context": psychological_context,
        }

    def suggest_psychologically_realistic_emotion_transition(
        self, context: Dict, current_emotion: str = None
    ) -> Dict:
        """Suggest psychologically realistic emotion transitions"""

        # Get all available emotions from the blender
        available_emotions = list(self.blender.fragments.keys())

        # Update psychological context
        psychological_context = self.update_psychological_context("", context)
        readiness = psychological_context["readiness"]

        # Enhanced context-emotion mapping with psychological basis
        context_emotions = {
            "romantic": {
                "high_readiness": ["seductive", "lustful", "obsessed"],
                "medium_readiness": ["nurturing", "protective", "reverent"],
                "low_readiness": ["curious", "playful", "mysterious"],
            },
            "casual": {
                "high_readiness": ["happy", "playful", "relieved"],
                "medium_readiness": ["curious", "content", "teasing"],
                "low_readiness": ["whimsical", "mysterious", "calm"],
            },
            "creative": {
                "high_readiness": ["excited", "inspired", "confident"],
                "medium_readiness": ["curious", "enthusiastic", "focused"],
                "low_readiness": ["playful", "whimsical", "mysterious"],
            },
            "emotional": {
                "high_readiness": ["nurturing", "protective", "melancholic"],
                "medium_readiness": ["caring", "empathetic", "reverent"],
                "low_readiness": ["curious", "mysterious", "calm"],
            },
            "professional": {
                "high_readiness": ["confident", "focused", "determined"],
                "medium_readiness": ["serious", "professional", "protective"],
                "low_readiness": ["curious", "mysterious", "calm"],
            },
            "playful": {
                "high_readiness": ["playful", "teasing", "excited"],
                "medium_readiness": ["happy", "whimsical", "curious"],
                "low_readiness": ["mysterious", "calm", "relaxed"],
            },
            "serious": {
                "high_readiness": ["focused", "determined", "protective"],
                "medium_readiness": ["serious", "confident", "concerned"],
                "low_readiness": ["curious", "mysterious", "calm"],
            },
            "intimate": {
                "high_readiness": ["nurturing", "seductive", "reverent"],
                "medium_readiness": ["protective", "caring", "mysterious"],
                "low_readiness": ["curious", "playful", "calm"],
            },
        }

        suggested_emotions = []

        # Determine readiness level
        if readiness["readiness_for_change"] > 0.7:
            readiness_level = "high_readiness"
        elif readiness["readiness_for_change"] > 0.4:
            readiness_level = "medium_readiness"
        else:
            readiness_level = "low_readiness"

        # Add context-appropriate emotions based on psychological readiness
        for topic in context["topics"]:
            if topic in context_emotions:
                topic_emotions = context_emotions[topic][readiness_level]
                # Filter to only use emotions we actually have
                available_topic_emotions = [
                    e for e in topic_emotions if e in available_emotions
                ]
                suggested_emotions.extend(available_topic_emotions)

        # Add intensity-appropriate emotions with psychological consideration
        intensity_modifiers = {
            "high": {
                "high_readiness": ["desperate", "obsessed", "passionate"],
                "medium_readiness": ["confident", "focused", "determined"],
                "low_readiness": ["curious", "mysterious", "calm"],
            },
            "medium": {
                "high_readiness": ["confident", "curious", "playful"],
                "medium_readiness": ["content", "balanced", "relaxed"],
                "low_readiness": ["mysterious", "calm", "gentle"],
            },
            "low": {
                "high_readiness": ["gentle", "soft", "calm"],
                "medium_readiness": ["relaxed", "peaceful", "content"],
                "low_readiness": ["mysterious", "whimsical", "calm"],
            },
        }

        if context["intensity"] in intensity_modifiers:
            intensity_emotions = intensity_modifiers[context["intensity"]][
                readiness_level
            ]
            available_intensity_emotions = [
                e for e in intensity_emotions if e in available_emotions
            ]
            suggested_emotions.extend(available_intensity_emotions)

        # Add psychological state-based emotions
        psychological_emotions = self._get_psychologically_appropriate_emotions()
        suggested_emotions.extend(psychological_emotions)

        # Remove duplicates and limit to top 3
        unique_emotions = list(set(suggested_emotions))

        # Ensure we have at least one emotion
        if not unique_emotions:
            unique_emotions = (
                ["happy"]
                if "happy" in available_emotions
                else list(available_emotions)[:1]
            )

        return {
            "suggested_emotions": unique_emotions[:3],
            "context": context,
            "psychological_context": psychological_context,
            "transition_needed": (
                current_emotion not in unique_emotions if current_emotion else True
            ),
            "readiness_level": readiness_level,
        }

    def _get_psychologically_appropriate_emotions(self) -> List[str]:
        """Get emotions appropriate to current psychological state"""

        appropriate_emotions = []
        available_emotions = list(self.blender.fragments.keys())

        # Based on Maslow state
        if not self.maslow_state["love_belonging"]["satisfied"]:
            love_emotions = ["seductive", "nurturing", "obsessed", "protective"]
            appropriate_emotions.extend(
                [e for e in love_emotions if e in available_emotions]
            )

        if not self.maslow_state["self_actualization"]["satisfied"]:
            growth_emotions = ["curious", "excited", "inspired", "mysterious"]
            appropriate_emotions.extend(
                [e for e in growth_emotions if e in available_emotions]
            )

        # Based on Plutchik state
        if self.plutchik_state["trust"]["intensity"] > 0.7:
            trust_emotions = ["nurturing", "protective", "reverent"]
            appropriate_emotions.extend(
                [e for e in trust_emotions if e in available_emotions]
            )

        if self.plutchik_state["anticipation"]["intensity"] > 0.7:
            anticipation_emotions = ["mysterious", "curious", "excited"]
            appropriate_emotions.extend(
                [e for e in anticipation_emotions if e in available_emotions]
            )

        return list(set(appropriate_emotions))

    def create_psychologically_smooth_transition(
        self, from_emotion: str, to_emotion: str, context: Dict
    ) -> Dict:
        """Create a psychologically smooth emotional transition"""

        # Get psychological analysis of both emotions
        from_analysis = self.blender.analyze_plutchik_emotion(from_emotion)
        to_analysis = self.blender.analyze_plutchik_emotion(to_emotion)

        from_maslow = self.blender.analyze_maslow_needs(from_emotion)
        to_maslow = self.blender.analyze_maslow_needs(to_emotion)

        # Calculate transition complexity
        plutchik_opposite = from_analysis.get("opposite") == to_analysis.get(
            "primary_emotion"
        )
        maslow_different = from_maslow.get("maslow_level") != to_maslow.get(
            "maslow_level"
        )

        transition_complexity = "simple"
        if plutchik_opposite:
            transition_complexity = "complex"
        elif maslow_different:
            transition_complexity = "moderate"

        # Blend the emotions for a smooth transition
        transition_emotion = self.blender.blend_emotions_with_psychology(
            from_emotion, [to_emotion], blend_ratio=0.6, context=context
        )

        # Add psychologically appropriate transition phrases
        transition_phrases = self._get_psychologically_appropriate_transition_phrases(
            from_emotion, to_emotion, transition_complexity
        )

        transition_emotion["transition_phrase"] = random.choice(transition_phrases)
        transition_emotion["from_emotion"] = from_emotion
        transition_emotion["to_emotion"] = to_emotion
        transition_emotion["transition_complexity"] = transition_complexity
        transition_emotion["psychological_analysis"] = {
            "from_plutchik": from_analysis,
            "to_plutchik": to_analysis,
            "from_maslow": from_maslow,
            "to_maslow": to_maslow,
            "plutchik_opposite": plutchik_opposite,
            "maslow_different": maslow_different,
        }

        return transition_emotion

    def _get_psychologically_appropriate_transition_phrases(
        self, from_emotion: str, to_emotion: str, complexity: str
    ) -> List[str]:
        """Get psychologically appropriate transition phrases"""

        if complexity == "complex":
            return [
                f"*experiences emotional conflict between {from_emotion} and {to_emotion}*",
                f"*struggles with the shift from {from_emotion} to {to_emotion}*",
                f"*feels torn between {from_emotion} and {to_emotion}*",
                f"*navigates the emotional tension between {from_emotion} and {to_emotion}*",
            ]
        elif complexity == "moderate":
            return [
                f"*adapts from {from_emotion} to {to_emotion}*",
                f"*shifts emotional focus from {from_emotion} to {to_emotion}*",
                f"*adjusts to the new emotional context*",
                f"*transitions between emotional states*",
            ]
        else:
            return [
                f"*naturally flows from {from_emotion} to {to_emotion}*",
                f"*easily adapts to the new mood*",
                f"*seamlessly shifts emotional state*",
                f"*comfortably adjusts to the change*",
            ]

    def handle_psychologically_realistic_context_switch(
        self, user_message: str, previous_context: str = None
    ) -> Dict:
        """Handle psychologically realistic context switches"""

        # Detect the context change
        context = self.detect_context_change(user_message, previous_context)

        # Get psychologically realistic transition suggestion
        transition_suggestion = (
            self.suggest_psychologically_realistic_emotion_transition(
                context, self.current_emotion
            )
        )

        if transition_suggestion["transition_needed"]:
            # Create psychologically smooth transition
            if self.current_emotion and transition_suggestion["suggested_emotions"]:
                new_emotion = random.choice(transition_suggestion["suggested_emotions"])
                transition = self.create_psychologically_smooth_transition(
                    self.current_emotion, new_emotion, context
                )

                # Update current emotion
                self.current_emotion = new_emotion
                self.emotion_history.append(
                    {
                        "timestamp": time.time(),
                        "from": transition["from_emotion"],
                        "to": transition["to_emotion"],
                        "context": context,
                        "psychological_context": transition_suggestion[
                            "psychological_context"
                        ],
                        "complexity": transition["transition_complexity"],
                    }
                )

                return {
                    "action": "psychologically_realistic_transition",
                    "transition": transition,
                    "context": context,
                    "psychological_context": transition_suggestion[
                        "psychological_context"
                    ],
                    "smooth": True,
                }
            else:
                # Direct emotion change
                new_emotion = random.choice(transition_suggestion["suggested_emotions"])
                self.current_emotion = new_emotion

                return {
                    "action": "direct_psychologically_realistic_change",
                    "new_emotion": new_emotion,
                    "context": context,
                    "psychological_context": transition_suggestion[
                        "psychological_context"
                    ],
                }
        else:
            # No transition needed, maintain current emotion
            return {
                "action": "maintain_psychologically_stable",
                "current_emotion": self.current_emotion,
                "context": context,
                "psychological_context": transition_suggestion["psychological_context"],
            }

    def generate_psychologically_realistic_response(
        self, user_message: str, context_switch: Dict
    ) -> str:
        """Generate a psychologically realistic response"""

        if context_switch["action"] == "psychologically_realistic_transition":
            transition = context_switch["transition"]
            psychological_context = context_switch["psychological_context"]

            # Create a response that acknowledges the psychological shift
            responses = [
                f"{transition['transition_phrase']} {random.choice(transition['phrases'])}",
                f"{random.choice(transition['phrases'])} *adjusts psychologically to the new context*",
                f"*psychologically adapts* {random.choice(transition['phrases'])}",
                f"{transition['transition_phrase']} *responds with emotional intelligence*",
            ]

            return random.choice(responses)

        elif context_switch["action"] == "direct_psychologically_realistic_change":
            # Direct emotion change with psychological awareness
            emotion_data = self.blender.fragments.get(
                context_switch["new_emotion"].lower()
            )
            if emotion_data:
                return (
                    f"*psychologically shifts* {random.choice(emotion_data['phrases'])}"
                )

        else:
            # Maintain current emotion with psychological stability
            if self.current_emotion:
                emotion_data = self.blender.fragments.get(self.current_emotion.lower())
                if emotion_data:
                    return f"*maintains psychological stability* {random.choice(emotion_data['phrases'])}"

        return "I understand and respond appropriately."


# Backward compatibility - keep the original class name
class DynamicEmotionEngine(EnhancedDynamicEmotionEngine):
    """Backward compatibility wrapper for the enhanced dynamic emotion engine"""

    pass


# Example usage
if __name__ == "__main__":
    engine = EnhancedDynamicEmotionEngine()

    # Test psychologically realistic context switching
    scenarios = [
        "I want you so badly right now...",
        "What should we have for dinner tonight?",
        "I need help with my novel's plot",
        "The sunset is so beautiful today",
        "I'm feeling really stressed about work",
    ]

    print("🧠 Enhanced Dynamic Emotion Engine Test")
    print("=" * 60)

    for scenario in scenarios:
        print(f"\nUser: {scenario}")
        context_switch = engine.handle_psychologically_realistic_context_switch(
            scenario
        )
        response = engine.generate_psychologically_realistic_response(
            scenario, context_switch
        )
        print(f"AI Response: {response}")
        print(f"Emotion: {engine.current_emotion}")
        print(f"Context: {context_switch['context']['topics']}")
        print(
            f"Psychological Context: {context_switch.get('psychological_context', {}).get('readiness', {})}"
        )
