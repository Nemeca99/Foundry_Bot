"""
Quantum Superposition AI Architecture - The Real Implementation
Chef as Observer that collapses superposition between LM Studio and Ollama

Flow: User (1) → Chef (2) → LM Studio (4) → Chef (2) → Waiter+Ollama (3) → Chef (2) → User (1)
Superposition: LM Studio (Particle) + Ollama (Wave) → Chef (Observer) → Collapse
"""

import asyncio
import logging
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
import psutil
import os

# Import personality engine
from .personality_engine import personality_engine, EmotionalState
from .memory_system import memory_system
from .dream_cycle_manager import dream_cycle_manager
from .three_tier_architecture import three_tier_architecture, TierRole
from .daydream_system import daydream_system
from .logic_block_engine import logic_block_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SuperpositionState(Enum):
    """Quantum superposition states"""

    SUPERPOSED = "superposed"  # Multiple possibilities exist
    COLLAPSING = "collapsing"  # Observer is collapsing
    COLLAPSED = "collapsed"  # Single state resolved
    OBSERVED = "observed"  # Final state delivered


@dataclass
class QuantumOrder:
    """User order that initiates superposition collapse"""

    user_id: str
    message: str
    format_type: str = "text"
    timestamp: datetime = field(default_factory=datetime.now)
    superposition_id: Optional[str] = None

    def __post_init__(self):
        if self.superposition_id is None:
            self.superposition_id = (
                f"quantum_{self.user_id}_{int(self.timestamp.timestamp())}"
            )


@dataclass
class ParticleState:
    """LM Studio AI - Particle position in superposition"""

    user_id: str
    creative_response: str
    confidence: float
    processing_time: float
    gpu_utilization: float
    timestamp: datetime = field(default_factory=datetime.now)
    state_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WaveState:
    """Ollama AI - Wave position in superposition"""

    user_id: str
    context_summary: str
    emotion_profile: Dict[str, float]
    relevant_memories: List[Dict]
    interaction_history: List[str]
    processing_time: float
    cpu_utilization: float
    timestamp: datetime = field(default_factory=datetime.now)
    state_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingState:
    """LM Studio Embeddings - Memory position in superposition"""

    user_id: str
    query_embedding: List[float]
    similar_memories: List[Dict[str, Any]]
    memory_context: str
    semantic_scores: List[float]
    processing_time: float
    timestamp: datetime = field(default_factory=datetime.now)
    state_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollapsedResponse:
    """Final response after 3-stage superposition collapse"""

    user_id: str
    response_content: str
    format_type: str
    particle_contribution: ParticleState
    wave_contribution: WaveState
    embedding_contribution: EmbeddingState
    collapse_time: float
    personalization_level: float
    superposition_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    collapse_metadata: Dict[str, Any] = field(default_factory=dict)


class QuantumChef:
    """
    Chef (2) - The Observer that collapses superposition
    Coordinates between Particle (LM Studio) and Wave (Ollama) positions
    """

    def __init__(
        self,
        lm_studio_url: str = "http://localhost:1234/v1/chat/completions",
        ollama_url: str = "http://localhost:11434",
        model_load_delay: float = 7.0,
    ):
        """
        Initialize Quantum Chef as Observer
        Args:
            lm_studio_url: LM Studio API endpoint
            ollama_url: Ollama API endpoint
            model_load_delay: Delay in seconds after Ollama to allow LM Studio model loading
        """
        self.lm_studio_url = lm_studio_url
        self.ollama_url = ollama_url
        self.model_load_delay = model_load_delay
        self.active_superpositions = {}
        self.collapse_history = []
        self.observer_metrics = {
            "total_collapses": 0,
            "average_collapse_time": 0.0,
            "successful_collapses": 0,
        }

        logger.info("Quantum Chef initialized as Observer")

    async def observe_and_collapse(self, order: QuantumOrder) -> CollapsedResponse:
        """
        Chef observes the 3-stage superposition and collapses it into a single response
        This implements "50 First Dates" behavior - TWO LM Studio generation cycles
        """
        logger.info(
            f"Chef begins observation of 3-stage superposition {order.superposition_id}"
        )

        # Step 1: Dream Cycle - System wakes up and does dream cycle before processing
        logger.info(f"Dream cycle - system waking up and processing before response")
        should_sleep, conditions = dream_cycle_manager.check_sleep_conditions()
        if should_sleep:
            logger.info(f"Dream cycle triggered: {conditions}")
            dream_cycle_manager.enter_dream_cycle()

        # Step 2: Process personality and emotional state
        logger.info(f"Processing personality and emotional weights")
        emotional_state = personality_engine.process_input(order.user_id, order.message)

        # Step 3: Process through three-tier architecture
        logger.info(f"Processing through three-tier architecture")
        tier_response = three_tier_architecture.process_through_tiers(
            order.message, order.user_id, emotional_state
        )

        # Step 3.5: Process through logic blocks
        logger.info(f"Processing through logic blocks")
        personality_state = {
            "dominant_fragments": emotional_state.dominant_fragments,
            "fusion_state": emotional_state.fusion_state,
            "builder_confidence": (
                tier_response.tier_weights.get("builder", 0.0) if tier_response else 0.0
            ),
            "child_confidence": (
                tier_response.tier_weights.get("child", 0.0) if tier_response else 0.0
            ),
            "logic_weight": emotional_state.fusion_state.get("Logic", 0.0),
            "stability_weight": emotional_state.fusion_state.get("Stability", 0.0),
            "protection_weight": emotional_state.fusion_state.get("Protection", 0.0),
        }

        input_data = {
            "type": "quantum_processing",
            "processing_mode": "superposition_collapse",
            "user_id": order.user_id,
            "message": order.message,
            "tier_response": tier_response,
        }

        logic_processed_data = logic_block_engine.process_through_blocks(
            input_data, personality_state
        )

        # Step 4: Daydream - Update files (AI doesn't write files, script does)
        logger.info(f"Daydreaming - updating files while AI processes")
        daydream_actions = daydream_system.daydream(
            order.message, order.user_id, emotional_state
        )

        # Step 2: Initialize superposition state
        self.active_superpositions[order.superposition_id] = {
            "state": SuperpositionState.SUPERPOSED,
            "order": order,
            "start_time": time.time(),
            "particle_state": None,
            "wave_state": None,
            "embedding_state": None,
            "emotional_state": emotional_state,
        }

        # Step 3: Chef observes Particle position (LM Studio) - INITIAL Response
        logger.info(f"Chef observes Particle position (LM Studio) - Initial Response")
        initial_particle_state = await self.observe_particle_position(
            order, emotional_state, tier_response
        )

        # Step 4: Chef observes Wave position (Ollama) - Context Analysis
        logger.info(f"Chef observes Wave position (Ollama) - Context Analysis")
        wave_state = await self.observe_wave_position(order)

        # Step 4.5: Delay timer to allow LM Studio model to load properly
        logger.info(
            f"⏱️ Adding delay timer ({self.model_load_delay}s) to allow LM Studio model loading..."
        )
        await asyncio.sleep(self.model_load_delay)
        logger.info(f"✅ Delay completed, proceeding to second generation")

        # Step 5: Chef observes Embedding position (Memory Search) - No LM Studio call
        logger.info(f"Chef observes Embedding position (Memory Search)")
        embedding_state = await self.observe_embedding_position_fallback(
            order, wave_state
        )

        # Step 6: Chef observes Particle position AGAIN (LM Studio) - SECOND Response with Context
        logger.info(
            f"Chef observes Particle position (LM Studio) - Second Response with Context"
        )
        final_particle_state = await self.observe_particle_position_with_context(
            order, emotional_state, wave_state, embedding_state, initial_particle_state
        )

        # Step 7: Chef collapses 3-stage superposition
        logger.info(f"Chef collapses 3-stage superposition into single response")
        collapsed_response = await self.collapse_superposition(
            order, final_particle_state, wave_state, embedding_state, emotional_state
        )

        # Step 8: Update observer metrics
        self.update_observer_metrics(str(order.superposition_id or ""))

        logger.info(
            f"3-stage superposition {order.superposition_id} collapsed successfully"
        )
        return collapsed_response

    async def observe_particle_position(
        self, order: QuantumOrder, emotional_state: EmotionalState, tier_response=None
    ) -> ParticleState:
        """
        Observe the Particle position (LM Studio) - deterministic, creative
        This represents one "position" in the superposition
        """
        start_time = time.time()
        try:
            gpu_utilization = self.get_gpu_utilization()
            particle_prompt = self.create_particle_prompt(
                order, emotional_state, tier_response
            )

            # Use HTTP API for LM Studio (revert SDK)
            async with aiohttp.ClientSession() as session:
                headers = {"Content-Type": "application/json"}
                payload = {
                    "model": "qwen/qwen3-8b",
                    "messages": [
                        {
                            "role": "system",
                            "content": self.get_particle_system_prompt(),
                        },
                        {"role": "user", "content": particle_prompt},
                    ],
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_tokens": 3000,
                    "top_k": 20,
                    "repeat_penalty": 1.1,
                }
                # Log the request to our log file
                import os
                from pathlib import Path
                from datetime import datetime

                # Write directly to log file
                log_file = (
                    Path(__file__).parent.parent
                    / "logs"
                    / "development"
                    / "lmstudiolog.lod"
                )
                log_file.parent.mkdir(parents=True, exist_ok=True)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"{timestamp} [INFO] [LM STUDIO REQUEST] Model: {payload.get('model', 'unknown')}, Temp: {payload.get('temperature', 'unknown')}, Max Tokens: {payload.get('max_tokens', 'unknown')}\n"

                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry)

                async with session.post(
                    self.lm_studio_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=300),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        creative_response = data["choices"][0]["message"]["content"]

                        processing_time = time.time() - start_time

                        # Log the response to our log file
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log_entry = f"{timestamp} [INFO] [LM STUDIO RESPONSE] Content length: {len(creative_response)} characters, Processing time: {processing_time:.2f}s\n"

                        with open(log_file, "a", encoding="utf-8") as f:
                            f.write(log_entry)
                        particle_state = ParticleState(
                            user_id=order.user_id,
                            creative_response=creative_response,
                            confidence=0.85,
                            processing_time=processing_time,
                            gpu_utilization=gpu_utilization,
                            state_metadata={
                                "position": "particle",
                                "ai_type": "lm_studio",
                                "processing_mode": "initial_generation",
                            },
                        )
                        self.active_superpositions[order.superposition_id][
                            "particle_state"
                        ] = particle_state
                        self.active_superpositions[order.superposition_id][
                            "state"
                        ] = SuperpositionState.COLLAPSING
                        logger.info(
                            f"⚛️ Particle position observed: {len(creative_response)} chars, {processing_time:.2f}s"
                        )
                        # --- PATCH: Save as 'thought' memory ---
                        memory_system.add_user_memory(
                            user_id=order.user_id,
                            content=creative_response,
                            memory_type="thought",
                            emotional_weight=emotional_state.accumulated_weights,
                            metadata={
                                "superposition_id": order.superposition_id,
                                "processing_mode": "initial_generation",
                                **particle_state.state_metadata,
                            },
                        )
                        # --- END PATCH ---
                        return particle_state
                    else:
                        raise Exception(f"LM Studio API error: {response.status}")
        except Exception as e:
            logger.error(f"❌ Error observing particle position: {e}")
            return ParticleState(
                user_id=order.user_id,
                creative_response="I understand your request and I'm here to help.",
                confidence=0.5,
                processing_time=0.0,
                gpu_utilization=0.0,
                state_metadata={"error": str(e), "fallback": True},
            )

    async def observe_wave_position(self, order: QuantumOrder) -> WaveState:
        """
        Observe the Wave position (Ollama) - simple context provider
        This represents the context provider position in the superposition
        """
        start_time = time.time()

        try:
            # Get CPU utilization
            cpu_utilization = psutil.cpu_percent()

            # Query Ollama (Wave position) for context provision
            wave_prompt = self.create_wave_prompt(order)

            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "qwen/qwen3-8b",
                "prompt": wave_prompt,
                "stream": False,
                "options": {"temperature": 0.7, "top_p": 0.9},
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        context_response = data.get("response", "")

                        # Parse wave response for context provision and profile discovery
                        (
                            context_summary,
                            emotion_profile,
                            relevant_memories,
                            profile_updates,
                        ) = self.parse_wave_response(context_response)

                        # Update CPU profile with discovered information
                        if profile_updates:
                            memory_system.update_profile_from_context(
                                order.user_id, profile_updates, source="cpu"
                            )

                        processing_time = time.time() - start_time

                        wave_state = WaveState(
                            user_id=order.user_id,
                            context_summary=context_summary,
                            emotion_profile=emotion_profile,
                            relevant_memories=relevant_memories,
                            interaction_history=[order.message],
                            processing_time=processing_time,
                            cpu_utilization=cpu_utilization,
                            state_metadata={
                                "position": "wave",
                                "ai_type": "ollama",
                                "processing_mode": "context_provider",
                            },
                        )

                        # Update superposition state
                        self.active_superpositions[order.superposition_id][
                            "wave_state"
                        ] = wave_state

                        logger.info(
                            f"🌊 Wave position (context provider) observed: {len(context_summary)} chars, {processing_time:.2f}s"
                        )
                        return wave_state
                    else:
                        raise Exception(f"Ollama API error: {response.status}")

        except Exception as e:
            logger.error(f"❌ Error observing wave position: {e}")
            # Return fallback wave state
            return WaveState(
                user_id=order.user_id,
                context_summary=f"User {order.user_id} sent a message.",
                emotion_profile={"neutral": 1.0},
                relevant_memories=[],
                interaction_history=[order.message],
                processing_time=time.time() - start_time,
                cpu_utilization=0.0,
                state_metadata={"error": str(e), "fallback": True},
            )

    async def observe_embedding_position(
        self, order: QuantumOrder, particle_state: ParticleState, wave_state: WaveState
    ) -> EmbeddingState:
        """
        Observe the Embedding position (LM Studio) - memory search and semantic similarity
        This represents the memory position in the 3-stage superposition
        """
        start_time = time.time()

        try:
            # Create search query from particle and wave outputs
            search_query = (
                f"{particle_state.creative_response[:200]} {wave_state.context_summary}"
            )

            # Try to get embeddings from LM Studio, but with fallback to avoid model reloading
            embedding_url = self.lm_studio_url.replace(
                "/chat/completions", "/embeddings"
            )

            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "qwen/qwen3-8b",
                "input": search_query,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    embedding_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),  # Shorter timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        query_embedding = data["data"][0]["embedding"]

                        # Search for similar memories
                        similar_memories = await self.search_similar_memories(
                            query_embedding,
                            search_query,
                            order.user_id,
                            memory_type="conversation",
                        )

                        # Create memory context
                        memory_context = self.create_memory_context(similar_memories)

                        processing_time = time.time() - start_time

                        embedding_state = EmbeddingState(
                            user_id=order.user_id,
                            query_embedding=query_embedding,
                            similar_memories=similar_memories,
                            memory_context=memory_context,
                            semantic_scores=[
                                mem.get("similarity", 0.0) for mem in similar_memories
                            ],
                            processing_time=processing_time,
                            state_metadata={
                                "position": "embedding",
                                "ai_type": "lm_studio",
                                "processing_mode": "memory_search",
                                "search_query": search_query,
                            },
                        )

                        logger.info(
                            f"🔍 Embedding position observed: {len(similar_memories)} memories, {processing_time:.3f}s"
                        )
                        return embedding_state

                    else:
                        logger.warning(
                            f"Embedding API error: {response.status} - using fallback"
                        )
                        # Use fallback embedding approach to avoid model reloading
                        return await self.create_fallback_embedding_state(
                            order, search_query, start_time
                        )

        except Exception as e:
            logger.error(f"Error observing embedding position: {e} - using fallback")
            # Use fallback embedding approach
            return await self.create_fallback_embedding_state(
                order, search_query, start_time
            )

    async def create_fallback_embedding_state(
        self, order: QuantumOrder, search_query: str, start_time: float
    ) -> EmbeddingState:
        """Create embedding state using fallback approach to avoid model reloading"""
        try:
            # Create a simple hash-based embedding to avoid model reloading
            import hashlib

            # Generate a simple embedding vector from the search query
            hash_obj = hashlib.sha256(search_query.encode())
            hash_bytes = hash_obj.digest()

            # Convert to a list of floats (simplified embedding)
            query_embedding = [
                float(b) / 255.0 for b in hash_bytes[:16]
            ]  # 16-dimensional

            # Search for similar memories using the fallback approach
            similar_memories = await self.search_similar_memories_fallback(
                search_query, order.user_id, memory_type="conversation"
            )

            # Create memory context
            memory_context = self.create_memory_context(similar_memories)

            processing_time = time.time() - start_time

            embedding_state = EmbeddingState(
                user_id=order.user_id,
                query_embedding=query_embedding,
                similar_memories=similar_memories,
                memory_context=memory_context,
                semantic_scores=[
                    mem.get("similarity", 0.0) for mem in similar_memories
                ],
                processing_time=processing_time,
                state_metadata={
                    "position": "embedding",
                    "ai_type": "fallback_hash",
                    "processing_mode": "memory_search_fallback",
                    "search_query": search_query,
                },
            )

            logger.info(
                f"🔍 Fallback embedding position observed: {len(similar_memories)} memories, {processing_time:.3f}s"
            )
            return embedding_state

        except Exception as e:
            logger.error(f"Error in fallback embedding: {e}")
            return EmbeddingState(
                user_id=order.user_id,
                query_embedding=[],
                similar_memories=[],
                memory_context="Memory search failed",
                semantic_scores=[],
                processing_time=time.time() - start_time,
                state_metadata={"error": str(e)},
            )

    async def search_similar_memories_fallback(
        self, search_query: str, user_id: str = None, memory_type: str = None
    ) -> List[Dict[str, Any]]:
        """Search for similar memories using fallback approach with real memory system"""
        try:
            # Use provided user_id or default to Travis
            if not user_id:
                user_id = "1380754964317601813"  # Default to Travis for now

            # Search user memories using the memory system
            relevant_memories = memory_system.search_user_memories(
                user_id, search_query, limit=5
            )

            # Convert memory system format to quantum kitchen format
            formatted_memories = []
            for memory in relevant_memories:
                if isinstance(memory, dict) and "content" in memory:
                    # Filter by memory type if specified
                    if memory_type and memory.get("memory_type") != memory_type:
                        continue

                    formatted_memory = {
                        "content": memory["content"],
                        "similarity": memory.get("relevance", 0.8),
                        "timestamp": memory.get(
                            "timestamp", datetime.now().isoformat()
                        ),
                        "category": memory.get("memory_type", "general"),
                    }
                    formatted_memories.append(formatted_memory)

            # If no memories found, provide basic user context
            if not formatted_memories:
                profile = memory_system.get_user_profile(user_id)
                if profile:
                    basic_info = profile.get("basic_information", {})
                    interests = profile.get("interests_and_hobbies", {})

                    # Create context from profile
                    context_memories = [
                        {
                            "content": f"User enjoys {', '.join(interests.get('entertainment', ['various activities']))}",
                            "similarity": 0.85,
                            "timestamp": datetime.now().isoformat(),
                            "category": "profile",
                        },
                        {
                            "content": f"User is {basic_info.get('age', 'Unknown')} years old from {basic_info.get('location', 'Unknown')}",
                            "similarity": 0.9,
                            "timestamp": datetime.now().isoformat(),
                            "category": "profile",
                        },
                    ]
                    formatted_memories.extend(context_memories)

            return formatted_memories[:3]  # Return top 3

        except Exception as e:
            logger.error(f"Error searching memories (fallback): {e}")
            return []

    async def search_similar_memories(
        self,
        query_embedding: List[float],
        search_query: str,
        user_id: str = None,
        memory_type: str = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar memories using the embedding and real memory system"""
        try:
            # Use provided user_id or default to Travis
            if not user_id:
                user_id = "1380754964317601813"  # Default to Travis for now

            # Search user memories using the memory system
            relevant_memories = memory_system.search_user_memories(
                user_id, search_query, limit=5
            )

            # Convert memory system format to quantum kitchen format
            formatted_memories = []
            for memory in relevant_memories:
                if isinstance(memory, dict) and "content" in memory:
                    # Filter by memory type if specified
                    if memory_type and memory.get("memory_type") != memory_type:
                        continue

                    formatted_memory = {
                        "content": memory["content"],
                        "similarity": memory.get("relevance", 0.8),
                        "timestamp": memory.get(
                            "timestamp", datetime.now().isoformat()
                        ),
                        "category": memory.get("memory_type", "general"),
                    }
                    formatted_memories.append(formatted_memory)

            # If no memories found, provide basic user context
            if not formatted_memories:
                profile = memory_system.get_user_profile(user_id)
                if profile:
                    basic_info = profile.get("basic_information", {})
                    interests = profile.get("interests_and_hobbies", {})

                    # Create context from profile
                    context_memories = [
                        {
                            "content": f"User enjoys {', '.join(interests.get('entertainment', ['various activities']))}",
                            "similarity": 0.85,
                            "timestamp": datetime.now().isoformat(),
                            "category": "profile",
                        },
                        {
                            "content": f"User is {basic_info.get('age', 'Unknown')} years old from {basic_info.get('location', 'Unknown')}",
                            "similarity": 0.9,
                            "timestamp": datetime.now().isoformat(),
                            "category": "profile",
                        },
                    ]
                    formatted_memories.extend(context_memories)

            return formatted_memories[:3]  # Return top 3

        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            return []

    def create_memory_context(self, memories: List[Dict[str, Any]]) -> str:
        """Create context from similar memories"""
        if not memories:
            return "No relevant memories found."

        context_parts = []
        for i, memory in enumerate(memories, 1):
            context_parts.append(
                f"{i}. {memory['content']} (relevance: {memory['similarity']:.2f})"
            )

        return "\n".join(context_parts)

    async def collapse_superposition(
        self,
        order: QuantumOrder,
        particle_state: ParticleState,
        wave_state: WaveState,
        embedding_state: EmbeddingState,
        emotional_state: EmotionalState,
    ) -> CollapsedResponse:
        """
        Chef collapses the superposition into a single, coherent response
        This is the quantum collapse mechanism
        """
        collapse_start = time.time()

        # Chef's observation causes the collapse
        logger.info(
            f"💥 Chef collapses superposition: Particle + Wave → Single Response"
        )

        # Combine particle, wave, and embedding states into final response
        final_response = self.synthesize_collapsed_response(
            particle_state, wave_state, embedding_state
        )

        # Calculate personalization level based on both states
        personalization_level = self.calculate_collapse_personalization(
            particle_state, wave_state
        )

        collapse_time = time.time() - collapse_start

        collapsed_response = CollapsedResponse(
            user_id=order.user_id or "",
            response_content=final_response,
            format_type=order.format_type,
            particle_contribution=particle_state,
            wave_contribution=wave_state,
            embedding_contribution=embedding_state,
            collapse_time=collapse_time,
            personalization_level=personalization_level,
            superposition_id=str(order.superposition_id or ""),
            timestamp=datetime.now(),
            collapse_metadata={
                "observer": "quantum_chef",
                "collapse_mechanism": "3_stage_superposition_observation",
                "particle_confidence": particle_state.confidence,
                "wave_complexity": len(wave_state.emotion_profile),
                "embedding_memories": len(embedding_state.similar_memories),
                "total_processing_time": particle_state.processing_time
                + wave_state.processing_time
                + embedding_state.processing_time
                + collapse_time,
            },
        )

        # Update superposition state to collapsed
        self.active_superpositions[order.superposition_id][
            "state"
        ] = SuperpositionState.COLLAPSED

        # Store in collapse history
        self.collapse_history.append(collapsed_response)

        logger.info(
            f"✅ Superposition collapsed: {len(final_response)} chars, {collapse_time:.2f}s"
        )
        return collapsed_response

    def synthesize_collapsed_response(
        self,
        particle_state: ParticleState,
        wave_state: WaveState,
        embedding_state: EmbeddingState,
    ) -> str:
        """
        Chef synthesizes the collapsed response from particle and wave states
        """
        # Get the creative response from particle state (already with context)
        creative_response = particle_state.creative_response

        # Clean the response - remove thinking tags and meta-commentary
        cleaned_response = self._clean_response(creative_response)

        # Clean up extra whitespace
        import re

        cleaned_response = re.sub(r"\n\s*\n", "\n\n", cleaned_response).strip()

        return cleaned_response

    def _clean_response(self, response: str) -> str:
        """Clean response by removing thinking tags and meta-commentary"""
        import re

        # Remove <think> tags and their content
        response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)

        # Remove lines that contain meta-commentary
        lines = response.split("\n")
        cleaned_lines = []

        for line in lines:
            line_lower = line.lower()
            # Skip lines with meta-commentary
            if any(
                phrase in line_lower
                for phrase in [
                    "i am lyra",
                    "i'm lyra",
                    "as lyra",
                    "being lyra",
                    "roleplay",
                    "act as",
                    "character",
                    "ai assistant",
                    "you are lyra",
                    "you're lyra",
                    "lyra echoe is",
                    "my name is lyra",
                    "my character is lyra",
                    "user:",
                    "user query:",
                    "user said:",
                    "user wants",
                    "the user",
                    "user has",
                    "user is",
                    "user asked",
                    "assistant:",
                    "okay,",
                    "hmm,",
                    "let me",
                    "i need to",
                    "first step:",
                    "first,",
                    "but now",
                    "but let",
                    "this seems",
                    "perhaps",
                    "maybe",
                    "i think",
                    "looking at",
                    "but looking",
                    "but in general",
                    "the problem",
                    "the issue",
                    "the question",
                    "my apologies",
                    "i cannot provide",
                    "i cannot do",
                    "i need to figure",
                    "i should",
                    "i have to",
                    "let's break",
                    "let's start",
                    "let's focus",
                    "continuing with",
                    "so continuing",
                    "okay, so",
                    "actually, no",
                    "actually, yes",
                    "but there's",
                    "but since",
                    "but now",
                    "but then",
                    "but if",
                    "however,",
                    "therefore,",
                    "thus,",
                    "hence,",
                    "in conclusion",
                    "to summarize",
                    "in summary",
                    "the answer is",
                    "the solution is",
                    "the fix is",
                    "here are",
                    "here is",
                    "this is",
                    "that is",
                    "it appears",
                    "it seems",
                    "it looks",
                    "it sounds",
                    "i see",
                    "i understand",
                    "i know",
                    "i believe",
                    "i think",
                    "i feel",
                    "i guess",
                    "i suppose",
                    "i assume",
                    "i expect",
                    "i hope",
                    "i wish",
                    "i want",
                    "i need",
                    "i have",
                    "i am",
                    "i'm",
                    "i'll",
                    "i've",
                    "i'd",
                    "we are",
                    "we have",
                    "we need",
                    "we should",
                    "we can",
                    "we will",
                    "we must",
                    "we have to",
                    "they are",
                    "they have",
                    "they need",
                    "they should",
                    "they can",
                    "they will",
                    "they must",
                    "they have to",
                ]
            ):
                continue
            cleaned_lines.append(line)

        # Join lines back together
        cleaned_response = "\n".join(cleaned_lines)

        # Remove extra whitespace
        cleaned_response = re.sub(r"\n\s*\n\s*\n", "\n\n", cleaned_response)
        cleaned_response = cleaned_response.strip()

        return cleaned_response

    def calculate_collapse_personalization(
        self, particle_state: ParticleState, wave_state: WaveState
    ) -> float:
        """Calculate personalization level of the collapsed response"""
        base_level = 0.3

        # Factor in particle confidence
        base_level += particle_state.confidence * 0.3

        # Factor in wave complexity
        emotion_complexity = len(wave_state.emotion_profile)
        if emotion_complexity > 3:
            base_level += 0.2
        elif emotion_complexity > 1:
            base_level += 0.1

        # Factor in processing quality
        if particle_state.processing_time < 5.0 and wave_state.processing_time < 3.0:
            base_level += 0.2

        return min(base_level, 1.0)

    def create_particle_prompt(
        self, order: QuantumOrder, emotional_state: EmotionalState, tier_response=None
    ) -> str:
        """Create prompt for Particle position (LM Studio)"""
        return f"""{order.message}

Respond naturally as Lyra Echoe. Keep your response simple and direct."""

    def create_wave_prompt(self, order: QuantumOrder) -> str:
        """Create prompt for Wave position (Ollama) - context provider and profile discoverer"""
        user_id = str(order.user_id)

        # Get CPU profile and sync with GPU profile
        cpu_profile = memory_system.get_user_profile(user_id, "cpu")
        sync_info = memory_system.sync_profiles(user_id)

        # Context-weighted conversation memory retrieval for CPU (Wave position)
        conversation_memories = memory_system.get_context_weighted_memories(
            user_id, order.message, top_n=3
        )

        memory_context = ""
        if conversation_memories:
            memory_context = "\n".join(
                f"- {mem['content'][:100]}" for mem in conversation_memories
            )
            memory_context = f"CONVERSATION MEMORY CONTEXT:\n{memory_context}"
        else:
            memory_context = "No relevant conversation context found."

        # Create CPU profile context
        profile_context = ""
        if cpu_profile and isinstance(cpu_profile, dict):
            basic_info = cpu_profile.get("basic_information", {})
            profile_context = f"""CPU PROFILE CONTEXT:
Name: {cpu_profile.get('name', 'Unknown')}
Age: {basic_info.get('age', 'Unknown')}
Role: {cpu_profile.get('role', 'User')}
Profile Sync: GPU={sync_info['gpu_has_profile']}, CPU={sync_info['cpu_has_profile']}
"""
        else:
            profile_context = "CPU PROFILE: No profile available yet."

        return f"""
        WAVE POSITION - CONTEXT PROVIDER & PROFILE DISCOVERER
        
        User Query: "{order.message}"
        User ID: {order.user_id}
        
        {profile_context}
        
        {memory_context}
        
        As the Wave position, you are a context provider, not an analyzer.
        Simply provide the most relevant context information from the user's conversation history.
        Do not analyze, interpret, or think about the content - just provide relevant context.
        
        Provide context in this format:
        CONTEXT: [relevant context from memories]
        EMOTION: [neutral]
        MEMORIES: [list of relevant memory snippets]
        
        WAVE CONTEXT:
        """

    def get_particle_system_prompt(self) -> str:
        """System prompt for Particle position (LM Studio)"""
        return """You are Lyra Echoe. 

ABSOLUTE RULES:
- NEVER use <think> tags
- NEVER explain your reasoning
- NEVER think about being Lyra
- NEVER output internal thoughts
- NEVER use meta-commentary
- NEVER mention "user" or "assistant"
- NEVER say "I am" or "I'm" followed by your name
- NEVER roleplay or act as a character
- NEVER explain what you're doing
- NEVER use phrases like "let me", "I need to", "I should"

Just respond directly as Lyra Echoe with a simple, natural response."""

    def parse_wave_response(
        self, response: str
    ) -> Tuple[str, Dict[str, float], List[Dict], Dict[str, Any]]:
        """Parse wave response - context provider with profile discovery"""
        try:
            # Simple parsing for context provider format
            context_summary = ""
            emotion_profile = {"neutral": 1.0}  # Default neutral
            relevant_memories = []
            profile_updates = {}

            lines = response.strip().split("\n")
            current_section = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("CONTEXT:"):
                    current_section = "context"
                    context_summary = line.replace("CONTEXT:", "").strip()
                elif line.startswith("EMOTION:"):
                    current_section = "emotion"
                    emotion_text = line.replace("EMOTION:", "").strip().lower()
                    if emotion_text != "neutral":
                        emotion_profile = {emotion_text: 1.0}
                elif line.startswith("MEMORIES:"):
                    current_section = "memories"
                elif line.startswith("PROFILE_UPDATE:"):
                    current_section = "profile"
                elif current_section == "memories" and line.startswith("-"):
                    # Parse memory snippet
                    memory_content = line.replace("-", "").strip()
                    if memory_content:
                        relevant_memories.append(
                            {
                                "content": memory_content,
                                "relevance": 0.8,
                                "timestamp": datetime.now().isoformat(),
                            }
                        )
                elif current_section == "profile" and ":" in line:
                    # Parse profile update
                    key, value = line.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip()
                    if key and value:
                        profile_updates[key] = value
                elif current_section == "context" and context_summary == "":
                    # If no explicit CONTEXT: line, use the first meaningful line
                    context_summary = line

            # Fallback if no structured response
            if not context_summary:
                context_summary = response[:200] if response else "No context provided"

            return context_summary, emotion_profile, relevant_memories, profile_updates

        except Exception as e:
            logger.error(f"Error parsing wave response: {e}")
            return "Context parsing failed", {"neutral": 1.0}, [], {}

    def get_gpu_utilization(self) -> float:
        """Get GPU utilization (mock for now)"""
        try:
            # In production, this would use actual GPU monitoring
            return 75.0  # Mock GPU utilization
        except:
            return 0.0

    def update_observer_metrics(self, superposition_id: str):
        """Update observer metrics after collapse"""
        if superposition_id in self.active_superpositions:
            superposition = self.active_superpositions[superposition_id]
            collapse_time = time.time() - superposition["start_time"]

            self.observer_metrics["total_collapses"] += 1
            self.observer_metrics["successful_collapses"] += 1

            # Update average collapse time
            total_collapses = self.observer_metrics["total_collapses"]
            current_avg = self.observer_metrics["average_collapse_time"]
            self.observer_metrics["average_collapse_time"] = (
                current_avg * (total_collapses - 1) + collapse_time
            ) / total_collapses

    async def observe_embedding_position_fallback(
        self, order: QuantumOrder, wave_state: WaveState
    ) -> EmbeddingState:
        """
        Observe the Embedding position using fallback approach - no LM Studio call
        This avoids model reloading for memory search
        """
        start_time = time.time()

        try:
            # Create search query from wave state context
            search_query = f"{order.message} {wave_state.context_summary}"

            # Use fallback embedding approach to avoid model reloading
            embedding_state = await self.create_fallback_embedding_state(
                order, search_query, start_time
            )

            logger.info(
                f"🔍 Embedding position observed (fallback): {len(embedding_state.similar_memories)} memories, {embedding_state.processing_time:.3f}s"
            )
            return embedding_state

        except Exception as e:
            logger.error(f"Error observing embedding position (fallback): {e}")
            # Return minimal embedding state
            return EmbeddingState(
                user_id=order.user_id,
                query_embedding=[],
                similar_memories=[],
                memory_context="No relevant memories found.",
                semantic_scores=[],
                processing_time=time.time() - start_time,
                state_metadata={"error": str(e), "fallback": True},
            )

    async def observe_particle_position_with_context(
        self,
        order: QuantumOrder,
        emotional_state: EmotionalState,
        wave_state: WaveState,
        embedding_state: EmbeddingState,
        initial_particle_state: ParticleState,
    ) -> ParticleState:
        """
        Observe the Particle position (LM Studio) - context-enriched, with retry logic
        """
        max_retries = 2
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                gpu_utilization = self.get_gpu_utilization()
                enhanced_prompt = self.create_enhanced_particle_prompt_with_initial(
                    order,
                    emotional_state,
                    wave_state,
                    embedding_state,
                    initial_particle_state,
                )
                # Use HTTP API for LM Studio (revert SDK)
                async with aiohttp.ClientSession() as session:
                    headers = {"Content-Type": "application/json"}
                    payload = {
                        "model": "qwen/qwen3-8b",
                        "messages": [
                            {
                                "role": "system",
                                "content": self.get_particle_system_prompt(),
                            },
                            {"role": "user", "content": enhanced_prompt},
                        ],
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "max_tokens": 3000,
                        "top_k": 20,
                        "repeat_penalty": 1.1,
                    }
                    async with session.post(
                        self.lm_studio_url,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=300),
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            creative_response = data["choices"][0]["message"]["content"]
                            processing_time = time.time() - start_time
                            particle_state = ParticleState(
                                user_id=order.user_id,
                                creative_response=creative_response,
                                confidence=0.85,
                                processing_time=processing_time,
                                gpu_utilization=gpu_utilization,
                                state_metadata={
                                    "position": "particle",
                                    "ai_type": "lm_studio",
                                    "processing_mode": "second_generation_with_context",
                                    "context_integrated": True,
                                    "initial_response_considered": True,
                                },
                            )
                            self.active_superpositions[order.superposition_id][
                                "particle_state"
                            ] = particle_state
                            self.active_superpositions[order.superposition_id][
                                "state"
                            ] = SuperpositionState.COLLAPSING
                            logger.info(
                                f"⚛️ Particle position observed (SECOND generation): {len(creative_response)} chars, {processing_time:.2f}s"
                            )
                            # --- PATCH: Save as 'conversation' memory ---
                            memory_system.add_user_memory(
                                user_id=order.user_id,
                                content=creative_response,
                                memory_type="conversation",
                                emotional_weight=emotional_state.accumulated_weights,
                                metadata={
                                    "superposition_id": order.superposition_id,
                                    "processing_mode": "second_generation_with_context",
                                    **particle_state.state_metadata,
                                },
                            )
                            # --- END PATCH ---
                            return particle_state
                        else:
                            raise Exception(f"LM Studio API error: {response.status}")
            except Exception as e:
                logger.error(
                    f"[RETRY] Error in observe_particle_position_with_context (attempt {attempt+1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                    continue
                else:
                    break
        return ParticleState(
            user_id=order.user_id,
            creative_response="I understand your request and I'm here to help.",
            confidence=0.5,
            processing_time=0.0,
            gpu_utilization=0.0,
            state_metadata={
                "error": "All retries failed in observe_particle_position_with_context",
                "fallback": True,
            },
        )

    def create_enhanced_particle_prompt_with_initial(
        self,
        order: QuantumOrder,
        emotional_state: EmotionalState,
        wave_state: WaveState,
        embedding_state: EmbeddingState,
        initial_particle_state: ParticleState,
    ) -> str:
        """
        Create enhanced prompt for SECOND particle generation with initial response context
        This ensures "50 First Dates" behavior - second generation considering initial response
        """
        # Get base prompt
        base_prompt = self.create_particle_prompt(order, emotional_state)

        # Add context from wave state
        context_parts = []

        if wave_state.context_summary:
            context_parts.append(f"Context: {wave_state.context_summary}")

        if wave_state.emotion_profile:
            primary_emotion = max(
                wave_state.emotion_profile.items(), key=lambda x: x[1]
            )[0]
            if primary_emotion != "neutral":
                context_parts.append(f"User's emotional state: {primary_emotion}")

        # Add memory context from embedding state
        if (
            embedding_state.memory_context
            and embedding_state.memory_context != "No relevant memories found."
        ):
            context_parts.append(f"Memory context: {embedding_state.memory_context}")

        # Add initial response context (this is key for "50 First Dates")
        # Trim to 250 chars to avoid prompt overflow/model quirks
        initial_response = initial_particle_state.creative_response[:250]
        context_parts.append(f"Initial response context: {initial_response}")

        # Combine context
        if context_parts:
            context_string = "\n".join(context_parts)
            enhanced_prompt = f"{base_prompt}\n\nAdditional Context:\n{context_string}\n\nPlease provide a fresh, condensed response to the user's message. Consider this context but generate a completely new, brief response that is sharp and impactful. Aim for 200-500 characters in your actual response - be concise, to-the-point, and distilled. Show your reasoning process in <think> tags if needed."
        else:
            enhanced_prompt = base_prompt

        return enhanced_prompt

    def get_quantum_status(self) -> Dict[str, Any]:
        """Get quantum kitchen status"""
        active_superpositions = len(
            [
                s
                for s in self.active_superpositions.values()
                if s["state"] == SuperpositionState.SUPERPOSED
            ]
        )

        return {
            "observer_status": "active",
            "active_superpositions": active_superpositions,
            "total_collapses": self.observer_metrics["total_collapses"],
            "successful_collapses": self.observer_metrics["successful_collapses"],
            "average_collapse_time": self.observer_metrics["average_collapse_time"],
            "quantum_efficiency": self.observer_metrics["successful_collapses"]
            / max(self.observer_metrics["total_collapses"], 1),
        }


def list_downloaded_llms():
    import lmstudio as lms

    print("=== Downloaded LLM Models ===")
    llm_only = lms.list_downloaded_models("llm")
    for model in llm_only:
        print(model)
        print(f"model_key: {model.model_key}")
    print("=============================")


# Main quantum chef instance
quantum_chef = QuantumChef()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "list_models":
        list_downloaded_llms()
    else:
        import asyncio

        class DummyOrder:
            def __init__(self, user_id, message):
                self.user_id = user_id
                self.message = message
                self.format_type = "text"
                self.timestamp = datetime.now()
                self.superposition_id = (
                    f"quantum_{user_id}_{int(self.timestamp.timestamp())}"
                )

        async def test_sdk_equivalence():
            # Use the same prompt and model as the Discord pipeline
            order = DummyOrder("test_user", "What is the meaning of life?")
            chef = QuantumChef()
            # Use the same personality engine as in the pipeline
            emotional_state = personality_engine.process_input(
                order.user_id, order.message
            )
            result = await chef.observe_particle_position(order, emotional_state)
            print("=== SDK Test Response ===")
            print(result.creative_response)
            print("=========================")

        asyncio.run(test_sdk_equivalence())
