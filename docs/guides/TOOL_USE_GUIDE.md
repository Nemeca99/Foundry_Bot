# Tool Use Guide for Authoring Bot

## Overview

The Authoring Bot now supports **Tool Use (Function Calling)** with your LM Studio model, enabling advanced AI-powered authoring capabilities. This feature allows the bot to intelligently call specific functions based on your requests, making it much more powerful for story creation, character development, and business analysis.

## How It Works

The bot uses the OpenAI-compatible Function Calling API to:
1. **Analyze your request** and determine which tools are needed
2. **Call specific functions** with the appropriate parameters
3. **Execute the functions** and gather results
4. **Provide a comprehensive response** based on the tool results

## Available Tools

### 1. **create_story_outline**
Creates detailed story outlines with chapters, characters, and plot points.

**Required Parameters:**
- `title`: The title of the story
- `genre`: The genre (fantasy, sci-fi, romance, etc.)
- `target_length`: Target length (short story, novella, novel)

**Optional Parameters:**
- `main_character`: Brief description of the main character
- `setting`: Brief description of the story setting

**Example Usage:**
```
!tools Create a story outline for a fantasy novel called "The Crystal Kingdom"
```

### 2. **generate_character_profile**
Generates detailed character profiles with backstory, personality, and motivations.

**Required Parameters:**
- `name`: Character name
- `role`: Character role (protagonist, antagonist, supporting, etc.)

**Optional Parameters:**
- `age`: Character age or age range
- `background`: Brief background or context for the character

**Example Usage:**
```
!tools Generate a character profile for a detective named Sarah
```

### 3. **analyze_market_trends**
Analyzes current market trends for book sales and publishing opportunities.

**Optional Parameters:**
- `genre`: Genre to analyze
- `timeframe`: Timeframe for analysis (last month, last 3 months, last year)

**Example Usage:**
```
!tools Analyze market trends for romance novels
```

### 4. **generate_promotional_content**
Generates promotional content for book marketing.

**Required Parameters:**
- `book_title`: Title of the book
- `content_type`: Type of content (blurb, social media post, email newsletter, etc.)

**Optional Parameters:**
- `target_audience`: Target audience for the content

**Example Usage:**
```
!tools Generate promotional content for my book "The Crystal Kingdom"
```

### 5. **track_sales_data**
Tracks and analyzes book sales data.

**Required Parameters:**
- `book_title`: Title of the book to track

**Optional Parameters:**
- `platform`: Sales platform (Amazon, KDP, etc.)
- `timeframe`: Timeframe for tracking (today, this week, this month)

**Example Usage:**
```
!tools Track sales data for "The Crystal Kingdom"
```

## Discord Commands

### Primary Tool Command
```
!tools <your request>
```

**Examples:**
```
!tools Create a story outline for a sci-fi novel about space exploration
!tools Generate a character profile for a villain named Dr. Malice
!tools Analyze market trends for young adult fantasy
!tools Generate promotional content for my romance novel
!tools Track sales data for my latest book
```

## How to Use

1. **Start with a clear request**: Describe what you want to accomplish
2. **Be specific**: Include relevant details like genre, character names, etc.
3. **Let the AI decide**: The bot will automatically choose the right tools
4. **Review the results**: The bot will show you which tools were used and provide a comprehensive response

## Example Conversations

### Story Creation
```
You: !tools I want to write a fantasy novel about a young wizard learning magic

Bot: I'll help you create a story outline for your fantasy novel. Let me use the story outline tool to generate a detailed structure for your wizard story.

[Tool Used: create_story_outline]
✅ Story outline created for 'The Young Wizard's Journey' in project 'The Young Wizard's Journey_20250805_143022'

Here's your story outline:

**Title:** The Young Wizard's Journey
**Genre:** Fantasy
**Target Length:** Novel
**Main Character:** A young apprentice wizard discovering their magical abilities
**Setting:** A mystical academy in a world where magic is real but rare

**Story Structure:**
- Chapter 1: Discovery of magical abilities
- Chapter 2: Enrollment in the academy
- Chapter 3: First magical lessons
- [Additional chapters and plot points...]

The outline has been saved to your project. You can now start writing individual chapters using the !write-chapter command.
```

### Character Development
```
You: !tools Create a character profile for a mysterious mentor figure

Bot: I'll generate a detailed character profile for your mysterious mentor. Let me use the character profile tool to create a comprehensive backstory and personality.

[Tool Used: generate_character_profile]
✅ Character profile generated for Mysterious Mentor

**Character Profile:**
**Name:** Master Elara
**Role:** Mentor/Supporting Character
**Age:** Appears ageless, possibly centuries old
**Background:** A former guardian of ancient magical knowledge

**Personality Traits:**
- Wise but enigmatic
- Speaks in riddles and metaphors
- Has a mysterious past that unfolds throughout the story
- Protective of their students but pushes them to grow

**Motivations:**
- Preserving ancient magical knowledge
- Training the next generation of wizards
- Hiding from a dark past that still hunts them

**Character Arc:**
- Initially mysterious and distant
- Gradually reveals their tragic backstory
- Becomes a trusted mentor and ally
- May sacrifice themselves for their student's growth

This character can serve as both a guide and a source of mystery in your story.
```

### Market Analysis
```
You: !tools What are the current trends in young adult fantasy?

Bot: I'll analyze the current market trends for young adult fantasy to help you understand the publishing landscape.

[Tool Used: analyze_market_trends]
✅ Market analysis completed for young adult fantasy genre

**Current Market Trends:**
- Rising popularity in self-published works
- Increased demand for diverse voices
- Growing market for audiobooks
- Strong sales in digital formats

**Recommendations for YA Fantasy:**
- Consider audiobook production
- Focus on digital marketing
- Explore self-publishing platforms
- Build author platform on social media

**Key Insights:**
- Diverse representation is highly valued
- Series continue to perform well
- Standalone novels are gaining popularity
- Crossover appeal to adult readers is strong

This analysis can help you position your YA fantasy novel for maximum market impact.
```

## Technical Details

### API Integration
- Uses LM Studio's OpenAI-compatible `/v1/chat/completions` endpoint
- Supports function calling with automatic tool selection
- Configurable timeout (default: 600 seconds)
- Handles both direct responses and tool-based responses

### Error Handling
- Graceful fallback if tools are unavailable
- Clear error messages for debugging
- Automatic retry logic for API calls
- Validation of tool parameters

### Performance
- Fast response times for simple queries
- Longer processing for complex tool chains
- Progress indicators for long-running operations
- Efficient tool result caching

## Best Practices

1. **Be Specific**: Include relevant details in your requests
2. **Use Natural Language**: Write as if talking to a human assistant
3. **Combine Tools**: The AI can use multiple tools for complex requests
4. **Review Results**: Always check the tool results for accuracy
5. **Iterate**: Refine your requests based on the responses

## Troubleshooting

### Common Issues

**"Tool manager not available"**
- Check that the tool_manager plugin is loaded
- Verify LM Studio is running and accessible
- Check the bot's status with `!status`

**"API call failed"**
- Verify LM Studio URL in config.py
- Check network connectivity
- Ensure the model is loaded in LM Studio

**"No response from model"**
- The model may be processing a complex request
- Try breaking down your request into smaller parts
- Check the timeout settings

### Getting Help

- Use `!help` to see all available commands
- Use `!status` to check bot and plugin status
- Use `!learning-stats` to check learning engine status

## Future Enhancements

The tool use system is designed to be extensible. Future versions may include:
- More specialized authoring tools
- Integration with external APIs
- Advanced market analysis tools
- Automated publishing workflows
- Enhanced character development tools

---

**Ready to enhance your authoring workflow with AI-powered tools!** 🚀 