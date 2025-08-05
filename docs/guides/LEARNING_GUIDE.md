# 🧠 Learning Engine Guide

## Overview
The Learning Engine processes your Wikipedia dataset and Book Collection to create training data for your authoring bot. It chunks text into manageable pieces and saves them as JSON files for future use.

## Quick Start

### 1. Test the System
```bash
python test_learning.py
```

### 2. Check Current Statistics
```bash
python start_learning.py --stats-only
```

### 3. Start Learning Process

#### For Testing (Small Sample)
```bash
python start_learning.py --wikipedia-max-files 100
```

#### For Full Processing (Will take a very long time!)
```bash
python start_learning.py
```

#### Process Only Books (Skip Wikipedia)
```bash
python start_learning.py --skip-books
```

## Configuration

The learning engine uses these default settings:
- **Chunk Size**: 1000 words per chunk
- **Overlap Size**: 200 words overlap between chunks
- **Max Workers**: 4 parallel processing threads
- **Batch Size**: 1000 chunks per batch file

## Data Sources

### Wikipedia Dataset
- **Path**: `D:/wikipedia_deduplicated`
- **Files Found**: 12,875,342 text files
- **Size**: 100+ GB
- **Processing**: Multi-threaded with progress bars

### Book Collection
- **Path**: `D:/Foundry_Bot/Book_Collection`
- **Files Found**: 20 text files
- **Books**: Anna, Eve, Mavlon, Random, Relic, Shadow
- **Processing**: Sequential with metadata

## Output

### Training Data
- **Location**: `models/training_data/`
- **Format**: JSON batches (`training_batch_000001.json`)
- **Structure**: Each batch contains chunks with content, metadata, and source info

### Statistics
- **File**: `models/training_data/learning_stats.json`
- **Tracks**: Total chunks, words, Wikipedia chunks, book chunks, errors

## Discord Commands

Once the bot is running, you can use these commands:

```
!learning-stats    - Show learning statistics
!help              - Show all available commands
```

## Processing Strategy

### For the Massive Wikipedia Dataset:
1. **Start Small**: Use `--wikipedia-max-files 1000` to test
2. **Monitor Progress**: Check stats regularly
3. **Scale Up**: Gradually increase file count
4. **Full Processing**: Only run full processing when ready for long-term operation

### For Your Books:
1. **Quick Processing**: Books process much faster
2. **Rich Metadata**: Each chunk includes book name, chapter info
3. **High Quality**: Your writing style will be preserved

## Performance Tips

### Memory Management
- The system processes files in batches to manage memory
- Each batch is saved immediately to disk
- Progress is tracked and can be resumed

### Processing Speed
- Wikipedia: ~12.8M files = Very long processing time
- Books: ~20 files = Quick processing
- Use `--wikipedia-max-files` to limit processing

### Error Handling
- Processing errors are logged and tracked
- Individual file failures don't stop the process
- Check `learning_stats.json` for error details

## Example Usage

### Test Run (Recommended First)
```bash
# Process 100 Wikipedia files + all books
python start_learning.py --wikipedia-max-files 100
```

### Book Collection Only
```bash
# Process only your books (fast)
python start_learning.py --skip-books
```

### Full Wikipedia Processing
```bash
# Process everything (will take days/weeks!)
python start_learning.py
```

## Monitoring Progress

### Check Statistics
```bash
python start_learning.py --stats-only
```

### View Output Files
```bash
# Check the training data directory
ls models/training_data/
```

### Monitor Disk Space
The Wikipedia dataset will generate many GB of training data. Monitor your disk space!

## Next Steps

1. **Start with a small test**: `--wikipedia-max-files 100`
2. **Process your books**: They're much smaller and contain your writing style
3. **Scale up gradually**: Increase Wikipedia file count as needed
4. **Monitor progress**: Use the stats commands to track processing
5. **Use the training data**: The chunks can be used for fine-tuning or RAG

## Troubleshooting

### Common Issues

**Memory Errors**
- Reduce `max_workers` in the learning engine
- Process smaller batches

**Disk Space**
- Monitor available space
- Process in smaller chunks

**Processing Errors**
- Check `learning_stats.json` for error details
- Individual file failures are logged but don't stop processing

**Slow Processing**
- Wikipedia dataset is massive (12.8M files)
- Use `--wikipedia-max-files` to limit processing
- Books process much faster

### Getting Help
- Check the test script: `python test_learning.py`
- Review statistics: `python start_learning.py --stats-only`
- Monitor the output directory: `models/training_data/` 