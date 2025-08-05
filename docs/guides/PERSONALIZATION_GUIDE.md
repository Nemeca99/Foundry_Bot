# Personalization Engine Guide for Authoring Bot

## Overview

The **Personalization Engine** is a powerful feature that learns from your writing style and conversation patterns to provide personalized assistance. It analyzes your existing work in the `Book_Collection` folder and adapts the bot's responses to match your unique writing style.

## How It Works

### 1. **Writing Style Analysis**
The engine analyzes all `.txt` files in your `Book_Collection` folder to understand:
- **Vocabulary patterns** - Your most commonly used words and phrases
- **Sentence structure** - Average sentence length and complexity
- **Thematic elements** - Recurring themes and topics in your writing
- **Writing characteristics** - Vocabulary richness, word length patterns

### 2. **Conversation Learning**
The bot records and analyzes your interactions to understand:
- **Communication preferences** - How you phrase requests
- **Topic patterns** - What you typically ask about
- **Response preferences** - What types of responses you prefer

### 3. **Personalized Prompts**
When generating content, the bot automatically enhances prompts with:
- Style recommendations based on your writing patterns
- Vocabulary suggestions from your existing work
- Thematic elements that match your style

## Discord Commands

### `!personalize analyze`
Analyzes your writing style from the `Book_Collection` folder.

**Example:**
```
!personalize analyze
```

**What it does:**
- Scans all `.txt` files in your Book_Collection
- Analyzes vocabulary, sentence structure, and themes
- Creates a "writing fingerprint" of your style
- Shows statistics about your writing characteristics

### `!personalize suggestions`
Gets personalized writing suggestions based on your style.

**Example:**
```
!personalize suggestions
```

**What it provides:**
- Style recommendations for improvement
- Vocabulary suggestions from your writing
- Thematic elements to incorporate
- Structure advice based on your patterns

### `!personalize stats`
Shows personalization statistics and status.

**Example:**
```
!personalize stats
```

**What it shows:**
- Whether your writing has been analyzed
- Number of conversation interactions recorded
- Style preferences saved
- Words analyzed and average sentence length

## Integration with Other Features

### **Enhanced Text Generation**
When you use commands like `!write-chapter`, the bot automatically:
- Applies your writing style preferences
- Uses vocabulary patterns from your work
- Incorporates thematic elements you commonly use
- Adjusts sentence structure to match your style

### **Learning Over Time**
The personalization improves as you:
- Add more content to your `Book_Collection`
- Interact more with the bot
- Provide feedback on generated content

## File Structure

The personalization data is stored in:
```
models/personalization/
├── writing_fingerprint.json    # Your writing style analysis
├── conversation_history.json    # Your interaction history
└── style_preferences.json      # Your style preferences
```

## Writing Style Analysis Details

### **Vocabulary Analysis**
- Identifies your most commonly used words (excluding common stop words)
- Analyzes word frequency patterns
- Tracks vocabulary richness and variety

### **Sentence Structure Analysis**
- Calculates average sentence length
- Analyzes sentence complexity patterns
- Identifies your preferred writing rhythm

### **Thematic Analysis**
- Finds common phrases and word combinations
- Identifies recurring themes in your writing
- Tracks topic preferences

### **Writing Characteristics**
- **Vocabulary Richness**: Ratio of unique words to total words
- **Average Word Length**: Typical length of words you use
- **Sentence Variety**: How much you vary sentence structure

## Best Practices

### **For Best Results:**
1. **Add your existing work** to the `Book_Collection` folder
2. **Use the bot regularly** to build conversation history
3. **Run analysis periodically** as you add new content
4. **Review suggestions** to understand your style patterns

### **Content Organization:**
```
Book_Collection/
├── Novel1/
│   ├── Chapter_1.txt
│   ├── Chapter_2.txt
│   └── ...
├── Novel2/
│   ├── Chapter_1.txt
│   └── ...
└── Short_Stories/
    ├── Story1.txt
    └── ...
```

## Troubleshooting

### **"No text found in Book_Collection"**
- Ensure you have `.txt` files in your `Book_Collection` folder
- Check that files are readable and contain text content
- Verify the path in `config.py` is correct

### **"Personalization engine not available"**
- Check that the `personalization_engine.py` plugin is in the `framework/plugins/` folder
- Ensure NLTK is installed: `pip install nltk`
- Restart the bot to reload plugins

### **Analysis takes too long**
- The analysis processes all text files in your collection
- Large collections may take several minutes
- Progress is shown in the Discord response

## Advanced Features

### **Style Preferences**
You can manually set style preferences:
```python
# In your code
personalization_engine.update_style_preferences({
    "preferred_genre": "fantasy",
    "writing_style": "descriptive",
    "target_audience": "young_adult"
})
```

### **Custom Analysis**
Access detailed analysis data:
```python
# Get comprehensive style profile
profile = personalization_engine.create_style_profile()

# Get specific writing characteristics
characteristics = personalization_engine.writing_fingerprint.get("characteristics", {})
```

## Privacy and Data

### **Local Storage**
- All personalization data is stored locally on your computer
- No data is sent to external servers
- You control all your writing and conversation data

### **Data Management**
- Conversation history is limited to the last 1000 interactions
- Writing fingerprint is updated when you run analysis
- You can delete personalization files to reset the system

## Future Enhancements

Planned features include:
- **Style transfer** - Apply your style to different genres
- **Collaborative learning** - Learn from multiple authors
- **Advanced analytics** - Detailed writing style reports
- **Style comparison** - Compare your style to other authors

## Support

If you encounter issues with the personalization engine:
1. Check the console logs for error messages
2. Verify your `Book_Collection` folder structure
3. Ensure all required dependencies are installed
4. Test with the `test_personalization.py` script

The personalization engine is designed to make your authoring experience more personal and effective by learning from your unique writing style and preferences. 