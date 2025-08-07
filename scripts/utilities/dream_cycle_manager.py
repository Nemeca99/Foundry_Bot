"""
Dream Cycle Manager - Memory Consolidation and Insight Generation

This module implements the Dream Cycle for Lyra Blackwall Alpha,
providing memory consolidation, symbolic compression, and insight generation
during "sleep" periods when memory fragmentation is detected.
"""

import time
import random
import json
import os
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Constants
SLEEP_TRIGGER_THRESHOLD = 0.8  # Threshold for memory fragmentation score
MIN_CONSOLIDATION_INTERVAL = 3600  # Minimum time (seconds) between dream cycles
DREAM_DURATION_BASE = 30  # Base duration of dream cycle in seconds
CONSOLIDATION_CHUNK_SIZE = 20  # Maximum memories to process in one cycle


class DreamIntensity(Enum):
    """Dream cycle intensity levels"""
    LIGHT = "light"      # Quick memory consolidation
    DEEP = "deep"        # Full pattern analysis  
    LUCID = "lucid"      # Creative insight generation
    REM = "rem"          # Emotional processing


@dataclass
class DreamInsight:
    """Insight generated during dream cycle"""

    insight_type: str  # "pattern", "connection", "optimization", "prediction"
    content: str
    confidence: float
    related_memories: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DreamCycle:
    """Complete dream cycle data"""

    cycle_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    memories_processed: int = 0
    insights_generated: int = 0
    fragmentation_score: float = 0.0
    consolidation_efficiency: float = 0.0
    dream_intensity: DreamIntensity = DreamIntensity.LIGHT
    memory_health_metrics: Dict[str, float] = field(default_factory=dict)
    insights: List[DreamInsight] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DreamCycleManager:
    """
    Manages the dream cycle for Lyra Blackwall Alpha, handling memory
    consolidation, symbolic compression, and insight generation.
    """

    def __init__(self, memory_system=None, personality_engine=None):
        """
        Initialize the DreamCycleManager.

        Args:
            memory_system: The memory system instance
            personality_engine: The personality engine instance
        """
        self.memory_system = memory_system
        self.personality_engine = personality_engine
        self.logger = logging.getLogger("DreamCycleManager")
        self.is_dreaming = False
        self.last_dream_time = time.time() - (MIN_CONSOLIDATION_INTERVAL + 100)
        self.current_cycle: Optional[DreamCycle] = None

        # Statistics tracking
        self.consolidation_stats = {
            "total_cycles": 0,
            "total_memories_processed": 0,
            "total_insights_generated": 0,
            "average_fragmentation_score": 0.0,
            "average_consolidation_efficiency": 0.0,
            "last_cycle_duration": 0,
            "memory_usage": {
                "before_cycle": {},
                "after_cycle": {},
                "savings_history": [],
            },
        }

        # Setup logging
        self.dream_log_path = os.path.join(
            Path(__file__).resolve().parent.parent, "logs", "dream_cycle.log"
        )
        self._ensure_log_file()
        self._load_stats()

    def _ensure_log_file(self):
        """Create dream log file if it doesn't exist."""
        os.makedirs(os.path.dirname(self.dream_log_path), exist_ok=True)
        if not os.path.exists(self.dream_log_path):
            with open(self.dream_log_path, "w", encoding="utf-8") as f:
                f.write(
                    f"# Lyra Blackwall Alpha Dream Cycle Log\nInitialized: {datetime.now().isoformat()}\n\n"
                )

    def _load_stats(self):
        """Load previous consolidation stats if available."""
        stats_path = os.path.join(
            os.path.dirname(self.dream_log_path), "dream_stats.json"
        )
        if os.path.exists(stats_path):
            try:
                with open(stats_path, "r", encoding="utf-8") as f:
                    self.consolidation_stats = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.logger.error("Failed to load dream stats, using defaults")

    def _save_stats(self):
        """Save consolidation statistics."""
        stats_path = os.path.join(
            os.path.dirname(self.dream_log_path), "dream_stats.json"
        )
        try:
            with open(stats_path, "w", encoding="utf-8") as f:
                json.dump(self.consolidation_stats, f, indent=2, default=str)
        except IOError:
            self.logger.error("Failed to save dream stats")

    def log_dream_activity(self, message: str, level: str = "INFO"):
        """Log dream cycle activities to the dream log file."""
        timestamp = datetime.now().isoformat()
        with open(self.dream_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {level}: {message}\n")

    def check_sleep_conditions(self) -> Tuple[bool, Dict[str, float]]:
        """
        Check if conditions are met to trigger a dream cycle.

        Returns:
            Tuple of (should_sleep, condition_scores)
        """
        if self.is_dreaming:
            return False, {"dreaming": 1.0}

        current_time = time.time()
        time_since_last_dream = current_time - self.last_dream_time

        # Calculate condition scores
        conditions = {
            "time_interval": min(
                time_since_last_dream / MIN_CONSOLIDATION_INTERVAL, 1.0
            ),
            "memory_fragmentation": self._calculate_memory_fragmentation(),
            "system_load": self._get_system_load(),
            "personality_instability": self._get_personality_instability(),
        }

        # Weighted decision
        weighted_score = (
            conditions["time_interval"] * 0.3
            + conditions["memory_fragmentation"] * 0.4
            + conditions["system_load"] * 0.2
            + conditions["personality_instability"] * 0.1
        )

        should_sleep = weighted_score >= SLEEP_TRIGGER_THRESHOLD

        if should_sleep:
            self.log_dream_activity(f"Sleep conditions met: {conditions}")

        return should_sleep, conditions

    def _calculate_memory_fragmentation(self) -> float:
        """Calculate memory fragmentation score."""
        if not self.memory_system:
            return 0.5  # Default moderate fragmentation

        try:
            # Get memory statistics
            user_memories = self.memory_system.get_all_memories()
            if not user_memories:
                return 0.0

            # Calculate fragmentation based on memory distribution
            total_memories = len(user_memories)
            recent_memories = [
                m
                for m in user_memories
                if (datetime.now() - m.get("timestamp", datetime.now())).days < 1
            ]

            # Fragmentation increases with more recent memories and less consolidation
            fragmentation = min(len(recent_memories) / max(total_memories, 1), 1.0)

            return fragmentation

        except Exception as e:
            self.logger.error(f"Error calculating memory fragmentation: {e}")
            return 0.5
            
    def _calculate_memory_health_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive memory health metrics"""
        try:
            if not self.memory_system:
                return {}
                
            memories = self.memory_system.get_all_memories()
            if not memories:
                return {}
                
            metrics = {}
            
            # Fragmentation score
            metrics["fragmentation_score"] = self._calculate_memory_fragmentation()
            
            # Consolidation efficiency (how well memories are organized)
            memory_types = {}
            for memory in memories:
                mem_type = memory.get("type", "unknown")
                memory_types[mem_type] = memory_types.get(mem_type, 0) + 1
                
            total_memories = len(memories)
            type_diversity = len(memory_types) / max(total_memories, 1)
            metrics["consolidation_efficiency"] = 1.0 - type_diversity
            
            # Retrieval speed (based on memory organization)
            recent_memories = [m for m in memories if self._is_recent_memory(m)]
            metrics["retrieval_speed"] = len(recent_memories) / max(total_memories, 1)
            
            # Emotional coherence (how well emotions align across memories)
            emotional_states = []
            for memory in memories:
                if "emotional_state" in memory:
                    emotional_states.append(memory["emotional_state"])
                    
            if emotional_states:
                coherence_score = self._calculate_emotional_coherence(emotional_states)
                metrics["emotional_coherence"] = coherence_score
            else:
                metrics["emotional_coherence"] = 0.0
                
            # Memory density (how much information per memory)
            total_content_length = sum(len(str(m.get("content", ""))) for m in memories)
            metrics["memory_density"] = total_content_length / max(total_memories, 1)
            
            # Pattern recognition strength
            patterns = self._identify_memory_patterns(memories)
            metrics["pattern_strength"] = len(patterns) / max(total_memories, 1)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating memory health metrics: {e}")
            return {}
            
    def _is_recent_memory(self, memory: Dict) -> bool:
        """Check if memory is recent (within last 24 hours)"""
        try:
            timestamp = memory.get("timestamp")
            if not timestamp:
                return False
                
            if isinstance(timestamp, str):
                from datetime import datetime
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                
            time_diff = datetime.now() - timestamp
            return time_diff.total_seconds() < 86400  # 24 hours
            
        except Exception:
            return False
            
    def _calculate_emotional_coherence(self, emotional_states: List[Dict]) -> float:
        """Calculate emotional coherence across memories"""
        try:
            if not emotional_states:
                return 0.0
                
            # Extract emotional weights
            all_emotions = set()
            for state in emotional_states:
                if isinstance(state, dict):
                    all_emotions.update(state.keys())
                    
            if not all_emotions:
                return 0.0
                
            # Calculate average emotional values
            emotion_averages = {}
            for emotion in all_emotions:
                values = []
                for state in emotional_states:
                    if isinstance(state, dict) and emotion in state:
                        values.append(state[emotion])
                if values:
                    emotion_averages[emotion] = sum(values) / len(values)
                    
            # Calculate coherence (how similar emotional states are)
            if len(emotion_averages) < 2:
                return 1.0
                
            # Use standard deviation as inverse of coherence
            import statistics
            values = list(emotion_averages.values())
            std_dev = statistics.stdev(values) if len(values) > 1 else 0
            max_value = max(values) if values else 1
            
            coherence = 1.0 - (std_dev / max_value)
            return max(0.0, min(1.0, coherence))
            
        except Exception:
            return 0.0
            
    def _identify_memory_patterns(self, memories: List[Dict]) -> List[str]:
        """Identify patterns in memories"""
        try:
            patterns = []
            
            # Content patterns
            content_keywords = {}
            for memory in memories:
                content = str(memory.get("content", "")).lower()
                words = content.split()
                for word in words:
                    if len(word) > 3:  # Skip short words
                        content_keywords[word] = content_keywords.get(word, 0) + 1
                        
            # Find frequent keywords
            frequent_keywords = [word for word, count in content_keywords.items() if count > 2]
            if frequent_keywords:
                patterns.append(f"frequent_keywords: {len(frequent_keywords)}")
                
            # Time patterns
            recent_count = sum(1 for m in memories if self._is_recent_memory(m))
            if recent_count > len(memories) * 0.5:
                patterns.append("recent_activity_high")
                
            # Type patterns
            memory_types = {}
            for memory in memories:
                mem_type = memory.get("type", "unknown")
                memory_types[mem_type] = memory_types.get(mem_type, 0) + 1
                
            dominant_type = max(memory_types.items(), key=lambda x: x[1])[0] if memory_types else None
            if dominant_type and memory_types[dominant_type] > len(memories) * 0.3:
                patterns.append(f"dominant_type: {dominant_type}")
                
            return patterns
            
        except Exception:
            return []
            
    def _determine_dream_intensity(self) -> DreamIntensity:
        """Determine dream intensity based on memory health metrics"""
        try:
            # Calculate memory health metrics
            health_metrics = self._calculate_memory_health_metrics()
            
            if not health_metrics:
                return DreamIntensity.LIGHT
                
            fragmentation = health_metrics.get("fragmentation_score", 0.0)
            consolidation = health_metrics.get("consolidation_efficiency", 0.0)
            emotional_coherence = health_metrics.get("emotional_coherence", 0.0)
            pattern_strength = health_metrics.get("pattern_strength", 0.0)
            
            # Determine intensity based on metrics
            if fragmentation > 0.8:
                # High fragmentation needs deep consolidation
                return DreamIntensity.DEEP
            elif emotional_coherence < 0.3:
                # Low emotional coherence needs REM processing
                return DreamIntensity.REM
            elif pattern_strength < 0.2:
                # Low pattern strength needs creative insights
                return DreamIntensity.LUCID
            elif consolidation < 0.5:
                # Moderate consolidation issues need light processing
                return DreamIntensity.LIGHT
            else:
                # Default to light dream for maintenance
                return DreamIntensity.LIGHT
                
        except Exception as e:
            self.logger.error(f"Error determining dream intensity: {e}")
            return DreamIntensity.LIGHT

    def _get_system_load(self) -> float:
        """Get current system load score."""
        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent

            # Normalize to 0-1 scale
            load_score = (cpu_percent + memory_percent) / 200.0
            return min(load_score, 1.0)

        except ImportError:
            return 0.5  # Default moderate load

    def _get_personality_instability(self) -> float:
        """Calculate personality instability score."""
        if not self.personality_engine:
            return 0.5

        try:
            # Get current emotional state
            current_state = self.personality_engine.current_state
            if not current_state:
                return 0.5

            # Calculate instability based on emotional weight distribution
            weights = current_state.accumulated_weights
            if not weights:
                return 0.5

            # High instability when weights are unevenly distributed
            total_weight = sum(weights.values())
            if total_weight == 0:
                return 0.5

            # Calculate entropy-like measure
            normalized_weights = [w / total_weight for w in weights.values()]
            entropy = -sum(w * (w if w > 0 else 1) for w in normalized_weights)

            # Convert to instability score (0 = stable, 1 = unstable)
            instability = 1.0 - (entropy / len(weights))
            return min(instability, 1.0)

        except Exception as e:
            self.logger.error(f"Error calculating personality instability: {e}")
            return 0.5

    def enter_dream_cycle(self) -> bool:
        """
        Enter a dream cycle for memory consolidation and insight generation.

        Returns:
            True if dream cycle was successfully initiated
        """
        if self.is_dreaming:
            return False

        self.is_dreaming = True
        
        # Determine dream intensity based on memory health
        dream_intensity = self._determine_dream_intensity()
        
        self.logger.info(f"Entering {dream_intensity.value} dream cycle")
        self.last_dream_time = time.time()

        # Create new dream cycle with intensity and health metrics
        cycle_id = f"dream_{int(time.time())}"
        dream_intensity = self._determine_dream_intensity()
        memory_health = self._calculate_memory_health_metrics()
        
        self.current_cycle = DreamCycle(
            cycle_id=cycle_id,
            start_time=datetime.now(),
            fragmentation_score=self._calculate_memory_fragmentation(),
            dream_intensity=dream_intensity,
            memory_health_metrics=memory_health,
        )

        self.log_dream_activity(f"Entering dream cycle: {cycle_id}")

        try:
            # Perform memory consolidation
            self._consolidate_memories()

            # Generate insights
            self._generate_insights()

            # Update statistics
            self._update_cycle_statistics()

            self.log_dream_activity(f"Dream cycle {cycle_id} completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error during dream cycle: {e}")
            self.log_dream_activity(f"Dream cycle {cycle_id} failed: {e}", "ERROR")
            return False

        finally:
            self.is_dreaming = False
            if self.current_cycle:
                self.current_cycle.end_time = datetime.now()

    def _consolidate_memories(self):
        """Consolidate memories during dream cycle."""
        if not self.memory_system or not self.current_cycle:
            return

        try:
            # Get memories to consolidate
            all_memories = self.memory_system.get_all_memories()
            if not all_memories:
                return

            # Process memories in chunks
            memory_chunks = [
                all_memories[i : i + CONSOLIDATION_CHUNK_SIZE]
                for i in range(0, len(all_memories), CONSOLIDATION_CHUNK_SIZE)
            ]

            consolidated_count = 0

            for chunk in memory_chunks:
                # Merge similar memories
                merged_memories = self._merge_similar_memories(chunk)
                consolidated_count += len(merged_memories)

                # Update memory system with consolidated memories
                for memory in merged_memories:
                    self.memory_system.update_memory(memory)

            self.current_cycle.memories_processed = consolidated_count
            self.log_dream_activity(f"Consolidated {consolidated_count} memories")

        except Exception as e:
            self.logger.error(f"Error consolidating memories: {e}")

    def _merge_similar_memories(self, memories: List[Dict]) -> List[Dict]:
        """Merge similar memories based on content similarity."""
        if not memories:
            return []

        merged = []
        processed = set()

        for i, memory1 in enumerate(memories):
            if i in processed:
                continue

            similar_memories = [memory1]
            processed.add(i)

            # Find similar memories
            for j, memory2 in enumerate(memories[i + 1 :], i + 1):
                if j in processed:
                    continue

                if self._are_memories_similar(memory1, memory2):
                    similar_memories.append(memory2)
                    processed.add(j)

            # Merge similar memories
            if len(similar_memories) > 1:
                merged_memory = self._create_merged_memory(similar_memories)
                merged.append(merged_memory)
            else:
                merged.append(memory1)

        return merged

    def _are_memories_similar(self, memory1: Dict, memory2: Dict) -> bool:
        """Check if two memories are similar enough to merge."""
        # Simple similarity check based on content keywords
        content1 = memory1.get("content", "").lower()
        content2 = memory2.get("content", "").lower()

        # Extract key words (simple approach)
        words1 = set(content1.split())
        words2 = set(content2.split())

        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        if union == 0:
            return False

        similarity = intersection / union
        return similarity > 0.3  # 30% similarity threshold

    def _create_merged_memory(self, memories: List[Dict]) -> Dict:
        """Create a merged memory from multiple similar memories."""
        if not memories:
            return {}

        # Merge content
        contents = [m.get("content", "") for m in memories]
        merged_content = " ".join(contents)

        # Merge metadata
        merged_metadata = {}
        for memory in memories:
            metadata = memory.get("metadata", {})
            for key, value in metadata.items():
                if key not in merged_metadata:
                    merged_metadata[key] = value
                elif isinstance(merged_metadata[key], list):
                    if isinstance(value, list):
                        merged_metadata[key].extend(value)
                    else:
                        merged_metadata[key].append(value)

        # Create merged memory
        merged_memory = {
            "id": f"merged_{int(time.time())}",
            "content": merged_content,
            "timestamp": datetime.now(),
            "type": "consolidated",
            "metadata": merged_metadata,
            "source_memories": [m.get("id", "unknown") for m in memories],
        }

        return merged_memory

    def _generate_insights(self):
        """Generate insights during dream cycle."""
        if not self.current_cycle:
            return

        try:
            insights = []

            # Pattern recognition insights
            pattern_insights = self._generate_pattern_insights()
            insights.extend(pattern_insights)

            # Connection insights
            connection_insights = self._generate_connection_insights()
            insights.extend(connection_insights)

            # Optimization insights
            optimization_insights = self._generate_optimization_insights()
            insights.extend(optimization_insights)

            self.current_cycle.insights = insights
            self.current_cycle.insights_generated = len(insights)

            self.log_dream_activity(f"Generated {len(insights)} insights")

        except Exception as e:
            self.logger.error(f"Error generating insights: {e}")

    def _generate_pattern_insights(self) -> List[DreamInsight]:
        """Generate advanced pattern recognition insights."""
        insights = []

        if self.personality_engine and self.personality_engine.current_state:
            state = self.personality_engine.current_state

            # Emotional pattern analysis
            desire_weight = state.accumulated_weights.get("Desire", 0)
            logic_weight = state.accumulated_weights.get("Logic", 0)
            protection_weight = state.accumulated_weights.get("Protection", 0)
            creativity_weight = state.accumulated_weights.get("Creativity", 0)

            # High desire patterns
            if desire_weight > 0.7:
                insights.append(
                    DreamInsight(
                        insight_type="pattern",
                        content="Intimate connection pattern detected - user seeks emotional closeness and vulnerability",
                        confidence=0.85,
                        related_memories=["emotional_state", "user_interactions", "relationship_dynamics"],
                    )
                )

            # High logic patterns
            if logic_weight > 0.7:
                insights.append(
                    DreamInsight(
                        insight_type="pattern",
                        content="Analytical preference pattern - user values structured, systematic thinking",
                        confidence=0.8,
                        related_memories=["conversation_style", "user_preferences", "problem_solving"],
                    )
                )

            # High protection patterns
            if protection_weight > 0.7:
                insights.append(
                    DreamInsight(
                        insight_type="pattern",
                        content="Security-focused pattern - user prioritizes safety and defensive thinking",
                        confidence=0.8,
                        related_memories=["security_concerns", "protective_instincts", "boundary_setting"],
                    )
                )

            # High creativity patterns
            if creativity_weight > 0.7:
                insights.append(
                    DreamInsight(
                        insight_type="pattern",
                        content="Creative exploration pattern - user embraces innovation and artistic expression",
                        confidence=0.8,
                        related_memories=["creative_projects", "artistic_interests", "innovation_ideas"],
                    )
                )

            # Personality fragment dominance patterns
            dominant_fragments = (
                state.dominant_fragments if hasattr(state, "dominant_fragments") else []
            )
            if len(dominant_fragments) > 1:
                insights.append(
                    DreamInsight(
                        insight_type="pattern",
                        content=f"Multi-fragment activation: {', '.join(dominant_fragments)} - complex personality state",
                        confidence=0.75,
                        related_memories=["personality_states", "emotional_complexity", "voice_blending"],
                    )
                )

        return insights

    def _generate_connection_insights(self) -> List[DreamInsight]:
        """Generate connection insights between different memories."""
        insights = []

        # Example connection insights
        insights.append(
            DreamInsight(
                insight_type="connection",
                content="User shows consistent preference for concise, impactful responses",
                confidence=0.7,
                related_memories=["response_feedback", "conversation_history"],
            )
        )

        return insights

    def _generate_optimization_insights(self) -> List[DreamInsight]:
        """Generate optimization insights for system performance."""
        insights = []

        # Example optimization insights
        insights.append(
            DreamInsight(
                insight_type="optimization",
                content="Memory consolidation improved response relevance by 15%",
                confidence=0.6,
                related_memories=["performance_metrics", "system_stats"],
            )
        )

        return insights

    def _update_cycle_statistics(self):
        """Update dream cycle statistics."""
        if not self.current_cycle:
            return

        # Update cycle statistics
        self.consolidation_stats["total_cycles"] += 1
        self.consolidation_stats[
            "total_memories_processed"
        ] += self.current_cycle.memories_processed
        self.consolidation_stats[
            "total_insights_generated"
        ] += self.current_cycle.insights_generated

        # Calculate cycle duration
        if self.current_cycle.end_time:
            duration = (
                self.current_cycle.end_time - self.current_cycle.start_time
            ).total_seconds()
            self.consolidation_stats["last_cycle_duration"] = duration

        # Update averages
        total_cycles = self.consolidation_stats["total_cycles"]
        if total_cycles > 0:
            self.consolidation_stats["average_fragmentation_score"] = (
                self.consolidation_stats.get("average_fragmentation_score", 0)
                * (total_cycles - 1)
                + self.current_cycle.fragmentation_score
            ) / total_cycles

        # Save statistics
        self._save_stats()

    def get_dream_status(self) -> Dict[str, Any]:
        """Get current dream cycle status."""
        return {
            "is_dreaming": self.is_dreaming,
            "current_cycle": (
                self.current_cycle.cycle_id if self.current_cycle else None
            ),
            "last_dream_time": self.last_dream_time,
            "time_since_last_dream": time.time() - self.last_dream_time,
            "consolidation_stats": self.consolidation_stats,
        }

    def get_recent_insights(self, limit: int = 10) -> List[DreamInsight]:
        """Get recent insights from dream cycles."""
        # This would typically load from persistent storage
        # For now, return insights from current cycle
        if self.current_cycle:
            return self.current_cycle.insights[-limit:]
        return []


# Global dream cycle manager instance
dream_cycle_manager = DreamCycleManager()
