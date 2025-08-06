#!/usr/bin/env python3
"""
Self-Learning System
Allows Luna to create her own optimized formats and learning patterns
"""

import json
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import time
import hashlib
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class LearningPattern:
    """Pattern learned by Luna for optimization"""
    pattern_id: str
    pattern_type: str
    data: bytes  # AI-optimized format
    frequency: int
    success_rate: float
    last_used: float
    created_at: float


class SelfLearningSystem:
    """System that allows Luna to create her own optimized formats and learn"""
    
    def __init__(self, learning_dir: str = "data/ai_learning"):
        self.learning_dir = Path(learning_dir)
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        # Learning patterns
        self.patterns = {}
        self.optimization_rules = {}
        self.format_preferences = {}
        
        # Performance tracking
        self.performance_metrics = defaultdict(list)
        self.optimization_history = []
        
        # Load existing patterns
        self._load_existing_patterns()
    
    def _load_existing_patterns(self):
        """Load existing learning patterns"""
        pattern_file = self.learning_dir / "learning_patterns.pkl"
        if pattern_file.exists():
            try:
                with open(pattern_file, 'rb') as f:
                    self.patterns = pickle.load(f)
                logger.info(f"Loaded {len(self.patterns)} existing patterns")
            except Exception as e:
                logger.error(f"Error loading patterns: {e}")
    
    def create_optimized_format(self, data: Any, context: str) -> bytes:
        """Create AI-optimized format based on learning patterns"""
        # Analyze data type and context
        data_type = type(data).__name__
        context_hash = hashlib.sha256(context.encode()).hexdigest()
        
        # Check if we have a learned pattern for this type
        pattern_key = f"{data_type}_{context_hash}"
        
        if pattern_key in self.patterns:
            pattern = self.patterns[pattern_key]
            # Use learned optimization
            return self._apply_learned_optimization(data, pattern)
        else:
            # Create new optimization pattern
            return self._create_new_optimization(data, data_type, context)
    
    def _apply_learned_optimization(self, data: Any, pattern: LearningPattern) -> bytes:
        """Apply learned optimization pattern"""
        # Convert to numpy arrays for efficiency
        if isinstance(data, dict):
            optimized = {}
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    optimized[key] = np.array([value], dtype=np.float32)
                elif isinstance(value, list):
                    optimized[key] = np.array(value, dtype=np.float32)
                else:
                    optimized[key] = value
        else:
            optimized = data
        
        # Use pickle protocol 4 for AI optimization
        return pickle.dumps(optimized, protocol=4)
    
    def _create_new_optimization(self, data: Any, data_type: str, context: str) -> bytes:
        """Create new optimization pattern"""
        # Analyze data structure
        if isinstance(data, dict):
            # Optimize dict structure
            optimized = self._optimize_dict_structure(data)
        elif isinstance(data, list):
            # Optimize list structure
            optimized = np.array(data, dtype=np.float32)
        else:
            optimized = data
        
        # Create learning pattern
        pattern = LearningPattern(
            pattern_id=f"{data_type}_{hashlib.sha256(context.encode()).hexdigest()}",
            pattern_type=data_type,
            data=pickle.dumps(optimized, protocol=4),
            frequency=1,
            success_rate=0.8,  # Initial assumption
            last_used=time.time(),
            created_at=time.time()
        )
        
        # Store pattern
        self.patterns[pattern.pattern_id] = pattern
        self._save_patterns()
        
        return pickle.dumps(optimized, protocol=4)
    
    def _optimize_dict_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize dictionary structure for AI processing"""
        optimized = {}
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                # Convert numbers to numpy arrays
                optimized[key] = np.array([value], dtype=np.float32)
            elif isinstance(value, list):
                # Check if list contains only numbers
                try:
                    optimized[key] = np.array(value, dtype=np.float32)
                except (ValueError, TypeError):
                    # If conversion fails, keep as list
                    optimized[key] = value
            elif isinstance(value, dict):
                # Recursively optimize nested dicts
                optimized[key] = self._optimize_dict_structure(value)
            else:
                # Keep other types as-is
                optimized[key] = value
        
        return optimized
    
    def learn_from_interaction(self, interaction_data: Dict[str, Any]):
        """Learn from interaction to improve future responses"""
        # Extract learning insights
        message_length = len(interaction_data.get("message", ""))
        response_length = len(interaction_data.get("response", ""))
        emotional_intensity = interaction_data.get("emotional_intensity", 0.5)
        response_time = interaction_data.get("response_time", 0.0)
        
        # Create learning insight
        insight = {
            "message_length": message_length,
            "response_length": response_length,
            "emotional_intensity": emotional_intensity,
            "response_time": response_time,
            "timestamp": time.time()
        }
        
        # Store insight
        self._store_learning_insight(insight)
        
        # Update performance metrics
        self.performance_metrics["response_times"].append(response_time)
        self.performance_metrics["emotional_intensities"].append(emotional_intensity)
        
        # Check if optimization is needed
        self._check_optimization_needs()
    
    def _store_learning_insight(self, insight: Dict[str, Any]):
        """Store learning insight for future optimization"""
        insight_file = self.learning_dir / f"insight_{time.time()}.pkl"
        
        try:
            with open(insight_file, 'wb') as f:
                pickle.dump(insight, f)
        except Exception as e:
            logger.error(f"Error storing insight: {e}")
    
    def _check_optimization_needs(self):
        """Check if optimization is needed based on performance"""
        if len(self.performance_metrics["response_times"]) > 10:
            avg_response_time = np.mean(self.performance_metrics["response_times"][-10:])
            
            if avg_response_time > 0.5:  # If average response time > 500ms
                self._trigger_optimization("response_time")
    
    def _trigger_optimization(self, optimization_type: str):
        """Trigger optimization based on performance issues"""
        optimization = {
            "type": optimization_type,
            "timestamp": time.time(),
            "performance_metrics": dict(self.performance_metrics)
        }
        
        self.optimization_history.append(optimization)
        
        # Apply optimization
        if optimization_type == "response_time":
            self._optimize_response_time()
    
    def _optimize_response_time(self):
        """Optimize for faster response times"""
        # Create optimization rule
        optimization_rule = {
            "type": "response_time_optimization",
            "cache_size": 100,
            "preload_patterns": True,
            "compression_level": "high"
        }
        
        self.optimization_rules["response_time"] = optimization_rule
        
        # Save optimization
        self._save_optimization_rules()
    
    def create_ai_native_database(self, data: Any, purpose: str) -> bytes:
        """Create AI-native database structure"""
        # Analyze data for optimal storage
        if isinstance(data, dict):
            # Create optimized structure
            optimized_structure = {
                "metadata": {
                    "purpose": purpose,
                    "created_at": time.time(),
                    "ai_optimized": True
                },
                "data": self._optimize_dict_structure(data),
                "indexes": self._create_ai_indexes(data)
            }
        else:
            optimized_structure = {
                "metadata": {
                    "purpose": purpose,
                    "created_at": time.time(),
                    "ai_optimized": True
                },
                "data": data,
                "indexes": {}
            }
        
        return pickle.dumps(optimized_structure, protocol=4)
    
    def _create_ai_indexes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create AI-optimized indexes for fast access"""
        indexes = {}
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                indexes[key] = {
                    "type": "numeric",
                    "min": value,
                    "max": value,
                    "avg": value
                }
            elif isinstance(value, list):
                indexes[key] = {
                    "type": "array",
                    "length": len(value),
                    "sample": value[:5] if len(value) > 5 else value
                }
            elif isinstance(value, str):
                indexes[key] = {
                    "type": "string",
                    "length": len(value),
                    "hash": hashlib.sha256(value.encode()).hexdigest()
                }
        
        return indexes
    
    def learn_emotional_patterns(self, emotional_data: Dict[str, Any]):
        """Learn from emotional patterns to improve responses"""
        # Extract emotional patterns
        emotional_state = emotional_data.get("state", "balanced")
        emotional_level = emotional_data.get("level", 0.5)
        trigger_words = emotional_data.get("trigger_words", [])
        
        # Create emotional pattern
        pattern = {
            "state": emotional_state,
            "level": emotional_level,
            "triggers": trigger_words,
            "timestamp": time.time()
        }
        
        # Store pattern
        pattern_id = f"emotional_{emotional_state}_{int(emotional_level * 10)}"
        self.patterns[pattern_id] = LearningPattern(
            pattern_id=pattern_id,
            pattern_type="emotional",
            data=pickle.dumps(pattern, protocol=4),
            frequency=1,
            success_rate=0.9,
            last_used=time.time(),
            created_at=time.time()
        )
        
        self._save_patterns()
    
    def get_optimized_response_format(self, response_type: str) -> Dict[str, Any]:
        """Get optimized format for response type"""
        if response_type in self.format_preferences:
            return self.format_preferences[response_type]
        
        # Create new format preference
        format_pref = {
            "type": response_type,
            "optimization_level": "high",
            "compression": True,
            "cache_priority": "high"
        }
        
        self.format_preferences[response_type] = format_pref
        return format_pref
    
    def _save_patterns(self):
        """Save learning patterns"""
        pattern_file = self.learning_dir / "learning_patterns.pkl"
        try:
            with open(pattern_file, 'wb') as f:
                pickle.dump(self.patterns, f)
        except Exception as e:
            logger.error(f"Error saving patterns: {e}")
    
    def _save_optimization_rules(self):
        """Save optimization rules"""
        rules_file = self.learning_dir / "optimization_rules.pkl"
        try:
            with open(rules_file, 'wb') as f:
                pickle.dump(self.optimization_rules, f)
        except Exception as e:
            logger.error(f"Error saving optimization rules: {e}")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning system statistics"""
        return {
            "total_patterns": len(self.patterns),
            "optimization_rules": len(self.optimization_rules),
            "format_preferences": len(self.format_preferences),
            "performance_metrics": dict(self.performance_metrics),
            "optimization_history": len(self.optimization_history)
        }


# Initialize self-learning system
self_learning_system = SelfLearningSystem() 