#!/usr/bin/env python3
"""
Consolidated Memory System for Aether_Project
Merges complex SQLite-based memory system with simple in-memory system
Provides both advanced and simple memory capabilities
"""

import os
import json
import logging
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sqlite3
from collections import defaultdict
import pickle
import asyncio


class ConsolidatedMemorySystem:
    """
    Consolidated memory system that provides both simple and advanced memory capabilities.
    Combines SQLite persistence with in-memory caching and simple mode for testing.
    """

    def __init__(self, config=None, simple_mode=False):
        self.config = config
        self.simple_mode = simple_mode
        self.logger = logging.getLogger("consolidated_memory")

        # Simple mode - in-memory only
        if simple_mode:
            self.memories = []
            self.logger.info("💾 Simple Memory System initialized")
            return

        # Advanced mode - SQLite + file system
        self._initialize_advanced_system()

    def _initialize_advanced_system(self):
        """Initialize advanced memory system with SQLite and file storage"""
        # Initialize memory paths
        self.memory_dir = Path("data/memory") if not self.config else Path(self.config.MEMORY_PATH)
        self.user_memory_dir = self.memory_dir / "user_memories"
        self.fragment_memory_dir = self.memory_dir / "fragment_memories"
        self.dream_cycle_dir = self.memory_dir / "dream_cycles"
        self.system_memory_dir = self.memory_dir / "system_memories"

        # Create directories
        for directory in [
            self.memory_dir,
            self.user_memory_dir,
            self.fragment_memory_dir,
            self.dream_cycle_dir,
            self.system_memory_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        # Initialize memory database
        self.db_path = self.memory_dir / "lyra_memory.db"
        self._init_database()

        # Memory caches
        self.user_cache = {}
        self.fragment_cache = {}
        self.system_cache = {}

        # Dream cycle state
        self.last_dream_cycle = self._load_dream_cycle_state()
        self.dream_cycle_interval = 3600  # 1 hour in seconds

        self.logger.info("💾 Advanced Memory System initialized")

    def _init_database(self):
        """Initialize SQLite database for memory storage"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # User memories table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        memory_type TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp REAL NOT NULL,
                        importance REAL DEFAULT 0.5,
                        fragment_weights TEXT,
                        metadata TEXT,
                        UNIQUE(user_id, memory_type, content)
                    )
                """
                )

                # Fragment memories table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS fragment_memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fragment_name TEXT NOT NULL,
                        memory_type TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp REAL NOT NULL,
                        weight REAL DEFAULT 0.5,
                        metadata TEXT,
                        UNIQUE(fragment_name, memory_type, content)
                    )
                """
                )

                # System memories table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS system_memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        memory_type TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp REAL NOT NULL,
                        importance REAL DEFAULT 0.5,
                        metadata TEXT,
                        UNIQUE(memory_type, content)
                    )
                """
                )

                conn.commit()

        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise

    # Simple mode methods
    def store_memory(self, content, relevance=0.5):
        """Store a memory (simple mode)"""
        if self.simple_mode:
            memory = {
                "content": content,
                "relevance": relevance,
                "timestamp": datetime.now().isoformat()
            }
            self.memories.append(memory)
            return memory
        else:
            return self.store_system_memory("simple", content, relevance)

    def retrieve_memories(self, query, limit=5):
        """Retrieve relevant memories (simple mode)"""
        if self.simple_mode:
            # Simple keyword matching for now
            relevant = []
            query_words = query.lower().split()
            
            for memory in self.memories:
                content_words = memory["content"].lower().split()
                matches = sum(1 for word in query_words if word in content_words)
                if matches > 0:
                    memory["relevance"] = matches / len(query_words)
                    relevant.append(memory)
            
            # Sort by relevance and return top results
            relevant.sort(key=lambda x: x["relevance"], reverse=True)
            return relevant[:limit]
        else:
            return self.get_system_memories("simple", limit, 0.0)

    async def store_message(self, user_id: str, content: str, guild_id: str = None):
        """Store a message in memory"""
        if self.simple_mode:
            memory = {
                "user_id": user_id,
                "content": content,
                "guild_id": guild_id,
                "timestamp": datetime.now().isoformat(),
                "type": "message"
            }
            self.memories.append(memory)
            return memory
        else:
            return self.store_user_memory(
                user_id=user_id,
                memory_type="message",
                content=content,
                metadata={"guild_id": guild_id}
            )

    async def start_background_tasks(self):
        """Start background memory processing tasks"""
        if self.simple_mode:
            print("🔄 Starting memory system background tasks")
            # For now, just a placeholder
            pass
        else:
            # Advanced background tasks
            self._clean_old_memories()
            self.run_dream_cycle()

    def get_status(self) -> str:
        """Get the status of the memory system"""
        try:
            if self.simple_mode:
                memory_count = len(self.memories)
                recent_memories = len([m for m in self.memories if m.get("type") == "message"])
                return f"Memories: {memory_count}, Messages: {recent_memories}"
            else:
                stats = self.get_stats()
                return f"Advanced Mode - Total: {stats.get('total_memories', 0)}, Users: {stats.get('active_users', 0)}"
        except Exception as e:
            return f"Error: {str(e)}"

    # Advanced mode methods
    def store_user_memory(
        self,
        user_id: str,
        memory_type: str,
        content: str,
        importance: float = 0.5,
        fragment_weights: Dict[str, float] = None,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """Store user memory in advanced mode"""
        if self.simple_mode:
            return self.store_memory(content, importance)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                fragment_weights_json = json.dumps(fragment_weights) if fragment_weights else None
                metadata_json = json.dumps(metadata) if metadata else None
                
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO user_memories 
                    (user_id, memory_type, content, timestamp, importance, fragment_weights, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        memory_type,
                        content,
                        time.time(),
                        importance,
                        fragment_weights_json,
                        metadata_json,
                    ),
                )
                
                conn.commit()
                
                # Update cache
                cache_key = f"{user_id}_{memory_type}"
                if cache_key not in self.user_cache:
                    self.user_cache[cache_key] = []
                self.user_cache[cache_key].append({
                    "content": content,
                    "importance": importance,
                    "timestamp": time.time(),
                    "fragment_weights": fragment_weights,
                    "metadata": metadata,
                })
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error storing user memory: {e}")
            return False

    def get_user_memories(
        self,
        user_id: str,
        memory_type: str = None,
        limit: int = 50,
        min_importance: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """Get user memories from advanced mode"""
        if self.simple_mode:
            return self.retrieve_memories(user_id, limit)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if memory_type:
                    cursor.execute(
                        """
                        SELECT content, importance, timestamp, fragment_weights, metadata
                        FROM user_memories 
                        WHERE user_id = ? AND memory_type = ? AND importance >= ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                        """,
                        (user_id, memory_type, min_importance, limit),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT content, importance, timestamp, fragment_weights, metadata
                        FROM user_memories 
                        WHERE user_id = ? AND importance >= ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                        """,
                        (user_id, min_importance, limit),
                    )
                
                results = []
                for row in cursor.fetchall():
                    content, importance, timestamp, fragment_weights_json, metadata_json = row
                    
                    fragment_weights = json.loads(fragment_weights_json) if fragment_weights_json else None
                    metadata = json.loads(metadata_json) if metadata_json else None
                    
                    results.append({
                        "content": content,
                        "importance": importance,
                        "timestamp": timestamp,
                        "fragment_weights": fragment_weights,
                        "metadata": metadata,
                    })
                
                return results
                
        except Exception as e:
            self.logger.error(f"Error getting user memories: {e}")
            return []

    def store_fragment_memory(
        self,
        fragment_name: str,
        memory_type: str,
        content: str,
        weight: float = 0.5,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """Store fragment memory in advanced mode"""
        if self.simple_mode:
            return self.store_memory(content, weight)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                metadata_json = json.dumps(metadata) if metadata else None
                
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO fragment_memories 
                    (fragment_name, memory_type, content, timestamp, weight, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        fragment_name,
                        memory_type,
                        content,
                        time.time(),
                        weight,
                        metadata_json,
                    ),
                )
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error storing fragment memory: {e}")
            return False

    def get_fragment_memories(
        self,
        fragment_name: str,
        memory_type: str = None,
        limit: int = 50,
        min_weight: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """Get fragment memories from advanced mode"""
        if self.simple_mode:
            return self.retrieve_memories(fragment_name, limit)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if memory_type:
                    cursor.execute(
                        """
                        SELECT content, weight, timestamp, metadata
                        FROM fragment_memories 
                        WHERE fragment_name = ? AND memory_type = ? AND weight >= ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                        """,
                        (fragment_name, memory_type, min_weight, limit),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT content, weight, timestamp, metadata
                        FROM fragment_memories 
                        WHERE fragment_name = ? AND weight >= ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                        """,
                        (fragment_name, min_weight, limit),
                    )
                
                results = []
                for row in cursor.fetchall():
                    content, weight, timestamp, metadata_json = row
                    
                    metadata = json.loads(metadata_json) if metadata_json else None
                    
                    results.append({
                        "content": content,
                        "weight": weight,
                        "timestamp": timestamp,
                        "metadata": metadata,
                    })
                
                return results
                
        except Exception as e:
            self.logger.error(f"Error getting fragment memories: {e}")
            return []

    def store_system_memory(
        self,
        memory_type: str,
        content: str,
        importance: float = 0.5,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """Store system memory in advanced mode"""
        if self.simple_mode:
            return self.store_memory(content, importance)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                metadata_json = json.dumps(metadata) if metadata else None
                
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO system_memories 
                    (memory_type, content, timestamp, importance, metadata)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        memory_type,
                        content,
                        time.time(),
                        importance,
                        metadata_json,
                    ),
                )
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error storing system memory: {e}")
            return False

    def get_system_memories(
        self, memory_type: str = None, limit: int = 50, min_importance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Get system memories from advanced mode"""
        if self.simple_mode:
            return self.retrieve_memories("system", limit)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if memory_type:
                    cursor.execute(
                        """
                        SELECT content, importance, timestamp, metadata
                        FROM system_memories 
                        WHERE memory_type = ? AND importance >= ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                        """,
                        (memory_type, min_importance, limit),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT content, importance, timestamp, metadata
                        FROM system_memories 
                        WHERE importance >= ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                        """,
                        (min_importance, limit),
                    )
                
                results = []
                for row in cursor.fetchall():
                    content, importance, timestamp, metadata_json = row
                    
                    metadata = json.loads(metadata_json) if metadata_json else None
                    
                    results.append({
                        "content": content,
                        "importance": importance,
                        "timestamp": timestamp,
                        "metadata": metadata,
                    })
                
                return results
                
        except Exception as e:
            self.logger.error(f"Error getting system memories: {e}")
            return []

    def consolidate_fragment_memories(self) -> Dict[str, Any]:
        """Consolidate fragment memories in advanced mode"""
        if self.simple_mode:
            return {"consolidated": self.memories}

        try:
            consolidated = {}
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all fragment names
                cursor.execute("SELECT DISTINCT fragment_name FROM fragment_memories")
                fragment_names = [row[0] for row in cursor.fetchall()]
                
                for fragment_name in fragment_names:
                    # Get memories for this fragment
                    cursor.execute(
                        """
                        SELECT content, weight, timestamp
                        FROM fragment_memories 
                        WHERE fragment_name = ?
                        ORDER BY weight DESC, timestamp DESC
                        LIMIT 100
                        """,
                        (fragment_name,),
                    )
                    
                    memories = []
                    for row in cursor.fetchall():
                        content, weight, timestamp = row
                        memories.append({
                            "content": content,
                            "weight": weight,
                            "timestamp": timestamp,
                        })
                    
                    # Consolidate content
                    if memories:
                        consolidated_content = self._consolidate_content([m["content"] for m in memories])
                        consolidated[fragment_name] = {
                            "content": consolidated_content,
                            "memory_count": len(memories),
                            "total_weight": sum(m["weight"] for m in memories),
                            "last_updated": max(m["timestamp"] for m in memories),
                        }
            
            return consolidated
            
        except Exception as e:
            self.logger.error(f"Error consolidating fragment memories: {e}")
            return {}

    def _consolidate_content(self, contents: List[str]) -> str:
        """Consolidate multiple content pieces into a single coherent summary"""
        if not contents:
            return ""
        
        # Simple consolidation - join with newlines and truncate
        consolidated = "\n".join(contents)
        
        # Limit to reasonable size
        if len(consolidated) > 10000:
            consolidated = consolidated[:10000] + "..."
        
        return consolidated

    def run_dream_cycle(self) -> Dict[str, Any]:
        """Run dream cycle consolidation in advanced mode"""
        if self.simple_mode:
            return {"dream_cycle": "Simple mode - no dream cycles"}

        try:
            current_time = time.time()
            
            # Check if enough time has passed since last dream cycle
            if self.last_dream_cycle and current_time - self.last_dream_cycle.get("timestamp", 0) < self.dream_cycle_interval:
                return self.last_dream_cycle
            
            # Consolidate fragment memories
            consolidated_fragments = self.consolidate_fragment_memories()
            
            # Clean old memories
            cleaned_count = self._clean_old_memories()
            
            # Create dream cycle result
            dream_cycle = {
                "timestamp": current_time,
                "consolidated_fragments": consolidated_fragments,
                "cleaned_memories": cleaned_count,
                "cycle_duration": time.time() - current_time,
            }
            
            # Save dream cycle state
            self.last_dream_cycle = dream_cycle
            self._save_dream_cycle_state()
            
            self.logger.info(f"Dream cycle completed: {len(consolidated_fragments)} fragments, {cleaned_count} memories cleaned")
            
            return dream_cycle
            
        except Exception as e:
            self.logger.error(f"Error running dream cycle: {e}")
            return {"error": str(e)}

    def _clean_old_memories(self) -> int:
        """Clean old memories in advanced mode"""
        if self.simple_mode:
            return 0

        try:
            cutoff_time = time.time() - (30 * 24 * 3600)  # 30 days ago
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clean old user memories
                cursor.execute(
                    "DELETE FROM user_memories WHERE timestamp < ?",
                    (cutoff_time,),
                )
                user_deleted = cursor.rowcount
                
                # Clean old fragment memories
                cursor.execute(
                    "DELETE FROM fragment_memories WHERE timestamp < ?",
                    (cutoff_time,),
                )
                fragment_deleted = cursor.rowcount
                
                # Clean old system memories
                cursor.execute(
                    "DELETE FROM system_memories WHERE timestamp < ?",
                    (cutoff_time,),
                )
                system_deleted = cursor.rowcount
                
                conn.commit()
                
                total_deleted = user_deleted + fragment_deleted + system_deleted
                self.logger.info(f"Cleaned {total_deleted} old memories")
                
                return total_deleted
                
        except Exception as e:
            self.logger.error(f"Error cleaning old memories: {e}")
            return 0

    def _load_dream_cycle_state(self) -> Dict[str, Any]:
        """Load dream cycle state from file"""
        if self.simple_mode:
            return {}

        try:
            state_file = self.memory_dir / "dream_cycle_state.json"
            if state_file.exists():
                with open(state_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading dream cycle state: {e}")
        
        return {}

    def _save_dream_cycle_state(self):
        """Save dream cycle state to file"""
        if self.simple_mode:
            return

        try:
            state_file = self.memory_dir / "dream_cycle_state.json"
            with open(state_file, "w") as f:
                json.dump(self.last_dream_cycle, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving dream cycle state: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        if self.simple_mode:
            return {
                "total_memories": len(self.memories),
                "active_users": len(set(m.get("user_id") for m in self.memories if m.get("user_id"))),
                "memory_size_mb": 0.0,
                "mode": "simple"
            }

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count total memories
                cursor.execute("SELECT COUNT(*) FROM user_memories")
                user_memories = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM fragment_memories")
                fragment_memories = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM system_memories")
                system_memories = cursor.fetchone()[0]
                
                total_memories = user_memories + fragment_memories + system_memories
                
                # Count active users
                cursor.execute("SELECT COUNT(DISTINCT user_id) FROM user_memories")
                active_users = cursor.fetchone()[0]
                
                # Calculate memory size
                memory_size_mb = self.db_path.stat().st_size / (1024 * 1024)
                
                return {
                    "total_memories": total_memories,
                    "user_memories": user_memories,
                    "fragment_memories": fragment_memories,
                    "system_memories": system_memories,
                    "active_users": active_users,
                    "memory_size_mb": memory_size_mb,
                    "mode": "advanced"
                }
                
        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return {"error": str(e)}

    def load_user_memory(self, user_id: str) -> Dict[str, Any]:
        """Load user memory data"""
        if self.simple_mode:
            user_memories = [m for m in self.memories if m.get("user_id") == user_id]
            return {"memories": user_memories}
        else:
            memories = self.get_user_memories(user_id)
            return {"memories": memories}

    def save_user_memory(self, user_id: str, memory_data: Dict[str, Any]) -> bool:
        """Save user memory data"""
        if self.simple_mode:
            # In simple mode, just store the data
            if "memories" in memory_data:
                for memory in memory_data["memories"]:
                    memory["user_id"] = user_id
                    self.memories.append(memory)
            return True
        else:
            # In advanced mode, store each memory
            if "memories" in memory_data:
                for memory in memory_data["memories"]:
                    self.store_user_memory(
                        user_id=user_id,
                        memory_type=memory.get("type", "user"),
                        content=memory.get("content", ""),
                        importance=memory.get("importance", 0.5),
                        metadata=memory.get("metadata", {})
                    )
            return True

    def get_all_users(self) -> List[str]:
        """Get all user IDs"""
        if self.simple_mode:
            return list(set(m.get("user_id") for m in self.memories if m.get("user_id")))
        else:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT DISTINCT user_id FROM user_memories")
                    return [row[0] for row in cursor.fetchall()]
            except Exception as e:
                self.logger.error(f"Error getting all users: {e}")
                return []


# Alias for backward compatibility
MemorySystem = ConsolidatedMemorySystem 