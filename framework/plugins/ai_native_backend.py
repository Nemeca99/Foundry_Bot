#!/usr/bin/env python3
"""
AI Native Backend System
Allows Luna to create her own optimized data structures and learning systems
"""

import json
import pickle
import sqlite3
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import hashlib
import time
import threading
from queue import Queue
import logging

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


class AINativeBackend:
    """AI-native backend system for Luna's optimized data management"""
    
    def __init__(self, data_dir: str = "data/ai_native"):
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
        
        # Threading for concurrent operations
        self.processing_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.processing_thread.start()
        
        # Initialize AI-optimized database
        self._init_ai_database()
    
    def _init_ai_database(self):
        """Initialize AI-optimized database structure"""
        self.db_path = self.data_dir / "ai_native.db"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS emotional_states (
                    user_id TEXT PRIMARY KEY,
                    state_data BLOB,
                    last_updated REAL,
                    access_count INTEGER DEFAULT 0
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_patterns (
                    pattern_hash TEXT PRIMARY KEY,
                    pattern_data BLOB,
                    frequency INTEGER DEFAULT 1,
                    last_used REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learning_models (
                    model_name TEXT PRIMARY KEY,
                    model_data BLOB,
                    accuracy REAL,
                    last_trained REAL
                )
            """)
            
            conn.commit()
    
    def create_ai_optimized_data(self, data: Any, data_type: str) -> AIOptimizedData:
        """Create AI-optimized data structure"""
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
                "ai_optimized": True
            },
            created_at=time.time(),
            last_accessed=time.time(),
            access_count=1
        )
    
    def store_emotional_state(self, user_id: str, emotional_state: Dict[str, Any]):
        """Store emotional state in AI-optimized format"""
        ai_data = self.create_ai_optimized_data(emotional_state, "emotional_state")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO emotional_states 
                (user_id, state_data, last_updated, access_count)
                VALUES (?, ?, ?, ?)
            """, (user_id, ai_data.content, time.time(), ai_data.access_count))
            conn.commit()
        
        # Cache for quick access
        self.emotional_cache[user_id] = ai_data
    
    def get_emotional_state(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve emotional state in AI-optimized format"""
        # Check cache first
        if user_id in self.emotional_cache:
            cached_data = self.emotional_cache[user_id]
            cached_data.last_accessed = time.time()
            cached_data.access_count += 1
            return pickle.loads(cached_data.content)
        
        # Query database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT state_data FROM emotional_states 
                WHERE user_id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            if result:
                emotional_state = pickle.loads(result[0])
                # Update cache
                ai_data = self.create_ai_optimized_data(emotional_state, "emotional_state")
                self.emotional_cache[user_id] = ai_data
                return emotional_state
        
        return None
    
    def store_conversation_pattern(self, pattern: Dict[str, Any]):
        """Store conversation pattern for learning"""
        pattern_hash = hashlib.sha256(json.dumps(pattern, sort_keys=True).encode()).hexdigest()
        ai_data = self.create_ai_optimized_data(pattern, "conversation_pattern")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO conversation_patterns 
                (pattern_hash, pattern_data, frequency, last_used)
                VALUES (?, ?, ?, ?)
            """, (pattern_hash, ai_data.content, 1, time.time()))
            conn.commit()
    
    def learn_from_interaction(self, user_id: str, message: str, response: str, emotional_context: Dict[str, Any]):
        """Learn from user interaction and improve responses"""
        pattern = {
            "user_id": user_id,
            "message": message,
            "response": response,
            "emotional_context": emotional_context,
            "timestamp": time.time()
        }
        
        # Store pattern for learning
        self.store_conversation_pattern(pattern)
        
        # Add to processing queue for background learning
        self.processing_queue.put({
            "type": "learning",
            "data": pattern
        })
    
    def _process_queue(self):
        """Background processing for AI learning and optimization"""
        while True:
            try:
                item = self.processing_queue.get(timeout=1)
                
                if item["type"] == "learning":
                    self._process_learning_item(item["data"])
                elif item["type"] == "typing_status":
                    self._update_typing_status(item["data"])
                
            except Exception as e:
                logger.error(f"Error processing queue item: {e}")
    
    def _process_learning_item(self, data: Dict[str, Any]):
        """Process learning data to improve AI responses"""
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
            "timestamp": time.time()
        }
        
        # Store in AI-optimized format
        ai_data = self.create_ai_optimized_data(learning_insight, "learning_insight")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO learning_models 
                (model_name, model_data, accuracy, last_trained)
                VALUES (?, ?, ?, ?)
            """, (f"pattern_{time.time()}", ai_data.content, 0.8, time.time()))
            conn.commit()
    
    def _update_typing_status(self, data: Dict[str, Any]):
        """Update typing status for Discord integration"""
        user_id = data["user_id"]
        is_typing = data["is_typing"]
        
        self.typing_status[user_id] = {
            "is_typing": is_typing,
            "timestamp": time.time()
        }
    
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
        self.processing_queue.put({
            "type": "typing_status",
            "data": {
                "user_id": user_id,
                "is_typing": is_typing
            }
        })
    
    def create_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Create AI-optimized user profile"""
        profile = {
            "user_id": user_id,
            "emotional_history": [],
            "conversation_patterns": [],
            "preferences": {},
            "created_at": time.time(),
            "last_interaction": time.time()
        }
        
        # Store in AI-optimized format
        ai_data = self.create_ai_optimized_data(profile, "user_profile")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO emotional_states 
                (user_id, state_data, last_updated, access_count)
                VALUES (?, ?, ?, ?)
            """, (user_id, ai_data.content, time.time(), 1))
            conn.commit()
        
        self.user_profiles[user_id] = ai_data
        return profile
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get AI-optimized user profile"""
        if user_id in self.user_profiles:
            return pickle.loads(self.user_profiles[user_id].content)
        
        # Try to load from database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT state_data FROM emotional_states 
                WHERE user_id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            if result:
                profile = pickle.loads(result[0])
                ai_data = self.create_ai_optimized_data(profile, "user_profile")
                self.user_profiles[user_id] = ai_data
                return profile
        
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
        with sqlite3.connect(self.db_path) as conn:
            emotional_count = conn.execute("SELECT COUNT(*) FROM emotional_states").fetchone()[0]
            pattern_count = conn.execute("SELECT COUNT(*) FROM conversation_patterns").fetchone()[0]
            model_count = conn.execute("SELECT COUNT(*) FROM learning_models").fetchone()[0]
        
        return {
            "emotional_states": emotional_count,
            "conversation_patterns": pattern_count,
            "learning_models": model_count,
            "cache_size": len(self.emotional_cache),
            "queue_size": self.processing_queue.qsize(),
            "typing_users": len(self.typing_status)
        }


# Initialize AI-native backend
ai_backend = AINativeBackend() 