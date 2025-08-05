#!/usr/bin/env python3
"""
Personality Creator for Luna
Automatically creates tailored personalities based on user interactions
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)


class PersonalityCreator:
    """Creates tailored personalities based on user data"""

    def __init__(self):
        self.personality_manager = None  # Will be set from external
        self.user_profile_manager = None  # Will be set from external

    def set_managers(self, personality_manager, user_profile_manager):
        """Set the manager instances"""
        self.personality_manager = personality_manager
        self.user_profile_manager = user_profile_manager

    def analyze_user_for_personality_creation(self, user_id: str) -> Dict[str, Any]:
        """Analyze user data to determine if a tailored personality should be created"""

        user_profile = self.user_profile_manager.get_or_create_profile(user_id)

        # Check if user has enough data for personality creation
        total_interactions = user_profile.get("total_interactions", 0)
        data_confidence = user_profile.get("meta_data", {}).get("data_confidence", 0.0)

        # Minimum requirements for personality creation
        if total_interactions < 10 or data_confidence < 0.3:
            return {
                "should_create": False,
                "reason": f"Insufficient data: {total_interactions} interactions, {data_confidence:.2f} confidence",
                "recommendation": "Continue collecting user data",
            }

        # Analyze user patterns
        analysis = self._analyze_user_patterns(user_profile)

        # Determine if personality creation is beneficial
        should_create = self._should_create_personality(analysis)

        return {
            "should_create": should_create,
            "analysis": analysis,
            "recommendation": self._get_recommendation(analysis, should_create),
        }

    def _analyze_user_patterns(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user patterns for personality tailoring"""

        analysis = {
            "writing_style": {},
            "communication_preferences": {},
            "personality_insights": {},
            "creative_preferences": {},
            "interaction_patterns": {},
            "strengths": [],
            "areas_for_improvement": [],
        }

        # Analyze writing profile
        writing_profile = user_profile.get("writing_profile", {})
        analysis["writing_style"] = {
            "preferred_genres": writing_profile.get("preferred_genres", []),
            "writing_style": writing_profile.get("writing_style", {}),
            "strengths": writing_profile.get("strengths", []),
            "improvement_areas": writing_profile.get("areas_for_improvement", []),
        }

        # Analyze communication preferences
        comm_prefs = user_profile.get("communication_preferences", {})
        analysis["communication_preferences"] = {
            "preferred_tone": comm_prefs.get("preferred_tone", "casual"),
            "response_length": comm_prefs.get("response_length", "medium"),
            "feedback_style": comm_prefs.get("feedback_style", "constructive"),
            "encouragement_level": comm_prefs.get("encouragement_level", "moderate"),
        }

        # Analyze personality insights
        personality = user_profile.get("personality_insights", {})
        analysis["personality_insights"] = {
            "learning_style": personality.get("learning_style", "unknown"),
            "motivation_type": personality.get("motivation_type", "unknown"),
            "communication_patterns": personality.get("communication_patterns", {}),
        }

        # Analyze creative preferences
        creative = user_profile.get("creative_preferences", {})
        analysis["creative_preferences"] = {
            "storytelling_style": creative.get("storytelling_style", "unknown"),
            "character_creation_approach": creative.get(
                "character_creation_approach", "unknown"
            ),
            "world_building_style": creative.get("world_building_style", "unknown"),
        }

        # Analyze interaction patterns
        interactions = user_profile.get("interaction_history", {}).get(
            "conversations", []
        )
        analysis["interaction_patterns"] = self._analyze_interaction_patterns(
            interactions
        )

        return analysis

    def _analyze_interaction_patterns(
        self, interactions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze interaction patterns"""

        if not interactions:
            return {}

        patterns = {
            "total_interactions": len(interactions),
            "average_length": 0,
            "common_topics": [],
            "sentiment_distribution": {},
            "command_usage": {},
            "peak_activity_times": [],
        }

        # Calculate average message length
        total_length = sum(interaction.get("length", 0) for interaction in interactions)
        patterns["average_length"] = (
            total_length / len(interactions) if interactions else 0
        )

        # Analyze topics
        all_topics = []
        for interaction in interactions:
            all_topics.extend(interaction.get("topics", []))

        # Count topic frequency
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        # Get most common topics
        patterns["common_topics"] = sorted(
            topic_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]

        # Analyze sentiment
        sentiments = [
            interaction.get("sentiment", "neutral") for interaction in interactions
        ]
        for sentiment in sentiments:
            patterns["sentiment_distribution"][sentiment] = (
                patterns["sentiment_distribution"].get(sentiment, 0) + 1
            )

        # Analyze command usage
        for interaction in interactions:
            commands = interaction.get("commands_used", [])
            for command in commands:
                patterns["command_usage"][command] = (
                    patterns["command_usage"].get(command, 0) + 1
                )

        return patterns

    def _should_create_personality(self, analysis: Dict[str, Any]) -> bool:
        """Determine if a tailored personality should be created"""

        # Check if user has distinct preferences
        has_distinct_preferences = (
            len(analysis["writing_style"]["preferred_genres"]) > 0
            or analysis["personality_insights"]["learning_style"] != "unknown"
            or analysis["creative_preferences"]["storytelling_style"] != "unknown"
        )

        # Check if user has consistent patterns
        interaction_patterns = analysis["interaction_patterns"]
        has_consistent_patterns = (
            interaction_patterns.get("total_interactions", 0) >= 10
            and len(interaction_patterns.get("common_topics", [])) > 0
        )

        # Check if user would benefit from personalization
        would_benefit = (
            analysis["communication_preferences"]["preferred_tone"] != "casual"
            or analysis["communication_preferences"]["response_length"] != "medium"
            or analysis["personality_insights"]["learning_style"] != "unknown"
        )

        return has_distinct_preferences and has_consistent_patterns and would_benefit

    def _get_recommendation(self, analysis: Dict[str, Any], should_create: bool) -> str:
        """Get recommendation based on analysis"""

        if should_create:
            # Determine best base personality
            base_personality = self._determine_best_base_personality(analysis)
            return f"Create tailored personality based on {base_personality}"
        else:
            return "Continue collecting user data for better personalization"

    def _determine_best_base_personality(self, analysis: Dict[str, Any]) -> str:
        """Determine the best base personality for the user"""

        # Check if user is focused on character roleplay
        character_roleplay_focus = self._detect_character_roleplay_interest(analysis)

        # Check if user is primarily focused on writing
        writing_focus = (
            len(analysis["writing_style"]["preferred_genres"]) > 0
            or analysis["creative_preferences"]["storytelling_style"] != "unknown"
        )

        # Check if user needs mentorship
        needs_mentorship = (
            analysis["personality_insights"]["learning_style"] != "unknown"
            or len(analysis["writing_style"]["improvement_areas"]) > 0
        )

        # Check if user has complex emotional needs
        complex_emotional = (
            analysis["communication_preferences"]["preferred_tone"] == "formal"
            or analysis["personality_insights"]["motivation_type"] != "unknown"
        )

        if character_roleplay_focus:
            return "character_roleplay"
        elif writing_focus:
            return "luna_writing"
        elif needs_mentorship:
            return "sage_mentor"
        elif complex_emotional:
            return "astra_core"
        else:
            return "luna_writing"  # Default

    def _detect_character_roleplay_interest(self, analysis: Dict[str, Any]) -> bool:
        """Detect if user is interested in character roleplay"""

        # Check interaction patterns for character-related topics
        interaction_patterns = analysis.get("interaction_patterns", {})
        common_topics = interaction_patterns.get("common_topics", [])

        character_keywords = [
            "character",
            "roleplay",
            "dialogue",
            "voice",
            "personality",
            "protagonist",
            "antagonist",
            "hero",
            "villain",
            "speak as",
            "act as",
            "be my character",
            "character development",
        ]

        # Check if any character-related topics are common
        for topic, count in common_topics:
            if any(keyword in topic.lower() for keyword in character_keywords):
                return True

        # Check writing style for character-focused content
        writing_style = analysis.get("writing_style", {})
        if writing_style.get("character_development_style") != "unknown":
            return True

        # Check creative preferences for character creation
        creative_prefs = analysis.get("creative_preferences", {})
        if creative_prefs.get("character_creation_approach") != "unknown":
            return True

        return False

    def create_tailored_personality(self, user_id: str) -> Dict[str, Any]:
        """Create a tailored personality for a user"""

        # Get user profile
        user_profile = self.user_profile_manager.get_or_create_profile(user_id)

        # Analyze user patterns
        analysis = self._analyze_user_patterns(user_profile)

        # Determine best base personality
        base_personality = self._determine_best_base_personality(analysis)

        # Create tailored personality
        tailored_personality = (
            self.personality_manager.create_user_tailored_personality(
                user_id, user_profile, base_personality
            )
        )

        # Add analysis data to personality
        tailored_personality["user_analysis"] = analysis
        tailored_personality["creation_reason"] = self._get_creation_reason(analysis)

        # Save updated personality
        file_path = (
            self.personality_manager.user_personalities_dir / f"{user_id}_tailored.json"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tailored_personality, f, indent=2, ensure_ascii=False)

        logger.info(
            f"Created tailored personality for user {user_id}: {tailored_personality['name']}"
        )
        return tailored_personality

    def _get_creation_reason(self, analysis: Dict[str, Any]) -> str:
        """Get the reason for personality creation"""

        reasons = []

        if analysis["writing_style"]["preferred_genres"]:
            genres = ", ".join(analysis["writing_style"]["preferred_genres"])
            reasons.append(f"Specific genre preferences: {genres}")

        if analysis["personality_insights"]["learning_style"] != "unknown":
            reasons.append(
                f"Distinct learning style: {analysis['personality_insights']['learning_style']}"
            )

        if analysis["communication_preferences"]["preferred_tone"] != "casual":
            reasons.append(
                f"Communication preference: {analysis['communication_preferences']['preferred_tone']}"
            )

        if analysis["creative_preferences"]["storytelling_style"] != "unknown":
            reasons.append(
                f"Creative style: {analysis['creative_preferences']['storytelling_style']}"
            )

        return "; ".join(reasons) if reasons else "General personalization needs"

    def suggest_personality_sharing(self, user_id: str) -> List[Dict[str, Any]]:
        """Suggest personality sharing opportunities"""

        user_profile = self.user_profile_manager.get_or_create_profile(user_id)

        # Find similar users
        similar_users = self.personality_manager.find_similar_users(
            user_id, user_profile
        )

        sharing_suggestions = []
        for similar_user in similar_users:
            if similar_user["similarity_score"] > 0.8:  # High similarity threshold
                sharing_suggestions.append(
                    {
                        "target_user_id": similar_user["user_id"],
                        "similarity_score": similar_user["similarity_score"],
                        "shared_interests": similar_user["shared_interests"],
                        "recommendation": "High similarity - consider sharing personality",
                    }
                )

        return sharing_suggestions

    def auto_create_personalities_for_active_users(self) -> List[Dict[str, Any]]:
        """Automatically create personalities for users who meet the criteria"""

        created_personalities = []

        # Check all users for personality creation
        for user_id, user_profile in self.user_profile_manager.profiles.items():

            # Skip if user already has a tailored personality
            if user_id in self.personality_manager.user_personalities:
                continue

            # Analyze user
            analysis_result = self.analyze_user_for_personality_creation(user_id)

            if analysis_result["should_create"]:
                try:
                    tailored_personality = self.create_tailored_personality(user_id)
                    created_personalities.append(
                        {
                            "user_id": user_id,
                            "personality_name": tailored_personality["name"],
                            "reason": analysis_result["recommendation"],
                        }
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to create personality for user {user_id}: {e}"
                    )

        return created_personalities


# Global instance
personality_creator = PersonalityCreator()
