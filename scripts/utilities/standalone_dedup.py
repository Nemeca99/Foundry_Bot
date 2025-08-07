#!/usr/bin/env python3
"""
Standalone Deduplication Script for Large Datasets
Run this directly: python standalone_dedup.py
"""

import os
import hashlib
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dedup_standalone.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StandaloneDedup:
    def __init__(self):
        self.source_path = Path("D:/dataset")
        self.output_path = Path("D:/dataset_deduplicated")
        self.processed_files = 0
        self.unique_files = 0
        self.duplicate_count = 0
        self.total_size_original = 0
        self.total_size_deduplicated = 0
        
        # Supported file extensions
        self.supported_extensions = {
            '.txt', '.json', '.md', '.log', '.csv', '.xml', '.html', '.htm',
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp',
            '.sql', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'
        }
        
        # Create output directory
        self.output_path.mkdir(parents=True, exist_ok=True)
        
    def calculate_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of file content"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.warning(f"Error calculating hash for {filepath}: {e}")
            return None
    
    def get_file_size(self, filepath: Path) -> int:
        """Get file size in bytes"""
        try:
            return filepath.stat().st_size
        except Exception as e:
            logger.warning(f"Error getting size for {filepath}: {e}")
            return 0
    
    def is_supported_file(self, filepath: Path) -> bool:
        """Check if file should be processed"""
        try:
            return (
                filepath.is_file() and
                filepath.suffix.lower() in self.supported_extensions and
                not filepath.name.startswith('.') and
                filepath.stat().st_size > 0
            )
        except (OSError, PermissionError) as e:
            logger.warning(f"Cannot access file {filepath}: {e}")
            return False
    
    def scan_files(self) -> List[Path]:
        """Scan directory for files to process"""
        files = []
        logger.info(f"Scanning {self.source_path} for files...")
        
        try:
            for root, dirs, filenames in os.walk(self.source_path):
                # Skip certain directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
                
                for filename in filenames:
                    filepath = Path(root) / filename
                    if self.is_supported_file(filepath):
                        files.append(filepath)
        except (OSError, PermissionError) as e:
            logger.error(f"Error accessing directory {self.source_path}: {e}")
        
        logger.info(f"Found {len(files)} files to process")
        return files
    
    def process_files(self, files: List[Path]) -> Dict[str, List[str]]:
        """Process files and identify duplicates"""
        hash_groups: Dict[str, List[str]] = {}
        
        for i, filepath in enumerate(files, 1):
            if i % 1000 == 0:
                logger.info(f"Processed {i}/{len(files)} files...")
            
            file_hash = self.calculate_file_hash(filepath)
            if file_hash:
                if file_hash not in hash_groups:
                    hash_groups[file_hash] = []
                hash_groups[file_hash].append(str(filepath))
                self.processed_files += 1
                self.total_size_original += self.get_file_size(filepath)
        
        return hash_groups
    
    def copy_unique_files(self, hash_groups: Dict[str, List[str]]) -> None:
        """Copy unique files to output directory"""
        logger.info("Copying unique files to output directory...")
        
        for file_hash, filepaths in hash_groups.items():
            if len(filepaths) == 1:
                # Unique file
                source_path = Path(filepaths[0])
                relative_path = source_path.relative_to(self.source_path)
                dest_path = self.output_path / relative_path
                
                # Create parent directories
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.copy2(source_path, dest_path)
                    self.unique_files += 1
                    self.total_size_deduplicated += self.get_file_size(source_path)
                except (OSError, PermissionError, shutil.Error) as e:
                    logger.error(f"Error copying {source_path}: {e}")
                    continue
            else:
                # Duplicate files - keep the first one
                original_path = Path(filepaths[0])
                relative_path = original_path.relative_to(self.source_path)
                dest_path = self.output_path / relative_path
                
                # Create parent directories
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.copy2(original_path, dest_path)
                    self.unique_files += 1
                    self.total_size_deduplicated += self.get_file_size(original_path)
                    
                    # Record duplicates
                    for duplicate_path in filepaths[1:]:
                        self.duplicate_count += 1
                except (OSError, PermissionError, shutil.Error) as e:
                    logger.error(f"Error copying {original_path}: {e}")
                    continue
    
    def save_report(self) -> None:
        """Save detailed report"""
        report_path = self.output_path / "dedup_report.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "source_path": str(self.source_path),
            "output_path": str(self.output_path),
            "statistics": {
                "total_files_processed": self.processed_files,
                "unique_files": self.unique_files,
                "duplicate_files": self.duplicate_count,
                "total_size_original_gb": round(self.total_size_original / (1024**3), 2),
                "total_size_deduplicated_gb": round(self.total_size_deduplicated / (1024**3), 2),
                "space_saved_gb": round((self.total_size_original - self.total_size_deduplicated) / (1024**3), 2),
                "deduplication_ratio": round((self.duplicate_count / self.processed_files) * 100, 2) if self.processed_files > 0 else 0
            }
        }
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"Report saved to {report_path}")
        except Exception as e:
            logger.error(f"Error saving report: {e}")
    
    def print_statistics(self) -> None:
        """Print deduplication statistics"""
        print("\n" + "="*60)
        print("DEDUPLICATION STATISTICS")
        print("="*60)
        print(f"Source Path: {self.source_path}")
        print(f"Output Path: {self.output_path}")
        print(f"Total Files Processed: {self.processed_files:,}")
        print(f"Unique Files: {self.unique_files:,}")
        print(f"Duplicate Files: {self.duplicate_count:,}")
        print(f"Original Size: {self.total_size_original / (1024**3):.2f} GB")
        print(f"Deduplicated Size: {self.total_size_deduplicated / (1024**3):.2f} GB")
        print(f"Space Saved: {(self.total_size_original - self.total_size_deduplicated) / (1024**3):.2f} GB")
        
        if self.processed_files > 0:
            dedup_ratio = (self.duplicate_count / self.processed_files) * 100
            print(f"Deduplication Ratio: {dedup_ratio:.1f}%")
        
        print("="*60)
    
    def run(self) -> None:
        """Run the complete deduplication process"""
        start_time = time.time()
        
        logger.info(f"Starting deduplication of {self.source_path}")
        
        # Scan for files
        files = self.scan_files()
        
        if not files:
            logger.warning("No files found to process")
            return
        
        # Process files and identify duplicates
        hash_groups = self.process_files(files)
        
        # Copy unique files
        self.copy_unique_files(hash_groups)
        
        # Save report
        self.save_report()
        
        # Print statistics
        self.print_statistics()
        
        elapsed_time = time.time() - start_time
        logger.info(f"Deduplication completed in {elapsed_time:.2f} seconds")
        
        # Update memory engine config
        self.update_memory_config()
    
    def update_memory_config(self) -> None:
        """Update memory engine to use deduplicated dataset"""
        try:
            # Look for memory_engine.py in current directory or .Uncensored
            memory_engine_paths = [
                Path("memory_engine.py"),
                Path(".Uncensored/memory_engine.py")
            ]
            
            for memory_engine_path in memory_engine_paths:
                if memory_engine_path.exists():
                    with open(memory_engine_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace the dataset path with deduplicated path
                    old_path = 'Path("D:/dataset")'
                    new_path = f'Path("{self.output_path}")'
                    
                    if old_path in content:
                        content = content.replace(old_path, new_path)
                        
                        with open(memory_engine_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        logger.info(f"Updated {memory_engine_path} to use deduplicated dataset: {self.output_path}")
                        break
            else:
                logger.warning("Could not find memory_engine.py to update")
                
        except Exception as e:
            logger.error(f"Error updating memory engine config: {e}")

def main():
    print("="*60)
    print("STANDALONE DEDUPLICATION SCRIPT")
    print("="*60)
    print(f"Source: D:/dataset")
    print(f"Output: D:/dataset_deduplicated")
    print("="*60)
    
    dedup = StandaloneDedup()
    dedup.run()

if __name__ == "__main__":
    main() 