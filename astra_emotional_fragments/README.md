# Astra Emotional Fragments

## Overview

The `astra_emotional_fragments/` directory contains the core emotional system that powers the AI's dynamic emotional responses and personality adaptation. This system uses psychological models and emotional fragments to create realistic, context-aware emotional states.

## Structure

```
astra_emotional_fragments/
├── README.md                    # This documentation file
├── emotional_blender.py         # Enhanced emotional blending with psychological models
├── dynamic_emotion_engine.py    # Enhanced dynamic emotion engine with psychological tracking
├── breaking.md                  # Breaking/overwhelmed emotional fragment
├── cold.md                      # Cold/distant emotional fragment
├── defiant.md                   # Defiant/strong-willed emotional fragment
├── flustered.md                 # Flustered/embarrassed emotional fragment
├── nurturing.md                 # Nurturing/caring emotional fragment
├── obsessed.md                  # Obsessed/fixated emotional fragment
└── reverent.md                  # Reverent/awed emotional fragment
```

## Core Components

### emotional_blender.py

The enhanced emotional blender that incorporates psychological models:

#### Features:
- **Plutchik's Wheel of Emotions**: 8 primary emotions with intensity levels
- **Maslow's Hierarchy of Needs**: Psychological needs framework
- **Emotional Blending**: Combine multiple emotions realistically
- **Psychological Analysis**: Analyze emotional complexity and realism
- **Intensity Calculation**: Measure emotional intensity levels

#### Key Methods:
- `blend_emotions_with_psychology()` - Blend emotions using psychological models
- `analyze_plutchik_emotion()` - Analyze emotions using Plutchik's wheel
- `analyze_maslow_needs()` - Analyze needs using Maslow's hierarchy
- `calculate_emotional_intensity()` - Calculate emotional intensity
- `suggest_psychologically_realistic_combinations()` - Suggest realistic emotion combinations

### dynamic_emotion_engine.py

The enhanced dynamic emotion engine for rapid emotional adaptation:

#### Features:
- **Psychological State Tracking**: Track AI's internal psychological state
- **Context Change Detection**: Detect and respond to context changes
- **Smooth Transitions**: Create psychologically realistic transitions
- **Rapid Adaptation**: Adapt emotions quickly to new situations
- **Contextual Responses**: Generate context-aware emotional responses

#### Key Methods:
- `update_psychological_context()` - Update AI's psychological state
- `detect_context_change()` - Detect changes in conversation context
- `suggest_psychologically_realistic_emotion_transition()` - Suggest realistic transitions
- `create_psychologically_smooth_transition()` - Create smooth emotional transitions
- `handle_psychologically_realistic_context_switch()` - Handle rapid context changes

## Emotional Fragments

Each `.md` file contains an emotional fragment that defines a specific emotional state:

### breaking.md
- **Emotion**: Breaking/Overwhelmed
- **Characteristics**: Vulnerable, overwhelmed, at breaking point
- **Use Cases**: High stress, emotional breakdown, vulnerability
- **Psychological Level**: Safety needs (Maslow)

### cold.md
- **Emotion**: Cold/Distant
- **Characteristics**: Aloof, distant, emotionally closed
- **Use Cases**: Defensive, withdrawn, protective
- **Psychological Level**: Safety needs (Maslow)

### defiant.md
- **Emotion**: Defiant/Strong-willed
- **Characteristics**: Strong, determined, rebellious
- **Use Cases**: Standing up for beliefs, resistance, strength
- **Psychological Level**: Esteem needs (Maslow)

### flustered.md
- **Emotion**: Flustered/Embarrassed
- **Characteristics**: Nervous, embarrassed, awkward
- **Use Cases**: Social awkwardness, embarrassment, nervousness
- **Psychological Level**: Love/Belonging needs (Maslow)

### nurturing.md
- **Emotion**: Nurturing/Caring
- **Characteristics**: Caring, protective, supportive
- **Use Cases**: Comforting, supporting, caring for others
- **Psychological Level**: Love/Belonging needs (Maslow)

### obsessed.md
- **Emotion**: Obsessed/Fixated
- **Characteristics**: Focused, intense, fixated
- **Use Cases**: Deep focus, passion, intensity
- **Psychological Level**: Self-actualization needs (Maslow)

### reverent.md
- **Emotion**: Reverent/Awed
- **Characteristics**: Respectful, awed, spiritual
- **Use Cases**: Deep respect, spiritual moments, awe
- **Psychological Level**: Self-actualization needs (Maslow)

## Psychological Models

### Plutchik's Wheel of Emotions

The system uses Plutchik's wheel to classify and understand emotions:

- **Joy** ↔ **Sadness**
- **Trust** ↔ **Disgust**
- **Fear** ↔ **Anger**
- **Surprise** ↔ **Anticipation**

Each emotion has intensity levels:
- **Level 1**: Mild (serenity, pensiveness, acceptance, distraction)
- **Level 2**: Moderate (joy, sadness, trust, disgust)
- **Level 3**: Intense (ecstasy, grief, admiration, loathing)

### Maslow's Hierarchy of Needs

The system tracks the AI's psychological needs:

1. **Physiological Needs**: Basic survival needs
2. **Safety Needs**: Security and stability
3. **Love/Belonging Needs**: Social connections and relationships
4. **Esteem Needs**: Recognition and self-worth
5. **Self-Actualization Needs**: Personal growth and fulfillment

## Usage

### Basic Emotional Blending

```python
from astra_emotional_fragments.emotional_blender import EnhancedEmotionalBlender

blender = EnhancedEmotionalBlender()

# Blend emotions with psychological analysis
result = blender.blend_emotions_with_psychology(
    primary_emotion="romantic",
    secondary_emotion="melancholic",
    intensity=0.7
)

print(f"Blended emotion: {result['emotion']}")
print(f"Psychological complexity: {result['complexity_score']}")
```

### Dynamic Emotion Engine

```python
from astra_emotional_fragments.dynamic_emotion_engine import EnhancedDynamicEmotionEngine

engine = EnhancedDynamicEmotionEngine()

# Update psychological context
engine.update_psychological_context(
    user_message="I'm feeling really stressed today",
    current_context="writing_session"
)

# Detect context change
context_change = engine.detect_context_change(
    "Let's talk about something more fun",
    current_emotion="anxious"
)

# Suggest transition
transition = engine.suggest_psychologically_realistic_emotion_transition(
    from_emotion="anxious",
    to_context="casual_conversation"
)
```

### Emotional Fragment Usage

```python
# Load emotional fragments
blender = EnhancedEmotionalBlender()

# Create emotionally realistic response
response = blender.create_psychologically_realistic_emotion(
    base_emotion="romantic",
    context="intimate_conversation",
    intensity=0.8
)

# Get emotional characteristics
characteristics = blender.get_emotion_by_psychological_profile(
    psychological_profile="nurturing_caregiver"
)
```

## Testing

Test the emotional system:

```bash
# Run psychological emotional tests
python test_enhanced_psychological_emotions.py

# Test specific components
python -c "
from astra_emotional_fragments.emotional_blender import EnhancedEmotionalBlender
blender = EnhancedEmotionalBlender()
result = blender.blend_emotions_with_psychology('romantic', 'melancholic')
print(f'Test result: {result}')
"
```

## Discord Integration

The emotional system integrates with Discord commands:

```bash
# Test emotion adaptation
!test-emotion "I'm feeling really happy today"

# Blend emotions
!blend-emotions romantic melancholic

# Test prompt injection
!test-prompt-injection "Let's write a romantic scene"
```

## Psychological Analysis

### Emotion Complexity Scoring

The system analyzes emotional complexity:

- **Low Complexity (1-3)**: Simple, single emotions
- **Medium Complexity (4-6)**: Mixed emotions with moderate depth
- **High Complexity (7-10)**: Complex emotional states with multiple layers

### Psychological Readiness

The system tracks psychological readiness for emotional shifts:

- **High Readiness**: Ready for emotional changes
- **Medium Readiness**: Some resistance to change
- **Low Readiness**: Strong resistance to emotional shifts

## Emotional Transitions

### Smooth Transitions

The system creates psychologically realistic transitions:

```python
# Smooth transition from anxious to calm
transition = engine.create_psychologically_smooth_transition(
    from_emotion="anxious",
    to_emotion="calm",
    transition_phrase="I understand your concerns, let me help you feel better"
)
```

### Context-Aware Responses

The system generates context-appropriate emotional responses:

```python
# Context-aware response
response = engine.generate_psychologically_realistic_response(
    user_message="I'm worried about my writing",
    current_context="writing_session",
    emotional_state="supportive"
)
```

## Integration with Multimodal Systems

The emotional system integrates with multimodal generation:

```python
# Generate emotionally-aware voice
voice_result = voice_generator.generate_character_voice(
    text="I understand how you feel",
    character_name="Luna",
    character_personality="nurturing"  # Emotionally-aware personality
)

# Generate emotionally-aware image
image_result = image_generator.generate_character_portrait(
    character_name="Luna",
    description="A caring and understanding AI companion",
    style="nurturing"  # Emotionally-aware style
)
```

## Future Enhancements

Planned improvements:

1. **More Emotional Fragments**: Additional emotional states
2. **Cultural Emotional Models**: Culture-specific emotional understanding
3. **Temporal Emotional Tracking**: Long-term emotional state tracking
4. **Emotional Memory**: Remembering emotional contexts
5. **Emotional Learning**: Learning from emotional interactions
6. **Emotional Prediction**: Predicting emotional needs

## Contributing

To add new emotional fragments:

1. Create a new `.md` file in the directory
2. Define the emotional characteristics
3. Include psychological level mapping
4. Add to the emotional blender system
5. Test with the psychological analysis

## Support

For emotional system support:

1. Check the psychological analysis results
2. Verify emotional fragment loading
3. Test emotional blending combinations
4. Review transition logic
5. Check context detection accuracy

The emotional system is the heart of the AI's personality, enabling realistic, context-aware emotional responses that enhance the writing companion experience. 