#!/usr/bin/env python3
"""
Robust Wikipedia XML Dataset Deduplication Script
Processes the Wikipedia XML dump with better error handling and incremental saving
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
import gc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("wikipedia_dedup_robust.log"), logging.StreamHandler()],
)


class RobustWikipediaDeduplicator:
    def __init__(self, xml_path: str, output_dir: str):
        self.xml_path = xml_path
        self.output_dir = output_dir
        self.article_hashes: Dict[str, str] = {}
        self.duplicate_count = 0
        self.unique_count = 0
        self.total_count = 0
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Batch processing
        self.batch_size = 10000
        self.current_batch = []
        self.batch_number = 0

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

    def save_batch(self, articles: List[Tuple[str, str]]) -> None:
        """Save a batch of articles to files"""
        if not articles:
            return
            
        batch_dir = os.path.join(self.output_dir, f"batch_{self.batch_number:04d}")
        os.makedirs(batch_dir, exist_ok=True)
        
        for i, (title, text) in enumerate(articles):
            # Create safe filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:100]  # Limit length
            filename = f"{i:06d}_{safe_title}.txt"
            filepath = os.path.join(batch_dir, filename)
            
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"Title: {title}\n\n{text}")
            except Exception as e:
                logging.warning(f"Failed to save article {title}: {e}")
        
        self.batch_number += 1
        logging.info(f"Saved batch {self.batch_number-1} with {len(articles)} articles")

    def extract_articles_from_xml_robust(self) -> None:
        """Extract articles from Wikipedia XML dump with robust error handling"""
        
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
                try:
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
                                    self.current_batch.append((current_title, cleaned_text))
                                    self.total_count += 1
                                    
                                    # Save batch when it reaches batch_size
                                    if len(self.current_batch) >= self.batch_size:
                                        self.save_batch(self.current_batch)
                                        self.current_batch = []
                                        gc.collect()  # Force garbage collection
                            
                            # Clear element to free memory
                            elem.clear()
                            in_page = False
                            
                            # Progress update every 10000 articles
                            if self.total_count % 10000 == 0:
                                logging.info(f"Processed {self.total_count} articles so far...")
                
                except Exception as e:
                    logging.warning(f"Error processing element: {e}")
                    continue
            
            # Save any remaining articles in the final batch
            if self.current_batch:
                self.save_batch(self.current_batch)
            
            logging.info(f"Extraction complete. Total articles processed: {self.total_count}")
            
        except Exception as e:
            logging.error(f"Error parsing XML: {e}")
            # Save whatever we have so far
            if self.current_batch:
                self.save_batch(self.current_batch)
            raise

    def create_metadata(self) -> None:
        """Create metadata file with processing information"""
        metadata = {
            "total_articles_processed": self.total_count,
            "batches_created": self.batch_number,
            "output_directory": self.output_dir,
            "source_file": self.xml_path,
            "processing_completed": True,
            "batch_size": self.batch_size
        }
        
        metadata_path = os.path.join(self.output_dir, "deduplication_metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Saved metadata to {metadata_path}")

    def run_deduplication(self) -> None:
        """Run the complete deduplication process"""
        start_time = time.time()
        
        logging.info("Starting robust Wikipedia XML deduplication process")
        logging.info(f"Source: {self.xml_path}")
        logging.info(f"Output: {self.output_dir}")
        
        # Check if source file exists
        if not os.path.exists(self.xml_path):
            logging.error(f"Source file not found: {self.xml_path}")
            return
        
        try:
            # Extract articles from XML with robust error handling
            self.extract_articles_from_xml_robust()
            
            # Create metadata
            self.create_metadata()
            
            end_time = time.time()
            duration = end_time - start_time
            
            logging.info("=" * 50)
            logging.info("DEDUPLICATION COMPLETE")
            logging.info("=" * 50)
            logging.info(f"Total articles processed: {self.total_count}")
            logging.info(f"Batches created: {self.batch_number}")
            logging.info(f"Processing time: {duration:.2f} seconds")
            logging.info(f"Output directory: {self.output_dir}")
            logging.info("=" * 50)
            
        except Exception as e:
            logging.error(f"Error during deduplication: {e}")
            # Still create metadata with what we have
            self.create_metadata()


def main():
    """Main function"""
    xml_path = r"D:\dataset\Portfolio\Portfolio_Projects\Custom_LLM\datasets\enwiki-20250201-pages-articles-multistream.xml"
    output_dir = r"D:\wikipedia_deduplicated"
    
    print("=" * 60)
    print("ROBUST WIKIPEDIA XML DEDUPLICATION SCRIPT")
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
    response = input("\nDo you want to proceed with robust deduplication? (y/n): ")
    if response.lower() != "y":
        print("Cancelled.")
        return
    
    # Run deduplication
    deduplicator = RobustWikipediaDeduplicator(xml_path, output_dir)
    deduplicator.run_deduplication()


if __name__ == "__main__":
    main() 