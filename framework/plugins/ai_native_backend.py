#!/usr/bin/env python3
"""
AI Native Backend System
Allows Luna to create her own optimized data structures and learning systems
"""

import os
import sys
import time
import sqlite3
import pickle
import threading
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from queue import Queue
import traceback

# Add framework directory to path for imports
framework_dir = Path(__file__).parent.parent
sys.path.insert(0, str(framework_dir))

from queue_manager import QueueProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AIOptimizedData:
    """AI-optimized data structure for efficient processing"""

    data_hash: str
    data_type: str
    content: bytes  # Binary format for AI processing
    metadata: Dict[str, Any]
    created_at: float
    last_accessed: float
    access_count: int


class AINativeBackend(QueueProcessor):
    """AI-native backend system for Luna's optimized data management"""

    def __init__(self, data_dir: str = "data/ai_native"):
        super().__init__("ai_native_backend")
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # AI-optimized storage
        self.emotional_cache = {}
        self.user_profiles = {}
        self.conversation_history = {}
        self.learning_patterns = {}

        # Queue system for concurrent processing
        self.processing_queue = Queue()
        self.typing_status = {}

        # Initialize AI-optimized database
        self._init_ai_database()

    def _init_ai_database(self):
        """Initialize AI-optimized database structure"""
        self.db_path = self.data_dir / "ai_native.db"

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS emotional_states (
                    user_id TEXT PRIMARY KEY,
                    state_data BLOB,
                    last_updated REAL,
                    access_count INTEGER DEFAULT 0
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation_patterns (
                    pattern_hash TEXT PRIMARY KEY,
                    pattern_data BLOB,
                    frequency INTEGER DEFAULT 1,
                    last_used REAL
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS learning_models (
                    model_name TEXT PRIMARY KEY,
                    model_data BLOB,
                    accuracy REAL,
                    last_trained REAL
                )
            """
            )

            conn.commit()

    def create_ai_optimized_data(self, data: Any, data_type: str) -> AIOptimizedData:
        """Create AI-optimized data structure"""
        try:
            # Convert to binary format optimized for AI processing
            if isinstance(data, dict):
                content = pickle.dumps(data, protocol=4)  # Optimized for AI
            else:
                content = pickle.dumps(data, protocol=4)

            data_hash = hashlib.sha256(content).hexdigest()

            return AIOptimizedData(
                data_hash=data_hash,
                data_type=data_type,
                content=content,
                metadata={
                    "size": len(content),
                    "compression_ratio": 1.0,  # Can be optimized later
                    "ai_optimized": True,
                },
                created_at=time.time(),
                last_accessed=time.time(),
                access_count=1,
            )
        except Exception as e:
            logger.error(f"Error creating AI optimized data: {e}")
            logger.error(f"Data type: {type(data)}, Data type string: {data_type}")
            import traceback

            logger.error(f"Create AI data traceback: {traceback.format_exc()}")
            # Return a minimal valid structure to prevent crashes
            return AIOptimizedData(
                data_hash="error_hash",
                data_type=data_type,
                content=b"",
                metadata={"error": str(e)},
                created_at=time.time(),
                last_accessed=time.time(),
                access_count=0,
            )

    def store_emotional_state(self, user_id: str, emotional_state: Dict[str, Any]):
        """Store emotional state in AI-optimized format"""
        try:
            ai_data = self.create_ai_optimized_data(emotional_state, "emotional_state")

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO emotional_states 
                    (user_id, state_data, last_updated, access_count)
                    VALUES (?, ?, ?, ?)
                """,
                    (user_id, ai_data.content, time.time(), ai_data.access_count),
                )
                conn.commit()

            # Cache for quick access
            self.emotional_cache[user_id] = ai_data

        except Exception as e:
            logger.error(f"Error storing emotional state: {e}")
            import traceback

            logger.error(f"Store emotional state traceback: {traceback.format_exc()}")

    def get_emotional_state(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve emotional state in AI-optimized format"""
        try:
            # Check cache first
            if user_id in self.emotional_cache:
                cached_data = self.emotional_cache[user_id]
                cached_data.last_accessed = time.time()
                cached_data.access_count += 1
                return pickle.loads(cached_data.content)

            # Query database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT state_data FROM emotional_states 
                    WHERE user_id = ?
                """,
                    (user_id,),
                )

                result = cursor.fetchone()
                if result:
                    emotional_state = pickle.loads(result[0])
                    # Update cache
                    ai_data = self.create_ai_optimized_data(
                        emotional_state, "emotional_state"
                    )
                    self.emotional_cache[user_id] = ai_data
                    return emotional_state

            return None

        except Exception as e:
            logger.error(f"Error getting emotional state: {e}")
            import traceback

            logger.error(f"Get emotional state traceback: {traceback.format_exc()}")
            return None

    def store_conversation_pattern(self, pattern: Dict[str, Any]):
        """Store conversation pattern for learning"""
        try:
            pattern_hash = hashlib.sha256(
                json.dumps(pattern, sort_keys=True).encode()
            ).hexdigest()
            ai_data = self.create_ai_optimized_data(pattern, "conversation_pattern")

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO conversation_patterns 
                    (pattern_hash, pattern_data, frequency, last_used)
                    VALUES (?, ?, ?, ?)
                """,
                    (pattern_hash, ai_data.content, 1, time.time()),
                )
                conn.commit()

        except Exception as e:
            logger.error(f"Error storing conversation pattern: {e}")
            import traceback

            logger.error(
                f"Store conversation pattern traceback: {traceback.format_exc()}"
            )

    def learn_from_interaction(
        self,
        user_id: str,
        message: str,
        response: str,
        emotional_context: Dict[str, Any],
    ):
        """Learn from user interaction and improve responses"""
        try:
            pattern = {
                "user_id": user_id,
                "message": message,
                "response": response,
                "emotional_context": emotional_context,
                "timestamp": time.time(),
            }

            # Store pattern for learning
            self.store_conversation_pattern(pattern)

            # Add to processing queue for background learning
            self.processing_queue.put({"type": "learning", "data": pattern})

        except Exception as e:
            logger.error(f"Error learning from interaction: {e}")
            import traceback

            logger.error(f"Learn from interaction traceback: {traceback.format_exc()}")

    def _process_item(self, item):
        """Process a queue item from the new queue system"""
        try:
            if isinstance(item.data, dict):
                if item.data.get("type") == "learning":
                    self._process_learning_item(item.data.get("data", {}))
                elif item.data.get("type") == "typing_status":
                    self._update_typing_status(item.data.get("data", {}))
                elif item.data.get("type") == "emotional_state":
                    self.store_emotional_state(
                        item.data.get("user_id", "unknown"),
                        item.data.get("emotional_state", {}),
                    )
                elif item.data.get("type") == "conversation_pattern":
                    self.store_conversation_pattern(item.data.get("pattern", {}))
                else:
                    # Default processing - just pass through
                    super()._process_item(item)
            else:
                # Default processing for non-dict data
                super()._process_item(item)

        except Exception as e:
            logger.error(f"Error processing item {item.id} in {self.system_name}: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            queue_manager.put_to_error_queue(self.system_name, item, str(e))

    def _process_learning_item(self, data: Dict[str, Any]):
        """Process learning data to improve AI responses"""
        try:
            # Validate required fields
            if not isinstance(data, dict):
                logger.error(f"Invalid data type for learning item: {type(data)}")
                return

            if (
                "message" not in data
                or "response" not in data
                or "emotional_context" not in data
            ):
                logger.error(
                    f"Missing required fields in learning data: {list(data.keys())}"
                )
                return

            # Analyze conversation patterns
            message_length = len(data["message"])
            response_length = len(data["response"])
            emotional_intensity = data["emotional_context"].get("intensity", 0.5)

            # Store learning insights
            learning_insight = {
                "pattern_type": "conversation",
                "message_length": message_length,
                "response_length": response_length,
                "emotional_intensity": emotional_intensity,
                "timestamp": time.time(),
            }

            # Store in AI-optimized format
            ai_data = self.create_ai_optimized_data(
                learning_insight, "learning_insight"
            )

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO learning_models 
                    (model_name, model_data, accuracy, last_trained)
                    VALUES (?, ?, ?, ?)
                """,
                    (f"pattern_{time.time()}", ai_data.content, 0.8, time.time()),
                )
                conn.commit()

        except Exception as e:
            logger.error(f"Error processing learning item: {e}")
            import traceback

            logger.error(f"Learning item traceback: {traceback.format_exc()}")

    def _update_typing_status(self, data: Dict[str, Any]):
        """Update typing status for Discord integration"""
        try:
            # Validate required fields
            if not isinstance(data, dict):
                logger.error(f"Invalid data type for typing status: {type(data)}")
                return

            if "user_id" not in data or "is_typing" not in data:
                logger.error(
                    f"Missing required fields in typing status data: {list(data.keys())}"
                )
                return

            user_id = data["user_id"]
            is_typing = data["is_typing"]

            self.typing_status[user_id] = {
                "is_typing": is_typing,
                "timestamp": time.time(),
            }

        except Exception as e:
            logger.error(f"Error updating typing status: {e}")
            import traceback

            logger.error(f"Typing status traceback: {traceback.format_exc()}")

    def get_typing_status(self, user_id: str) -> bool:
        """Get current typing status for user"""
        if user_id in self.typing_status:
            status = self.typing_status[user_id]
            # Auto-clear typing status after 5 seconds
            if time.time() - status["timestamp"] > 5:
                del self.typing_status[user_id]
                return False
            return status["is_typing"]
        return False

    def set_typing_status(self, user_id: str, is_typing: bool):
        """Set typing status for user"""
        try:
            self.processing_queue.put(
                {
                    "type": "typing_status",
                    "data": {"user_id": user_id, "is_typing": is_typing},
                }
            )
        except Exception as e:
            logger.error(f"Error setting typing status: {e}")
            import traceback

            logger.error(f"Set typing status traceback: {traceback.format_exc()}")

    def create_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Create AI-optimized user profile"""
        try:
            profile = {
                "user_id": user_id,
                "emotional_history": [],
                "conversation_patterns": [],
                "preferences": {},
                "created_at": time.time(),
                "last_interaction": time.time(),
            }

            # Store in AI-optimized format
            ai_data = self.create_ai_optimized_data(profile, "user_profile")

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO emotional_states 
                    (user_id, state_data, last_updated, access_count)
                    VALUES (?, ?, ?, ?)
                """,
                    (user_id, ai_data.content, time.time(), 1),
                )
                conn.commit()

            self.user_profiles[user_id] = ai_data
            return profile

        except Exception as e:
            logger.error(f"Error creating user profile: {e}")
            import traceback

            logger.error(f"Create user profile traceback: {traceback.format_exc()}")
            # Return a minimal profile to prevent crashes
            return {
                "user_id": user_id,
                "emotional_history": [],
                "conversation_patterns": [],
                "preferences": {},
                "created_at": time.time(),
                "last_interaction": time.time(),
                "error": str(e),
            }

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get AI-optimized user profile"""
        try:
            if user_id in self.user_profiles:
                return pickle.loads(self.user_profiles[user_id].content)

            # Try to load from database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT state_data FROM emotional_states 
                    WHERE user_id = ?
                """,
                    (user_id,),
                )

                result = cursor.fetchone()
                if result:
                    profile = pickle.loads(result[0])
                    ai_data = self.create_ai_optimized_data(profile, "user_profile")
                    self.user_profiles[user_id] = ai_data
                    return profile

            return None

        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            import traceback

            logger.error(f"Get user profile traceback: {traceback.format_exc()}")
            return None

    def optimize_for_ai(self, data: Any) -> bytes:
        """Optimize data for AI processing"""
        # Convert to numpy arrays for efficient AI processing
        if isinstance(data, dict):
            # Convert dict to optimized format
            optimized = {}
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    optimized[key] = np.array([value], dtype=np.float32)
                elif isinstance(value, list):
                    optimized[key] = np.array(value, dtype=np.float32)
                else:
                    optimized[key] = value
            return pickle.dumps(optimized, protocol=4)
        else:
            return pickle.dumps(data, protocol=4)

    def get_system_stats(self) -> Dict[str, Any]:
        """Get AI-native backend statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                emotional_count = conn.execute(
                    "SELECT COUNT(*) FROM emotional_states"
                ).fetchone()[0]
                pattern_count = conn.execute(
                    "SELECT COUNT(*) FROM conversation_patterns"
                ).fetchone()[0]
                model_count = conn.execute(
                    "SELECT COUNT(*) FROM learning_models"
                ).fetchone()[0]

            return {
                "emotional_states": emotional_count,
                "conversation_patterns": pattern_count,
                "learning_models": model_count,
                "cache_size": len(self.emotional_cache),
                "queue_size": self.processing_queue.qsize(),
                "typing_users": len(self.typing_status),
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            import traceback

            logger.error(f"Get system stats traceback: {traceback.format_exc()}")
            return {
                "emotional_states": 0,
                "conversation_patterns": 0,
                "learning_models": 0,
                "cache_size": len(self.emotional_cache),
                "queue_size": self.processing_queue.qsize(),
                "typing_users": len(self.typing_status),
                "error": str(e),
            }

    def clear_queue(self):
        """Clear the processing queue to prevent memory issues"""
        try:
            while not self.processing_queue.empty():
                self.processing_queue.get_nowait()
            logger.info("Processing queue cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing queue: {e}")

    def reset_system(self):
        """Reset the AI-native backend system"""
        try:
            # Clear caches
            self.emotional_cache.clear()
            self.user_profiles.clear()
            self.typing_status.clear()

            # Clear queue
            self.clear_queue()

            logger.info("AI-native backend system reset successfully")
        except Exception as e:
            logger.error(f"Error resetting system: {e}")
            import traceback

            logger.error(f"Reset system traceback: {traceback.format_exc()}")


# Initialize AI-native backend
ai_backend = AINativeBackend()
