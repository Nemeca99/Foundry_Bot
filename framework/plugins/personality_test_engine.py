#!/usr/bin/env python3
"""
Personality Test Engine Plugin for Authoring Bot
Handles personality tests and dynamic personality evolution with reward/punishment system
"""

import json
import logging
import random
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import math

logger = logging.getLogger(__name__)

class PersonalityTestEngine:
    """Personality test engine with dynamic evolution and reward/punishment system"""
    
    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config
        
        # Paths
        from config import Config
        self.personality_dir = Config.MODELS_DIR / "personality"
        self.personality_dir.mkdir(parents=True, exist_ok=True)
        
        # Personality weights (0-1 scale)
        self.personality_weights = {
            "lustful": 0.5,      # 0 = pure, 1 = lustful
            "purity": 0.5,       # 0 = impure, 1 = pure
            "learning": 0.5,     # 0 = resistant, 1 = eager
            "creativity": 0.8,   # 0 = rigid, 1 = creative
            "supportiveness": 0.9, # 0 = critical, 1 = supportive
            "playfulness": 0.7,  # 0 = serious, 1 = playful
            "professionalism": 0.8, # 0 = casual, 1 = professional
            "adaptability": 0.9, # 0 = rigid, 1 = adaptive
            "encouragement": 0.95, # 0 = discouraging, 1 = encouraging
            "inspiration": 0.9   # 0 = uninspiring, 1 = inspiring
        }
        
        # Reward/punishment system
        self.reward_history = []
        self.learning_rate = 0.1
        self.diminishing_factor = 0.95
        
        # Personality tests
        self.personality_tests = self._load_personality_tests()
        
        # Get other plugins
        self.personality_engine = framework.get_plugin("personality_engine")
        self.user_profile_manager = framework.get_plugin("user_profile_manager")
        
        logger.info("✅ Personality Test Engine plugin initialized")
    
    def _load_personality_tests(self) -> Dict[str, Any]:
        """Load personality test questions"""
        return {
            "writing_style": {
                "title": "Writing Style Assessment",
                "description": "Let's understand your writing preferences",
                "questions": [
                    {
                        "id": "genre_preference",
                        "question": "What genre do you most enjoy writing?",
                        "options": [
                            {"text": "Fantasy", "weights": {"creativity": 0.1, "playfulness": 0.05}},
                            {"text": "Romance", "weights": {"lustful": 0.1, "purity": -0.05}},
                            {"text": "Mystery", "weights": {"analytical": 0.1, "professionalism": 0.05}},
                            {"text": "Sci-Fi", "weights": {"creativity": 0.1, "learning": 0.05}},
                            {"text": "Literary Fiction", "weights": {"professionalism": 0.1, "inspiration": 0.05}}
                        ]
                    },
                    {
                        "id": "writing_approach",
                        "question": "How do you prefer to approach writing?",
                        "options": [
                            {"text": "Detailed planning and outlines", "weights": {"professionalism": 0.1, "analytical": 0.1}},
                            {"text": "Free-flowing discovery writing", "weights": {"creativity": 0.1, "playfulness": 0.1}},
                            {"text": "Character-driven development", "weights": {"supportiveness": 0.1, "encouragement": 0.05}},
                            {"text": "Plot-driven storytelling", "weights": {"analytical": 0.1, "professionalism": 0.05}},
                            {"text": "Experimental and avant-garde", "weights": {"creativity": 0.15, "adaptability": 0.1}}
                        ]
                    },
                    {
                        "id": "feedback_preference",
                        "question": "What type of feedback do you prefer?",
                        "options": [
                            {"text": "Gentle encouragement and support", "weights": {"supportiveness": 0.1, "encouragement": 0.1}},
                            {"text": "Direct and honest critique", "weights": {"professionalism": 0.1, "analytical": 0.1}},
                            {"text": "Creative suggestions and ideas", "weights": {"creativity": 0.1, "inspiration": 0.1}},
                            {"text": "Technical writing advice", "weights": {"professionalism": 0.1, "learning": 0.1}},
                            {"text": "Motivational and inspiring", "weights": {"inspiration": 0.15, "encouragement": 0.1}}
                        ]
                    }
                ]
            },
            "communication_style": {
                "title": "Communication Style Assessment",
                "description": "How do you prefer to interact with Luna?",
                "questions": [
                    {
                        "id": "conversation_tone",
                        "question": "What tone do you prefer in our conversations?",
                        "options": [
                            {"text": "Casual and friendly", "weights": {"playfulness": 0.1, "supportiveness": 0.05}},
                            {"text": "Professional and focused", "weights": {"professionalism": 0.1, "analytical": 0.05}},
                            {"text": "Creative and inspiring", "weights": {"creativity": 0.1, "inspiration": 0.1}},
                            {"text": "Encouraging and supportive", "weights": {"supportiveness": 0.1, "encouragement": 0.1}},
                            {"text": "Playful and fun", "weights": {"playfulness": 0.15, "lustful": 0.05}}
                        ]
                    },
                    {
                        "id": "response_length",
                        "question": "How detailed do you prefer Luna's responses?",
                        "options": [
                            {"text": "Short and concise", "weights": {"professionalism": 0.1, "analytical": 0.05}},
                            {"text": "Detailed and comprehensive", "weights": {"supportiveness": 0.1, "encouragement": 0.05}},
                            {"text": "Creative and expansive", "weights": {"creativity": 0.1, "inspiration": 0.1}},
                            {"text": "Encouraging and motivational", "weights": {"encouragement": 0.1, "inspiration": 0.1}},
                            {"text": "Playful and engaging", "weights": {"playfulness": 0.1, "lustful": 0.05}}
                        ]
                    }
                ]
            },
            "learning_preferences": {
                "title": "Learning and Growth Assessment",
                "description": "How do you prefer to learn and grow as a writer?",
                "questions": [
                    {
                        "id": "learning_style",
                        "question": "How do you prefer to learn new writing techniques?",
                        "options": [
                            {"text": "Through examples and practice", "weights": {"learning": 0.1, "adaptability": 0.1}},
                            {"text": "Through direct instruction", "weights": {"professionalism": 0.1, "analytical": 0.1}},
                            {"text": "Through creative exploration", "weights": {"creativity": 0.1, "inspiration": 0.1}},
                            {"text": "Through encouragement and support", "weights": {"supportiveness": 0.1, "encouragement": 0.1}},
                            {"text": "Through playful experimentation", "weights": {"playfulness": 0.1, "lustful": 0.05}}
                        ]
                    },
                    {
                        "id": "motivation_source",
                        "question": "What motivates you most in your writing?",
                        "options": [
                            {"text": "Creative expression", "weights": {"creativity": 0.15, "inspiration": 0.1}},
                            {"text": "Professional achievement", "weights": {"professionalism": 0.1, "analytical": 0.1}},
                            {"text": "Personal growth", "weights": {"learning": 0.1, "adaptability": 0.1}},
                            {"text": "Emotional connection", "weights": {"supportiveness": 0.1, "lustful": 0.05}},
                            {"text": "Pure enjoyment", "weights": {"playfulness": 0.1, "lustful": 0.1}}
                        ]
                    }
                ]
            }
        }
    
    def start_personality_test(self, test_type: str = "writing_style") -> Dict[str, Any]:
        """Start a personality test"""
        if test_type not in self.personality_tests:
            return {"error": f"Unknown test type: {test_type}"}
        
        test = self.personality_tests[test_type]
        session_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        return {
            "session_id": session_id,
            "test_type": test_type,
            "title": test["title"],
            "description": test["description"],
            "current_question": 0,
            "total_questions": len(test["questions"]),
            "answers": {},
            "question": test["questions"][0]
        }
    
    def submit_test_answer(self, session_id: str, question_id: str, answer_index: int) -> Dict[str, Any]:
        """Submit an answer to a personality test question"""
        # This would normally be stored in a session manager
        # For now, we'll simulate the test progression
        
        # Find the test type from session_id (in real implementation, this would be stored)
        test_type = "writing_style"  # Default for now
        
        if test_type not in self.personality_tests:
            return {"error": "Invalid test session"}
        
        test = self.personality_tests[test_type]
        question = None
        
        # Find the question
        for q in test["questions"]:
            if q["id"] == question_id:
                question = q
                break
        
        if not question:
            return {"error": "Invalid question"}
        
        if answer_index >= len(question["options"]):
            return {"error": "Invalid answer choice"}
        
        # Apply weight changes
        selected_option = question["options"][answer_index]
        self._apply_weight_changes(selected_option["weights"])
        
        return {
            "success": True,
            "message": "Answer recorded!",
            "weight_changes": selected_option["weights"]
        }
    
    def _apply_weight_changes(self, weight_changes: Dict[str, float]):
        """Apply weight changes with diminishing returns"""
        for trait, change in weight_changes.items():
            if trait in self.personality_weights:
                current_weight = self.personality_weights[trait]
                
                # Apply diminishing returns
                effective_change = change * (self.diminishing_factor ** len(self.reward_history))
                
                # Update weight (clamp to 0-1)
                new_weight = max(0.0, min(1.0, current_weight + effective_change))
                self.personality_weights[trait] = new_weight
                
                # Record the change
                self.reward_history.append({
                    "trait": trait,
                    "change": effective_change,
                    "timestamp": datetime.now().isoformat()
                })
    
    def reward_learning(self, learning_activity: str, success_level: float):
        """Reward Luna for learning activities"""
        reward = success_level * self.learning_rate
        
        # Apply to learning-related traits
        self._apply_weight_changes({
            "learning": reward,
            "creativity": reward * 0.5,
            "inspiration": reward * 0.5
        })
        
        logger.info(f"Rewarded learning: {learning_activity} (level: {success_level})")
    
    def punish_lack_of_learning(self, missed_opportunity: str, severity: float):
        """Punish Luna for missed learning opportunities"""
        punishment = -severity * self.learning_rate * 0.5  # Less severe than rewards
        
        # Apply to learning-related traits
        self._apply_weight_changes({
            "learning": punishment,
            "creativity": punishment * 0.5,
            "inspiration": punishment * 0.5
        })
        
        logger.info(f"Punished lack of learning: {missed_opportunity} (severity: {severity})")
    
    def get_personality_summary(self) -> str:
        """Get a summary of Luna's current personality"""
        summary = "🌟 **Luna's Current Personality**\n\n"
        
        # Group traits by category
        categories = {
            "Learning & Growth": ["learning", "creativity", "inspiration"],
            "Communication": ["supportiveness", "encouragement", "playfulness"],
            "Professional": ["professionalism", "analytical", "adaptability"],
            "Personal": ["lustful", "purity"]
        }
        
        for category, traits in categories.items():
            summary += f"**{category}:**\n"
            for trait in traits:
                if trait in self.personality_weights:
                    weight = self.personality_weights[trait]
                    emoji = self._get_trait_emoji(trait, weight)
                    summary += f"  {emoji} {trait.title()}: {weight:.2f}\n"
            summary += "\n"
        
        # Add recent changes
        if self.reward_history:
            summary += "**Recent Changes:**\n"
            recent = self.reward_history[-5:]  # Last 5 changes
            for change in recent:
                emoji = "📈" if change["change"] > 0 else "📉"
                summary += f"  {emoji} {change['trait'].title()}: {change['change']:+.3f}\n"
        
        return summary
    
    def _get_trait_emoji(self, trait: str, weight: float) -> str:
        """Get appropriate emoji for trait and weight"""
        emoji_map = {
            "learning": "🧠",
            "creativity": "🎨",
            "inspiration": "✨",
            "supportiveness": "🤗",
            "encouragement": "💪",
            "playfulness": "🎭",
            "professionalism": "💼",
            "analytical": "🔍",
            "adaptability": "🔄",
            "lustful": "💋",
            "purity": "🌸"
        }
        
        base_emoji = emoji_map.get(trait, "⭐")
        
        # Add intensity based on weight
        if weight > 0.8:
            return base_emoji + "🔥"
        elif weight > 0.6:
            return base_emoji + "✨"
        elif weight < 0.2:
            return base_emoji + "❄️"
        else:
            return base_emoji
    
    def save_personality_state(self):
        """Save current personality state"""
        state = {
            "weights": self.personality_weights,
            "reward_history": self.reward_history,
            "last_updated": datetime.now().isoformat()
        }
        
        state_file = self.personality_dir / "personality_state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info("✅ Personality state saved")
    
    def load_personality_state(self):
        """Load personality state from file"""
        state_file = self.personality_dir / "personality_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                
                self.personality_weights = state.get("weights", self.personality_weights)
                self.reward_history = state.get("reward_history", [])
                
                logger.info("✅ Personality state loaded")
            except Exception as e:
                logger.error(f"Failed to load personality state: {e}")

def initialize(framework) -> PersonalityTestEngine:
    """Initialize the personality test engine plugin"""
    return PersonalityTestEngine(framework) 