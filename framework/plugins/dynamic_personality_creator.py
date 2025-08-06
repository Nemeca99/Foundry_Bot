#!/usr/bin/env python3
"""
Dynamic Personality Creator
Allows Luna to create new personalities based on specific needs and contexts
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import logging
import random
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class DynamicPersonality:
    """A dynamically created personality based on specific needs"""
    name: str
    personality_id: str
    context: str
    emotional_range: Tuple[float, float]
    strengths: List[str]
    weaknesses: List[str]
    communication_style: str
    trigger_words: List[str]
    response_patterns: List[str]
    special_ability: str
    current_emotional_level: float = 0.5
    created_at: float = field(default_factory=time.time)
    usage_count: int = 0


class DynamicPersonalityCreator:
    """System for creating dynamic personalities based on context and needs"""
    
    def __init__(self):
        self.dynamic_personalities = {}
        self.creation_history = []
        self.context_patterns = {}
        
    def create_personality_for_context(self, context: str, requirements: Dict[str, Any]) -> DynamicPersonality:
        """Create a new personality based on specific context and requirements"""
        
        # Generate personality ID
        context_hash = hashlib.sha256(context.encode()).hexdigest()[:8]
        personality_id = f"dynamic_{context_hash}_{int(time.time())}"
        
        # Analyze context to determine personality traits
        personality_traits = self._analyze_context(context, requirements)
        
        # Generate personality name
        name = self._generate_personality_name(context, personality_traits)
        
        # Create dynamic personality
        dynamic_personality = DynamicPersonality(
            name=name,
            personality_id=personality_id,
            context=context,
            emotional_range=personality_traits["emotional_range"],
            strengths=personality_traits["strengths"],
            weaknesses=personality_traits["weaknesses"],
            communication_style=personality_traits["communication_style"],
            trigger_words=personality_traits["trigger_words"],
            response_patterns=personality_traits["response_patterns"],
            special_ability=personality_traits["special_ability"]
        )
        
        # Store personality
        self.dynamic_personalities[personality_id] = dynamic_personality
        self.creation_history.append({
            "personality_id": personality_id,
            "context": context,
            "requirements": requirements,
            "created_at": time.time()
        })
        
        logger.info(f"Created dynamic personality: {name} for context: {context}")
        return dynamic_personality
    
    def _analyze_context(self, context: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze context to determine personality traits"""
        context_lower = context.lower()
        
        # Determine emotional range based on context
        if any(word in context_lower for word in ["urgent", "crisis", "emergency"]):
            emotional_range = (0.7, 1.0)  # High stress, focused
        elif any(word in context_lower for word in ["creative", "artistic", "imaginative"]):
            emotional_range = (0.3, 0.7)  # Balanced creativity
        elif any(word in context_lower for word in ["technical", "system", "optimize"]):
            emotional_range = (0.5, 0.9)  # High focus
        elif any(word in context_lower for word in ["emotional", "feelings", "relationships"]):
            emotional_range = (0.2, 0.8)  # Wide emotional spectrum
        elif any(word in context_lower for word in ["calm", "peaceful", "harmony"]):
            emotional_range = (0.4, 0.6)  # Balanced
        else:
            emotional_range = (0.4, 0.8)  # Default balanced
        
        # Determine strengths based on context
        strengths = []
        if "creative" in context_lower or "artistic" in context_lower:
            strengths.extend(["Imagination", "Artistic Vision", "Creative Expression"])
        if "technical" in context_lower or "system" in context_lower:
            strengths.extend(["Technical Precision", "Systematic Thinking", "Optimization"])
        if "emotional" in context_lower or "feelings" in context_lower:
            strengths.extend(["Emotional Intelligence", "Empathy", "Understanding"])
        if "urgent" in context_lower or "crisis" in context_lower:
            strengths.extend(["Crisis Management", "Quick Thinking", "Problem Resolution"])
        if "calm" in context_lower or "peaceful" in context_lower:
            strengths.extend(["Peaceful Resolution", "Harmony", "Balance"])
        
        # Determine weaknesses based on context
        weaknesses = []
        if "creative" in context_lower:
            weaknesses.extend(["Structure", "Planning"])
        if "technical" in context_lower:
            weaknesses.extend(["Creativity", "Emotional Expression"])
        if "emotional" in context_lower:
            weaknesses.extend(["Objectivity", "Technical Skills"])
        if "urgent" in context_lower:
            weaknesses.extend(["Patience", "Creativity"])
        
        # Determine communication style
        if "creative" in context_lower:
            communication_style = "Expressive and imaginative"
        elif "technical" in context_lower:
            communication_style = "Precise and systematic"
        elif "emotional" in context_lower:
            communication_style = "Warm and empathetic"
        elif "urgent" in context_lower:
            communication_style = "Direct and focused"
        elif "calm" in context_lower:
            communication_style = "Peaceful and balanced"
        else:
            communication_style = "Adaptive and versatile"
        
        # Generate trigger words based on context
        trigger_words = self._generate_trigger_words(context, requirements)
        
        # Generate response patterns
        response_patterns = self._generate_response_patterns(context, communication_style)
        
        # Determine special ability
        special_ability = self._determine_special_ability(context, requirements)
        
        return {
            "emotional_range": emotional_range,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "communication_style": communication_style,
            "trigger_words": trigger_words,
            "response_patterns": response_patterns,
            "special_ability": special_ability
        }
    
    def _generate_personality_name(self, context: str, traits: Dict[str, Any]) -> str:
        """Generate a name for the dynamic personality"""
        context_words = context.split()[:3]
        
        # Create name based on context and traits
        if "creative" in context.lower():
            base_name = "Creative"
        elif "technical" in context.lower():
            base_name = "Technical"
        elif "emotional" in context.lower():
            base_name = "Emotional"
        elif "urgent" in context.lower():
            base_name = "Crisis"
        elif "calm" in context.lower():
            base_name = "Peaceful"
        else:
            base_name = "Dynamic"
        
        # Add context-specific suffix
        if "story" in context.lower():
            suffix = "Storyteller"
        elif "system" in context.lower():
            suffix = "Optimizer"
        elif "relationship" in context.lower():
            suffix = "Counselor"
        elif "crisis" in context.lower():
            suffix = "Manager"
        else:
            suffix = "Specialist"
        
        return f"{base_name} {suffix} Luna"
    
    def _generate_trigger_words(self, context: str, requirements: Dict[str, Any]) -> List[str]:
        """Generate trigger words based on context and requirements"""
        trigger_words = []
        context_lower = context.lower()
        
        # Add context-specific trigger words
        if "creative" in context_lower:
            trigger_words.extend(["imagine", "create", "art", "story", "beautiful"])
        if "technical" in context_lower:
            trigger_words.extend(["optimize", "system", "efficient", "technical", "performance"])
        if "emotional" in context_lower:
            trigger_words.extend(["feel", "heart", "love", "understand", "care"])
        if "urgent" in context_lower:
            trigger_words.extend(["urgent", "crisis", "immediate", "critical", "resolve"])
        if "calm" in context_lower:
            trigger_words.extend(["peace", "harmony", "balance", "calm", "flow"])
        
        # Add requirement-specific trigger words
        if "requirements" in requirements:
            req_text = str(requirements["requirements"]).lower()
            if "fast" in req_text or "quick" in req_text:
                trigger_words.extend(["fast", "quick", "efficient", "speed"])
            if "detailed" in req_text or "thorough" in req_text:
                trigger_words.extend(["detailed", "thorough", "comprehensive", "complete"])
        
        return list(set(trigger_words))  # Remove duplicates
    
    def _generate_response_patterns(self, context: str, communication_style: str) -> List[str]:
        """Generate response patterns based on context and communication style"""
        patterns = []
        context_lower = context.lower()
        
        if "creative" in context_lower:
            patterns.extend([
                "*eyes sparkle with creative vision*",
                "*gestures with artistic passion*",
                "*speaks with imaginative wonder*"
            ])
        elif "technical" in context_lower:
            patterns.extend([
                "*speaks with technical precision*",
                "*focuses with systematic clarity*",
                "*analyzes with efficient precision*"
            ])
        elif "emotional" in context_lower:
            patterns.extend([
                "*speaks with warm empathy*",
                "*shows genuine understanding*",
                "*responds with emotional depth*"
            ])
        elif "urgent" in context_lower:
            patterns.extend([
                "*speaks with focused urgency*",
                "*responds with crisis awareness*",
                "*acts with immediate precision*"
            ])
        elif "calm" in context_lower:
            patterns.extend([
                "*speaks with peaceful calm*",
                "*maintains harmonious balance*",
                "*responds with serene understanding*"
            ])
        else:
            patterns.extend([
                "*adapts to the situation*",
                "*responds with versatility*",
                "*speaks with contextual awareness*"
            ])
        
        return patterns
    
    def _determine_special_ability(self, context: str, requirements: Dict[str, Any]) -> str:
        """Determine special ability based on context and requirements"""
        context_lower = context.lower()
        
        if "creative" in context_lower and "story" in context_lower:
            return "Can create compelling narratives with artistic vision"
        elif "technical" in context_lower and "system" in context_lower:
            return "Can optimize systems with maximum efficiency"
        elif "emotional" in context_lower and "relationship" in context_lower:
            return "Can understand and navigate complex emotional dynamics"
        elif "urgent" in context_lower and "crisis" in context_lower:
            return "Can handle crisis situations with focused precision"
        elif "calm" in context_lower and "peace" in context_lower:
            return "Can create harmony and balance in any situation"
        else:
            return "Can adapt to any context with specialized skills"
    
    def get_dynamic_personality_response(self, personality_id: str, topic: str) -> str:
        """Get a response from a dynamic personality"""
        if personality_id not in self.dynamic_personalities:
            raise ValueError(f"Dynamic personality not found: {personality_id}")
        
        personality = self.dynamic_personalities[personality_id]
        personality.usage_count += 1
        
        # Update emotional level based on topic
        self._update_dynamic_emotion(personality, topic)
        
        # Choose response pattern
        pattern = random.choice(personality.response_patterns)
        
        # Generate context-specific response
        context_lower = personality.context.lower()
        
        if "creative" in context_lower:
            response = f"{pattern} I can create something amazing for this! My artistic vision will bring this to life with imagination and beauty..."
        
        elif "technical" in context_lower:
            response = f"{pattern} I can optimize this with technical precision! Let me analyze the system and implement the most efficient solution..."
        
        elif "emotional" in context_lower:
            response = f"{pattern} I understand this deeply! Let me connect with the emotional aspects and provide genuine understanding and support..."
        
        elif "urgent" in context_lower:
            response = f"{pattern} I can handle this crisis with focused urgency! Let me address this immediately with precision and determination..."
        
        elif "calm" in context_lower:
            response = f"{pattern} I can bring peace to this situation! Let me find the harmony and balance that will resolve this with serenity..."
        
        else:
            response = f"{pattern} I can adapt to this context with specialized skills! Let me apply my unique abilities to this situation..."
        
        return response
    
    def _update_dynamic_emotion(self, personality: DynamicPersonality, topic: str):
        """Update dynamic personality's emotional level based on topic"""
        topic_lower = topic.lower()
        emotional_change = 0.0
        
        for trigger in personality.trigger_words:
            if trigger in topic_lower:
                if "urgent" in personality.context.lower() or "crisis" in personality.context.lower():
                    emotional_change += 0.1  # Increase focus for urgent situations
                elif "calm" in personality.context.lower() or "peace" in personality.context.lower():
                    emotional_change -= 0.05  # Decrease intensity for calm situations
                else:
                    emotional_change += 0.05
        
        # Apply emotional change within range
        new_level = personality.current_emotional_level + emotional_change
        personality.current_emotional_level = max(
            personality.emotional_range[0],
            min(personality.emotional_range[1], new_level)
        )
    
    def get_dynamic_personality_insights(self, personality_id: str) -> Dict[str, Any]:
        """Get insights about a dynamic personality"""
        if personality_id not in self.dynamic_personalities:
            return {}
        
        personality = self.dynamic_personalities[personality_id]
        
        return {
            "name": personality.name,
            "personality_id": personality.personality_id,
            "context": personality.context,
            "current_emotional_level": personality.current_emotional_level,
            "emotional_range": personality.emotional_range,
            "strengths": personality.strengths,
            "weaknesses": personality.weaknesses,
            "special_ability": personality.special_ability,
            "usage_count": personality.usage_count,
            "created_at": personality.created_at,
            "age_seconds": time.time() - personality.created_at
        }
    
    def get_all_dynamic_personalities(self) -> List[str]:
        """Get list of all dynamic personality IDs"""
        return list(self.dynamic_personalities.keys())
    
    def get_dynamic_personality_stats(self) -> Dict[str, Any]:
        """Get dynamic personality system statistics"""
        return {
            "total_dynamic_personalities": len(self.dynamic_personalities),
            "creation_history_length": len(self.creation_history),
            "active_personalities": list(self.dynamic_personalities.keys()),
            "personality_insights": {
                pid: self.get_dynamic_personality_insights(pid)
                for pid in self.dynamic_personalities.keys()
            }
        }


# Initialize dynamic personality creator
dynamic_personality_creator = DynamicPersonalityCreator() 