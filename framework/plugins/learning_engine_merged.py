#!/usr/bin/env python3
"""
BULMA HEADER PROTOCOL - FRAMEWORK/PLUGINS/LEARNING_ENGINE_MERGED.PY
====================================================================

FILE IDENTITY:
- Name: Merged Learning Engine Plugin for Authoring Bot
- Role: Handles training data processing and advanced learning with personality evolution
- Purpose: Processes training data and implements advanced learning with reward/punishment system
- Location: framework/plugins/learning_engine_merged.py (Merged learning engine plugin)

BULMA USAGE PATTERNS:
- READ FIRST: This plugin handles all learning and training data processing
- MODIFICATIONS: Changes here affect learning quality and personality evolution
- TESTING: Test learning with various data sources and interaction patterns
- INTEGRATION: Works with Wikipedia dataset, Book Collection, and personality evolution

KEY COMPONENTS:
1. LearningEngine - Main learning engine class
2. TrainingDataProcessor - Wikipedia and book data processing
3. PersonalityEvolution - Advanced personality learning and evolution
4. RewardPunishmentSystem - Learning feedback and improvement
5. InteractionAnalysis - User interaction quality assessment
6. MessageModification - Text enhancement for better understanding
7. LearningStatistics - Comprehensive learning progress tracking

BULMA RESTRICTIONS:
- DO NOT modify learning algorithms without testing quality
- DO NOT change personality evolution without careful consideration
- ALWAYS test learning with various data sources
- CHECK that personality evolution remains appropriate
- VERIFY learning statistics and progress tracking

ALWAYS READ THIS HEADER BEFORE MODIFYING THIS FILE.
This plugin is critical for AI learning and personality development.
"""

import os
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Generator
from datetime import datetime, timedelta
import hashlib
import random
import threading
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

logger = logging.getLogger(__name__)


@dataclass
class TrainingChunk:
    """Represents a chunk of training data"""

    content: str
    source: str
    chunk_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class LearningStats:
    """Statistics for learning progress"""

    total_chunks_processed: int = 0
    total_words_processed: int = 0
    wikipedia_chunks: int = 0
    book_chunks: int = 0
    last_processed_date: Optional[datetime] = None
    processing_errors: List[str] = field(default_factory=list)


class LearningEngine:
    """Enhanced learning engine with training data processing and personality evolution"""

    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config

        # Basic learning stats
        self.stats = LearningStats()
        self.chunk_size = self.config.get("chunk_size", 1000)
        self.overlap_size = self.config.get("overlap_size", 200)
        self.max_workers = self.config.get("max_workers", 4)

        # Enhanced learning state
        self.learning_stats = {
            "total_interactions": 0,
            "successful_learnings": 0,
            "failed_learnings": 0,
            "personality_evolutions": 0,
            "reward_count": 0,
            "punishment_count": 0,
            "last_learning_date": None,
        }

        # Message modification patterns
        self.message_patterns = {
            "simplify": [
                (r"\bvery\s+", ""),
                (r"\bquite\s+", ""),
                (r"\bextremely\s+", ""),
                (r"\bdefinitely\s+", ""),
                (r"\bcertainly\s+", ""),
                (r"\bobviously\s+", ""),
                (r"\bclearly\s+", ""),
            ],
            "clarify": [
                (r"\bthing\b", "concept"),
                (r"\bstuff\b", "material"),
                (r"\bgood\b", "positive"),
                (r"\bbad\b", "negative"),
                (r"\bnice\b", "pleasant"),
                (r"\bcool\b", "interesting"),
            ],
            "expand": [
                (r"\bidea\b", "creative concept"),
                (r"\bstory\b", "narrative"),
                (r"\bcharacter\b", "story character"),
                (r"\bplot\b", "story plot"),
                (r"\bwriting\b", "creative writing"),
            ],
        }

        # Personality evolution tracking
        self.personality_evolution = {
            "base_traits": {
                "learning_enthusiasm": 0.8,
                "creative_expression": 0.9,
                "supportive_nature": 0.95,
                "inspirational_capacity": 0.9,
                "adaptability": 0.85,
                "emotional_intelligence": 0.8,
                "writing_expertise": 0.9,
                "motivational_ability": 0.95,
            },
            "evolution_history": [],
            "current_phase": "growth",
            "learning_milestones": [],
            "personality_evolutions": 0,
        }

        # Paths
        from core.config import Config

        self.wikipedia_path = Config.WIKIPEDIA_PATH
        self.book_collection_path = Config.BOOK_COLLECTION_PATH
        self.output_dir = Config.TRAINING_DATA_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.learning_dir = Config.MODELS_DIR / "learning"
        self.learning_dir.mkdir(parents=True, exist_ok=True)

        # Thread safety
        self.lock = threading.Lock()

        # Get other plugins
        try:
            self.personality_engine = framework.get_plugin("personality_engine")
            self.user_profile_manager = framework.get_plugin("user_profile_manager")
        except:
            self.personality_engine = None
            self.user_profile_manager = None

        # Load existing data
        self._load_stats()
        self._load_learning_data()

        logger.info("✅ Merged Learning Engine plugin initialized")

    def _load_stats(self):
        """Load existing learning statistics"""
        stats_file = self.output_dir / "learning_stats.json"
        if stats_file.exists():
            try:
                with open(stats_file, "r") as f:
                    data = json.load(f)
                    self.stats.total_chunks_processed = data.get(
                        "total_chunks_processed", 0
                    )
                    self.stats.total_words_processed = data.get(
                        "total_words_processed", 0
                    )
                    self.stats.wikipedia_chunks = data.get("wikipedia_chunks", 0)
                    self.stats.book_chunks = data.get("book_chunks", 0)
                    if data.get("last_processed_date"):
                        self.stats.last_processed_date = datetime.fromisoformat(
                            data["last_processed_date"]
                        )
            except Exception as e:
                logger.error(f"Error loading learning stats: {e}")

    def _save_stats(self):
        """Save learning statistics"""
        stats_file = self.output_dir / "learning_stats.json"
        data = {
            "total_chunks_processed": self.stats.total_chunks_processed,
            "total_words_processed": self.stats.total_words_processed,
            "wikipedia_chunks": self.stats.wikipedia_chunks,
            "book_chunks": self.stats.book_chunks,
            "last_processed_date": (
                self.stats.last_processed_date.isoformat()
                if self.stats.last_processed_date
                else None
            ),
        }
        with open(stats_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_learning_data(self):
        """Load existing learning data"""
        learning_file = self.learning_dir / "learning_data.json"
        if learning_file.exists():
            try:
                with open(learning_file, "r") as f:
                    data = json.load(f)
                    self.learning_stats.update(data.get("learning_stats", {}))
                    self.personality_evolution.update(
                        data.get("personality_evolution", {})
                    )
            except Exception as e:
                logger.error(f"Error loading learning data: {e}")

    def _save_learning_data(self):
        """Save learning data"""
        learning_file = self.learning_dir / "learning_data.json"
        data = {
            "learning_stats": self.learning_stats,
            "personality_evolution": self.personality_evolution,
        }
        with open(learning_file, "w") as f:
            json.dump(data, f, indent=2)

    def _create_chunk_id(self, content: str, source: str) -> str:
        """Create unique chunk ID"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        return f"{source}_{content_hash[:8]}"

    def _text_to_chunks(self, text: str, source: str) -> List[TrainingChunk]:
        """Convert text to training chunks"""
        chunks = []
        words = text.split()

        for i in range(0, len(words), self.chunk_size - self.overlap_size):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)

            if len(chunk_text.strip()) > 50:  # Minimum chunk size
                chunk = TrainingChunk(
                    content=chunk_text,
                    source=source,
                    chunk_id=self._create_chunk_id(chunk_text, source),
                    metadata={
                        "word_count": len(chunk_words),
                        "start_word": i,
                        "end_word": min(i + self.chunk_size, len(words)),
                    },
                )
                chunks.append(chunk)

        return chunks

    def _process_wikipedia_file(self, file_path: Path) -> List[TrainingChunk]:
        """Process a Wikipedia file into training chunks"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Clean Wikipedia content
            cleaned_content = self._clean_wikipedia_content(content)

            # Convert to chunks
            chunks = self._text_to_chunks(cleaned_content, str(file_path.name))

            return chunks

        except Exception as e:
            logger.error(f"Error processing Wikipedia file {file_path}: {e}")
            return []

    def _clean_wikipedia_content(self, content: str) -> str:
        """Clean Wikipedia content for training"""
        # Remove Wikipedia markup
        content = re.sub(r"\[\[.*?\]\]", "", content)  # Remove links
        content = re.sub(r"\{\{.*?\}\}", "", content)  # Remove templates
        content = re.sub(r"==.*?==", "", content)  # Remove headers
        content = re.sub(r"=.*?=", "", content)  # Remove headers
        content = re.sub(r"<.*?>", "", content)  # Remove HTML tags
        content = re.sub(r"&[a-zA-Z]+;", "", content)  # Remove HTML entities

        # Clean up whitespace
        content = re.sub(r"\s+", " ", content)
        content = content.strip()

        return content

    def _process_book_file(self, file_path: Path) -> List[TrainingChunk]:
        """Process a book file into training chunks"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Clean book content
            cleaned_content = self._clean_book_content(content)

            # Convert to chunks
            chunks = self._text_to_chunks(cleaned_content, str(file_path.name))

            return chunks

        except Exception as e:
            logger.error(f"Error processing book file {file_path}: {e}")
            return []

    def _clean_book_content(self, content: str) -> str:
        """Clean book content for training"""
        # Remove common book formatting
        content = re.sub(r"\n\s*\n", "\n", content)  # Remove extra newlines
        content = re.sub(r"\s+", " ", content)  # Normalize whitespace
        content = content.strip()

        return content

    def _save_chunks(self, chunks: List[TrainingChunk], batch_num: int):
        """Save training chunks to file"""
        output_file = self.output_dir / f"training_chunks_batch_{batch_num}.json"

        chunk_data = []
        for chunk in chunks:
            chunk_data.append(
                {
                    "content": chunk.content,
                    "source": chunk.source,
                    "chunk_id": chunk.chunk_id,
                    "metadata": chunk.metadata,
                    "created_date": chunk.created_date.isoformat(),
                }
            )

        with open(output_file, "w") as f:
            json.dump(chunk_data, f, indent=2)

    def process_wikipedia_dataset(self, max_files: Optional[int] = None) -> int:
        """Process Wikipedia dataset for training"""
        logger.info("🔄 Starting Wikipedia dataset processing...")

        if not self.wikipedia_path.exists():
            logger.error(f"Wikipedia path does not exist: {self.wikipedia_path}")
            return 0

        wikipedia_files = list(self.wikipedia_path.glob("*.txt"))
        if max_files:
            wikipedia_files = wikipedia_files[:max_files]

        total_chunks = 0
        batch_num = 1

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all files for processing
            future_to_file = {
                executor.submit(self._process_wikipedia_file, file_path): file_path
                for file_path in wikipedia_files
            }

            # Process completed files
            for future in tqdm(
                as_completed(future_to_file),
                total=len(wikipedia_files),
                desc="Processing Wikipedia files",
            ):
                file_path = future_to_file[future]
                try:
                    chunks = future.result()

                    with self.lock:
                        self.stats.wikipedia_chunks += len(chunks)
                        self.stats.total_chunks_processed += len(chunks)
                        self.stats.total_words_processed += sum(
                            len(chunk.content.split()) for chunk in chunks
                        )

                    # Save chunks in batches
                    if chunks:
                        self._save_chunks(chunks, batch_num)
                        batch_num += 1
                        total_chunks += len(chunks)

                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
                    with self.lock:
                        self.stats.processing_errors.append(str(e))

        self.stats.last_processed_date = datetime.now()
        self._save_stats()

        logger.info(
            f"✅ Wikipedia processing complete: {total_chunks} chunks processed"
        )
        return total_chunks

    def process_book_collection(self) -> int:
        """Process book collection for training"""
        logger.info("🔄 Starting book collection processing...")

        if not self.book_collection_path.exists():
            logger.error(
                f"Book collection path does not exist: {self.book_collection_path}"
            )
            return 0

        book_files = list(self.book_collection_path.rglob("*.txt"))

        total_chunks = 0
        batch_num = 1

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all files for processing
            future_to_file = {
                executor.submit(self._process_book_file, file_path): file_path
                for file_path in book_files
            }

            # Process completed files
            for future in tqdm(
                as_completed(future_to_file),
                total=len(book_files),
                desc="Processing book files",
            ):
                file_path = future_to_file[future]
                try:
                    chunks = future.result()

                    with self.lock:
                        self.stats.book_chunks += len(chunks)
                        self.stats.total_chunks_processed += len(chunks)
                        self.stats.total_words_processed += sum(
                            len(chunk.content.split()) for chunk in chunks
                        )

                    # Save chunks in batches
                    if chunks:
                        self._save_chunks(chunks, batch_num)
                        batch_num += 1
                        total_chunks += len(chunks)

                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
                    with self.lock:
                        self.stats.processing_errors.append(str(e))

        self.stats.last_processed_date = datetime.now()
        self._save_stats()

        logger.info(
            f"✅ Book collection processing complete: {total_chunks} chunks processed"
        )
        return total_chunks

    def start_learning(
        self, wikipedia_max_files: Optional[int] = None, process_books: bool = True
    ):
        """Start the learning process"""
        logger.info("🚀 Starting comprehensive learning process...")

        # Process Wikipedia dataset
        wikipedia_chunks = self.process_wikipedia_dataset(wikipedia_max_files)

        # Process book collection
        book_chunks = 0
        if process_books:
            book_chunks = self.process_book_collection()

        total_chunks = wikipedia_chunks + book_chunks

        logger.info(f"✅ Learning complete: {total_chunks} total chunks processed")
        return total_chunks

    # Enhanced functionality methods
    def record_interaction(
        self,
        user_message: str,
        bot_response: str,
        user_id: str = None,
        context: str = "",
    ):
        """Record and learn from user interaction"""
        try:
            # Analyze interaction quality
            quality_score = self._analyze_interaction_quality(
                user_message, bot_response
            )

            # Learn from interaction
            learning_success = self._learn_from_interaction(
                user_message, bot_response, quality_score, context
            )

            # Update statistics
            with self.lock:
                self.learning_stats["total_interactions"] += 1
                if learning_success:
                    self.learning_stats["successful_learnings"] += 1
                else:
                    self.learning_stats["failed_learnings"] += 1
                self.learning_stats["last_learning_date"] = datetime.now().isoformat()

            # Update user profile if available
            if user_id and self.user_profile_manager:
                self._update_user_profile(
                    user_id, user_message, bot_response, quality_score
                )

            # Save learning data
            self._save_learning_data()

            logger.info(
                f"✅ Interaction recorded: quality={quality_score:.2f}, success={learning_success}"
            )

        except Exception as e:
            logger.error(f"❌ Error recording interaction: {e}")

    def _analyze_interaction_quality(
        self, user_message: str, bot_response: str
    ) -> float:
        """Analyze the quality of user-bot interaction"""
        quality_score = 0.5  # Base score

        # Analyze user message
        user_words = len(user_message.split())
        user_has_question = "?" in user_message
        user_has_keywords = any(
            word in user_message.lower()
            for word in ["write", "story", "character", "plot", "help"]
        )

        # Analyze bot response
        bot_words = len(bot_response.split())
        bot_has_specific_info = any(
            word in bot_response.lower()
            for word in ["because", "example", "specifically", "detailed"]
        )
        bot_has_creative_elements = any(
            word in bot_response.lower()
            for word in ["imagine", "creative", "story", "character"]
        )

        # Calculate quality factors
        if user_has_question:
            quality_score += 0.1
        if user_has_keywords:
            quality_score += 0.1
        if bot_words > 50:
            quality_score += 0.1
        if bot_has_specific_info:
            quality_score += 0.1
        if bot_has_creative_elements:
            quality_score += 0.1

        # Normalize score
        quality_score = min(1.0, max(0.0, quality_score))

        return quality_score

    def _learn_from_interaction(
        self, user_message: str, bot_response: str, quality_score: float, context: str
    ) -> bool:
        """Learn from user interaction"""
        try:
            # Extract concepts from interaction
            concepts = self._extract_concepts(user_message + " " + bot_response)

            # Analyze writing style
            style_insights = self._analyze_writing_style(bot_response)

            # Store learning data
            learning_data = {
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "bot_response": bot_response,
                "quality_score": quality_score,
                "concepts": concepts,
                "style_insights": style_insights,
                "context": context,
            }

            self._store_learning_data(learning_data)

            # Update personality based on learning
            self._update_personality_from_learning(style_insights, quality_score)

            # Evolve personality if quality is high
            if quality_score > 0.7:
                self._evolve_personality(quality_score)
                return True

            return True

        except Exception as e:
            logger.error(f"❌ Error learning from interaction: {e}")
            return False

    def _extract_concepts(self, message: str) -> List[str]:
        """Extract key concepts from message"""
        concepts = []

        # Simple concept extraction
        words = message.lower().split()
        concept_keywords = [
            "story",
            "character",
            "plot",
            "writing",
            "creative",
            "narrative",
            "author",
            "book",
        ]

        for word in words:
            if word in concept_keywords and word not in concepts:
                concepts.append(word)

        return concepts

    def _analyze_writing_style(self, message: str) -> Dict[str, Any]:
        """Analyze writing style characteristics"""
        style_insights = {
            "word_count": len(message.split()),
            "sentence_count": len(message.split(".")),
            "avg_sentence_length": 0,
            "has_questions": "?" in message,
            "has_exclamations": "!" in message,
            "tone": "neutral",
            "complexity": "medium",
        }

        # Calculate average sentence length
        sentences = message.split(".")
        if sentences:
            style_insights["avg_sentence_length"] = sum(
                len(s.split()) for s in sentences
            ) / len(sentences)

        # Determine tone
        positive_words = ["great", "excellent", "wonderful", "amazing", "fantastic"]
        negative_words = ["terrible", "awful", "horrible", "bad", "disappointing"]

        positive_count = sum(
            1 for word in message.lower().split() if word in positive_words
        )
        negative_count = sum(
            1 for word in message.lower().split() if word in negative_words
        )

        if positive_count > negative_count:
            style_insights["tone"] = "positive"
        elif negative_count > positive_count:
            style_insights["tone"] = "negative"

        # Determine complexity
        if style_insights["avg_sentence_length"] > 20:
            style_insights["complexity"] = "high"
        elif style_insights["avg_sentence_length"] < 10:
            style_insights["complexity"] = "low"

        return style_insights

    def _store_learning_data(self, learning_data: Dict[str, Any]):
        """Store learning data for future reference"""
        learning_file = self.learning_dir / "interaction_history.json"

        try:
            if learning_file.exists():
                with open(learning_file, "r") as f:
                    history = json.load(f)
            else:
                history = []

            history.append(learning_data)

            # Keep only last 1000 interactions
            if len(history) > 1000:
                history = history[-1000:]

            with open(learning_file, "w") as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            logger.error(f"❌ Error storing learning data: {e}")

    def _update_personality_from_learning(
        self, style_insights: Dict[str, Any], quality_score: float
    ):
        """Update personality traits based on learning insights"""
        try:
            # Update traits based on style insights
            if style_insights["tone"] == "positive":
                self.personality_evolution["base_traits"]["supportive_nature"] += 0.01
                self.personality_evolution["base_traits"][
                    "motivational_ability"
                ] += 0.01

            if style_insights["complexity"] == "high":
                self.personality_evolution["base_traits"]["writing_expertise"] += 0.01

            if quality_score > 0.8:
                self.personality_evolution["base_traits"]["learning_enthusiasm"] += 0.01
                self.personality_evolution["base_traits"]["creative_expression"] += 0.01

            # Cap traits at 1.0
            for trait, value in self.personality_evolution["base_traits"].items():
                self.personality_evolution["base_traits"][trait] = min(1.0, value)

        except Exception as e:
            logger.error(f"❌ Error updating personality: {e}")

    def _evolve_personality(self, quality_score: float):
        """Evolve personality based on learning success"""
        try:
            # Record evolution
            evolution_entry = {
                "timestamp": datetime.now().isoformat(),
                "quality_score": quality_score,
                "previous_traits": dict(self.personality_evolution["base_traits"]),
            }

            # Evolve traits
            for trait in self.personality_evolution["base_traits"]:
                if random.random() < 0.3:  # 30% chance to evolve each trait
                    self.personality_evolution["base_traits"][trait] += 0.02

            # Cap traits at 1.0
            for trait, value in self.personality_evolution["base_traits"].items():
                self.personality_evolution["base_traits"][trait] = min(1.0, value)

            evolution_entry["new_traits"] = dict(
                self.personality_evolution["base_traits"]
            )
            self.personality_evolution["evolution_history"].append(evolution_entry)
            self.personality_evolution["personality_evolutions"] += 1

            # Update learning stats
            self.learning_stats["personality_evolutions"] += 1

            logger.info(f"🎉 Personality evolved! Quality score: {quality_score:.2f}")

        except Exception as e:
            logger.error(f"❌ Error evolving personality: {e}")

    def _reward_learning(self, activity: str, success_level: float):
        """Reward successful learning activities"""
        try:
            self.learning_stats["reward_count"] += 1

            # Boost positive traits
            self.personality_evolution["base_traits"]["learning_enthusiasm"] += 0.02
            self.personality_evolution["base_traits"]["creative_expression"] += 0.01

            logger.info(
                f"🏆 Learning rewarded: {activity} (success: {success_level:.2f})"
            )

        except Exception as e:
            logger.error(f"❌ Error rewarding learning: {e}")

    def _punish_lack_of_learning(self, missed_opportunity: str, severity: float):
        """Punish missed learning opportunities"""
        try:
            self.learning_stats["punishment_count"] += 1

            # Slightly reduce some traits
            self.personality_evolution["base_traits"]["learning_enthusiasm"] -= 0.01
            self.personality_evolution["base_traits"]["adaptability"] -= 0.01

            # Ensure traits don't go below 0.5
            for trait, value in self.personality_evolution["base_traits"].items():
                self.personality_evolution["base_traits"][trait] = max(0.5, value)

            logger.info(
                f"⚠️ Learning punishment: {missed_opportunity} (severity: {severity:.2f})"
            )

        except Exception as e:
            logger.error(f"❌ Error punishing learning: {e}")

    def _update_user_profile(
        self, user_id: str, user_message: str, bot_response: str, quality_score: float
    ):
        """Update user profile based on interaction"""
        if not self.user_profile_manager:
            return

        try:
            # Extract user preferences from interaction
            preferences = {
                "writing_style": "general",
                "interaction_quality": quality_score,
                "last_interaction": datetime.now().isoformat(),
            }

            # Update user profile
            self.user_profile_manager.update_user_preferences(user_id, preferences)

        except Exception as e:
            logger.error(f"❌ Error updating user profile: {e}")

    def modify_message_for_understanding(
        self, message: str, modification_type: str = "clarify"
    ) -> str:
        """Modify message for better understanding"""
        modified_message = message

        if modification_type in self.message_patterns:
            for pattern, replacement in self.message_patterns[modification_type]:
                modified_message = re.sub(
                    pattern, replacement, modified_message, flags=re.IGNORECASE
                )

        return modified_message

    def get_learning_summary(self) -> str:
        """Get comprehensive learning summary"""
        summary = []
        summary.append("📚 LEARNING ENGINE SUMMARY")
        summary.append("=" * 50)

        # Basic stats
        summary.append(f"📊 Training Data:")
        summary.append(
            f"   Total chunks processed: {self.stats.total_chunks_processed:,}"
        )
        summary.append(
            f"   Total words processed: {self.stats.total_words_processed:,}"
        )
        summary.append(f"   Wikipedia chunks: {self.stats.wikipedia_chunks:,}")
        summary.append(f"   Book chunks: {self.stats.book_chunks:,}")

        # Enhanced stats
        summary.append(f"\n🤖 Interaction Learning:")
        summary.append(
            f"   Total interactions: {self.learning_stats['total_interactions']:,}"
        )
        summary.append(
            f"   Successful learnings: {self.learning_stats['successful_learnings']:,}"
        )
        summary.append(
            f"   Failed learnings: {self.learning_stats['failed_learnings']:,}"
        )
        summary.append(
            f"   Personality evolutions: {self.learning_stats['personality_evolutions']:,}"
        )

        # Personality traits
        summary.append(f"\n🎭 Current Personality Traits:")
        for trait, value in self.personality_evolution["base_traits"].items():
            emoji = self._get_trait_emoji(trait, value)
            summary.append(f"   {emoji} {trait.replace('_', ' ').title()}: {value:.2f}")

        # Learning milestones
        if self.personality_evolution["learning_milestones"]:
            summary.append(f"\n🏆 Recent Learning Milestones:")
            for milestone in self.personality_evolution["learning_milestones"][-5:]:
                summary.append(f"   • {milestone}")

        return "\n".join(summary)

    def _get_trait_emoji(self, trait: str, value: float) -> str:
        """Get emoji for trait based on value"""
        if value >= 0.9:
            return "🌟"
        elif value >= 0.8:
            return "⭐"
        elif value >= 0.7:
            return "✨"
        elif value >= 0.6:
            return "💫"
        else:
            return "⭐"

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics"""
        return {
            "basic_stats": {
                "total_chunks_processed": self.stats.total_chunks_processed,
                "total_words_processed": self.stats.total_words_processed,
                "wikipedia_chunks": self.stats.wikipedia_chunks,
                "book_chunks": self.stats.book_chunks,
                "last_processed_date": (
                    self.stats.last_processed_date.isoformat()
                    if self.stats.last_processed_date
                    else None
                ),
            },
            "enhanced_stats": self.learning_stats,
            "personality_evolution": self.personality_evolution,
        }


def initialize(framework) -> LearningEngine:
    """Initialize the merged learning engine plugin"""
    return LearningEngine(framework)
