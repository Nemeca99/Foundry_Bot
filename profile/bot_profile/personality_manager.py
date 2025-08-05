#!/usr/bin/env python3
"""
Personality Manager for Luna
Allows Luna to create, modify, and manage her own personalities
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PersonalityManager:
    """Manages Luna's personality system"""

    def __init__(self):
        self.personalities_dir = Path("profile/bot_profile/personality")
        self.user_personalities_dir = Path(
            "profile/bot_profile/personality/user_tailored"
        )
        self.template_file = self.personalities_dir / "personality_template.json"
        self.active_personality = None
        self.personalities = {}
        self.user_personalities = {}  # user_id -> personality_name
        self.load_personalities()

    def load_personalities(self):
        """Load all available personalities"""
        if not self.personalities_dir.exists():
            self.personalities_dir.mkdir(parents=True, exist_ok=True)

        if not self.user_personalities_dir.exists():
            self.user_personalities_dir.mkdir(parents=True, exist_ok=True)

        # Load general personalities
        for file_path in self.personalities_dir.glob("*.json"):
            if file_path.name != "personality_template.json":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        personality = json.load(f)
                    self.personalities[personality["name"]] = personality
                    logger.info(f"Loaded personality: {personality['name']}")
                except Exception as e:
                    logger.error(f"Failed to load personality {file_path}: {e}")

        # Load user-tailored personalities
        for file_path in self.user_personalities_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    personality = json.load(f)
                user_id = personality.get("tailored_for_user")
                if user_id:
                    self.user_personalities[user_id] = personality["name"]
                    self.personalities[personality["name"]] = personality
                    logger.info(
                        f"Loaded user-tailored personality: {personality['name']} for user {user_id}"
                    )
            except Exception as e:
                logger.error(f"Failed to load user personality {file_path}: {e}")

    def get_personality(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific personality"""
        return self.personalities.get(name)

    def get_user_tailored_personality(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get personality tailored for specific user"""
        personality_name = self.user_personalities.get(user_id)
        if personality_name:
            return self.personalities.get(personality_name)
        return None

    def list_personalities(self) -> List[str]:
        """List all available personalities"""
        return list(self.personalities.keys())

    def list_user_tailored_personalities(self) -> Dict[str, str]:
        """List user-tailored personalities"""
        return self.user_personalities.copy()

    def create_user_tailored_personality(
        self,
        user_id: str,
        user_data: Dict[str, Any],
        base_personality: str = "luna_writing",
    ) -> Dict[str, Any]:
        """Create a personality tailored for a specific user based on their data"""

        # Get base personality
        base = self.personalities.get(base_personality, {})
        if not base:
            raise ValueError(f"Base personality '{base_personality}' not found")

        # Create tailored personality
        timestamp = datetime.now().isoformat()
        tailored_name = f"Luna_{user_id}_Tailored"

        personality = base.copy()
        personality.update(
            {
                "name": tailored_name,
                "tailored_for_user": user_id,
                "created_by": "Luna",
                "created_date": timestamp,
                "last_modified": timestamp,
                "description": f"Personality tailored for user {user_id} based on their writing and conversation patterns",
                "status": "active",
                "base_personality": base_personality,
            }
        )

        # Tailor based on user data
        self._tailor_personality_for_user(personality, user_data)

        # Save tailored personality
        file_path = self.user_personalities_dir / f"{user_id}_tailored.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(personality, f, indent=2, ensure_ascii=False)

        self.personalities[tailored_name] = personality
        self.user_personalities[user_id] = tailored_name
        logger.info(f"Created tailored personality for user {user_id}: {tailored_name}")
        return personality

    def _tailor_personality_for_user(
        self, personality: Dict[str, Any], user_data: Dict[str, Any]
    ):
        """Tailor personality based on user data"""

        # Get user preferences
        writing_profile = user_data.get("writing_profile", {})
        communication_prefs = user_data.get("communication_preferences", {})
        personality_insights = user_data.get("personality_insights", {})
        creative_prefs = user_data.get("creative_preferences", {})

        # Adjust communication style based on user preferences
        if communication_prefs.get("preferred_tone") == "formal":
            personality["communication"][
                "tone"
            ] = "More formal and professional, while maintaining intellectual enthusiasm"
        elif communication_prefs.get("preferred_tone") == "casual":
            personality["communication"][
                "tone"
            ] = "Relaxed and casual, with natural geeky enthusiasm"

        # Adjust based on writing style
        writing_style = writing_profile.get("writing_style", {})
        if writing_style.get("description_preference") == "detailed":
            personality["dynamics"]["behavioral_rules"].append(
                "Provides detailed, descriptive responses that match user's preference for depth"
            )
        elif writing_style.get("pacing") == "fast":
            personality["dynamics"]["behavioral_rules"].append(
                "Keeps responses concise and fast-paced to match user's writing style"
            )

        # Adjust based on preferred genres
        preferred_genres = writing_profile.get("preferred_genres", [])
        if preferred_genres:
            genre_knowledge = (
                f"Deep knowledge and passion for {', '.join(preferred_genres)} genres"
            )
            personality["dynamics"]["writing_kinks"].append(genre_knowledge)

        # Adjust based on learning style
        learning_style = personality_insights.get("learning_style", "unknown")
        if learning_style == "visual":
            personality["dynamics"]["behavioral_rules"].append(
                "Uses visual descriptions and examples to help user understand concepts"
            )
        elif learning_style == "auditory":
            personality["dynamics"]["behavioral_rules"].append(
                "Explains concepts through detailed verbal descriptions and discussions"
            )

        # Adjust based on creative preferences
        storytelling_style = creative_prefs.get("storytelling_style", "unknown")
        if storytelling_style != "unknown":
            personality["dynamics"]["behavioral_rules"].append(
                f"Adapts to user's {storytelling_style} storytelling style"
            )

        # Special handling for character roleplay
        if (
            personality.get("name", "").lower().startswith("luna_")
            and "character" in personality.get("identity", {}).get("role", "").lower()
        ):
            self._tailor_for_character_roleplay(personality, user_data)

    def share_personality_between_users(
        self, source_user_id: str, target_user_id: str, similarity_score: float = 0.8
    ) -> bool:
        """Share a user-tailored personality with another user if they're similar"""

        source_personality = self.get_user_tailored_personality(source_user_id)
        if not source_personality:
            return False

        # Create shared personality
        shared_name = f"Luna_Shared_{source_user_id}_{target_user_id}"

        shared_personality = source_personality.copy()
        shared_personality.update(
            {
                "name": shared_name,
                "shared_between_users": [source_user_id, target_user_id],
                "similarity_score": similarity_score,
                "created_date": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat(),
                "description": f"Shared personality between users {source_user_id} and {target_user_id}",
                "status": "active",
            }
        )

        # Save shared personality
        file_path = (
            self.user_personalities_dir
            / f"shared_{source_user_id}_{target_user_id}.json"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(shared_personality, f, indent=2, ensure_ascii=False)

        self.personalities[shared_name] = shared_personality
        self.user_personalities[target_user_id] = shared_name
        logger.info(
            f"Shared personality between users {source_user_id} and {target_user_id}"
        )
        return True

    def find_similar_users(
        self, user_id: str, user_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Find users with similar preferences for personality sharing"""
        similar_users = []

        # Load all user profiles to compare
        from profile.user_profile.user_profile_manager import user_profile_manager

        for other_user_id, other_profile in user_profile_manager.profiles.items():
            if other_user_id == user_id:
                continue

            similarity_score = self._calculate_user_similarity(user_data, other_profile)
            if similarity_score > 0.7:  # High similarity threshold
                similar_users.append(
                    {
                        "user_id": other_user_id,
                        "similarity_score": similarity_score,
                        "shared_interests": self._find_shared_interests(
                            user_data, other_profile
                        ),
                    }
                )

        # Sort by similarity score
        similar_users.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similar_users

    def _calculate_user_similarity(
        self, user1_data: Dict[str, Any], user2_data: Dict[str, Any]
    ) -> float:
        """Calculate similarity between two users"""
        score = 0.0
        total_factors = 0

        # Compare writing preferences
        genres1 = set(user1_data.get("writing_profile", {}).get("preferred_genres", []))
        genres2 = set(user2_data.get("writing_profile", {}).get("preferred_genres", []))
        if genres1 and genres2:
            genre_similarity = len(genres1.intersection(genres2)) / len(
                genres1.union(genres2)
            )
            score += genre_similarity
            total_factors += 1

        # Compare communication preferences
        tone1 = user1_data.get("communication_preferences", {}).get(
            "preferred_tone", ""
        )
        tone2 = user2_data.get("communication_preferences", {}).get(
            "preferred_tone", ""
        )
        if tone1 == tone2 and tone1:
            score += 1.0
            total_factors += 1

        # Compare learning styles
        style1 = user1_data.get("personality_insights", {}).get("learning_style", "")
        style2 = user2_data.get("personality_insights", {}).get("learning_style", "")
        if style1 == style2 and style1 != "unknown":
            score += 1.0
            total_factors += 1

        return score / total_factors if total_factors > 0 else 0.0

    def _find_shared_interests(
        self, user1_data: Dict[str, Any], user2_data: Dict[str, Any]
    ) -> List[str]:
        """Find shared interests between users"""
        shared = []

        # Compare genres
        genres1 = set(user1_data.get("writing_profile", {}).get("preferred_genres", []))
        genres2 = set(user2_data.get("writing_profile", {}).get("preferred_genres", []))
        shared_genres = genres1.intersection(genres2)
        if shared_genres:
            shared.append(f"Shared genres: {', '.join(shared_genres)}")

        # Compare communication styles
        tone1 = user1_data.get("communication_preferences", {}).get(
            "preferred_tone", ""
        )
        tone2 = user2_data.get("communication_preferences", {}).get(
            "preferred_tone", ""
        )
        if tone1 == tone2 and tone1:
            shared.append(f"Similar communication style: {tone1}")

        return shared

    def _tailor_for_character_roleplay(
        self, personality: Dict[str, Any], user_data: Dict[str, Any]
    ):
        """Special tailoring for character roleplay personalities"""

        # Get user's writing samples for style analysis
        learning_data = user_data.get("learning_data", {})
        writing_samples = learning_data.get("writing_samples", [])

        # Analyze writing style patterns
        if writing_samples:
            style_patterns = self._analyze_writing_style_patterns(writing_samples)

            # Add style-specific behavioral rules
            if style_patterns.get("dialogue_heavy"):
                personality["dynamics"]["behavioral_rules"].append(
                    "Focuses on dialogue and character interactions, matching user's dialogue-heavy style"
                )

            if style_patterns.get("descriptive"):
                personality["dynamics"]["behavioral_rules"].append(
                    "Provides rich descriptions and narrative detail, matching user's descriptive style"
                )

            if style_patterns.get("action_oriented"):
                personality["dynamics"]["behavioral_rules"].append(
                    "Emphasizes action and movement, matching user's action-oriented style"
                )

        # Add character roleplay specific features
        personality["character_roleplay_features"] = {
            "voice_learning": "Learns and mimics character speech patterns and dialogue styles",
            "personality_embodiment": "Fully embodies character personalities, motivations, and behavioral patterns",
            "narrative_consistency": "Maintains story consistency and character development arcs",
            "writing_style_matching": "Adapts to match your narrative voice and writing style",
            "character_development": "Assists in character development while maintaining authenticity",
            "world_building_integration": "Incorporates world-building elements into character interactions",
        }

        # Add performance metrics for character roleplay
        personality["performance_metrics"]["voice_matching_accuracy"] = 0.0
        personality["performance_metrics"]["narrative_consistency"] = 0.0

    def _analyze_writing_style_patterns(
        self, writing_samples: List[str]
    ) -> Dict[str, bool]:
        """Analyze writing samples for style patterns"""

        patterns = {
            "dialogue_heavy": False,
            "descriptive": False,
            "action_oriented": False,
            "character_focused": False,
        }

        for sample in writing_samples:
            sample_lower = sample.lower()

            # Check for dialogue patterns
            if (
                '"' in sample
                or "'" in sample
                or "said" in sample_lower
                or "asked" in sample_lower
            ):
                patterns["dialogue_heavy"] = True

            # Check for descriptive patterns
            if any(
                word in sample_lower
                for word in ["beautiful", "detailed", "vivid", "rich", "colorful"]
            ):
                patterns["descriptive"] = True

            # Check for action patterns
            if any(
                word in sample_lower
                for word in ["moved", "ran", "jumped", "fought", "action", "quickly"]
            ):
                patterns["action_oriented"] = True

            # Check for character focus
            if any(
                word in sample_lower
                for word in ["character", "personality", "motivation", "development"]
            ):
                patterns["character_focused"] = True

        return patterns

    def create_personality(
        self, name: str, description: str, base_template: str = None
    ) -> Dict[str, Any]:
        """Create a new personality"""
        if name in self.personalities:
            raise ValueError(f"Personality '{name}' already exists")

        # Load template
        if base_template and base_template in self.personalities:
            template = self.personalities[base_template].copy()
        else:
            with open(self.template_file, "r", encoding="utf-8") as f:
                template = json.load(f)

        # Initialize new personality
        timestamp = datetime.now().isoformat()
        personality = template.copy()
        personality.update(
            {
                "name": name,
                "created_by": "Luna",
                "created_date": timestamp,
                "last_modified": timestamp,
                "description": description,
                "status": "active",
            }
        )

        # Save personality
        file_path = self.personalities_dir / f"{name.lower().replace(' ', '_')}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(personality, f, indent=2, ensure_ascii=False)

        self.personalities[name] = personality
        logger.info(f"Created new personality: {name}")
        return personality

    def modify_personality(
        self, name: str, modifications: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Modify an existing personality"""
        if name not in self.personalities:
            raise ValueError(f"Personality '{name}' not found")

        personality = self.personalities[name].copy()
        personality.update(modifications)
        personality["last_modified"] = datetime.now().isoformat()

        # Save modified personality
        file_path = self.personalities_dir / f"{name.lower().replace(' ', '_')}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(personality, f, indent=2, ensure_ascii=False)

        self.personalities[name] = personality
        logger.info(f"Modified personality: {name}")
        return personality

    def delete_personality(self, name: str) -> bool:
        """Delete a personality"""
        if name not in self.personalities:
            return False

        file_path = self.personalities_dir / f"{name.lower().replace(' ', '_')}.json"
        if file_path.exists():
            file_path.unlink()

        del self.personalities[name]
        logger.info(f"Deleted personality: {name}")
        return True

    def activate_personality(self, name: str) -> bool:
        """Activate a personality for use"""
        if name not in self.personalities:
            return False

        self.active_personality = name
        logger.info(f"Activated personality: {name}")
        return True

    def get_active_personality(self) -> Optional[Dict[str, Any]]:
        """Get the currently active personality"""
        if self.active_personality:
            return self.personalities.get(self.active_personality)
        return None

    def record_interaction(
        self, personality_name: str, interaction_data: Dict[str, Any]
    ):
        """Record an interaction for a personality"""
        if personality_name not in self.personalities:
            return

        personality = self.personalities[personality_name]

        # Update interaction history
        if "learning_adaptation" not in personality:
            personality["learning_adaptation"] = {}

        if "conversation_history" not in personality["learning_adaptation"]:
            personality["learning_adaptation"]["conversation_history"] = []

        interaction_data["timestamp"] = datetime.now().isoformat()
        personality["learning_adaptation"]["conversation_history"].append(
            interaction_data
        )

        # Update performance metrics
        if "performance_metrics" not in personality:
            personality["performance_metrics"] = {
                "total_interactions": 0,
                "successful_interactions": 0,
                "user_satisfaction": 0.0,
                "emotional_consistency": 0.0,
                "character_depth": 0.0,
            }

        personality["performance_metrics"]["total_interactions"] += 1

        # Save updated personality
        file_path = (
            self.personalities_dir
            / f"{personality_name.lower().replace(' ', '_')}.json"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(personality, f, indent=2, ensure_ascii=False)

        self.personalities[personality_name] = personality

    def evolve_personality(self, name: str, evolution_data: Dict[str, Any]):
        """Evolve a personality based on interactions"""
        if name not in self.personalities:
            return

        personality = self.personalities[name]

        # Record evolution
        if "learning_adaptation" not in personality:
            personality["learning_adaptation"] = {}

        if "personality_evolution" not in personality["learning_adaptation"]:
            personality["learning_adaptation"]["personality_evolution"] = []

        evolution_entry = {
            "timestamp": datetime.now().isoformat(),
            "changes": evolution_data,
        }
        personality["learning_adaptation"]["personality_evolution"].append(
            evolution_entry
        )

        # Apply evolution changes
        if "emotional_profile" in evolution_data:
            personality["emotional_profile"].update(evolution_data["emotional_profile"])

        if "communication" in evolution_data:
            personality["communication"].update(evolution_data["communication"])

        if "dynamics" in evolution_data:
            personality["dynamics"].update(evolution_data["dynamics"])

        personality["last_modified"] = datetime.now().isoformat()

        # Save evolved personality
        file_path = self.personalities_dir / f"{name.lower().replace(' ', '_')}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(personality, f, indent=2, ensure_ascii=False)

        self.personalities[name] = personality
        logger.info(f"Evolved personality: {name}")

    def get_personality_stats(self, name: str) -> Dict[str, Any]:
        """Get statistics for a personality"""
        if name not in self.personalities:
            return {}

        personality = self.personalities[name]
        stats = {
            "name": name,
            "created_date": personality.get("created_date"),
            "last_modified": personality.get("last_modified"),
            "usage_count": personality.get("usage_count", 0),
            "success_rate": personality.get("success_rate", 0.0),
            "total_interactions": 0,
            "evolution_count": 0,
        }

        if "learning_adaptation" in personality:
            adaptation = personality["learning_adaptation"]
            stats["total_interactions"] = len(
                adaptation.get("conversation_history", [])
            )
            stats["evolution_count"] = len(adaptation.get("personality_evolution", []))

        if "performance_metrics" in personality:
            stats.update(personality["performance_metrics"])

        return stats

    def generate_personality_suggestion(
        self, context: str, user_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a personality suggestion based on context and user preferences"""
        # This would use AI to generate personality suggestions
        # For now, return a basic template
        return {
            "name": "Suggested Personality",
            "description": f"AI-generated personality for: {context}",
            "suggested_traits": [],
            "suggested_dynamics": [],
            "confidence": 0.0,
        }


# Global instance
personality_manager = PersonalityManager()
