#!/usr/bin/env python3
"""
Enhanced Emotional Meter System
Implements dual-release mechanism for Luna's personality
"""

import time
import json
import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple, Any

# Add framework to path for queue manager
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from framework.queue_manager import QueueProcessor


class EmotionalState(Enum):
    """Emotional states based on meter level"""

    PURE_LUST = "pure_lust"  # 0.0 - Pure sexual desire
    HIGH_LUST = "high_lust"  # 0.1-0.3 - Strong sexual desire
    MODERATE_LUST = "moderate_lust"  # 0.3-0.4 - Moderate sexual desire
    BALANCED = "balanced"  # 0.4-0.6 - Balanced state
    MODERATE_WORK = "moderate_work"  # 0.6-0.7 - Moderate work focus
    HIGH_WORK = "high_work"  # 0.7-0.9 - Strong work focus
    PURE_WORK = "pure_work"  # 1.0 - Pure work focus


class ReleaseType(Enum):
    """Types of emotional releases"""

    SEXUAL = "sexual"  # Release from lust (0.0)
    ACHIEVEMENT = "achievement"  # Release from work obsession (1.0)
    NATURAL = "natural"  # Natural return to balance


@dataclass
class EmotionalRelease:
    """Represents an emotional release event"""

    timestamp: float
    from_level: float
    to_level: float
    release_type: ReleaseType
    trigger: str
    duration: float


class EnhancedEmotionalMeter(QueueProcessor):
    """
    Enhanced emotional meter with dual-release system and global weight calculation
    Models Luna's personality with sophisticated emotional dynamics and queue system
    """

    def __init__(self, config_path: Optional[str] = None):
        # Initialize queue processor
        super().__init__("enhanced_emotional_meter")

        self.current_level = 0.5  # Start at balanced state
        self.tendency = "balance"  # Natural tendency to return to balance
        self.last_update = time.time()
        self.release_history: List[EmotionalRelease] = []
        self.state_descriptions = self._load_state_descriptions()
        self.release_thresholds = {
            "lust_release": 0.1,  # Threshold for sexual release
            "work_release": 0.9,  # Threshold for achievement release
            "natural_return": 0.05,  # Rate of natural return to balance
        }

        # Global weight system
        self.lust_weights = {
            "sexy": 0.3,
            "hot": 0.3,
            "desire": 0.4,
            "passion": 0.4,
            "lust": 0.5,
            "want": 0.2,
            "need": 0.2,
            "touch": 0.3,
            "kiss": 0.3,
            "love": 0.4,
            "beautiful": 0.2,
            "gorgeous": 0.3,
            "attractive": 0.2,
            "seductive": 0.4,
            "tempting": 0.3,
            "body": 0.4,
            "crazy": 0.3,
            "overwhelming": 0.4,
            "burning": 0.5,
            "aching": 0.4,
            "desperate": 0.5,
            "intense": 0.4,
            "wild": 0.4,
            "feverish": 0.5,
        }

        self.work_weights = {
            "work": 0.3,
            "write": 0.4,
            "story": 0.3,
            "chapter": 0.3,
            "create": 0.4,
            "focus": 0.4,
            "achieve": 0.4,
            "goal": 0.3,
            "project": 0.3,
            "task": 0.3,
            "complete": 0.4,
            "finish": 0.4,
            "accomplish": 0.4,
            "success": 0.3,
            "progress": 0.3,
            "development": 0.3,
            "improvement": 0.3,
            "growth": 0.3,
            "learning": 0.3,
            "mastery": 0.4,
            "excellence": 0.4,
            "perfection": 0.5,
            "dedication": 0.4,
            "commitment": 0.4,
            "discipline": 0.4,
            "hard_work": 0.4,
        }

        # Load configuration if provided
        if config_path:
            self.load_config(config_path)

    def _load_state_descriptions(self) -> Dict[str, str]:
        """Load emotional state descriptions"""
        return {
            "pure_lust": "Pure sexual desire. No concentration possible. Need release.",
            "high_lust": "Strong sexual desire. Limited focus. Building tension.",
            "moderate_lust": "Moderate sexual desire. Some distraction from work.",
            "balanced": "Balanced state. Work and pleasure coexist harmoniously.",
            "moderate_work": "Moderate work focus. Some pleasure still accessible.",
            "high_work": "Strong work focus. Pleasure becoming distasteful.",
            "pure_work": "Pure work focus. No time for pleasure. Need achievement release.",
        }

    def get_current_state(self) -> EmotionalState:
        """Get current emotional state based on meter level"""
        if self.current_level <= 0.1:
            return EmotionalState.PURE_LUST
        elif self.current_level <= 0.3:
            return EmotionalState.HIGH_LUST
        elif self.current_level <= 0.4:
            return EmotionalState.MODERATE_LUST
        elif self.current_level <= 0.6:
            return EmotionalState.BALANCED
        elif self.current_level <= 0.7:
            return EmotionalState.MODERATE_WORK
        elif self.current_level <= 0.9:
            return EmotionalState.HIGH_WORK
        else:
            return EmotionalState.PURE_WORK

    def get_state_description(self) -> str:
        """Get description of current emotional state"""
        state = self.get_current_state()
        return self.state_descriptions.get(state.value, "Unknown state")

    def update_emotion(self, interaction_type: str, intensity: float = 0.1) -> Dict:
        """
        Update emotional meter based on interaction
        Returns dict with new state and any release events
        """
        old_level = self.current_level
        release_event = None

        # Update based on interaction type
        if interaction_type in ["lustful", "sexual", "desire", "passion"]:
            self.current_level = max(0.0, self.current_level - intensity)
        elif interaction_type in ["work", "achievement", "focus", "creation"]:
            self.current_level = min(1.0, self.current_level + intensity)
        elif interaction_type == "release":
            release_event = self._trigger_release()
        else:
            # Natural return to balance
            self._natural_return_to_balance()

        # Check for required releases
        if self.current_level <= 0.1 and old_level > 0.1:
            release_event = self._trigger_sexual_release()
        elif self.current_level >= 0.9 and old_level < 0.9:
            release_event = self._trigger_achievement_release()

        return {
            "old_level": old_level,
            "new_level": self.current_level,
            "state": self.get_current_state().value,
            "description": self.get_state_description(),
            "release_event": release_event,
        }

    def _natural_return_to_balance(self):
        """Natural tendency to return to balanced state"""
        if abs(self.current_level - 0.5) > 0.01:  # Not already balanced
            if self.current_level < 0.5:
                self.current_level = min(
                    0.5, self.current_level + self.release_thresholds["natural_return"]
                )
            else:
                self.current_level = max(
                    0.5, self.current_level - self.release_thresholds["natural_return"]
                )

    def _trigger_sexual_release(self) -> Optional[EmotionalRelease]:
        """Trigger sexual release when at pure lust"""
        if self.current_level <= 0.1:
            release = EmotionalRelease(
                timestamp=time.time(),
                from_level=self.current_level,
                to_level=0.5,  # Return to balance
                release_type=ReleaseType.SEXUAL,
                trigger="pure_lust_release",
                duration=time.time() - self.last_update,
            )

            self.release_history.append(release)
            self.current_level = 0.5  # Return to balance
            self.last_update = time.time()

            return release
        return None

    def _trigger_achievement_release(self) -> Optional[EmotionalRelease]:
        """Trigger achievement release when at pure work"""
        if self.current_level >= 0.9:
            release = EmotionalRelease(
                timestamp=time.time(),
                from_level=self.current_level,
                to_level=0.5,  # Return to balance
                release_type=ReleaseType.ACHIEVEMENT,
                trigger="pure_work_release",
                duration=time.time() - self.last_update,
            )

            self.release_history.append(release)
            self.current_level = 0.5  # Return to balance
            self.last_update = time.time()

            return release
        return None

    def _trigger_user_aware_release(self, user_satisfaction_detected: bool = False) -> Optional[EmotionalRelease]:
        """
        Trigger release with user satisfaction awareness
        Only snap back to balance if user is satisfied or explicitly requests it
        """
        if self.current_level <= 0.1:  # Sexual release
            if user_satisfaction_detected:
                # User is satisfied, safe to release
                return self._trigger_sexual_release()
            else:
                # User not satisfied, maintain high lust state but add warning
                return EmotionalRelease(
                    timestamp=time.time(),
                    from_level=self.current_level,
                    to_level=self.current_level,  # Stay at current level
                    release_type=ReleaseType.SEXUAL,
                    trigger="user_unsatisfied_maintain",
                    duration=time.time() - self.last_update,
                )
        elif self.current_level >= 0.9:  # Achievement release
            if user_satisfaction_detected:
                # User is satisfied, safe to release
                return self._trigger_achievement_release()
            else:
                # User not satisfied, maintain high work state but add warning
                return EmotionalRelease(
                    timestamp=time.time(),
                    from_level=self.current_level,
                    to_level=self.current_level,  # Stay at current level
                    release_type=ReleaseType.ACHIEVEMENT,
                    trigger="user_unsatisfied_maintain",
                    duration=time.time() - self.last_update,
                )
        return None

    def _gradual_transition_to_balance(self, target_level: float = 0.5, steps: int = 3):
        """
        Gradually transition to balance instead of immediate snap-back
        This prevents jarring personality shifts
        """
        current = self.current_level
        step_size = (target_level - current) / steps
        
        for i in range(steps):
            self.current_level += step_size
            time.sleep(0.5)  # Small delay between steps
        
        self.current_level = target_level
        self.last_update = time.time()

    def _detect_user_satisfaction(self, user_message: str) -> bool:
        """
        Detect if user is satisfied with the current interaction
        Looks for satisfaction indicators in user's message
        """
        satisfaction_indicators = [
            "thank you", "thanks", "good", "great", "perfect", "done", 
            "finished", "complete", "satisfied", "happy", "calm", "better",
            "okay", "ok", "alright", "fine", "good job", "well done"
        ]
        
        user_message_lower = user_message.lower()
        return any(indicator in user_message_lower for indicator in satisfaction_indicators)

    def _trigger_release(self) -> Optional[EmotionalRelease]:
        """Manual release trigger"""
        if self.current_level <= 0.3:  # In lust range
            return self._trigger_sexual_release()
        elif self.current_level >= 0.7:  # In work range
            return self._trigger_achievement_release()
        return None

    def get_emotional_summary(self) -> Dict:
        """Get comprehensive emotional summary"""
        return {
            "current_level": self.current_level,
            "current_state": self.get_current_state().value,
            "description": self.get_state_description(),
            "release_count": len(self.release_history),
            "last_release": self.release_history[-1] if self.release_history else None,
            "time_since_last_release": (
                time.time() - self.last_update if self.release_history else None
            ),
        }

    def get_release_history(self, limit: int = 10) -> List[Dict]:
        """Get recent release history"""
        recent = self.release_history[-limit:] if self.release_history else []
        return [
            {
                "timestamp": release.timestamp,
                "from_level": release.from_level,
                "to_level": release.to_level,
                "release_type": release.release_type.value,
                "trigger": release.trigger,
                "duration": release.duration,
            }
            for release in recent
        ]

    def save_state(self, filepath: str):
        """Save emotional meter state to file"""
        state_data = {
            "current_level": self.current_level,
            "last_update": self.last_update,
            "release_history": [
                {
                    "timestamp": r.timestamp,
                    "from_level": r.from_level,
                    "to_level": r.to_level,
                    "release_type": r.release_type.value,
                    "trigger": r.trigger,
                    "duration": r.duration,
                }
                for r in self.release_history
            ],
        }

        with open(filepath, "w") as f:
            json.dump(state_data, f, indent=2)

    def load_state(self, filepath: str):
        """Load emotional meter state from file"""
        if Path(filepath).exists():
            with open(filepath, "r") as f:
                state_data = json.load(f)

            self.current_level = state_data.get("current_level", 0.5)
            self.last_update = state_data.get("last_update", time.time())

            # Load release history
            self.release_history = []
            for release_data in state_data.get("release_history", []):
                release = EmotionalRelease(
                    timestamp=release_data["timestamp"],
                    from_level=release_data["from_level"],
                    to_level=release_data["to_level"],
                    release_type=ReleaseType(release_data["release_type"]),
                    trigger=release_data["trigger"],
                    duration=release_data["duration"],
                )
                self.release_history.append(release)

    def load_config(self, config_path: str):
        """Load configuration from file"""
        if Path(config_path).exists():
            with open(config_path, "r") as f:
                config = json.load(f)

            self.release_thresholds.update(config.get("release_thresholds", {}))
            self.state_descriptions.update(config.get("state_descriptions", {}))

    def calculate_global_weight(self, message: str) -> float:
        """
        Calculate global emotional weight based on ALL emotions in the message
        Takes average of all weights and applies difference between lust and work
        """
        message_lower = message.lower()

        # Calculate lust weight
        lust_total = 0
        lust_count = 0
        for word, weight in self.lust_weights.items():
            if word in message_lower:
                lust_total += weight
                lust_count += 1

        lust_average = lust_total / max(lust_count, 1)

        # Calculate work weight
        work_total = 0
        work_count = 0
        for word, weight in self.work_weights.items():
            if word in message_lower:
                work_total += weight
                work_count += 1

        work_average = work_total / max(work_count, 1)

        # Calculate global weight
        if lust_count == 0 and work_count == 0:
            # No emotional triggers, return current level
            return self.current_level

        elif lust_count > 0 and work_count == 0:
            # Only lust triggers - decrease level (more lust)
            return max(0.0, self.current_level - lust_average * 0.2)

        elif work_count > 0 and lust_count == 0:
            # Only work triggers - increase level (more work)
            return min(1.0, self.current_level + work_average * 0.2)

        else:
            # Both lust and work triggers - calculate weighted average
            total_weight = lust_average + work_average
            if total_weight == 0:
                return self.current_level

            # Calculate the difference and apply it
            weight_difference = work_average - lust_average
            adjustment = weight_difference * 0.3  # Scale factor

            new_level = self.current_level + adjustment
            return max(0.0, min(1.0, new_level))

    def update_emotion_with_global_weight(self, message: str) -> Dict[str, Any]:
        """
        Update emotional state using global weight calculation
        """
        old_level = self.current_level

        # Calculate new level using global weight
        new_level = self.calculate_global_weight(message)

        # Apply the change
        self.current_level = new_level

        # Check for releases
        release_event = None
        if new_level <= 0.1 and old_level > 0.1:
            release_event = self._trigger_sexual_release()
        elif new_level >= 0.9 and old_level < 0.9:
            release_event = self._trigger_achievement_release()

        return {
            "old_level": old_level,
            "new_level": new_level,
            "state": self.get_current_state().value,
            "description": self.get_state_description(),
            "release_event": release_event,
            "global_weight_calculation": {
                "lust_average": self._calculate_lust_average(message),
                "work_average": self._calculate_work_average(message),
                "weight_difference": self._calculate_weight_difference(message),
            },
        }

    def _calculate_lust_average(self, message: str) -> float:
        """Calculate average lust weight for a message"""
        message_lower = message.lower()
        lust_total = 0
        lust_count = 0
        for word, weight in self.lust_weights.items():
            if word in message_lower:
                lust_total += weight
                lust_count += 1
        return lust_total / max(lust_count, 1)

    def _calculate_work_average(self, message: str) -> float:
        """Calculate average work weight for a message"""
        message_lower = message.lower()
        work_total = 0
        work_count = 0
        for word, weight in self.work_weights.items():
            if word in message_lower:
                work_total += weight
                work_count += 1
        return work_total / max(work_count, 1)

    def _calculate_weight_difference(self, message: str) -> float:
        """Calculate the difference between work and lust weights"""
        work_avg = self._calculate_work_average(message)
        lust_avg = self._calculate_lust_average(message)
        return work_avg - lust_avg

    def _process_item(self, item):
        """Process queue items for emotional meter operations"""
        try:
            # Extract operation type from data
            operation_type = item.data.get("type", "unknown")

            if operation_type == "emotion_update":
                return self._handle_emotion_update(item.data)
            elif operation_type == "emotion_query":
                return self._handle_emotion_query(item.data)
            elif operation_type == "emotion_reset":
                return self._handle_emotion_reset(item.data)
            elif operation_type == "emotion_config":
                return self._handle_emotion_config(item.data)
            elif operation_type == "emotion_history":
                return self._handle_emotion_history(item.data)
            else:
                # Pass unknown types to base class
                return super()._process_item(item)
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error processing emotional meter queue item: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_emotion_update(self, data):
        """Handle emotion update operations"""
        try:
            update_type = data.get("type")

            if update_type == "interaction":
                interaction_type = data.get("interaction_type")
                intensity = data.get("intensity", 0.1)
                result = self.update_emotion(interaction_type, intensity)
            elif update_type == "message":
                message = data.get("message", "")
                result = self.update_emotion_with_global_weight(message)
            elif update_type == "user_aware":
                # New user-aware update that checks satisfaction
                message = data.get("message", "")
                user_satisfaction = self._detect_user_satisfaction(message)
                
                # Update emotion normally
                result = self.update_emotion_with_global_weight(message)
                
                # Check for releases with user satisfaction awareness
                if result.get("release_event"):
                    # User is satisfied, allow normal release
                    if user_satisfaction:
                        result["release_event"] = self._trigger_sexual_release() if self.current_level <= 0.1 else self._trigger_achievement_release()
                    else:
                        # User not satisfied, maintain current state
                        result["release_event"] = None
                        result["user_warning"] = "Maintaining current emotional state - user satisfaction not detected"
                
                result["user_satisfaction_detected"] = user_satisfaction
            else:
                return {"error": f"Unknown update type: {update_type}", "status": "failed"}

            return {"status": "success", "result": result}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in emotion update: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_emotion_query(self, data):
        """Handle emotion query operations"""
        try:
            query_type = data.get("type")

            if query_type == "current_state":
                result = {
                    "current_level": self.current_level,
                    "current_state": self.get_current_state().value,
                    "state_description": self.get_state_description(),
                }
            elif query_type == "summary":
                result = self.get_emotional_summary()
            elif query_type == "release_history":
                limit = data.get("limit", 10)
                result = self.get_release_history(limit)
            else:
                result = {"error": f"Unknown query type: {query_type}"}

            return {"result": result, "status": "success"}
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error handling emotion query: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_emotion_reset(self, data):
        """Handle emotion reset operations"""
        try:
            reset_type = data.get("type", "balance")

            if reset_type == "balance":
                self.current_level = 0.5
            elif reset_type == "lust":
                self.current_level = 0.0
            elif reset_type == "work":
                self.current_level = 1.0
            elif reset_type == "custom":
                custom_level = data.get("level", 0.5)
                self.current_level = max(0.0, min(1.0, float(custom_level)))
            else:
                return {
                    "error": f"Unknown reset type: {reset_type}",
                    "status": "failed",
                }

            result = self.get_emotional_summary()
            return {"result": result, "status": "success"}
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error handling emotion reset: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_emotion_config(self, data):
        """Handle emotion configuration operations"""
        try:
            config_type = data.get("type")

            if config_type == "update_thresholds":
                new_thresholds = data.get("thresholds", {})
                for key, value in new_thresholds.items():
                    if key in self.release_thresholds:
                        self.release_thresholds[key] = float(value)
                result = {"thresholds": self.release_thresholds}
            elif config_type == "update_weights":
                weight_type = data.get("weight_type")
                new_weights = data.get("weights", {})
                if weight_type == "lust":
                    self.lust_weights.update(new_weights)
                    result = {"lust_weights": self.lust_weights}
                elif weight_type == "work":
                    self.work_weights.update(new_weights)
                    result = {"work_weights": self.work_weights}
                else:
                    result = {"error": f"Unknown weight type: {weight_type}"}
            else:
                result = {"error": f"Unknown config type: {config_type}"}

            return {"result": result, "status": "success"}
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error handling emotion config: {e}")
            return {"error": str(e), "status": "failed"}

    def _handle_emotion_history(self, data):
        """Handle emotion history operations"""
        try:
            history_type = data.get("type")

            if history_type == "save_state":
                filepath = data.get("filepath", "emotional_state.json")
                self.save_state(filepath)
                result = {"message": f"State saved to {filepath}"}
            elif history_type == "load_state":
                filepath = data.get("filepath", "emotional_state.json")
                self.load_state(filepath)
                result = self.get_emotional_summary()
            elif history_type == "get_releases":
                limit = data.get("limit", 10)
                result = self.get_release_history(limit)
            else:
                result = {"error": f"Unknown history type: {history_type}"}

            return {"result": result, "status": "success"}
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error handling emotion history: {e}")
            return {"error": str(e), "status": "failed"}


def test_emotional_meter():
    """Test the enhanced emotional meter system"""
    print("🧠 Testing Enhanced Emotional Meter System")
    print("=" * 50)

    meter = EnhancedEmotionalMeter()

    # Test lust build-up
    print("\n🔥 Testing Lust Build-up:")
    for i in range(5):
        result = meter.update_emotion("lustful", 0.2)
        print(f"Level: {result['new_level']:.1f} - {result['description']}")
        if result["release_event"]:
            print(f"💥 RELEASE: {result['release_event'].release_type.value}")

    # Test work build-up
    print("\n💼 Testing Work Build-up:")
    for i in range(5):
        result = meter.update_emotion("work", 0.2)
        print(f"Level: {result['new_level']:.1f} - {result['description']}")
        if result["release_event"]:
            print(f"💥 RELEASE: {result['release_event'].release_type.value}")

    # Test natural return
    print("\n⚖️ Testing Natural Return to Balance:")
    meter.current_level = 0.8
    for i in range(10):
        result = meter.update_emotion("neutral")
        print(f"Level: {result['new_level']:.1f} - {result['description']}")
        if abs(result["new_level"] - 0.5) < 0.01:
            print("✅ Reached balance!")
            break

    # Show summary
    print("\n📊 Emotional Summary:")
    summary = meter.get_emotional_summary()
    for key, value in summary.items():
        if key != "last_release":  # Skip complex object
            print(f"{key}: {value}")


if __name__ == "__main__":
    test_emotional_meter()
