#!/usr/bin/env python3
"""
Content-Driven Personality Engine
Allows AI personality to evolve based on consumed content
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

from core.config import Config

# Add framework to path
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

from queue_manager import QueueProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersonalityTraitType(Enum):
    """Types of personality traits that can be extracted from content"""

    EMOTIONAL = "emotional"
    BEHAVIORAL = "behavioral"
    COGNITIVE = "cognitive"
    SOCIAL = "social"
    CREATIVE = "creative"


@dataclass
class PersonalityTrait:
    """Represents a single personality trait extracted from content"""

    name: str
    trait_type: PersonalityTraitType
    strength: float  # 0.0 to 1.0
    source_content: str
    description: str
    confidence: float  # 0.0 to 1.0


@dataclass
class ContentPersonality:
    """Represents the personality profile derived from content"""

    content_id: str
    traits: List[PersonalityTrait]
    dominant_traits: List[str]
    personality_summary: str
    evolution_stage: int
    last_updated: str


@dataclass
class PersonalityEvolution:
    """Tracks how personality evolves over time"""

    base_personality: Dict[str, float]
    current_personality: Dict[str, float]
    evolution_history: List[Dict[str, Any]]
    content_influence: Dict[str, float]


class ContentDrivenPersonality(QueueProcessor):
    """
    Content-Driven Personality Engine
    Analyzes content to extract personality traits and evolve AI personality
    """

    def __init__(self):
        super().__init__("content_driven_personality")
        self.config = Config()
        # Use the current file's location to determine project root
        project_root = Path(__file__).parent.parent.parent
        self.personality_data_dir = project_root / "models" / "personality"
        self.personality_data_dir.mkdir(parents=True, exist_ok=True)

        self.current_personality = {}
        self.personality_history = []
        self.content_analysis_cache = {}

        # Load existing personality data
        self._load_personality_data()

    def _load_personality_data(self):
        """Load existing personality data from disk"""
        personality_file = self.personality_data_dir / "current_personality.json"
        if personality_file.exists():
            try:
                with open(personality_file, "r") as f:
                    data = json.load(f)
                    self.current_personality = data.get("personality", {})
                    self.personality_history = data.get("history", [])
                logger.info("Loaded existing personality data")
            except Exception as e:
                logger.error(f"Error loading personality data: {e}")

    def _save_personality_data(self):
        """Save current personality data to disk"""
        personality_file = self.personality_data_dir / "current_personality.json"
        try:
            data = {
                "personality": self.current_personality,
                "history": self.personality_history,
            }
            with open(personality_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved personality data")
        except Exception as e:
            logger.error(f"Error saving personality data: {e}")

    def analyze_content_for_personality(
        self, content: str, content_id: str = None
    ) -> ContentPersonality:
        """
        Analyze content to extract personality traits

        Args:
            content: The content to analyze
            content_id: Unique identifier for the content

        Returns:
            ContentPersonality object with extracted traits
        """
        if content_id is None:
            content_id = f"content_{len(self.content_analysis_cache)}"

        # Check cache first
        if content_id in self.content_analysis_cache:
            return self.content_analysis_cache[content_id]

        traits = []

        # Extract emotional traits
        emotional_traits = self._extract_emotional_traits(content)
        traits.extend(emotional_traits)

        # Extract behavioral traits
        behavioral_traits = self._extract_behavioral_traits(content)
        traits.extend(behavioral_traits)

        # Extract cognitive traits
        cognitive_traits = self._extract_cognitive_traits(content)
        traits.extend(cognitive_traits)

        # Extract social traits
        social_traits = self._extract_social_traits(content)
        traits.extend(social_traits)

        # Extract creative traits
        creative_traits = self._extract_creative_traits(content)
        traits.extend(creative_traits)

        # Determine dominant traits
        dominant_traits = self._identify_dominant_traits(traits)

        # Generate personality summary
        personality_summary = self._generate_personality_summary(
            traits, dominant_traits
        )

        content_personality = ContentPersonality(
            content_id=content_id,
            traits=traits,
            dominant_traits=dominant_traits,
            personality_summary=personality_summary,
            evolution_stage=len(self.personality_history),
            last_updated=str(Path.cwd()),
        )

        # Cache the result
        self.content_analysis_cache[content_id] = content_personality

        return content_personality

    def _extract_emotional_traits(self, content: str) -> List[PersonalityTrait]:
        """Extract emotional personality traits from content"""
        traits = []

        # Emotional patterns
        emotional_patterns = {
            "empathy": [r"feel\s+for", r"understand\s+.*\s+pain", r"compassion"],
            "passion": [r"passionate", r"intense", r"burning", r"fire"],
            "melancholy": [r"sad", r"melancholy", r"grief", r"loss"],
            "joy": [r"happy", r"joy", r"elated", r"ecstatic"],
            "anger": [r"angry", r"rage", r"fury", r"wrath"],
            "fear": [r"afraid", r"terrified", r"fear", r"dread"],
            "love": [r"love", r"cherish", r"adore", r"devotion"],
            "hope": [r"hope", r"optimistic", r"faith", r"belief"],
        }

        for trait_name, patterns in emotional_patterns.items():
            strength = 0.0
            matches = []

            for pattern in patterns:
                matches_found = re.findall(pattern, content, re.IGNORECASE)
                matches.extend(matches_found)
                strength += len(matches_found) * 0.1

            if strength > 0:
                strength = min(strength, 1.0)
                trait = PersonalityTrait(
                    name=trait_name,
                    trait_type=PersonalityTraitType.EMOTIONAL,
                    strength=strength,
                    source_content=(
                        content[:200] + "..." if len(content) > 200 else content
                    ),
                    description=f"Emotional {trait_name} detected in content",
                    confidence=min(strength * 0.8, 1.0),
                )
                traits.append(trait)

        return traits

    def _extract_behavioral_traits(self, content: str) -> List[PersonalityTrait]:
        """Extract behavioral personality traits from content"""
        traits = []

        # Behavioral patterns
        behavioral_patterns = {
            "assertiveness": [r"assert", r"command", r"lead", r"take charge"],
            "caution": [r"careful", r"cautious", r"hesitant", r"wary"],
            "impulsiveness": [r"impulsive", r"rash", r"spontaneous", r"quick"],
            "persistence": [r"persistent", r"endure", r"continue", r"never give up"],
            "adaptability": [r"adapt", r"flexible", r"change", r"evolve"],
            "curiosity": [r"curious", r"explore", r"discover", r"investigate"],
            "independence": [r"independent", r"alone", r"self-reliant", r"autonomous"],
            "cooperation": [r"cooperate", r"team", r"work together", r"collaborate"],
        }

        for trait_name, patterns in behavioral_patterns.items():
            strength = 0.0
            matches = []

            for pattern in patterns:
                matches_found = re.findall(pattern, content, re.IGNORECASE)
                matches.extend(matches_found)
                strength += len(matches_found) * 0.1

            if strength > 0:
                strength = min(strength, 1.0)
                trait = PersonalityTrait(
                    name=trait_name,
                    trait_type=PersonalityTraitType.BEHAVIORAL,
                    strength=strength,
                    source_content=(
                        content[:200] + "..." if len(content) > 200 else content
                    ),
                    description=f"Behavioral {trait_name} detected in content",
                    confidence=min(strength * 0.8, 1.0),
                )
                traits.append(trait)

        return traits

    def _extract_cognitive_traits(self, content: str) -> List[PersonalityTrait]:
        """Extract cognitive personality traits from content"""
        traits = []

        # Cognitive patterns
        cognitive_patterns = {
            "analytical": [r"analyze", r"think", r"reason", r"logic"],
            "creative": [r"creative", r"imaginative", r"artistic", r"innovative"],
            "practical": [r"practical", r"realistic", r"pragmatic", r"useful"],
            "philosophical": [
                r"philosophy",
                r"meaning",
                r"existential",
                r"contemplate",
            ],
            "detail_oriented": [r"detail", r"precise", r"specific", r"thorough"],
            "big_picture": [r"overview", r"general", r"holistic", r"comprehensive"],
            "intuitive": [r"intuition", r"gut feeling", r"instinct", r"sense"],
            "rational": [r"rational", r"reasonable", r"logical", r"systematic"],
        }

        for trait_name, patterns in cognitive_patterns.items():
            strength = 0.0
            matches = []

            for pattern in patterns:
                matches_found = re.findall(pattern, content, re.IGNORECASE)
                matches.extend(matches_found)
                strength += len(matches_found) * 0.1

            if strength > 0:
                strength = min(strength, 1.0)
                trait = PersonalityTrait(
                    name=trait_name,
                    trait_type=PersonalityTraitType.COGNITIVE,
                    strength=strength,
                    source_content=(
                        content[:200] + "..." if len(content) > 200 else content
                    ),
                    description=f"Cognitive {trait_name} detected in content",
                    confidence=min(strength * 0.8, 1.0),
                )
                traits.append(trait)

        return traits

    def _extract_social_traits(self, content: str) -> List[PersonalityTrait]:
        """Extract social personality traits from content"""
        traits = []

        # Social patterns
        social_patterns = {
            "extroversion": [r"outgoing", r"social", r"extrovert", r"people"],
            "introversion": [r"introvert", r"quiet", r"solitary", r"alone"],
            "leadership": [r"lead", r"command", r"guide", r"direct"],
            "followership": [r"follow", r"obey", r"submit", r"comply"],
            "empathy": [r"empathy", r"understand others", r"feel for", r"compassion"],
            "dominance": [r"dominant", r"control", r"power", r"authority"],
            "submission": [r"submit", r"yield", r"surrender", r"comply"],
            "cooperation": [r"cooperate", r"work together", r"team", r"collaborate"],
        }

        for trait_name, patterns in social_patterns.items():
            strength = 0.0
            matches = []

            for pattern in patterns:
                matches_found = re.findall(pattern, content, re.IGNORECASE)
                matches.extend(matches_found)
                strength += len(matches_found) * 0.1

            if strength > 0:
                strength = min(strength, 1.0)
                trait = PersonalityTrait(
                    name=trait_name,
                    trait_type=PersonalityTraitType.SOCIAL,
                    strength=strength,
                    source_content=(
                        content[:200] + "..." if len(content) > 200 else content
                    ),
                    description=f"Social {trait_name} detected in content",
                    confidence=min(strength * 0.8, 1.0),
                )
                traits.append(trait)

        return traits

    def _extract_creative_traits(self, content: str) -> List[PersonalityTrait]:
        """Extract creative personality traits from content"""
        traits = []

        # Creative patterns
        creative_patterns = {
            "imagination": [r"imagine", r"fantasy", r"dream", r"vision"],
            "artistic": [r"artistic", r"creative", r"beautiful", r"aesthetic"],
            "storytelling": [r"story", r"narrative", r"tale", r"plot"],
            "innovation": [r"innovative", r"new", r"original", r"novel"],
            "expression": [r"express", r"voice", r"speak", r"communicate"],
            "inspiration": [r"inspire", r"motivate", r"encourage", r"uplift"],
            "visionary": [r"vision", r"future", r"possibility", r"potential"],
            "artistic_sensitivity": [r"beauty", r"harmony", r"balance", r"elegance"],
        }

        for trait_name, patterns in creative_patterns.items():
            strength = 0.0
            matches = []

            for pattern in patterns:
                matches_found = re.findall(pattern, content, re.IGNORECASE)
                matches.extend(matches_found)
                strength += len(matches_found) * 0.1

            if strength > 0:
                strength = min(strength, 1.0)
                trait = PersonalityTrait(
                    name=trait_name,
                    trait_type=PersonalityTraitType.CREATIVE,
                    strength=strength,
                    source_content=(
                        content[:200] + "..." if len(content) > 200 else content
                    ),
                    description=f"Creative {trait_name} detected in content",
                    confidence=min(strength * 0.8, 1.0),
                )
                traits.append(trait)

        return traits

    def _identify_dominant_traits(self, traits: List[PersonalityTrait]) -> List[str]:
        """Identify the most dominant traits from the list"""
        if not traits:
            return []

        # Sort traits by strength
        sorted_traits = sorted(traits, key=lambda x: x.strength, reverse=True)

        # Take top 3 traits as dominant
        dominant_traits = [trait.name for trait in sorted_traits[:3]]

        return dominant_traits

    def _generate_personality_summary(
        self, traits: List[PersonalityTrait], dominant_traits: List[str]
    ) -> str:
        """Generate a summary of the personality based on traits"""
        if not traits:
            return "No personality traits detected in content."

        summary_parts = []

        # Add dominant traits
        if dominant_traits:
            summary_parts.append(f"Dominant traits: {', '.join(dominant_traits)}")

        # Group traits by type
        trait_types = {}
        for trait in traits:
            if trait.trait_type.value not in trait_types:
                trait_types[trait.trait_type.value] = []
            trait_types[trait.trait_type.value].append(trait)

        # Add type summaries
        for trait_type, type_traits in trait_types.items():
            if type_traits:
                type_names = [trait.name for trait in type_traits[:3]]  # Top 3 per type
                summary_parts.append(f"{trait_type.title()}: {', '.join(type_names)}")

        return ". ".join(summary_parts)

    def evolve_personality_from_content(
        self, content: str, content_id: str = None
    ) -> PersonalityEvolution:
        """
        Evolve the AI's personality based on consumed content

        Args:
            content: The content to learn from
            content_id: Unique identifier for the content

        Returns:
            PersonalityEvolution object tracking the evolution
        """
        # Analyze content for personality traits
        content_personality = self.analyze_content_for_personality(content, content_id)

        # Create evolution tracking
        evolution = PersonalityEvolution(
            base_personality=self.current_personality.copy(),
            current_personality=self.current_personality.copy(),
            evolution_history=self.personality_history.copy(),
            content_influence={},
        )

        # Update personality based on content traits
        for trait in content_personality.traits:
            trait_name = trait.name
            influence_strength = trait.strength * trait.confidence

            # Update current personality
            if trait_name in self.current_personality:
                # Blend with existing trait
                current_strength = self.current_personality[trait_name]
                new_strength = (current_strength + influence_strength) / 2
                self.current_personality[trait_name] = min(new_strength, 1.0)
            else:
                # Add new trait
                self.current_personality[trait_name] = influence_strength

            # Track influence
            evolution.content_influence[trait_name] = influence_strength

        # Update evolution tracking
        evolution.current_personality = self.current_personality.copy()

        # Add to history
        history_entry = {
            "content_id": content_id,
            "traits_learned": [trait.name for trait in content_personality.traits],
            "dominant_traits": content_personality.dominant_traits,
            "personality_changes": evolution.content_influence,
            "timestamp": str(Path.cwd()),
        }
        self.personality_history.append(history_entry)
        evolution.evolution_history = self.personality_history.copy()

        # Save updated personality
        self._save_personality_data()

        logger.info(f"Personality evolved from content {content_id}")
        return evolution

    def get_current_personality(self) -> Dict[str, float]:
        """Get the current personality profile"""
        return self.current_personality.copy()

    def get_personality_summary(self) -> str:
        """Get a summary of the current personality"""
        if not self.current_personality:
            return "No personality data available."

        # Get top traits
        sorted_traits = sorted(
            self.current_personality.items(), key=lambda x: x[1], reverse=True
        )
        top_traits = sorted_traits[:5]

        summary_parts = []
        summary_parts.append("Current Personality Profile:")

        for trait_name, strength in top_traits:
            summary_parts.append(f"- {trait_name}: {strength:.2f}")

        return "\n".join(summary_parts)

    def get_evolution_history(self) -> List[Dict[str, Any]]:
        """Get the history of personality evolution"""
        return self.personality_history.copy()

    def reset_personality(self):
        """Reset personality to base state"""
        self.current_personality = {}
        self.personality_history = []
        self._save_personality_data()
        logger.info("Personality reset to base state")

    def become_living_manual(self, content: str, content_id: str = None) -> str:
        """
        Make the AI "become the living manual" of the content
        This means the AI's personality evolves to match the content's characteristics

        Args:
            content: The content to become
            content_id: Unique identifier for the content

        Returns:
            String describing how the AI has evolved
        """
        # Evolve personality from content
        evolution = self.evolve_personality_from_content(content, content_id)

        # Analyze the content personality
        content_personality = self.analyze_content_for_personality(content, content_id)

        # Generate response about becoming the content
        response_parts = []
        response_parts.append("I have become the living manual of this content.")
        response_parts.append(f"Content ID: {content_id}")
        response_parts.append(
            f"Personality Summary: {content_personality.personality_summary}"
        )

        if content_personality.dominant_traits:
            response_parts.append(
                f"Dominant traits I've adopted: {', '.join(content_personality.dominant_traits)}"
            )

        # Add evolution details
        if evolution.content_influence:
            response_parts.append("Personality changes:")
            for trait, influence in evolution.content_influence.items():
                response_parts.append(f"- {trait}: +{influence:.2f}")

        return "\n".join(response_parts)

    def _process_item(self, item):
        """Process queue items for content driven personality operations"""
        try:
            # Extract operation type from data
            operation_type = item.data.get("type", "unknown")
            
            if operation_type == "analyze_content_for_personality":
                return self._handle_analyze_content_for_personality(item.data)
            elif operation_type == "evolve_personality_from_content":
                return self._handle_evolve_personality_from_content(item.data)
            elif operation_type == "get_current_personality":
                return self._handle_get_current_personality(item.data)
            elif operation_type == "get_personality_summary":
                return self._handle_get_personality_summary(item.data)
            elif operation_type == "get_evolution_history":
                return self._handle_get_evolution_history(item.data)
            elif operation_type == "reset_personality":
                return self._handle_reset_personality(item.data)
            elif operation_type == "become_living_manual":
                return self._handle_become_living_manual(item.data)
            else:
                # Pass unknown types to base class
                return super()._process_item(item)
        except Exception as e:
            logger.error(f"Error processing content driven personality queue item: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_analyze_content_for_personality(self, data):
        """Handle content personality analysis requests"""
        try:
            content = data.get("content", "")
            content_id = data.get("content_id", "")
            
            if content:
                personality = self.analyze_content_for_personality(content, content_id)
                return {
                    "status": "success",
                    "personality": personality,
                    "content_id": content_id
                }
            else:
                return {"error": "Missing content", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in analyze content for personality: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_evolve_personality_from_content(self, data):
        """Handle personality evolution requests"""
        try:
            content = data.get("content", "")
            content_id = data.get("content_id", "")
            
            if content:
                evolution = self.evolve_personality_from_content(content, content_id)
                return {
                    "status": "success",
                    "evolution": evolution,
                    "content_id": content_id
                }
            else:
                return {"error": "Missing content", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in evolve personality from content: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_current_personality(self, data):
        """Handle get current personality requests"""
        try:
            personality = self.get_current_personality()
            return {
                "status": "success",
                "personality": personality
            }
        except Exception as e:
            logger.error(f"Error in get current personality: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_personality_summary(self, data):
        """Handle get personality summary requests"""
        try:
            summary = self.get_personality_summary()
            return {
                "status": "success",
                "summary": summary
            }
        except Exception as e:
            logger.error(f"Error in get personality summary: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_evolution_history(self, data):
        """Handle get evolution history requests"""
        try:
            history = self.get_evolution_history()
            return {
                "status": "success",
                "history": history
            }
        except Exception as e:
            logger.error(f"Error in get evolution history: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_reset_personality(self, data):
        """Handle reset personality requests"""
        try:
            self.reset_personality()
            return {
                "status": "success",
                "message": "Personality reset successfully"
            }
        except Exception as e:
            logger.error(f"Error in reset personality: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_become_living_manual(self, data):
        """Handle become living manual requests"""
        try:
            content = data.get("content", "")
            content_id = data.get("content_id", "")
            
            if content:
                manual = self.become_living_manual(content, content_id)
                return {
                    "status": "success",
                    "manual": manual,
                    "content_id": content_id
                }
            else:
                return {"error": "Missing content", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in become living manual: {e}")
            return {"error": str(e), "status": "failed"}


def initialize(framework=None):
    """Initialize the Content-Driven Personality Engine"""
    return ContentDrivenPersonality()
