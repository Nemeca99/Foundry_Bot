#!/usr/bin/env python3
"""
Character Development Engine
Provides character growth and evolution systems, character arc tracking, and character development suggestions
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime
import random

from core.config import Config

# Add framework to path
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

from queue_manager import QueueProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DevelopmentStage(Enum):
    """Stages of character development"""

    INTRODUCTION = "introduction"
    CONFLICT = "conflict"
    GROWTH = "growth"
    CRISIS = "crisis"
    RESOLUTION = "resolution"
    TRANSFORMATION = "transformation"


class DevelopmentTrigger(Enum):
    """Triggers that can cause character development"""

    STORY_EVENT = "story_event"
    CHARACTER_INTERACTION = "character_interaction"
    EMOTIONAL_EXPERIENCE = "emotional_experience"
    CHALLENGE_OVERCOME = "challenge_overcome"
    RELATIONSHIP_CHANGE = "relationship_change"
    SELF_REFLECTION = "self_reflection"


@dataclass
class CharacterArc:
    """Represents a character's development arc"""

    arc_id: str
    character_name: str
    current_stage: DevelopmentStage
    arc_description: str
    development_triggers: List[DevelopmentTrigger]
    growth_areas: List[str]
    challenges_overcome: List[str]
    transformation_summary: str
    timestamp: str


@dataclass
class DevelopmentEvent:
    """Represents a character development event"""

    event_id: str
    character_name: str
    trigger: DevelopmentTrigger
    description: str
    impact_score: float  # 0.0 to 1.0
    growth_areas_affected: List[str]
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    timestamp: str


@dataclass
class CharacterGrowth:
    """Represents character growth in specific areas"""

    character_name: str
    growth_areas: Dict[str, float]  # area: growth_score
    development_history: List[str]
    current_challenges: List[str]
    future_goals: List[str]
    transformation_level: float  # 0.0 to 1.0


class CharacterDevelopmentEngine(QueueProcessor):
    """
    Character Development Engine
    Provides character growth and evolution tracking
    """

    def __init__(self):
        super().__init__("character_development_engine")
        self.config = Config()
        # Use the current file's location to determine project root
        project_root = Path(__file__).parent.parent.parent
        self.development_data_dir = project_root / "models" / "development"
        self.development_data_dir.mkdir(parents=True, exist_ok=True)

        self.character_arcs = {}
        self.development_events = {}
        self.character_growth = {}

        # Load existing development data
        self._load_development_data()

    def _load_development_data(self):
        """Load existing development data from disk"""
        development_file = self.development_data_dir / "development_data.json"
        if development_file.exists():
            try:
                with open(development_file, "r") as f:
                    data = json.load(f)
                    self.character_arcs = data.get("character_arcs", {})
                    self.development_events = data.get("development_events", [])
                    self.character_growth = data.get("character_growth", {})
                logger.info("Loaded existing development data")
            except Exception as e:
                logger.error(f"Error loading development data: {e}")

    def _save_development_data(self):
        """Save current development data to disk"""
        development_file = self.development_data_dir / "development_data.json"
        try:
            # Convert enum values to strings for JSON serialization
            serializable_arcs = {}
            for character, arc_data in self.character_arcs.items():
                if isinstance(arc_data, dict):
                    serializable_arcs[character] = arc_data
                else:
                    # Convert CharacterArc to dict
                    arc_dict = asdict(arc_data)
                    arc_dict["current_stage"] = arc_data.current_stage.value
                    arc_dict["development_triggers"] = [
                        trigger.value for trigger in arc_data.development_triggers
                    ]
                    serializable_arcs[character] = arc_dict

            serializable_events = []
            for event in self.development_events:
                if isinstance(event, dict):
                    # Already a dict, just ensure enum values are strings
                    event_copy = event.copy()
                    if "trigger" in event_copy and hasattr(
                        event_copy["trigger"], "value"
                    ):
                        event_copy["trigger"] = event_copy["trigger"].value
                    serializable_events.append(event_copy)
                else:
                    # Convert dataclass to dict with string enum values
                    event_dict = asdict(event)
                    event_dict["trigger"] = event.trigger.value
                    serializable_events.append(event_dict)

            data = {
                "character_arcs": serializable_arcs,
                "development_events": serializable_events,
                "character_growth": self.character_growth,
            }
            with open(development_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved development data")
        except Exception as e:
            logger.error(f"Error saving development data: {e}")

    def _process_item(self, item):
        """Process queue items for character development engine operations"""
        try:
            # Extract operation type from data
            operation_type = item.data.get("type", "unknown")
            
            if operation_type == "create_character_arc":
                return self._handle_create_character_arc(item.data)
            elif operation_type == "add_development_event":
                return self._handle_add_development_event(item.data)
            elif operation_type == "get_character_arc":
                return self._handle_get_character_arc(item.data)
            elif operation_type == "get_development_events":
                return self._handle_get_development_events(item.data)
            elif operation_type == "get_character_growth":
                return self._handle_get_character_growth(item.data)
            elif operation_type == "suggest_character_development":
                return self._handle_suggest_character_development(item.data)
            elif operation_type == "analyze_character_progress":
                return self._handle_analyze_character_progress(item.data)
            elif operation_type == "get_character_development_summary":
                return self._handle_get_character_development_summary(item.data)
            elif operation_type == "create_development_scenario":
                return self._handle_create_development_scenario(item.data)
            elif operation_type == "advance_character_manually":
                return self._handle_advance_character_manually(item.data)
            elif operation_type == "reset_character_development":
                return self._handle_reset_character_development(item.data)
            elif operation_type == "reset_all_development":
                return self._handle_reset_all_development(item.data)
            else:
                # Pass unknown types to base class
                return super()._process_item(item)
        except Exception as e:
            logger.error(f"Error processing character development engine queue item: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_create_character_arc(self, data):
        """Handle create character arc requests"""
        try:
            character_name = data.get("character_name", "")
            arc_description = data.get("arc_description", "")
            initial_stage = data.get("initial_stage", "introduction")
            
            if character_name and arc_description:
                if initial_stage == "introduction":
                    stage = DevelopmentStage.INTRODUCTION
                elif initial_stage == "conflict":
                    stage = DevelopmentStage.CONFLICT
                elif initial_stage == "growth":
                    stage = DevelopmentStage.GROWTH
                elif initial_stage == "crisis":
                    stage = DevelopmentStage.CRISIS
                elif initial_stage == "resolution":
                    stage = DevelopmentStage.RESOLUTION
                elif initial_stage == "transformation":
                    stage = DevelopmentStage.TRANSFORMATION
                else:
                    stage = DevelopmentStage.INTRODUCTION
                
                arc = self.create_character_arc(character_name, arc_description, stage)
                return {
                    "status": "success",
                    "arc": arc,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name or arc_description", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in create character arc: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_add_development_event(self, data):
        """Handle add development event requests"""
        try:
            character_name = data.get("character_name", "")
            trigger = data.get("trigger", "")
            description = data.get("description", "")
            impact_score = data.get("impact_score", 0.5)
            growth_areas_affected = data.get("growth_areas_affected", [])
            before_state = data.get("before_state", {})
            after_state = data.get("after_state", {})
            
            if character_name and trigger and description:
                if trigger == "story_event":
                    dev_trigger = DevelopmentTrigger.STORY_EVENT
                elif trigger == "character_interaction":
                    dev_trigger = DevelopmentTrigger.CHARACTER_INTERACTION
                elif trigger == "emotional_experience":
                    dev_trigger = DevelopmentTrigger.EMOTIONAL_EXPERIENCE
                elif trigger == "challenge_overcome":
                    dev_trigger = DevelopmentTrigger.CHALLENGE_OVERCOME
                elif trigger == "relationship_change":
                    dev_trigger = DevelopmentTrigger.RELATIONSHIP_CHANGE
                elif trigger == "self_reflection":
                    dev_trigger = DevelopmentTrigger.SELF_REFLECTION
                else:
                    dev_trigger = DevelopmentTrigger.STORY_EVENT
                
                event = self.add_development_event(character_name, dev_trigger, description, impact_score, growth_areas_affected, before_state, after_state)
                return {
                    "status": "success",
                    "event": event,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing required parameters", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in add development event: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_character_arc(self, data):
        """Handle get character arc requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                arc = self.get_character_arc(character_name)
                return {
                    "status": "success",
                    "arc": arc,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get character arc: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_development_events(self, data):
        """Handle get development events requests"""
        try:
            character_name = data.get("character_name", "")
            trigger = data.get("trigger", "")
            
            if character_name:
                if trigger:
                    if trigger == "story_event":
                        dev_trigger = DevelopmentTrigger.STORY_EVENT
                    elif trigger == "character_interaction":
                        dev_trigger = DevelopmentTrigger.CHARACTER_INTERACTION
                    elif trigger == "emotional_experience":
                        dev_trigger = DevelopmentTrigger.EMOTIONAL_EXPERIENCE
                    elif trigger == "challenge_overcome":
                        dev_trigger = DevelopmentTrigger.CHALLENGE_OVERCOME
                    elif trigger == "relationship_change":
                        dev_trigger = DevelopmentTrigger.RELATIONSHIP_CHANGE
                    elif trigger == "self_reflection":
                        dev_trigger = DevelopmentTrigger.SELF_REFLECTION
                    else:
                        dev_trigger = None
                else:
                    dev_trigger = None
                
                events = self.get_development_events(character_name, dev_trigger)
                return {
                    "status": "success",
                    "events": events,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get development events: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_character_growth(self, data):
        """Handle get character growth requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                growth = self.get_character_growth(character_name)
                return {
                    "status": "success",
                    "growth": growth,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get character growth: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_suggest_character_development(self, data):
        """Handle suggest character development requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                suggestions = self.suggest_character_development(character_name)
                return {
                    "status": "success",
                    "suggestions": suggestions,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in suggest character development: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_analyze_character_progress(self, data):
        """Handle analyze character progress requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                analysis = self.analyze_character_progress(character_name)
                return {
                    "status": "success",
                    "analysis": analysis,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in analyze character progress: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_get_character_development_summary(self, data):
        """Handle get character development summary requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                summary = self.get_character_development_summary(character_name)
                return {
                    "status": "success",
                    "summary": summary,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in get character development summary: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_create_development_scenario(self, data):
        """Handle create development scenario requests"""
        try:
            character_name = data.get("character_name", "")
            scenario_type = data.get("scenario_type", "")
            
            if character_name and scenario_type:
                scenario = self.create_development_scenario(character_name, scenario_type)
                return {
                    "status": "success",
                    "scenario": scenario,
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name or scenario_type", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in create development scenario: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_advance_character_manually(self, data):
        """Handle advance character manually requests"""
        try:
            character_name = data.get("character_name", "")
            new_stage = data.get("new_stage", "")
            
            if character_name and new_stage:
                if new_stage == "introduction":
                    stage = DevelopmentStage.INTRODUCTION
                elif new_stage == "conflict":
                    stage = DevelopmentStage.CONFLICT
                elif new_stage == "growth":
                    stage = DevelopmentStage.GROWTH
                elif new_stage == "crisis":
                    stage = DevelopmentStage.CRISIS
                elif new_stage == "resolution":
                    stage = DevelopmentStage.RESOLUTION
                elif new_stage == "transformation":
                    stage = DevelopmentStage.TRANSFORMATION
                else:
                    return {"error": "Invalid stage", "status": "failed"}
                
                self.advance_character_manually(character_name, stage)
                return {
                    "status": "success",
                    "message": f"Character {character_name} advanced to {new_stage}",
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name or new_stage", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in advance character manually: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_reset_character_development(self, data):
        """Handle reset character development requests"""
        try:
            character_name = data.get("character_name", "")
            if character_name:
                self.reset_character_development(character_name)
                return {
                    "status": "success",
                    "message": f"Development reset for {character_name}",
                    "character_name": character_name
                }
            else:
                return {"error": "Missing character_name", "status": "failed"}
        except Exception as e:
            logger.error(f"Error in reset character development: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_reset_all_development(self, data):
        """Handle reset all development requests"""
        try:
            self.reset_all_development()
            return {
                "status": "success",
                "message": "All development data reset"
            }
        except Exception as e:
            logger.error(f"Error in reset all development: {e}")
            return {"error": str(e), "status": "failed"}

    def create_character_arc(
        self,
        character_name: str,
        arc_description: str,
        initial_stage: DevelopmentStage = DevelopmentStage.INTRODUCTION,
    ) -> CharacterArc:
        """Create a character development arc"""
        arc_id = f"arc_{len(self.character_arcs)}"

        arc = CharacterArc(
            arc_id=arc_id,
            character_name=character_name,
            current_stage=initial_stage,
            arc_description=arc_description,
            development_triggers=[],
            growth_areas=[],
            challenges_overcome=[],
            transformation_summary="",
            timestamp=datetime.now().isoformat(),
        )

        # Add to character arcs
        arc_dict = asdict(arc)
        arc_dict["current_stage"] = arc.current_stage.value
        arc_dict["development_triggers"] = [
            trigger.value for trigger in arc.development_triggers
        ]
        self.character_arcs[character_name] = arc_dict

        self._save_development_data()
        logger.info(f"Created character arc for {character_name}")
        return arc

    def add_development_event(
        self,
        character_name: str,
        trigger: DevelopmentTrigger,
        description: str,
        impact_score: float = 0.5,
        growth_areas_affected: List[str] = None,
        before_state: Dict[str, Any] = None,
        after_state: Dict[str, Any] = None,
    ) -> DevelopmentEvent:
        """Add a development event for a character"""
        event_id = f"event_{len(self.development_events)}"

        event = DevelopmentEvent(
            event_id=event_id,
            character_name=character_name,
            trigger=trigger,
            description=description,
            impact_score=impact_score,
            growth_areas_affected=growth_areas_affected or [],
            before_state=before_state or {},
            after_state=after_state or {},
            timestamp=datetime.now().isoformat(),
        )

        # Add to development events
        event_dict = asdict(event)
        event_dict["trigger"] = event.trigger.value
        self.development_events.append(event_dict)

        # Update character arc if it exists
        if character_name in self.character_arcs:
            self._update_character_arc_from_event(character_name, event)

        # Update character growth
        self._update_character_growth(character_name, event)

        self._save_development_data()
        logger.info(f"Added development event for {character_name}: {trigger.value}")
        return event

    def _update_character_arc_from_event(
        self, character_name: str, event: DevelopmentEvent
    ):
        """Update character arc based on development event"""
        arc_data = self.character_arcs[character_name]

        # Add trigger to arc
        if event.trigger.value not in arc_data.get("development_triggers", []):
            arc_data["development_triggers"].append(event.trigger.value)

        # Update growth areas
        for area in event.growth_areas_affected:
            if area not in arc_data.get("growth_areas", []):
                arc_data["growth_areas"].append(area)

        # Potentially advance to next stage based on impact
        if event.impact_score > 0.7:
            self._advance_character_stage(character_name)

    def _advance_character_stage(self, character_name: str):
        """Advance character to next development stage"""
        arc_data = self.character_arcs[character_name]
        current_stage = arc_data.get("current_stage", "introduction")

        stage_progression = {
            "introduction": "conflict",
            "conflict": "growth",
            "growth": "crisis",
            "crisis": "resolution",
            "resolution": "transformation",
            "transformation": "transformation",  # Final stage
        }

        next_stage = stage_progression.get(current_stage, current_stage)
        arc_data["current_stage"] = next_stage

        logger.info(f"Advanced {character_name} from {current_stage} to {next_stage}")

    def _update_character_growth(self, character_name: str, event: DevelopmentEvent):
        """Update character growth tracking"""
        if character_name not in self.character_growth:
            self.character_growth[character_name] = {
                "character_name": character_name,
                "growth_areas": {},
                "development_history": [],
                "current_challenges": [],
                "future_goals": [],
                "transformation_level": 0.0,
            }

        growth_data = self.character_growth[character_name]

        # Update growth areas
        for area in event.growth_areas_affected:
            if area not in growth_data["growth_areas"]:
                growth_data["growth_areas"][area] = 0.0
            growth_data["growth_areas"][area] += event.impact_score

        # Add to development history
        growth_data["development_history"].append(
            f"{event.timestamp}: {event.description}"
        )

        # Update transformation level
        total_growth = sum(growth_data["growth_areas"].values())
        growth_data["transformation_level"] = min(
            total_growth / 10.0, 1.0
        )  # Normalize to 0-1

    def get_character_arc(self, character_name: str) -> Dict:
        """Get a character's development arc"""
        return self.character_arcs.get(character_name, {})

    def get_development_events(
        self, character_name: str, trigger: DevelopmentTrigger = None
    ) -> List[Dict]:
        """Get development events for a character"""
        events = []

        for event in self.development_events:
            if event.get("character_name") == character_name:
                if trigger is None or event.get("trigger") == trigger.value:
                    events.append(event)

        return events

    def get_character_growth(self, character_name: str) -> Dict:
        """Get a character's growth data"""
        return self.character_growth.get(character_name, {})

    def suggest_character_development(self, character_name: str) -> List[str]:
        """Generate development suggestions for a character"""
        suggestions = []
        arc_data = self.get_character_arc(character_name)
        growth_data = self.get_character_growth(character_name)

        if not arc_data:
            suggestions.append(
                f"Create a character arc for {character_name} to track their development journey"
            )
            return suggestions

        current_stage = arc_data.get("current_stage", "introduction")

        # Stage-specific suggestions
        if current_stage == "introduction":
            suggestions.append(
                f"Introduce {character_name} to a significant challenge or conflict"
            )
            suggestions.append(
                f"Establish {character_name}'s initial goals and motivations"
            )
        elif current_stage == "conflict":
            suggestions.append(
                f"Create opportunities for {character_name} to face their fears"
            )
            suggestions.append(
                f"Introduce obstacles that test {character_name}'s core beliefs"
            )
        elif current_stage == "growth":
            suggestions.append(f"Show {character_name} learning from their experiences")
            suggestions.append(
                f"Have {character_name} develop new skills or perspectives"
            )
        elif current_stage == "crisis":
            suggestions.append(
                f"Present {character_name} with their biggest challenge yet"
            )
            suggestions.append(
                f"Force {character_name} to question their fundamental assumptions"
            )
        elif current_stage == "resolution":
            suggestions.append(
                f"Allow {character_name} to overcome their final obstacle"
            )
            suggestions.append(f"Show {character_name} achieving their primary goal")
        elif current_stage == "transformation":
            suggestions.append(
                f"Demonstrate {character_name}'s complete transformation"
            )
            suggestions.append(
                f"Show how {character_name} has changed the world around them"
            )

        # Growth area suggestions
        if growth_data:
            growth_areas = growth_data.get("growth_areas", {})
            if growth_areas:
                weakest_area = min(growth_areas.items(), key=lambda x: x[1])
                suggestions.append(
                    f"Focus on developing {character_name}'s {weakest_area[0]} (current level: {weakest_area[1]:.2f})"
                )

        return suggestions

    def analyze_character_progress(self, character_name: str) -> Dict[str, Any]:
        """Analyze a character's development progress"""
        arc_data = self.get_character_arc(character_name)
        growth_data = self.get_character_growth(character_name)
        events = self.get_development_events(character_name)

        if not arc_data:
            return {"message": f"No development data available for {character_name}"}

        # Calculate progress metrics
        total_events = len(events)
        high_impact_events = len([e for e in events if e.get("impact_score", 0) > 0.7])
        average_impact = (
            sum(e.get("impact_score", 0) for e in events) / total_events
            if total_events > 0
            else 0
        )

        # Analyze growth areas
        growth_areas = growth_data.get("growth_areas", {})
        strongest_area = (
            max(growth_areas.items(), key=lambda x: x[1])
            if growth_areas
            else ("none", 0)
        )
        weakest_area = (
            min(growth_areas.items(), key=lambda x: x[1])
            if growth_areas
            else ("none", 0)
        )

        progress = {
            "character_name": character_name,
            "current_stage": arc_data.get("current_stage", "unknown"),
            "total_development_events": total_events,
            "high_impact_events": high_impact_events,
            "average_impact_score": average_impact,
            "transformation_level": growth_data.get("transformation_level", 0.0),
            "strongest_growth_area": strongest_area[0],
            "strongest_area_score": strongest_area[1],
            "weakest_growth_area": weakest_area[0],
            "weakest_area_score": weakest_area[1],
            "development_triggers": arc_data.get("development_triggers", []),
            "growth_areas_count": len(growth_areas),
            "challenges_overcome": len(arc_data.get("challenges_overcome", [])),
        }

        return progress

    def get_character_development_summary(self, character_name: str) -> str:
        """Get a summary of a character's development"""
        arc_data = self.get_character_arc(character_name)
        growth_data = self.get_character_growth(character_name)
        events = self.get_development_events(character_name)

        if not arc_data:
            return f"No development data available for {character_name}"

        summary_parts = []
        summary_parts.append(f"Character Development Summary for {character_name}:")
        summary_parts.append(
            f"- Current stage: {arc_data.get('current_stage', 'unknown')}"
        )
        summary_parts.append(f"- Total development events: {len(events)}")
        summary_parts.append(
            f"- Transformation level: {growth_data.get('transformation_level', 0.0):.2f}"
        )

        # Growth areas
        growth_areas = growth_data.get("growth_areas", {})
        if growth_areas:
            summary_parts.append("- Growth areas:")
            for area, score in growth_areas.items():
                summary_parts.append(f"  * {area}: {score:.2f}")

        # Development triggers
        triggers = arc_data.get("development_triggers", [])
        if triggers:
            summary_parts.append(f"- Development triggers: {', '.join(triggers)}")

        # Challenges overcome
        challenges = arc_data.get("challenges_overcome", [])
        if challenges:
            summary_parts.append(f"- Challenges overcome: {len(challenges)}")

        return "\n".join(summary_parts)

    def create_development_scenario(
        self, character_name: str, scenario_type: str
    ) -> Dict[str, Any]:
        """Create a development scenario for a character"""
        arc_data = self.get_character_arc(character_name)
        current_stage = (
            arc_data.get("current_stage", "introduction")
            if arc_data
            else "introduction"
        )

        scenarios = {
            "challenge": {
                "title": f"Challenge for {character_name}",
                "description": f"A difficult situation that tests {character_name}'s abilities and beliefs",
                "trigger": DevelopmentTrigger.STORY_EVENT,
                "impact_score": 0.8,
                "growth_areas": ["courage", "problem_solving", "resilience"],
            },
            "relationship": {
                "title": f"Relationship Development for {character_name}",
                "description": f"A meaningful interaction that changes {character_name}'s perspective",
                "trigger": DevelopmentTrigger.CHARACTER_INTERACTION,
                "impact_score": 0.6,
                "growth_areas": ["empathy", "communication", "trust"],
            },
            "emotional": {
                "title": f"Emotional Growth for {character_name}",
                "description": f"An experience that deeply affects {character_name}'s emotional state",
                "trigger": DevelopmentTrigger.EMOTIONAL_EXPERIENCE,
                "impact_score": 0.7,
                "growth_areas": ["emotional_intelligence", "self_awareness", "healing"],
            },
            "transformation": {
                "title": f"Transformation Opportunity for {character_name}",
                "description": f"A moment that could fundamentally change {character_name}'s character",
                "trigger": DevelopmentTrigger.CHALLENGE_OVERCOME,
                "impact_score": 0.9,
                "growth_areas": ["identity", "purpose", "wisdom"],
            },
        }

        scenario = scenarios.get(scenario_type, scenarios["challenge"])
        scenario["character_name"] = character_name
        scenario["current_stage"] = current_stage

        return scenario

    def advance_character_manually(
        self, character_name: str, new_stage: DevelopmentStage
    ):
        """Manually advance a character to a specific development stage"""
        if character_name not in self.character_arcs:
            logger.warning(f"No character arc found for {character_name}")
            return False

        arc_data = self.character_arcs[character_name]
        arc_data["current_stage"] = new_stage.value

        self._save_development_data()
        logger.info(f"Manually advanced {character_name} to {new_stage.value}")
        return True

    def reset_character_development(self, character_name: str):
        """Reset all development data for a character"""
        if character_name in self.character_arcs:
            del self.character_arcs[character_name]

        # Remove development events for this character
        self.development_events = [
            event
            for event in self.development_events
            if event.get("character_name") != character_name
        ]

        if character_name in self.character_growth:
            del self.character_growth[character_name]

        self._save_development_data()
        logger.info(f"Reset all development data for {character_name}")

    def reset_all_development(self):
        """Reset all development data"""
        self.character_arcs = {}
        self.development_events = []
        self.character_growth = {}
        self._save_development_data()
        logger.info("Reset all development data")


def initialize(framework=None):
    """Initialize the Character Development Engine"""
    return CharacterDevelopmentEngine()
