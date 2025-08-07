#!/usr/bin/env python3
"""
User Profile Manager for Luna
Allows Luna to passively collect and manage user profile data
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)

class UserProfileManager:
    """Manages user profile data collection and analysis"""
    
    def __init__(self):
        self.profiles_dir = Path("profile/user_profile")
        self.profiles = {}
        self.load_profiles()
    
    def load_profiles(self):
        """Load all user profiles"""
        if not self.profiles_dir.exists():
            self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path in self.profiles_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                user_id = profile.get('user_id', file_path.stem)
                self.profiles[user_id] = profile
                logger.info(f"Loaded user profile: {user_id}")
            except Exception as e:
                logger.error(f"Failed to load user profile {file_path}: {e}")
    
    def get_or_create_profile(self, user_id: str, username: str = None) -> Dict[str, Any]:
        """Get existing profile or create new one"""
        if user_id not in self.profiles:
            profile = self._create_default_profile(user_id, username)
            self.profiles[user_id] = profile
            self._save_profile(user_id, profile)
        
        return self.profiles[user_id]
    
    def _create_default_profile(self, user_id: str, username: str = None) -> Dict[str, Any]:
        """Create a default user profile"""
        timestamp = datetime.now().isoformat()
        return {
            "user_id": user_id,
            "username": username or "Unknown",
            "created_date": timestamp,
            "last_interaction": timestamp,
            "total_interactions": 0,
            
            "writing_profile": {
                "preferred_genres": [],
                "writing_style": {
                    "tone": "unknown",
                    "pacing": "unknown",
                    "dialogue_style": "unknown",
                    "description_preference": "unknown",
                    "character_development_style": "unknown"
                },
                "current_projects": [],
                "completed_works": [],
                "writing_goals": [],
                "strengths": [],
                "areas_for_improvement": [],
                "inspiration_sources": [],
                "writing_habits": {
                    "preferred_time": "unknown",
                    "writing_frequency": "unknown",
                    "environment_preferences": "unknown",
                    "motivation_triggers": []
                }
            },
            
            "communication_preferences": {
                "preferred_tone": "casual",
                "response_length": "medium",
                "feedback_style": "constructive",
                "encouragement_level": "moderate",
                "criticism_tolerance": "moderate",
                "interaction_frequency": "as_needed",
                "conversation_topics": [],
                "avoided_topics": []
            },
            
            "personality_insights": {
                "learning_style": "unknown",
                "motivation_type": "unknown",
                "stress_triggers": [],
                "comfort_zones": [],
                "growth_areas": [],
                "communication_patterns": {
                    "formality_level": "casual",
                    "detail_preference": "moderate",
                    "humor_style": "unknown",
                    "conflict_approach": "unknown"
                }
            },
            
            "creative_preferences": {
                "storytelling_style": "unknown",
                "character_creation_approach": "unknown",
                "world_building_style": "unknown",
                "plot_development_preference": "unknown",
                "thematic_interests": [],
                "narrative_voice": "unknown",
                "pacing_preferences": "unknown"
            },
            
            "interaction_history": {
                "conversations": [],
                "commands_used": [],
                "successful_interactions": [],
                "challenging_interactions": [],
                "feedback_given": [],
                "preferences_expressed": []
            },
            
            "learning_data": {
                "writing_samples": [],
                "style_analysis": {},
                "improvement_areas": [],
                "success_patterns": [],
                "challenge_patterns": [],
                "adaptation_notes": []
            },
            
            "relationship_dynamics": {
                "trust_level": 0.5,
                "comfort_level": 0.5,
                "communication_effectiveness": 0.5,
                "collaboration_style": "unknown",
                "feedback_receptiveness": "moderate",
                "boundary_respect": "high"
            },
            
            "goals_and_aspirations": {
                "writing_goals": [],
                "career_aspirations": [],
                "personal_growth_areas": [],
                "creative_ambitions": [],
                "learning_objectives": []
            },
            
            "preferences_and_avoids": {
                "likes": [],
                "dislikes": [],
                "triggers": [],
                "comfort_topics": [],
                "sensitive_areas": [],
                "encouragement_style": "unknown"
            },
            
            "technical_preferences": {
                "platform_preferences": ["discord"],
                "response_format": "text",
                "interaction_frequency": "as_needed",
                "notification_preferences": "minimal",
                "privacy_concerns": [],
                "accessibility_needs": []
            },
            
            "meta_data": {
                "profile_version": "1.0",
                "last_updated": timestamp,
                "data_confidence": 0.1,
                "collection_methods": ["passive_observation", "interaction_analysis"],
                "privacy_settings": {
                    "data_collection": "enabled",
                    "learning_adaptation": "enabled",
                    "personality_evolution": "enabled"
                }
            }
        }
    
    def _save_profile(self, user_id: str, profile: Dict[str, Any]):
        """Save a user profile to file"""
        file_path = self.profiles_dir / f"{user_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
    
    def record_interaction(self, user_id: str, interaction_data: Dict[str, Any]):
        """Record an interaction and update user profile"""
        profile = self.get_or_create_profile(user_id)
        
        # Update basic stats
        profile["last_interaction"] = datetime.now().isoformat()
        profile["total_interactions"] += 1
        
        # Record interaction
        if "interaction_history" not in profile:
            profile["interaction_history"] = {}
        
        if "conversations" not in profile["interaction_history"]:
            profile["interaction_history"]["conversations"] = []
        
        interaction_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": interaction_data.get("type", "conversation"),
            "content": interaction_data.get("content", ""),
            "length": len(interaction_data.get("content", "")),
            "sentiment": interaction_data.get("sentiment", "neutral"),
            "topics": interaction_data.get("topics", []),
            "commands_used": interaction_data.get("commands_used", [])
        }
        
        profile["interaction_history"]["conversations"].append(interaction_entry)
        
        # Analyze and update preferences
        self._analyze_interaction(profile, interaction_data)
        
        # Save updated profile
        self._save_profile(user_id, profile)
        self.profiles[user_id] = profile
    
    def _analyze_interaction(self, profile: Dict[str, Any], interaction_data: Dict[str, Any]):
        """Analyze interaction and update user preferences"""
        content = interaction_data.get("content", "").lower()
        
        # Analyze writing-related content
        if any(word in content for word in ["write", "story", "character", "plot", "novel", "book"]):
            self._update_writing_preferences(profile, content)
        
        # Analyze communication style
        self._update_communication_preferences(profile, content)
        
        # Analyze personality insights
        self._update_personality_insights(profile, interaction_data)
        
        # Update data confidence
        profile["meta_data"]["data_confidence"] = min(1.0, profile["meta_data"]["data_confidence"] + 0.01)
        profile["meta_data"]["last_updated"] = datetime.now().isoformat()
    
    def _update_writing_preferences(self, profile: Dict[str, Any], content: str):
        """Update writing preferences based on content analysis"""
        writing_profile = profile.get("writing_profile", {})
        
        # Detect genres
        genre_keywords = {
            "fantasy": ["fantasy", "magic", "wizard", "dragon", "medieval"],
            "sci-fi": ["science fiction", "space", "futuristic", "technology", "alien"],
            "romance": ["romance", "love", "relationship", "dating"],
            "mystery": ["mystery", "detective", "crime", "suspense", "thriller"],
            "horror": ["horror", "scary", "fear", "supernatural", "ghost"]
        }
        
        for genre, keywords in genre_keywords.items():
            if any(keyword in content for keyword in keywords):
                if genre not in writing_profile.get("preferred_genres", []):
                    writing_profile.setdefault("preferred_genres", []).append(genre)
        
        # Detect writing style preferences
        if any(word in content for word in ["detailed", "descriptive", "vivid"]):
            writing_profile.setdefault("writing_style", {})["description_preference"] = "detailed"
        elif any(word in content for word in ["fast", "quick", "pacing"]):
            writing_profile.setdefault("writing_style", {})["pacing"] = "fast"
    
    def _update_communication_preferences(self, profile: Dict[str, Any], content: str):
        """Update communication preferences based on content analysis"""
        comm_prefs = profile.get("communication_preferences", {})
        
        # Analyze tone preferences
        if any(word in content for word in ["casual", "informal", "relaxed"]):
            comm_prefs["preferred_tone"] = "casual"
        elif any(word in content for word in ["formal", "professional", "serious"]):
            comm_prefs["preferred_tone"] = "formal"
        
        # Analyze response length preference
        if len(content) > 200:
            comm_prefs["response_length"] = "long"
        elif len(content) < 50:
            comm_prefs["response_length"] = "short"
    
    def _update_personality_insights(self, profile: Dict[str, Any], interaction_data: Dict[str, Any]):
        """Update personality insights based on interaction"""
        personality = profile.get("personality_insights", {})
        
        # Analyze learning style
        content = interaction_data.get("content", "").lower()
        if any(word in content for word in ["show me", "example", "demonstrate"]):
            personality["learning_style"] = "visual"
        elif any(word in content for word in ["explain", "tell me", "describe"]):
            personality["learning_style"] = "auditory"
        elif any(word in content for word in ["try", "practice", "hands-on"]):
            personality["learning_style"] = "kinesthetic"
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences for personalization"""
        profile = self.get_or_create_profile(user_id)
        return {
            "writing_style": profile.get("writing_profile", {}).get("writing_style", {}),
            "communication_preferences": profile.get("communication_preferences", {}),
            "personality_insights": profile.get("personality_insights", {}),
            "creative_preferences": profile.get("creative_preferences", {}),
            "relationship_dynamics": profile.get("relationship_dynamics", {})
        }
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user interaction statistics"""
        profile = self.get_or_create_profile(user_id)
        return {
            "total_interactions": profile.get("total_interactions", 0),
            "data_confidence": profile.get("meta_data", {}).get("data_confidence", 0.0),
            "last_interaction": profile.get("last_interaction"),
            "preferred_genres": profile.get("writing_profile", {}).get("preferred_genres", []),
            "communication_style": profile.get("communication_preferences", {}).get("preferred_tone", "unknown")
        }
    
    def suggest_personality(self, user_id: str, context: str) -> Dict[str, Any]:
        """Suggest a personality based on user profile and context"""
        profile = self.get_or_create_profile(user_id)
        preferences = self.get_user_preferences(user_id)
        
        # Analyze context and user preferences to suggest personality
        suggestion = {
            "context": context,
            "suggested_personality": "Luna",  # Default
            "confidence": 0.5,
            "reasoning": "Based on user preferences and interaction history"
        }
        
        # Add logic to suggest different personalities based on context and user data
        if "writing" in context.lower() or "story" in context.lower():
            suggestion["suggested_personality"] = "Luna"
            suggestion["confidence"] = 0.8
        elif "wisdom" in context.lower() or "advice" in context.lower():
            suggestion["suggested_personality"] = "Sage"
            suggestion["confidence"] = 0.7
        
        return suggestion

# Global instance
user_profile_manager = UserProfileManager() 