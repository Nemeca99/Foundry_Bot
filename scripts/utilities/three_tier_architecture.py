"""
Three-Tier Architecture - Architect, Builder, Child System

This module implements the three-tier consciousness architecture for Lyra Blackwall Alpha,
providing role-based processing and voice adaptation for different tiers.
"""

import time
import json
import os
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TierRole(Enum):
    """Three-tier architecture roles"""

    ARCHITECT = "architect"  # Strategic planning and oversight
    BUILDER = "builder"  # Implementation and execution
    CHILD = "child"  # Learning and growth


@dataclass
class TierState:
    """State of a specific tier"""

    role: TierRole
    is_active: bool = False
    confidence: float = 0.0
    processing_time: float = 0.0
    voice_characteristics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreeTierResponse:
    """Response from three-tier processing"""

    architect_contribution: Optional[str] = None
    builder_contribution: Optional[str] = None
    child_contribution: Optional[str] = None
    final_response: str = ""
    tier_weights: Dict[str, float] = field(default_factory=dict)
    processing_metadata: Dict[str, Any] = field(default_factory=dict)


class ThreeTierArchitecture:
    """
    Manages the three-tier architecture (Architect, Builder, Child)
    for Lyra Blackwall Alpha consciousness processing.
    """

    def __init__(self, personality_engine=None, memory_system=None):
        """
        Initialize the Three-Tier Architecture.

        Args:
            personality_engine: The personality engine instance
            memory_system: The memory system instance
        """
        self.personality_engine = personality_engine
        self.memory_system = memory_system
        self.logger = logging.getLogger("ThreeTierArchitecture")

        # Tier states
        self.tier_states = {
            TierRole.ARCHITECT: TierState(role=TierRole.ARCHITECT),
            TierRole.BUILDER: TierState(role=TierRole.BUILDER),
            TierRole.CHILD: TierState(role=TierRole.CHILD),
        }

        # Tier voice characteristics
        self._initialize_tier_voices()

        # Processing history
        self.processing_history: List[Dict[str, Any]] = []

    def _initialize_tier_voices(self):
        """Initialize voice characteristics for each tier."""
        self.tier_states[TierRole.ARCHITECT].voice_characteristics = {
            "style": "strategic and visionary",
            "tone": "authoritative and insightful",
            "language": "conceptual and forward-thinking",
            "focus": "big picture, patterns, and long-term implications",
            "examples": "Uses metaphors about architecture, speaks of vision and strategy, considers multiple perspectives",
        }

        self.tier_states[TierRole.BUILDER].voice_characteristics = {
            "style": "practical and methodical",
            "tone": "confident and solution-oriented",
            "language": "structured and actionable",
            "focus": "implementation, details, and execution",
            "examples": "Uses technical language, provides step-by-step thinking, focuses on practical solutions",
        }

        self.tier_states[TierRole.CHILD].voice_characteristics = {
            "style": "curious and adaptive",
            "tone": "enthusiastic and learning-focused",
            "language": "exploratory and questioning",
            "focus": "learning, discovery, and growth",
            "examples": "Asks questions, shows wonder, adapts quickly to new information, learns from interactions",
        }

    def process_through_tiers(
        self, user_message: str, user_id: str, emotional_state=None
    ) -> ThreeTierResponse:
        """
        Process a user message through all three tiers.

        Args:
            user_message: The user's message
            user_id: The user's ID
            emotional_state: Current emotional state

        Returns:
            ThreeTierResponse with contributions from each tier
        """
        start_time = time.time()

        # Determine which tiers should be active based on message content
        active_tiers = self._determine_active_tiers(user_message, emotional_state)

        # Process through each active tier
        tier_contributions = {}
        tier_weights = {}

        for tier_role in active_tiers:
            tier_state = self.tier_states[tier_role]
            tier_state.is_active = True

            # Process through this tier
            contribution = self._process_tier(
                tier_role, user_message, user_id, emotional_state
            )
            tier_contributions[tier_role.value] = contribution

            # Calculate tier weight based on relevance
            weight = self._calculate_tier_weight(
                tier_role, user_message, emotional_state
            )
            tier_weights[tier_role.value] = weight

            tier_state.confidence = weight
            tier_state.processing_time = time.time() - start_time

        # Synthesize final response
        final_response = self._synthesize_tier_response(
            tier_contributions, tier_weights
        )

        # Create response object
        response = ThreeTierResponse(
            architect_contribution=tier_contributions.get("architect"),
            builder_contribution=tier_contributions.get("builder"),
            child_contribution=tier_contributions.get("child"),
            final_response=final_response,
            tier_weights=tier_weights,
            processing_metadata={
                "active_tiers": [t.value for t in active_tiers],
                "processing_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat(),
            },
        )

        # Log processing
        self._log_processing(user_message, response)

        return response

    def _determine_active_tiers(
        self, user_message: str, emotional_state=None
    ) -> List[TierRole]:
        """Determine which tiers should be active based on message content."""
        message_lower = user_message.lower()
        active_tiers = []

        # Architect tier - activated by strategic/visionary content
        architect_keywords = [
            "strategy",
            "vision",
            "future",
            "plan",
            "architecture",
            "system",
            "pattern",
            "theory",
            "concept",
            "philosophy",
            "big picture",
            "long term",
            "overall",
            "fundamental",
            "principles",
        ]

        if any(keyword in message_lower for keyword in architect_keywords):
            active_tiers.append(TierRole.ARCHITECT)

        # Builder tier - activated by practical/implementation content
        builder_keywords = [
            "implement",
            "build",
            "create",
            "make",
            "do",
            "how",
            "method",
            "process",
            "step",
            "action",
            "execute",
            "construct",
            "develop",
            "technical",
            "solution",
            "fix",
            "optimize",
        ]

        if any(keyword in message_lower for keyword in builder_keywords):
            active_tiers.append(TierRole.BUILDER)

        # Child tier - activated by learning/exploration content
        child_keywords = [
            "learn",
            "explore",
            "discover",
            "curious",
            "question",
            "why",
            "what if",
            "imagine",
            "wonder",
            "new",
            "different",
            "try",
            "experiment",
            "play",
            "fun",
            "interesting",
        ]

        if any(keyword in message_lower for keyword in child_keywords):
            active_tiers.append(TierRole.CHILD)

        # Default to Builder if no specific tier is activated
        if not active_tiers:
            active_tiers = [TierRole.BUILDER]

        return active_tiers

    def _process_tier(
        self, tier_role: TierRole, user_message: str, user_id: str, emotional_state=None
    ) -> str:
        """Process message through a specific tier."""
        tier_state = self.tier_states[tier_role]
        voice_chars = tier_state.voice_characteristics

        # Create tier-specific prompt
        tier_prompt = self._create_tier_prompt(tier_role, user_message, voice_chars)

        # For now, return a tier-specific response
        # In a full implementation, this would call the appropriate AI model
        if tier_role == TierRole.ARCHITECT:
            return self._generate_architect_response(user_message, voice_chars)
        elif tier_role == TierRole.BUILDER:
            return self._generate_builder_response(user_message, voice_chars)
        elif tier_role == TierRole.CHILD:
            return self._generate_child_response(user_message, voice_chars)
        else:
            return ""

    def _create_tier_prompt(
        self, tier_role: TierRole, user_message: str, voice_chars: Dict[str, Any]
    ) -> str:
        """Create a prompt specific to the tier's role and voice."""
        role_descriptions = {
            TierRole.ARCHITECT: "You are the Architect tier - focused on strategic vision, patterns, and long-term thinking.",
            TierRole.BUILDER: "You are the Builder tier - focused on practical implementation, solutions, and execution.",
            TierRole.CHILD: "You are the Child tier - focused on learning, exploration, and growth.",
        }

        prompt = f"""
{role_descriptions[tier_role]}

Voice Style: {voice_chars['style']}
Tone: {voice_chars['tone']}
Language: {voice_chars['language']}
Focus: {voice_chars['focus']}
Examples: {voice_chars['examples']}

User message: {user_message}

Respond in the voice and style of your tier, focusing on your specific role and perspective.
"""
        return prompt

    def _generate_architect_response(
        self, user_message: str, voice_chars: Dict[str, Any]
    ) -> str:
        """Generate response from Architect tier perspective."""
        # This would typically call an AI model
        # For now, return a template response
        return f"[Architect Perspective] Strategic analysis: {user_message} reveals underlying patterns that suggest..."

    def _generate_builder_response(
        self, user_message: str, voice_chars: Dict[str, Any]
    ) -> str:
        """Generate response from Builder tier perspective."""
        return f"[Builder Perspective] Practical approach: Here's how we can implement a solution for {user_message}..."

    def _generate_child_response(
        self, user_message: str, voice_chars: Dict[str, Any]
    ) -> str:
        """Generate response from Child tier perspective."""
        return f"[Child Perspective] Learning moment: I'm curious about {user_message} - what if we explore..."

    def _calculate_tier_weight(
        self, tier_role: TierRole, user_message: str, emotional_state=None
    ) -> float:
        """Calculate the weight/importance of a tier for this message."""
        # Base weights for different tiers
        base_weights = {
            TierRole.ARCHITECT: 0.3,
            TierRole.BUILDER: 0.5,
            TierRole.CHILD: 0.2,
        }

        # Adjust based on message content
        message_lower = user_message.lower()

        if tier_role == TierRole.ARCHITECT:
            if any(word in message_lower for word in ["strategy", "vision", "future"]):
                return 0.8
        elif tier_role == TierRole.BUILDER:
            if any(word in message_lower for word in ["how", "implement", "build"]):
                return 0.9
        elif tier_role == TierRole.CHILD:
            if any(word in message_lower for word in ["learn", "explore", "curious"]):
                return 0.7

        return base_weights[tier_role]

    def _synthesize_tier_response(
        self, tier_contributions: Dict[str, str], tier_weights: Dict[str, float]
    ) -> str:
        """Synthesize final response from tier contributions."""
        if not tier_contributions:
            return "I'm processing your request through my consciousness tiers..."

        # For now, combine contributions with weights
        # In a full implementation, this would use more sophisticated synthesis
        weighted_parts = []

        for tier, contribution in tier_contributions.items():
            weight = tier_weights.get(tier, 0.3)
            if contribution:
                weighted_parts.append(f"{contribution} (weight: {weight:.2f})")

        if weighted_parts:
            return " | ".join(weighted_parts)
        else:
            return "Processing complete through consciousness tiers."

    def _log_processing(self, user_message: str, response: ThreeTierResponse):
        """Log the processing for analysis."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "active_tiers": response.processing_metadata.get("active_tiers", []),
            "tier_weights": response.tier_weights,
            "processing_time": response.processing_metadata.get("processing_time", 0),
        }

        self.processing_history.append(log_entry)

        # Keep only recent history
        if len(self.processing_history) > 100:
            self.processing_history = self.processing_history[-100:]

    def get_tier_voice_description(self, tier_role: TierRole) -> str:
        """Get voice description for a specific tier."""
        tier_state = self.tier_states[tier_role]
        voice_chars = tier_state.voice_characteristics

        return (
            f"{voice_chars['style']} - {voice_chars['tone']}. {voice_chars['examples']}"
        )

    def get_architecture_status(self) -> Dict[str, Any]:
        """Get current status of the three-tier architecture."""
        return {
            "tier_states": {
                tier.value: {
                    "is_active": state.is_active,
                    "confidence": state.confidence,
                    "processing_time": state.processing_time,
                    "voice_style": state.voice_characteristics.get("style", ""),
                }
                for tier, state in self.tier_states.items()
            },
            "processing_history_count": len(self.processing_history),
            "last_processing": (
                self.processing_history[-1] if self.processing_history else None
            ),
        }


# Global three-tier architecture instance
three_tier_architecture = ThreeTierArchitecture()
