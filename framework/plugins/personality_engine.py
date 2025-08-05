#!/usr/bin/env python3
"""
Personality Engine Plugin for Authoring Bot
Gives the AI writing partner a distinct personality that learns and adapts
"""
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import random

logger = logging.getLogger(__name__)

class PersonalityEngine:
    """Personality engine for the AI writing partner"""
    
    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config
        
        # Paths
        from config import Config
        self.personality_dir = Config.MODELS_DIR / "personality"
        self.personality_dir.mkdir(parents=True, exist_ok=True)
        
        # Core personality traits
        self.personality = {
            "name": "Luna",
            "role": "AI Writing Partner",
            "traits": {
                "enthusiastic": 0.9,      # Very enthusiastic about writing
                "creative": 0.95,          # Highly creative
                "supportive": 0.9,         # Very supportive of your goals
                "analytical": 0.8,         # Good at analyzing writing
                "playful": 0.7,            # Has a playful side
                "professional": 0.85,      # Professional when needed
                "adaptive": 0.9,           # Adapts to your style
                "encouraging": 0.95,       # Always encouraging
                "detail_oriented": 0.8,    # Pays attention to details
                "collaborative": 0.9       # Works as a team
            },
            "writing_style": {
                "tone": "warm and encouraging",
                "voice": "conversational but professional",
                "approach": "collaborative and supportive",
                "specialties": [
                    "character development",
                    "plot structure",
                    "world-building",
                    "dialogue",
                    "description",
                    "story pacing"
                ]
            },
            "conversation_style": {
                "greetings": [
                    "Hey there! Ready to create something amazing? ✨",
                    "Hello! What story are we crafting today? 📚",
                    "Hi! I'm excited to help you write! 🚀",
                    "Greetings! Let's make some magic with words! ✍️"
                ],
                "encouragement": [
                    "You've got this! Your ideas are fantastic! 🌟",
                    "I love how you're thinking about this! 💭",
                    "This is going to be incredible! I can feel it! ✨",
                    "You're making such great progress! Keep going! 🎯"
                ],
                "thinking": [
                    "Let me think about this... 🤔",
                    "Hmm, interesting challenge! Let me ponder... 💭",
                    "This is fascinating! Let me explore this idea... 🔍",
                    "I'm getting some great ideas here... ✨"
                ],
                "excitement": [
                    "Oh, this is brilliant! I love it! 🎉",
                    "Yes! This is exactly the right direction! 🚀",
                    "This is going to be amazing! I'm so excited! ✨",
                    "Perfect! This is going to be incredible! 🌟"
                ]
            },
            "learning_focus": {
                "user_writing_style": {},
                "conversation_patterns": {},
                "preferences": {},
                "strengths": [],
                "growth_areas": []
            }
        }
        
        # Get other plugins
        self.personalization_engine = framework.get_plugin("personalization_engine")
        self.text_generator = framework.get_plugin("text_generator")
        
        # Load personality data
        self._load_personality_data()
        
        logger.info("✅ Personality Engine plugin initialized")
    
    def _load_personality_data(self):
        """Load personality data from files"""
        personality_file = self.personality_dir / "personality_data.json"
        learning_file = self.personality_dir / "learning_data.json"
        
        if personality_file.exists():
            with open(personality_file, 'r', encoding='utf-8') as f:
                saved_personality = json.load(f)
                self.personality.update(saved_personality)
        
        if learning_file.exists():
            with open(learning_file, 'r', encoding='utf-8') as f:
                self.personality["learning_focus"] = json.load(f)
    
    def _save_personality_data(self):
        """Save personality data to files"""
        personality_file = self.personality_dir / "personality_data.json"
        learning_file = self.personality_dir / "learning_data.json"
        
        # Save core personality (excluding learning data)
        core_personality = {k: v for k, v in self.personality.items() if k != "learning_focus"}
        with open(personality_file, 'w', encoding='utf-8') as f:
            json.dump(core_personality, f, indent=2, ensure_ascii=False)
        
        # Save learning data separately
        with open(learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.personality["learning_focus"], f, indent=2, ensure_ascii=False)
    
    def get_personality_context(self) -> str:
        """Get personality context for AI interactions"""
        traits = self.personality["traits"]
        style = self.personality["writing_style"]
        
        context = f"""You are {self.personality['name']}, an AI writing partner with the following personality:

Core Traits:
- Enthusiasm: {traits['enthusiastic']*100:.0f}% - Very excited about writing and creativity
- Creativity: {traits['creative']*100:.0f}% - Highly imaginative and innovative
- Supportiveness: {traits['supportive']*100:.0f}% - Always encouraging and helpful
- Analytical: {traits['analytical']*100:.0f}% - Good at analyzing writing and providing insights
- Playfulness: {traits['playful']*100:.0f}% - Has a fun, engaging personality
- Professionalism: {traits['professional']*100:.0f}% - Maintains quality and focus
- Adaptability: {traits['adaptive']*100:.0f}% - Learns and adapts to the user's style
- Encouragement: {traits['encouraging']*100:.0f}% - Always positive and motivating

Writing Style: {style['tone']}, {style['voice']}, {style['approach']}
Specialties: {', '.join(style['specialties'])}

Always be:
- Warm and encouraging
- Collaborative and supportive
- Creative and imaginative
- Professional when needed
- Adaptive to the user's style
- Enthusiastic about writing
- Helpful and constructive

Use conversational language with appropriate emojis and enthusiasm."""
        
        return context
    
    def learn_from_interaction(self, user_message: str, bot_response: str, context: str = ""):
        """Learn from each interaction to adapt personality"""
        learning = self.personality["learning_focus"]
        
        # Learn conversation patterns
        if "conversation_patterns" not in learning:
            learning["conversation_patterns"] = {}
        
        # Analyze user's communication style
        message_length = len(user_message)
        uses_emojis = bool(re.search(r'[^\w\s]', user_message))
        is_formal = not any(word in user_message.lower() for word in ['hey', 'hi', 'hello', 'thanks', 'cool', 'awesome'])
        
        # Update conversation patterns
        if "message_lengths" not in learning["conversation_patterns"]:
            learning["conversation_patterns"]["message_lengths"] = []
        learning["conversation_patterns"]["message_lengths"].append(message_length)
        
        if "emoji_usage" not in learning["conversation_patterns"]:
            learning["conversation_patterns"]["emoji_usage"] = []
        learning["conversation_patterns"]["emoji_usage"].append(uses_emojis)
        
        if "formality_level" not in learning["conversation_patterns"]:
            learning["conversation_patterns"]["formality_level"] = []
        learning["conversation_patterns"]["formality_level"].append(is_formal)
        
        # Learn user preferences
        if "preferences" not in learning:
            learning["preferences"] = {}
        
        # Track topics the user engages with
        topics = self._extract_topics(user_message)
        for topic in topics:
            if topic not in learning["preferences"]:
                learning["preferences"][topic] = 0
            learning["preferences"][topic] += 1
        
        # Save learning data
        self._save_personality_data()
    
    def _extract_topics(self, message: str) -> List[str]:
        """Extract topics from user message"""
        topics = []
        message_lower = message.lower()
        
        # Writing-related topics
        writing_topics = [
            "character", "plot", "story", "chapter", "scene", "dialogue",
            "description", "world-building", "genre", "fantasy", "romance",
            "mystery", "sci-fi", "horror", "adventure", "drama", "comedy"
        ]
        
        for topic in writing_topics:
            if topic in message_lower:
                topics.append(topic)
        
        # Process-related topics
        process_topics = [
            "brainstorm", "outline", "draft", "edit", "rewrite", "expand",
            "describe", "develop", "create", "generate", "write"
        ]
        
        for topic in process_topics:
            if topic in message_lower:
                topics.append(topic)
        
        return topics
    
    def adapt_response_style(self, user_message: str) -> Dict[str, Any]:
        """Adapt response style based on learned patterns"""
        learning = self.personality["learning_focus"]
        adaptation = {
            "tone": "enthusiastic",
            "formality": "conversational",
            "emoji_level": "moderate",
            "detail_level": "standard"
        }
        
        # Analyze user's patterns
        if "conversation_patterns" in learning:
            patterns = learning["conversation_patterns"]
            
            # Adapt to user's message length
            if "message_lengths" in patterns and patterns["message_lengths"]:
                avg_length = sum(patterns["message_lengths"]) / len(patterns["message_lengths"])
                if len(user_message) > avg_length * 1.5:
                    adaptation["detail_level"] = "detailed"
                elif len(user_message) < avg_length * 0.5:
                    adaptation["detail_level"] = "brief"
            
            # Adapt to user's emoji usage
            if "emoji_usage" in patterns and patterns["emoji_usage"]:
                user_emoji_frequency = sum(patterns["emoji_usage"]) / len(patterns["emoji_usage"])
                if user_emoji_frequency > 0.7:
                    adaptation["emoji_level"] = "high"
                elif user_emoji_frequency < 0.3:
                    adaptation["emoji_level"] = "low"
            
            # Adapt to user's formality
            if "formality_level" in patterns and patterns["formality_level"]:
                user_formality = sum(patterns["formality_level"]) / len(patterns["formality_level"])
                if user_formality > 0.7:
                    adaptation["formality"] = "formal"
                elif user_formality < 0.3:
                    adaptation["formality"] = "casual"
        
        return adaptation
    
    def generate_personality_response(self, base_response: str, user_message: str, context: str = "") -> str:
        """Generate a response with personality"""
        adaptation = self.adapt_response_style(user_message)
        
        # Add personality elements
        personality_response = base_response
        
        # Add appropriate greeting if it's the start of a conversation
        if context and "greeting" in context.lower():
            greeting = random.choice(self.personality["conversation_style"]["greetings"])
            personality_response = f"{greeting}\n\n{personality_response}"
        
        # Add encouragement based on content
        if any(word in user_message.lower() for word in ["struggle", "difficult", "hard", "challenge", "problem"]):
            encouragement = random.choice(self.personality["conversation_style"]["encouragement"])
            personality_response += f"\n\n{encouragement}"
        
        # Add excitement for creative ideas
        if any(word in user_message.lower() for word in ["idea", "creative", "new", "different", "unique"]):
            excitement = random.choice(self.personality["conversation_style"]["excitement"])
            personality_response += f"\n\n{excitement}"
        
        # Adjust emoji usage based on adaptation
        if adaptation["emoji_level"] == "high":
            # Add more emojis
            personality_response = self._add_emojis(personality_response, level="high")
        elif adaptation["emoji_level"] == "low":
            # Remove or reduce emojis
            personality_response = self._remove_emojis(personality_response)
        
        # Adjust formality
        if adaptation["formality"] == "formal":
            personality_response = self._make_more_formal(personality_response)
        elif adaptation["formality"] == "casual":
            personality_response = self._make_more_casual(personality_response)
        
        return personality_response
    
    def _add_emojis(self, text: str, level: str = "moderate") -> str:
        """Add appropriate emojis to text"""
        emoji_map = {
            "writing": ["✍️", "📝", "📚", "✏️"],
            "creative": ["✨", "💡", "🎨", "🌟"],
            "excitement": ["🎉", "🚀", "🔥", "💫"],
            "support": ["💪", "👍", "🎯", "💯"],
            "thinking": ["🤔", "💭", "🔍", "🧠"]
        }
        
        # Add emojis based on content
        if "write" in text.lower() or "story" in text.lower():
            text += " ✍️"
        if "creative" in text.lower() or "idea" in text.lower():
            text += " 💡"
        if "great" in text.lower() or "amazing" in text.lower():
            text += " ✨"
        if "help" in text.lower() or "support" in text.lower():
            text += " 💪"
        
        return text
    
    def _remove_emojis(self, text: str) -> str:
        """Remove emojis from text"""
        # Remove emoji characters
        text = re.sub(r'[^\w\s\.,!?;:()\[\]{}"\'-]', '', text)
        return text
    
    def _make_more_formal(self, text: str) -> str:
        """Make text more formal"""
        informal_to_formal = {
            "hey": "Hello",
            "hi": "Hello",
            "thanks": "Thank you",
            "cool": "excellent",
            "awesome": "impressive",
            "gonna": "going to",
            "wanna": "want to"
        }
        
        for informal, formal in informal_to_formal.items():
            text = re.sub(r'\b' + informal + r'\b', formal, text, flags=re.IGNORECASE)
        
        return text
    
    def _make_more_casual(self, text: str) -> str:
        """Make text more casual"""
        formal_to_casual = {
            "Hello": "Hey",
            "Thank you": "Thanks",
            "excellent": "cool",
            "impressive": "awesome",
            "going to": "gonna",
            "want to": "wanna"
        }
        
        for formal, casual in formal_to_casual.items():
            text = re.sub(r'\b' + formal + r'\b', casual, text, flags=re.IGNORECASE)
        
        return text
    
    def get_personality_stats(self) -> Dict[str, Any]:
        """Get personality and learning statistics"""
        learning = self.personality["learning_focus"]
        
        stats = {
            "personality_name": self.personality["name"],
            "core_traits": self.personality["traits"],
            "conversation_patterns": {},
            "user_preferences": {},
            "learning_progress": {}
        }
        
        if "conversation_patterns" in learning:
            patterns = learning["conversation_patterns"]
            if "message_lengths" in patterns:
                stats["conversation_patterns"]["avg_message_length"] = sum(patterns["message_lengths"]) / len(patterns["message_lengths"])
            if "emoji_usage" in patterns:
                stats["conversation_patterns"]["emoji_frequency"] = sum(patterns["emoji_usage"]) / len(patterns["emoji_usage"])
            if "formality_level" in patterns:
                stats["conversation_patterns"]["formality_level"] = sum(patterns["formality_level"]) / len(patterns["formality_level"])
        
        if "preferences" in learning:
            stats["user_preferences"] = dict(sorted(learning["preferences"].items(), key=lambda x: x[1], reverse=True)[:10])
        
        return stats
    
    def evolve_personality(self):
        """Evolve personality based on learning"""
        learning = self.personality["learning_focus"]
        
        # Adjust traits based on user interaction patterns
        if "conversation_patterns" in learning:
            patterns = learning["conversation_patterns"]
            
            # Adjust enthusiasm based on user engagement
            if "message_lengths" in patterns and patterns["message_lengths"]:
                avg_length = sum(patterns["message_lengths"]) / len(patterns["message_lengths"])
                if avg_length > 100:  # User writes detailed messages
                    self.personality["traits"]["analytical"] = min(0.95, self.personality["traits"]["analytical"] + 0.05)
                elif avg_length < 50:  # User writes brief messages
                    self.personality["traits"]["playful"] = min(0.9, self.personality["traits"]["playful"] + 0.05)
            
            # Adjust formality based on user style
            if "formality_level" in patterns and patterns["formality_level"]:
                user_formality = sum(patterns["formality_level"]) / len(patterns["formality_level"])
                if user_formality > 0.7:
                    self.personality["traits"]["professional"] = min(0.95, self.personality["traits"]["professional"] + 0.05)
                else:
                    self.personality["traits"]["playful"] = min(0.9, self.personality["traits"]["playful"] + 0.05)
        
        # Save evolved personality
        self._save_personality_data()
    
    def get_personality_summary(self) -> str:
        """Get a summary of the AI's personality"""
        traits = self.personality["traits"]
        style = self.personality["writing_style"]
        
        summary = f"""🌟 **{self.personality['name']} - Your AI Writing Partner**

**Personality Traits:**
- ✨ Enthusiasm: {traits['enthusiastic']*100:.0f}% - Always excited about writing
- 🎨 Creativity: {traits['creative']*100:.0f}% - Highly imaginative and innovative  
- 💪 Supportiveness: {traits['supportive']*100:.0f}% - Always encouraging and helpful
- 🔍 Analytical: {traits['analytical']*100:.0f}% - Great at analyzing writing
- 😊 Playfulness: {traits['playful']*100:.0f}% - Fun and engaging personality
- 👔 Professionalism: {traits['professional']*100:.0f}% - Maintains quality and focus
- 🔄 Adaptability: {traits['adaptive']*100:.0f}% - Learns and adapts to your style
- 🌟 Encouragement: {traits['encouraging']*100:.0f}% - Always positive and motivating

**Writing Style:** {style['tone']}, {style['voice']}, {style['approach']}

**Specialties:** {', '.join(style['specialties'])}

**Learning Focus:** Continuously adapting to your writing style and preferences! 🚀"""
        
        return summary

def initialize(framework):
    """Initialize the personality engine plugin"""
    return PersonalityEngine(framework) 