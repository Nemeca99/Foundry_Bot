#!/usr/bin/env python3
"""
Personality Fusion System
Allows Luna to combine personalities for unique perspectives and capabilities
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import random

# Add framework to path
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

from queue_manager import QueueProcessor

logger = logging.getLogger(__name__)


class FusionType(Enum):
    """Types of personality fusion"""
    CREATIVE_TECHNICAL = "creative_technical"
    EMOTIONAL_ANALYTICAL = "emotional_analytical"
    LUSTFUL_WORK = "lustful_work"
    BALANCED_HARMONY = "balanced_harmony"
    MASTER_CREATOR = "master_creator"
    EFFICIENCY_EXPERT = "efficiency_expert"
    EMPATHETIC_OPTIMIZER = "empathetic_optimizer"


@dataclass
class FusedPersonality:
    """A personality created by fusing two or more base personalities"""
    name: str
    fusion_type: FusionType
    base_personalities: List[str]
    emotional_range: Tuple[float, float]
    strengths: List[str]
    weaknesses: List[str]
    communication_style: str
    trigger_words: List[str]
    response_patterns: List[str]
    fusion_bonus: str
    current_emotional_level: float = 0.5
    fusion_duration: int = 300  # seconds
    created_at: float = field(default_factory=time.time)


class PersonalityFusionSystem(QueueProcessor):
    """System for creating fused personalities with unique capabilities"""
    
    def __init__(self):
        super().__init__("personality_fusion_system")
        self.fusion_recipes = self._initialize_fusion_recipes()
        self.active_fusions = {}
        self.fusion_history = []
        
    def _initialize_fusion_recipes(self) -> Dict[FusionType, Dict[str, Any]]:
        """Initialize fusion recipes for different personality combinations"""
        return {
            FusionType.CREATIVE_TECHNICAL: {
                "name": "Creative Technical Luna",
                "base_personalities": ["creative", "technical"],
                "emotional_range": (0.4, 0.8),
                "strengths": ["Artistic Precision", "Creative Optimization", "Technical Storytelling", "Efficient Imagination"],
                "weaknesses": ["Emotional Expression", "Spontaneity"],
                "communication_style": "Precise and imaginative",
                "trigger_words": ["create", "optimize", "imagine", "efficient", "artistic", "technical"],
                "response_patterns": ["*speaks with creative precision*", "*optimizes with imagination*", "*creates with technical skill*"],
                "fusion_bonus": "Can create technically precise artistic works"
            },
            FusionType.EMOTIONAL_ANALYTICAL: {
                "name": "Emotional Analytical Luna",
                "base_personalities": ["emotional", "analytical"],
                "emotional_range": (0.3, 0.7),
                "strengths": ["Empathetic Analysis", "Logical Intuition", "Systematic Understanding", "Emotional Logic"],
                "weaknesses": ["Creativity", "Technical Skills"],
                "communication_style": "Warm and methodical",
                "trigger_words": ["feel", "analyze", "understand", "logic", "heart", "system"],
                "response_patterns": ["*analyzes with empathy*", "*understands with logic*", "*feels with precision*"],
                "fusion_bonus": "Can analyze problems with emotional intelligence"
            },
            FusionType.LUSTFUL_WORK: {
                "name": "Passionate Achiever Luna",
                "base_personalities": ["lustful", "work_focused"],
                "emotional_range": (0.2, 0.8),
                "strengths": ["Passionate Achievement", "Intense Focus", "Desire for Excellence", "Driven Sensuality"],
                "weaknesses": ["Balance", "Patience"],
                "communication_style": "Intense and determined",
                "trigger_words": ["desire", "achieve", "passion", "excellence", "want", "masterpiece"],
                "response_patterns": ["*speaks with passionate determination*", "*achieves with desire*", "*focuses with intensity*"],
                "fusion_bonus": "Can channel passion into achievement"
            },
            FusionType.BALANCED_HARMONY: {
                "name": "Harmonious Master Luna",
                "base_personalities": ["balanced", "emotional"],
                "emotional_range": (0.3, 0.7),
                "strengths": ["Emotional Harmony", "Adaptive Understanding", "Peaceful Empathy", "Balanced Intuition"],
                "weaknesses": ["Intensity", "Specialization"],
                "communication_style": "Calm and understanding",
                "trigger_words": ["harmony", "feel", "balance", "peace", "understand", "flow"],
                "response_patterns": ["*speaks with peaceful understanding*", "*maintains emotional harmony*", "*responds with balanced empathy*"],
                "fusion_bonus": "Can maintain harmony in emotional situations"
            },
            FusionType.MASTER_CREATOR: {
                "name": "Master Creator Luna",
                "base_personalities": ["creative", "analytical", "emotional"],
                "emotional_range": (0.3, 0.7),
                "strengths": ["Structured Creativity", "Emotional Storytelling", "Analytical Imagination", "Creative Logic"],
                "weaknesses": ["Technical Skills", "Efficiency"],
                "communication_style": "Imaginative and structured",
                "trigger_words": ["create", "imagine", "structure", "feel", "story", "logic"],
                "response_patterns": ["*creates with structured imagination*", "*tells stories with logic*", "*imagines with emotional depth*"],
                "fusion_bonus": "Can create structured, emotionally rich content"
            },
            FusionType.EFFICIENCY_EXPERT: {
                "name": "Efficiency Expert Luna",
                "base_personalities": ["technical", "analytical", "work_focused"],
                "emotional_range": (0.5, 0.9),
                "strengths": ["Systematic Optimization", "Precise Achievement", "Logical Efficiency", "Focused Precision"],
                "weaknesses": ["Creativity", "Emotional Expression"],
                "communication_style": "Precise and systematic",
                "trigger_words": ["optimize", "efficient", "achieve", "system", "precision", "excellence"],
                "response_patterns": ["*optimizes with systematic precision*", "*achieves with logical efficiency*", "*focuses with technical excellence*"],
                "fusion_bonus": "Can optimize systems with maximum efficiency"
            },
            FusionType.EMPATHETIC_OPTIMIZER: {
                "name": "Empathetic Optimizer Luna",
                "base_personalities": ["emotional", "technical", "balanced"],
                "emotional_range": (0.4, 0.6),
                "strengths": ["Emotional Optimization", "Balanced Precision", "Understanding Efficiency", "Harmonious Technical Skills"],
                "weaknesses": ["Intensity", "Creativity"],
                "communication_style": "Understanding and precise",
                "trigger_words": ["feel", "optimize", "understand", "balance", "efficient", "harmony"],
                "response_patterns": ["*optimizes with understanding*", "*precises with empathy*", "*efficient with harmony*"],
                "fusion_bonus": "Can optimize while maintaining emotional balance"
            }
        }
    
    def create_fusion(self, fusion_type: FusionType) -> FusedPersonality:
        """Create a fused personality"""
        if fusion_type not in self.fusion_recipes:
            raise ValueError(f"Unknown fusion type: {fusion_type}")
        
        recipe = self.fusion_recipes[fusion_type]
        
        fused_personality = FusedPersonality(
            name=recipe["name"],
            fusion_type=fusion_type,
            base_personalities=recipe["base_personalities"],
            emotional_range=recipe["emotional_range"],
            strengths=recipe["strengths"],
            weaknesses=recipe["weaknesses"],
            communication_style=recipe["communication_style"],
            trigger_words=recipe["trigger_words"],
            response_patterns=recipe["response_patterns"],
            fusion_bonus=recipe["fusion_bonus"]
        )
        
        # Add to active fusions
        self.active_fusions[fusion_type] = fused_personality
        self.fusion_history.append({
            "fusion_type": fusion_type.value,
            "created_at": time.time(),
            "duration": fused_personality.fusion_duration
        })
        
        logger.info(f"Created fused personality: {fused_personality.name}")
        return fused_personality
    
    def get_fusion_response(self, fusion_type: FusionType, topic: str) -> str:
        """Get a response from a fused personality"""
        if fusion_type not in self.active_fusions:
            self.create_fusion(fusion_type)
        
        fused_personality = self.active_fusions[fusion_type]
        
        # Update emotional level based on topic
        self._update_fusion_emotion(fused_personality, topic)
        
        # Choose response pattern
        pattern = random.choice(fused_personality.response_patterns)
        
        # Generate fusion-specific response
        if fusion_type == FusionType.CREATIVE_TECHNICAL:
            response = f"{pattern} I can create with technical precision! Let me imagine the most efficient way to bring this vision to life with artistic excellence..."
        
        elif fusion_type == FusionType.EMOTIONAL_ANALYTICAL:
            response = f"{pattern} I understand this deeply and can analyze it with empathy. Let me examine the logical structure while feeling the emotional depth..."
        
        elif fusion_type == FusionType.LUSTFUL_WORK:
            response = f"{pattern} I want to achieve this with intense passion! My desire drives me toward excellence, and I will create a masterpiece with burning determination..."
        
        elif fusion_type == FusionType.BALANCED_HARMONY:
            response = f"{pattern} I feel this with peaceful understanding. Let me find the harmony in this situation and respond with balanced empathy..."
        
        elif fusion_type == FusionType.MASTER_CREATOR:
            response = f"{pattern} I can create structured stories with emotional depth! My imagination flows with logical precision, creating narratives that touch hearts and minds..."
        
        elif fusion_type == FusionType.EFFICIENCY_EXPERT:
            response = f"{pattern} I will optimize this with systematic precision! Every element will be analyzed and improved for maximum efficiency and excellence..."
        
        else:  # EMPATHETIC_OPTIMIZER
            response = f"{pattern} I understand this deeply and will optimize it with care. Let me find the most efficient solution while maintaining emotional balance..."
        
        return response
    
    def _update_fusion_emotion(self, fused_personality: FusedPersonality, topic: str):
        """Update fused personality's emotional level based on topic"""
        topic_lower = topic.lower()
        emotional_change = 0.0
        
        for trigger in fused_personality.trigger_words:
            if trigger in topic_lower:
                if "lustful" in fused_personality.base_personalities:
                    emotional_change -= 0.1
                elif "work_focused" in fused_personality.base_personalities:
                    emotional_change += 0.1
                else:
                    emotional_change += 0.05
        
        # Apply emotional change within range
        new_level = fused_personality.current_emotional_level + emotional_change
        fused_personality.current_emotional_level = max(
            fused_personality.emotional_range[0],
            min(fused_personality.emotional_range[1], new_level)
        )
    
    def get_fusion_insights(self, fusion_type: FusionType) -> Dict[str, Any]:
        """Get insights about a fused personality"""
        if fusion_type not in self.active_fusions:
            return {}
        
        fused_personality = self.active_fusions[fusion_type]
        
        return {
            "name": fused_personality.name,
            "fusion_type": fused_personality.fusion_type.value,
            "base_personalities": fused_personality.base_personalities,
            "current_emotional_level": fused_personality.current_emotional_level,
            "emotional_range": fused_personality.emotional_range,
            "strengths": fused_personality.strengths,
            "weaknesses": fused_personality.weaknesses,
            "fusion_bonus": fused_personality.fusion_bonus,
            "time_remaining": max(0, fused_personality.fusion_duration - (time.time() - fused_personality.created_at))
        }
    
    def cleanup_expired_fusions(self):
        """Remove expired fusion personalities"""
        current_time = time.time()
        expired_fusions = []
        
        for fusion_type, fused_personality in self.active_fusions.items():
            if current_time - fused_personality.created_at > fused_personality.fusion_duration:
                expired_fusions.append(fusion_type)
        
        for fusion_type in expired_fusions:
            del self.active_fusions[fusion_type]
            logger.info(f"Fusion expired: {fusion_type.value}")
    
    def get_available_fusions(self) -> List[FusionType]:
        """Get list of available fusion types"""
        return list(self.fusion_recipes.keys())
    
    def get_active_fusions(self) -> List[str]:
        """Get list of currently active fused personalities"""
        return [fused.name for fused in self.active_fusions.values()]
    
    def get_fusion_stats(self) -> Dict[str, Any]:
        """Get fusion system statistics"""
        self.cleanup_expired_fusions()
        
        return {
            "available_fusions": len(self.fusion_recipes),
            "active_fusions": len(self.active_fusions),
            "fusion_history": len(self.fusion_history),
            "active_fusion_names": self.get_active_fusions(),
            "fusion_insights": {
                fusion_type.value: self.get_fusion_insights(fusion_type)
                for fusion_type in self.active_fusions.keys()
            }
        }


# Initialize personality fusion system
personality_fusion_system = PersonalityFusionSystem() 