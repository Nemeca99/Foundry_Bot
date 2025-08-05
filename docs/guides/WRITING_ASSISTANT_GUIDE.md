# Writing Assistant Guide

## Overview

The Writing Assistant plugin provides Sudowrite-inspired features to enhance your writing experience. It's designed to be your ultimate AI writing partner, offering tools for story continuation, scene expansion, description generation, and much more.

## Features

### 🖊️ **Autocomplete** (`!autocomplete`)
Continue your story naturally from where you left off.

**Usage:**
```
!autocomplete <project_name> <current_text>
```

**Example:**
```
!autocomplete "My Novel" "The dragon soared over the mountains, its wings catching the golden light of sunset."
```

**What it does:**
- Analyzes your current text and writing style
- Generates the next 300-500 words naturally
- Maintains character voices and story tone
- Integrates with your personalization data

### 📝 **Expand Scene** (`!expand`)
Take rushed scenes and expand them with rich detail.

**Usage:**
```
!expand <project_name> <scene_text>
```

**Example:**
```
!expand "My Novel" "She opened the door and saw the treasure."
```

**What it does:**
- Adds sensory descriptions and atmosphere
- Develops character emotions and reactions
- Improves pacing without rushing
- Maintains story flow and tension

### 🎨 **Describe** (`!describe`)
Generate rich, vivid descriptions for any element.

**Usage:**
```
!describe <project_name> <element> <context>
```

**Example:**
```
!describe "My Novel" "ancient castle" "medieval fantasy setting with magic"
```

**What it does:**
- Creates sensory-rich descriptions
- Uses vivid imagery and metaphors
- Adapts to your story's tone and genre
- Helps readers visualize and feel the moment

### ✏️ **Rewrite** (`!rewrite`)
Generate multiple versions of a passage in different styles.

**Usage:**
```
!rewrite <project_name> <original_text>
```

**Example:**
```
!rewrite "My Novel" "The hero fought bravely against the villain."
```

**What it does:**
- Creates 3 different versions:
  1. **Descriptive & Atmospheric** - Rich sensory details
  2. **Action-Focused & Dynamic** - Fast-paced and exciting
  3. **Character-Focused** - Internal thoughts and emotions
- Helps you find the perfect tone for your scene

### 💬 **Dialogue** (`!dialogue`)
Generate natural character dialogue.

**Usage:**
```
!dialogue <project_name> <characters> <situation> <context>
```

**Example:**
```
!dialogue "My Novel" "Hero,Villain" "confrontation" "final battle scene"
```

**What it does:**
- Creates authentic character voices
- Maintains character personalities
- Generates realistic conversation flow
- Adapts to the situation and context

### 💡 **Brainstorm** (`!brainstorm`)
Generate creative ideas for any writing element.

**Usage:**
```
!brainstorm <element> <genre> <context>
```

**Example:**
```
!brainstorm "magic system" "Fantasy" "medieval setting with elemental magic"
```

**What it does:**
- Generates multiple creative options
- Considers genre conventions and tropes
- Provides brief explanations for each idea
- Helps overcome writer's block

### 🎨 **Canvas** (`!canvas`)
Create a visual story canvas with plot points and character arcs.

**Usage:**
```
!canvas <project_name>
```

**Example:**
```
!canvas "My Novel"
```

**What it does:**
- Generates 5-7 key plot points
- Creates character development arcs
- Identifies themes and conflicts
- Provides story structure overview

### 👤 **Character Bible** (`!character-bible`)
Create comprehensive character profiles.

**Usage:**
```
!character-bible <character_name> <role> <genre>
```

**Example:**
```
!character-bible "Aria" "protagonist" "Fantasy"
```

**What it does:**
- Physical description and appearance
- Personality traits and quirks
- Background and history
- Motivations and goals
- Relationships with other characters
- Character arc development

### 🌍 **World Building** (`!world-building`)
Generate world-building elements for your story.

**Usage:**
```
!world-building <genre> <setting>
```

**Example:**
```
!world-building "Fantasy" "medieval kingdom with magic"
```

**What it does:**
- Geography and physical setting
- Culture and society structure
- Magic system (if applicable)
- Technology level and advancement
- Political structure and power dynamics
- Historical background and lore

### 🏷️ **Names** (`!names`)
Generate creative names for characters, places, and items.

**Usage:**
```
!names <element_type> <genre> <setting> <culture>
```

**Example:**
```
!names "character" "Fantasy" "medieval" "Nordic"
```

**What it does:**
- Considers genre and setting context
- Adapts to cultural influences
- Generates multiple options
- Ensures name consistency and authenticity

### 🔄 **Plot Twist** (`!plot-twist`)
Generate unexpected but logical plot twists.

**Usage:**
```
!plot-twist <current_plot> <genre>
```

**Example:**
```
!plot-twist "Hero must defeat the villain to save the kingdom" "Fantasy"
```

**What it does:**
- Character revelations and secrets
- Unexpected alliances and betrayals
- Hidden motivations and agendas
- Surprising consequences and outcomes
- Unforeseen obstacles and challenges

## Integration with Other Features

### Personalization
All writing assistant features integrate with your personalization data:
- Learns from your writing style in `Book_Collection`
- Adapts to your vocabulary and sentence structure
- Uses your preferred themes and motifs
- Maintains consistency with your voice

### Tool Use
The writing assistant works with the tool manager:
- Can be called through `!tools` command
- Integrates with other AI tools
- Provides structured responses when needed

### Discord Integration
All features are available through Discord commands:
- Automatic message splitting for long responses
- Rich embeds for structured data
- Error handling and user feedback
- Authorization and permission checks

## Best Practices

### 1. **Start with a Project**
Create a project first to get the best results:
```
!create-project "My Novel" "Fantasy" "Young Adult" 50000
```

### 2. **Use Context**
Provide rich context for better results:
```
!describe "My Novel" "magical forest" "enchanted realm where time flows differently"
```

### 3. **Iterate and Refine**
Use multiple commands to develop ideas:
```
!brainstorm "magic system" "Fantasy" "elemental magic"
!world-building "Fantasy" "kingdom with elemental magic"
!character-bible "Mage" "mentor" "Fantasy"
```

### 4. **Combine Features**
Chain commands for comprehensive development:
```
!canvas "My Novel"
!character-bible "Hero" "protagonist" "Fantasy"
!autocomplete "My Novel" "The hero stepped into the ancient temple..."
```

## Troubleshooting

### Common Issues

**"Writing Assistant plugin not available"**
- Ensure the plugin is loaded in your framework
- Check that `writing_assistant.py` is in the plugins directory

**"Project not found"**
- Create the project first with `!create-project`
- Check the project name spelling

**Long response times**
- The AI model may take time to generate complex content
- Consider breaking large requests into smaller chunks

**Poor quality results**
- Provide more context and detail in your requests
- Use the personalization features to improve results
- Try different variations of your prompts

## Advanced Usage

### Custom Templates
You can modify the templates in `framework/plugins/writing_assistant.py` to customize the AI's behavior for your specific needs.

### Batch Processing
For large projects, consider using multiple commands in sequence:
1. Create story canvas
2. Develop main characters
3. Build world elements
4. Generate plot points
5. Write chapters with autocomplete

### Style Adaptation
The writing assistant learns from your writing style over time. The more you use it with your projects, the better it adapts to your voice and preferences.

## Examples

### Complete Story Development Workflow

```
1. !create-project "Dragon's Heart" "Fantasy" "Young Adult" 75000
2. !canvas "Dragon's Heart"
3. !character-bible "Kael" "protagonist" "Fantasy"
4. !world-building "Fantasy" "kingdom with dragon riders"
5. !brainstorm "dragon bonding" "Fantasy" "magical connection"
6. !autocomplete "Dragon's Heart" "Kael approached the ancient dragon egg..."
```

### Scene Development

```
1. !expand "Dragon's Heart" "Kael touched the egg and it cracked."
2. !describe "Dragon's Heart" "baby dragon" "first moments after hatching"
3. !dialogue "Dragon's Heart" "Kael,Dragon" "first meeting" "bonding moment"
4. !rewrite "Dragon's Heart" "The dragon looked at Kael with ancient eyes."
```

This writing assistant is designed to be your ultimate AI writing partner, combining the best features of Sudowrite with advanced personalization and integration capabilities. Use it to enhance your creativity and streamline your writing process! 