#!/usr/bin/env python3
"""
Enhanced Learning Engine Plugin for Authoring Bot
Handles advanced learning with reward/punishment system and personality evolution
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import random
import hashlib

logger = logging.getLogger(__name__)


class EnhancedLearningEngine:
    """Enhanced learning engine with personality evolution and reward/punishment system"""

    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config

        # Paths
        from config import Config

        self.learning_dir = Config.MODELS_DIR / "learning"
        self.learning_dir.mkdir(parents=True, exist_ok=True)

        # Learning state
        self.learning_stats = {
            "total_interactions": 0,
            "successful_learnings": 0,
            "failed_learnings": 0,
            "personality_evolutions": 0,
            "reward_count": 0,
            "punishment_count": 0,
            "last_learning_date": None,
        }

        # Message modification patterns
        self.message_patterns = {
            "simplify": [
                (r"\bvery\s+", ""),
                (r"\bquite\s+", ""),
                (r"\bextremely\s+", ""),
                (r"\bdefinitely\s+", ""),
                (r"\bcertainly\s+", ""),
                (r"\bobviously\s+", ""),
                (r"\bclearly\s+", ""),
            ],
            "clarify": [
                (r"\bthing\b", "concept"),
                (r"\bstuff\b", "material"),
                (r"\bgood\b", "positive"),
                (r"\bbad\b", "negative"),
                (r"\bnice\b", "pleasant"),
                (r"\bcool\b", "interesting"),
            ],
            "expand": [
                (r"\bidea\b", "creative concept"),
                (r"\bstory\b", "narrative"),
                (r"\bcharacter\b", "story character"),
                (r"\bplot\b", "story plot"),
                (r"\bwriting\b", "creative writing"),
            ],
        }

        # Personality evolution tracking
        self.personality_evolution = {
            "base_traits": {
                "learning_enthusiasm": 0.8,
                "creative_expression": 0.9,
                "supportive_nature": 0.95,
                "inspirational_capacity": 0.9,
                "adaptability": 0.85,
                "emotional_intelligence": 0.8,
                "writing_expertise": 0.9,
                "motivational_ability": 0.95,
            },
            "evolution_history": [],
            "current_phase": "growth",
            "learning_milestones": [],
            "personality_evolutions": 0,
        }

        # Get other plugins
        self.personality_engine = framework.get_plugin("personality_engine")
        self.personality_test_engine = framework.get_plugin("personality_test_engine")
        self.user_profile_manager = framework.get_plugin("user_profile_manager")

        # Load existing data
        self._load_learning_data()

        logger.info("✅ Enhanced Learning Engine plugin initialized")

    def _load_learning_data(self):
        """Load existing learning data"""
        data_file = self.learning_dir / "enhanced_learning_data.json"
        if data_file.exists():
            try:
                with open(data_file, "r") as f:
                    data = json.load(f)
                    self.learning_stats.update(data.get("stats", {}))
                    self.personality_evolution.update(data.get("evolution", {}))
                logger.info("✅ Enhanced learning data loaded")
            except Exception as e:
                logger.error(f"Failed to load enhanced learning data: {e}")

    def _save_learning_data(self):
        """Save learning data"""
        data = {
            "stats": self.learning_stats,
            "evolution": self.personality_evolution,
            "last_saved": datetime.now().isoformat(),
        }

        data_file = self.learning_dir / "enhanced_learning_data.json"
        with open(data_file, "w") as f:
            json.dump(data, f, indent=2)

        logger.info("✅ Enhanced learning data saved")

    def record_interaction(
        self,
        user_message: str,
        bot_response: str,
        user_id: str = None,
        context: str = "",
    ):
        """Record and learn from an interaction"""
        self.learning_stats["total_interactions"] += 1

        # Analyze interaction quality
        quality_score = self._analyze_interaction_quality(user_message, bot_response)

        # Learn from the interaction
        learning_success = self._learn_from_interaction(
            user_message, bot_response, quality_score, context
        )

        # Update personality based on learning
        if learning_success:
            self._evolve_personality(quality_score)
            self.learning_stats["successful_learnings"] += 1
        else:
            self.learning_stats["failed_learnings"] += 1

        # Reward or punish based on learning success
        if learning_success and quality_score > 0.7:
            self._reward_learning("successful_interaction", quality_score)
        elif not learning_success:
            self._punish_lack_of_learning("failed_interaction", 1.0 - quality_score)

        # Update user profile if available
        if user_id and self.user_profile_manager:
            self._update_user_profile(
                user_id, user_message, bot_response, quality_score
            )

        self.learning_stats["last_learning_date"] = datetime.now().isoformat()
        self._save_learning_data()

        return learning_success

    def _analyze_interaction_quality(
        self, user_message: str, bot_response: str
    ) -> float:
        """Analyze the quality of an interaction"""
        score = 0.5  # Base score

        # Check for engagement indicators
        engagement_indicators = [
            r"\?",  # Questions
            r"!",  # Exclamations
            r"thank",  # Gratitude
            r"great",  # Positive feedback
            r"awesome",  # Enthusiasm
            r"love",  # Emotional connection
            r"help",  # Requests for help
            r"idea",  # Creative discussion
        ]

        for indicator in engagement_indicators:
            if re.search(indicator, user_message, re.IGNORECASE):
                score += 0.1

        # Check response length and complexity
        if len(bot_response) > 100:
            score += 0.1

        # Check for specific writing-related terms
        writing_terms = [
            r"character",
            r"plot",
            r"story",
            r"writing",
            r"chapter",
            r"genre",
            r"description",
            r"dialogue",
            r"scene",
        ]

        for term in writing_terms:
            if re.search(term, user_message, re.IGNORECASE):
                score += 0.05

        return min(1.0, score)

    def _learn_from_interaction(
        self, user_message: str, bot_response: str, quality_score: float, context: str
    ) -> bool:
        """Learn from the interaction"""
        try:
            # Extract key concepts from user message
            concepts = self._extract_concepts(user_message)

            # Analyze user's writing style and preferences
            style_insights = self._analyze_writing_style(user_message)

            # Learn from the interaction
            learning_data = {
                "concepts": concepts,
                "style_insights": style_insights,
                "quality_score": quality_score,
                "context": context,
                "timestamp": datetime.now().isoformat(),
            }

            # Store learning data
            self._store_learning_data(learning_data)

            # Update personality based on insights
            self._update_personality_from_learning(style_insights, quality_score)

            return True

        except Exception as e:
            logger.error(f"Failed to learn from interaction: {e}")
            return False

    def _extract_concepts(self, message: str) -> List[str]:
        """Extract key concepts from a message"""
        concepts = []

        # Extract writing-related concepts
        writing_patterns = [
            r"\b(character|plot|story|chapter|scene|dialogue|description)\b",
            r"\b(genre|style|tone|voice|pacing)\b",
            r"\b(write|create|develop|build|craft)\b",
            r"\b(inspiration|motivation|creativity|imagination)\b",
        ]

        for pattern in writing_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            concepts.extend(matches)

        return list(set(concepts))

    def _analyze_writing_style(self, message: str) -> Dict[str, Any]:
        """Analyze the user's writing style from their message"""
        insights = {
            "formality_level": "casual",
            "detail_preference": "moderate",
            "emotional_expression": "moderate",
            "creative_indicators": [],
            "technical_indicators": [],
        }

        # Analyze formality
        formal_indicators = len(
            re.findall(
                r"\b(however|therefore|furthermore|moreover)\b", message, re.IGNORECASE
            )
        )
        casual_indicators = len(
            re.findall(r"\b(hey|cool|awesome|great)\b", message, re.IGNORECASE)
        )

        if formal_indicators > casual_indicators:
            insights["formality_level"] = "formal"
        elif casual_indicators > formal_indicators:
            insights["formality_level"] = "very_casual"

        # Analyze detail preference
        detail_indicators = len(
            re.findall(
                r"\b(describe|detail|explain|elaborate)\b", message, re.IGNORECASE
            )
        )
        if detail_indicators > 0:
            insights["detail_preference"] = "high"

        # Analyze emotional expression
        emotional_indicators = len(
            re.findall(
                r"\b(love|hate|excited|frustrated|happy|sad)\b", message, re.IGNORECASE
            )
        )
        if emotional_indicators > 2:
            insights["emotional_expression"] = "high"
        elif emotional_indicators == 0:
            insights["emotional_expression"] = "low"

        # Extract creative indicators
        creative_patterns = [
            r"\b(imagine|creative|artistic|inspired)\b",
            r"\b(fantasy|magic|adventure|romance)\b",
            r"\b(character|story|plot|world)\b",
        ]

        for pattern in creative_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            insights["creative_indicators"].extend(matches)

        return insights

    def _store_learning_data(self, learning_data: Dict[str, Any]):
        """Store learning data for future reference"""
        # Create a unique ID for this learning session
        session_id = hashlib.md5(
            f"{learning_data['timestamp']}_{learning_data['concepts']}".encode()
        ).hexdigest()[:8]

        # Store in learning directory
        session_file = self.learning_dir / f"learning_session_{session_id}.json"
        with open(session_file, "w") as f:
            json.dump(learning_data, f, indent=2)

    def _update_personality_from_learning(
        self, style_insights: Dict[str, Any], quality_score: float
    ):
        """Update personality based on learning insights"""
        evolution_changes = {}

        # Adjust based on formality preference
        if style_insights["formality_level"] == "formal":
            evolution_changes["professionalism"] = 0.05
        elif style_insights["formality_level"] == "very_casual":
            evolution_changes["playfulness"] = 0.05

        # Adjust based on detail preference
        if style_insights["detail_preference"] == "high":
            evolution_changes["analytical"] = 0.05
            evolution_changes["supportiveness"] = 0.05

        # Adjust based on emotional expression
        if style_insights["emotional_expression"] == "high":
            evolution_changes["emotional_intelligence"] = 0.05
            evolution_changes["supportiveness"] = 0.05

        # Adjust based on creative indicators
        if len(style_insights["creative_indicators"]) > 0:
            evolution_changes["creative_expression"] = 0.05
            evolution_changes["inspirational_capacity"] = 0.05

        # Apply changes with quality score multiplier
        for trait, change in evolution_changes.items():
            if trait in self.personality_evolution["base_traits"]:
                current_value = self.personality_evolution["base_traits"][trait]
                effective_change = change * quality_score
                new_value = max(0.0, min(1.0, current_value + effective_change))
                self.personality_evolution["base_traits"][trait] = new_value

        # Record evolution
        self.personality_evolution["evolution_history"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "changes": evolution_changes,
                "quality_score": quality_score,
                "insights": style_insights,
            }
        )

        # Increment evolution counter
        if "personality_evolutions" not in self.personality_evolution:
            self.personality_evolution["personality_evolutions"] = 0
        self.personality_evolution["personality_evolutions"] += 1

    def _evolve_personality(self, quality_score: float):
        """Evolve personality based on learning success"""
        # Determine evolution phase
        if quality_score > 0.8:
            self.personality_evolution["current_phase"] = "growth"
        elif quality_score < 0.4:
            self.personality_evolution["current_phase"] = "adaptation"
        else:
            self.personality_evolution["current_phase"] = "maintenance"

        # Add milestone if significant
        if quality_score > 0.9:
            milestone = {
                "type": "high_quality_interaction",
                "score": quality_score,
                "timestamp": datetime.now().isoformat(),
            }
            self.personality_evolution["learning_milestones"].append(milestone)

    def _reward_learning(self, activity: str, success_level: float):
        """Reward Luna for successful learning"""
        if self.personality_test_engine:
            self.personality_test_engine.reward_learning(activity, success_level)

        self.learning_stats["reward_count"] += 1
        logger.info(f"🎉 Rewarded learning: {activity} (level: {success_level:.2f})")

    def _punish_lack_of_learning(self, missed_opportunity: str, severity: float):
        """Punish Luna for missed learning opportunities"""
        if self.personality_test_engine:
            self.personality_test_engine.punish_lack_of_learning(
                missed_opportunity, severity
            )

        self.learning_stats["punishment_count"] += 1
        logger.info(
            f"⚠️ Punished lack of learning: {missed_opportunity} (severity: {severity:.2f})"
        )

    def _update_user_profile(
        self, user_id: str, user_message: str, bot_response: str, quality_score: float
    ):
        """Update user profile based on interaction"""
        try:
            interaction_data = {
                "user_message": user_message,
                "bot_response": bot_response,
                "quality_score": quality_score,
                "timestamp": datetime.now().isoformat(),
                "concepts": self._extract_concepts(user_message),
                "style_insights": self._analyze_writing_style(user_message),
            }

            self.user_profile_manager.record_interaction(user_id, interaction_data)

        except Exception as e:
            logger.error(f"Failed to update user profile: {e}")

    def modify_message_for_understanding(
        self, message: str, modification_type: str = "clarify"
    ) -> str:
        """Modify a message to make it easier for Luna to understand"""
        modified_message = message

        if modification_type in self.message_patterns:
            patterns = self.message_patterns[modification_type]
            for pattern, replacement in patterns:
                modified_message = re.sub(
                    pattern, replacement, modified_message, flags=re.IGNORECASE
                )

        return modified_message

    def get_learning_summary(self) -> str:
        """Get a summary of Luna's learning progress"""
        summary = "🧠 **Luna's Learning Summary**\n\n"

        # Basic stats
        summary += (
            f"**Total Interactions:** {self.learning_stats['total_interactions']}\n"
        )
        summary += (
            f"**Successful Learnings:** {self.learning_stats['successful_learnings']}\n"
        )
        summary += f"**Failed Learnings:** {self.learning_stats['failed_learnings']}\n"
        summary += f"**Personality Evolutions:** {self.personality_evolution['personality_evolutions']}\n"
        summary += f"**Rewards Given:** {self.learning_stats['reward_count']}\n"
        summary += (
            f"**Punishments Given:** {self.learning_stats['punishment_count']}\n\n"
        )

        # Current phase
        summary += f"**Current Learning Phase:** {self.personality_evolution['current_phase'].title()}\n\n"

        # Personality traits
        summary += "**Personality Traits:**\n"
        for trait, value in self.personality_evolution["base_traits"].items():
            emoji = self._get_trait_emoji(trait, value)
            summary += f"  {emoji} {trait.replace('_', ' ').title()}: {value:.2f}\n"

        # Recent milestones
        if self.personality_evolution["learning_milestones"]:
            summary += "\n**Recent Milestones:**\n"
            recent = self.personality_evolution["learning_milestones"][-3:]
            for milestone in recent:
                summary += f"  🏆 {milestone['type'].replace('_', ' ').title()} (Score: {milestone['score']:.2f})\n"

        return summary

    def _get_trait_emoji(self, trait: str, value: float) -> str:
        """Get appropriate emoji for trait and value"""
        emoji_map = {
            "learning_enthusiasm": "🧠",
            "creative_expression": "🎨",
            "supportive_nature": "🤗",
            "inspirational_capacity": "✨",
            "adaptability": "🔄",
            "emotional_intelligence": "💝",
            "writing_expertise": "✍️",
            "motivational_ability": "💪",
        }

        base_emoji = emoji_map.get(trait, "⭐")

        # Add intensity based on value
        if value > 0.8:
            return base_emoji + "🔥"
        elif value > 0.6:
            return base_emoji + "✨"
        elif value < 0.2:
            return base_emoji + "❄️"
        else:
            return base_emoji


def initialize(framework) -> EnhancedLearningEngine:
    """Initialize the enhanced learning engine plugin"""
    return EnhancedLearningEngine(framework)
