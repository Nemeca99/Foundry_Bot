#!/usr/bin/env python3
"""
Learning Engine Plugin for Authoring Bot
Handles training data processing from Wikipedia and Book Collection
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Generator, Any
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from tqdm import tqdm


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
    """Handles learning from Wikipedia dataset and Book Collection"""

    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config
        self.stats = LearningStats()
        self.chunk_size = self.config.get("chunk_size", 1000)
        self.overlap_size = self.config.get("overlap_size", 200)
        self.max_workers = self.config.get("max_workers", 4)

        # Paths
        from config import Config

        self.wikipedia_path = Config.WIKIPEDIA_PATH
        self.book_collection_path = Config.BOOK_COLLECTION_PATH
        self.output_dir = Config.TRAINING_DATA_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Thread safety
        self.lock = threading.Lock()

        # Load existing stats
        self._load_stats()

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
                logging.error(f"Error loading learning stats: {e}")

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
            "processing_errors": self.stats.processing_errors,
        }
        with open(stats_file, "w") as f:
            json.dump(data, f, indent=2)

    def _create_chunk_id(self, content: str, source: str) -> str:
        """Create a unique chunk ID"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        return f"{source}_{content_hash[:8]}"

    def _text_to_chunks(self, text: str, source: str) -> List[TrainingChunk]:
        """Split text into overlapping chunks"""
        chunks = []
        words = text.split()

        for i in range(0, len(words), self.chunk_size - self.overlap_size):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)

            if len(chunk_text.strip()) < 100:  # Skip very short chunks
                continue

            chunk_id = self._create_chunk_id(chunk_text, source)
            chunk = TrainingChunk(
                content=chunk_text,
                source=source,
                chunk_id=chunk_id,
                metadata={"word_count": len(chunk_words), "chunk_index": len(chunks)},
            )
            chunks.append(chunk)

        return chunks

    def _process_wikipedia_file(self, file_path: Path) -> List[TrainingChunk]:
        """Process a single Wikipedia file"""
        chunks = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Clean Wikipedia content
            content = self._clean_wikipedia_content(content)

            if len(content.strip()) > 100:
                file_chunks = self._text_to_chunks(
                    content, f"wikipedia_{file_path.name}"
                )
                chunks.extend(file_chunks)

        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            with self.lock:
                self.stats.processing_errors.append(error_msg)
            logging.error(error_msg)

        return chunks

    def _clean_wikipedia_content(self, content: str) -> str:
        """Clean Wikipedia content"""
        # Remove HTML tags
        content = re.sub(r"<[^>]+>", "", content)

        # Remove Wikipedia markup
        content = re.sub(r"\[\[([^|\]]*?)\]\]", r"\1", content)  # Simple links
        content = re.sub(
            r"\[\[([^|\]]*?)\|([^\]]*?)\]\]", r"\2", content
        )  # Named links
        content = re.sub(r"\{\{[^}]*\}\}", "", content)  # Templates
        content = re.sub(r"==+([^=]+)==+", r"\1", content)  # Headers
        content = re.sub(r"==+", "", content)  # Remaining headers

        # Clean up whitespace
        content = re.sub(r"\s+", " ", content)
        content = content.strip()

        return content

    def _process_book_file(self, file_path: Path) -> List[TrainingChunk]:
        """Process a single book file"""
        chunks = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if len(content.strip()) > 100:
                # Extract book metadata from path
                book_name = file_path.parent.name
                chapter_name = file_path.stem

                file_chunks = self._text_to_chunks(
                    content, f"book_{book_name}_{chapter_name}"
                )

                # Add book-specific metadata
                for chunk in file_chunks:
                    chunk.metadata.update(
                        {
                            "book_name": book_name,
                            "chapter_name": chapter_name,
                            "file_path": str(file_path),
                        }
                    )

                chunks.extend(file_chunks)

        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            with self.lock:
                self.stats.processing_errors.append(error_msg)
            logging.error(error_msg)

        return chunks

    def _save_chunks(self, chunks: List[TrainingChunk], batch_num: int):
        """Save chunks to JSON file"""
        batch_file = self.output_dir / f"training_batch_{batch_num:06d}.json"

        serializable_chunks = []
        for chunk in chunks:
            serializable_chunk = {
                "content": chunk.content,
                "source": chunk.source,
                "chunk_id": chunk.chunk_id,
                "metadata": chunk.metadata,
                "created_date": chunk.created_date.isoformat(),
            }
            serializable_chunks.append(serializable_chunk)

        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(serializable_chunks, f, indent=2, ensure_ascii=False)

    def process_wikipedia_dataset(self, max_files: Optional[int] = None) -> int:
        """Process Wikipedia dataset"""
        if not self.wikipedia_path.exists():
            logging.error(f"Wikipedia path does not exist: {self.wikipedia_path}")
            return 0

        print(f"🔍 Scanning Wikipedia dataset at: {self.wikipedia_path}")

        # Find all text files
        text_files = list(self.wikipedia_path.rglob("*.txt"))
        if max_files:
            text_files = text_files[:max_files]

        print(f"📚 Found {len(text_files)} Wikipedia files to process")

        total_chunks = 0
        batch_size = 1000
        current_batch = []
        batch_num = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all files for processing
            future_to_file = {
                executor.submit(self._process_wikipedia_file, file_path): file_path
                for file_path in text_files
            }

            # Process completed files
            for future in tqdm(
                as_completed(future_to_file),
                total=len(text_files),
                desc="Processing Wikipedia",
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

                    current_batch.extend(chunks)
                    total_chunks += len(chunks)

                    # Save batch when it gets large enough
                    if len(current_batch) >= batch_size:
                        self._save_chunks(current_batch, batch_num)
                        batch_num += 1
                        current_batch = []

                except Exception as e:
                    logging.error(f"Error processing {file_path}: {e}")

        # Save remaining chunks
        if current_batch:
            self._save_chunks(current_batch, batch_num)

        self.stats.last_processed_date = datetime.now()
        self._save_stats()

        print(f"✅ Processed {total_chunks} Wikipedia chunks")
        return total_chunks

    def process_book_collection(self) -> int:
        """Process Book Collection"""
        if not self.book_collection_path.exists():
            logging.error(
                f"Book collection path does not exist: {self.book_collection_path}"
            )
            return 0

        print(f"📖 Processing Book Collection at: {self.book_collection_path}")

        # Find all text files
        text_files = list(self.book_collection_path.rglob("*.txt"))
        print(f"📚 Found {len(text_files)} book files to process")

        total_chunks = 0
        batch_size = 500  # Smaller batches for books
        current_batch = []
        batch_num = 0

        for file_path in tqdm(text_files, desc="Processing Books"):
            chunks = self._process_book_file(file_path)

            with self.lock:
                self.stats.book_chunks += len(chunks)
                self.stats.total_chunks_processed += len(chunks)
                self.stats.total_words_processed += sum(
                    len(chunk.content.split()) for chunk in chunks
                )

            current_batch.extend(chunks)
            total_chunks += len(chunks)

            # Save batch when it gets large enough
            if len(current_batch) >= batch_size:
                self._save_chunks(current_batch, batch_num)
                batch_num += 1
                current_batch = []

        # Save remaining chunks
        if current_batch:
            self._save_chunks(current_batch, batch_num)

        self.stats.last_processed_date = datetime.now()
        self._save_stats()

        print(f"✅ Processed {total_chunks} book chunks")
        return total_chunks

    def start_learning(
        self, wikipedia_max_files: Optional[int] = None, process_books: bool = True
    ):
        """Start the learning process"""
        print("🧠 Starting Learning Engine...")
        print("=" * 50)

        total_chunks = 0

        # Process Wikipedia dataset
        if self.wikipedia_path.exists():
            print("\n🌐 Processing Wikipedia Dataset...")
            wikipedia_chunks = self.process_wikipedia_dataset(wikipedia_max_files)
            total_chunks += wikipedia_chunks
        else:
            print(f"⚠️  Wikipedia path not found: {self.wikipedia_path}")

        # Process Book Collection
        if process_books and self.book_collection_path.exists():
            print("\n📚 Processing Book Collection...")
            book_chunks = self.process_book_collection()
            total_chunks += book_chunks
        elif not self.book_collection_path.exists():
            print(f"⚠️  Book collection path not found: {self.book_collection_path}")

        print("\n" + "=" * 50)
        print(f"🎉 Learning Complete!")
        print(f"📊 Total chunks processed: {total_chunks:,}")
        print(f"📊 Total words processed: {self.stats.total_words_processed:,}")
        print(f"📊 Wikipedia chunks: {self.stats.wikipedia_chunks:,}")
        print(f"📊 Book chunks: {self.stats.book_chunks:,}")
        print(f"📁 Output directory: {self.output_dir}")

        if self.stats.processing_errors:
            print(f"⚠️  {len(self.stats.processing_errors)} processing errors occurred")
            for error in self.stats.processing_errors[-5:]:  # Show last 5 errors
                print(f"   - {error}")

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get current learning statistics"""
        return {
            "total_chunks_processed": self.stats.total_chunks_processed,
            "total_words_processed": self.stats.total_words_processed,
            "wikipedia_chunks": self.stats.wikipedia_chunks,
            "book_chunks": self.stats.book_chunks,
            "last_processed_date": (
                self.stats.last_processed_date.isoformat()
                if self.stats.last_processed_date
                else None
            ),
            "processing_errors_count": len(self.stats.processing_errors),
            "output_directory": str(self.output_dir),
        }


def initialize(framework) -> LearningEngine:
    """Initialize the Learning Engine plugin"""
    return LearningEngine(framework)
