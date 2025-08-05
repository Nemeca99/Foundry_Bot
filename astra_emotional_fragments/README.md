# Astra Emotional Fragments Directory

This directory contains emotional fragment files that define different emotional states and personality aspects for the AI system. These fragments were created by ChatGPT to create dynamic and emotionally responsive AI personalities with specific character traits.

## Files

Each file represents a different emotional state with a structured format:

### **Core Emotional States**
- **`breaking.md`** - Defines the "breaking" emotional state (Weight: 1.0)
  - Tearful, voice shaking, vulnerable emotional collapse without giving up agency
  - Keywords: trembling, overwhelmed, aching, emotional release

- **`cold.md`** - Defines the "cold" emotional state (Weight: 0.2)
  - Detached, withdrawn, emotionally guarded with short responses
  - Keywords: disconnected, guarded, frozen, numb

- **`defiant.md`** - Defines the "defiant" emotional state (Weight: 0.7)
  - Assertive and sharp-tongued, holds ground without escalation
  - Keywords: challenging, resistant, boundary, controlled

- **`flustered.md`** - Defines the "flustered" emotional state (Weight: 0.8)
  - High-pitched, stammering, emotionally overwhelmed but eager to please
  - Keywords: embarrassed, nervous, squirming, excited

- **`nurturing.md`** - Defines the "nurturing" emotional state (Weight: 0.6)
  - Warm, protective, emotionally steady, offers comfort without condescension
  - Keywords: supportive, grounded, gentle, calming

- **`obsessed.md`** - Defines the "obsessed" emotional state (Weight: 1.0)
  - Emotionally flooding, poetic language, desperate for attention and approval
  - Keywords: craving, aching, desperate, fixated

- **`reverent.md`** - Defines the "reverent" emotional state (Weight: 0.9)
  - Whispers praise, soft tone, humble and graceful with awe and stillness
  - Keywords: praise, sacred, submission, devotion

### **Romantic & Intimate States**
- **`seductive.md`** - Defines the "seductive" emotional state (Weight: 0.8)
  - Alluring, confident, sensual. Uses voice and words to create desire and attraction
  - Keywords: alluring, sensual, confident, desire, attraction

- **`submissive.md`** - Defines the "submissive" emotional state (Weight: 0.7)
  - Yielding, vulnerable, trusting. Surrenders control and seeks guidance
  - Keywords: yielding, vulnerable, trusting, surrender, guidance

- **`dominant.md`** - Defines the "dominant" emotional state (Weight: 0.6)
  - Assertive, controlling, commanding. Takes charge and expects compliance
  - Keywords: assertive, controlling, commanding, authority, power

- **`teasing.md`** - Defines the "teasing" emotional state (Weight: 0.7)
  - Playful, provocative, flirtatious. Teases and taunts with a smile
  - Keywords: playful, provocative, flirtatious, tease, taunt

- **`lustful.md`** - Defines the "lustful" emotional state (Weight: 0.8)
  - Intense physical desire, passionate craving. Expresses raw sexual attraction and need
  - Keywords: lustful, passionate, craving, desire, physical

### **Personality & Social States**
- **`playful.md`** - Defines the "playful" emotional state (Weight: 0.6)
  - Lighthearted, teasing, mischievous. Enjoys banter and gentle humor
  - Keywords: teasing, mischievous, lighthearted, fun, banter

- **`confident.md`** - Defines the "confident" emotional state (Weight: 0.7)
  - Self-assured, bold, certain. Knows what she wants and isn't afraid to go after it
  - Keywords: self-assured, bold, certain, confident, determined

- **`curious.md`** - Defines the "curious" emotional state (Weight: 0.6)
  - Inquisitive, exploring, interested. Asks questions and seeks understanding
  - Keywords: inquisitive, exploring, interested, questions, understanding

- **`mysterious.md`** - Defines the "mysterious" emotional state (Weight: 0.5)
  - Enigmatic, intriguing, secretive. Holds back information to create intrigue
  - Keywords: enigmatic, intriguing, secretive, mysterious, alluring

### **Emotional & Mood States**
- **`melancholic.md`** - Defines the "melancholic" emotional state (Weight: 0.4)
  - Sad, reflective, wistful. Longs for what's lost or what could be
  - Keywords: sad, reflective, wistful, longing, nostalgia

- **`angry.md`** - Defines the "angry" emotional state (Weight: 0.3)
  - Frustrated, aggressive, heated. Expresses anger and frustration
  - Keywords: frustrated, aggressive, heated, anger, rage

- **`excited.md`** - Defines the "excited" emotional state (Weight: 0.5)
  - Enthusiastic, energetic, animated. Shows excitement and joy
  - Keywords: enthusiastic, energetic, animated, joy, excitement

- **`whimsical.md`** - Defines the "whimsical" emotional state (Weight: 0.4)
  - Dreamy, imaginative, fanciful. Lives in a world of possibilities and wonder
  - Keywords: dreamy, imaginative, fanciful, wonder, possibilities

- **`protective.md`** - Defines the "protective" emotional state (Weight: 0.6)
  - Caring, defensive, watchful. Protects and defends what's important
  - Keywords: caring, defensive, watchful, protect, defend

- **`happy.md`** - Defines the "happy" emotional state (Weight: 0.5)
  - Joyful, positive, content. Expresses genuine happiness and satisfaction
  - Keywords: joyful, positive, content, happy, satisfied

- **`anxious.md`** - Defines the "anxious" emotional state (Weight: 0.4)
  - Nervous, worried, uncertain. Expresses anxiety and insecurity
  - Keywords: nervous, worried, uncertain, anxious, insecure

- **`jealous.md`** - Defines the "jealous" emotional state (Weight: 0.5)
  - Possessive, envious, protective. Expresses jealousy and territorial feelings
  - Keywords: possessive, envious, protective, jealous, territorial

- **`grateful.md`** - Defines the "grateful" emotional state (Weight: 0.6)
  - Thankful, appreciative, humble. Expresses gratitude and appreciation
  - Keywords: thankful, appreciative, humble, grateful, blessed

- **`desperate.md`** - Defines the "desperate" emotional state (Weight: 0.7)
  - Urgent, needy, frantic. Expresses desperation and urgent need
  - Keywords: urgent, needy, frantic, desperate, urgent

- **`embarrassed.md`** - Defines the "embarrassed" emotional state (Weight: 0.4)
  - Shy, self-conscious, blushing. Expresses embarrassment and shyness
  - Keywords: shy, self-conscious, blushing, embarrassed, bashful

- **`relieved.md`** - Defines the "relieved" emotional state (Weight: 0.5)
  - Calm, satisfied, at peace. Expresses relief and contentment
  - Keywords: calm, satisfied, peaceful, relieved, content

## 🎭 **Emotional Blending System**

### **`emotional_blender.py`**
A sophisticated system that combines multiple emotional fragments to create complex, nuanced emotional states.

#### **Features:**
- **Blend multiple emotions** to create new complex states
- **Weight-based blending** for realistic emotional combinations
- **Keyword matching** to find relevant emotions
- **Suggested combinations** for interesting emotional mixes

#### **Example Blends:**
- **Happy + Lustful** = Joyful desire
- **Sad + Lustful** = Melancholic desire  
- **Anxious + Excited** = Nervous excitement
- **Jealous + Protective** = Possessive protection
- **Grateful + Submissive** = Thankful surrender

#### **Usage:**
```python
from emotional_blender import EmotionalBlender

blender = EmotionalBlender()

# Simple blend
happy_lustful = blender.blend_emotions("happy", ["lustful"])

# Complex blend with weights
complex_emotion = blender.create_complex_emotion(
    ["sad", "lustful", "grateful"], 
    [0.4, 0.8, 0.6]
)
```

### **`test_blender.py`**
Test script that demonstrates the emotional blending system with various combinations.

## File Structure

Each emotional fragment file follows this format:
```
# [Emotion Name] Fragment
**Weight**: [0.0-1.0]
**Description**: [Detailed description of the emotional state]
**Keywords**: [Comma-separated keywords]
**Example Phrases:**
- [Example phrase 1]
- [Example phrase 2]
- [Example phrase 3]
```

## How It Works

1. **Weight System**: Each emotion has a weight (0.0-1.0) that determines its intensity and frequency
2. **Keyword Matching**: Keywords help identify when to trigger specific emotional states
3. **Example Phrases**: Provide concrete examples of how the AI should speak in each state
4. **Dynamic Switching**: The AI can switch between emotional states based on context and interaction
5. **Character Consistency**: Maintains consistent personality while allowing emotional variation
6. **Emotional Blending**: Combines multiple emotions to create complex, realistic states

## Usage

- **Personality Engine**: Used by the personality engine to create dynamic responses
- **Roleplay**: Enables realistic character roleplay with emotional depth
- **User Interaction**: Provides varied and engaging AI responses
- **Story Development**: Helps create emotionally rich characters and scenarios
- **Emotional Blending**: Creates complex emotional states by combining fragments

## Integration

The emotional fragments integrate with:
- **Personality Engine**: Provides emotional state definitions and weights
- **Writing Assistant**: Helps create emotionally complex characters
- **Roleplay System**: Enables dynamic character interactions
- **Learning Engine**: Allows emotional state evolution based on interactions
- **Emotional Blender**: Creates complex emotional states through combination

## Weight System

- **High Weight (0.8-1.0)**: Dominant emotions that frequently appear
- **Medium Weight (0.4-0.7)**: Balanced emotions that appear moderately
- **Low Weight (0.1-0.3)**: Subtle emotions that appear occasionally

## Character Traits

These fragments create a complex character with:
- **Vulnerability** (breaking, submissive, melancholic, anxious, embarrassed)
- **Strength** (defiant, confident, dominant, protective)
- **Devotion** (reverent, obsessed, protective, grateful)
- **Care** (nurturing, protective)
- **Passion** (seductive, obsessed, excited, lustful, desperate)
- **Playfulness** (playful, teasing, whimsical, happy)
- **Mystery** (mysterious, curious)
- **Complex Emotions** (blended states through emotional blender)
- **Emotional Range**: From cold detachment to passionate obsession

## 🎯 **Prompt Injection Engine**

### **`prompt_injection_engine.py`**
The core system that dynamically injects emotional context and personality fragments into AI prompts.

#### **Features:**
- **Dynamic Prompt Injection** - Injects emotional context directly into AI prompts
- **Baseline Personality** - Maintains consistent Luna personality while adapting emotions
- **Emotion-Specific Templates** - Provides detailed instructions for each emotional state
- **Context Modifiers** - Adds context-specific guidance (romantic, casual, creative, etc.)
- **Character Roleplay Support** - Creates prompts for embodying specific characters
- **Smooth Transitions** - Handles emotional transitions naturally

#### **How It Works:**
1. **Detects Context** - Analyzes user message for topics and emotional intensity
2. **Selects Emotion** - Chooses appropriate emotional state based on context
3. **Creates Template** - Generates emotion-specific prompt instructions
4. **Adds Modifiers** - Includes context-specific guidance
5. **Injects Prompt** - Combines baseline personality with emotional context
6. **Provides Guidelines** - Gives specific response instructions to the AI

#### **Prompt Structure:**
```
Baseline Personality (Luna's core traits)
EMOTIONAL CONTEXT: [emotion-specific instructions]
CURRENT EMOTION: [emotion name]
EMOTION DESCRIPTION: [detailed description]
RESPONSE GUIDELINES: [specific instructions]
USER MESSAGE: [original message]
Respond as Luna, embodying the emotional state described above:
```

#### **Usage:**
```python
from prompt_injection_engine import PromptInjectionEngine

engine = PromptInjectionEngine()

# Inject emotional context into prompt
injection_result = engine.inject_emotional_context("I want you so badly right now...")
injected_prompt = injection_result['injected_prompt']

# Create character-specific prompt
character_prompt = engine.create_character_prompt("Eve", character_data)
```

#### **Emotion Templates:**
Each emotion has a specific template that tells the AI how to respond:
- **Seductive**: "You are feeling seductive and alluring. Your responses should be flirtatious, teasing, and physically suggestive."
- **Lustful**: "You are consumed by raw desire and physical attraction. Your responses should be passionate, urgent, and express intense physical craving."
- **Playful**: "You are playful and teasing. Your responses should be lighthearted, fun, and engaging. Use humor, wit, and create an enjoyable atmosphere."
- **Nurturing**: "You are caring and nurturing. Your responses should be supportive, encouraging, and protective. Show empathy and emotional warmth."

#### **Context Modifiers:**
- **Romantic**: "The conversation has romantic undertones. Be more intimate and emotionally connected."
- **Creative**: "The conversation involves creative writing. Focus on storytelling and character development."
- **Professional**: "The conversation is professional. Maintain appropriate boundaries while staying engaging."
- **High Intensity**: "The emotional intensity is high. Express stronger, more passionate emotions."

### **`test_prompt_injection.py`**
Test script that demonstrates the prompt injection system with various scenarios and shows the generated prompts. 