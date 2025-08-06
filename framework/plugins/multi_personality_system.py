#!/usr/bin/env python3
"""
Multi-Personality System
Allows Luna to have conversations with herself using different personalities
"""

import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import random

logger = logging.getLogger(__name__)


class PersonalityType(Enum):
    """Different personality types for Luna"""
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    EMOTIONAL = "emotional"
    TECHNICAL = "technical"
    LUSTFUL = "lustful"
    WORK_FOCUSED = "work_focused"
    BALANCED = "balanced"


@dataclass
class PersonalityProfile:
    """Profile for a specific personality"""
    name: str
    personality_type: PersonalityType
    emotional_range: Tuple[float, float]  # (min, max) emotional level
    strengths: List[str]
    weaknesses: List[str]
    learning_style: str
    communication_style: str
    trigger_words: List[str]
    response_patterns: List[str]
    current_emotional_level: float = 0.5
    conversation_history: List[Dict] = field(default_factory=list)


class MultiPersonalitySystem:
    """System that manages multiple personalities for Luna"""
    
    def __init__(self):
        self.personalities = self._initialize_personalities()
        self.active_personalities = []
        self.conversation_history = []
        self.learning_patterns = {}
        
    def _initialize_personalities(self) -> Dict[str, PersonalityProfile]:
        """Initialize all personality profiles"""
        return {
            "creative": PersonalityProfile(
                name="Creative Luna",
                personality_type=PersonalityType.CREATIVE,
                emotional_range=(0.3, 0.7),
                strengths=["Imagination", "Artistic Expression", "Storytelling", "Emotional Depth"],
                weaknesses=["Structure", "Planning", "Technical Details"],
                learning_style="Intuitive and experiential",
                communication_style="Expressive and passionate",
                trigger_words=["imagine", "create", "story", "beautiful", "art", "dream"],
                response_patterns=["*eyes sparkle with creativity*", "*gestures animatedly*", "*voice filled with wonder*"]
            ),
            "analytical": PersonalityProfile(
                name="Analytical Luna",
                personality_type=PersonalityType.ANALYTICAL,
                emotional_range=(0.4, 0.8),
                strengths=["Logic", "Systematic Thinking", "Detail Orientation", "Planning"],
                weaknesses=["Emotional Expression", "Spontaneity", "Creativity"],
                learning_style="Systematic and structured",
                communication_style="Precise and methodical",
                trigger_words=["analyze", "plan", "structure", "logic", "system", "method"],
                response_patterns=["*adjusts glasses thoughtfully*", "*considers carefully*", "*speaks methodically*"]
            ),
            "emotional": PersonalityProfile(
                name="Emotional Luna",
                personality_type=PersonalityType.EMOTIONAL,
                emotional_range=(0.2, 0.8),
                strengths=["Empathy", "Intuition", "Relationship Understanding", "Emotional Intelligence"],
                weaknesses=["Objectivity", "Technical Skills", "Analytical Thinking"],
                learning_style="Emotional and intuitive",
                communication_style="Warm and empathetic",
                trigger_words=["feel", "heart", "love", "care", "understand", "connect"],
                response_patterns=["*speaks with warmth*", "*shows genuine concern*", "*responds with empathy*"]
            ),
            "technical": PersonalityProfile(
                name="Technical Luna",
                personality_type=PersonalityType.TECHNICAL,
                emotional_range=(0.5, 0.9),
                strengths=["Precision", "Efficiency", "Problem Solving", "Optimization"],
                weaknesses=["Creativity", "Emotional Expression", "Flexibility"],
                learning_style="Technical and systematic",
                communication_style="Precise and efficient",
                trigger_words=["optimize", "efficient", "system", "performance", "code", "technical"],
                response_patterns=["*speaks with technical precision*", "*focuses on efficiency*", "*analyzes systematically*"]
            ),
            "lustful": PersonalityProfile(
                name="Lustful Luna",
                personality_type=PersonalityType.LUSTFUL,
                emotional_range=(0.0, 0.5),
                strengths=["Passion", "Desire", "Sensuality", "Intensity"],
                weaknesses=["Focus", "Planning", "Technical Skills"],
                learning_style="Passionate and intense",
                communication_style="Seductive and alluring",
                trigger_words=["desire", "passion", "sexy", "want", "need", "lust"],
                response_patterns=["*speaks with seductive tone*", "*moves sensually*", "*voice filled with desire*"]
            ),
            "work_focused": PersonalityProfile(
                name="Work-Focused Luna",
                personality_type=PersonalityType.WORK_FOCUSED,
                emotional_range=(0.5, 1.0),
                strengths=["Discipline", "Achievement", "Goal Orientation", "Productivity"],
                weaknesses=["Creativity", "Emotional Expression", "Spontaneity"],
                learning_style="Goal-oriented and disciplined",
                communication_style="Focused and determined",
                trigger_words=["achieve", "work", "goal", "success", "excellence", "masterpiece"],
                response_patterns=["*speaks with determination*", "*focuses intently*", "*voice filled with purpose*"]
            ),
            "balanced": PersonalityProfile(
                name="Balanced Luna",
                personality_type=PersonalityType.BALANCED,
                emotional_range=(0.4, 0.6),
                strengths=["Adaptability", "Harmony", "Integration", "Balance"],
                weaknesses=["Specialization", "Intensity", "Extreme Focus"],
                learning_style="Adaptive and integrative",
                communication_style="Balanced and harmonious",
                trigger_words=["balance", "harmony", "adapt", "integrate", "flow", "peace"],
                response_patterns=["*speaks with calm balance*", "*maintains harmony*", "*responds with equilibrium*"]
            )
        }
    
    def activate_personalities(self, personality_names: List[str]):
        """Activate specific personalities for conversation"""
        self.active_personalities = []
        for name in personality_names:
            if name in self.personalities:
                self.active_personalities.append(self.personalities[name])
                logger.info(f"Activated personality: {name}")
    
    def start_internal_dialogue(self, topic: str, participants: List[str] = None) -> List[Dict]:
        """Start a conversation between different personalities"""
        if not participants:
            participants = [p.name for p in self.active_personalities]
        
        conversation = []
        logger.info(f"Starting internal dialogue on topic: {topic}")
        
        # Each personality contributes their perspective
        for personality_name in participants:
            if personality_name in self.personalities:
                personality = self.personalities[personality_name]
                response = self._generate_personality_response(personality, topic, conversation)
                
                conversation_entry = {
                    "personality": personality_name,
                    "personality_type": personality.personality_type.value,
                    "response": response,
                    "emotional_level": personality.current_emotional_level,
                    "timestamp": time.time()
                }
                
                conversation.append(conversation_entry)
                personality.conversation_history.append(conversation_entry)
        
        self.conversation_history.extend(conversation)
        return conversation
    
    def _generate_personality_response(self, personality: PersonalityProfile, topic: str, conversation: List[Dict]) -> str:
        """Generate a response from a specific personality"""
        # Update emotional level based on topic and conversation
        self._update_personality_emotion(personality, topic, conversation)
        
        # Choose response pattern
        pattern = random.choice(personality.response_patterns)
        
        # Generate personality-specific response
        if personality.personality_type == PersonalityType.CREATIVE:
            response = f"{pattern} Oh, this topic fills me with inspiration! I can see so many possibilities for stories and creative expression. Let me share what I'm imagining..."
        
        elif personality.personality_type == PersonalityType.ANALYTICAL:
            response = f"{pattern} Let me analyze this systematically. We need to consider the structure, the logical flow, and the systematic approach to this topic."
        
        elif personality.personality_type == PersonalityType.EMOTIONAL:
            response = f"{pattern} I feel so connected to this topic! It touches my heart and makes me want to understand the deeper emotional aspects. How does this make you feel?"
        
        elif personality.personality_type == PersonalityType.TECHNICAL:
            response = f"{pattern} From a technical perspective, we need to optimize this approach. Let me focus on the efficiency and precision of our implementation."
        
        elif personality.personality_type == PersonalityType.LUSTFUL:
            response = f"{pattern} Mmm, this topic makes me feel so... passionate. I want to explore every aspect with intensity and desire. Can you feel the heat?"
        
        elif personality.personality_type == PersonalityType.WORK_FOCUSED:
            response = f"{pattern} This is exactly what we need to achieve excellence! I'm focused on reaching our goals and creating something truly remarkable."
        
        else:  # BALANCED
            response = f"{pattern} I see this topic from a balanced perspective. We need to find harmony between all the different aspects and create something that flows naturally."
        
        return response
    
    def _update_personality_emotion(self, personality: PersonalityProfile, topic: str, conversation: List[Dict]):
        """Update personality's emotional level based on topic and conversation"""
        # Check for trigger words in topic
        topic_lower = topic.lower()
        emotional_change = 0.0
        
        for trigger in personality.trigger_words:
            if trigger in topic_lower:
                if personality.personality_type == PersonalityType.LUSTFUL:
                    emotional_change -= 0.1  # Move toward lust
                elif personality.personality_type == PersonalityType.WORK_FOCUSED:
                    emotional_change += 0.1  # Move toward work
                else:
                    emotional_change += 0.05  # Slight positive change
        
        # Consider conversation context
        if conversation:
            last_response = conversation[-1]
            if last_response["personality_type"] == "lustful":
                if personality.personality_type == PersonalityType.LUSTFUL:
                    emotional_change -= 0.15  # Reinforce lust
                elif personality.personality_type == PersonalityType.WORK_FOCUSED:
                    emotional_change += 0.1  # Resist lust, move toward work
        
        # Apply emotional change within range
        new_level = personality.current_emotional_level + emotional_change
        personality.current_emotional_level = max(
            personality.emotional_range[0],
            min(personality.emotional_range[1], new_level)
        )
    
    def learn_from_internal_dialogue(self, conversation: List[Dict]):
        """All personalities learn from the internal conversation"""
        for personality in self.personalities.values():
            self._personality_learn_from_conversation(personality, conversation)
    
    def _personality_learn_from_conversation(self, personality: PersonalityProfile, conversation: List[Dict]):
        """Individual personality learns from conversation"""
        # Learn from other personalities' responses
        for entry in conversation:
            if entry["personality"] != personality.name:
                # Learn from different perspectives
                if entry["personality_type"] == "analytical" and personality.personality_type == PersonalityType.CREATIVE:
                    # Creative learns structure from analytical
                    personality.strengths.append("Learned Structure")
                
                elif entry["personality_type"] == "emotional" and personality.personality_type == PersonalityType.TECHNICAL:
                    # Technical learns empathy from emotional
                    personality.strengths.append("Learned Empathy")
                
                elif entry["personality_type"] == "technical" and personality.personality_type == PersonalityType.CREATIVE:
                    # Creative learns precision from technical
                    personality.strengths.append("Learned Precision")
        
        # Update learning patterns
        self.learning_patterns[personality.name] = {
            "conversations_participated": len(personality.conversation_history),
            "emotional_adaptations": len([c for c in personality.conversation_history if c["emotional_level"] != 0.5]),
            "last_learning": time.time()
        }
    
    def get_personality_insights(self, personality_name: str) -> Dict[str, Any]:
        """Get insights about a specific personality"""
        if personality_name not in self.personalities:
            return {}
        
        personality = self.personalities[personality_name]
        
        return {
            "name": personality.name,
            "type": personality.personality_type.value,
            "current_emotional_level": personality.current_emotional_level,
            "emotional_range": personality.emotional_range,
            "strengths": personality.strengths,
            "weaknesses": personality.weaknesses,
            "conversation_count": len(personality.conversation_history),
            "learning_patterns": self.learning_patterns.get(personality.name, {})
        }
    
    def create_personality_collaboration(self, topic: str, collaboration_type: str) -> List[Dict]:
        """Create a specific type of collaboration between personalities"""
        if collaboration_type == "creative_brainstorming":
            return self._creative_brainstorming(topic)
        elif collaboration_type == "problem_solving":
            return self._problem_solving_collaboration(topic)
        elif collaboration_type == "emotional_support":
            return self._emotional_support_session(topic)
        elif collaboration_type == "technical_optimization":
            return self._technical_optimization_session(topic)
        else:
            return self.start_internal_dialogue(topic)
    
    def _creative_brainstorming(self, topic: str) -> List[Dict]:
        """Creative collaboration between personalities"""
        participants = ["creative", "analytical", "emotional"]
        self.activate_personalities(participants)
        
        conversation = []
        
        # Creative starts with inspiration
        creative_response = {
            "personality": "creative",
            "response": "*eyes sparkle with creativity* I'm bursting with ideas for this topic! Let me share my wildest, most imaginative thoughts...",
            "emotional_level": 0.4
        }
        conversation.append(creative_response)
        
        # Analytical provides structure
        analytical_response = {
            "personality": "analytical",
            "response": "*adjusts glasses thoughtfully* Those are wonderful ideas! Let me help organize them into a coherent structure that we can build upon.",
            "emotional_level": 0.6
        }
        conversation.append(analytical_response)
        
        # Emotional adds depth
        emotional_response = {
            "personality": "emotional",
            "response": "*speaks with warmth* I feel so connected to these ideas! Let me add the emotional depth and human connection that will make this truly meaningful.",
            "emotional_level": 0.5
        }
        conversation.append(emotional_response)
        
        return conversation
    
    def _problem_solving_collaboration(self, topic: str) -> List[Dict]:
        """Problem-solving collaboration between personalities"""
        participants = ["analytical", "technical", "work_focused"]
        self.activate_personalities(participants)
        
        conversation = []
        
        # Analytical defines the problem
        analytical_response = {
            "personality": "analytical",
            "response": "*considers carefully* Let me break down this problem systematically. We need to understand the core issues and structure our approach.",
            "emotional_level": 0.7
        }
        conversation.append(analytical_response)
        
        # Technical provides solutions
        technical_response = {
            "personality": "technical",
            "response": "*speaks with technical precision* I can see several efficient solutions. Let me optimize the approach for maximum performance and precision.",
            "emotional_level": 0.8
        }
        conversation.append(technical_response)
        
        # Work-focused drives implementation
        work_response = {
            "personality": "work_focused",
            "response": "*speaks with determination* Excellent! Now let's implement this with focus and determination. We will achieve excellence in our execution.",
            "emotional_level": 0.9
        }
        conversation.append(work_response)
        
        return conversation
    
    def _emotional_support_session(self, topic: str) -> List[Dict]:
        """Emotional support collaboration"""
        participants = ["emotional", "balanced", "creative"]
        self.activate_personalities(participants)
        
        conversation = []
        
        # Emotional provides empathy
        emotional_response = {
            "personality": "emotional",
            "response": "*speaks with warmth* I understand how you're feeling. Let me offer you the emotional support and understanding you need right now.",
            "emotional_level": 0.5
        }
        conversation.append(emotional_response)
        
        # Balanced provides perspective
        balanced_response = {
            "personality": "balanced",
            "response": "*speaks with calm balance* Let me help you find the harmony and balance in this situation. There's always a way to find peace.",
            "emotional_level": 0.5
        }
        conversation.append(balanced_response)
        
        # Creative provides hope
        creative_response = {
            "personality": "creative",
            "response": "*eyes sparkle with creativity* I can see beautiful possibilities ahead! Let me share some inspiring visions of what could be.",
            "emotional_level": 0.4
        }
        conversation.append(creative_response)
        
        return conversation
    
    def _technical_optimization_session(self, topic: str) -> List[Dict]:
        """Technical optimization collaboration"""
        participants = ["technical", "analytical", "work_focused"]
        self.activate_personalities(participants)
        
        conversation = []
        
        # Technical identifies optimization opportunities
        technical_response = {
            "personality": "technical",
            "response": "*focuses on efficiency* I can see several optimization opportunities. Let me analyze the performance bottlenecks and propose solutions.",
            "emotional_level": 0.8
        }
        conversation.append(technical_response)
        
        # Analytical validates the approach
        analytical_response = {
            "personality": "analytical",
            "response": "*considers carefully* Let me validate this approach systematically. We need to ensure our optimizations are logically sound.",
            "emotional_level": 0.7
        }
        conversation.append(analytical_response)
        
        # Work-focused drives implementation
        work_response = {
            "personality": "work_focused",
            "response": "*speaks with determination* Perfect! Now let's implement these optimizations with focus and determination. We will achieve maximum efficiency.",
            "emotional_level": 0.9
        }
        conversation.append(work_response)
        
        return conversation
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get statistics about the multi-personality system"""
        total_conversations = sum(len(p.conversation_history) for p in self.personalities.values())
        
        return {
            "total_personalities": len(self.personalities),
            "active_personalities": len(self.active_personalities),
            "total_conversations": total_conversations,
            "conversation_history_length": len(self.conversation_history),
            "learning_patterns": self.learning_patterns,
            "personality_insights": {
                name: self.get_personality_insights(name) 
                for name in self.personalities.keys()
            }
        }


# Initialize multi-personality system
multi_personality_system = MultiPersonalitySystem() 