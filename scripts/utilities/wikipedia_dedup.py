#!/usr/bin/env python3
"""
Wikipedia XML Dataset Deduplication Script
Processes the Wikipedia XML dump and creates a deduplicated dataset
"""

import os
import sys
import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple
import xml.etree.ElementTree as ET
from collections import defaultdict
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("wikipedia_dedup.log"), logging.StreamHandler()],
)


class WikipediaDeduplicator:
    def __init__(self, xml_path: str, output_dir: str):
        self.xml_path = xml_path
        self.output_dir = output_dir
        self.article_hashes: Dict[str, str] = {}
        self.duplicate_count = 0
        self.unique_count = 0
        self.total_count = 0

    def calculate_article_hash(self, title: str, text: str) -> str:
        """Calculate hash for article content"""
        content = f"{title.lower().strip()}:{text.lower().strip()}"
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    def clean_text(self, text: str) -> str:
        """Clean and normalize article text"""
        if not text:
            return ""

        # Remove excessive whitespace
        text = " ".join(text.split())

        # Remove very short articles (likely stubs)
        if len(text) < 100:
            return ""

        return text

    def extract_articles_from_xml(self) -> List[Tuple[str, str]]:
        """Extract articles from Wikipedia XML dump"""
        articles = []

        logging.info(f"Starting to parse Wikipedia XML: {self.xml_path}")

        try:
            # Use iterparse for memory efficiency with large XML files
            context = ET.iterparse(self.xml_path, events=("start", "end"))

            current_title = ""
            current_text = ""
            in_page = False
            in_title = False
            in_text = False

            for event, elem in context:
                if event == "start":
                    if elem.tag.endswith("page"):
                        in_page = True
                        current_title = ""
                        current_text = ""
                    elif elem.tag.endswith("title") and in_page:
                        in_title = True
                    elif elem.tag.endswith("text") and in_page:
                        in_text = True

                elif event == "end":
                    if elem.tag.endswith("title") and in_title:
                        current_title = elem.text or ""
                        in_title = False
                    elif elem.tag.endswith("text") and in_text:
                        current_text = elem.text or ""
                        in_text = False
                    elif elem.tag.endswith("page") and in_page:
                        # Process completed page
                        if current_title and current_text:
                            cleaned_text = self.clean_text(current_text)
                            if cleaned_text:  # Only add if text is substantial
                                articles.append((current_title, cleaned_text))

                        # Clear element to free memory
                        elem.clear()
                        in_page = False

                        # Progress update every 1000 articles
                        if len(articles) % 1000 == 0:
                            logging.info(
                                f"Processed {len(articles)} articles so far..."
                            )

            logging.info(f"Finished parsing XML. Found {len(articles)} articles.")
            return articles

        except Exception as e:
            logging.error(f"Error parsing XML: {str(e)}")
            return []

    def deduplicate_articles(
        self, articles: List[Tuple[str, str]]
    ) -> List[Tuple[str, str]]:
        """Deduplicate articles based on content hash"""
        logging.info("Starting deduplication process...")

        unique_articles = []
        seen_hashes = set()

        for title, text in articles:
            self.total_count += 1

            # Calculate hash for this article
            article_hash = self.calculate_article_hash(title, text)

            if article_hash not in seen_hashes:
                seen_hashes.add(article_hash)
                unique_articles.append((title, text))
                self.unique_count += 1
                self.article_hashes[title] = article_hash
            else:
                self.duplicate_count += 1

            # Progress update
            if self.total_count % 1000 == 0:
                logging.info(
                    f"Processed {self.total_count} articles, {self.unique_count} unique, {self.duplicate_count} duplicates"
                )

        logging.info(
            f"Deduplication complete: {self.unique_count} unique articles, {self.duplicate_count} duplicates"
        )
        return unique_articles

    def save_articles(self, articles: List[Tuple[str, str]]) -> None:
        """Save deduplicated articles to output directory"""
        os.makedirs(self.output_dir, exist_ok=True)

        logging.info(f"Saving {len(articles)} articles to {self.output_dir}")

        # Save as individual text files for easy processing
        for i, (title, text) in enumerate(articles):
            # Create safe filename
            safe_title = "".join(
                c for c in title if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            safe_title = safe_title[:100]  # Limit length

            filename = f"{i:06d}_{safe_title}.txt"
            filepath = os.path.join(self.output_dir, filename)

            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"Title: {title}\n")
                    f.write(f"Hash: {self.article_hashes.get(title, 'unknown')}\n")
                    f.write(f"Length: {len(text)} characters\n")
                    f.write("-" * 50 + "\n")
                    f.write(text)
            except Exception as e:
                logging.error(f"Error saving article {title}: {str(e)}")

        # Save metadata
        metadata = {
            "total_articles_processed": self.total_count,
            "unique_articles": self.unique_count,
            "duplicate_articles": self.duplicate_count,
            "deduplication_ratio": (
                self.duplicate_count / self.total_count if self.total_count > 0 else 0
            ),
            "output_directory": self.output_dir,
            "source_file": self.xml_path,
        }

        metadata_path = os.path.join(self.output_dir, "deduplication_metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        logging.info(
            f"Saved {len(articles)} articles and metadata to {self.output_dir}"
        )

    def run_deduplication(self) -> None:
        """Run the complete deduplication process"""
        start_time = time.time()

        logging.info("Starting Wikipedia XML deduplication process")
        logging.info(f"Source: {self.xml_path}")
        logging.info(f"Output: {self.output_dir}")

        # Check if source file exists
        if not os.path.exists(self.xml_path):
            logging.error(f"Source file not found: {self.xml_path}")
            return

        # Extract articles from XML
        articles = self.extract_articles_from_xml()

        if not articles:
            logging.error("No articles extracted from XML")
            return

        # Deduplicate articles
        unique_articles = self.deduplicate_articles(articles)

        # Save deduplicated articles
        self.save_articles(unique_articles)

        end_time = time.time()
        duration = end_time - start_time

        logging.info("=" * 50)
        logging.info("DEDUPLICATION COMPLETE")
        logging.info("=" * 50)
        logging.info(f"Total articles processed: {self.total_count}")
        logging.info(f"Unique articles: {self.unique_count}")
        logging.info(f"Duplicate articles: {self.duplicate_count}")
        logging.info(
            f"Deduplication ratio: {self.duplicate_count / self.total_count:.2%}"
        )
        logging.info(f"Processing time: {duration:.2f} seconds")
        logging.info(f"Output directory: {self.output_dir}")
        logging.info("=" * 50)


def main():
    """Main function"""
    xml_path = r"D:\dataset\Portfolio\Portfolio_Projects\Custom_LLM\datasets\enwiki-20250201-pages-articles-multistream.xml"
    output_dir = r"D:\wikipedia_deduplicated"

    print("=" * 60)
    print("WIKIPEDIA XML DEDUPLICATION SCRIPT")
    print("=" * 60)
    print(f"Source XML: {xml_path}")
    print(f"Output Directory: {output_dir}")
    print("=" * 60)

    # Check if source file exists
    if not os.path.exists(xml_path):
        print(f"❌ ERROR: Source file not found: {xml_path}")
        print("Please check the file path and try again.")
        return

    # Get file size
    file_size = os.path.getsize(xml_path)
    file_size_gb = file_size / (1024**3)
    print(f"📁 Source file size: {file_size_gb:.2f} GB")

    # Confirm with user
    response = input("\nDo you want to proceed with deduplication? (y/n): ")
    if response.lower() != "y":
        print("Cancelled.")
        return

    # Run deduplication
    deduplicator = WikipediaDeduplicator(xml_path, output_dir)
    deduplicator.run_deduplication()


if __name__ == "__main__":
    main()
