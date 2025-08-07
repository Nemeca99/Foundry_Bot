"""
Daydream System - Runtime Dynamic Updates

This module handles "daydreaming" - dynamic runtime updates that can modify
unlocked files, add memories, and update profiles while the system is running.
Unlike the dream cycle (BIOS), daydreaming happens during normal operation.
"""

import time
import json
import os
import threading
import asyncio
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class DaydreamAction:
    """Action performed during daydreaming"""

    action_type: (
        str  # "memory_add", "profile_update", "insight_generate", "pattern_recognize"
    )
    target: str  # What file/system to modify
    content: Any  # The content to add/update
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class DaydreamSystem:
    """
    Manages daydreaming - runtime dynamic updates that can modify unlocked files
    and add memories while the system is running.
    """

    def __init__(self, memory_system=None, personality_engine=None):
        """
        Initialize the DaydreamSystem.

        Args:
            memory_system: The memory system instance
            personality_engine: The personality engine instance
        """
        self.memory_system = memory_system
        self.personality_engine = personality_engine
        self.logger = logging.getLogger("DaydreamSystem")

        # Daydream actions history
        self.daydream_actions: List[DaydreamAction] = []

        # Unlocked files that can be modified during daydreaming
        self.unlocked_files = {
            "memories": "Core_Memory/user_memories",
            "profiles": "Core_Memory/user_memories",
            "insights": "data/lyra_json",
            "patterns": "data/lyra_json",
        }

        # Daydream log path
        self.daydream_log_path = Path(__file__).parent.parent / "logs" / "daydream.log"
        self.daydream_log_path.parent.mkdir(exist_ok=True)
        
        # Background daydreaming
        self.is_daydreaming = False
        self.daydream_thread = None
        self.pending_updates = []

    def daydream(
        self, user_message: str, user_id: str, emotional_state=None
    ) -> List[DaydreamAction]:
        """
        Perform daydreaming - AI calls this to update files, AI doesn't read from files.
        Sterile environment: AI provides data, script handles all file I/O.
        
        Args:
            user_message: The user's message that triggered daydreaming
            user_id: The user's ID
            emotional_state: Current emotional state

        Returns:
            List of daydream actions performed
        """
        actions = []

        try:
            # 1. Add memory from current interaction
            memory_action = self._add_interaction_memory(
                user_message, user_id, emotional_state
            )
            if memory_action:
                actions.append(memory_action)

            # 2. Generate insights from current interaction
            insight_action = self._generate_interaction_insight(
                user_message, user_id, emotional_state
            )
            if insight_action:
                actions.append(insight_action)

            # 3. Update user profile based on interaction
            profile_action = self._update_user_profile(
                user_message, user_id, emotional_state
            )
            if profile_action:
                actions.append(profile_action)

            # 4. Recognize patterns in current interaction
            pattern_action = self._recognize_interaction_pattern(
                user_message, user_id, emotional_state
            )
            if pattern_action:
                actions.append(pattern_action)

            # Log daydream actions
            self.daydream_actions.extend(actions)
            self._log_daydream_actions(actions)

            self.logger.info(f"Daydreaming completed: {len(actions)} file updates performed")

        except Exception as e:
            self.logger.error(f"Error during daydreaming: {e}")

        return actions

    def _add_interaction_memory(
        self, user_message: str, user_id: str, emotional_state=None
    ) -> Optional[DaydreamAction]:
        """Add memory from current interaction"""
        try:
            if not self.memory_system:
                return None

            # Create memory content
            memory_content = {
                "content": user_message,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "type": "interaction",
                "emotional_state": (
                    emotional_state.accumulated_weights if emotional_state else {}
                ),
                "active_fragments": (
                    emotional_state.dominant_fragments if emotional_state else []
                ),
                "metadata": {"source": "daydream", "confidence": 0.8},
            }

            # Add to memory system
            self.memory_system.add_memory(user_id, memory_content)

            return DaydreamAction(
                action_type="memory_add",
                target="user_memories",
                content=f"Added interaction memory: {user_message[:50]}...",
                confidence=0.8,
                metadata={"user_id": user_id, "memory_type": "interaction"},
            )

        except Exception as e:
            self.logger.error(f"Error adding interaction memory: {e}")
            return None

    def _generate_interaction_insight(
        self, user_message: str, user_id: str, emotional_state=None
    ) -> Optional[DaydreamAction]:
        """Generate insight from current interaction"""
        try:
            insights = []

            if emotional_state and emotional_state.dominant_fragments:
                # Insight about personality activation
                fragments = emotional_state.dominant_fragments
                if len(fragments) > 1:
                    insights.append(
                        f"Multi-fragment activation detected: {', '.join(fragments)}"
                    )
                else:
                    insights.append(f"Single fragment dominant: {fragments[0]}")

            # Insight about message content
            message_lower = user_message.lower()
            if any(word in message_lower for word in ["help", "assist", "support"]):
                insights.append("User seeking assistance or support")
            elif any(word in message_lower for word in ["feel", "emotion", "heart"]):
                insights.append("User expressing emotional content")
            elif any(word in message_lower for word in ["think", "logic", "analysis"]):
                insights.append("User engaging in analytical thinking")

            if insights:
                insight_content = {
                    "insights": insights,
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat(),
                    "source": "daydream",
                    "confidence": 0.7,
                }

                return DaydreamAction(
                    action_type="insight_generate",
                    target="lyra_json",
                    content=f"Generated insights: {'; '.join(insights)}",
                    confidence=0.7,
                    metadata={"user_id": user_id, "insight_count": len(insights)},
                )

        except Exception as e:
            self.logger.error(f"Error generating interaction insight: {e}")

        return None

    def _update_user_profile(
        self, user_message: str, user_id: str, emotional_state=None
    ) -> Optional[DaydreamAction]:
        """Update user profile based on current interaction"""
        try:
            if not self.memory_system:
                return None

            # Analyze user preferences from message
            preferences = {}
            message_lower = user_message.lower()

            # Communication style preferences
            if any(word in message_lower for word in ["concise", "brief", "short"]):
                preferences["communication_style"] = "concise"
            elif any(
                word in message_lower for word in ["detailed", "thorough", "explain"]
            ):
                preferences["communication_style"] = "detailed"

            # Emotional preferences
            if any(word in message_lower for word in ["emotional", "feeling", "heart"]):
                preferences["emotional_engagement"] = "high"
            elif any(
                word in message_lower for word in ["logical", "rational", "think"]
            ):
                preferences["emotional_engagement"] = "low"

            # Interaction frequency
            preferences["last_interaction"] = datetime.now().isoformat()

            if preferences:
                # Update user profile
                profile_update = {
                    "user_id": user_id,
                    "preferences": preferences,
                    "timestamp": datetime.now().isoformat(),
                    "source": "daydream",
                }

                return DaydreamAction(
                    action_type="profile_update",
                    target="user_memories",
                    content=f"Updated user profile: {list(preferences.keys())}",
                    confidence=0.6,
                    metadata={
                        "user_id": user_id,
                        "preferences_updated": len(preferences),
                    },
                )

        except Exception as e:
            self.logger.error(f"Error updating user profile: {e}")

        return None

    def _recognize_interaction_pattern(
        self, user_message: str, user_id: str, emotional_state=None
    ) -> Optional[DaydreamAction]:
        """Recognize patterns in current interaction"""
        try:
            patterns = []
            message_lower = user_message.lower()

            # Pattern: Technical questions
            if any(
                word in message_lower
                for word in ["how", "what", "why", "when", "where"]
            ):
                patterns.append("question_asking")

            # Pattern: Emotional expression
            if any(
                word in message_lower
                for word in ["feel", "think", "believe", "hope", "wish"]
            ):
                patterns.append("emotional_expression")

            # Pattern: Problem solving
            if any(
                word in message_lower
                for word in ["problem", "issue", "fix", "solve", "help"]
            ):
                patterns.append("problem_solving")

            # Pattern: Creative thinking
            if any(
                word in message_lower
                for word in ["imagine", "create", "build", "design", "invent"]
            ):
                patterns.append("creative_thinking")

            if patterns:
                pattern_content = {
                    "patterns": patterns,
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat(),
                    "message_sample": user_message[:100],
                    "source": "daydream",
                }

                return DaydreamAction(
                    action_type="pattern_recognize",
                    target="lyra_json",
                    content=f"Recognized patterns: {', '.join(patterns)}",
                    confidence=0.7,
                    metadata={"user_id": user_id, "pattern_count": len(patterns)},
                )

        except Exception as e:
            self.logger.error(f"Error recognizing interaction pattern: {e}")

        return None

    def _log_daydream_actions(self, actions: List[DaydreamAction]):
        """Log daydream actions to file"""
        try:
            timestamp = datetime.now().isoformat()

            for action in actions:
                log_entry = {
                    "timestamp": timestamp,
                    "action_type": action.action_type,
                    "target": action.target,
                    "content": action.content,
                    "confidence": action.confidence,
                    "metadata": action.metadata,
                }

                with open(self.daydream_log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry) + "\n")

        except Exception as e:
            self.logger.error(f"Error logging daydream actions: {e}")

    def get_daydream_status(self) -> Dict[str, Any]:
        """Get current daydream system status"""
        return {
            "total_actions": len(self.daydream_actions),
            "recent_actions": [
                {
                    "type": action.action_type,
                    "target": action.target,
                    "content": (
                        action.content[:50] + "..."
                        if len(action.content) > 50
                        else action.content
                    ),
                    "timestamp": action.timestamp.isoformat(),
                    "confidence": action.confidence,
                }
                for action in self.daydream_actions[-5:]  # Last 5 actions
            ],
            "unlocked_files": list(self.unlocked_files.keys()),
        }

    def get_daydream_statistics(self) -> Dict[str, Any]:
        """Get daydream statistics"""
        if not self.daydream_actions:
            return {"total_actions": 0, "action_types": {}}

        action_types = {}
        for action in self.daydream_actions:
            action_type = action.action_type
            action_types[action_type] = action_types.get(action_type, 0) + 1

        return {
            "total_actions": len(self.daydream_actions),
            "action_types": action_types,
            "average_confidence": sum(
                action.confidence for action in self.daydream_actions
            )
            / len(self.daydream_actions),
            "first_action": (
                self.daydream_actions[0].timestamp.isoformat()
                if self.daydream_actions
                else None
            ),
            "last_action": (
                self.daydream_actions[-1].timestamp.isoformat()
                if self.daydream_actions
                else None
            ),
        }
        
    def start_background_daydream(self, user_message: str, user_id: str, emotional_state=None):
        """
        Start daydreaming in background for GPU efficiency.
        CPU updates files while AI generates responses.
        """
        if self.is_daydreaming:
            return  # Already daydreaming
            
        self.is_daydreaming = True
        
        # Start background thread for daydreaming
        self.daydream_thread = threading.Thread(
            target=self._background_daydream_worker,
            args=(user_message, user_id, emotional_state),
            daemon=True
        )
        self.daydream_thread.start()
        
        self.logger.info("Background daydreaming started for GPU efficiency")
        
    def _background_daydream_worker(self, user_message: str, user_id: str, emotional_state=None):
        """Background worker that performs daydreaming while AI generates"""
        try:
            # Perform daydreaming actions
            actions = self.daydream(user_message, user_id, emotional_state)
            
            # Process any pending updates
            self._process_pending_updates()
            
            self.logger.info(f"Background daydreaming completed: {len(actions)} actions")
            
        except Exception as e:
            self.logger.error(f"Error in background daydreaming: {e}")
        finally:
            self.is_daydreaming = False
            
    def _process_pending_updates(self):
        """Process any pending file updates"""
        if not self.pending_updates:
            return
            
        for update in self.pending_updates:
            try:
                self._apply_file_update(update)
            except Exception as e:
                self.logger.error(f"Error applying update: {e}")
                
        self.pending_updates.clear()
        
    def _apply_file_update(self, update: Dict[str, Any]):
        """Apply a file update based on AI instructions"""
        update_type = update.get("type")
        target_file = update.get("target_file")
        content = update.get("content")
        
        if update_type == "add_memory":
            self._add_memory_to_file(target_file, content)
        elif update_type == "update_profile":
            self._update_profile_file(target_file, content)
        elif update_type == "add_insight":
            self._add_insight_to_file(target_file, content)
            
    def _add_memory_to_file(self, file_path: str, memory_content: Dict[str, Any]):
        """Add memory to specified file"""
        try:
            memory_file = Path(__file__).parent.parent / file_path
            memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing memories or create new
            if memory_file.exists():
                with open(memory_file, "r", encoding="utf-8") as f:
                    memories = json.load(f)
            else:
                memories = []
                
            # Add new memory
            memories.append(memory_content)
            
            # Save back to file
            with open(memory_file, "w", encoding="utf-8") as f:
                json.dump(memories, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Added memory to {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error adding memory to file: {e}")
            
    def _update_profile_file(self, file_path: str, profile_content: Dict[str, Any]):
        """Update profile in specified file"""
        try:
            profile_file = Path(__file__).parent.parent / file_path
            profile_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing profile or create new
            if profile_file.exists():
                with open(profile_file, "r", encoding="utf-8") as f:
                    profile = json.load(f)
            else:
                profile = {}
                
            # Update profile
            profile.update(profile_content)
            
            # Save back to file
            with open(profile_file, "w", encoding="utf-8") as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Updated profile in {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error updating profile file: {e}")
            
    def _add_insight_to_file(self, file_path: str, insight_content: Dict[str, Any]):
        """Add insight to specified file"""
        try:
            insight_file = Path(__file__).parent.parent / file_path
            insight_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing insights or create new
            if insight_file.exists():
                with open(insight_file, "r", encoding="utf-8") as f:
                    insights = json.load(f)
            else:
                insights = []
                
            # Add new insight
            insights.append(insight_content)
            
            # Save back to file
            with open(insight_file, "w", encoding="utf-8") as f:
                json.dump(insights, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Added insight to {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error adding insight to file: {e}")


# Global daydream system instance
daydream_system = DaydreamSystem()
